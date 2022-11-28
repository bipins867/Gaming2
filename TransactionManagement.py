import TimeUtils as tu
import mainPage as mp
import myStringLib as ms
import time

class Transaction:

    def __init__(self):
        pass

    def fetchEventsUCTrans(self,userName,eventId):

        trans=mp.dtm.getEventsUserTrans(userName,eventId)

        if len(trans)==0:
            return None
        else:
            return trans[-1]

    def getEventsPaymentStatus(self,userName,eventId):
        trans=self.fetchEventsUCTrans(userName,eventId)

        if trans is not None:
            p_link=trans[2]

            status=mp.razor.fetchPaymentStatusByPLink(p_link)
            return status
        else:
            return None

    def fetchUserPrevTrans(self,userName):
        data=mp.dtm.getUserTransaction(userName)

        if len(data)==0:
            return None
        else:
            data=ms.modifySqlResult(data)
            return data

    def getStructPrevTrans(self,userName):
        data=self.fetchUserPrevTrans(userName)

        if data is not None:
            xr=[]
            for i in data:
                event_id=i[1]
                p_link=i[2]
                p_id=i[3]
                amount=i[4]
                status=i[5]
                paid_time=int(i[6])
                paid_time=time.ctime(paid_time)

                ar=[event_id,p_link,p_id,amount,status,paid_time]
                xr.append(ar)
            return xr

    def checkUserEventsPaymentEligibilty(self,userName,eventId):
        trans=self.getEventsPaymentStatus(userName,eventId)

        if trans is not None:
            if trans=='created':
                return 0
            elif trans=='paid' or trans=='captured':
                return 1
            elif trans=='expired':
                return -2
            else:
                return -1
        else:
            return None
