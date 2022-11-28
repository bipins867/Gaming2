import dbquery2 as db
import time
import myStringLib as ms
import SecurityManage as sm
import TimeUtils as tu
from flask import *

mydb=db.genMdb()
#mydb=db.genBySSHTunnel()


cursor=mydb.cursor();



cb=db.cb1(cursor,'GamingWorld')
#cb=db.cb1(cursor,isssh=True)
dataSeq=sm.DataSecurity()

class DefaultData:

    def __init__(self):
        self.userProfile='_UserProfile'

    def getNameByUserName(self,userName,email=False):
        if not email:
            data=cb.selectParticularData('_UserProfile','userName','name',userName)
        else:
            data=cb.selectParticularData('_UserProfile','userName','name,email',userName)
        data=ms.modifySqlResult(data)
        return data[0]

class Manage:

    def __init__(self):
        pass

    def setUpFirstTime(self):

        cb.createTableTextSize('_UserProfile',['UserName','Name','Email','MobNo','Vpa','VpaName'])
        cb.createTableTextSize('_UserSequrity',['UserName','Password'])


    def insertUserProfile(self,userName,dataProf,dataSeq):
        xr=[userName,dataProf['userName'],dataProf['userEmail'],dataProf['userMobNo'],
        dataProf['userVpa'],dataProf['userVpaName']]
        cb.insertDataN('_UserProfile',xr)

        cb.insertDataN('_UserSequrity',[userName,dataSeq])

        mydb.commit()
        return True


    def updateUserProfile(self,userName,col,data):
        cb.updateParticularData('_UserProfile','userName',col,userName,data)
        mydb.commit()


    def getUserNameByEmail(self,email):
        data=cb.selectAllDataByCondition('_UserProfile','email',email)[0]
        return data[0]

    def getUserNameByMobNo(self,MobNo):
        data=cb.selectAllDataByCondition('_UserProfile','MobNo',MobNo)[0]
        return data[0]


    def getUserVpa(self,userName):
        data=cb.selectAllDataByCondition('_UserProfile','UserName',userName)[0]
        return data[4]

    def getUserVpaName(self,userName):
        data=cb.selectAllDataByCondition('_UserProfile','UserName',userName)[0]
        return data[5]

    def getUserPassword(self,userName):
        data=cb.selectAllDataByCondition('_UserSequrity','UserName',userName)[0]
        return data[1]

    def getDecUserPassword(self,userName):
        passw=self.getUserPassword(userName)
        return dataSeq.decPassword(passw)

    def getUser_Name(self,userName):
        data=cb.selectAllDataByCondition('_UserProfile','UserName',userName)[0]
        return data[1]

    def getUserProfile(self,userName):
        data=cb.selectAllDataByCondition('_UserProfile','UserName',userName)[0]
        return data

    def getUserDictProfile(self,userName):
        data=self.getUserProfile(userName)

        d={}

        d['user_name']=data[1]
        d['userEmail']=data[2]
        d['userMobNo']=data[3]
        d['userVpa']=data[4]
        d['userVpaName']=data[5]

        return d

    def checkEmailExist(self,email):
        cond=cb.checkData('_UserProfile','email',email)
        return cond

    def checkMobNoExist(self,mobNo):
        cond=cb.checkData('_UserProfile','mobNo',mobNo)
        return cond

    def checkVpaExist(self,vpa):
        cond=cb.checkData('_UserProfile','vpa',vpa)
        return cond

    def checkUserNameExist(self,userName):
        cond=cb.checkData('_UserProfile','userName',userName)
        return cond

