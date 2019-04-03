# -*- coding: utf-8 -*-
import pymongo
class MyDataBase():        
    client=pymongo.MongoClient(host='localhost',port=27017)
    db=client.emailDB
    mailCollection=db.mail

    def storeInDb(self,dic):
        self.mailCollection.insert_one(dic)
