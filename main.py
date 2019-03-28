#-*- encoding: utf-8 -*-
from emailController import myEmail
import emailParser

mail=myEmail()
mail.imapConnect()
mailList=mail.getUnseen()
for eachmail in mailList:
    emailParser.parseEmail(eachmail[0],eachmail[1])