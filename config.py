import re
whiteList = (

)


class CommandList():
    newProblem = '创建问题'
    updateProblem = '修改问题'
    finishProblem = '结束问题'
    trackProblem = '问题编号(.+?)'


newTemplate = '【产品名称\*】(.+?)【问题类型】(.+?)【严重程度】(.+?)【反馈人\*】(.+?)【联系方式\*】(.+?)【备注】(.+?)【问题描述\*】(.+?)--end--'
updateTemplate = ''
finTemplate = ''
