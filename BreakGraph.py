import sys 
import random
import re


def CycleCheck(Rings):
    C_cnt=0
    tC_cnt=0
    Node1=[]
    Node2=[]
    for Cyc in range(len(Rings)):
       print("Compare first and last") 
       Nde1=Rings[Cyc][0]
       Nde2=Rings[Cyc][-1]
       #print("Head: ",Rings[Cyc][0],"Tail: ",Rings[Cyc][-1]) 
       print("Head: ",Nde1," Tail: ",Nde2)
       if idMatch(Nde1,Nde2):
           print("Trivial cycle") 
           tC_cnt+=1
       elif partMatch(Nde1,Nde2): 
           print("Cycle of size ",len(Rings[Cyc])," confirmed")
           C_cnt+=1
       else:
           print("Somethings wrong, this is not a cycle")

    return tC_cnt, C_cnt

def makeList(pGeneGraph):
##  put bracked pairs into a list
    ##  merely a format change, list of 2 elemnt lists
    aNode=[]
    nodez=pGeneGraph.split(")")
    for e in nodez:
       matches=re.findall("\d+",e)
       if len(matches) > 0:
           matches[0]=int(matches[0])
           matches[1]=int(matches[1])
           aNode.append(matches)
    return aNode

################################################
#   Exact node match, a trivial cycle 
################################################
def idMatch(N1,N2):
    Match=False    

    if N1[0]==N2[0] and N1[1]==N2[1]:
       Match=True
    elif N1[0]==N2[1] and N1[1]==N2[0]:
       Match=True
       
    return Match 


#######################################################
#   partial node match, two edge pts match, a connect 
#######################################################
def partMatch(N1,N2):
    Match=False    

    if N1[0]==N2[0]: 
       Match=True
    elif N1[1]==N2[1]:
       Match=True
    elif N1[0]==N2[1]: 
       Match=True
    elif N1[1]==N2[0]:
       Match=True
       
    return Match 

def findCycles(pG1,pG2):
    allCycles=[]
    Cycle=[] 
    State=1
    ptr1=0
    ptr2=0
    SafeT=0
    G1=makeList(pG1)
    G2=makeList(pG2)
    print("In findCycles G1:",G1)
    print("In findCycles G2:",G2)
    idum=G1.pop(ptr1)
    Cycle.append(idum)
    aLoop=0
    #while len(G1) > 0 and len(G1) > 0:
    while len(G1) > 0:
       #print(">",aLoop)
       #print("ptr1:",ptr1," and ptr2:",ptr2)
       aLoop+=1
       while (State==1 and ptr2 < len(G2)):
          #print("compare ",Cycle[-1]," to ",G2[ptr2]," at ptr1:",ptr1," and ptr2:",ptr2)
          if partMatch(Cycle[-1],G2[ptr2]):
             Cycle.append(G2.pop(ptr2))
             #print("State:",State," ",Cycle)
             ptr2=0
             State=2
          else:
             ptr2+=1

       ptr1=0
       ptr2=0
       while (State==2) and ptr1 < len(G1):
          #print("compare ",Cycle[-1]," to ",G1[ptr1]," at ptr1:",ptr1," and ptr2:",ptr2)
          if partMatch(Cycle[-1],G1[ptr1]):
             Cycle.append(G1.pop(ptr1))
             #print("State:",State," ",Cycle)
             #print(G1," ",G2," ",ptr1," ",ptr2)
             ptr1=0
             State=1
          else:
             ptr1+=1
       #print("End of a cycle? ptr1=",ptr1," and ptr2 is ",ptr2)
       if ptr1 >= len(G1) or ptr2 >= len(G2):
          #print("Cycle has ended, no more to match ") 
          allCycles.append(Cycle)
          print("Found a cycle")
          print(Cycle)
          Cycle=[]
          if len(G1) > 0:
             Cycle.append(G1.pop(0))
          State=1
          ptr1=0   
          ptr2=0   
          #print("Bottom of while, allCycle is ",allCycles)
       else:
          #print("Cycle is not ended")
          pass
    if ptr1!=0 and ptr2!=0:
       print("Ptr1: ",ptr1," ptr2: ",ptr2)
       if partMatch(Cycle[-1],G2[ptr2]):
          Cycle.append(G2.pop(ptr2))
          allCycles.append(Cycle)

    if len(G1) > 0 or len(G2) > 0:
        print("Problem: Nodes remain")
        print("G1 is ",G1," and G2 is ",G2)
        print("Cycle is ",Cycle)
        if len(Cycle) > 0:
           Cycle.append(G2[0])
           allCycles.append(Cycle)
        else:
           allCycles[-1].append(G2[0])

    return allCycles 

