import myStringLib as ms
import dbquery2 as db
import mysql.connector
import sshtunnel
import MySQLdb
'''
def genMdb(host='bipins8671.mysql.pythonanywhere-services.com',passwd='shivangisingh'):

    mydb=mysql.connector.connect(
        host=host,
        database='bipins8671$GamingWorld',
        user='bipins8671',
        passwd=passwd,
        #charset='utf8'
        )

    return mydb

'''
def genMdb(host='localhost',passwd='bipinsingh'):
#def genMdb(host='34.28.125.151',passwd='bipinsingh'):

    mydb=mysql.connector.connect(
        host=host,
        user='root',
        passwd=passwd,
        #charset='utf8'
        )

    return mydb


def genBySSHTunnel():

    tun=sshtunnel.SSHTunnelForwarder(('ssh.pythonanywhere.com'),
                                     ssh_username='bipins8671',
                                     ssh_password='Bipin@867',
                                     remote_bind_address=('bipins8671.mysql.pythonanywhere-services.com', 3306),
                                     )
    tun.start()

    mydb=MySQLdb.connect(
                host='127.0.0.1',
                db='bipins8671$GamingWorld',
                user='bipins8671',
                passwd='shivangisingh',
                port=tun.local_bind_port,
                #charset='utf8'
                )

    return mydb

