import sys
import numpy as np
import matplotlib.pyplot as plt
halt=False
pc=0
reg_name={"000":"R0","001":"R1","010":"R2","011":"R3","100":"R4","101":"R5","110":"R6","111":"FLAGS"}
reg_val={"R0":"0000000000000000","R1":"0000000000000000","R2":"0000000000000000","R3":"0000000000000000","R4":"0000000000000000","R5":"0000000000000000","R6":"0000000000000000","FLAGS":"0000000000000000"}
f = open("output.txt", "a")
mem=[0]*256
j_pc=-1
x=[]
y=[]
cycle=0
 
def reset_flag():
     global reg_val
     reg_val["FLAGS"]="0000000000000000"
     
def addn(reg1,reg2,reg3):
     reset_flag()
     global pc,reg_val
     sum=int(reg_val[reg2],2)+int(reg_val[reg3],2)
     sum=bin(sum).replace("0b", "")
     if len(sum)<=16:
          while len(sum)!=16:
               sum="0"+sum 
          reg_val[reg1]=str(sum)
     elif len(sum)>16:
          reg_val[reg1]=str(sum[len(sum)-16:])
          reg_val["FLAGS"]="0000000000001000"
def subn(reg1,reg2,reg3):
     reset_flag()
     global pc,reg_val
     if int(reg_val[reg2], 2) < int(reg_val[reg3], 2):
          reg_val[reg1]="0000000000000000"
          reg_val["FLAGS"]="0000000000001000"
     else:
          subn = bin(int(reg_val[reg2], 2)-int(reg_val[reg3], 2))
          subn=subn[2:]
          while len(subn)!=16:
           subn="0"+subn
          reg_val[reg1]=str(subn)
          
def RS(reg1,value):
    reset_flag()
    global pc,reg_val
    k = reg_val[reg1]
    c = int(value,2)
    v= ""
    for i in range(16-c,16):
        v = v + "0"
    v = v + k[:16-c]
    reg_val[reg1]= v

def LS(reg1,value):
    reset_flag()
    global pc,reg_val
    k = reg_val[reg1]
    c = int(value,2)
    v= ""
    for i in range((16-c),16):
        v = v + "0"
    v =  k[(c) :] + v
    reg_val[reg1]= v

def movi(reg1,im):
     global reg_val
     while len(im)!=16:
          im="0"+im
     reg_val[reg1]=im
     reset_flag()
def mov(reg1,reg2):
     global reg_val
     reg_val[reg1]=reg_val[reg2]
     reset_flag()
def ld(reg1,memadr):
     reset_flag()
     global reg_val,x,y
     reg_val[reg1]=mem[int(memadr,2)]
     x.append(cycle)
     y.append(int(memadr,2))
def st(reg1,memadr):
     reset_flag()
     global reg_val,x,y
     mem[int(memadr,2)]= reg_val[reg1]
     x.append(cycle)
     y.append(int(memadr,2))
def multiply(reg1,reg2,reg3):
     reset_flag()
     mul=int(reg_val[reg2],2)*int(reg_val[reg3],2)
     mul=bin(mul).replace("0b", "")
     if len(mul)<=16:
          while len(mul)!=16:
               mul="0"+mul
          reg_val[reg1]=str(mul)
     elif len(mul)>16:
          reg_val[reg1]=str(mul[len(mul)-16:])
          reg_val["FLAGS"]="0000000000001000"

def divide(reg1,reg2):
     reset_flag()
     global reg_val
     q=int(int(reg_val[reg1], 2) / int(reg_val[reg2], 2))
     r=int(reg_val[reg1], 2) % int(reg_val[reg2], 2)
     q=bin(q).replace("0b", "")
     while len(q)!=16:
          q="0"+q
     r=bin(r).replace("0b", "")
     while len(r)!=16:
          r="0"+r
     reg_val["R0"]=q
     reg_val["R1"]=r

def cmp(reg1,reg2):
    reset_flag()
    global pc,reg_val
    if int(reg_val[reg1],2) < int(reg_val[reg2],2):
          reg_val["FLAGS"] = "0000000000000100"
    elif int(reg_val[reg1],2) > int(reg_val[reg2],2):
          reg_val["FLAGS"] = "0000000000000010"  
    elif int(reg_val[reg1],2) == int(reg_val[reg2],2):
          reg_val["FLAGS"] = "0000000000000001"
def And(reg1,reg2,reg3):
    reset_flag()
    global pc,reg_val
    l = ""
    for i in range(16):
      k =  int(reg_val[reg2][i]) & int(reg_val[reg3][i])
      l = l + str(k)
    reg_val[reg1] = l

def XOR(reg1,reg2,reg3):
    reset_flag()
    global pc,reg_val
    l = ""
    for i in range(0,16):
      k =  int(reg_val[reg1][i]) ^ int(reg_val[reg2][i])
      l = l + str(k)
    reg_val[reg3] = l
   

def OR(reg1,reg2,reg3):
    reset_flag()
    global pc,reg_val
    l = ""
    for i in range(0,16):
      k =  int(reg_val[reg1][i]) | int(reg_val[reg2][i])
      l = l + str(k)
    reg_val[reg3] = l

