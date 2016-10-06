# -*- coding=utf-8 -*-
import requests
from bs4 import BeautifulSoup
import re,json
from requests.exceptions import Timeout,ConnectionError,ConnectTimeout


class login_helper:

    def __init__(self,mobileNo="",passwd=""):
        self.__mobileNo=mobileNo
        self.__passwd=passwd
        self.__session=requests.Session()
        self.__logincookies={}
        self._baseurl = 'http://www.bjguahao.gov.cn'
        self.__verifycode=""
        self.islogin=False
        self.__doctor_info=[]
        #预约用信息
        self.__hospitalid=""
        self.__departmentid=""
        self.__dutyDate=""
        self.__dutyCode=1
        self.__dutySourceId=[]
        self.__doctorId=[]
        self.__mk_doctorId=""
        self.__mk_dutySourceId=""
        self.__mk_appoint_url=""
        self.__patientid=""

    def set_info(self,mobileNo,passWord):
        self.__mobileNo=mobileNo
        self.__passwd=passWord

    def reset(self):
        self.__doctor_info = []
        self.__hospitalid = ""
        self.__departmentid = ""
        self.__dutyDate = ""
        self.__dutyCode = 1
        self.__dutySourceId = []
        self.__doctorId = []
        self.__mk_appoint_url = ""
        self.__patientid = ""

    #登录
    def login(self):
        main_url='http://www.bjguahao.gov.cn/index.htm'
        url='http://www.bjguahao.gov.cn/quicklogin.htm'
        headers={
            'Referer':'http://www.bjguahao.gov.cn/index.htm',
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36',
            'X-Requested-With':'XMLHttpRequest'
        }
        paras={'mobileNo':self.__mobileNo,
               'password':self.__passwd,
               'yzm':'',
               'isAjax':'true'
               }
        try:
            wbtext=self.__session.post(url,headers=headers,params=paras)
        except ConnectionError,e:
            raise e
        except Timeout,e:
            raise e
        wbtext.encoding='utf-8'
        json_str=json.loads(wbtext.content)
        status=json_str['msg']
        if status=="OK":
            self.islogin=True
            self.reset()
            return True
        else:
            return False



    #加载登录后页面，url=_appoint_url，appoint_info=result_list[i]
    def load_appoint_page(self,url,appoint_info):
        self.reset()
        getid=re.compile(r'\d{3}-\d{9}')
        ids=getid.search(url).group(0)
        self.__hospitalid=ids.split('-')[0]
        self.__departmentid=ids.split('-')[1]
        self.__dutyDate=appoint_info.split(':')[0].split(' ')[0]
        appoint_time=appoint_info.split(':')[0].split(' ')[1]
        if appoint_time==u'上午':
            self.__dutyCode=1
        else:
            self.__dutyCode=2
        headers={
            'Referer':url,
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest'
        }

        paras={
            'hospitalId':self.__hospitalid,
            'departmentId':self.__departmentid,
            'dutyCode':self.__dutyCode,
            'dutyDate':self.__dutyDate,
            'isAjax':'true'
        }
        loaded_page=self.__session.post('http://www.bjguahao.gov.cn/dpt/partduty.htm',headers=headers,params=paras)
        json_str=json.loads(loaded_page.content,encoding='utf-8')
        tmp_info=json_str['data']
        for item in tmp_info:
            self.__dutySourceId.append(item['dutySourceId'])
            self.__doctorId.append(item['doctorId'])
            doctor_title=item['doctorTitleName']
            doctor_skill=item['skill']
            totalFee=item['totalFee']
            remain_number=item['remainAvailableNumber']
            tmp_doctor_info=doctor_title + ' ' + doctor_skill + '\n' + u'挂号费：' + str(totalFee)
            if remain_number>0:
                self.__doctor_info.append(tmp_doctor_info)
            # self.__dutySourceId=json_str['data'][0]['dutySourceId']
            # self.__doctorId=json_str['data'][0]['doctorId']
            # #显示出的医生信息
            # doctor_title=json_str['data'][0]['doctorTitleName']
            # doctor_skill = json_str['data'][0]['skill']
            # totalFee = json_str['data'][0]['totalFee']
            # self.__doctor_info = doctor_title + ' ' + doctor_skill + '\n' + u'挂号费：' + str(totalFee)

    def get_patientid(self,index):
        doctorId=self.__doctorId[index]
        self.__mk_doctorId=str(doctorId)
        dutySourceId=self.__dutySourceId[index]
        self.__mk_dutySourceId=dutySourceId
        self.__mk_appoint_url=self._baseurl+'/order/confirm/'+str(self.__hospitalid)+'-'+str(self.__departmentid)+'-'+str(doctorId)+'-'+str(dutySourceId)+'.htm'
        #取得patient_id
        wbtext=self.__session.get(self.__mk_appoint_url)
        wbtext.encoding='utf-8'
        soup=BeautifulSoup(wbtext.text,'lxml')
        self.__patientid=soup.select('#Reservation_info > div.Rese_db > dl > dd > p > input[type="radio"]')[0]['value']

    def get_doctor_info(self):
        return self.__doctor_info

    def send_sms_verify(self):
        headers = {
            'Referer': self.__mk_appoint_url,
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest'
        }
        # 发送短信验证码
        result = self.__session.post('http://www.bjguahao.gov.cn/v/sendorder.htm', headers=headers)


    #预约
    def make_appoint(self,hospitalCardId,medicareCardId,reimbursementType,sms_verifycode):
        reimbursementTypeCode=1
        headers={
            'Referer':self.__mk_appoint_url,
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36',
            'X-Requested-With':'XMLHttpRequest'
        }
        params={
            'dutySourceId':self.__mk_dutySourceId,
            'hospitalId':self.__hospitalid,
            'departmentId':self.__departmentid,
            'doctorId':self.__mk_doctorId,
            'patientId':self.__patientid,
            'hospitalCardId':hospitalCardId,#就诊卡
            'medicareCardId':medicareCardId,#医保卡
            'reimbursementType':reimbursementTypeCode,
            'smsVerifyCode':sms_verifycode,
            'isFirstTime':'1',
            'hasPowerHospitalCard':'2',
            'cidType':'1',
            'childrenBirthday':'',
            'childrenGender':'2',
            'isAjax':'true'
        }
        result=self.__session.post('http://www.bjguahao.gov.cn/order/confirm.htm',headers=headers,params=params)
        json_str=json.loads(result.content)
        print result.content
        status=json_str['msg']
        if status=="OK":
            return 0
        elif status==u'短信验证码不能为空！':
            return 1
        elif status==u'短信验证码错误！':
            return 2

    def close_loginer(self):
        self.__session.cookies.clear()
        self.__session.close()