def Match(N1,N2):
    Minus1=False
    Plus1=False
    #N1[1] tail
    #N2[0] heads
    # tail is even

    if ((N1[1]%2)==0): 
       Minus1=True
    else:
       Plus1=True

    if (Minus1):
       if N1[1]-N2[0]==1:
          return True

    else:
       if N1[1]-N2[0]==-1:
          return True

    return False

def buildRings(CGraph):
    Ring=[] 
    allRings=[] 

    print("In build rings with ",CGraph)
    #CGraph=[[2, 6], [5, 12], [11, 10], [9, 1], [4, 8], [7, 3]]
    StartNode=CGraph.pop(0)
    Ring.append(StartNode)
    print("First Start with ",StartNode)
    Lptr=0

    while (len(CGraph) >= 1):
       #print("*********CGraph is ",CGraph)
       #print("*********CGraph size is ",len(CGraph))
       #print("*********Ring is ",Ring)
       #print("*********StartNode is ",StartNode)
       #print("*********Lptr is ",Lptr)
       #print("allRings is ",allRings)

       for j in range(len(CGraph)):
           #print("Lptr is ",Lptr)
           #print("StartNode is ",StartNode)
           #print("I is ",CGraph[Lptr])
           if Match(StartNode,CGraph[Lptr]):
              NewFind=CGraph.pop(Lptr)
              #print("New find ",NewFind)
              Ring.append(NewFind)
              StartNode=NewFind
              #print("Start is now",StartNode)
           else:
              # keep looking
              Lptr+=1

       # end of the pass through
       # all rings are made, start a new ring and look
       Lptr=0
       allRings.append(Ring)
       print("allRing is now:=>",allRings)
       Ring=[]
       if len(CGraph) > 0:
          StartNode=CGraph.pop(0)
          Ring.append(StartNode)
       Lptr=0
   
    #allRings.append(Ring)
    #print("final: Ring is ",Ring)
    #print("final: allRing is ",allRings)
    #print("Graph should be empty, its size is ",len(CGraph))
    return allRings



#################################################
####   Core SubRoutines                ##########
#################################################

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def ChromoToList(aString):
    # Syntany blocks is a string in parens converted to a list of signed integers
    newList=[0]
    aString=aString.strip('(')
    aString=aString.strip(')')
    tList=aString.split()

    for x in range(len(tList)):
       newList.append(int(tList[x]))

    return newList
##########################################
#  Heres another chromosome to cycle on line 24 
##########################################
def ChromosomeToCycle(pChromo):
    '''
    Creates graph where odd numbers are the head, even the tail.
    Direction is preserved by the pairs being in order or not
    So 3,4 is clockwise, in order while 4,3 is reversed
    '''
    # convert a single chromosome into a cycle
    # represented as a sequence of integers in Nodes
    Nodes=[]
    for j in range(1,len(pChromo)):
       i=pChromo[j]
       if i > 0:
           ndx1=2*j-1
           ndx2=2*j
           Nodes.insert(ndx1,2*i-1)
           Nodes.insert(ndx2,2*i)
       else:
           ndx1=2*j-1
           ndx2=2*j
           Nodes.insert(ndx1,-2*i)
           Nodes.insert(ndx2,-2*i-1)

    return Nodes


def equalTups(tup1,tup2):

    #print("Comparing ",tup1," to ",tup2)
    if tup1==tup2:
       return True

    #print("Comparing ",tup1[0]," to ",tup2[1]," and ",tup1[1]," to ",tup2[0])
    if tup1[0]==tup2[1] and tup1[1]==tup2[0]:
       return True
    return False

