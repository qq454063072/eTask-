#-*- encoding: utf-8 -*-
import imapclient
import email 
from email.mime.text import MIMEText
import re
import config

def parseEmail(mail):
    '''解析一个邮件，返回含有重要信息的List，其中[0]邮件id[1]主题[2]发件人
    [3]时间[4]问题类别[5]严重等级'''
    result=[]
    for messageId,message in mail.items():
        msg=email.message_from_bytes(message[b'BODY[]'])
        subject=str(email.header.make_header(email.header.decode_header(msg['SUBJECT'])))
        mail_from=str(email.header.make_header(email.header.decode_header(msg['FROM'])))
        mail_date=str(email.header.make_header(email.header.decode_header(msg['DATE'])))
        
        #如果不是白名单，只记录主题类信息
        # if(mail_from not in whiteList):
        #     return []
        
        for part in msg.walk():               
            if(not part.is_multipart()):
                charset=re.findall('charset="(.*?)"',str(part),re.S)#可能为空
                # print(charset)
                if(charset):
                    #print("thisPart:")
                    #print(part)
                    text=part.get_payload(decode=True).decode(str(charset[0]))
                    cookText(text)
        result.append(messageId)
        result.append(subject)
        result.append(mail_from)
        result.append(mail_date)
        print(result)
    return result

def cookText(text):
    '''处理一个text,提取重要信息返回为列表[0]问题类型[1]严重等级'''
    
    pass

def makeMsg():
    '''(待完成)制作一个邮件内容，然后返回MIMEText类型的msg'''
    text="Hello!\n这是一条由python发送的邮件。\n用来学习和测试stmp"
    msg=MIMEText(text,_subtype='plain',_charset='utf-8')
    msg['Subject']='邮件发送测试'
    return msg