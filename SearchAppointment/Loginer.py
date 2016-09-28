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

        #预约用信息
        self.__hospitalid=""
        self.__departmentid=""
        self.__dutyDate=""
        self.__dutyCode=1
        self.__dutySourceId=""
        self.__doctorId=""
        self.__mk_appoint_url=""
        self.__patientid=""

    def set_info(self,mobileNo,passWord):
        self.__mobileNo=mobileNo
        self.__passwd=passWord

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
        wbtext=self.__session.post(url,headers=headers,params=paras)
        wbtext.encoding='utf-8'
        cookie={'JSESSIONID':wbtext.cookies['JSESSIONID'],
                'SESSION_COOKIE':wbtext.cookies['SESSION_COOKIE']
                }
        self.__logincookies=cookie

    #加载登录后页面
    def load_appoint_page(self,url,appoint_info):
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
        self.__dutySourceId=json_str['data'][0]['dutySourceId']
        self.__doctorId=json_str['data'][0]['doctorId']
        self.__mk_appoint_url=self._baseurl+'/order/confirm/'+str(self.__hospitalid)+'-'+str(self.__departmentid)+'-'+str(self.__doctorId)+'-'+str(self.__dutySourceId)+'.htm'
        wbtext=self.__session.get(self.__mk_appoint_url)
        wbtext.encoding='utf-8'
        soup=BeautifulSoup(wbtext.text,'lxml')
        self.__patientid=soup.select('#Reservation_info > div.Rese_db > dl > dd > p > input[type="radio"]')[0]['value']


    def send_sms_verify(self):
        headers = {
            'Referer': self.__mk_appoint_url,
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest'
        }
        # 发送短信验证码
        result = self.__session.post('http://www.bjguahao.gov.cn/v/sendorder.htm', headers=headers)

    def make_appoint(self,reimbursementType,sms_verifycode):
        reimbursementTypeCode=1
        headers={
            'Referer':self.__mk_appoint_url,
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36',
            'X-Requested-With':'XMLHttpRequest'
        }
        params={
            'dutySourceId':self.__dutySourceId,
            'hospitalId':self.__hospitalid,
            'departmentId':self.__departmentid,
            'doctorId':self.__doctorId,
            'patientId':self.__patientid,
            'hospitalCardId':'',
            'medicareCardId':'',
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
        if result.status_code==200:
            return True
        else:
            return False