def TBreakonGenomeGraph(pGeneGraph,a,b,c,d):
    print("************  at the start of TBreakonGenomeGraph, genomeGraph is")
    print(pGeneGraph)
    aNode=[]

    bp=[]    
    bp.append((a,b))
    bp.append((c,d))

    newBp=[]
    newBp.append((a,c))
    newBp.append((b,d))


    print("Find position of ",bp[0])
    print("and position of ",bp[1])
    ##  put bracked pairs into a list
    ##
    nodez=pGeneGraph.split(")")
    for e in nodez:
       matches=re.findall("\d+",e)
       if len(matches) > 0:
           matches[0]=int(matches[0])
           matches[1]=int(matches[1])
           aNode.append(matches)
    print("Only lists of pairs, all in one list")
    tupZ=[]
    for i in range(len(aNode)):
        tupZ.append((aNode[i][0],aNode[i][1])) 

    print("About to assign BreakPts found in tupZ:",tupZ)
    for x in range(len(tupZ)):
       if equalTups(bp[0],tupZ[x]):
          BreakPt1=x
    for x in range(len(tupZ)):
       if equalTups(bp[1],tupZ[x]):
          BreakPt2=x

    print("Breakpts are ",BreakPt1," and ",BreakPt2)

    #  first new pair goes in lowest, find that 
    if BreakPt1 < BreakPt2:
       bFirst=BreakPt1
       bSecond=BreakPt2
    elif BreakPt2 < BreakPt1:
       bFirst=BreakPt2
       bSecond=BreakPt1

    print("Positions are ",bFirst," and ",bSecond)
    print("***  breakage here, look closely   ******")
    print("output of tupZ ",tupZ)
    print("Change ",tupZ[BreakPt1]," and ",tupZ[BreakPt2]," to ",newBp[0]," and ",newBp[1])
    ###   Swap determined, now change them in the list
    ###   Loop thru to find the old tupZ[BreakPt1] and 2, substitute in the new ones
    ###   This one is in place
    print("tupZ before ",tupZ)
    print("find and delete ",bp[0])
    del tupZ[BreakPt1]
    print("find and delete ",bp[1])
    del tupZ[BreakPt2]
    #for xx in range(len(tupZ)):
    #   print("Comp ",tupZ[xx]," to ",bp[0])
    #   if tupZ[xx]==bp[0]:
    #      del tupZ[xx] 
    #   print("Comp ",tupZ[xx]," to ",bp[1])
    #   if tupZ[xx]==bp[1]:
    #      del tupZ[xx] 
    print("tupZ after deletion",tupZ)
    tupZ.append(newBp[0])
    tupZ.append(newBp[1])
    print("tupZ after adding new nodes")


    return tupZ 


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def GraphToGenome(pGeneGraph):
    aNode=[]

    ##  put bracked pairs into a list
    ##  merely a format change, list of 2 elemnt lists
    nodez=pGeneGraph.split(")")
    for e in nodez:
       matches=re.findall("\d+",e)
       if len(matches) > 0:
           matches[0]=int(matches[0])
           matches[1]=int(matches[1])
           aNode.append(matches)
    print("2:",aNode)

    # make the rings 
    allRings=buildRings(aNode)

    P=[]
    RingCnt=0
    for e in range(len(allRings)):
       GenomeGraph=allRings[e]
       fGenomeG=[]
       for x in range(len(GenomeGraph)):
           print(GenomeGraph[x][0],GenomeGraph[x][1])
           fGenomeG.append(GenomeGraph[x][0])
           fGenomeG.append(GenomeGraph[x][1])
       #print(fGenomeG) 
       Chromos=CycleToChromosome(fGenomeG)
       print(Chromos) 
       P.append(Chromos)
       RingCnt+=1


    return RingCnt, P 

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Line 175
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def ColoredEdges(pP):
    CEdges=[]
    print(pP)
    for element in pP:
       #print("Heres an element in pP ",element)
       Chromo=ChromoToList(element)
       #print("Heres the returned Chromosome ",Chromo)
       Nodes=ChromosomeToCycle(Chromo)
       #print("Appending to Nodes now",Nodes)
       Nodes.append(Nodes[0])
       Nodes.insert(0,0)
       #print("Back in Colored Edges with Nodes: ",Nodes)
       for j in range(1,len(Chromo)):
           ndx1=2*j
           ndx2=ndx1+1
           CEdges.append((Nodes[ndx1],Nodes[ndx2]))

    #print("Finished in Colored Edges with Nodes: ",CEdges)
    #print("")
    return CEdges




#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#  heres one of the C2C on line 200
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def ChromosomeToCycle(pChromo):
    '''
    Creates graph where odd numbers are the head, even the tail.  
    Direction is preserved by the pairs being in order or not
    So 3,4 is clockwise, in order while 4,3 is reversed
    '''
    print("Inside ChromosomeToCycle")
    # convert a single chromosome into a cycle 
    # represented as a sequence of integers in Nodes
    Nodes=[]
    for j in range(1,len(pChromo)):
       i=pChromo[j]
       if i > 0:
           ndx1=2*j-1
           ndx2=2*j
           Nodes.insert(ndx1,2*i-1)
           Nodes.insert(ndx2,2*i)
       else:
           ndx1=2*j-1
           ndx2=2*j
           Nodes.insert(ndx1,-2*i)
           Nodes.insert(ndx2,-2*i-1)

    return Nodes

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def CycleToChromosome(Nodes):
    #Nodes=ChromoToList(pString)
    #Nodes=Nodes[1:]
    print("In cycle2chromo")
    print(Nodes)
    print("Size of nodes ",len(Nodes))
    #zSize=int(len(Nodes)/2)+1
    zSize=int(len(Nodes)/2)
    print("zSize of nodes ",zSize)
    Chromosome=[]
    for j in range(zSize):
        print(j)
        ndx1=2*j-1
        ndx2=2*j
        if Nodes[ndx1] < (Nodes[ndx2]):
           Chromosome.insert(j,Nodes[ndx2]/2)
        else:
           Chromosome.insert(j,-Nodes[ndx1]/2)


    C=NiceList2(Chromosome)
    
    return C





