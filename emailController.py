#-*- encoding: utf-8 -*-
import imapclient
import email 
import smtplib
class myEmail:
    __sendName='eTask'
    __loginEmail=''
    __loginPassword='jolzhtvvtkykcaih'
    __smtp=None
    __smtphost='smtp.qq.com'
    __smtpport='465'
    __imap=None
    __imaphost='imap.qq.com'
    __imapport='993' 

    def imapConnect(self,t_host=__imaphost,t_post=__imapport):
        '''和服务器建立imap连接用于收邮件'''
        self.__imap=imapclient.IMAPClient(host = t_host,port=t_post,ssl=True)
        self.__imap.login(self.__loginEmail,self.__loginPassword)
        print('imap已连接')
    
    def smtpConnect(self,t_host=__smtphost,t_port=__smtpport):
        '''和服务器建立smtp连接用于发邮件'''
        self.__smtp=smtplib.SMTP_SSL(self.__smtphost,self.__smtpport)
        self.__smtp.login(self.__loginEmail,self.__loginPassword)
        print('smtp连接已建立')
    
    def getUnseen(self):
        '''读取已经建立的连接的所有未读邮件,fetch到每一封的邮件内容并以list形式存储并返回该list'''
        self.__imap.select_folder('INBOX')
        mailIdList=self.__imap.search('UNSEEN')
        mailList=[]
        for id in mailIdList:
            mailList.append(self.__imap.fetch(id, ['BODY.PEEK[]']))
            #self.__imap.set_flags(id,b'\\Seen')#将邮件设为已读
        return mailList

    def forwordById(self,id,receiver):
        '''根据每个邮件的id寻找这个邮件，并转发给某个邮箱'''
        pass
    
    def sendTo(self,msg,receiver):
        '''将已经排版完成的信息添加收发人再发送给某个邮箱'''
        msg['From']=email.utils.formataddr([self.__sendName,self.__loginEmail])
        msg['to']=email.utils.formataddr(['User',receiver])
        self.__smtp.sendmail(self.__loginEmail,[receiver],msg.as_string())
        