class cb1:
    def __init__(self,mycursor,database=None,isssh=False):
        self.mycursor=mycursor

        if not isssh:
            self.database=database
            
            try:
                
                self.mycursor.execute('use '+database);
            except:
                self.mycursor.execute('create database '+database)
                self.mycursor.execute('use '+database);
                print("Database not found \nCreating New One");


    def getNextColByLength(self,tableName,ident,length):
        cb=db.cb1(self.mycursor,self.database)
        cols=cb.getColName(tableName)
        if(ident in cols):

            index=cols.index(ident)
            index=index+length-1
            if(len(cols)-2>=index):
                if(index<-1):
                    print('out of range')
                else:

                    return cols[index+1]
            else:
                print('out of range')
        else:
            print('cols is not present in table')


    def getPrevColByLength(self,tableName,ident,length):
        length=-length
        dataa=self.getNextColByLength(tableName,ident,length)

        return dataa

    def getColByData(self,tableName,word):
        cb=db.cb1(self.mycursor,self.database)

        cols=cb.getColName(tableName)
        data=[]

        for i in cols:
            cond=cb.checkData(tableName,i,word)
            if(cond):
                data.append(i)

        data=ms.modifySqlResult(data)

        return data

    def getAftColByCol(self,tableName,col):
        cb=db.cb1(self.mycursor,self.database)
        cols=cb.getColName(tableName)
        ind=cols.index(col)

        data=cols[ind+1:]

        return data

    def getBefColByCol(self,tableName,col):
        cb=db.cb1(self.mycursor,self.database)
        cols=cb.getColName(tableName)
        ind=cols.index(col)

        data=cols[:ind]

        return data



    def executeSqlFormula(self,sqlFormula,modifyRes=False,isReturn=True,values=None):
        if values is None:
            self.mycursor.execute(sqlFormula)
        else:
            self.mycursor.execute(sqlFormula,values)

        #print("-------------------------------------------------------")
        #print(sqlFormula)
        if isReturn:
            res=self.mycursor.fetchall()
            if modifyRes:
                res=ms.modifySqlResult(res)
            #print(res)
            return res


    def showTablesByLike(self,like):
        sqlFormula='show tables like "{0}"'.format(like)
        return ms.modifySqlResult(self.executeSqlFormula(sqlFormula))


    def getColName(self,tableName):
        sqlFormula='desc '+tableName
        table=self.showTables()

        if(table is None or (not ms.inEqual(tableName,table))):
            return None
        else:


            self.mycursor.execute(sqlFormula)
            res=self.mycursor.fetchall()

            field=[]
            for i in res:
                field.append(i[0])
            return field


    def showTables(self):
        sqlFormula='show tables'
        return ms.modifySqlResult(self.executeSqlFormula(sqlFormula))

    def selectAllData(self,tableName,part='*'):
        sqlFormula='select '+part+' from '+tableName

        return self.executeSqlFormula(sqlFormula)

    def selectParticularData(self,tableName,field1,field2,word):
        sqlFormula='select '+field2 +' from '+tableName+' where '+field1 +' = "'+word+'"'
        return self.executeSqlFormula(sqlFormula)

    def selectAllDataByCondition(self,tableName,field,word,part='*'):
        word=str(word)
        sqlFormula='select '+part+' from '+tableName+' where '+field +' = "'+word+'"'
        #print(sqlFormula)
        return self.executeSqlFormula(sqlFormula)

    def selectAllLikeData(self,tableName,field,like):
        sqlFormula='select * from {0} where {1} like "{2}"'.format(tableName,field,like)
        res= self.executeSqlFormula(sqlFormula)
        res=ms.modifySqlResult(res)
        return res

    def selectWhByWhCheck(self,tableName,word):
        cb=db.cb1(self.mycursor,self.database)
        col=cb.getColName(tableName)
        data=[]
        for i in col:
            d=cb.selectByMulAndCond(tableName,[i],[word])


            if(d is not None ):
                for i in d:


                        data.append(i)



        if(len(data)==0):
           return None
        else:
            return data

    def selectByMulOrCondNot(self,tableName,fields,words,f,w,part='*'):

        values=[]
        for i in range(0,len(fields)):
            d=fields[i]+'="'+words[i]+'" '
            values.append(d)

        val=[]
        for i in range(0,len(f)):
            d=f[i]+'!="'+w[i]+'" '
            val.append(d)
        values=ms.mergeInString(values,' or ')
        val=ms.mergeInString(val,' and ')

        sqlFormula='select '+part+' from {0} where ({1}) and {2}'.format(tableName,values,val)
        #print(sqlFormula)
        return self.executeSqlFormula(sqlFormula)

    def selectByMulOrCond(self,tableName,fields,words,part='*'):

        values=[]
        for i in range(0,len(fields)):
            d=fields[i]+'="'+words[i]+'" '
            values.append(d)

        values=ms.mergeInString(values,' or ')
        sqlFormula='select '+part+' from {0} where {1}'.format(tableName,values)
        #print(sqlFormula)
        return self.executeSqlFormula(sqlFormula)


    def selectByMulAndCond(self,tableName,fields,words,part='*'):

        values=[]
        for i in range(0,len(fields)):
            d=fields[i]+'="'+words[i]+'" '
            values.append(d)

        values=ms.mergeInString(values,' and ')
        sqlFormula='select '+part+' from {0} where {1}'.format(tableName,values)
        #print(sqlFormula)
        return self.executeSqlFormula(sqlFormula)



    def selectRangeData(self,tableName,field,r1,r2,part='*'):
        sqlFormula='select '+part+' from {0} where {1} >= {2} and {3}<={4}'.format(tableName,field,r1,field,r2)

        return self.executeSqlFormula(sqlFormula)

    def selectGreaterFieldData(self,tableName,field,value,gretType='<=',part='*'):
        sqlFormula='select {0} from {1} where  {2}{3}{4}'.format(part,tableName,field,gretType,value)
        return self.executeSqlFormula(sqlFormula)

    def selectRangeDataByTwoCol(self,tableName,uppField,lowField,val,part='*'):
        sqlFormula='select '+part+' from {0} where {1} >= {2} and {3}<={4}'.format(tableName,uppField,val,lowField,val)

        return self.executeSqlFormula(sqlFormula)

    def selectRangeDataByMulCond(self,tableName,xField,xValue,field,r1,r2,part='*',nots=True):
        if nots:
            sqlFormula='select '+part+' from {0} where {1} >= {2} and {3}<={4} and {5}="{6}"'.format(tableName,field,r1,field,r2,xField,xValue)
        else:
            sqlFormula='select '+part+' from {0} where {1} >= {2} and {3}<={4} and {5}!="{6}"'.format(tableName,field,r1,field,r2,xField,xValue)

        #print(sqlFormula)
        return self.executeSqlFormula(sqlFormula)

    def selectFieldByCond(self,tableName,fieldsAr,fields,values):
        #[] [] []
        fieldsAr=ms.mergeInString(fieldsAr,',')
        temp=[]
        for  i in range(0,len(values)):

            fi=fields[i]
            val=values[i]
            d=fi+'="'+val+'"'
            temp.append(d)

        temp=ms.mergeInString(temp,' and ')
        sqlFormula='select {0} from {1} where {2}'.format(fieldsAr,tableName,temp)
        return self.executeSqlFormula(sqlFormula)

    def selectSomeField(self,tableName,fields,values):
        temp=[]
        for  i in range(0,len(values)):

            fi=fields[i]
            val=values[i]
            d=fi+'="'+val+'"'
            temp.append(d)

        temp=ms.mergeInString(temp,' and ')
        sqlFormula='select * from {1} where {2}'.format(tableName,temp)
        return self.executeSqlFormula(sqlFormula)

    def selectAllParticularData(self,tableName,field1,field2,word):
        sqlFormula='select '+field2 +' from '+tableName+' where '+field1 +' = "'+word+'"'
        return self.executeSqlFormula(sqlFormula)

    def selectInRangeByValue(self,tableName,rField,value):
        data=[]

        for i in rField:
            d=self.selectByMulAndCond(tableName,[i],[value])
            if(len(d)==0):
                continue
            if(d is not None):
                data.append(d)


        return data

    def selectInRangeByCondValue(self,tableName,rField,value,cFields,cValue):
        data=[]

        for i in rField:
            tempf=[]
            tempv=[]
            tempf=[i]+cFields
            tempv=[value]+cValue
            d=self.selectByMulAndCond(tableName,tempf,tempv)
            if(len(d)==0):
                continue
            if(d is not None):
                for i in d:
                    data.append(i)


        return data


    def selectFieldData(self,tableName,field='*'):
        sqlFormula='select '+ field +' from '+tableName

        return self.executeSqlFormula(sqlFormula)

    def selectFieldLikeData(self,tableName,reqField,field,like):
        sqlFormula='select {0} from {1} where {2} like "{3}"'.format(reqField,tableName,field,like)
        return self.executeSqlFormula(sqlFormula,modifyRes=True)

    def selectRandomWithLike(self,tableName,field,like,reqField='*',limit=2):
        sqlFormula=f'select {reqField} from {tableName} where {field} like "{like}" order by rand() limit {limit}'

        return self.executeSqlFormula(sqlFormula,modifyRes=True)

    def selectRandomData(self,tableName,fields='*',limit=2):

        sqlFormula=f'select {fields} from {tableName} order by rand() limit {limit}';

        return self.executeSqlFormula(sqlFormula)

    def selectDataFrom1NotExistIn2(self,tableName1,tableName2,commonColumn,fieldSel='*',limit=1000):
        sqlFormula=f'select {fieldSel} from {tableName1} where {tableName1}.{commonColumn} not in (select {commonColumn} from {tableName2}) limit {limit} '

        return self.executeSqlFormula(sqlFormula)

    def deleteData(self,tableName):
        sqlFormula='delete from {0}'.format(tableName)

        return self.executeSqlFormula(sqlFormula,isReturn=False)

    def deleteBySingleCond(self,tableName,field,value):
        sqlFormula='delete from {0} where {1} ="{2}"'.format(tableName,field,value)

        return self.executeSqlFormula(sqlFormula,isReturn=False)

    def deleteBySingleRangeCond(self,tableName,field,value,less=True):
        xr1='>='
        xr2='<='

        if less:
            xr=xr2
        else:
            xr=xr1


        sqlFormula='delete from {0} where {1}{2}{3}'.format(tableName,field,xr,value)

        return self.executeSqlFormula(sqlFormula,isReturn=False)

    def deleteByMulAndCon(self,tableName,fields,values):
        if(len(fields)==len(values)):
            con=[]
            for i in range(0,len(fields)):
               field=fields[i]
               value=values[i]
               co=field+'="'+value+'"'
               con.append(co)

            condition=ms.mergeInString(con,' and ')

            sqlFormula='delete from {0} where {1}'.format(tableName,condition)
            return self.executeSqlFormula(sqlFormula,isReturn=False)
        else:
            print('error : values length are not same')

    def deleteByMulOrCon(self,tableName,fields,values):
        if(len(fields)==len(values)):
            con=[]
            for i in range(0,len(fields)):
               field=fields[i]
               value=values[i]
               co=field+'="'+value+'"'
               con.append(co)

            condition=ms.mergeInString(con,' or ')

            sqlFormula='delete from {0} where {1}'.format(tableName,condition)
            return self.executeSqlFormula(sqlFormula,isReturn=False)
        else:
            print('error : values length are not same')


    def createTable(self,tableName,fields,size):
        length=len(fields)
        tables=self.showTables()
        if (tables is None):
                string=''

                for i in range(0,length):
                    string=string+fields[i] +' varchar ('+str(size[i])+'),'

                string=string[:-1]


                sqlFormula= sqlFormula='create table '+tableName+ '('+string+')'#print(sqlFormula)
                self.executeSqlFormula(sqlFormula,isReturn=False)
                return True
        else:
            if(ms.inEqual(tableName,tables)):

                return False
            else:

                string=''

                for i in range(0,length):
                    string=string+fields[i] +' varchar ('+str(size[i])+'),'

                string=string[:-1]


                sqlFormula= 'create table '+tableName+ '('+string+')'#print(sqlFormula)
                self.executeSqlFormula(sqlFormula,isReturn=False)
                return True


    def createTableTextSize(self,tableName,fields,fieldType='longtext'):
        length=len(fields)
        tables=self.showTables()
        if (tables is None):
                string=''

                for i in range(0,length):
                    string=string+fields[i] +' '+fieldType+' ,'

                string=string[:-1]


                sqlFormula= sqlFormula='create table '+tableName+ '('+string+')'#print(sqlFormula)

                self.executeSqlFormula(sqlFormula,isReturn=False)
                return True
        else:

            if(False):

                return False
            else:

                string=''

                for i in range(0,length):
                    string=string+fields[i] +' '+fieldType+' ,'

                string=string[:-1]


                sqlFormula= 'create table '+tableName+ '('+string+')'#print(sqlFormula)

                self.executeSqlFormula(sqlFormula,isReturn=False)
                return True

    def checkTable(self,tableName):
        table=self.showTables()

        if(table is None or (not ms.inEqual(tableName,table))):
           return False
        else:
           return True


    def modifyColTable(self,tableName,field,size,text=True,ftype='varchar',isInt=False):

        sqlFormula=''
        if isInt:
             sqlFormula='alter table '+tableName+' modify '+field+' int'
        elif(text):
            sqlFormula='alter table '+tableName+' modify '+field+' text'
        else:
            sqlFormula='alter table '+tableName+' modify '+field+' '+ftype+'('+str(size)+')'

        return self.executeSqlFormula(sqlFormula,isReturn=False)

    def changeColTable(self,tableName,oldField,newField,size,text=True):
        sqlFormula=''
        if(text):
            sqlFormula='alter table '+tableName+' change '+oldField+' '+newField+' text'
        else:
            sqlFormula='alter table '+tableName+' change '+oldField+' '+newField+' varchar('+str(size)+')'

        return self.executeSqlFormula(sqlFormula,isReturn=False)

    def dropColTable(self,tableName,field):
        sqlFormula='alter table '+tableName+' drop '+field
        return self.executeSqlFormula(sqlFormula,isReturn=False)

    def addColTable(self,tableName,field,size,text=True):
        sqlForumal=''

        if(text):
            sqlFormula='alter table '+tableName+' add ' +field+' text'
        else:
            sqlFormula='alter table '+tableName+' add '+field+' varchar('+str(size)+')'

        return self.executeSqlFormula(sqlFormula,isReturn=False)

    def checkingWords(self,words):


        for i in words:
            first=i[0]
            data=self.selectAllData(first)
            #print(data,i)
            if(data==None):
                print('hii')
                return False
            elif(ms.inEqual(i,data)):
                return True
            else:
                return False
    #Adding identity field to the tables from a-z

    def addColumns(self,tableName):
        sqlQuery='alter table '+tableName+' change identifies identity  text'

        self.executeSqlFormula(sqlFormula,isReturn=False)

        return True
    def updateParticularData(self,tableName,field1,field2,word,value):
        sqlFormula='update '+tableName+ ' set '+  field2+ '="'+value+'" where '+field1+'="'+word+'"'

        self.executeSqlFormula(sqlFormula,isReturn=False)
    #Simple insertion of data into the table
    #For alfabates table Only
    def updateDataByMulCond(self,tableName,fields,values,field,value,isStr=True):

        xt=''
        for i in range(len(fields)):
            f=fields[i]
            v=values[i]

            a=' {0}="{1}"'.format(f,v)
            if i!=len(fields)-1:
                a=a+' and'
            xt=xt+a
        if isStr:
            sqlFormula='update '+tableName+ ' set '+  field+ '="'+value+'" where '+xt
        else:
            sqlFormula='update '+tableName+ ' set '+  field+ '='+str(value)+' where '+xt
        #print(sqlFormula)
        self.executeSqlFormula(sqlFormula,isReturn=False)

    #Inserting the word in alfabates


    def insertInAlfa(self,word,identity):
        tableName=word[0]
        cols=self.getColName(tableName)
        data=self.selectAllData(tableName)
        dic={}


        if data==None:

            newIdentity=ms.mergeString(identity,'/')
            sqlFormula='insert into '+tableName+ ' values("'+word+'","'+newIdentity+'")'

            self.executeSqlFormula(sqlFormula,isReturn=False)
        else:
            d1=[]
            for i in data:
                dic.__setitem__(i[0].lower(),i[1].lower())
                d1.append(i[0].lower())

            if(ms.inEqual(word,d1)):

                ident=dic[word]

                dis=ms.distributeString(ident,'/')

                nident=ms.sortOut(dis,identity)
                newmid=ms.mergeString(nident,'/')
                self.updateParticularData(tableName,cols[0],cols[1],word,newmid)

            else:
                newIdentity=ms.mergeString(identity,'/')
                sqlFormula='insert into '+tableName+ ' values("'+word+'","'+newIdentity+'")'
                self.executeSqlFormula(sqlFormula,isReturn=False)


    #Identity table creation and inserting the values in it
    def insertInIdentity(self,word,identity):
        tables=self.showTables()

        oddTables=ms.oddOut(tables,identity)
        #Table creation if not present
        if(len(oddTables)==0):
            pass
        else:
            for i in oddTables:
                field=['word']
                size=[100]
                self.createTable(i,field,size)

        for i in identity:
            data=self.selectAllData(i)

            if(data ==None):
                sqlFormula='insert into '+i+ ' values("'+word+'")'

                self.executeSqlFormula(sqlFormula,isReturn=False)
            else:
                if(ms.inEqual(word,data)):
                    pass
                else:
                    sqlFormula='insert into '+i+ ' values("'+word+'")'
                    self.executeSqlFormula(sqlFormula,isReturn=False)

    def checkMulAndData(self,tableName,fields,words):

        aftw=[]
        for i in range(0,len(fields)):
            field=fields[i]
            word=words[i]

            d=field+'="'+word+'" '
            aftw.append(d)

        aftw=ms.mergeInString(aftw,'and ')

        sqlFormula='select * from {0} where {1}'.format(tableName,aftw)

        res=self.executeSqlFormula(sqlFormula)

        if(res is None or  len(res)==0):
            return False
        else:
            return True


    def checkMulOrData(self,tableName,fields,words):

        aftw=[]
        for i in range(0,len(fields)):
            field=fields[i]
            word=words[i]

            d=field+'="'+word+'" '
            aftw.append(d)

        aftw=ms.mergeInString(aftw,'or ')

        sqlFormula='select * from {0} where {1}'.format(tableName,aftw)

        res=self.executeSqlFormula(sqlFormula)

        if(res is None or  len(res)==0):
            return False
        else:
            return True

    def checkData(self,tableName,field,word):

        sqlFormula='select * from '+tableName+' where '+field+'="'+word+'"'
        #print(sqlFormula)
        res=self.executeSqlFormula(sqlFormula)

        temp=[]
        if(len(res)==0 or res is None):
            return False
        else:
            return True

    #Check Data By Condition
    #Table and in Range of columns get the Value

    def checkDataInRField(self,tableName,rField,value):
        con=False
        for i in rField:
            c=self.checkData(tableName,i,value)
            if(c):
                con=True
                break

        return con
    #_ [] [] [] _
    def checkDataInRFieldCond(self,tableName,cFields,cValues,rField,value):
        con=False
        for i in rField:
            c=self.checkDataCond(tableName,cFields+[i],cValues+[value])
            if(c):
                con=True
                break

        return con


    def checkDataCond(self,tableName,fields,words):

        sen=[]
        for i in range(0,len(fields)):
            d=fields[i]+'="'+words[i]+'"'
            sen.append(d)

        sen=ms.mergeInString(sen,' and ')

        sqlFormula='select * from {0} where {1}'.format(tableName,sen)

        res=self.executeSqlFormula(sqlFormula)

        if(res is None or len(res)==0):
            return False
        else:
            return True


    def checkWholeTable(self,tableName,word):
        col=self.getColName(tableName)
        con=False
        for i in col:
            if(self.checkData(tableName,i,word)):
                con=True
                break
        return con
    #Now merging two words
    def createOneColTable(self,tableName):
        tables=self.showTables()
        field=['word']
        size=[100]
        if(tables is None):


            self.createTable(tableName,field,size)

        else:
            if(ms.inEqual(tableName,tables)):
                pass
            else:
               self.createTable(tableName,field,size)

    def updateParticularDataByAdding(self,tableName,field1,field2,word1,word2):
        data=self.selectParticularData(tableName,field1,field2,word1)

        if((data is None) or ms.equalWord(data,'_NULL') or data==''):
            self.updateParticularData(tableName,field1,field2,word1,word2)
        else:
            if(ms.equalWord(word2,'_NULL')):
                pass
            else:
                if(ms.equalWord(data,word2)):
                    pass
                else:

                    deta=ms.slashMakerDataIdentity(data,[word2])

                    self.updateParticularData(tableName,field1,field2,word1,deta)


    def insertSomeData(self,tableName,field1,field2,word1,word2):
        tables=self.showTables()

        if(tables is None):
            self.createOneColTable(tableName)
        else:
            if(ms.inEqual(tableName,tables)):
                pass
            else:
                self.createOneColTable(tableName)

        col=self.getColName(tableName)

        if(ms.inEqual(field1,col)):
            pass
        else:
            self.addColTable(tableName,field1,34)

        col=self.getColName(tableName)

        data=self.selectFieldData(tableName,'word')

        if(data is None or(not ms.inEqual(word1,data))):
            self.insertTwoDataOnly(tableName,field2,word1,word2)
        else:
            self.updateParticularDataByAdding(tableName,field1,field2,word1,word2)

    def insertDataN(self,tableName,values,typeStr=True):
        values=ms.mergeInString(values,'","',typeStr)

        sqlFormula='insert into {0} values ("{1}")'.format(tableName,values)

        #print(sqlFormula)

        self.executeSqlFormula(sqlFormula,isReturn=False)

    def insertData(self,tableName,*values):
        field=self.getColName(tableName)
        if(len(values)==1):
            value=values[0]
            sqlFormula='insert into '+tableName+ ' values("'+value+'")'

            self.executeSqlFormula(sqlFormula,isReturn=False)
        else:

            fields=ms.mergeInString(field,',')
            fields=fields
            val=''
            for i in field:
                val=val+'%s,'
            val=val[:-1]

            sqlFormula='insert into  '+tableName+'('+fields+') values('+val+')'
            self.executeSqlFormula(sqlFormula,isReturn=False,values=values)

    def insertOneFieldData(self,tableName,word):

        if(not self.checkData(tableName,'word',word)):
            self.insertData(tableName,word)

    def insertTwoFieldData(self,tableName,word1,word2):
        col=self.getColName(tableName)
        data=self.selectFieldData(tableName,'word')
        if(self.checkData(tableName,'word',word1)):
            parData=self.selectParticularData(tableName,col[0],col[1],word1)


            st=ms.slashAddData(parData,word2)

            self.updateParticularData(tableName,col[0],col[1],word1,st)


        else:

            self.insertData(tableName,word1,word2)

    def insertTwoDataOnly(self,tableName,field,value1,value2):
        sqlFormula='insert into '+tableName+'(word,'+field+')'+ 'values ("'+value1+'","'+value2+'")'
        self.executeSqlFormula(sqlFormula,isReturn=False)

    def insertTwoInOne(self,word1,identity1,word2,identity2):
        tables=ms.makePair(identity1,identity2)
        dtable=self.showTables()

        outTables=ms.oddOut(dtable,tables)

        #Table is created

        if(len(outTables)==0):
            pass
        else:

            for i in outTables:
                fields=['word1','word2']
                size=[100,100]
                self.createTable(i,fields,size)

        for i in tables:

            data=self.selectAllData(i)
            if(data==None):
                sqlFormula='insert into '+i+' values ("'+word1+'","'+word2+'")'
                self.executeSqlFormula(sqlFormula,isReturn=False)
            else:
                dic=ms.makeDictionary(data)

                d1=[]
                for ni in data:
                    d1.append(ni[0])

                if(ms.inEqual(word1,d1)):
                    wo=dic[word1]
                    if(ms.equalWord(wo,word2,trim=True)):
                        pass
                    else:
                        sqlFormula='insert into '+i+' values ("'+word1+'","'+word2+'")'
                        self.executeSqlFormula(sqlFormula,isReturn=False)
                else:
                    sqlFormula='insert into '+i+' values ("'+word1+'","'+word2+'")'
                    self.executeSqlFormula(sqlFormula,isReturn=False)

    def checkInData(self,tableName,word,field='word'):

        sqlFormula='select * from '+tableName+' where '+field+'="'+word+'"'

        res=self.executeSqlFormula(sqlFormula)

        temp=[]
        if(len(res)==0 or res is None):
            return False
        else:
            return True

    def insertInOnlyField(self,tableName,word1,word2,field):

        sqlFormula='insert into '+tableName+' (word,'+field+')'+' values ("'+word1+'","'+word2+'")'

        self.executeSqlFormula(sqlFormula,isReturn=False)

    def selectAllCheckData(self,tableName,field,word):
        sqlFormula='select * from '+tableName+'  where '+field+'="'+word+'"'

        res=self.executeSqlFormula(sqlFormula)

        temp=[]
        if(len(res)==0 or res is None):
            return None
        else:
            temp=[]
            if(len(res[0])==1):
                for i in  res:
                    temp.append(i[0])

            else:
                temp=res

            return temp


    def selectOnlyFieldAllData(self,tableName,word,field='word',field2='word'):
        sqlFormula='select '+field2+' from '+tableName+'  where '+field+'="'+word+'"'

        res=self.executeSqlFormula(sqlFormula)

        temp=[]
        if(len(res)==0 or res is None):
            return None
        else:
            temp=[]
            if(len(res[0])==1):
                for i in  res:
                    temp.append(i[0])

            else:
                temp=res

            return temp

    def insertInSpecialColumn(self,tableName,cols,values):
        if(len(cols)==len(values)):

            column=ms.mergeInString(cols,',')
            value=ms.mergeInString(values,'","')
            sqlFormula='insert into {0}({1}) values ("{2}")'.format(tableName,column,value)

            self.executeSqlFormula(sqlFormula,isReturn=False)
        else:
            print('Error : column length and values length are not equal')

    def dropTable(self,tableName):
        sqlFormula='drop table {0}'.format(tableName)

        self.executeSqlFormula(sqlFormula,isReturn=False)

    def dropAllTables(self):
        tables=self.showTables()

        if(tables is not None):
            for i in tables:
                self.dropTable(i)

    def checkCount(self,tableName,field,count,symbol='>'):

        sqlFormula='select * from {0} group by  {1} having count({2}){3}{4}'.format(tableName,field,field,symbol,count)

        data=self.executeSqlFormula(sqlFormula,modifyRes=True)

        if(data is None):
            return False
        else:
            return True

    def checkCountCond(self,tableName,field,count,fieldAr,valueAr,symbol='>'):

        sen=[]
        for i in range(0,len(fieldAr)):
            sen.append(fieldAr[i]+'="'+valueAr[i]+'"')

        sen=ms.mergeInString(sen,' and ')

        sqlFormula='select * from {0} where {1} group by  {2} having count({3}){4}{5}'.format(tableName,sen,field,field,symbol,count)

        data=self.executeSqlFormula(sqlFormula,modifyRes=True)

        if(data is None):
            return False
        else:
            return True

    def countValues(self,tableName):
        sqlFormula='select count(*) from {0}'.format(tableName)

        data=self.executeSqlFormula(sqlFormula,modifyRes=True)

        return data[0]

    def countByCond(self,tableName,fields,values):
        sen=[]
        for i in range(0,len(fields)):
            sen.append(fields[i]+'="'+values[i]+'"')

        sen=ms.mergeInString(sen,' and ')
        sqlFormula='select count(*) from {0} where {1}'.format(tableName,sen)
        data=self.executeSqlFormula(sqlFormula,modifyRes=True)

        return data[0]
