#-*- encoding: utf-8 -*-
from emailController import myEmail
import emailParser
import dbController
import email

db=dbController.MyDataBase()
mail=myEmail()
mail.imapConnect()
mailList=mail.getUnseen()
for eachmail in mailList:
    tempdata=emailParser.parseEmail(eachmail)
    print(tempdata)
    db.storeInDb(tempdata)
# mail.smtpConnect()
# msg=emailParser.makeMsg()
