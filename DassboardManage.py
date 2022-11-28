import mainPage as mp
import time
from flask import *


class Dassboard:

    def __init__(self,app):
        self.amount=1
        self.setupUrl(app)

        #Static profile paths
        self.viewProfilePath='/dassboard/viewProfile/'
        self.notificationPath='/dassboard/notifications/'
        self.prevTransactionPath='/dassboard/prevTransaction/'
        self.viewResultPath='/dassboard/viewResult/'
        self.payEventPath='/dassboard/payEvent/'

    def setupUrl(self,app):
        app.add_url_rule('/dassboard/viewProfile','ViewProfile',self.viewProfilePage)
        app.add_url_rule('/dassboard/payEvent/<eventId>','PayTodaysEvent',self.payEventPage)
        app.add_url_rule('/dassboard/prevTransaction','PrevTransaction',self.prevTransactionPage)
        app.add_url_rule('/dassboard/payEventNow/<eventId>','PayNow',self.payEventNowPage)
        app.add_url_rule('/dassboard/paymentSuccess','PaymentSuccess',self.paymentSuccessPage)
        app.add_url_rule('/dassboard/viewResult','ViewResult',self.viewResultPage)
        app.add_url_rule('/dassboard/viewResult/<eventId>','ViewResultEventId',self.viewResultEventIdPage)
        app.add_url_rule('/dassboard/notification','Notification',self.notificationPage)
        app.add_url_rule('/dassboard/eventHistory','EventHistory',self.eventHistoryPage)
        app.add_url_rule('/dassboard/serverTransaction','ServerTransaction',self.serverTransactionPage)

    def render_template(self,temp,**context):

        if 'logType' in context:
            return render_template(temp,**context)
        else:
            return render_template(temp,logType=None,**context)

    def viewProfilePage(self):
        dataF=mp.pathFinder(self.viewProfilePath)

        cond=mp.checkUserInSession()
        if cond:
            userName=session['userName']

            data=mp.dataMan.getUserDictProfile(userName)


            return self.render_template('/dassboard/viewProfile.html',dataF=dataF,data=data)
            #return self.render_template('/testing.html',data=data)

        else:
            return redirect('/login')

    def prevTransactionPage(self):

        dataF=mp.pathFinder(self.prevTransactionPath)
        cond=mp.checkUserInSession()
        if cond:
            userName=session['userName']
            data=mp.transMan.getStructPrevTrans(userName)
            cols=['Event Id','Payment Link Id','Payment Id','Amount','Status','Time']
            #[event_id,p_link,amount,status,paid_time]
            if data is None:
                data=0
                length=0

            else:
                length=len(data)

            return self.render_template('/dassboard/prevTransaction.html',dataF=dataF,cols=cols,data=data,length=length)
        else:
            return redirect('/login')

    def eventHistoryPage(self):
        cond=mp.checkUserInSession()
        dataF=mp.pathFinder(self.viewProfilePath)

        if cond:
            cols=['Event Id','Event Name','Amount','Created On','Expired On','Participants','Status','Result Time','Open Link']
            allEvent,eventInfo=mp.dEventMan.getStructEventHistoryV2()
            length=0
            if allEvent is not None:
                length=len(allEvent)

            return self.render_template('/dassboard/eventHistory.html',dataF=dataF,cols=cols,allEvent=allEvent,eventInfo=eventInfo,length=length)

        else:
            redirect('/login')

    def serverTransactionPage(self):
        cond=mp.checkUserInSession()
        dataF=mp.pathFinder(self.viewProfilePath)

        if cond:
            return self.render_template('/dassboard/serverTransaction.html',dataF=dataF)
        else:
            redirect('/login')

    def payEventPage(self,eventId):

        dataF=mp.pathFinder(self.payEventPath)
        cond=mp.checkUserInSession()
        condEvent=mp.dEventMan.checkEventIdExist(eventId)

        if cond:
            userName=session['userName']

            trans=mp.transMan.checkUserEventsPaymentEligibilty(userName,eventId)
            condAliveEvent=mp.dRes.checkEventExist(eventId)
            crrTie=time.time()

            if condAliveEvent:
                data="Event Expired ...."
                dataEvent=mp.dEventMan.fetchEventDetails(eventId)

                dataEvent['creTime']=time.ctime(dataEvent['creTime'])
                dataEvent['expTime']=time.ctime(dataEvent['expTime'])


                partEvent=mp.dEventMan.getPaidUserInEvent(eventId)
                return self.render_template('/dassboard/payEvent.html',dataF=dataF,dataEvent=dataEvent,partEvent=partEvent,status_msg=data,trans=trans,eventIdExist=False)

            else:
                if condEvent:
                    dataEvent=mp.dEventMan.fetchEventDetails(eventId)

                    dataEvent['creTime']=time.ctime(dataEvent['creTime'])
                    dataEvent['expTime']=time.ctime(dataEvent['expTime'])


                    partEvent=mp.dEventMan.getPaidUserInEvent(eventId)

                    if trans==None or trans ==-2 or trans ==-1:
                        data=''
                    elif trans==0:
                        data='Your payment link is already created ... '
                    elif trans==1:
                        data='You have already paid for todays event'
                    else:
                        data='Some error occured.. Try creating new payment link'

                    return self.render_template('/dassboard/payEvent.html',dataF=dataF,status_msg=data,trans=trans,partEvent=partEvent,dataEvent=dataEvent,eventId=eventId,eventIdExist=True)

                else:
                    data="Event Id ({0}) don't exist".format(eventId)
                    return self.render_template('/dassboard/dassboardError.html',dataF=dataF,status_msg=data,trans=trans,eventIdExist=False)

        else:
            return redirect('/login')

    def payEventNowPage(self,eventId):
        cond=mp.checkUserInSession()
        dataF=mp.pathFinder(self.viewProfilePath)
        condEvent=mp.dEventMan.checkEventIdExist(eventId)

        if cond:

            if condEvent:
                crrTime=time.time()
                condEventExp=mp.dEventMan.checkEventExpiry(crrTime,eventId)

                if condEventExp:
                    data='Event is already expired \n Particpate in another event.'
                    return self.render_template('/dassboard/dassboardError.html',dataF=dataF,status_msg=data)

                else:


                    #if condEventExp expired then it must return to expired page link

                    userName=session['userName']

                    trans=mp.transMan.checkUserEventsPaymentEligibilty(userName,eventId)
                    if trans==None or trans ==-2 or trans ==-1:
                        data=''
                        xtime=time.time()
                        amount=mp.dEventMan.getEventAmount(eventId)
                        xdata=mp.dataMan.getUserDictProfile(userName)
                        xr=mp.razor.createPaymentLink(amount,xdata['user_name'],xdata['userEmail'],xdata['userMobNo'])
                        mp.dtm.insertCreatedUserTrans(userName,eventId,xr['id'],amount,xr['status'],xtime)
                        return redirect(xr['short_url'])
                    elif trans==0:

                        data='Your payment link is already created ... '
                        p_link=mp.transMan.fetchEventsUCTrans(userName,eventId)[2]
                        link=mp.razor.fetchPaymentLinkUrl(p_link)

                        return redirect(link)

                    elif trans==1:
                        return redirect('/dassboard')


                    else:
                        print("DassboardManage.py payment problem ----8888888888888***********")
                        return redirect('/')
            else:
                data="Event don't Exist."
                return self.render_template('/dassboard/dassboardError.html',dataF=dataF,status_msg=data)


        else:
            return redirect('/login')

    def paymentSuccessPage(self):
        dataF=mp.pathFinder(self.prevTransactionPath)
        cond=mp.checkUserInSession()
        if cond:
            userName=session['userName']
            rPayId=request.args.get('razorpay_payment_id')
            if rPayId ==None:

                return redirect('/dassboard')
            else:
                rPayLId=request.args.get('razorpay_payment_link_id')
                rPayLStatus=request.args.get('razorpay_payment_link_status')
                dicD={'rPayId':rPayId,'rPayLId':rPayLId,'rPayLStatus':rPayLStatus}
                amount=mp.razor.fetchPaymentByLinkId(rPayLId)['amount']
                amount=int(int(amount)/100)
                #condLink=mp.dtm.checkPLinkInUserTrans(rPayLId)
                condULink=mp.dtm.checkUserPLink(userName,rPayLId)
                if condULink:

                    getDataStatus=mp.dtm.getUserTransStatus(userName,rPayLId)
                    dataAll=mp.razor.fetchPaymentByLinkId(rPayLId)
                    realStatus=dataAll['status']
                    t1=dataAll['updated_at']
                    if realStatus==getDataStatus:
                        pass
                    else:
                        if realStatus=='paid' or realStatus=='expired':
                            data=mp.razor.fetchPaymentByLinkId(rPayLId)
                            if data['payments'] is not None:
                                payId=data['payments'][0]['payment_id']
                                mp.dtm.updateUserTransPayId(userName,rPayLId,payId)

                            mp.dtm.updateUserTransStatus(userName,rPayLId,realStatus)
                            t1=time.time()
                            mp.dtm.updateUserTransPaidTime(userName,rPayLId,t1)

                        else:
                            pass
                    return self.render_template('/dassboard/paymentSuccess.html',dataF=dataF,payData=dicD)



                else:

                    return redirect('/dassboard')


        else:
            return redirect('/login')

    def viewResultPage(self):
        dataF=mp.pathFinder(self.viewResultPath)
        data=mp.dRes.getResultTypeInfo()

        xdata=None
        cols=['Event ID','Time','Open Link']
        if data is None:
            length=0
            xlen=0
        else:

            length=len(data)
            xdata=[]

            for i in data:

                url='/dassboard/viewResult/'+i[0]
                xdata.append(i+[url])
            if xdata !=[]:
                xlen=len(xdata[0])
            else:
                xlen=0



        return self.render_template('/dassboard/viewResult.html',dataF=dataF,xlen=xlen,xdata=xdata,length=length,cols=cols)

    def viewResultEventIdPage(self,eventId):

        dataF=mp.pathFinder(self.viewResultPath)
        cond=mp.dRes.checkEventExist(eventId)
        xlen=0

        if cond:
            xdata,timeData=mp.dRes.getStructDataByEventId(eventId)
            cols=['Name','Email','Rank','Status']
            if xdata is not None:
                xlen=len(xdata)
            for i in xdata:
                print(i)
            return self.render_template('/dassboard/viewResultIn.html',dataF=dataF,xlen=xlen,cols=cols ,eventId=eventId,xdata=xdata,timeData=timeData)
        else:

            return self.render_template('/dassboard/viewResultIn.html',dataF=dataF,xlen=xlen ,eventId=eventId,data=None)

    def notificationPage(self):
        dataF=mp.pathFinder(self.notificationPath)

        cond=mp.checkUserInSession()
        if cond:
            #cols=['Notification','notifId','Time']
            userName=session['userName']
            notif=mp.dnotf.fetchNotification(userName)

            xlen=len(notif)



            return self.render_template('/dassboard/notification.html',dataF=dataF,xlen=xlen,data=notif)
        else:
            return redirect('/login')
