#GamingWorld

from flask import *

app=Flask(__name__)
app.secret_key = '----This is __secret'


@app.route('/')
def homePage():
    #{{ url_for('static', filename='css/buttonPaint.css') }}
    print(url_for('static', filename='css/buttonPaint.css'))
    #print("It is sessions-------------",flask.sessions())
    print(url_for('loginPage'))
    print("User connected /t",request.remote_addr)

    return render_template('home.html')

@app.route('/setCookie',methods=['POST','GET'])
def setCookie():
    if request.method=='POST':
        value=request.form['nm']
        session['bharosa']=value[-5:]
        session['userName']=value
        return redirect('/')
    else:
        return render_template('setCookie.html')

@app.route('/getCookie')
def getCookie():
    try:
        print("hallowing")
        vr=session['userName']+'or ---'+session['bharosa']
        print("Printing ",vr,'-ok')
        if vr==None:
            print("It is none")
            return "No cookies found"
        return vr
    except:
        return "No cookies found"
@app.route('/temp/<tr>')
def temp(tr):
    print("I am printing something")
    print(tr)
    return redirect('/')

@app.route('/login',methods=['POST','GET'])
def loginPage():
    if request.method=='POST':
        data=request.form
        print("Forum data ******")
        print(data['email_num'])
        print(data['passw'])
        return redirect('/')
    else:
        return render_template('login.html')
    #return redirect('/signUp')

@app.route('/signUp')
def signUpPage():
    return render_template('signUp.html')

@app.route('/dassboard')
def dassboardPage():
    return render_template('dassboard.html')


@app.route('/forgetPass')
def forgetPassPage():

    return render_template('forgetPass.html')

app.debug=True


app.run(host='0.0.0.0',threaded=True)
'''
@app.route('/')
def homePage():

    return render_template('home.html')

@app.route('/login',methods=['POST','GET'])
def loginPage():
    cond=checkUserInSession()

    if cond:
        return redirect(url_for('dassboardPage'))

    if request.method=='POST':
        data=request.form
        cond=hms.checkLoginDetails(data)
        userEM=data['userEM']
        if cond[0]==True:
            userName=None
            if cond[1]==1:
                condEmail=dataMan.checkEmailExist(userEM)

                if condEmail:
                    userName=dataMan.getUserNameByEmail(userEM)
                else:
                    return render_template('login.html',login_message="No Records Found- Invalid Credentials",userEM=data['userEM'])
            else:
                condMobNo=dataMan.checkMobNoExist(userEM)

                if condMobNo:
                    userName=dataMan.getUserNameByMobNo(userEM)
                else:
                    return render_template('login.html',login_message="No Records Found- Invalid Credentials",userEM=data['userEM'])

            userPass=data['userPass']
            serverPass=dataMan.getDecUserPassword(userName)

            if serverPass==userPass:
                session['userName']=userName
                return redirect('/dassboard')
            else:
                #print("False Password")
                return render_template('login.html',login_message="Invalid Credentials",userEM=data['userEM'])
        else:
            return render_template('login.html',login_message=cond[1],userEM=data['userEM'])
    else:

        return render_template('login.html')

@app.route('/signUp',methods=['POST','GET'])
def signUpPage():
    cond=checkUserInSession()

    if cond:
        return redirect(url_for('dassboardPage'))
    if request.method=='POST':

        data=request.form
        cond=hms.checkSignUpDetails(data)

        if cond==True:

            val=hrs.getExistSignValues(data)

            dataf=[data['userEmail'],data['userMobNo'],data['userVpa']]
            cond=hrd.checkSignUpCredentials(dataf)

            if cond==True:

                userName=dataSeq.genUserName()
                passw=dataSeq.encPassword(data['userPass'])

                cond=dataMan.insertUserProfile(userName,data,passw)
                if not cond:
                    print("Some kind of error")
                    signUp_message="There is some problem. Try after some time"
                    return render_template('signUp.html',signUp_message=signUp_message)
                else:

                    return redirect('/login')
            else:

                return render_template('signUp.html',value=val,msg=cond)


        else:

            val=hrs.getExistSignValues(data)
            return render_template('signUp.html',value=val,msg=cond)
    else:
        val=hrs.genDefaultSignResp()
        return render_template('signUp.html',value=val,msg={})

@app.route('/dassboard')
def dassboardPage():
    cond=checkUserInSession()

    if not cond:
        return redirect(url_for('loginPage'))
    else:
        userName=session['userName']
        return render_template('dassboard.html',userName=userName)

@app.route('/forgetPass')
def forgetPassPage():

    return render_template('forgetPassword.html')

@app.route('/logOut')
def logOutPage():
    cond=checkUserInSession()
    if cond:
        session.pop('userName',None)

    return redirect('/login')
app.debug=True


app.run(host='0.0.0.0',threaded=True)
'''
