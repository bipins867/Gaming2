import myStringLib as ms
import re
import string
from cryptography.fernet import Fernet
import time

class DataControl:

    def __init__(self):
        self.regexEmail = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        self.regexVpa=r'\b[A-Za-z0-9]+@[A-Za-z0-9]{2,}'
        self.regexMobNo=r'\b[0-9]{10}'


    def checkValidEmail(self,email):

        if re.fullmatch(self.regexEmail,email):
            return True
        else:
            return "Enter a valid Email"

    def checkValidVpa(self,vpa):

        if re.fullmatch(self.regexVpa,vpa):
            return True
        else:
            return "Enter a valid VPA"
    def checkValidVpaName(self,name):
        ln=len(name)

        cond=True

        if ln>4 and ln<20:
            for i in name:
                if i not in string.ascii_letters+' ':
                    cond=False
        else:
            cond="Enter a valid Name"

        return cond

    def checkValidMobNo(self,mob):

        if re.fullmatch(self.regexMobNo,mob):
            return True
        else:
            return "Enter a valid Mobile Number"


    def checkValidName(self,name):
        ln=len(name)

        cond=True

        if ln>4 and ln<20:
            for i in name:
                if i not in string.ascii_letters+' ':
                    cond=False
        else:
            cond="Enter a valid Name"

        return cond

    def checkValidPassword(self,password):

        ln=len(password)
        up=string.ascii_uppercase
        lo=string.ascii_lowercase
        dig=string.digits
        symb='''`~!@#$%^&*()-_=+[]{}\\|;:.,<>/?'"'''
        cond=0

        if ln<8 or ln>40:
            #Length is less than 1

            return "Length of password must be in between [8-40]"
        else:
            condUp=False
            condLo=False
            condSymb=False
            condNum=False
            for i in password:
                if i in up:
                    condUp=True
                    continue

                if i in lo:
                    condLo=True

                if i in dig:
                    condNum=True

                if i in symb:
                    condSymb=True
        if not condUp:
            return 'Password must contain at least 1 uppercase character. Eg. - AKSIX'
        elif not condLo:
            return 'Password must contain at least 1 lowercase character. Eg.abcdef'
        elif not condSymb:
            return 'Password must contain at least 1 symbol. Eg. ~@#$%^&*'
        elif not condNum:
            return 'Password must contain at least 1 digit. Eg. 0123'
        else:
            return True


class DataSecurity:

    def __init__(self):
        key=b'eQ5jxFcJNYII5Z4vhBtvT-mNiqx64yQEUln1SOoYEDA='
        self.fernet=Fernet(key)


    def enc(self,data):
        data=bytes(data,'utf-8')
        data=self.fernet.encrypt(data)
        data=data.decode()
        return data

    def dec(self,data):
        data=bytes(data,'utf-8')
        data=self.fernet.decrypt(data)
        data=data.decode()
        return data

    def encPassword(self,password):
        passw=self.enc(password)
        return passw


    def decPassword(self,password):
        passw=self.dec(password)
        return passw


    def genUserName(self):
        user=str(int(time.time()*1000))+'_user'
        return user
