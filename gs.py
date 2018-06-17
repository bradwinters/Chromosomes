import sys 

def NiceList(pList):

    OutString="("
    for e in range(1,len(pList)):
        OutString+=pList[e]+" " 

    #preO=OutString[:len(OutString)-1]    
    preO=OutString[:-1]    
    preO+=")"
    return preO

def isSorted(pk,aList):
    ''' Assume its sorted, look for out of order elements and note them
    '''
    Sorted=False
    #print("Check sign, Compare ",aList[pk]," to ",pk)
    xx=abs(int(aList[pk]))
    yy=abs(int(pk))
    #print("Check sign, Compare ",xx," to ",yy)
    if xx==yy:
       Sorted=True
    
    return Sorted

def sabs(aString):
    tString=""

    tString=abs(int(aString))
    return str(tString)

def FlipIt(aList):
    # convert a list of strings to a reversed sign flipped list
    # +5 -3 -9 will become +9 +3 -5
   
    aList=aList[::-1] 
    #print("****",aList)
    
    NumberList=[]
    OutList=[]

    # convert to a number list
    for e in range(len(aList)):
       tt=int(aList[e]) * -1
       NumberList.append(tt)
   
    # convert back to string list
    for e in range(len(NumberList)):
       if NumberList[e] < 0:
          x=str(NumberList[e])
          OutList.append(x)
       elif NumberList[e] >= 0:
          x='+'+str(NumberList[e])
          OutList.append(x)

    #print("Returning ",OutList) 
    return (OutList)

def ksortRev(pk,pP):
    
    newP=pP
    pPlen=len(pP)
    J=sabs(pk) 
    toFlip=[]
    preFix=pP[:pk]
    markr=0
    for i in range(pk,pPlen):
        if sabs(pP[i])==J:
           markr=i
    markr+=1
    suffix=pP[pk:markr]

    toFlip=FlipIt(suffix)
    cutOld=pP[markr:]
    #print("Prefix: ",preFix," First: ",toFlip," second: ",cutOld)
    newString=preFix+toFlip+cutOld
    # fishhead
    ThenewString=NiceList(newString)
    print(ThenewString)

    return  newString

def GreedySorting(P):
   
    pLen=len(P) 
    RevDist=0
    sorted=False
    for k in range(pLen):
        sorted=isSorted(k,P)
        if sorted==False: 
            P=ksortRev(k,P)
            RevDist=RevDist+1
        if P[k][0] == '-':
           plusIt(P,k)
           RevDist=RevDist+1
  
    return RevDist,P

def plusIt(aList,anIndex):
      
    Val=abs(int(aList[anIndex]))
    newVal="+"+str(Val)
    aList[anIndex]=newVal
    ThenewString=NiceList(aList)
    print(ThenewString)
       
    return aList

def ModeList(pintList):
    Min =99999
    Max =-99999
    for e in pintList:
        #print(":",e,":")
        E=abs(int(e))
        if E < Min:
            Min=E
        if E > Max:
            Max=E

    #print("Max is ", Max)
    #print("Min is ", Min)
    span=Max-Min+1
    OrdList=[]
    for j in range(Min,Max+1):
       mu='+'+str(j)
       OrdList.append(mu)
    return OrdList

def readData():
    lines = sys.stdin.read().splitlines() 

    #for i in range(len(lines)):
    #    print('Line ' + str(i+1)+' is '+str(len(lines[i]))+' characters long.')

    stri=""
    for j in lines:
        stri+=j

    jj=stri.split()
    vals=["+0"]
    for m in jj:
        q=m.strip("(")
        r=q.strip(")")
        #s=r.strip("+")
        vals.append(r)

    return(vals)


intList=readData()

# Create the target model arrangement with just getting min/max
Mlist=ModeList(intList)
#print(Mlist)

ans,Flist=GreedySorting(intList)
FinalAns=NiceList(Flist)
#print(ans)
#print(FinalAns)


