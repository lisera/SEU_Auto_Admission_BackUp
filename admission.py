# coding: utf-8
# Author：quzard
import json
import re
import time
from datetime import date, timedelta, datetime
from urllib import parse
import execjs
import requests


class Admission(object):
    def __init__(self, uname, pwd, path):
        self.uname = uname
        self.pwd = pwd
        self.path = path
        self.cookie_url = 'http://ehall.seu.edu.cn/qljfwapp3/sys/funauthapp/api/getAppConfig/lwWiseduElectronicPass-5824595920058328.do'
        self.base_addr = 'http://ehall.seu.edu.cn/'
        self.application = self.base_addr + 'qljfwapp3/sys/lwWiseduElectronicPass/modules/application.do'
        self.queryNextDayInschoolCount = self.base_addr + 'qljfwapp3/sys/lwWiseduElectronicPass/modules/application/queryNextDayInschoolCount.do'
        self.validateApply = self.base_addr + 'qljfwapp3/sys/lwWiseduElectronicPass/api/validateApply.do'

        # 申请url
        self.T_APPLY_LIMITE_QUERY = self.base_addr + 'qljfwapp3/sys/lwWiseduElectronicPass/modules/application/T_APPLY_LIMITE_QUERY.do'
        self.applicationSave = self.base_addr + 'qljfwapp3/sys/lwWiseduElectronicPass/modules/application/applicationSave.html?av=30000'
        self.undefined = self.base_addr + 'qljfwapp3/sys/emapcomponent/file/getUploadedAttachment/undefined.do'
        self.hqdqryyqsbxx = self.base_addr + 'qljfwapp3/sys/lwWiseduElectronicPass/modules/application/hqdqryyqsbxx.do'
        self.SEX = self.base_addr + 'qljfwapp3/code/2d7772bc-4fb3-4e2c-a224-6df948cce897/SEX.do'
        self.ID_TYPE = self.base_addr + 'qljfwapp3/code/2d7772bc-4fb3-4e2c-a224-6df948cce897/ID_TYPE.do'
        self.STATUS = self.base_addr + 'qljfwapp3/code/2d7772bc-4fb3-4e2c-a224-6df948cce897/STATUS.do'
        self.hqsqjzsj = self.base_addr + 'qljfwapp3/sys/lwWiseduElectronicPass/modules/application/hqsqjzsj.do'
        self.queryFirstUserTaskToolbar = self.base_addr + 'qljfwapp3/sys/emapflow/definition/queryFirstUserTaskToolbar.do?defKey=lwWiseduElectronicPass.MainFlow'
        # 填写url
        self.COMMON_STATE = self.base_addr + 'qljfwapp3/code/2d7772bc-4fb3-4e2c-a224-6df948cce897/COMMON_STATE.do'
        self.pass_campus = self.base_addr + 'qljfwapp3/code/038e533b-1c26-4572-9320-b8f2efa3f2d1.do'
        self.SQLY = self.base_addr + 'qljfwapp3/code/2d7772bc-4fb3-4e2c-a224-6df948cce897/SQLY.do'
        self.uploadTempFile = self.base_addr + 'qljfwapp3/sys/emapcomponent/file/uploadTempFile.do'

        self.queryNextDayInschoolCount = self.base_addr + 'qljfwapp3/sys/lwWiseduElectronicPass/modules/application/queryNextDayInschoolCount.do'
        self.validateApply = self.base_addr + 'qljfwapp3/sys/lwWiseduElectronicPass/api/validateApply.do'
        # startFlow
        self.startFlow = self.base_addr + 'qljfwapp3/sys/emapflow/tasks/startFlow.do'

    # 登陆
    def login(self):
        login_url = 'https://newids.seu.edu.cn/authserver/login?service=http%3A%2F%2Fehall.seu.edu.cn%2Fqljfwapp3%2Fsys%2FlwWiseduElectronicPass%2Findex.do'
        get_login = self.sess.get(login_url)

        get_login.encoding = 'utf-8'
        lt = re.search('name="lt" value="(.*?)"', get_login.text).group(1)
        salt = re.search('id="pwdDefaultEncryptSalt" value="(.*?)"', get_login.text).group(1)
        execution = re.search('name="execution" value="(.*?)"', get_login.text).group(1)

        f = open(self.path + "/encrypt.js", 'r', encoding='UTF-8')
        line = f.readline()
        js = ''
        while line:
            js = js + line
            line = f.readline()
        ctx = execjs.compile(js)
        password = ctx.call('_ep', self.pwd, salt)

        login_post_url = 'https://newids.seu.edu.cn/authserver/login?service=http%3A%2F%2Fehall.seu.edu.cn%2Fqljfwapp3%2Fsys%2FlwWiseduElectronicPass%2Findex.do'
        personal_info = {'username': self.uname,
                         'password': password,
                         'lt': lt,
                         'dllt': 'userNamePasswordLogin',
                         'execution': execution,
                         '_eventId': 'submit',
                         'rmShown': '1'}
        post_login = self.sess.post(login_post_url, personal_info)
        post_login.encoding = 'utf-8'
        if re.search("deptName", post_login.text):
            self.USER_INFO = re.search('{"deptName":.*}', post_login.text).group()
            self.USER_INFO = json.loads(self.USER_INFO)
            return "登陆成功!"
        else:
            return "登陆失败!"

    # 设置self.header
    def getheader(self):
        get_cookie = self.sess.get(self.cookie_url)
        cookie = requests.utils.dict_from_cookiejar(self.sess.cookies)
        c = ""
        for key, value in cookie.items():
            c += key + "=" + value + "; "
        self.header = {'Referer': 'http://ehall.seu.edu.cn/qljfwapp3/sys/lwWiseduElectronicPass/index.do',
                       'Cookie': c}

    # 获取之前信息
    def get_info(self):
        url = 'http://ehall.seu.edu.cn/qljfwapp3/sys/emapflow/*default/index/queryUserTasks.do'
        self.header['Content-Type'] = 'application/x-www-form-urlencoded;charset=utf-8'
        FormData = {'taskType': 'ALL_TASK', "nodeId": "usertask1", "appName": "lwWiseduElectronicPass",
                    "module": "modules",
                    "page": "application",
                    "action": "getApplicationData",
                    "*order": "-CREATED_AT",
                    "pageSize": 10000,
                    "pageNumber": 1
                    }
        data = parse.urlencode(FormData)

        get_personal_info = self.sess.post(url, data=data,
                                           headers=self.header)
        return get_personal_info
    # 获取之前信息
    def get_info2(self, WID):
        url = 'http://ehall.seu.edu.cn/qljfwapp3/sys/lwWiseduElectronicPass/modules/application/getStuApplicationDatas.do'
        self.header['Content-Type'] = 'application/json; charset=UTF-8'
        FormData = {'WID': WID}
        data = parse.urlencode(FormData)

        get_personal_info = self.sess.post(url, data=data,
                                           headers=self.header)
        return json.loads(get_personal_info.text)['datas']['getStuApplicationDatas']['rows'][0]

    # 撤回
    def callback(self, datas):
        url = 'http://ehall.seu.edu.cn/qljfwapp3/sys/emapflow/tasks/callback.do'
        url2 = 'http://ehall.seu.edu.cn/qljfwapp3/sys/emapflow/definition/queryUserTaskToolbar.do?taskId='
        self.header['Content-Type'] = 'application/x-www-form-urlencoded'
        now_time = datetime.now()
        for data in datas:
            if False or (now_time.strftime("%Y-%m-%d") not in data['IN_SCHOOL_TIME'] and (now_time + timedelta(days=+1)).strftime("%Y-%m-%d") not in data['IN_SCHOOL_TIME']):
                # FLOWSTATUS：1-审核中；2-已驳回；3-已完成；4-草稿；5-已终止；6-已撤回；0-未知状态
                if data["FLOWSTATUSNAME"] == "审核中": 
                    commands = json.loads(self.sess.get(url2 + str(data['TASKID']), headers=self.header).text)['commands']
                    if len(commands) > 0:
                        print("撤回: ", data["IN_SCHOOL_TIME"])
                        post_info = {
                            "formData": {},
                            "sendMessage": "true",
                            "id": "callback",
                            "commandType": "callback",
                            "execute": "do_callback",
                            "name": "撤回",
                            "url": "/sys/emapflow/tasks/callback.do",
                            "buttonType": "warning",
                            "taskId": str(data["TASKID"]),
                            "defKey": str(data["DEFKEY"]),
                            "flowComment":"" 
                        }
                        get_personal_info = self.sess.post(url, data=parse.urlencode(post_info), headers=self.header)  

    # 删除草稿
    def deleteInstance(self, datas):
        url = 'http://ehall.seu.edu.cn/qljfwapp3/sys/emapflow/tasks/deleteInstance.do'
        url2 = 'http://ehall.seu.edu.cn/qljfwapp3/sys/lwWiseduElectronicPass/modules/application/T_ELECTRONIC_PASS_CHECKIN_DELETE.do'
        self.header['Content-Type'] = 'application/x-www-form-urlencoded; charset=UTF-8'
        for data in datas:
            if data["FLOWSTATUSNAME"] == "已撤回" or data["FLOWSTATUSNAME"] == "已驳回":
                print("删除: ", data["IN_SCHOOL_TIME"])                
                post_info = {
                    "processInstanceId": str(data["PROCESSINSTANCEID"]),
                    "isDelete": "true",
                    "appName": "lwWiseduElectronicPass",
                    "defKey": str(data["DEFKEY"])
                }
                info = (self.sess.post(url, data=parse.urlencode(post_info), headers=self.header).text)
                if "true" in info:
                    post_info = {
                        "T_ELECTRONIC_PASS_CHECKIN_DELETE": {"WID":data['WID']}
                    }
                    (self.sess.post(url2, data=parse.urlencode(post_info), headers=self.header).text)


    def askForAdimission(self):
        # 设置header
        self.getheader()

        get_personal_info = self.get_info()
        if get_personal_info.status_code == 200:
            print('获取前一日信息成功!')
        else:
            print("获取信息失败!")
            return "获取信息失败!"
        # 撤回
        self.callback(json.loads(get_personal_info.text)['datas']['queryUserTasks']['rows'])
        # 删除
        get_personal_info = self.get_info()
        self.deleteInstance(json.loads(get_personal_info.text)['datas']['queryUserTasks']['rows'])
        
        get_personal_info = self.get_info()
        raw_personal_info = json.loads(get_personal_info.text)['datas']['queryUserTasks']['rows']
        if len(raw_personal_info) == 0:
            print("之前没有上报!")
            return "之前没有上报!"
        raw_personal_info = raw_personal_info[0]
        now_time = datetime.now()
        if  (now_time + timedelta(days=+1)).strftime("%Y-%m-%d")  in raw_personal_info['IN_SCHOOL_TIME']:
        # if  raw_personal_info["FLOWSTATUSNAME"] == "已完成" and (now_time + timedelta(days=+1)).strftime("%Y-%m-%d")  in raw_personal_info['IN_SCHOOL_TIME']:
            return '已存在通过的申请'
        valid = self.sess.post(self.validateApply, {'userid': self.uname, 'campus': str(raw_personal_info['CAMPUS']), 'beginTime': (now_time + timedelta(days=+1)).strftime("%Y-%m-%d")}).text
        if "false" in valid:
            return "存在通行证" 
        raw_personal_info2 = self.get_info2(raw_personal_info['WID'])

        # 健康码
        if raw_personal_info['YL6'] == None or raw_personal_info['YL6'] == '' or raw_personal_info['YL6'] == "":
            return "上一次入校没有健康码"
        self.scope = raw_personal_info['YL6'][:-1]
        self.filetoken = raw_personal_info['YL6']

        # 通行时间生成
        today_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        print('当前时间：', today_time)

        tomorrow_year = (date.today() + timedelta(days=1)).strftime("%Y")
        tomorrow_month = (date.today() + timedelta(days=1)).strftime("%m")
        tomorrow_day = (date.today() + timedelta(days=1)).strftime("%d")
        tomorrow = str(tomorrow_year) + "-" + str(tomorrow_month) + "-" + str(tomorrow_day)
        tomorrow_begin_time = str(tomorrow_year) + "-" + str(tomorrow_month) + "-" + str(tomorrow_day) + " 06:00:00"
        tomorrow_end_time = str(tomorrow_year) + "-" + str(tomorrow_month) + "-" + str(tomorrow_day) + " 23:00:00"
        print('明天日期：', tomorrow)
        print('通行开始时间：', tomorrow_begin_time)
        print('通行结束时间：', tomorrow_end_time)

        # 申请按键模拟发包
        LIMITE_QUERY = self.sess.post(self.T_APPLY_LIMITE_QUERY, {'USER_ID': self.uname}).text
        if len(json.loads(LIMITE_QUERY)['datas']['T_APPLY_LIMITE_QUERY']['rows']) == 0:
            return "你现在暂时不满足申请条件，若有疑问请联系院系辅导员"

        self.sess.get(self.applicationSave)
        self.sess.post(self.application, {'*json': '1'})
        self.sess.post(self.undefined)
        data = self.sess.post(self.hqdqryyqsbxx, {'USERID': self.uname}).text
        data = json.loads(data)['datas']['hqdqryyqsbxx']['rows']
        if len(data) == 0:
            return "您今天还没有提交每日健康申报，请先在健康申报系统中完成填报，再进行进校预约"
        else:
            if data[0]['CHECKED'] !="YES":
                return "您今天还没有提交每日健康申报，请先在健康申报系统中完成填报，再进行进校预约"
            else:
                if self.USER_INFO['stuZslx'] =="XWZS" and data[0]['IS_YPKYRX']=="0":
            	    return "校医院对您健康信息研判结果为不可进校，如有疑问请联系院系管理员"
                elif self.USER_INFO['stuZslx']=="XWZS" and data[0]['IS_14D_ZNJ'] == "0":
                    return "您在宁未满14天，不允许入校"

        self.sess.post(self.SEX)
        self.sess.post(self.ID_TYPE)
        self.sess.post(self.STATUS)
        self.sess.post(self.hqsqjzsj)
        self.sess.get(self.queryFirstUserTaskToolbar)
        print('申请')

        # 填写过程模拟发包
        self.sess.post(self.COMMON_STATE)
        self.sess.post(self.pass_campus)
        self.sess.post(self.SQLY)
        self.sess.post(self.uploadTempFile,
                       {'scope': self.scope, 'fileToken': self.filetoken, 'size': '0', 'type': 'jpg,jpeg,png',
                        'storeId': 'image',
                        'isSingle': '0', 'fileName': '', 'files[]': '行程卡.PNG'})
        self.submit1 = self.base_addr + 'qljfwapp3/sys/emapcomponent/file/saveAttachment/' + str(
            self.scope) + '/' + str(self.filetoken) + '.do'
        self.submit2 = self.base_addr + 'qljfwapp3/sys/emapcomponent/file/getUploadedAttachment/' + str(
            self.filetoken) + '.do'

        self.sess.post(self.submit1,
                       {'attachmentParam': str({"storeId": "image", "scope": self.scope, "fileToken": self.filetoken})})
        submit_response = self.sess.post(self.submit2)
        self.sess.post(self.queryNextDayInschoolCount, {'DEPT_CODE': raw_personal_info['DEPT_CODE'], 'PERSON_TYPE': raw_personal_info2['STUDENT_TYPE']})
        valid = self.sess.post(self.validateApply, {'userid': self.uname, 'campus': str(raw_personal_info['CAMPUS']), 'beginTime': (now_time + timedelta(days=+1)).strftime("%Y-%m-%d")}).text
        if "false" in valid:
            return "存在通行证"

        datas = {
            "WID": "",
            "CREATED_AT": "",
            "CZR": "",
            "CZZXM": "",
            "CZRQ": "",
            "IS_FLOW": "1",
            "STATUS_DISPLAY": "审核中",
            "STATUS": "2",
            "USER_ID": "",
            "USER_NAME": "",
            "STUDENT_ID": "",
            "GENDER_CODE_DISPLAY": "",
            "GENDER_CODE": "",
            "PHONE_NUMBER": "",
            "MAJOR_CODE": "",
            "MAJOR": "",
            "CLASS": "",
            "ID_TYPE_DISPLAY": "",
            "ID_TYPE": "",
            "ID_NO": "",
            "PERSON_TYPE_DISPLAY": "",
            "PERSON_TYPE": "",
            "DEPT_CODE": "",
            "DEPT_NAME": "",
            "STUDENT_TYPE_DISPLAY": "",
            "STUDENT_TYPE": "",
            "PYFS_DISPLAY": "",
            "XXXS_DISPLAY": "",
            "JTBG_ADDRESS": "",
            "ZS_ADDRESS": "",
            "SFFHFHYQ_DISPLAY": "",
            "SFFHFHYQ": "",
            "NFZHGRFH_DISPLAY": "",
            "NFZHGRFH": "",
            "YL2_DISPLAY": "",
            "YL2": "",
            "DZ_SFYJCS4": "",
            "DZ_SFYJCS1": "",
            "DZ_SFYJCS2": "",
            "DZ_SFYJCS3": "",
            "SFYZNJJJGL": "",
            "DZ_JRSTZK_DISPLAY": "",
            "DZ_JRSTZK": "",
            "SFJBZJHBXLXTJ_DISPLAY": "",
            "SFJBZJHBXLXTJ": "",
            "LXFS": "",
            "YL7": "",
            "CAMPUS_DISPLAY": "",
            "CAMPUS": "",
            "IN_SCHOOL_TIME": "",
            "OFF_SCHOOL_TIME": "",
            "SDLY": "",
            "RESSON_DISPLAY": "",
            "RESSON": "",
            "SQ_REASON_DISPLAY": "",
            "SQ_REASON": "",
            "QTGZ": "",
            "REMARK": "",
            "TIMES": "",
            "YL1": "",
            "YL4": "",
            "YL3_DISPLAY": "",
            "YL3": "",
            "YL6": "",
            "userType": "false",
            "stuType": "true"
        }
        post_info = {
            "WID": "",
            "CREATED_AT": today_time,
            "CZR": "",
            "CZZXM": "",
            "CZRQ": "",
            "IS_FLOW": "1",
            "STATUS_DISPLAY": "审核中",
            "STATUS": "2",
            "userType": "false",
            "stuType": "true",
            "IN_SCHOOL_TIME": tomorrow_begin_time,
            "OFF_SCHOOL_TIME": tomorrow_end_time
        }
        for key, value in datas.items():
            if key in post_info:
                continue
            if key in raw_personal_info:
                if raw_personal_info[key] == 'null' or raw_personal_info[key] == None or raw_personal_info[key] == '' or raw_personal_info[key] == "":
                    post_info[key] = ''
                else:
                    post_info[key] = raw_personal_info[key]
            elif key in raw_personal_info2:
                if raw_personal_info2[key] == 'null' or raw_personal_info2[key] == None or raw_personal_info2[key] == '' or raw_personal_info2[key] == "":
                    post_info[key] = ''
                else:
                    post_info[key] = raw_personal_info2[key]
            else:
                post_info[key] = ''

        print('提交')

        
        startFlow_data = {
            'formData': str(post_info),
            'sendMessage': 'true',
            'id': 'start',
            'commandType': 'start',
            'execute': 'do_start',
            'name': '提交',
            'url': '/sys/emapflow/tasks/startFlow.do',
            'buttonType': 'success',
            'taskId': '',
            'defKey': 'lwWiseduElectronicPass.MainFlow'
        }

        # startFlow
        startFlow_response = self.sess.post(self.startFlow, startFlow_data)
        print(startFlow_response.text)
        if "true" in startFlow_response.text:
            return '入校申请成功'
        else:
            return '入校申请失败'

    def do_report(self):
        self.sess = requests.session()
        if self.login() == "登陆失败!":
            self.sess.close()
            return "登陆失败!"

        msg = self.askForAdimission()
        self.sess.close()
        return msg
