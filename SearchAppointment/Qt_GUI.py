# -*- coding=utf-8 -*-
from Searcher import searcher
from Loginer import login_helper
from requests.exceptions import ConnectionError,Timeout
from PyQt4 import QtGui,QtCore
import threading


is_login=False

#预约信息填写窗口
class fill_info_window(QtGui.QDialog):
    def __init__(self):
        QtGui.QWidget.__init__(self)
        self.resize(320,320)
        self.setWindowTitle(u'预约信息填写')
        self.setWindowIcon(QtGui.QIcon('red_cross.ico'))
        self.patient_card_lbl=QtGui.QLabel(u'就诊卡：')
        self.patient_card_txt=QtGui.QLineEdit(self)
        self.medic_card_lbl=QtGui.QLabel(u'医保卡：')
        self.medic_card_txt=QtGui.QLineEdit(self)
        self.bx_lbl=QtGui.QLabel(u'报销类型：')
        self.bx_combobox=QtGui.QComboBox(self)
        self.sms_verify_lbl=QtGui.QLabel(u'短信验证码：')
        self.sms_verify_txt=QtGui.QLineEdit(self)
        self.mk_btn=QtGui.QPushButton(u'确定')
        self.return_btn=QtGui.QPushButton(u'返回')

        self._msgbox=QtGui.QMessageBox(self)
        self._error_msg=QtGui.QErrorMessage(self)

        self.bx_code={}
        self._loginer=login_helper()
        self.initGUI()

    def set_loginer(self,loginer):
        self._loginer=loginer

    def initGUI(self):
        grid=QtGui.QGridLayout(self)
        grid.addWidget(self.patient_card_lbl,0,0)
        grid.addWidget(self.patient_card_txt,0,1)
        grid.addWidget(self.medic_card_lbl,1,0)
        grid.addWidget(self.medic_card_txt,1,1)
        grid.addWidget(self.bx_lbl,2,0)
        grid.addWidget(self.bx_combobox,2,1)
        grid.addWidget(self.sms_verify_lbl,3,0)
        grid.addWidget(self.sms_verify_txt,3,1)
        grid.addWidget(self.mk_btn,4,0)
        grid.addWidget(self.return_btn,4,1)
        kind_of_bx=[u'医疗保险',u'商业保险',
                    u'公费医疗',u'新农合',
                    u'异地医保',u'红本医疗',
                    u'工伤',u'一老一小',u'超转',
                    u'自费',u'生育险',u'其他'
                    ]
        for i in range(0,len(kind_of_bx)):
            self.bx_code[kind_of_bx[i]]=i
            self.bx_combobox.addItem(kind_of_bx[i])
        self.setLayout(grid)
        self.mk_btn.clicked.connect(self.on_mk_btn_clicked)
        self.return_btn.clicked.connect(self.on_cancel_btn_clicked)


    @QtCore.pyqtSlot()
    def on_mk_btn_clicked(self):
        bx_kind=self.bx_combobox.currentText()
        print bx_kind
        hospitalCardId=str(self.patient_card_txt.text())#就诊卡
        medicareCardId=str(self.medic_card_txt.text())#医保卡
        reimbursementType=self.bx_code[unicode(bx_kind)]
        sms_verify=str(self.sms_verify_txt.text())
        status=self._loginer.make_appoint(hospitalCardId=hospitalCardId,medicareCardId=medicareCardId,reimbursementType=reimbursementType,sms_verifycode=sms_verify)
        if status==0:
            self._msgbox.information(self,u'预约成功！',u'预约成功！')
            self.close()
        elif status==1:
            self._error_msg.showMessage(u'短信验证码不能为空！')
        elif status==2:
            self._error_msg.showMessage(u'短信验证码错误！')


    @QtCore.pyqtSlot()
    def on_cancel_btn_clicked(self):
        self.patient_card_txt.setText("")
        self.medic_card_txt.setText("")
        self.close()





#登录窗口
class login_window(QtGui.QDialog):
    def __init__(self):
        QtGui.QWidget.__init__(self)
        self.resize(320,160)
        self._loginer=login_helper()
        self.setWindowTitle(u'登录')
        self.setWindowIcon(QtGui.QIcon('red_cross.ico'))
        self.mobile_lbl=QtGui.QLabel(u'请输入手机号：')
        self.mobile_txt=QtGui.QLineEdit(self)
        self.passwd_lbl=QtGui.QLabel(u'请输入密码：')
        self.passwd_txt=QtGui.QLineEdit(self)
        self.passwd_txt.setEchoMode(QtGui.QLineEdit.Password)
        self.login_btn=QtGui.QPushButton(u'登录')
        self.cancel_btn=QtGui.QPushButton(u'取消')
        self._error_msg=QtGui.QErrorMessage(self)
        self._msgbox=QtGui.QMessageBox(self)
        self.isLogin=False
        self.initGUI()

    def initGUI(self):
        grid=QtGui.QGridLayout(self)
        grid.addWidget(self.mobile_lbl,0,0)
        grid.addWidget(self.mobile_txt,0,1)
        grid.addWidget(self.passwd_lbl,1,0)
        grid.addWidget(self.passwd_txt,1,1)
        grid.addWidget(self.login_btn,2,0)
        grid.addWidget(self.cancel_btn,2,1)
        self.setLayout(grid)
        #设置信号和槽
        self.login_btn.clicked.connect(self.on_login_btn_clicked)
        self.cancel_btn.clicked.connect(self.on_cancel_btn_clicked)

    def get_login_helper(self):
        return self._loginer

    def get_islogin(self):
        return self.isLogin

    @QtCore.pyqtSlot()
    def on_login_btn_clicked(self):
        global is_login
        mobile_no=str(self.mobile_txt.text())
        passwd=str(self.passwd_txt.text())
        self._loginer.set_info(mobileNo=mobile_no,passWord=passwd)
        try:
            self.isLogin=self._loginer.login()
        except ConnectionError:
            self._error_msg.showMessage(u'无网络连接，请检查网络！')
        except Timeout:
            self._error_msg.showMessage(u'连接超时，请检查网络！')
        if self.isLogin==False:
            self._error_msg.showMessage(u'登录失败，请检查用户名和密码！')
            self.passwd_txt.setText("")
        else:
            self._msgbox.information(self,u'登录成功',u'登录成功')
            self.mobile_txt.setText("")
            self.passwd_txt.setText("")
            is_login=True
        self.close()

    @QtCore.pyqtSlot()
    def on_cancel_btn_clicked(self):
        self.close()

