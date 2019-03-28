#-*- encoding: utf-8 -*-
import imapclient
import email 
import re

def parseEmail(id,mail):
    '''解析一个邮件，返回含有重要信息的List，其中[0]邮件id[1]主题[2]发件人
    [3]时间[4]问题类别[5]严重等级'''
    result=[id]
    for messageId,message in mail.items():
        msg=email.message_from_bytes(message[b'BODY[]'])
        # print(msg)
        subject=str(email.header.make_header(email.header.decode_header(msg['SUBJECT'])))
        mail_from=str(email.header.make_header(email.header.decode_header(msg['FROM'])))
        mail_date=str(email.header.make_header(email.header.decode_header(msg['DATE'])))
        for part in msg.walk():               
            if(not part.is_multipart()):
                charset=re.findall('charset="(.*?)"',str(part),re.S)#可能为空
                # print(charset)
                if(charset):
                    print("thisPart:")
                    #print(part)
                    text=part.get_payload(decode=True).decode(str(charset[0]))
                    print(text)
        #待处理html
        result.append(subject)
        result.append(mail_from)
        result.append(mail_date)
        print(result)
    return result