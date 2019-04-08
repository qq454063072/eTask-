# -*- encoding: utf-8 -*-
import imapclient
from email.mime.text import MIMEText
import email
import re
from lxml import etree
import config


def parseEmail(mail):
    '''解析一个邮件，返回含有重要信息的List，其中[0]邮件id[1]主题[2]发件人
    [3]时间[4]信息类型(新建问题New,追踪问题Tracking,非白名单用户Not WhiteList,错误格式邮件Error)[5]对应信息'''
    for messageId, message in mail.items():
        result = {}
        msg = email.message_from_bytes(message[b'BODY[]'])
        subject = str(email.header.make_header(
            email.header.decode_header(msg['SUBJECT'])))
        mail_from = str(email.header.make_header(
            email.header.decode_header(msg['FROM'])))
        mail_date = str(email.header.make_header(
            email.header.decode_header(msg['DATE'])))
        result['mail_ID'] = messageId
        result['mail_subject'] = subject
        result['From'] = mail_from
        result['Date'] = mail_date
        # 如果不是白名单，只记录主题类信息
        if(re.findall('<(.*?)>', mail_from)[0] not in config.whiteList):
            result['type'] = 'Error'
            result['msg'] = 'Not WhiteList'
            return result
        # 在白名单中，先找到正文
        text = ''
        for part in msg.walk():
            if(not part.is_multipart()):
                charset = re.findall(
                    'charset="(.*?)"', str(part), re.S)  # 可能为空
                contentType = re.findall(
                    'Content-Type: (.*?);', str(part), re.S)[0]
                # Content-Type: application/octet-stream
                # print(charset)
                if(contentType == 'text/html'):
                    text = part.get_payload(
                        decode=True).decode(str(charset[0]))
                    # print(text)
        if(not text):
            result['type'] = 'Error'
            result['msg'] = '读邮件正文失败'
            return result
        # 查找是否有命令语句
        command = re.findall('【(.*?)】|\[(.*?)\]', subject)
        if(command):
            command = list(command[0])
            command.remove('')
            command = command[0]
            # print(command)

            if(command == config.CommandList.newProblem):
                # 判断是否为新问题命令
                return newProblemSolution(result, text)
            elif(command == config.CommandList.updateProblem):
                # 判断是否为更新任务命令
                return updateProblemSolution(result, text)
            elif(command == config.CommandList.finishProblem):
                # 判断是否为结束任务命令
                return finishProblemSolution(result, text)
            elif(re.match(config.CommandList.trackProblem, command)):
                return trackProblemSolution(result, text)
            else:
                # 命令错误
                result['type'] = 'Error'
                result['msg'] = '未定义的命令'
                return result
        else:
            # 没有命令语句,也许为任务追踪,在正文中找问题id
            return trackProblemSolution(result, text)


def newProblemSolution(result, text):
    '''处理创建一个问题的邮件文本'''
    s = cookText(text)
    if(not re.match(config.newTemplate, s)):
        result['type'] = 'Error'
        result['msg'] = '格式不符合模板!'
        return result
    product = re.findall('产品名称\*】(.*?)【', s)[0][1:]
    qtype = re.findall('问题类型】(.*?)【', s)[0][1:]
    qdangerLv = re.findall('严重程度】(.*?)【', s)[0][1:]
    qfromName = re.findall('反馈人\*】(.*?)【', s)[0][1:]
    qfromPhone = re.findall('联系方式\*】(.*?)【', s)[0][1:]
    qothers = re.findall('备注】(.*?)【', s)[0][1:]
    qintro = re.findall('问题描述\*】(.*?)--end--', s)[0][1:]
    if(product and qintro and qfromName and qfromPhone):
        # 判定是否必填项缺失
        result['type'] = 'New'
        result['msg'] = [product, qtype, qdangerLv,
                         qfromName, qfromPhone, qothers, qintro]
    else:
        result['type'] = 'Error'
        result['msg'] = '创建时必填项缺失'
    return result


def updateProblemSolution(result, text):
    '''处理修改一个问题的邮件文本'''
    result['type'] = 'Update'
    return result


def finishProblemSolution(result, text):
    '''处理完成一个问题的邮件文本'''
    result['type'] = 'Fin'
    return result


def trackProblemSolution(result, text):
    '''处理跟踪一个问题的邮件文本'''
    s = cookText(text)
    if(re.findall('【问题编号(.*?)】', result['mail_subject'])):
        id = re.findall('【问题编号(.*?)】', result['mail_subject'])[0][1:]
    elif(re.findall('【问题编号(.*?)】', s)):
        id = re.findall('【问题编号(.*?)】', s)[0][1:]
    else:
        # 找不到编号
        result['type'] = 'Error'
        result['msg'] = '找不到命令或问题编号'
        return result
    result['type'] = 'Track'
    result['msg'] = id
    return result


def cookText(text):
    '''处理一个text,提取重要信息返回为字符串'''
    RawData = etree.HTML(text).xpath('//text()')
    for i in range(len(RawData)):
        RawData[i] = RawData[i].replace(' ', '')
        RawData[i] = RawData[i].replace('\t', '')
        RawData[i] = RawData[i].replace('\r', '')
        RawData[i] = RawData[i].replace('\xa0', '')
        RawData[i] = RawData[i].replace('\n', '')
        if(re.match('<!--.*?-->', RawData[i], re.S)):
            RawData[i] = ''
    for i in range(RawData.count('')):
        RawData.remove('')
    s = ''
    for each in RawData:
        s = s+each
    # print(s)
    return s


def makeMsg(resultDic):
    '''制作一个邮件内容，然后返回MIMEText类型的msg'''
    # text = "Hello!\n这是一条由python发送的邮件。\n用来学习和测试stmp"
    if (resultDic['Type'] == 'Error'):
        text = 'Error!\n'
        text += resultDic['ErrorMsg']
    elif (resultDic['Type'] == 'New'):
        text = '创建问题成功！\n'
        text += '【问题编号：'+str(resultDic['Qid'])+'】\n请务必牢记，以便后期使用。'
    elif (resultDic['Type'] == 'Track'):
        text = '已将该邮件添加于 【问题编号：'+str(resultDic['Qid'])+'】 下！'
    msg = MIMEText(text, _subtype='plain', _charset='utf-8')
    msg['Subject'] = '邮件发送测试'
    receiver = [re.findall('(.*)<', resultDic['Receiver'])[0], re.findall('<(.*?)>', resultDic['Receiver'])[0]]
    msg['To'] = email.utils.formataddr(receiver)
    return msg
