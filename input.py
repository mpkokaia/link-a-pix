import copy
import sys
sys.setrecursionlimit(100000)

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
            self.look_for_the_route(i,j,self.inp[i][j][0],[],[],[])
        else:
            self.output_tmp.append([])
        self.output=copy.copy(self.output_tmp)
        self.output_tmp=[]
        return self.output.pop()

class linkapix():
    condition = [[[]]]
    variants = [[[]]]
    height = 0
    width = 0

    def init(self, filename):
        #читаем данные из входного файла
        with open(filename, 'r') as hFile:
            data = hFile.read()

        tempdata = []
        prevNumber = False
        for i in data:
            if i == '\n':
                if not prevNumber:
                    tempdata.append([0, 0])
                self.condition.append(tempdata)
                prevNumber = False
                tempdata = []
                continue

            if not i == ',':
                tempdata.append([int(i), 0])
                prevNumber = True
            else:
                if prevNumber:
                    prevNumber = False
                else:
                    tempdata.append([0, 0])
        if not prevNumber:
            tempdata.append([0, 0])
        self.condition.append(tempdata)
        self.condition.remove(self.condition[0])

        #инициализируем массив под варианты
        tempdata = [[]]
        self.height = len(self.condition)
        self.width = len(self.condition[0])
        for i in range(self.height):
            for ii in range(self.width-1):
                tempdata.append([])
            self.variants.append(tempdata)
            tempdata = [[]]
        self.variants.remove(self.variants[0])

#функция заполняет массив всевозможных вариантов для каждого элемента кроссворда
def getVariants(crossword):
    for i in range(crossword.height):
        for j in range(crossword.width):
            if (not crossword.condition[i][j][0] == 0) and (not crossword.condition[i][j][1] == 1):
                crossword.variants[i][j] = copy.deepcopy(Step(crossword.condition).write_output(i, j))
                if len(crossword.variants[i][j]) == 0:
                    return False
    return True

#функция, которая закрашивает клетки по указанному маршруту
def paint(crossword, route):
    for i in route:
        crossword[int(i / crossword.height)][i % crossword.width] = -1

#функиця, которая закрашивает маршрут
def paintRoute(crossword, strcounter, counter, route):
    if crossword.condition[strcounter][counter][1] == 1:
        return True

    crossword.condition[strcounter][counter][1] = 1
    lroute = copy.deepcopy(route[0])
    l = len(route)
    count = 0
    for i in lroute:
        if crossword.condition[i[0]][i[1]][1] == 1:
            return False

        crossword.condition[i[0]][i[1]][1] = 1

    return True

def heurPredetect(crossword):
    for i in crossword.condition:
        for ii in i:
            if ii[0] == 1:
                ii[1] = 1

def alreadySolved(crosswod):
    for i in crossword.condition:
        if (not i[0] == 0) and (i[1] == 0):
            return False
    return True

#рекурсивная функция, основная
def solveLinkAPix(crossword):
    newcrossword = linkapix()
    newcrossword.condition = copy.deepcopy(crossword.condition)
    newcrossword.height = copy.deepcopy(crossword.height)
    newcrossword.width = copy.deepcopy(crossword.width)

    #назаполняем варианты с единственными решениями
    again = True
    while again:
        again = False
        #позовём функцию, которая заполнит newcrossword.variants, если она для какого то элемента не нашла варианты,
        #комбинация ошибочна и возвращаем рекурсию на один уровень вверх
        if not getVariants(newcrossword):
            return False

        for stringstrcounter in range(len(newcrossword.variants)):
            toRemove = []
            for counter in range(len(newcrossword.variants[stringstrcounter])):
                if len(newcrossword.variants[stringstrcounter][counter]) == 1:
                    if paintRoute(newcrossword, stringstrcounter, counter, newcrossword.variants[stringstrcounter][counter]):
                        again = True
                        toRemove.append(counter)
                    else:
                        return False
            for i in toRemove:
                newcrossword.variants[stringstrcounter][i] = []

    if alreadySolved(newcrossword):
        crossword.condition = copy.deepcopy(newcrossword.condition)
        return True

    #выбрать вариант, пробовать пока пробуется и удалять если не подошли



    #for test
    crossword.condition = copy.deepcopy(newcrossword.condition)

        #пока заполняется, заполняем варианты с единственным решением, по одному за итерацию цикла
        #if paintFirstOneVariants(newcrossword):
        #    again = True
    #WARNING!!! функция недописана

crossword = linkapix()
#читаем входной файл и парсим данные из него
crossword.init('sample1.txt')
heurPredetect(crossword)
#пытаемся решить
solved = solveLinkAPix(crossword)
for i in crossword.condition:
    for ii in i:
        sys.stdout.write(str(ii[1]))
    sys.stdout.write("\n")