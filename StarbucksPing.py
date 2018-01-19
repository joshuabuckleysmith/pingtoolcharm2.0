import os
from app import tkwindows

os.system("del 1\\*.* /Q/F")
os.system("IF NOT EXIST 1 mkdir 1")
os.system("attrib 1 +h")

tkwindows.buttons()
