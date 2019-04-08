# -*- encoding: utf-8 -*-
from emailController import myEmail
import emailParser
import dbController

db = dbController.MyDataBase()
mail = myEmail()
mail.imapConnect()
mailList = mail.getUnseen()
for eachmail in mailList:
    tempdata = emailParser.parseEmail(eachmail)
    print(tempdata)
    stroeResult = db.storeInDb(tempdata)
    mail.smtpConnect()
    msg = emailParser.makeMsg(stroeResult)
    mail.sendTo(msg)
