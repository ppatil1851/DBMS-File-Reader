#Team Members: 
#Priyanka Patil: 1001981851
#Pragya Agarwal: 1001861779
import copy
import os
input=[]
locktable=[]
transactiontable=[]
timeStamp =1

#Function for begin transaction
def beginTransaction(l):
    global timeStamp
    transactionId=l[1]
    transactiondetails=[transactionId,timeStamp,'Active',[]]
    timeStamp=timeStamp+1
    transactiontable.append(transactiondetails)
    # print(transactiondetails)
    output_file.write("T"+str(l[1])+" Begins Id="+str(l[1])+" TS="+str(timeStamp) +" State=Active")
    output_file.write('\n')
    #output_file.write('\n')
    
#Function for block transaction
def transactionBlock(transId1,transId2,l):
    # print(transId1,transId2,l)
    pass

#Function for abort transaction
def transactionAbort(transId1):
    # print(transId1)
    global transactiontable
    global locktable
    for i in range(len(transactiontable)):
        if transactiontable[i][0]==transId1:
            transactiontable[i][2]='Abort'
            #transactiontable[i][2]='Abort'
            transactiontable[i][3]=[]
            for i in range(len(locktable)):
                # print(i)
                if transId1 in locktable[i][2]:
                    if len(locktable[i][2])!=1:
                        locktable[i][2].remove(transId1)
                    else:
                        locktable.remove(locktable[i])

#Function for read lock
def readLock(l):
    global transactiontable
    global locktable
    transactionId=l[1]
    operation=l[0]
    # resourceName=l[3]
    timeStamp1=0
    timeStamp2=0
    flag=0
    locktableIndex=0
    activeTransactionIndex=0
    if "X" in l:
        resourceName = "X"
    elif "Y" in l:
        resourceName = "Y"
    elif "Z" in l:
        resourceName = "Z"
    # print(resourceName)
    # if len(transactiontable)==0:
    #     return 0
    for i in range(len(transactiontable)):
        # print("test")
        if transactiontable[i][0]==transactionId and transactiontable[i][2]=='Block':
            transactiontable[i][3].append(l)
        if transactiontable[i][0]==transactionId and transactiontable[i][2]=='Active':
            activeTransactionIndex=i
            if len(locktable)==0: #first entry to the lockTable
                locktableDetails=[resourceName,operation,[transactionId]]
                # print(locktableDetails)
                locktable.append(locktableDetails)
                output_file.write("ITEM "+str(resourceName)+" is read locked by T"+str(l[1]))
                output_file.write('\n')
            else:
                #if the locktable already has data. To check all conditions and write to output file
                for i in range(len(locktable)):
                    if locktable[i][0]==resourceName:
                        flag=1
                        locktableIndex=i
                        if locktable[locktableIndex][1]=='r' and transactionId not in locktable[locktableIndex][2]:
                            # locktableDetails=[resourceName,operation,[transactionId]]
                            # locktable.append(locktableDetails) 
                            locktable[locktableIndex][2].append(transactionId)
                            # print("ITEM "+str(resourceName)+" is read locked by T"+str(transactionId))
                            output_file.write("ITEM "+str(resourceName)+" is read locked by T"+str(transactionId))
                            output_file.write('\n') 
                        elif locktable[locktableIndex][1]=='r' and transactionId in locktable[locktableIndex][2]:
                            locktableDetails=[resourceName,operation,[transactionId]]
                            locktable.append(locktableDetails) 
                            output_file.write("ITEM "+str(resourceName)+" is read locked by T"+str(transactionId))
                            output_file.write('\n')
                        elif locktable[locktableIndex][1]=='w' and transactionId not in locktable[locktableIndex][2]:
                            transId1=transactiontable[activeTransactionIndex][0]
                            transId2=locktable[locktableIndex][2][0] #the first data in the list of transaction id
                            for j in transactiontable:
                                #find timestamp
                                if j[0]==transId1:
                                    timeStamp1=j[1]
                                if j[0]==transId2:
                                    timeStamp2=j[1]
                            if timeStamp2<timeStamp1:
                                output_file.write("T"+str(transId1)+" aborted due to wait-die")
                                output_file.write('\n')
                                transactionAbort(transId1) 
                            elif timeStamp2>timeStamp1:
                                output_file.write("T"+str(transId1)+" blocked\waiting due to wait-die")
                                output_file.write('\n')
                                transactionBlock(transId1,transId2,l)
                # if there is no read locked found for current transaction then append the read lock
                if flag==0:
                    output_file.write("ITEM "+str(resourceName)+" is read locked by T"+str(transactionId))
                    output_file.write('\n')  
                    locktableDetails=[resourceName,operation,[transactionId]]
                    locktable.append(locktableDetails)
    # print(locktable)       

