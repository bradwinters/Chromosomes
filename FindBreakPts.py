import sys 

def NiceList(pList):

    OutString="("
    for e in range(1,len(pList)):
        OutString+=pList[e]+" " 

    #preO=OutString[:len(OutString)-1]    
    preO=OutString[:-1]    
    preO+=")"
    return preO



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
print(intList)
print("REad in the file")
nplus1='+'+str(len(intList))
intList.append(nplus1)
print(intList)
print("Convert to integers")

y=list(map(lambda x : int(x),intList))
print(y)
#x=list(filter(lambda x: y[x] - y[x+1] == -1, y))
Adjacent=0
BreakPt=0
for bp in range(len(y)-1):
    print(bp)
    if y[bp]-y[bp+1]==-1:
       Adjacent+=1
    else:
       BreakPt+=1

# Show it in the output format
FinalList=NiceList(intList)
print(FinalList)
print("Adjacnet Points",Adjacent)
print("Break Points",BreakPt)

