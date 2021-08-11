class Student:
    def __init__(self,id,Name,LastName):
        self.SetID(id)
        self.name = Name
        self.lastname = LastName

    def GetID(self):
        return self.__id

    def SetID(self,id):
        self.__id= id

    def __str__(self):
        return str(self.__id)+" "+self.name+" "+self.lastname

def readFile(file,x)->list: # x is for splits
    myFile=open(file,"r",encoding="utf-8") #utf-8 for adding turkish characters (ü,ğ,ı,ş,ö...)
    lines = myFile.readlines()
    records = []
    for line in lines:
        line = line.rstrip() # clear up  \n
        line = line.split(x) #split them
        records.append(line) # append each students
    myFile.close()
    return records
def fromlisttostudents(records)->list:
    studentList=[]
    for record in records:
        object= Student(int(record[0]),record[1],record[2]) # (id,name,lastname)
        studentList.append(object)
    return studentList
# 1
def search(studentList,id):
    for st in studentList:
        if st.GetID()==id: #for finding the student
            result= st.name+" "+st.lastname
            return result
    return "There is no student with the id."

#studentList = fromlisttostudents(readFile("student.txt"," "))
#print(search(studentList,117987))

# 2
def maxpoint(): # for finding max point
    pointFile= readFile("university.txt",",")
    points=[]
    for i in pointFile:
        points.append(int(i[2]))
    return max(points)
def maxuni(): # for comparing each universities's point to max point
    myFile= readFile("university.txt",",")
    res=[]
    for i in myFile:
        if int(i[2])==maxpoint():
            res.append(i[1])
    return res
#print(maxuni())

#3

def results():
    answers= readFile("answers.txt"," ")
    keys= readFile("key.txt"," ")
    students= readFile("student.txt"," ")
    universities=readFile("university.txt",",")
    results=[]
    for answer in answers:
        result=[]
        if answer[1]=="A": # if book type is A
            rightAnswers= keys[0][0]
        if answer[1]=="B": # if book type is B
            rightAnswers=keys[1][0]
        k=0
        correct1=0 # first correct (total correct answers)
        false=0
        blank=0
        correct2=0 # after wrong ans(1 in 4) subtracting from corrects
        for i in answer[2]:
            if i== rightAnswers[k]:
                correct1+=1
            elif i=='-':
                blank+=1
            else:
                false+=1
            k+=1
        correct2= correct1-(false//4)
        if correct2<0:
            correct2=0
        score=correct2 * 15
        for student in students:
            if student[0]==answer[0]:
                result.append(str(student[0])) # id
                result.append(student[1])   # name
                result.append(student[2])   # lastname
                result.append(answer[1])   # book type
                result.append(str(correct1))  # total corrects
                result.append(str(false))  # false answers
                result.append(str(blank))   # blank answers
                result.append(str(correct2))   # after subtructing from correct ans
                result.append(str(score))   # score of student
        for uni in universities:
            if int(uni[0]) == int(answer[3]):  # first-choice school
                result.append(uni[1])
                break
        for uni in universities:
            if int(uni[0]) == int(answer[4]):  # second-choice school
                result.append(uni[1])
                break
        results.append(result)
        wFile = open("results.txt", "w", encoding="utf-8")
        for res in results:
            print(res)
            wFile.write(",".join(res))
            wFile.write("\n")

        wFile.close()

    results()
#4
def sortvalue()->list: # sorting scores
    scores = readFile("results.txt", ",")
    dict = {}
    v = []
    for sc in scores:
        res= sc[0]+" "+sc[1]+" "+sc[2]
        dict[res]=int(sc[8])
    for val in dict.values():
        v.append(val)
    for i in range(len(v)-1):
        for j in range(len(v)-1):
            if v[j]>v[j+1]:  # bubble sort
                temp=v[j]
                v[j]=v[j+1]
                v[j+1]=temp
    return v

def sortscores(lst)->list:
    scores= readFile("results.txt",",")
    dict={}
    sorted_list=[]

    for sc in scores:
        res= sc[0]+" "+sc[1]+" "+sc[2]
        dict[res]=int(sc[8])
    for val in dict.values():
        lst.append(val)

    for i in range(len(lst)):
        for k in dict.keys():
            if dict[k] == lst[i]:
                if k in sorted_list: # if already there is the student, so do not append again
                    continue
                else:
                    sorted_list.append(k)
    return sorted_list

#print(sortscores(sortvalue()))

#5
def placeduni():
    results= readFile("results.txt",",")
    universities= readFile("university.txt",",")

    mdict={} #key- uni name, value-list of students {'mugla pc': ['ali', 'veli'], 'ege pc': ['merve', 'ayşe']}
    for uni in universities:
        mdict[uni[1]]=[]
    mdict['unplacedStudents'] = []
    for result in results:
        for i in [9, 10]:  # result[9] is first uni result[10] is second uni
            # but second uni have \n for the new line
            uniName = result[i]
            if i == 10 and result[10][-1:] == "\n":
                uniName = result[10][:-1]

            uniInfo = {} # keys are score and capacity
            for university in universities:
                #print( uniName,university[1])
                if university[1] == uniName:
                    uniInfo = {'score': university[2], 'capacity': university[3]}
                    break
            if int(result[8]) >= int(uniInfo['score']) and len(mdict[uniName]) < int(uniInfo['capacity']):
                mdict[uniName].append(result[1] + " " + result[2])
                break
            elif i == 10:
                mdict['unplacedStudents'].append(result[1] + " " + result[2])
                # if this part of the code works then student won't be placed any universtiy
    #print(mdict)
    return mdict



#7
def departments()->list:
    departments=[]
    unis=readFile("university.txt",",")
    splituni=[]
    for uni in unis:
        splituni=(uni[1]).split(" ")
        res= splituni[-2]+" "+splituni[-1]
        if res not in departments:
            departments.append(res)
    return departments


#print(departments())

import os


while(True):
    print("1 : Search for a student with id\n"   
          "2 : List the uni/unis with a maximum base point\n"
          "3 : results.txt\n"
          "4 : List the students sorted by their score\n"
          "5 : List the students placed in every university/department\n"
          "6 : List the unplaced students\n"
          "7 : List all the departments\n")
        # choices table
    choice= int(input("Enter your choice(1,2,4,5,6,7)(for stop -1):.."))
    if(choice==1):
        stid= int(input("Enter the student's id(6 digits):.."))
        studentList = fromlisttostudents(readFile("student.txt", " "))
        print(search(studentList, stid))

    if(choice==2):
        print(maxuni())
    if(choice==4):
        print(sortscores(sortvalue()))
    if(choice==5 or choice==6):
        for i in placeduni():
            if choice==5 and i != "unplacedStudents": # placed students
                print(i,"= ", placeduni()[i])
            if choice==6 and i== "unplacedStudents":  # unplaced students
                print(i, "= ",placeduni()[i])

    if(choice==7):
        print(departments())

    if(choice== -1):
        break

    input("press any key for clean-up the screen")
    os.system("cls")  # for clean-up the screen

    try:
        myFile = open("student.txt", "r")

    except IOError:
        print("An error!")
    finally:
        myFile.close()