def invert(reg1,reg2):
    reset_flag()
    global pc,reg_val
    l = ""
    for i in range(0,16):
        if reg_val[reg2][i] == "1":
            l = l + "0"
        elif reg1[i] == "0":
            l = l + "1"
    reg_val[reg1] = l
    
def jmp(memadr):
     reset_flag()
     global pc,j_pc
     temp=int(memadr,2)
     j_pc=temp-1
def jlt(memadr):
     if reg_val["FLAGS"][13]=="1":
          global pc,j_pc
          temp=int(memadr,2)
          j_pc=temp-1
     reset_flag()
def jgt(memadr):
     if reg_val["FLAGS"][14]=="1":
          global pc,j_pc
          temp=int(memadr,2)
          j_pc=temp-1
     reset_flag()
def je(memadr):
     if reg_val["FLAGS"][15]=="1":
          global pc,j_pc
          temp=int(memadr,2)
          j_pc=temp-1
     reset_flag()
     
def hlt():
     reset_flag()
     global pc,halt
     halt=True
     
def execute(inst):
     if inst[:5]=="00000":
          addn(reg_name[inst[7:10]],reg_name[inst[10:13]],reg_name[inst[13:16]])
     elif inst[:5]=="00110":
          multiply(reg_name[inst[7:10]],reg_name[inst[10:13]],reg_name[inst[13:16]])
     elif inst[:5]=="00111":
          divide(reg_name[inst[10:13]],reg_name[inst[13:16]])
     elif inst[:5]=="00001":
          subn(reg_name[inst[7:10]],reg_name[inst[10:13]],reg_name[inst[13:16]])    
     elif inst[:5]=="00010":
          movi(reg_name[inst[5:8]],inst[8:16])
     elif inst[:5]=="01000":
          RS(reg_name[inst[5:8]],inst[8:16])
     elif inst[:5]=="01001":
          LS(reg_name[inst[5:8]],inst[8:16])
     elif inst[:5]=="00011":
          mov(reg_name[inst[10:13]],reg_name[inst[13:16]])
     elif inst[:5]=="00100":
          ld(reg_name[inst[5:8]],inst[8:16])
     elif inst[:5]=="00101":
          st(reg_name[inst[5:8]],inst[8:16])
     elif inst[:5]=="01110":
          cmp(reg_name[inst[10:13]],reg_name[inst[13:16]])
     elif inst[:5]=="01100":
          And(reg_name[inst[7:10]],reg_name[inst[10:13]],reg_name[inst[13:16]])
     elif inst[:5]=="01011":
          OR(reg_name[inst[7:10]],reg_name[inst[10:13]],reg_name[inst[13:16]])
     elif inst[:5]=="00110":
          XOR(reg_name[inst[7:10]],reg_name[inst[10:13]],reg_name[inst[13:16]])
     elif inst[:5]=="00110":
          invert(reg_name[inst[10:13]],reg_name[inst[13:16]])
     elif inst[:5]=="01111":
          jmp(inst[8:16])
     elif inst[:5]=="10000":
          jlt(inst[8:16])
     elif inst[:5]=="10001":
          jgt(inst[8:16])
     elif inst[:5]=="10010":
          je(inst[8:16])
     elif inst[:5]=="10011":
          hlt()


def pc_rf():
     p=bin(pc).replace("0b", "")
     while len(p)!=8:
          p="0"+p
     sys.stdout.write(p+" "+reg_val["R0"]+" "+reg_val["R1"]+" "+reg_val["R2"]+" "+reg_val["R3"]+" "+reg_val["R4"]+" "+reg_val["R5"]+" "+reg_val["R6"]+" "+reg_val["FLAGS"]+"\n")
     f.write(p+" "+reg_val["R0"]+" "+reg_val["R1"]+" "+reg_val["R2"]+" "+reg_val["R3"]+" "+reg_val["R4"]+" "+reg_val["R5"]+" "+reg_val["R6"]+" "+reg_val["FLAGS"]+"\n")

def main():
     global mem
     #file2=open('SimpleSimulator\source\input.txt','r')
     #complete_input = file2.read()
     complete_input = sys.stdin.read()
     temp=complete_input.splitlines()
     for k in range(len(temp)):
          mem[k]=temp[k]
     for z in range (len(temp),256):
          mem[z]="0000000000000000"
        
     global pc,j_pc,cycle,x,y
     while not halt:    
          execute(mem[pc])
          pc_rf()
          x.append(cycle)
          y.append(pc)
          cycle=cycle+1
          if(j_pc==-1):
               pc=pc+1
          else:
               pc=j_pc+1
               j_pc=-1
     for cm in mem:
          sys.stdout.write(cm+"\n")
          f.write(cm+"\n")
     x_axis = np.array(x)
     y_axis = np.array(y)
     plt.scatter(x_axis, y_axis)
     plt.xlabel("Cycle Number")
     plt.ylabel("Address Accessed")
     plt.savefig('plot.png', dpi=300, bbox_inches='tight')
     plt.show()

if __name__ == '__main__':
	main()