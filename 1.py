# -*- coding: utf-8 -*-
import copy
class Step:
    def __init__(self, inp):
        self.inp=inp
        self.output=[]
        self.output_tmp=[]
    def step_right(self,i,j):
        if(i==(len(self.inp[0])-1)):
            return False
        elif (self.inp[i+1][j][1]==1):
            return False
        else:
            return [i+1,j]

    def step_left(self,i,j):
        if(i==0):
            return False
        elif (self.inp[i-1][j][1]==1):
            return False
        else:
            return [i-1,j]

    def step_up(self,i,j):
        if(j==0):
            return False
        elif (self.inp[i][j-1][1]==1):
            return False
        else:
            return [i,j-1]

    def step_down(self,i,j):
        if(j==(len(self.inp[0])-1)):
            return False
        elif (self.inp[i][j+1][1]==1):
            return False
        else:
            return [i,j+1]

    def choosee_step1(self,index_operation,i,j):
        operations=[self.step_right,self.step_down,self.step_left,self.step_up]
        for p in range(index_operation,4):
            f=operations[p](i,j)
            if (f!=False):
                return [p,f] 
        return False

    def choosee_step(self,index_operation,i,j,prev):
        operations=[self.step_right,self.step_down,self.step_left,self.step_up]
        for p in range(index_operation,4):
            if(prev==0):
                if(p==2):
                    continue     
            elif(prev==1):
                if(p==3):
                    continue 
            elif(prev==2):
                if(p==0):
                    continue 
            elif(prev==3):
                if(p==1):
                    continue 
            f=operations[p](i,j)
            if (f!=False):
                return [p,f]    
        return False
        
    def look_for_the_route(self,i,j,l,directions,route,var):
        i0=i
        j0=j
        index_operation=0
        p=0
        prev=-1
        if(len(directions)!=0):
            index_operation=directions.pop()+1
            p=l-2
            route.pop()
            if(len(directions)!=0):
                prev=directions[-1]
                i=route[-1][0]
                j=route[-1][1]
            else:
                prev=-1            
                i=i0
                j=j0

        while ((p< (l-1) ) and (p!=-1) ):            
            data=self.choosee_step(index_operation,i,j,prev)
            if(data!=False):
                p+=1
                i=data[1][0]
                j=data[1][1]
                route.append(copy.copy([i,j]))
                directions.append(copy.copy(data[0]))
                prev=data[0]
                index_operation=0
            else:
                p-=1
                if (p!=-1):
                    index_operation=directions.pop()+1
                    route.pop()
                    if(len(route)!=0):
                        prev=directions[-1]
                        i=route[-1][0]
                        j=route[-1][1]
                    else:
                        prev=-1
                        i=i0
                        j=j0        
        if (p==-1):
            self.output_tmp.append(copy.copy(var))
            return var
        elif (self.inp[i][j][0]==l):
            var.append(copy.copy(route))
            self.look_for_the_route(i0,j0,l,directions,route,var)
            return var
        else:
            self.look_for_the_route(i0,j0,l,directions,route,var)       

    def write_output(self,i,j):
        if(self.inp[i][j][0]>0):
            if (inp[i][j][0]==1):
                self.output_tmp.append([i,j])
            else:
                self.look_for_the_route(i,j,inp[i][j][0],[],[],[])
        else:
            self.output_tmp.append([])
        self.output=copy.copy(self.output_tmp)
        self.output_tmp=[]
        return self.output.pop()

#Допустим есть такая матрица
inp=[[[3,0],[0,0],[3,0]],[[0,0],[0,0],[0,0]],[[3,0],[0,0],[1,0]]]

#Красиво напечатаем ее, убрать это потом естественно
print "Input:\n"
for i in range(len(inp)):
    for j in range(len(inp[0])):
        print " ",
        print str(inp[i][j][0]),
    print "\n"

#вот собстенно требуемая функция
def get_var(inp,i,j):
    return Step(inp).write_output(i,j)

#позовем ее
print get_var(inp,2,0)


