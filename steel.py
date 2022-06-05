length = [1995, 1950, 2075, 2332]
L = 6050

n = [int(L/x) for x in length]
m = [L - j*length[i] for i,j in enumerate(n)]

print(f'จำนวนชิ้นงานเริ่มต้น :{n}')
print(f'เศษเหลือเริ่มต้น : {m}')

for i, j in enumerate(length): 
  for x in range(n[i], 0, -1):
    print(f':: index = {i} ความยาวชิ้นงาน = {j}  จำนวนชิ้นที่ตัด = {x}  เศษเหลือ = {L - x*j}')
    for a, b in enumerate(length):
      if a != i:
        for y in range(1, n[a]):
          if L - x*j >= b*y:
            print('>>', y,"ชิ้น",b,"mm","เศษเหลือ =", L - x*j - b*y) 
            for c, d in enumerate(length):
              if c != i:
                for z in range(1, n[c]): 
                  if  L - x*j - b*y >=  d*z :
                    print('>>>', z,"ชิ้น",d,"mm","เศษเหลือ =", L - x*j - b*y-d*z) 

# (new) Min Cost เหล็กราง
from pulp import *  
import pandas as pd 
import numpy as np 

#set
pattern = ["pattern1","pattern2","pattern3","pattern4","pattern5","pattern6","pattern7","pattern8","pattern9","patterna","patternb"]
name_work = ["202-05","205-05","210-05","240-17"]

#parameter
unitcost_steel =int(input("unitcost_steel:"))
length ={"202-05":1995,"205-05":1950, "210-05":2075,"240-17":2332}

demand= {
    "202-05" : int(input("Demand 202-05 :")) ,
    "205-05" : int(input("Demand 205-05 :")) ,
    "210-05" : int(input("Demand 210-05 :")),
    "240-17" : int(input("Demand 240-17 :"))
}
work_piece ={
    "pattern1":{"202-05":3 ,"205-05":0 ,"210-05":0 ,"240-17":0},

    "pattern2":{"202-05":2 ,"205-05":1 ,"210-05":0 ,"240-17":0},

    "pattern3":{"202-05":1 ,"205-05":1 ,"210-05":1 ,"240-17":0},

    "pattern4":{"202-05":1 ,"205-05":2 ,"210-05":0 ,"240-17":0},

    "pattern5":{"202-05":0 ,"205-05":3 ,"210-05":0 ,"240-17":0},

    "pattern6":{"202-05":0 ,"205-05":0 ,"210-05":2 ,"240-17":0},

    "pattern7":{"202-05":0 ,"205-05":0 ,"210-05":1 ,"240-17":1},

    "pattern8":{"202-05":0 ,"205-05":0 ,"210-05":0 ,"240-17":2},

    "pattern9":{"202-05":1 ,"205-05":0 ,"210-05":0 ,"240-17":1},

    "patterna":{"202-05":0 ,"205-05":2 ,"210-05":1 ,"240-17":0},
    
    "patternb":{"202-05":0 ,"205-05":1 ,"210-05":0 ,"240-17":1}

 }

loss_pattern = {
    "pattern1":65  ,
    "pattern2":110 ,
    "pattern3":30  ,
    "pattern4":155 ,
    "pattern5":200 ,
    "pattern6":1900 ,
    "pattern7":1643 ,
    "pattern8":1386 ,
    "pattern9":1732 ,
    "patterna":75 ,
    "patternb":1768 
}

#name_plomblem_minimize
model =LpProblem("Cutting Stock_U" ,LpMinimize)

#decision variable
x =LpVariable.dict("x",pattern,lowBound=0 ,cat =LpInteger)

#objective function
model += lpSum(x[i]*unitcost_steel for i in pattern)
#model += lpSum(x[i]*loss_pattern[i] for i in pattern)

#constrain
for j in name_work : 
  model += lpSum(x[i]*work_piece[i][j] for i in pattern) >=demand[j] #เงื่อนไขผลิตงานให้ได้มากกว่าหรือเท่ากับdemand

#solve
model.solve()
print(model)
print("Status Model:",LpStatus[model.status]) #check status model
print("Opjective Funtion [Min_Cost]  = " , value(model.objective) ,"Baht") #เเสดงค่าobjective function

#เเสดงค่าdecision variabe
sum=0
for v in model.variables():
  if v.varValue > 0 : 
    print("Cutting" ,v.name,"=",v.varValue,"เส้น")
    sum =sum +v.varValue  
print("Total Steel = " ,sum,"เส้น")

d=[] #list decistion variable
for v in model.variables():
   d.append(v.varValue )
w=np.array(d)

l=[] #list loss_pattern
for i in loss_pattern.values():
  l.append(i)
q=np.array(l)

print("Total Loss =",np.sum(w*q),"mm") #เเสดงค่า loss

#เก็บlistชิ้นงาน

p1=[]
p2=[]
p3=[]
p4=[]

for i in work_piece.values():
  p1.append(i["202-05"])
  p2.append(i["205-05"])
  p3.append(i["210-05"])
  p4.append(i["240-17"])

p_202_05 =np.array(p1)
p_205_05 =np.array(p2)
p_210_05 =np.array(p3)
p_240_17 =np.array(p4)

#เเสดงค่าจำนวนชิ้นงาน
print("Number of [202-05] =",np.sum(p_202_05*w),"pieces" )
print("Number of [205-05] =",np.sum(p_205_05*w),"pieces")
print("Number of [210-05] =",np.sum(p_210_05*w),"pieces" )
print("Number of [240-17] =",np.sum(p_240_17*w),"pieces" )