#Function for write lock                               
def writeLock(l):
    global transactiontable
    global locktable
    # print(transactiontable)
    # print(locktable)
    transactionId=l[1]
    operation=l[0]
    # resourceName=l[3]
    timeStamp1=0
    timeStamp2=0
    flag=0
    locktableIndex=0
    activeTransactionIndex=0
    if "X" in l:
        resourceName = "X"
    elif "Y" in l:
        resourceName = "Y"
    elif "Z" in l:
        resourceName = "Z"
    # print(resourceName)
    for i in range(len(transactiontable)):
        if transactiontable[i][0]==transactionId and transactiontable[i][2]=='Block':
            transactiontable[i][3].append(l)
        if transactiontable[i][0]==transactionId and transactiontable[i][2]=='Active':
            activeTransactionIndex=i
        if len(locktable)==0:
            #Lock Table is Empty 
            print("No read operation found to upgrade into write")
        else:
            for i in range(len(locktable)):
                #search the entry for the resource
                if locktable[i][0]==resourceName:
                    locktableIndex=i
                    if locktable[locktableIndex][1]=='r' and transactionId in locktable[locktableIndex][2]:
                        if len(locktable[locktableIndex][2])==1 and locktable[locktableIndex][0]==resourceName:
                            locktable[locktableIndex][1]='w'
                            output_file.write("Read lock on "+str(resourceName)+" by T"+str(transactionId)+" is upgraded to write lock")
                            output_file.write('\n')
                        elif len(locktable[locktableIndex][2])>1:
                            # print(locktable)
                            #check if present in transaction table.If present then take timestamp
                            for j in transactiontable:
                                if j[0]==transactionId:
                                    timeStamp1=j[1]
                            #find the different transaction id for comparison which is not present in the list of transaction id in locktable
                            for j in locktable[locktableIndex][2]:
                                if j!=transactionId:
                                    for k in transactiontable:
                                        if k[0]==j:
                                            timeStamp2=k[1]
                                    if timeStamp2<timeStamp1:
                                        output_file.write("T"+str(transactionId)+" aborted due to wait-die")
                                        output_file.write('\n')
                                        transactionAbort(transactionId) 
                                    elif timeStamp2>timeStamp1:
                                        output_file.write("T"+str(j)+" blocked\waiting due to wait-die")
                                        output_file.write('\n')
                                        transactionBlock(transactionId,j,l)
                    elif locktable[locktableIndex][1]=='w' and transactionId not in locktable[locktableIndex][2]:
                        transId1=transactiontable[activeTransactionIndex][0]
                        transId2=locktable[locktableIndex][2][0] #the first data in the list of transaction id
                        for j in transactiontable:
                            #find timestamp
                            if j[0]==transId1:
                                timeStamp1=j[1]
                            if j[0]==transId2:
                                timeStamp2=j[1]
                        if timeStamp2<timeStamp1:
                            output_file.write("T"+str(transId1)+" aborted due to wait-die")
                            output_file.write('\n')
                            transactionAbort(transId1) 
                        elif timeStamp2>timeStamp1:
                            output_file.write("T"+str(transId1)+" blocked\waiting due to wait-die")
                            output_file.write('\n')
                            transactionBlock(transId1,transId2,l)                   
#Function for commit
def commit(l):
    global transactiontable
    global locktable
    transactionId=l[1]
    operation=l[0]
    flag=0
    for i in range(len(transactiontable)):
        if transactiontable[i][0]==transactionId and transactiontable[i][2]=='Active':
            index=i
            flag=1
            transactiontable[i][2]=='Committed'
            output_file.write("T"+transactionId+" is committed")
            output_file.write('\n')
        elif transactiontable[i][0]==transactionId and transactiontable[i][2]=='Abort':
            output_file.write("T"+transactionId+" is already aborted")
            output_file.write('\n')
    if flag==1:
        for i in locktable:
            for j in i[2]:
                if transactionId==j:
                    if len(i[2])==1:
                        locktable.remove(i)
                    else:
                        i[2].remove(transactionId)

#Main Function    
def mainFunction(l):
    if 'b' in l:
        beginTransaction(l)
    elif 'r' in l:
        # print("Read operation")
        readLock(l)
    elif 'w' in l:
        # print("Write operation")
        writeLock(l)
    elif 'e' in l:
        # print("Commit")
        commit(l)
path=".\input"       
os.chdir(".\input")
for file in os.listdir():
    if file.endswith('.txt'):
        with open(file, 'r') as text:
            for line in text:
                input.append(line)
c=0
for l in input:
    if(l[0]=='b' and l[1]=='1'):
        os.chdir(os.path.abspath("../."))
        os.chdir(".\output")
        c=c+1
        output_file = open("output"+str(c)+".txt", 'w')
        timeStamp=0
        locktable=[]  
        transactiontable=[]    
        input=[] 
    mainFunction(l)
    
#Reference:
#https://github.com/shubhang-arora/two-phase-locking
#https://www.geeksforgeeks.org/categories-of-two-phase-locking-strict-rigorous-conservative/    