#################################################
####   Utilities                       ##########
#################################################

#  ( 1 2 4 3 6 5...) to a list of just numbers.
def ChromoToList(aString):
    # Syntany blocks is a string in parens converted to a list of signed integers
    newList=[0]
    aString=aString.strip('(')
    aString=aString.strip(')')
    tList=aString.split()
    for x in range(len(tList)):
       newList.append(int(tList[x]))
       
    return newList

def NiceList2(pList):

    OutString="("
    for e in range(len(pList)):
        if pList[e] > 0:
            OutString+="+"+str(int(pList[e]))+" " 
        else:
            OutString+=str(int(pList[e]))+" " 

    #preO=OutString[:len(OutString)-1]    
    preO=OutString[:-1]    
    preO+=")"
    return preO

def NiceList(pList):

    OutString="("
    for e in range(len(pList)):
            OutString+=str(pList[e])+" " 

    #preO=OutString[:len(OutString)-1]    
    preO=OutString[:-1]    
    preO+=")"
    return preO

#####################################################
##    readData routines for various expected inputs
#####################################################
def readDataChromosomeBreak():
    ###  This read expects a chromosome on the first line followed by 4 integers, 2 pairs, that are break pts
    ###  
    ###  (+1 +2 +3 +4 +5 +6 +7 +8 +9 +10 +11 +12)
    ###  3 4 10 11 
    ##  It returns the four integers and a chromosome

    lines = sys.stdin.read().splitlines()
    Allines=[]
    Cnt=0
    for i in range(len(lines)):
       Cnt+=1
       if Cnt==1:
           startList=[]
           endList=[]
           aline=lines[i]
           for q in range(len(aline)):
               if aline[q]=='(':
                  startList.append(q)
               elif aline[q]==')':
                  endList.append(q)

           for x in range(len(startList)):
               Joe=aline[startList[x]:endList[x]+1]
               #print(Joe)
               Allines.append((Cnt,Joe))
           #print(Allines)
           print("-----------------------------")
       if Cnt==2:
           Is=lines[i] 

    return Is, Allines

def readDataGraph():
    ###  This read expects a chromosome on the first line followed by 4 integers, 2 pairs, that are break pts
    ###  
    ###  (+1 +2 +3 +4 +5 +6 +7 +8 +9 +10 +11 +12)
    ###  3 4 10 11 
    ##  It returns the four integers and a chromosome

    lines = sys.stdin.read().splitlines() 
    Allines=[] 
    Cnt=0
    for i in range(len(lines)):
       Cnt+=1
       if Cnt==1:
          aline=lines[i]
       elif Cnt==2:
          Is=lines[i] 
       else:
          print("Expected only 2 lines, more found")
          exit()
    print("-----------------------------")
    return Is, aline

#################################################################################
#   Read a file of chromosome sets. 2 typically. 
#   Set 1 may have multiple chromos, as well as 2
#   The routine returns 1 list, each element is a tuple where part 0 is is the 
#   chromosome set (line) and part two is the actual chromosome.
#   Each line will be part one of the list, a tuple, indicating the chromosome.  1 or 2
#   input:
#   line1:( +x +y -z -k  ...   ) ( +x +y -z -k  ...   ) ( +x +y -z -k  ...   )
#   line2:( +x +m -z -j  ...   )( +o +p -m -q  ...   ) ( +x +y -z -k  ...   )
#   product:
#   [1,( +x +y -z -k  ...   ) 1,( +x +y -z -k  ...   ) 1,( +x +y -z -k  ...   )
#   (2, +x +y -z_(-k  ...   )(2, +x +y -z -k  ...   ) (2, +x +y -z -k  ...   )]
#
#################################################################################
def readDataChromosomes():
    lines = sys.stdin.read().splitlines() 
    Allines=[] 
    Cnt=0
    for i in range(len(lines)):
       Cnt+=1
       startList=[]
       endList=[]
       aline=lines[i]
       for q in range(len(aline)):
           if aline[q]=='(':
              startList.append(q) 
           elif aline[q]==')':
              endList.append(q) 

       for x in range(len(startList)): 
           Joe=aline[startList[x]:endList[x]+1]
           #print(Joe)
           Allines.append((Cnt,Joe))
       #print(Allines)
       print("-----------------------------")


    return(Allines)

