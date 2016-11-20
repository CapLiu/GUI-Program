# -*- coding=utf-8 -*-
import sqlite3,os,time,base64

class db_helper:
    def __init__(self):
        self.__basename='usual_user.db'
        self.__basepath=os.path.dirname(__file__)
        self.__db_path=os.path.join(self.__basepath,self.__basename)
        #建立表
        conn=sqlite3.connect(self.__db_path)
        create_sql='''
        CREATE TABLE SA_usr (id nchar(20) unique NOT NULL,
                             mobile nchar(20) unique NOT NULL,
                             pwd nchar(20) NOT NULL,
                             comment
                             )
        '''
        try:
            conn.execute(create_sql)
            conn.commit()
        except sqlite3.OperationalError:
            pass
        finally:
            conn.close()

    #添加用户
    def create_user(self,usrname,password,comment=""):
        if usrname == "" or password == "":
            return False
        conn = sqlite3.connect(self.__db_path)
        cur = conn.cursor()
        sql_statement = r'insert into SA_usr values (?,?,?,?)'
        try:
            cur.execute(sql_statement, (str(time.time()), str(usrname), str(password),unicode(comment)))
            conn.commit()
        except sqlite3.OperationalError,e:
            return e
        except sqlite3.IntegrityError,e:
            print e.message
            return e
        finally:
            cur.close()
            conn.close()
        return True

    #获取用户
    def get_usr(self,mobile_no):
        conn=sqlite3.connect(self.__db_path)
        cur=conn.cursor()
        try:
            cur.execute(r'select mobile,pwd from SA_usr where mobile=?',(str(mobile_no),))
            result=cur.fetchone()
        except sqlite3.OperationalError:
            return False
        finally:
            cur.close()
            conn.close()
        return (result[0],result[1])

    #获取用户名单
    def get_user_list(self):
        conn=sqlite3.connect(self.__db_path)
        cur=conn.cursor()
        try:
            cur.execute(r'select mobile from SA_usr')
            result = cur.fetchall()
        except sqlite3.OperationalError:
            return False
        finally:
            cur.close()
            conn.close()
        return result



