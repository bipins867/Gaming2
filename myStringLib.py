#my
import myStringLib as ms
import threading
import time
import re
import random

def modifySqlResult(result):
        res=result
        
        
        if( res is None or len(res)==0 ):
            return None
        else:
            nres=[]
            if(len(res[0])==1):
                
                for i in res:
                    nres.append(i[0])
                return nres
            else:
                return res

def genRandStr(length):
	d=''
	for i in range(length):
		d=d+chr(random.randint(60,120))
	return d

def getPos1(words,agent):
    pos=[m.start() for m in re.finditer(agent,words)]

    tpos=[]
    for i in pos:
        tpos.append(i)
    return tpos

def getPos(words,agent):
    pos=[m.start() for m in re.finditer(agent,words)]

    tpos=[]
    for i in pos:
        tpos.append([i,i+len(agent)])
    return tpos

def getFirstPos(word,agent,limit=2):
    pos=ms.getPos(word,agent)
    p=[]
    for i in pos:
        p.append(i[0])

    return p[:limit]

def distributeString(words,agent=' '):
        words=words.split(agent)
        return words

def mergeInString(word,agent,typeStr=True):
        if not typeStr:
                fword=[]
                for i in word:
                        fword.append(str(i))
                word=fword
        agent=agent.join(word)
        return agent

def trimString(word,agent):
    word=word.strip(agent)
    return word


def replaceBy_String(st,word,agent=' '):
    st=st.replace(word,agent)
    return st


def check_word(data,word):
    if word in data:
            return data.index(word)
    else:
            return False

def check_get_word(data,word):
    pos=getPos1(data,word)
    if pos==[]:
        return [False,pos]
    else:
        return [True,pos]


def find_mid_text(data,start,end):
    
    cond1=check_word(data,start)
    cond2=check_word(data,end)
    
    if str(cond1) !='False' and str(cond2)!='False':
            string=data
            index1=string.index(start)+len(start)
            index2=string.index(end)
            txt=string[index1:index2]
            return txt
    else:
            return False
#get rhs data

def get_rhs_data(data,start):
    cond=check_word(data,start)
    if str(cond)!='False':
        index=data.index(start)
        return data[index+len(start):]
    else:
            return None

def get_lhs_data(data,end):
    cond=check_word(data,end)
    if str(cond)!='False':
        index=data.index(end)
        return data[:index]
    else:
            return None

def equalWord(word1,word2,trim=True):


    if trim:

        word1=trimString(word1,' ')
        word2=trimString(word2,' ')
    len1=len(word1)
    len2=len(word2)
    con=[]
    if(len1 ==len2):
        for i in range(0,len1):
            l1=word1[i]
            l2=word2[i]


            if(l1==l2):
                con.append('t')
            elif(l1==l2.lower()):
                con.append('t')
            elif(l1==l2.upper()):
                con.append('t')
            else:

                con.append('f')
                break

    else:
        con.append('f')
    if('f' in con):
        return False
    else:
        return True

def inEqual(word,array):

    con=[]
    for i in array:
        if(equalWord(word,i)):
            con.append('t')
            break
        else:
            con.append('f')

    if('t' in con):
        return True
    else:
        return False



def inMultipleEqual(array1,array2):
    con=False
    for i in array1:
        if(ms.inEqual(i,array2)):
            con=True
            break

    return con
