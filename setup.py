#from distutils.core import setup
#import py2exe

from distutils.core import setup
import py2exe, sys, os

sys.argv.append('py2exe')

setup(
    options = {'py2exe': {'bundle_files': 2, 'compressed': True}},
    windows = [{'script': "StarbucksPing.py"}],
    zipfile = None,
)



#setup(console=['StarbucksPing.py'])
