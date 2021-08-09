import sys
finalbin=[]
opp_dic={"add":"A","sub":"A","mov":"B","ld":"D","st":"D","mul":"A","div":"C","rs":"B","ls":"B","xor":"A","or":"A",
"and":"A","not":"C","cmp":"C","jmp":"E","jlt":"E","jgt":"E","je":"E","hlt":"F"}
opp_code={"add":"00000","sub":"00001","movi":"00010","mov":"00011","ld":"00100","st":"00101","mul":"00110","div":"00111",
"rs":"01000","ls":"01001","xor":"01010","or":"01011",
"and":"01100","not":"01101","cmp":"01110","jmp":"01111","jlt":"10000","10001":"E","je":"10010","hlt":"10011"}

reg_add={"R0":"000","R1":"001","R2":"010","R3":"011","R4":"100","R5":"101","R6":"110","flag":"111"}

def typeA(oc,r1,r2,r3):
    global reg_add
    return oc+"00"+reg_add[r1]+reg_add[r2]+reg_add[r3]
def typeF(oc):
    return oc+"000000000000"

def convertb(a):
    li=a.split()
    global opp_dic,opp_code
    type=opp_dic.get(li[0])
    if type!=None:
        op_c=opp_code.get(li[0])
    if type=="A":
        return typeA(op_c,li[1],li[2],li[3])
    if type=="F":
        return typeF(op_c)


def main():
    complete_input = sys.stdin.read()
    commands=complete_input.splitlines()
    global finalbin
    for cm in commands:
        finalbin.append(convertb(cm))
    for k in finalbin:
        sys.stdout.write(k+"\n")
     
    
if __name__ == '__main__':
	main()



