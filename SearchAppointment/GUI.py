# -*- coding=utf-8 -*-
from Tkinter import *
from Searcher import searcher
import Tkinter
import ttk
import tkMessageBox
from requests.exceptions import Timeout,ConnectionError
class my_app:
    def __init__(self):
        self._app=Tkinter.Tk()
        self._searcher=searcher()
        self._app.geometry('280x260')
        self._app.title(u'北京市医院挂号查询')
        self._app.maxsize(width=280,height=260)
        self._app.iconbitmap('red_cross.ico')
        self._consult_namelist=[]
        self._hospital_list=None
        self._consult_list=ttk.Combobox(master=self._app,state='readonly')
        self._result_list=Listbox()

    def get_consult_name(self,url):
        try:
            self._searcher.get_consulting(url)
        except ConnectionError:
            tkMessageBox.showerror(u'网络问题', u'无网络连接，请检查网络！')
        self._consult_namelist=[]
        self._consult_namelist=self._searcher.get_consult_keys()

    def create_consult_list(self,event):
        self.get_consult_name(self._searcher.get_value_from_hosp(self._hospital_list.get()))
        self._consult_list=None
        self._consult_list=ttk.Combobox(master=self._app,values=self._consult_namelist,state='readonly')
        self._consult_list.bind('<<ComboboxSelected>>', self.get_search_result)
        self._consult_list.current(0)
        self._consult_list.grid(row=1, column=1,sticky=E)

    def get_search_result(self,event):
        consult_url=self._searcher.get_value_from_consult(self._consult_list.get())
        try:
            self._searcher.search_appointment(consult_url)
        except ConnectionError:
            tkMessageBox.showerror(u'网络问题', u'无网络连接，请检查网络！')
        result_list_tmp=self._searcher.get_result_list()
        self._result_list.delete(0,self._result_list.size())
        if result_list_tmp:
            for i in range(0,len(result_list_tmp)):
                self._result_list.insert(self._result_list.size(),result_list_tmp[i])
        else:
            self._result_list.insert(0,u'无预约号源')


    def createwindow(self):
        hospital_label=Label(master=self._app,text=u'医院：',width=3,height=1,padx=8)
        hospital_label.grid(row=0,column=0)
        consult_label=Label(master=self._app,text=u'诊室：',width=3,height=1,padx=8)
        consult_label.grid(row=1,column=0)
        consult_result = Label(master=self._app, text=u'结果：', width=3, height=1, padx=8)
        consult_result.grid(row=2, column=0)
        try:
            self._searcher.get_hospital()
        except ConnectionError:
            tkMessageBox.showerror(u'网络问题',u'无网络连接，请检查网络！')
            exit(1)
        hospital_name_list=self._searcher.get_hospital_keys()
        self._hospital_list=ttk.Combobox(master=self._app,values=hospital_name_list,state='readonly')
        self._hospital_list.current(0)
        self._consult_list.grid(row=1, column=1,sticky=E)
        self._hospital_list.bind('<<ComboboxSelected>>',self.create_consult_list)
        self._hospital_list.grid(row=0,column=1,sticky=E)
        self._result_list=Listbox(master=self._app,width=30,height=10)
        self._result_list.grid(row=2,column=1,sticky=E)


    def run(self):
        self.createwindow()
        self._app.mainloop()