#!/usr/bin/python3
#coding=utf-8
import urllib3
import json
import datetime as dt
import time
import sys
import logging
import traceback
import random
'''
特别声明:
本程序只有甜糖客户端和server酱的相关的api的访问，请仔细查阅程序安全性。
本程序仅用于测试和学习研究，禁止用于商业用途，不能保证其合法性，准确性，完整性和有效性，请根据情况自行判断.
本脚本的唯一下载地址https://www.right.com.cn/forum/thread-4048219-1-1.html  其它地方下载的可能存在危险，概不负责。
对任何脚本问题概不负责，包括但不限于由任何脚本错误导致的任何损失或损害.
请勿将本程序的任何内容用于商业或非法目的，否则后果自负.

如果任何单位或个人认为本程序可能涉嫌侵犯其权利，则应及时通知并提供身份证明，所有权证明，我们将在收到认证文件后删除相关程序.
任何以任何方式查看此程序的人或直接或间接使用该程序的使用者都应仔细阅读此声明。作者保留随时更改或补充此免责声明的权利。
一旦使用并复制了任何相关程序，则视为您已接受此免责声明.
您使用或者复制了本程序且本人制作的任何脚本，则视为已接受此声明，请仔细阅读
您必须在下载后的24小时内从计算机或手机中完全删除以上内容.
'''
def HandleException( excType, excValue, tb):
	ErrorMessage = traceback.format_exception(excType, excValue, tb)  # 异常信息
	logging.exception('ErrorMessage: %s' % ErrorMessage)  # 将异常信息记录到日志中
	str=""
	for item in ErrorMessage:
		str=str+item
	sendServerJiang("[甜糖星愿]程序错误警报","####程序运行错误，请停用程序，手动领取星愿，并联系程序开发者！-三只松鼠\n```python\nErrorMessage:%s\n```" %str)
	return

sys.excepthook = HandleException #全局错误异常处理！