class TransactionManage:

    def __init__(self):
        self.tableUt='_UserTransaction'




    def intifyCol(self,tableName,cols):
        cb.modifyColTable(tableName,cols,10,isInt=True)

    def initialSetup(self):
        cols=['userName','eventId','p_link','p_id','amount','status','t_period','paid_Time']

        cb.createTableTextSize(self.tableUt,cols)
        self.intifyCol(self.tableUt,'t_period')
        self.intifyCol(self.tableUt,'paid_Time')


    def getUserTransaction(self,userName):

        data=cb.selectAllDataByCondition(self.tableUt,'userName',userName)
        return data

    def getUserTransStatus(self,userName,p_link):
        fields=['userName','p_link']
        values=[userName,p_link]
        data=cb.selectByMulAndCond(self.tableUt,fields,values,'status')

        return data

    def getTransStatusByPLink(self,p_link):
        fields=['p_link']
        values=[p_link]
        data=cb.selectByMulAndCond(self.tableUt,fields,values,'status')

        return data

    def getUserTransFromToData(self,userName,_from,to):
        data=cb.selectRangeData(self.tableUt,'t_period',_from,to)
        return data

    def updateUserTransPayId(self,userName,p_link,p_id):
        fields=['userName','p_link']
        values=[userName,p_link]

        cb.updateDataByMulCond(self.tableUt,fields,values,'p_id',p_id,isStr=True)
        mydb.commit()

    def updateUserTransStatus(self,userName,p_link,status):
        fields=['userName','p_link']
        values=[userName,p_link]

        cb.updateDataByMulCond(self.tableUt,fields,values,'status',status,isStr=True)
        mydb.commit()

    def updateTransactionStatusByPLink(self,p_link,status):
        fields=['p_link']
        values=[p_link]

        cb.updateDataByMulCond(self.tableUt,fields,values,'status',status,isStr=True)
        mydb.commit()
    def updateTransactionPaymentIdByPLink(self,p_link,payId):
        fields=['p_link']
        values=[p_link]

        cb.updateDataByMulCond(self.tableUt,fields,values,'p_id',payId,isStr=True)
        mydb.commit()

    def updateUserTransPaidTime(self,userName,p_link,paid_Time):
        fields=['userName','p_link']
        values=[userName,p_link]

        cb.updateDataByMulCond(self.tableUt,fields,values,'paid_Time',paid_Time,isStr=False)
        mydb.commit()

    def getToday2BackDataUserTrans(self,userName,backTime):
        xtime=tu.crr2TodaysInit()
        xtime=xtime-backTime
        crrTime=time.time()

        data=cb.selectRangeDataByMulCond(self.tableUt,'userName',userName,'t_period',xtime,crrTime)

        return data

    def getTodaysAllUserTrans(self):
        xtime=tu.crr2TodaysInit()
        crrTime=time.time()

        data=cb.selectRangeData(self.tableUt,'t_period',xtime,crrTime)
        return data

    def getEventsAllUnpaidUserTrans(self,eventId):
        xtime=tu.crr2TodaysInit()
        crrTime=time.time()

        data=cb.selectRangeDataByMulCond(self.tableUt,'status','paid','t_period',xtime,crrTime,nots=False,part='p_link')

        data=ms.modifySqlResult(data)
        return data

    def getEventsAllPaidUserTrans(self,eventId,partData='P_link'):
        fields=['eventId','status']
        values=[eventId,'paid']
        data=cb.selectByMulAndCond(self.tableUt,fields,values,partData)

        data=ms.modifySqlResult(data)
        return data

    def getEventsUserTrans(self,userName,eventId):

        fields=['userName','eventId']
        values=[userName,eventId]

        data=cb.selectByMulAndCond(self.tableUt,fields,values)
        return data


    def checkPLinkInUserTrans(self,p_link):
        cond=cb.checkData(self.tableUt,'p_link',p_link)
        return cond

    def checkUserPLink(self,userName,p_link):
        #self.tableUct
        fields=['userName','p_link']
        values=[userName,p_link]

        cond=cb.checkDataCond(self.tableUt,fields,values)
        return cond


    def getEventsAllTransaction(self,eventId):
        data=cb.selectAllDataByCondition(self,tableUt,'eventId',eventId)
        data=ms.modifySqlResult(data)
        return data

    def getEventsAllTransAccToStatus(self,eventId,status='paid'):
        fields=['eventId','status']
        values=[eventId,status]
        data=cb.selectByMulAndCond(self.tableUt,fields,values)

        data=ms.modifySqlResult(data)
        return data



    def insertCreatedUserTrans(self,userName,eventId,p_link,amount,status,t_period):
        #cols=['userName','p_link','amount','status','t_period','paid_Time']
        cb.insertData(self.tableUt,userName,eventId,p_link,'None',amount,status,t_period,0)
        mydb.commit()

