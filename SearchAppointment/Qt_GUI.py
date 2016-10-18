# -*- coding=utf-8 -*-
from Searcher import searcher
from Loginer import login_helper
from requests.exceptions import ConnectionError,Timeout
from PyQt4 import QtGui,QtCore
import threading


is_login=False
#个人信息窗口
class info_window(QtGui.QDialog):
    def __init__(self):
        QtGui.QWidget.__init__(self)
        self.resize(320,320)
        self.setWindowTitle(u'个人信息')
        self.setWindowIcon(QtGui.QIcon('info.ico'))
        self._font=QtGui.QFont('黑体',15)
        self.__loginer=login_helper()
        #窗口组件
        self.__name_lbl=QtGui.QLabel(u'姓名：')
        self.__sex_lbl=QtGui.QLabel(u'性别：')
        self.__paper_lbl=QtGui.QLabel(u'证件：')
        self.__mobile_lbl=QtGui.QLabel(u'手机：')
        self.__name_lbl_val = QtGui.QLabel()
        self.__sex_lbl_val = QtGui.QLabel()
        self.__paper_lbl_val = QtGui.QLabel()
        self.__mobile_lbl_val = QtGui.QLabel()
        self.__entry_btn=QtGui.QPushButton(u'确定')
        self.initGUI()

    def initGUI(self):
        grid=QtGui.QGridLayout(self)
        grid.addWidget(self.__name_lbl,0,0)
        grid.addWidget(self.__name_lbl_val,0,1)
        grid.addWidget(self.__sex_lbl,1,0)
        grid.addWidget(self.__sex_lbl_val,1,1)
        grid.addWidget(self.__paper_lbl,2,0)
        grid.addWidget(self.__paper_lbl_val,2,1)
        grid.addWidget(self.__mobile_lbl,3,0)
        grid.addWidget(self.__mobile_lbl_val,3,1)
        grid.addWidget(self.__entry_btn,4,1)
        self.setLayout(grid)
        self.__name_lbl.setFont(self._font)
        self.__name_lbl_val.setFont(self._font)
        self.__sex_lbl.setFont(self._font)
        self.__sex_lbl_val.setFont(self._font)
        self.__paper_lbl.setFont(self._font)
        self.__paper_lbl_val.setFont(self._font)
        self.__mobile_lbl.setFont(self._font)
        self.__mobile_lbl_val.setFont(self._font)
        self.__entry_btn.setFont(self._font)
        self.__entry_btn.clicked.connect(self.on_entry_btn_clicked)

    def set_loginer(self,loginer):
        self.__loginer=loginer

    def set_info(self):
        self.__loginer.person_info()
        tmp_info=self.__loginer.get_person_info()
        self.__name_lbl_val.setText(unicode(tmp_info[0]))
        self.__sex_lbl_val.setText(unicode(tmp_info[1]))
        self.__paper_lbl_val.setText(unicode(tmp_info[2]))
        self.__mobile_lbl_val.setText(unicode(tmp_info[3]))

    @QtCore.pyqtSlot()
    def on_entry_btn_clicked(self):
        self.close()


