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

        while not data.count(' ') == 0:
            data = data.replace(' ', '')
        data = data.split("\n")

        for i in data:
            stringData = []
            i = i.split(",")
            for ii in i:
                if len(ii) == 0:
                    stringData.append([0,0])
                else:
                    stringData.append([int(ii),0])
            self.condition.append(stringData)
            self.width = len(stringData)
        self.condition.remove(self.condition[0])
        self.height = len(self.condition)
        tempdata = []
        for i in range(self.width):
            tempdata.append([])
        for i in range(self.height):
            self.variants.append(copy.deepcopy(tempdata))
        self.variants.remove(self.variants[0])

#функция заполняет массив всевозможных вариантов для каждого элемента кроссворда
def getVariants(crossword):
    for i in range(crossword.height):
        for j in range(crossword.width):
            if (not crossword.condition[i][j][0] == 0) and (not crossword.condition[i][j][1] == 1):
                crossword.variants[i][j] = copy.deepcopy(Step(crossword.condition).write_output(i, j))
                print(crossword.condition[0][2])
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
    l = len(route)
    count = 0
    for i in route:
        if crossword.condition[i[0]][i[1]][1] == 1:
            return False

        crossword.condition[i[0]][i[1]][1] = 1

    return True

def heurPredetect(crossword):
    for i in crossword.condition:
        for ii in i:
            if ii[0] == 1:
                ii[1] = 1

def heurDetectFalses(crossword):
    toRemove = []
    for h in range(crossword.height):
        for w in range(crossword.width):
            for variant in crossword.variants[h][w]:
                removed = False
                #stage one - return to self point check
                for i in variant:
                    if (i[0] == h) and (i[1] == w):
                        toRemove.append(variant)
                        removed = True
                        break
                if removed:
                    continue
                #stage two - check for one point meets twice in array
                for i in range(len(variant)):
                    for j in range(1+i, len(variant)):
                        if (variant[i][0] == variant[j][0]) and (variant[i][1] == variant[j][1]):
                            toRemove.append(variant)
                            removed = True
                            break
                    if removed:
                        break
                if removed:
                    continue
                #stage three - check for points already painted
                alreadyPainted = False
                if not crossword.condition[h][w][1] == 0:
                    alreadyPainted = True
                for i in variant:
                    if not crossword.condition[i[0]][i[1]][1] == 0:
                        if not alreadyPainted:
                            toRemove.append(variant)
                            removed = True
                            break
                    else:
                        if alreadyPainted:
                            toRemove.append(variant)
                            removed = True
                            break
                if removed:
                    continue

                for i in range(len(variant)-1):
                    if crossword.condition[variant[i][0]][variant[i][1]][0] > 0:
                        toRemove.append(variant)
                        removed = True
                        break
            for rem in toRemove:
                crossword.variants[h][w].remove(rem)
            toRemove = []

            if (len(crossword.variants[h][w]) == 0) and (not crossword.condition[h][w][0] == 0) and (crossword.condition[h][w][1] == 0):
                print("ololo")
                return False

    return True

#рекурсивная функция, основная
def solveLinkAPix(crossword, counter):
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

        if not heurDetectFalses(newcrossword):
            return False

        for stringstrcounter in range(len(newcrossword.variants)):
            toRemove = []
            for numcounter in range(len(newcrossword.variants[stringstrcounter])):
                if len(newcrossword.variants[stringstrcounter][numcounter]) == 1:
                    if paintRoute(newcrossword, stringstrcounter, numcounter, newcrossword.variants[stringstrcounter][numcounter][0]):
                        again = True
                        toRemove.append(numcounter)
                    else:
                        return False
            for i in toRemove:
                newcrossword.variants[stringstrcounter][i] = []

    #находим первый нерешённый элемент
    newcounter = -1
    for i in range(1+counter, newcrossword.height*newcrossword.width):
        if len(newcrossword.variants[i//newcrossword.height][i%newcrossword.width]) > 0:
            newcounter = i
            break

    #а может всё уже решено
    if newcounter == -1:
        crossword.condition = copy.deepcopy(newcrossword.condition)
        return True

    #выбрать вариант, пробовать пока пробуется и удалять если не подошли
    testCrossword = linkapix()
    testCrossword.condition = copy.deepcopy(newcrossword.condition)
    testCrossword.width = copy.deepcopy(newcrossword.width)
    testCrossword.height = copy.deepcopy(newcrossword.height)
    testCrossword.variants = copy.deepcopy(newcrossword.variants)

    while not len(testCrossword.variants[newcounter//testCrossword.height][newcounter%testCrossword.width]) == 0:

        painted = paintRoute(testCrossword, newcounter//testCrossword.height, newcounter%testCrossword.width,
            testCrossword.variants[newcounter//testCrossword.height][newcounter%testCrossword.width][0])

        testCrossword.variants[newcounter//testCrossword.height][newcounter%testCrossword.width].remove(
            testCrossword.variants[newcounter//testCrossword.height][newcounter%testCrossword.width][0])

        if not painted:
            testCrossword.condition = copy.deepcopy(newcrossword.condition)
            continue

        if solveLinkAPix(testCrossword, newcounter):
            crossword.condition = copy.deepcopy(testCrossword.condition)
            return True

        testCrossword.condition = copy.deepcopy(newcrossword.condition)

    return False

crossword = linkapix()
#читаем входной файл и парсим данные из него
crossword.init('sample2.txt')
heurPredetect(crossword)
#пытаемся решить
solved = solveLinkAPix(crossword, 0)
print(solved)
for i in crossword.condition:
    for ii in i:
        sys.stdout.write(str(ii[1]))
    sys.stdout.write("\n")