class NotificationManage:

    def __init__(self):
        self.userTable='_UserNotification'
        self.allUserTable='_AllUserNotification'



    def intifyCol(self,tableName,cols):
        cb.modifyColTable(tableName,cols,10,isInt=True)

    def initialSetup(self):
        cols1=['userName','notifId','notification','types','time']
        cols2=['notifId','notification','types','time']
        cb.createTableTextSize(self.userTable,cols1)
        cb.createTableTextSize(self.allUserTable,cols2)

        self.intifyCol(self.userTable,'time')
        self.intifyCol(self.allUserTable,'time')

    def insertUserTable(self,userName,notifId,notification,types,t1=None):
        if t1 is None:
            t1=time.time()

        cb.insertData(self.userTable,userName,notifId,notification,types,t1)

        mydb.commit()

    def insertAllUserTable(self,notifId,notification,types,t1=None):
        if t1 is None:
            t1=time.time()

        cb.insertData(self.allUserTable,notifId,notification,types,t1)
        mydb.commit()

    def fetchUserNotification(self,userName,limit=10):
        data=cb.selectAllDataByCondition(self.userTable,'userName',userName,part='time,notifId,notification')

        data=ms.modifySqlResult(data)
        if data is None:
            return None

        data=data[::-1]

        return data[:limit]

    def fetchAllUserNotification(self,backTime=60*60*24*10):
        xtime=tu.crr2TodaysInit()
        xtime=xtime-backTime
        crrTime=time.time()

        data=cb.selectRangeData(self.allUserTable,'time',xtime,crrTime,part='time,notifId,notification')

        data=ms.modifySqlResult(data)

        if data is None:
            return data

        return data[::-1]

    def fetchNotification(self,userName):
        nuser=self.fetchUserNotification(userName)
        auser=self.fetchAllUserNotification()

        x=[]

        if nuser!=None:
            x=nuser

        if auser!=None:
            x=x+auser


        x.sort()
        xn=[]
        for i in x:
            #Time,notifId,notification
            xn.append([time.ctime(i[0]),i[1],i[2]])
        return xn

    def deleteUserNotification(self,fixTime=60*60*24*11):
        cb.deleteBySingleRangeCond(self.userTable,'time',fixTime)
        cb.deleteBySingleRangeCond(self.allUserTable,'time',fixTime)

class ResultManage(DefaultData):

    def __init__(self):
        self.table='_EventResult'

    def intifyCol(self,tableName,cols):
        cb.modifyColTable(tableName,cols,10,isInt=True)

    def initialSetup(self):
        cols=['userName','ranks','status','time','eventId']
        cb.createTableTextSize(self.table,cols)

        self.intifyCol(self.table,'ranks')
        self.intifyCol(self.table,'time')

    def insertData(self,data):

        cb.insertData(self.table,data[0],data[1],data[2],data[3],data[4])

        mydb.commit()


    def checkEventInResult(self,eventId):
        cond=cb.checkData(self.table,'eventId',eventId)
        return  cond

    def getTimeByEventId(self,eventId):
        data=cb.selectParticularData(self.table,'eventId','time',eventId)
        data=ms.modifySqlResult(data)
        if data is not None:
            return data[0]

    def fetchDataByEventId(self,eventId):
        data=cb.selectAllDataByCondition(self.table,'eventId',eventId,part='userName,ranks,status')
        data=ms.modifySqlResult(data)
        return data

    def getStructDataByEventId(self,eventId):
        data=self.fetchDataByEventId(eventId)

        timeData=self.getTimeByEventId(eventId)
        timeData=time.ctime(timeData)
        if data is None:
            return data

        xdata=[]

        for i in data:
            uname,uemail=self.getNameByUserName(i[0],email=True)
            xdata.append([uname,uemail,i[1],i[2]])

        return xdata,timeData

    def fetchParticipants(self,eventId):
        data=cb.selectAllDataByCondition(self.table,'eventId',eventId,'userName')
        data=ms.modifySqlResult(data)
        return data

    def countParticipants(self,eventId):
        data=self.fetchParticipants(eventId)
        if data is not None:
            return len(data)
        else:
            return 0


    def getEventIdByTime(self,t1):
        t1=str(t1)
        data=cb.selectAllDataByCondition(self.table,'time',t1,'eventId')
        data=ms.modifySqlResult(data)
        if data is None:
            return data

        return data[0]

    def checkEventExist(self,eventId):
        cond=cb.checkData(self.table,'eventId',eventId)
        return cond

    def fetchBackDayResult(self,backTime):
        xtime=tu.crr2TodaysInit()
        xtime=xtime-backTime
        crrTime=time.time()

        data=cb.selectRangeData(self.table,'time',xtime,crrTime,part='time')

        data=ms.modifySqlResult(data)

        if data is None:
            return data


        setData=set(data)

        setData=list(setData)
        setData.sort()
        data=setData
        return data[::-1]

    def getResultTypeInfo(self,backTime=60*60*24*10):
        data=self.fetchBackDayResult(backTime)

        if data is None:
            return data


        strcData=[]
        for i in data:
            evid=self.getEventIdByTime(i)
            ti=time.ctime(i)
            strcData.append([evid,ti])

        return strcData

    def fetchResultOnDay(self,dayTime):
        data=cb.selectAllDataByCondition(self.table,'time',dayTime)
        return data

    def fetchWinResultOnDay(self,dayTime,winType='win'):
        fields=['time','status']
        values=[dayTime,winType]
        data=cb.selectByMulAndCond(self.table,fields,words,'userName')
        return data

    def deleteResult(self,fixTime=60*60*24*11):
        cb.deleteBySingleRangeCond(self.table,'time',fixTime)

