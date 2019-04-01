#-*- encoding: utf-8 -*-
from emailController import myEmail
import emailParser
import email

mail=myEmail()
mail.imapConnect()
mailList=mail.getUnseen()
for eachmail in mailList:
    emailParser.parseEmail(eachmail)
# mail.smtpConnect()
# msg=emailParser.makeMsg()
# mail.sendTo(msg,'454063072@qq.com')
