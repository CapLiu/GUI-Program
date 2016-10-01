# -*- coding=utf-8 -*-
#from GUI import my_app
from Qt_GUI import my_app
from PyQt4 import QtGui
import sys

if __name__=="__main__":
    app=QtGui.QApplication(sys.argv)
    myapp=my_app()
    myapp.run()
    sys.exit(app.exec_())