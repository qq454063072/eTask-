# -*- coding: utf-8 -*-
import pymongo
import re
from datetime import datetime


class MyDataBase():
    client = pymongo.MongoClient(host='localhost', port=27017)
    db = client.emailDB
    mailCollection = db.mail
    questionCollection = db.question

    def makeQid(self, Date):
        # 将其转换为时间数组
        Date = re.findall(', (.*?) \+0', Date)[0]
        dt = datetime.strptime(Date, '%d %b %Y %H:%M:%S')
        index = self.questionCollection.find().count()+1
        Qid = dt.year*100000+dt.month*1000+index
        # print(Qid)
        return Qid

    def storeInDb(self, dic):
        # 一定记得去重复存储
        storeResult = {'Receiver': dic['From']}
        # self.mailCollection.update({'mail_ID':dic['mail_ID']},{'$set':dic},upsert=True)
        if(self.mailCollection.find_one({'mail_ID': int(dic['mail_ID'])})):
            storeResult['Type'] = 'Error'
            storeResult['ErrorMsg'] = '该邮件已经解析完成，请勿重新解析'
            return storeResult
        self.mailCollection.insert_one(dic)
        # self.mailCollection.insert_one(dic)
        # 如果type是new，在question表里建立新问题
        if(dic['type'] == 'New'):
            Qid = self.makeQid(dic['Date'])
            storeResult['Type'] = 'New'
            storeResult['Qid'] = Qid
            newTask = {
                'Qid': Qid,
                'Product_Name': dic['msg'][0],
                'Question_Type': dic['msg'][1],
                'Danger_Level': dic['msg'][2],
                'From_Name': dic['msg'][3],
                'From_Phone': dic['msg'][4],
                'Remarks': dic['msg'][5],
                'Question_Intro': dic['msg'][6],
                'Related_Mails': [dic['mail_ID']]}
            self.questionCollection.insert_one(newTask)
        # 如果是track，在question表里
        # 1.如果问题不存在，报错
        # 2.如果存在，在表中追加邮件id
        elif(dic['type'] == 'Track'):
            thisQ = self.questionCollection.find_one({'Qid': int(dic['msg'])})
            if(not thisQ):
                storeResult['Type'] = 'Error'
                storeResult['ErrorMsg'] = '数据库中没有问题编号，请重新检查或创建问题'
            else:
                thisQ['Related_Mails'].append(dic['mail_ID'])
                self.questionCollection.update_one(
                    {'Qid': int(dic['msg'])}, {'$set': thisQ})
                storeResult['Type'] = 'Track'
                storeResult['Qid'] = dic['msg']
        # 或者回报错邮件
        elif(dic['type'] == 'Error'):
            storeResult['Type'] = 'Error'
            storeResult['ErrorMsg'] = dic['msg']

        return storeResult
