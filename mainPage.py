#GamingWorld

from flask import *
import Message as mess
import SecurityManage as sm
import DataManage as dm
import LoginSignUp as logSign
import DassboardManage as dassMan
import RazorPayApi as rpa
import TransactionManagement as tm
import BackendManage as bm
import os
import MyUtils as mu

webName='Only 1 rupee'

folderPath='C:/Users/Bipin/Desktop/Gaming-world/static/'

transMan=tm.Transaction()

razor=rpa.Razor()

dataMan=dm.Manage()
dtm=dm.TransactionManage()
dnotf=dm.NotificationManage()
dRes=dm.ResultManage()
dEventMan=dm.EventManage()
dFeedback=dm.FeedbackManage()

winMan=bm.WinManage()
notifMan=bm.NotifManage()
transVerMan=bm.TransVerfManage()


dataSeq=sm.DataSecurity()

hrs=mess.HandleReqRes()
hms=mess.HandleMessage()
hrd=mess.HandleReqDatabase()

def checkUserInSession():
    return 'userName' in session

def pathFinder(paths,basePath=''):
    if basePath=='':
        basePath=folderPath
    dirs=os.listdir(basePath+paths)
    dicts={}
    for i in dirs:
        dicts[i]=paths+i
    return dicts

if __name__=='__main__':
    app=Flask(__name__)
    app.secret_key = '----This is __secret'

    loSi=logSign.LoginSignUp(app)
    dass=dassMan.Dassboard(app)
    app.debug=True
    app.run('0.0.0.0',threaded=True)


'''
razorpay_payment_id=pay_KZ48HUsV1pM0dK
&razorpay_payment_link_id=plink_KZ47mLzbomggoG
&razorpay_payment_link_reference_id=
&razorpay_payment_link_status=paid
&razorpay_signature=59d345dd1c1358deebe67703cb84b9ad5975c0c2167e498159448b16f196fbdc
'''
