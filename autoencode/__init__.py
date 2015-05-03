'''
Created on May 2, 2015

@author: McSwindler
'''
import os
import sys
import hashlib
import shutil
import subprocess
import traceback
import psutil
import enzyme
from datetime import datetime
import sqlite3 as lite

FILE_TYPES = ['.mkv']

class AutoEncode:
    def __init__(self, args):
        for directory in args.indir:
            if not os.path.exists(directory):
                raise IOError("No such file or directory", directory)
        if not os.path.exists(args.outdir):
            os.makedirs(args.outdir)
        if args.tempdir and not os.path.exists(args.tempdir):
            os.makedirs(args.tempdir)
            os.makedirs(args.tempdir + os.sep + 'encoding')
        
        self._args = args
        self.file = self.getNewFile()
        if self.file:
            print "New File: %s" %self.file
            if self._args.tempdir:
                print "Copying File..."
                shutil.copy(self.file, self._args.tempdir)
                self.file = self._args.tempdir + os.sep + os.path.basename(self.file)
                
            print "Starting HandBrake"
            outfile = self.handbrake(self.file)
            if outfile:
                self._complete(self.file, outfile)
            else:
                self._fail()
                
            self.file = None
                
        else:
            print "No Files to Process"
            
    def __del__(self):
        self._fail()
        
    def getNewFile(self, index=None):
        if index is None:
            for i in range(len(self._args.indir)):
                f = self.getNewFile(i)
                if f:
                    return f
        elif index in range(len(self._args.indir)):
            indir = self._args.indir[index]
            os.chdir(indir)
            con = self._connect()
            with con:
                files = self._getFiles(con, indir)
                if len(files) > 0:
                    f = files[0]
                    cur = con.cursor()
                    cur.execute('INSERT INTO videos (name, date_started) VALUES (?, ?)', (os.path.basename(f), str(datetime.now())))
                    con.commit()
                    return f
        return None
    
    def _complete(self, infile, outfile):
        if self._args.tempdir:
            print "Copying File..."
            shutil.copy(outfile, self._args.outdir)
        con = self._connect() 
        with con:
            cur = con.cursor()
            cur.execute('UPDATE videos SET date_completed = ? WHERE name = ?', (str(datetime.now()), os.path.basename(infile)))
            con.commit()
            
    def _fail(self):
        if not self.file:
            return
        
        con = self._connect() 
        with con:
            cur = con.cursor()
            cur.execute('DELETE FROM videos WHERE name = ?', (os.path.basename(self.file)))
            con.commit()
                
    def handbrake(self, infile):
        cmd = list(self._args.options)
        outfile = self._outputFile(infile)
        cmd.insert(0, outfile)
        cmd.insert(0, '-o')
        cmd.insert(0, infile)
        cmd.insert(0, '-i')
        cmd.insert(0, self._args.handbrake)
        process = subprocess.Popen(cmd, shell=True)
        p = psutil.Process(process.pid)
        p.nice(psutil.HIGH_PRIORITY_CLASS)
        process.wait()
        if process.returncode > 0:
            return None
        else:
            return outfile
        
    def _outputFile(self, infile):
        filename, ext = os.path.splitext(os.path.basename(infile));
        if ext == '.mkv':
            with open(infile, 'rb') as f:
                mkv = enzyme.MKV(f)
                if mkv.info.title:
                    filename = mkv.info.title
                    
        filename =  filename + '.mkv'
        if self._args.tempdir:
            return self._args.tempdir + os.sep + 'encoding' + os.sep + filename
        else:
            return self._args.outdir + os.sep + filename
    
    def _getFiles(self, con, indir):
        flist = list()
        dbFiles = self._getFilesFromDb(con)
        for subdir, dirs, files in os.walk(indir):
            if subdir == self._args.outdir or subdir == self._args.tempdir:
                continue
            for f in files:
                f = os.path.join(subdir, f)
                name = os.path.basename(f)
                ext = os.path.splitext(name)[1]
                if ext not in FILE_TYPES or name in dbFiles:
                    continue
                try:
                    open(f)
                    flist.append(f)
                except IOError, e:
                    print e
        return flist
    
    def _getFilesFromDb(self, con):
        files = list()
        cur = con.cursor()
        cur.execute('SELECT * FROM videos WHERE date_started OR date_completed')
        for row in cur.fetchall():
            files.append(row[0])
        return files           
                    
    def _connect(self):
        try:
            con = lite.connect('autoencode.db')
            cur = con.cursor()
            cur.execute("CREATE TABLE IF NOT EXISTS videos(name TEXT, date_started TEXT, date_completed TEXT)")
        except lite.Error:
            print traceback.format_exc()
            if con:
                con.close()
        return con       