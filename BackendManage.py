import mainPage as mp
import time
import threading

#Winner Selector Algorithmss
class WinManage:

    def __init__(self):
        #Winner Selector
        pass

    def genAllUserNotification(self,t1):
        dateData=time.ctime(t1)
        notif='The result of '+dateData+' is declayerd.'

        return notif

    def genUserNotification(self,status,t1):
        dateData=time.ctime(t1)
        if status==1:
            notif='Congraculation !! You won the '+dateData+' Event.'
        else:

            notif='You loose in '+dateData+' event. Better luck next time.'

        return notif



    def genWinner(self,userNames):
        #Generating the sorted list
        userNames.sort()

        return userNames

    def insertWinners(self,userNames,lnWin,eventId,t1=None):

        if t1==None:
            t1=time.time()

        for i in range(len(userNames)):
            userName=userNames[i]

            if i<=lnWin:
                status='Win'
            else:
                status='loose'

            data=[userName,i,status,t1,eventId]
            mp.dRes.insertData(data)

        self.insertAllUserWinResultNotification(t1)
        self.insertUsersWinResultNotification(userNames,lnWin,t1)

    def genEventWinn(self,eventId,lnWin=2):
        userNames=mp.dtm.getEventsAllPaidUserTrans(eventId,'userName')

        winUserNames=self.genWinner(userNames)

        self.insertWinners(winUserNames,lnWin,eventId)


    def insertAllUserWinResultNotification(self,t1):
        notif=self.genAllUserNotification(t1)
        notifId='Id_'+str(int(time.time()*1000))
        mp.dnotf.insertAllUserTable(notifId,notif,'Event',t1)

    def insertUsersWinResultNotification(self,userNames,lnWin,t1):
        notifId='Id_'+str(int(time.time()*1000))
        for i in range(len(userNames)):
            userName=userNames[i]

            if i <=lnWin:
                notif=self.genUserNotification(1,t1)

            else:
                notif=self.genUserNotification(0, t1)

            mp.dnotf.insertUserTable(userName,notifId,notif,'EventResult',t1)

#Verifying the notification
class NotifManage:

    def __init__(self):
        pass


    def createUserNotificatin(self,userName,notifId,notification,types,t1):
        mp.dnotf.insertUserTable(userName,notifId,notification,types,t1)

    def createNotification(self,notifId,notification,types,t1):
        mp.dnotf.insertAllUserTable(notifId,notification,types,t1)

#Verifying the transaction
class TransVerfManage:

    def __init__(self):
        pass


    def updateEventsUnPaidTrans(self,eventId):
        trans=mp.dtm.getEventsAllUnpaidUserTrans(eventId)

        if trans is not None:

            for p_link in trans:

                status=mp.razor.fetchPaymentStatusByPLink(p_link)
                payId=mp.razor.fetchPaymentIdByPLink(p_link)
                mp.dtm.updateTransactionPaymentIdByPLink(p_link,str(payId))
                #dataStatus=mp.dtm.getTransStatusByPLink(p_link)
                mp.dtm.updateTransactionStatusByPLink(p_link,status)

    def updateEventsPaidTrans(self,eventId):
        trans=mp.dtm.getEventsAllPaidUserTrans(eventId)

        if trans is not None:

            for p_link in trans:

                status=mp.razor.fetchPaymentStatusByPLink(p_link)

                payId=mp.razor.fetchPaymentIdByPLink(p_link)
                mp.dtm.updateTransactionPaymentIdByPLink(p_link,str(payId))
                #dataStatus=mp.dtm.getTransStatusByPLink(p_link)
                mp.dtm.updateTransactionStatusByPLink(p_link,status)


    def updateTransDatabase(self,eventId):

        self.updateEventsUnPaidTrans(eventId)
        self.updateEventsPaidTrans(eventId)

class EventManage:

    def __init__(self):
        pass

    def createEvent(self,eventName,amount,sortDesc,expDur=60*60*24):
        crrTime=time.time()
        eventId='Id_'+str(int(crrTime*1000))
        expTime=crrTime+expDur

        mp.dEventMan.insertEvent(eventId,eventName,sortDesc,amount,crrTime,expTime)

    def deleteEvent(self,eventId):
        mp.dEventMan.deleteEventByEventId(eventId)
