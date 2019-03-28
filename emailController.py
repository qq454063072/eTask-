#-*- encoding: utf-8 -*-
import imapclient
import email 
class myEmail:
    __loginEmail='454063072@qq.com'
    __loginPassword='jolzhtvvtkykcaih'
    __smtp=None
    __smtphost=''
    __smtpport=''
    __imap=None
    __imaphost='imap.qq.com'
    __imapport='993' 

    def imapConnect(self,t_host=__imaphost,t_post=__imapport):
        '''和服务器建立imap连接用于收邮件,返回一个建立完成的imapClient'''
        self.__imap=imapclient.IMAPClient(host = t_host,port=t_post,ssl=True)
        self.__imap.login(self.__loginEmail,self.__loginPassword)
        print('imap已连接')
    
    def smtpConnect(self,t_host=__smtphost,t_port=__smtpport):
        '''和服务器建立smtp连接用于发邮件'''
        pass
    
    def getUnseen(self):
        '''读取已经建立的连接的所有未读邮件,返回一个list，list中每个元素为一个二元list,[0]是邮件id，[1]是fetch到的内容'''
        self.__imap.select_folder('INBOX')
        mailIdList=self.__imap.search('UNSEEN')
        mailList=[]
        for id in mailIdList:
            mailList.append([id,self.__imap.fetch(id, ['BODY.PEEK[]'])])
            #self.__imap.set_flags(id,b'\\Seen')#将邮件设为已读
        return mailList

    def forwordById(self,id,receiver):
        '''根据每个邮件的id寻找这个邮件，并转发给某个邮箱'''
        pass
    
    def sendTo(self,mail,receiver):
        '''将已经排版完成的邮件发送给某个邮箱'''
        pass

    