#TimeUtils
import time



def todaysInit(sxr,times):
    hrs=sxr[3]*60*60
    mins=sxr[4]*60
    sec=sxr[5]
    total=hrs+mins+sec
    return times-total


def crr2TodaysInit():
	t1=time.time()
	sxr=time.strptime(time.ctime(t1))
	return todaysInit(sxr,t1)