class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.resize(950,300)
        self.setWindowTitle(u'北京市医院挂号查询')
        #登录窗口
        self._login_win=login_window()
        #信息填写窗口
        self._info_win=fill_info_window()
        #工具栏
        self._login = QtGui.QAction(QtGui.QIcon('login.ico'), u'登录', self)
        self._reconnect=QtGui.QAction(QtGui.QIcon('reconnect.ico'),u'重新连接',self)
        self.toolbar=self.addToolBar('Login')
        self.toolbar=self.addToolBar('Reconnect')
        self.toolbar.addAction(self._login)
        self.toolbar.addAction(self._reconnect)
        #窗口组件
        self._hospital_label=QtGui.QLabel(u'医院：')
        self._consult_label=QtGui.QLabel(u'诊室：')
        self._result_label=QtGui.QLabel(u'结果：')
        self._hospital_list=QtGui.QComboBox(self)
        self._consult_list=QtGui.QComboBox(self)
        self._result_list=QtGui.QListWidget(self)
        self._show_doctor_btn=QtGui.QPushButton('>>')
        self._show_doctor_list=QtGui.QListWidget(self)
        #
        self._searcher=searcher()
        self._consult_namelist=[]
        self._loginer=login_helper()
        self._error_msg=QtGui.QErrorMessage(self)
        self.setWindowIcon(QtGui.QIcon('red_cross.ico'))
        #重设布局
        self.wid=QtGui.QWidget(self)
        self.setCentralWidget(self.wid)
        self.initUI()


    def initUI(self):
        grid=QtGui.QGridLayout()
        grid.addWidget(self._hospital_label,0,0)
        grid.addWidget(self._hospital_list,0,1)
        grid.addWidget(self._consult_label,1,0)
        grid.addWidget(self._consult_list,1,1)
        grid.addWidget(self._result_label,2,0)
        grid.addWidget(self._result_list,2,1)
        grid.addWidget(self._show_doctor_btn,2,2)
        grid.addWidget(self._show_doctor_list,2,3)
        self.wid.setLayout(grid)
        self._show_doctor_btn.setFixedWidth(30)
        self._show_doctor_btn.setFixedHeight(80)
        #获取hospital_list
        self.get_hospital_list()
        #设置信号和槽
        self._hospital_list.activated.connect(self.on_hospital_list_activated)
        self._consult_list.activated.connect(self.on_consult_list_activated)
        self._show_doctor_list.itemDoubleClicked.connect(self.on_show_doctor_list_doubleclick)
        self._login.triggered.connect(self.show_login_win)
        self._reconnect.triggered.connect(self.on_reconnect_clicked)
        self._show_doctor_btn.clicked.connect(self.on_show_doctor_btn_clicked)



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

    def get_loginer(self):
        return self._loginer

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

    @QtCore.pyqtSlot()
    def show_login_win(self):
        self._login_win.show()

    @QtCore.pyqtSlot()
    def on_show_doctor_btn_clicked(self):
        global is_login
        if is_login:
            self._show_doctor_list.clear()
            self._loginer=self._login_win.get_login_helper()
            #tmp_login=self._login_win.get_login_helper()
            index=self._result_list.currentRow()
            self._loginer.load_appoint_page(self._searcher.get_appoint_url(),str(self._result_list.item(index).text()))
            doctor_result=self._loginer.get_doctor_info()
            for item in doctor_result:
                self._show_doctor_list.addItem(item)
        else:
            self._error_msg.showMessage(u'请先登录，登录后方可预约。',u'Error')

    @QtCore.pyqtSlot()
    def on_show_doctor_list_doubleclick(self):
        index=self._show_doctor_list.currentRow()
        self._loginer.get_patientid(index)
        self._loginer.send_sms_verify()
        self._info_win.set_loginer(self._loginer)
        self._info_win.show()

class my_app:
    def __init__(self):
        self.__mainwindow=MainWindow()

    def run(self):
        self.__mainwindow.show()
