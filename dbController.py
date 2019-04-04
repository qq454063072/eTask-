# -*- coding: utf-8 -*-
import pymongo
class MyDataBase():        
    client=pymongo.MongoClient(host='localhost',port=27017)
    db=client.emailDB
    mailCollection=db.mail
    questionCollection=db.question
    def storeInDb(self,dic):
        #一定记得去重复存储
        self.mailCollection.insert_one(dic)

        #如果type是new，在question表里建立新问题

        #如果是track，在question表里
        #1.如果问题不存在，报错
        #2.如果存在，在表中追加邮件id

