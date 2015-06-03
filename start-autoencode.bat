@ECHO OFF
python autoencode.py -i "Z:\Staging\MKV" -o Z:\Staging\Fetch\Movie 
rem -O " -f mkv --decomb --strict-anamorphic -e x264 -q 20 -a 1 -E copy -6 auto -R Auto -B auto -D 0.0 -m -x ref=2:bframes=2:subq=6:mixed-refs=0:weightb=0:8x8dct=0:trellis=0 --verbose=1 -s 1 -N eng --native-dub"
rem -f mkv --detelecine --decomb --loose-anamorphic -e x264 -q 20 -a 1 -E copy -6 auto -R Auto -B auto -D 0.0 -m -x b-adapt=2:rc-lookahead=50 --verbose=1 -s 1

