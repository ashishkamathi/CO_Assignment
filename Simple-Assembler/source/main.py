import sys
finalbin=[]
opp_dic={"add":"A","sub":"A","movi":"B","mov":"C","ld":"D","st":"D","mul":"A","div":"C","rs":"B","ls":"B","xor":"A","or":"A",
"and":"A","not":"C","cmp":"C","jmp":"E","jlt":"E","jgt":"E","je":"E","hlt":"F"}
opp_code={"add":"00000","sub":"00001","movi":"00010","mov":"00011","ld":"00100","st":"00101","mul":"00110","div":"00111",
"rs":"01000","ls":"01001","xor":"01010","or":"01011",
"and":"01100","not":"01101","cmp":"01110","jmp":"01111","jlt":"10000","jgt":"10001","je":"10010","hlt":"10011"}
reg_add={"R0":"000","R1":"001","R2":"010","R3":"011","R4":"100","R5":"101","R6":"110","FLAGS":"111"}
var_add={}
label_add={}
var_count=0
current_line=0
hlt_c=0
f = open("output.txt", "a")

def typeA(oc,r1,r2,r3):
    global reg_add,f
    if r1 not in reg_add or r2 not in reg_add or r3 not in reg_add:
         sys.stdout.write("Error Line:"+str(str(current_line))+":"+"Wrong Register"+"\n")
         f.write("Error Line:"+str(str(current_line))+":"+"Wrong Register"+"\n")
         exit()
    return oc+"00"+reg_add[r1]+reg_add[r2]+reg_add[r3]
def typeC(oc,r1,r2):
    global reg_add,f
    if r1 not in reg_add or r2 not in reg_add :
         sys.stdout.write("Error Line:"+str(current_line)+":"+"Wrong Register"+"\n")
         f.write("Error Line:"+str(current_line)+":"+"Wrong Register"+"\n")
         exit()
    return oc+"00000"+reg_add[r1]+reg_add[r2]
def typeF(oc):
    return oc+"00000000000"
def typeB(oc,r1,im):
    global reg_add,f
    if int(im) <0 or int(im)>255 or r1 not in reg_add:
         sys.stdout.write("Error Line:"+str(str(current_line))+":"+"Wrong Immediate Value"+"\n")
         f.write("Error Line:"+str(str(current_line))+":"+"Immediate Value"+"\n")
         exit()
    bi=bin(int(im)).replace("0b", "")
    while len(bi)!=8:
        bi="0"+bi
    return oc+reg_add[r1]+bi
def typeC(oc,r1,r2):
    global reg_add,f
    if r1 not in reg_add or r2 not in reg_add :
         sys.stdout.write("Error Line:"+str(current_line)+":"+"Wrong Register"+"\n")
         f.write("Error Line:"+str(current_line)+":"+"Wrong Register"+"\n")
         exit()
    return oc+"00000"+reg_add[r1]+reg_add[r2]
def typeD(oc,r1,var):
    global var_add,f
    if r1 not in reg_add or var not in var_add :
         sys.stdout.write("Error Line:"+str(current_line)+":"+"Wrong Register/variable"+"\n")
         f.write("Error Line:"+str(current_line)+":"+"Wrong Register/variable"+"\n")
         exit()
    return (oc+reg_add[r1]+var_add[var])
def typeE(oc,adr):
    global label_add,f
    if adr not in label_add :
         sys.stdout.write("Error Line:"+str(current_line)+":"+"Wrong label"+"\n")
         f.write("Error Line:"+str(current_line)+":"+"Wrong label"+"\n")
         exit()
    return(oc+"000"+label_add[adr])

