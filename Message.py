import string
import os
import SecurityManage as sm
import DataManage as dm


dataCon=sm.DataControl()
dataMan=dm.Manage()





class HandleMessage:

    def __init__(self):
        self.signFields=['userName','userEmail','userMobNo','userVpa','userVpaName']


    def validSignUp2Password(self,form):
        userPass=form['userPass']
        confPass=form['userCPass']

        if userPass==confPass:
            data=dataCon.checkValidPassword(userPass)
            return data
        else:
            return "Password are not matched each other"


    def overAllSignUpValidate(self,conds):
        cond=True

        for  i in conds:
            if i!=True:
                cond=False
                break
        return cond

    def checkSignUpDetails(self,form):
        condName=dataCon.checkValidName(form['userName'])
        condEmail=dataCon.checkValidEmail(form['userEmail'])
        condMobNo=dataCon.checkValidMobNo(form['userMobNo'])
        condVpa=dataCon.checkValidVpa(form['userVpa'])
        condVpaName=dataCon.checkValidVpaName(form['userVpaName'])

        condPass=self.validSignUp2Password(form)
        conds=[condName,condEmail,condMobNo,condVpa,condVpaName,condPass]
        overAllCond=self.overAllSignUpValidate(conds)

        if overAllCond==True:

            return overAllCond
        else:

            msg={}
            if True:
                if condName==True:
                    msg['userName']=''
                else:
                    msg['userName']=condName

                if condEmail==True:
                    msg['userEmail']=''
                else:
                    msg['userEmail']=condEmail

                if condMobNo==True:
                    msg['userMobNo']=''
                else:
                    msg['userMobNo']=condMobNo

                if condVpa==True:
                    msg['userVpa']=''
                else:
                    msg['userVpa']=condVpa

                if condVpaName==True:
                    msg['userVpaName']=''
                else:
                    msg['userVpaName']=condVpaName

                if condPass==True:
                    msg['userPass']=''
                else:
                    msg['userPass']=condPass

            return msg

    def isEmailOrMobNo(self,data):
        condEmail=dataCon.checkValidEmail(data)
        condMobNo=dataCon.checkValidMobNo(data)

        if condEmail==True:
            return True, 1
        elif condMobNo==True:
            return True,2
        else:
            return False,"Invalid Credentials"

    def checkLoginDetails(self,form):
        userEM=form['userEM']
        isEM=self.isEmailOrMobNo(userEM)

        return isEM


class HandleReqRes:

    def __init__(self):
        self.signFields=['userName','userEmail','userMobNo','userVpa','userVpaName']
        self.loginFields=['userEM']

    def genDefaultSignResp(self):

        val={}
        for i in self.signFields:
            val[i]=''
        return val

    def genDefaultLoginResp(self):

        val={}
        for i in self.loginFields:
            val[i]=''
        return val

    def getExistSignValues(self,form):
        val={}

        for i in self.signFields:
            val[i]=form[i]
        return val

    def getExistLoginValues(self,form):
        val={}
        for i in self.loginFields:
            val[i]=form[i]
        return val


class HandleReqDatabase:

    def __init__(self):
        pass


    def checkEmail(self,email):
        cond=dataMan.checkEmailExist(email)

        if cond:
            return "Email Already Exist"
        else:
            return True

    def checkMobNo(self,mobNo):
        cond=dataMan.checkMobNoExist(mobNo)

        if cond:
            return "Mobile Number already exist"
        else:
            return True

    def checkVpa(self,vpa):
        cond=dataMan.checkVpaExist(vpa)

        if cond:
            return "Vpa Already Exist"
        else:
            return True

    def overAllCheck(self,data):
        #Data=[email,mobNo,vpa]

        condEmail=self.checkEmail(data[0])
        condMobNo=self.checkMobNo(data[1])
        condVpa=self.checkVpa(data[2])

        cond=True

        a1=[condEmail,condMobNo,condVpa]

        for i in a1:
            if i!=True:
                cond=False
                break
        return cond,a1



    def checkSignUpCredentials(self,data):
        #Data=[email,mobNo,vpa]
        #This must be the data
        cond=self.overAllCheck(data)
        if cond[0]:
            return True
        else:
            data=cond[1]
            msg={}

            if data[0]!=True:
                msg['userEmail']=data[0]

            if data[1]!=True:
                msg['userMobNo']=data[1]

            if data[2]!=True:
                msg['userVpa']=data[2]

            return msg
