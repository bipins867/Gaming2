import mainPage as mp
import time
from flask import *

class LoginSignUp:

    def __init__(self,app):
        self.setupUrl(app)
        self.dassboardPath='/dassboard/_dassboard/'
        self.loginPath='/login/'
        self.signUpPath='/signUp/'
        self.forgetPassPath='/login/'
        self.homePagePath='/_homePage/'
        self.aboutPath='/about/'
        self.donatePath='/donate/'
        self.feedbackPath='/feedback/'
        self.reportPath='/report/'

    def setupUrl(self,app):
        app.add_url_rule('/','index',self.homePage)
        app.add_url_rule('/login','LoginPage',self.loginPage,methods=['POST','GET'])
        app.add_url_rule('/signUp','SignUp',self.signUpPage,methods=['POST','GET'])
        app.add_url_rule('/dassboard','Dassboard',self.dassboardPage,methods=['POST','GET'])
        app.add_url_rule('/forgetPass','ForgetPass',self.forgetPassPage)
        app.add_url_rule('/logOut','LogOut',self.logOutPage)
        app.add_url_rule('/about','About',self.aboutPage)
        app.add_url_rule('/feedback','Feedback',self.feedbackPage,methods=['POST','GET'])
        app.add_url_rule('/report','Report',self.reportPage,methods=['POST','GET'])
        app.add_url_rule('/donate','Donate',self.donatePage,methods=['GET','POST'])
        app.add_url_rule('/donateSuccess','DonateSuccess',self.donateSuccessPage)


    def render_template(self,temp,**context):

        if 'logType' in context:
            return render_template(temp,**context)
        else:
            return render_template(temp,logType=None,**context)


    def homePage(self):
        dataF=mp.pathFinder(self.homePagePath)
        locPath='/_homePage/eventImages/'
        eventData=mp.mu.path2DictIndex(locPath,basePath=mp.folderPath)
        linkPath='/dassboard/payEvent/'

        lenEvent=len(eventData)
        return self.render_template('home.html',
                                    logType=1,
                                    dataF=dataF,
                                    linkPath=linkPath,
                                    locPath=locPath,
                                    eventData=eventData,
                                    lenEvent=lenEvent,
                                    )

    def loginPage(self):
        cond=mp.checkUserInSession()
        dataF=mp.pathFinder(self.loginPath)
        if cond:
            return redirect('/dassboard')

        if request.method=='POST':
            data=request.form
            cond=mp.hms.checkLoginDetails(data)
            userEM=data['userEM']
            if cond[0]==True:
                userName=None
                if cond[1]==1:
                    condEmail=mp.dataMan.checkEmailExist(userEM)

                    if condEmail:
                        userName=mp.dataMan.getUserNameByEmail(userEM)
                    else:
                        return self.render_template('login.html',dataF=dataF,login_message="Invalid Credentials",userEM=data['userEM'])
                else:
                    condMobNo=mp.dataMan.checkMobNoExist(userEM)

                    if condMobNo:
                        userName=mp.dataMan.getUserNameByMobNo(userEM)
                    else:
                        return self.render_template('login.html',dataF=dataF,login_message="Invalid Credentials",userEM=data['userEM'])

                userPass=data['userPass']
                serverPass=mp.dataMan.getDecUserPassword(userName)

                if serverPass==userPass:
                    session['userName']=userName
                    return redirect('/dassboard')
                else:
                    #print("False Password")
                    return self.render_template('login.html',dataF=dataF,login_message="Invalid Credentials",userEM=data['userEM'])
            else:
                return self.render_template('login.html',dataF=dataF,login_message=cond[1],userEM=data['userEM'])
        else:

            return self.render_template('login.html',dataF=dataF,logTypeName='Login',logType='login')


    def signUpPage(self):
        cond=mp.checkUserInSession()
        dataF=mp.pathFinder(self.signUpPath)
        if cond:
            return redirect('/dassboard')
        if request.method=='POST':

            data=request.form
            cond=mp.hms.checkSignUpDetails(data)

            if cond==True:

                val=mp.hrs.getExistSignValues(data)

                dataf=[data['userEmail'],data['userMobNo'],data['userVpa']]
                cond=mp.hrd.checkSignUpCredentials(dataf)

                if cond==True:

                    userName=mp.dataSeq.genUserName()
                    passw=mp.dataSeq.encPassword(data['userPass'])

                    cond=mp.dataMan.insertUserProfile(userName,data,passw)
                    if not cond:
                        print("Some kind of error")
                        signUp_message="There is some problem. Try after some time"
                        return self.render_template('signUp.html',dataF=dataF,signUp_message=signUp_message)
                    else:

                        return redirect('/login')
                else:

                    return self.render_template('signUp.html',dataF=dataF,value=val,msg=cond)


            else:

                val=mp.hrs.getExistSignValues(data)
                return self.render_template('signUp.html',dataF=dataF,value=val,msg=cond)
        else:
            val=mp.hrs.genDefaultSignResp()
            return self.render_template('signUp.html',dataF=dataF,value=val,msg={})


    def dassboardPage(self):
        cond=mp.checkUserInSession()
        dataF=mp.pathFinder(self.dassboardPath)
        #print(url_for('loginPage'))
        if not cond:
            return redirect('/login')
        else:
            userName=session['userName']
            user_name=mp.dataMan.getUser_Name(userName)
            crrTime=time.time()
            dataEvent=mp.dEventMan.fetchCurrAllEvent(crrTime)
            if dataEvent is not None:
                data=[]
                for i in dataEvent:
                    cond=mp.dRes.checkEventExist(i[0])
                    if not cond:
                        data.append(i)
                dataEvent=data

            partEvent=mp.dEventMan.getAllParticipants(dataEvent)
            xEveLen=0
            #print(dataEvent)
            if dataEvent is  not None:
                xEveLen=len(dataEvent)

            return self.render_template('dassboard.html',partEvent=partEvent,xEveLen=xEveLen,logType=2,dataF=dataF,dataEvent=dataEvent,user_name=user_name)

    def forgetPassPage(self):
        dataF=mp.pathFinder(self.loginPath)
        return self.render_template('forgetPassword.html',dataF=dataF)

    def logOutPage(self):
        cond=mp.checkUserInSession()
        if cond:
            session.pop('userName',None)

        return redirect('/')

    def reportPage(self):
        cond=mp.checkUserInSession()
        dataF=mp.pathFinder(self.reportPath)
        statusMessage=''
        if request.method=='POST':
            data=request.form
            message=data['message']


            if cond:
                userName=session['userName']
                mp.dFeedback.insertUserFeedback(userName,message,ftype='Report')
            else:
                mp.dFeedback.insertFeedback(message,ftype='Report')

            statusMessage='Report updated successfully..'
            return self.render_template('report.html',dataF=dataF,statusMessage=statusMessage)
        elif request.method=='GET':
            if not cond:
                statusMessage='Hey !!! Currently you are not a active user. Please Login..'
            return self.render_template('report.html',dataF=dataF,statusMessage=statusMessage)
        else:
            statusMessage='Something Went wrong'
            return self.render_template('report.html',dataF=dataF,statusMessage=statusMessage)


    def feedbackPage(self):
        cond=mp.checkUserInSession()
        dataF=mp.pathFinder(self.feedbackPath)
        statusMessage=''
        if request.method=='POST':
            data=request.form
            message=data['message']


            if cond:
                userName=session['userName']
                mp.dFeedback.insertUserFeedback(userName,message,ftype='Feedback')
            else:
                mp.dFeedback.insertFeedback(message,ftype='Feedback')

            statusMessage='Feedback updated successfully..'
            return self.render_template('feedback.html',dataF=dataF,statusMessage=statusMessage)
        elif request.method=='GET':
            if not cond:
                statusMessage='Hey !!! Currently you are not a active user. Please Login..'
            return self.render_template('feedback.html',dataF=dataF,statusMessage=statusMessage)
        else:
            statusMessage='Something Went wrong'
            return self.render_template('feedback.html',dataF=dataF,statusMessage=statusMessage)

    def aboutPage(self):
        dataF=mp.pathFinder(self.aboutPath)

        return self.render_template('about.html',dataF=dataF,webName=mp.webName)

    def donatePage(self):
        dataF=mp.pathFinder(self.donatePath)
        if mp.request.method=='POST':

            amount=int(mp.request.form['amount'])
            message=mp.request.form['message']
            xr=mp.razor.createPaymentLink(amount,desc=message,
                                    callback_url="http://localhost:5000/donateSuccess")

            return redirect(xr['short_url'])
        else:

            return self.render_template('donate.html',dataF=dataF)

    def donateSuccessPage(self):
        dataF=mp.pathFinder(self.donatePath)
        return self.render_template('donateSuccess.html',dataF=dataF)