path=sys.path[0] #脚本所在目录
logging.basicConfig(filename=path + '/sendTTnodeMSG.log',format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s', level=logging.DEBUG)
logging.debug("日志开始")
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
####################以下内容请不要乱动，程序写得很菜，望大佬手下留情#########################################
devices=''
inactivedPromoteScore=0
total=0
accountScore=0
msgTitle="[甜糖星愿]星愿日结详细"
msg="\n"
def sendServerJiang(text,desp):#发送server酱代码
    url="https://sc.ftqq.com/"+sckey+".send"
    header={"Content-Type":"application/x-www-form-urlencoded"}
    body_json="text="+text+"&"+"desp="+desp
    encoded_body=body_json.encode('utf-8')
    http = urllib3.PoolManager()
    response= http.request('POST', url,body=encoded_body,headers=header)
    if response.status!=200:
       print("sendServerJiang方法请求失败，结束程序")
       logging.debug("sendServerJiang方法请求失败，结束程序")
       exit()
    data=response.data.decode('utf-8')
    data=json.loads(data)
    return

def getInitInfo():#甜糖用户初始化信息，可以获取待收取的推广信息数，可以获取账户星星数
    url="http://tiantang.mogencloud.com/web/api/account/message/loading"
    header={"Content-Type":"application/json","authorization":authorization}
    http = urllib3.PoolManager()
    response= http.request('POST', url,headers=header)
    if response.status!=200:
       print("getInitInfo方法请求失败，结束程序")
       logging.debug("getInitInfo方法请求失败，结束程序")
       raise Exception("响应状态码:"+str(response.status)+"\n请求url:"+url+"\n消息:API出现异常，请暂停使用程序！")
    data=response.data.decode('utf-8')
    data=json.loads(data)
    if data['errCode']!=0:
        print("发送推送微信，authorization已经失效")
        sendServerJiang("[甜糖星愿]-Auth失效通知","#### authorization已经失效，请通过手机号码和验证码进行重新生成配置\n \ndocker版：\n```python\ndocker exec -it autottnode /bin/bash -c \"python3 /root/AutomationTTnode/ttnodeConfig.py\" \n```\n源码版：\n```python\npython3 /你的路径/ttnodeConfig.py"+end)
        exit()
    data=data['data']

    return data

def getDevices():#获取当前设备列表，可以获取待收的星星数
    url="http://tiantang.mogencloud.com/api/v1/devices?page=1&type=2&per_page=200"
    header={"Content-Type":"application/json","authorization":authorization}
    http = urllib3.PoolManager()
    response= http.request('GET', url,headers=header)
    if response.status!=200:
        print("getDevices方法请求失败，结束程序")
        logging.debug("getDevices方法请求失败，结束程序")
        raise Exception("响应状态码:"+str(response.status)+"\n请求url:"+url+"\n消息:API出现异常，请暂停使用程序！")
    data=response.data.decode('utf-8')
    data=json.loads(data)
    if data['errCode']!=0:
       raise Exception("响应状态码:"+str(response.status)+"\n请求url:"+url+"\n消息:API可能已经变更，请暂停使用程序！")


    data=data['data']['data']
    if len(data)==0:
        sendServerJiang("[甜糖星愿]请绑定通知","#### 该账号尚未绑定设备，请绑定设备后再运行！\n填写邀请码123463支持作者！\n")
        exit()
    return data



def promote_score_logs(score):#收取推广奖励星星
    global msg
    if score==0:
        msg=msg+"\n [推广奖励]0-🌟\n"
        return
    url="http://tiantang.mogencloud.com/api/v1/promote/score_logs"
    header={"Content-Type":"application/json","authorization":authorization}
    body_json={'score':score}
    encoded_body=json.dumps(body_json).encode('utf-8')
    http = urllib3.PoolManager()
    response= http.request('POST', url,body=encoded_body,headers=header)
    if response.status!=201 and response.status!=200:
       print("promote_score_logs方法请求失败，结束程序")
       logging.debug("promote_score_logs方法请求失败，结束程序")
       raise Exception("响应状态码:"+str(response.status)+"\n请求url:"+url+"\n消息:API出现异常，请暂停使用程序！")
    data=response.data.decode('utf-8')
    data=json.loads(data)

    if data['errCode']!=0:
        msg=msg+"\n [推广奖励]0-🌟(收取异常)\n"
        return
    msg=msg+"\n [推广奖励]"+str(score)+"-🌟\n"
    global total
    total=total+score
    data=data['data']
    #发送微信推送，啥设备，获取了啥星星数
    return

def score_logs(device_id,score,name):#收取设备奖励
    global msg
    if score==0:
        msg=msg+"\n ["+name+"]0-🌟\n"
        return
    url="http://tiantang.mogencloud.com/api/v1/score_logs"
    header={"Content-Type":"application/json","authorization":authorization}
    body_json={'device_id':device_id,'score':score}
    encoded_body=json.dumps(body_json).encode('utf-8')
    http = urllib3.PoolManager()
    response= http.request('POST', url,body=encoded_body,headers=header)
    if response.status!=201 and response.status!=200:
       print("score_logs方法请求失败，结束程序")
       logging.debug("score_logs方法请求失败，结束程序")
       raise Exception("响应状态码:"+str(response.status)+"\n请求url:"+url+"\n消息:API出现异常，请暂停使用程序！")
    data=response.data.decode('utf-8')
    data=json.loads(data)

    if data['errCode']!=0:
        msg=msg+"\n ["+name+"]0-🌟(收取异常)\n"
        return
    msg=msg+"\n ["+name+"]"+str(score)+"-🌟\n"
    global total
    total=total+int(score)
    data=data['data']
    #发送微信推送，啥设备，获取了啥星星数
    return

def sign_in():#签到功能
	url="http://tiantang.mogencloud.com/web/api/account/sign_in"
	header={"Content-Type":"application/json","authorization":authorization}
	http = urllib3.PoolManager()
	response= http.request('POST', url,headers=header)
	if response.status!=201 and response.status!=200:
		print("sign_in方法请求失败，结束程序")
		logging.debug("sign_in方法请求失败，结束程序")
		raise Exception("响应状态码:"+str(response.status)+"\n请求url:"+url+"\n消息:API出现异常，请暂停使用程序！")
	data=response.data.decode('utf-8')
	data=json.loads(data)
	global msg

	if data['errCode']!=0:
		msg=msg+"\n [签到奖励]0-🌟(失败:"+data['msg']+")\n"
		return

	msg=msg+"\n [签到奖励]"+str(data['data'])+"-🌟 \n"
	global total
	total=total+data['data']
	return

    
def readConfig(filePath):#读取配置文件
	try:
		file=open(filePath,"a+",encoding="utf-8",errors="ignore")
		file.seek(0)
		result=file.read()
	finally:
		if file:
			file.close()
			print("文件流已经关闭")

	return result
def withdraw_logs(bean):#支付宝提现
    url="http://tiantang.mogencloud.com/api/v1/withdraw_logs"
    score=bean["score"]
    score=score-score%100
    real_name=bean["real_name"]
    card_id=bean["card_id"]
    bank_name="支付宝"
    sub_bank_name=""
    type="zfb"
    
    if score<1000:
        return "\n####[自动提现]提现失败，星愿数不足1000\n"
    
    body_json="score="+str(score)+"&real_name="+real_name+"&card_id="+card_id+"&bank_name="+bank_name+"&sub_bank_name="+sub_bank_name+"&type="+type
    encoded_body=body_json.encode('utf-8')
    header={"Content-Type":"application/x-www-form-urlencoded;charset=UTF-8","authorization":authorization}
    http = urllib3.PoolManager()
    response= http.request('POST', url,body=encoded_body,headers=header)
    if response.status!=201 and response.status!=200:
        logging.debug("withdraw_logs方法请求失败")
        return "\n####[自动提现]提现失败，请关闭自动提现等待更新并及时查看甜糖客户端app的账目\n"
       
    data=response.data.decode('utf-8')
    data=json.loads(data)

    if data['errCode']!=0:
        print(""+data['msg']+str(score))
        return "\n####[自动提现]提现失败，请关闭自动提现等待更新并及时查看甜糖客户端app的账目\n"

    data=data['data']
    zfbID=data['card_id']
    pre=zfbID[0:4]
    end=zfbID[7:11]
    zfbID=pre+"***"+end
    return "\n####[自动提现]扣除"+str(score)+"-🌟("+zfbID+")\n"
#*********************************main***********************************************************************************
#*********************************读取配置*************************************
config=readConfig(path+"/ttnodeConfig.config")
print("config:"+config)

if len(config)==0:
	print("错误提示ttnodeConfig.config为空，请重新运行ttnodeconfig.py")
	logging.debug("错误提示ttnodeConfig.config为空，请重新运行ttnodeconfig.py")
	exit()

config=eval(config)#转成字典
authorization=config.get("authorization","")
sckey=config.get("sckey","")
week=config.get("week",0)
if len(authorization)==0:
	print("错误提示authorization为空，请重新运行ttnodeconfig.py")
	exit()
if len(sckey)==0:
	print("错误提示sckey为空，请重新运行ttnodeconfig.py")
	exit()
authorization=authorization.strip()
sckey=sckey.strip()
week=int(week)
end="\n```\n***\n注意:以上统计仅供参考，一切请以甜糖客户端APP为准\n填写邀请码123463支持作者！"
#*********************************错峰延时执行*************************************
sleep_time=random.randint(1,300)
print("错峰延时执行"+str(sleep_time)+"秒，请耐心等待")
logging.debug("错峰延时执行"+str(sleep_time)+"秒，请耐心等待")
time.sleep(sleep_time)

#*********************************获取用户信息*************************************
data=getInitInfo()
inactivedPromoteScore=data['inactivedPromoteScore']
accountScore=data['score']

devices=getDevices()#获取设备列表信息
#*********************************获取用户信息*************************************

msg=msg+"\n####[收益详细]：\n```python"
sign_in()#收取签到收益
promote_score_logs(inactivedPromoteScore)#收取推广收益



for device in devices:
    score_logs(device['hardware_id'],device['inactived_score'],device['alias'])#收取设备收益
    time.sleep(1)
#*********************************自动提现*************************************
withdraw=""
now_week=dt.datetime.now().isoweekday()#获取今天是星期几返回1-7
now_week=int(now_week)
week=0
if week==now_week:
    userInfo=getInitInfo()
    zfbList=userInfo['zfbList']#获取支付宝列表
    if len(zfbList)==0:
        withdraw="\n####[自动提现]提现失败，请绑定支付宝账户\n"
    else:
        bean={}
        bean["score"]=userInfo['score']
        bean["real_name"]=zfbList[0]['name']
        bean["card_id"]=zfbList[0]['account']
        withdraw=withdraw_logs(bean)
#*********************************收益统计并发送微信消息*************************************
total_str="\n####[总共收取]"+str(total)+"-🌟\n"
nowdata=getInitInfo()
accountScore=nowdata['score']
nickName="\n####[账户昵称]"+nowdata['nickName']+"\n"
accountScore_str="\n####[账户星愿]"+str(accountScore)+"-🌟\n"


now_time = dt.datetime.now().strftime('%F %T')
now_time_str="\n***\n####[当前时间]"+now_time+"\n"
msg=now_time_str+nickName+accountScore_str+total_str+withdraw+msg+end
sendServerJiang(msgTitle,msg)
print("微信消息已推送。请注意查看。")
title="[甜糖星愿]特别通知"
content="####由于甜糖官方更改提现规则，所以暂时关闭自动提现功能，等待作者更新程序！近期甜糖更新改动较大，如有发现程序出现问题，请及时反馈-三只松鼠"
sendServerJiang(title,content)
exit()
