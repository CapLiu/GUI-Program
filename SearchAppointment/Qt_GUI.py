# -*- coding=utf-8 -*-
from Searcher import searcher
from requests.exceptions import ConnectionError
from PyQt4 import QtGui,QtCore

class MainWindow(QtGui.QWidget):
    def __init__(self):
        super(MainWindow,self).__init__()
        self.resize(450,260)
        self.setWindowTitle(u'北京市医院挂号查询')
        self._hospital_label=QtGui.QLabel(u'医院：')
        self._consult_label=QtGui.QLabel(u'诊室：')
        self._result_label=QtGui.QLabel(u'结果：')
        self._reconnect_btn=QtGui.QPushButton(u'重新连接')
        self._hospital_list=QtGui.QComboBox(self)
        self._consult_list=QtGui.QComboBox(self)
        self._result_list=QtGui.QListWidget(self)
        self._searcher=searcher()
        self._consult_namelist=[]
        self._error_msg=QtGui.QErrorMessage(self)
        self.setWindowIcon(QtGui.QIcon('red_cross.ico'))
        self.initUI()

    def initUI(self):
        grid=QtGui.QGridLayout()
        grid.addWidget(self._hospital_label,0,0)
        grid.addWidget(self._hospital_list,0,1)
        grid.addWidget(self._consult_label,1,0)
        grid.addWidget(self._consult_list,1,1)
        grid.addWidget(self._result_label,2,0)
        grid.addWidget(self._result_list,2,1)
        grid.addWidget(self._reconnect_btn,0,2)
        self.setLayout(grid)
        #获取hospital_list
        self.get_hospital_list()
        #设置信号和槽
        self._hospital_list.activated.connect(self.on_hospital_list_activated)
        self._consult_list.activated.connect(self.on_consult_list_activated)
        self._reconnect_btn.clicked.connect(self.on_reconnect_clicked)



    def get_hospital_list(self):
        try:
            self._searcher.get_hospital()
        except ConnectionError:
            self._error_msg.setWindowTitle(u'网络错误')
            self._error_msg.showMessage(u'无网络连接，请检查网络！',u'Error')
        hospital_name_list = self._searcher.get_hospital_keys()
        if hospital_name_list == []:
            hospital_name_list = [u'无预约号源']
            self._error_msg.setWindowTitle(u'网络错误')
            self._error_msg.showMessage(u'无法连接至挂号平台，请检查网络！',u'Error')
        for item in hospital_name_list:
            self._hospital_list.addItem(item)

    def get_consult_name(self, url):
        try:
            self._searcher.get_consulting(url)
        except ConnectionError:
            self._error_msg.setWindowTitle(u'网络错误')
            self._error_msg.showMessage(u'无网络连接，请检查网络！',u'Error')
        self._consult_namelist = []
        self._consult_namelist = self._searcher.get_consult_keys()

    @QtCore.pyqtSlot()
    def on_hospital_list_activated(self):
        self._consult_list.clear()
        self._result_list.clear()
        self.get_consult_name(self._searcher.get_value_from_hosp((unicode(self._hospital_list.currentText()))))
        for item in self._consult_namelist:
            self._consult_list.addItem(unicode(item))

    @QtCore.pyqtSlot()
    def on_consult_list_activated(self):
        self._result_list.clear()
        consult_url = self._searcher.get_value_from_consult(unicode(self._consult_list.currentText()))
        try:
            self._searcher.search_appointment(consult_url)
        except ConnectionError:
            self._error_msg.setWindowTitle(u'网络错误')
            self._error_msg.showMessage(u'无网络连接，请检查网络！',u'Error')
        result_list_tmp = self._searcher.get_result_list()
        self._result_list.clear()
        if result_list_tmp:
            for item in result_list_tmp:
                self._result_list.addItem(item)
        else:
            self._result_list.addItem(u'无预约号源')

    @QtCore.pyqtSlot()
    def on_reconnect_clicked(self):
        try:
            self._searcher.get_hospital()
        except ConnectionError:
            self._error_msg.setWindowTitle(u'网络错误')
            self._error_msg.showMessage(u'无网络连接，请检查网络！',u'Error')
        hospital_name_list = self._searcher.get_hospital_keys()
        self._hospital_list.clear()
        self._consult_list.clear()
        for item in hospital_name_list:
            self._hospital_list.addItem(unicode(item))


class my_app:
    def __init__(self):
        self.__mainwindow=MainWindow()

    def run(self):
        self.__mainwindow.show()
