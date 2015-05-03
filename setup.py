from setuptools import setup, find_packages
from codecs import open


setup(
    name='autoencode',
    version='0.1',
    description='Automatically encode files using handbrake',
    long_description='Visit GitHub for more information: https://github.com/McSwindler/python-autoencode',
    url='https://github.com/McSwindler/python-autoencode',
    author='McSwindler',
    author_email='wilingua@gmail.com',
    license='MIT',

    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    keywords='handbrake makemkv encode',
    packages=["autoencode"],
    install_requires=["psutil", "enzyme"],
)