class FeedbackManage:

    def __init__(self):
        self.table='_Feedback'
        self.userTable='_UserFeedback'

    def intifyCol(self,tableName,cols):
        cb.modifyColTable(tableName,cols,10,isInt=True)

    def initialSetup(self):
        cols1=['Feedback','type','Time']
        cols2=['userName','Feedback','type','Time']

        cb.createTableTextSize(self.table,cols1)
        cb.createTableTextSize(self.userTable,cols2)

        self.intifyCol(self.table,'time')
        self.intifyCol(self.userTable,'time')

    def insertFeedback(self,feedback,ftype,t1=None):
        if t1 is None:
            t1=time.time()
        feedback=dataSeq.enc(feedback)
        cb.insertData(self.table,feedback,ftype,t1)
        mydb.commit()

    def insertUserFeedback(self,userName,feedback,ftype,t1=None):
        if t1 is None:
            t1=time.time()
        feedback=dataSeq.enc(feedback)

        cb.insertData(self.userTable,userName,feedback,ftype,t1)
        mydb.commit()


    def deleteResult(self,fixTime=60*60*24*11):
        cb.deleteBySingleRangeCond(self.table,'time',fixTime)
        cb.deleteBySingleRangeCond(self.userTable,'time',fixTime)

class EventManage(TransactionManage,ResultManage):

    def __init__(self):
        self.eventTable='_eventManage'
        self.userTransTable='_UserTransaction'
        self.table=self.eventRes='_EventResult'
        self.tableUt='_UserTransaction'

    def intifyCol(self,tableName,cols):
        cb.modifyColTable(tableName,cols,10,isInt=True)

    def initialSetup(self):
        cols=['eventId','eventName','sortDesc','Amount','creTime','expTime']

        cb.createTableTextSize(self.eventTable,cols)


        self.intifyCol(self.eventTable,'Amount')
        self.intifyCol(self.eventTable,'creTime')
        self.intifyCol(self.eventTable,'expTime')

    def insertEvent(self,eventId,eventName,sortDesc,amount,creTime,expTime):

        cb.insertData(self.eventTable,eventId,eventName,sortDesc,amount,creTime,expTime)
        mydb.commit()

    def getEventByEventName(self,eventId):
        data=cb.selectAllDataByCondition(self,eventTable,'eventId',eventId)

        data=ms.modifySqlResult(data)

        if data is not None:
            return data[0]

    def getEventAmount(self,eventId):
        data=cb.selectParticularData(self.eventTable,'eventId','amount',eventId)

        data=ms.modifySqlResult(data)

        if data is not None:
            return data[0]

    def changeTimeFormatEvent(self,data):
        xr=[]
        for i in data:
            a=i[:4]
            a4=time.ctime(i[4])
            a5=time.ctime(i[5])
            a=list(a)+[a4,a5]
            xr.append(a)
        return xr

    def checkEventIdExist(self,eventId):
        cond=cb.checkData(self.eventTable,'eventId',eventId)
        return cond

    def checkEventExpiry(self,crrTime,eventId):

        data=cb.selectParticularData(self.eventTable,'eventId','expTime',eventId)
        data=ms.modifySqlResult(data)

        if data is not None:
            expTime=data[0]

            if crrTime>expTime:
                return True
            else:
                return False

    def getPaidUserInEvent(self,eventId):
        fields=['eventId','status']
        values=[eventId,'paid']
        count=cb.countByCond(self.userTransTable,fields,values)
        return count

    def getUnpaidUserInEvent(self,eventId):
        cPaid=self.getPaidUserInEvent(eventId)
        allUser=self.getAllUserInEvent(eventId)

        return int(allUser)-int(cPaid)

    def getAllParticipants(self,eventIdList):
        data={}
        if eventIdList is None:
            return None
        for ev in eventIdList:
            event=ev[0]
            data[event]=self.getPaidUserInEvent(event)
        return data

    def fetchEventDetails(self,eventId,isDict=True):
        data=cb.selectAllDataByCondition(self.eventTable,'eventId',eventId)
        data=ms.modifySqlResult(data)
        if data is not None:
            if isDict:
                cols=cb.getColName(self.eventTable)
                data=data[0]

                xr={}
                for i in range(len(data)):
                    f=cols[i]
                    val=data[i]
                    xr[f]=val
                data=xr

        return data

    def getAllUserInEvent(self,eventId):
        fields=['eventId']
        values=[eventId]
        count=cb.countByCond(self.userTransTable,fields,values)
        return count

    def fetchCurrAllEvent(self,crrTime):
        #crrTime=time.time()
        data=cb.selectRangeDataByTwoCol(self.eventTable,'expTime','creTime',crrTime)

        data=ms.modifySqlResult(data)

        if data is not None:
            data=self.changeTimeFormatEvent(data)

        return data

    def changeTimeInEventData(self,data):
        if data is not None:
            xdata=[]
            for xi in range(len(data)):
                i=data[xi]
                kr=[]
                print(i)
                for f in range(len(i)):
                    if f==4 or f==3:

                        kr.append(time.ctime(i[f]))
                    else:
                        kr.append(i[f])

                xdata.append(kr)
            return xdata

    def fetchAllEvent(self):
        data=cb.selectAllData(self.eventTable,part='eventId,eventName,Amount,creTime,expTime')
        data=ms.modifySqlResult(data)
        data=self.changeTimeInEventData(data)
        return data

    def getStructEventHistoryV2(self):
        allEvent=self.fetchAllEvent()

        if allEvent is not None:
            data={}
            for i in allEvent:
                eventId=i[0]
                partic=self.getPaidUserInEvent(eventId)
                cond=self.checkEventInResult(eventId)
                eveTime=self.getTimeByEventId(eventId)
                if cond:
                    eveTime=time.ctime(eveTime)
                if cond:
                    cond='Declayred'
                else:
                    condExp=self.checkEventExpiry(time.time(),eventId)
                    if condExp:
                        cond='Awaited'
                    else:
                        cond='OnGoing'
                data[eventId]=[partic,cond,eveTime]
            return allEvent,data

        else:
            return None


    def getActiveEventList(self,crrTime=None):
        if crrTime is None:
            crrTime=time.time()

        data=cb.selectGreaterFieldData(self.eventTable,'expTime',crrTime,gretType='>=',part='eventId')
        data=ms.modifySqlResult(data)
        return data


    def getEventListFromCreTime(self,fromTime):

        data=cb.selectGreaterFieldData(self.eventTable,'creTime',fromTime,gretType='>=',part='eventId')
        data=ms.modifySqlResult(data)
        return data

    def deleteEventByEventId(self,eventId):
        cb.deleteBySingleCond(self.eventTable,'eventId',eventId)
        mydb.commit()

    #This is something else type of comments

    def checkEventExpiryV2(self,eventId,toTime=None):
        if toTime==None:
            toTime=time.time()
        #This statements can only produce error when event dont exist
        data=cb.selectAllDataByCondition(self.eventTable,'eventId',eventId,part='expTime')[0]

        if int(toTime)>=int(data):
            return True
        else:
            return False


    def getStrutResultTypeDataForHistory(self,dataMan):
        data={}
        #data[eventId]=[participants,status,DeclarationTime]
        for i in dataMan:
            eventId=i[0]
            condRes=cb.checkData(self.eventRes,'eventId',eventId)
            dr=[]
            if condRes:
                dat=cb.selectAllDataByCondition(self.eventRes,'eventId',eventId)
                participants=len(dat)
                resTime=dat[0][3]
                resStatus='Declayred'
                data[eventId]=[participants,resTime,resStatus]

            else:
                paidPartic=self.getEventsAllTransAccToStatus(eventId)
                if paidPartic is None:
                    paidPartic=0
                else:
                    paidPartic=len(paidPartic)

                eventExp=self.checkEventExpiryV2(eventId)
                if eventExp:
                    data[eventId]=[paidPartic,None,'Awaited']
                else:
                    data[eventId]=[paidPartic,None,'OnGoing']
        return data

    def getStructEventHistory(self,timeBack=60*60*24*10):
        #EventName and id
        #Event Status , running or ended
        #Event Created time and expiry time,
        #Event Amount and participants
        #Result Status -- same as event status
        crrTime=time.time()
        backTime=crrTime-timeBack
        dataMan=cb.selectRangeData(self.eventTable,'creTime',backTime,crrTime)
        dResData=self.getStrutResultTypeDataForHistory(dataMan)

        return dataMan,dResData

class DonationManage:
    def __init__(self):

        self.tableAll='_DonationManage'


    def initialSetup(self):

        cols=['userName','p_link','amount','status','disc','creTime']

        cb.createTableTextSize(self.tableAll,cols)


    def insertDonation(self,p_link,amount,status,desc,userName=None,creTime=None):
        if creTime==None:
            creTime=time.time()

        cb.insertData(self.tableUser,userName,p_link,amount,status,desc,creTime)