def CreateChrome(tupList,C):
    Chromo=[]
    for x in range(len(tupList)): 
        if tupList[x][0]==C:
            Chromo.append(tupList[x][1])
    return Chromo

#################################################
####   Main                            ##########
#################################################
#  read in a genome, convert it to a GeneGraph


Chromo=readDataChromosomes()
print("File read")
#print("Heres are the chromosomes, its a tupal, 0 element is the chrom number")
#print("1 element is the actual chromosome")
#
#  Create two lists, one for the source Chromosome and one for the target
#  Lists within both SrcChromosome and TrgChromosome contain ind strands
#
SrcChromo=[]
print("Pull out just the source chromosome, 1")
for e in Chromo:
    if e[0]==1:
       SrcChromo.append(e[1])
print("Src Chromosome list is ")
print(SrcChromo)
for srcC in SrcChromo:
    print("==>",srcC,"<==")

########
##  Process P
########
print("Send Source Chromo into Colored Edges") 
Edges= ColoredEdges(SrcChromo)
print(Edges)
BlocksCntP=0
aString=""
for e in Edges:
   BlocksCntP+=1
   aString+=str(e)+", "
geneGraphP=aString[:-2]

TrgChromo=[]
print("Pull out just the Target chromosome, 2")
for e in Chromo:
    if e[0]==2:
       TrgChromo.append(e[1])
print("Trg Chromosome list is ")
print(TrgChromo)
for trgC in TrgChromo:
    print("==>",trgC,"<==")

########
##  Process Q
########
print("Send Target Chromo into Colored Edges") 
Edges= ColoredEdges(TrgChromo)
print(Edges)
BlocksCntQ=0
aString=""
for e in Edges:
   BlocksCntQ+=1
   aString+=str(e)+", "
geneGraphQ=aString[:-2]
print("Show both P and Q gene graphs")
print("they are type:",type(geneGraphQ))
print("P")
print(geneGraphP)
print("Q")
print(geneGraphQ)
print("resort Q to match order of syntany blocks and merge into Red/Blue graph")
print("Create Red/Blue graph by putting Q in to the order of P")
print("This should make for alternating edges between P and Q")

#RedBlueGraph=MergePQ(geneGraphQ,geneGraphP)

print("Count the Cycles in the Red/Blue resulting graph")
print("Subtract cycles from Blocks for the breakpoint count")
#######################################################
####  Finally, call 2 break on the Graph 
####  Will be wrapped in TBreakonGenome to loop thru 
####  Qs and Ps, inline here for one
#######################################################
#ans=TBreakonGenomeGraph(geneGraph,a,b,c,d)
#final=""
#for n in ans:
#   final+=str(n)+", " 
#geneGraph=final[:-2]
#print("-"+geneGraph+"-")
#print("is of type ",type(geneGraph))


#######################################################
####  Now work backwards 
#######################################################

print("**  Graph ",geneGraphQ," back to Genome**")
print("Format of geneGraph=(2, 4), (3, 1), (7, 5), (6, 8) which is a string")
#fish

ans=findCycles(geneGraphQ,geneGraphP)
print("Number of cycles is ",len(ans))
print("Check and count cycles")
TrivCycCnt, CycCnt=CycleCheck(ans)
print("Trivial Cycles: ",TrivCycCnt," and Cycles: ",CycCnt)
print("BlocksCnt is ",BlocksCntQ)
print("BlocksCnt is ",BlocksCntP)
print("BlocksCnt-Cycles")
print(BlocksCntQ-len(ans))
exit()

Qcnt, genomeQ=GraphToGenome(geneGraphQ)
Pcnt, genomeP=GraphToGenome(geneGraphP)
print("Q cycles",Qcnt)
print("P cycles",Pcnt)
print("Genome Q",genomeQ)
print("Genome P",genomeP)
print("Blocks Q size is :",BlocksCntQ)
print("Blocks P size is :",BlocksCntP)
print("Finally")
print("Cycles in P and Q separate:",Pcnt," and ",Qcnt) 

print("Total Breaks")
print(BlocksCntP-(Pcnt+Qcnt))

#print("Final Answer")
#ChrmoZome=""
#for Chrmo in genome:    
#    ChrmoZome+=Chrmo
#print(ChrmoZome)