#预约信息填写窗口
class fill_info_window(QtGui.QDialog):
    def __init__(self):
        QtGui.QWidget.__init__(self)
        self.resize(320,320)
        self.setWindowTitle(u'预约信息填写')
        self.setWindowIcon(QtGui.QIcon('red_cross.ico'))
        self._font=QtGui.QFont('黑体',15)
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
        self._error_msg.setWindowTitle(u'错误')

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
            self.bx_code[kind_of_bx[i]]=i+1
            self.bx_combobox.addItem(kind_of_bx[i])
        self.bx_lbl.setFont(self._font)
        self.bx_combobox.setFont(self._font)
        self.patient_card_lbl.setFont(self._font)
        self.patient_card_txt.setFont(self._font)
        self.medic_card_lbl.setFont(self._font)
        self.medic_card_txt.setFont(self._font)
        self.sms_verify_lbl.setFont(self._font)
        self.sms_verify_txt.setFont(self._font)
        self.mk_btn.setFont(self._font)
        self.return_btn.setFont(self._font)
        self._msgbox.setFont(self._font)
        self._error_msg.setFont(self._font)
        self.setLayout(grid)
        self.mk_btn.clicked.connect(self.on_mk_btn_clicked)
        self.return_btn.clicked.connect(self.on_cancel_btn_clicked)


    @QtCore.pyqtSlot()
    def on_mk_btn_clicked(self):
        bx_kind=self.bx_combobox.currentText()
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
        else:
            self._error_msg.showMessage(u'未知错误！')


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
        self._font=QtGui.QFont('黑体',15)

        self._loginer=login_helper()
        self.setWindowTitle(u'登录')
        self.setWindowIcon(QtGui.QIcon('red_cross.ico'))
        #窗体组件
        self.mobile_lbl=QtGui.QLabel(u'请输入手机号：')
        self.mobile_txt=QtGui.QLineEdit(self)
        self.passwd_lbl=QtGui.QLabel(u'请输入密码：')
        self.passwd_txt=QtGui.QLineEdit(self)
        self.passwd_txt.setEchoMode(QtGui.QLineEdit.Password)
        self.login_btn=QtGui.QPushButton(u'登录')
        self.cancel_btn=QtGui.QPushButton(u'取消')
        self._error_msg=QtGui.QErrorMessage(self)
        self._error_msg.setWindowTitle(u'错误')
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
        self.mobile_lbl.setFont(self._font)
        self.passwd_lbl.setFont(self._font)
        self.mobile_txt.setFont(self._font)
        self.passwd_txt.setFont(self._font)
        self.login_btn.setFont(self._font)
        self.cancel_btn.setFont(self._font)
        self._msgbox.setFont(self._font)
        self._error_msg.setFont(self._font)
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
        self._font=QtGui.QFont('黑体',15)
        #登录窗口
        self._login_win=login_window()
        #信息填写窗口
        self._info_win=fill_info_window()
        #个人信息窗口
        self._person_info=info_window()
        #工具栏
        self._login = QtGui.QAction(QtGui.QIcon('login.ico'), u'登录', self)
        self._reconnect=QtGui.QAction(QtGui.QIcon('reconnect.ico'),u'重新连接',self)
        self._personInfo=QtGui.QAction(QtGui.QIcon('info.ico'),u'个人信息',self)
        self._logout=QtGui.QAction(QtGui.QIcon('logout.ico'),u'退出',self)
        self.toolbar=self.addToolBar('MainToolbar')
        self.toolbar.addAction(self._login)
        self.toolbar.addAction(self._reconnect)
        self.toolbar.addAction(self._personInfo)
        self.toolbar.addAction(self._logout)

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
        self._error_msg.setWindowTitle(u'错误')
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
        self._hospital_list.setEditable(True)
        self._hospital_list.completer().setCompletionMode(QtGui.QCompleter.PopupCompletion)
        self._consult_list.setEditable(True)
        self._consult_list.completer().setCompletionMode(QtGui.QCompleter.PopupCompletion)
        self.wid.setLayout(grid)
        self._show_doctor_btn.setFixedWidth(30)
        self._show_doctor_btn.setFixedHeight(80)
        #设置字体
        self._hospital_label.setFont(self._font)
        self._consult_label.setFont(self._font)
        self._result_label.setFont(self._font)
        self._hospital_list.setFont(self._font)
        self._consult_list.setFont(self._font)
        self._result_list.setFont(self._font)
        self._show_doctor_list.setFont(self._font)
        self._error_msg.setFont(self._font)
        #获取hospital_list
        self.get_hospital_list()
        #设置信号和槽
        self._hospital_list.activated.connect(self.on_hospital_list_activated)
        self._consult_list.activated.connect(self.on_consult_list_activated)
        self._show_doctor_list.itemDoubleClicked.connect(self.on_show_doctor_list_doubleclick)
        self._login.triggered.connect(self.show_login_win)
        self._reconnect.triggered.connect(self.on_reconnect_clicked)
        self._show_doctor_btn.clicked.connect(self.on_show_doctor_btn_clicked)
        self._logout.triggered.connect(self.logout)
        self._personInfo.triggered.connect(self.on_personInfo_click)



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

    def closeEvent(self, *args, **kwargs):
        self._loginer.close_loginer()

    @QtCore.pyqtSlot()
    def on_hospital_list_activated(self):
        self._consult_list.clear()
        self._result_list.clear()
        try:
            self.get_consult_name(self._searcher.get_value_from_hosp((unicode(self._hospital_list.currentText()))))
        except KeyError:
            self._error_msg.showMessage(u'无此医院，请检查医院名称！')
        for item in self._consult_namelist:
            self._consult_list.addItem(unicode(item))

    @QtCore.pyqtSlot()
    def on_consult_list_activated(self):
        self._result_list.clear()
        try:
            consult_url = self._searcher.get_value_from_consult(unicode(self._consult_list.currentText()))
        except KeyError:
            self._error_msg.showMessage(u'无此科室，请检查科室名称！')
            return
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
    def logout(self):
        global is_login
        if is_login:
            self._loginer.close_loginer()
        self.close()

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

    @QtCore.pyqtSlot()
    def on_personInfo_click(self):
        global is_login
        if is_login:
            self._loginer=self._login_win.get_login_helper()
            self._person_info.set_loginer(self._loginer)
            self._person_info.set_info()
            self._person_info.show()
        else:
            self._error_msg.showMessage(u'请先登录！')

class my_app:
    def __init__(self):
        self.__mainwindow=MainWindow()

    def run(self):
        self.__mainwindow.show()
