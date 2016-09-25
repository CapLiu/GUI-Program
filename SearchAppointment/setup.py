# -*- coding=utf-8 -*-
from distutils.core import setup
import py2exe

data_files=[('',[r'red_cross.ico'])]
options={"py2exe":{"compressed": 1, #压缩
                     "optimize": 2,
                     "bundle_files": 1 #所有文件打包成一个exe文件
                     }}
setup(windows=[{'script':'main.py','data_files':data_files,'icon_resources':[(1,'red_cross.ico')]}])