def convertb(a):
    li=a.split()
    global opp_dic,opp_code,f,current_line
    if li[0] not in opp_dic:
         sys.stdout.write("Error Line:"+str(current_line)+":"+"Wrong Oppcode"+"\n")
         f.write("Error Line:"+str(current_line)+":"+"Wrong Oppcode"+"\n")
         exit()

    type=opp_dic.get(li[0])
    
    if type=="C" and li[2][0]=="$":
        type="B"
    if type!=None:
        op_c=opp_code.get(li[0])
    if type=="A":
        if len(li)<4:
         sys.stdout.write("Error Line:"+str(current_line)+":"+"Wrong format"+"\n")
         f.write("Error Line:"+str(current_line)+":"+"Wrong format"+"\n")
         exit()
        return typeA(op_c,li[1],li[2],li[3])
    if type=="C":
        if len(li)<3:
         sys.stdout.write("Error Line:"+str(current_line)+":"+"Wrong format"+"\n")
         f.write("Error Line:"+str(current_line)+":"+"Wrong format"+"\n")
         exit()
        return typeC(op_c,li[1],li[2])
    if type=="F":
        return typeF(op_c)
    if type=="B":
        if len(li)<3:
         sys.stdout.write("Error Line:"+str(current_line)+":"+"Wrong format"+"\n")
         f.write("Error Line:"+str(current_line)+":"+"Wrong format"+"\n")
         exit()
        if li[0]=="mov":
            op_c=opp_code.get(li[0]+"i")
            return typeB(op_c,li[1],li[2][1:])
        else:
             return typeB(op_c,li[1],li[2][1:])
    if type=="D":
        if len(li)<3:
         sys.stdout.write("Error Line:"+str(current_line)+":"+"Wrong format"+"\n")
         f.write("Error Line:"+str(current_line)+":"+"Wrong format"+"\n")
         exit()
        return(typeD(op_c,li[1],li[2]))
    if type=="C":
        if len(li)<3:
         sys.stdout.write("Error Line:"+str(current_line)+":"+"Wrong format"+"\n")
         f.write("Error Line:"+str(current_line)+":"+"Wrong format"+"\n")
         exit()
        return(typeC(op_c,li[1],li[2]))
    if type=="E":
        if len(li)<2:
         sys.stdout.write("Error Line:"+str(current_line)+":"+"Wrong format"+"\n")
         f.write("Error Line:"+str(current_line)+":"+"Wrong format"+"\n")
         exit()
        return(typeE(op_c,li[1]))
 
def main():
    #file2=open('Simple-Assembler\source\input.txt','r')
    #complete_input = file2.read()
    complete_input = sys.stdin.read()
    commands=complete_input.splitlines()
    global finalbin,f,current_line,hlt_c
   
    for cm in commands:
        if cm=="hlt":
            hlt_c=hlt_c+1
        if "var" in cm:
            global var_count
            var_count=var_count+1    
    if hlt_c>1:
         sys.stdout.write("Error Line:"+str(current_line)+":"+"Multiple Hlt "+"\n")
         f.write("Error Line:"+str(current_line)+":"+"Multiple Hlt"+"\n")
         exit()

    for k in range (len(commands)):
        temp=commands[k].split()
        if(":" in temp[0]):
            global label_add
            bi=bin(k-var_count).replace("0b", "")
            while len(bi)!=8:
                bi="0"+bi
            label_add[temp[0].replace(":","")]=bi
            if len(temp)==2:
                 commands[k]=temp[1]
            if len(temp)==3:
                commands[k]=temp[1]+" "+temp[2]
            if len(temp)==4:
                commands[k]=temp[1]+" "+temp[2]+" "+temp[3]
            if len(temp)==5:
                commands[k]=temp[1]+" "+temp[2]+" "+temp[3]+" "+temp[4]    

    for cm in commands:
        current_line=current_line+1
        temp=cm.split()
        if temp[0]=="var":
            global var_add
            adr= len(commands)-var_count
            bi=bin(adr).replace("0b", "")
            while len(bi)!=8:
                bi="0"+bi
            var_add[temp[1]]=bi
            var_count=var_count-1
        elif cm==" ":
            None
        else:
            finalbin.append(convertb(cm))
 
    if "hlt" not in commands[len(commands)-1]:
         sys.stdout.write("Error Line:"+str(current_line)+":"+"Hlt Missing"+"\n")
         f.write("Error Line:"+str(current_line)+":"+"Hltmissing"+"\n")
         exit()

    for k in finalbin:   
        sys.stdout.write(k+"\n")
        f.write(k+"\n")
    
    f.close()
      
if __name__ == '__main__':
	main()



