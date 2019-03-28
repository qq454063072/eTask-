#-*- encoding: utf-8 -*-
import imapclient
import email 

def parseEmail(id,mail):
    '''解析一个邮件，返回含有重要信息的List，其中[0]邮件id[1]主题[2]发件人[3]时间[4]问题类别[5]严重等级'''
    result=[id]
    for messageId,message in mail.items():
        e=email.message_from_bytes(message[b'BODY[]'])
        subject=email.header.make_header(email.header.decode_header(e['SUBJECT']))
        mail_from=email.header.make_header(email.header.decode_header(e['FROM']))
        mail_date=email.header.make_header(email.header.decode_header(e['DATE']))
        # print(message)
        print('Subject: ',subject)
        print('From: ',mail_from)
        print('Date: ',mail_date)
        #maintype = e.get_content_maintype()
        #mail_content=''
        # if(maintype == 'multipart'):
        #     for part in e.get_payload():
        #         if(part.get_content_maintype() == 'text'):
        #             mail_content = part.get_payload(decode=True).strip().decode('base64')
        # elif(maintype == 'text'):
        #     mail_content = e.get_payload(decode=True).strip().decode('base64')
        result.append(subject)
        result.append(mail_from)
        result.append(mail_date)
        print(result)
    return result