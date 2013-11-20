from copy import deepcopy


class linkapix():
    condition = [[]]
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
                    tempdata.append(0)
                self.condition.append(tempdata)
                prevNumber = False
                tempdata = []
                continue

            if not i == ',':
                tempdata.append(int(i))
                prevNumber = True
            else:
                if prevNumber:
                    prevNumber = False
                else:
                    tempdata.append(0)
        if not prevNumber:
            tempdata.append(0)
        self.condition.append(tempdata)
        self.condition.remove(self.condition[0])

        #инициализируем массив под варианты
        tempdata = [[]]
        self.height = len(self.condition)
        self.width = len(self.condition[0])
        for i in range(self.height):
            for ii in (range(self.width) - 1):
                tempdata.append([])
            self.variants.append(tempdata)
            tempdata = [[]]
        self.variants.remove(self.variants[0])

#функция заполняет массив всевозможных вариантов для каждого элемента кроссворда
def getVariants(crossword):
    #WARNING!!! нужно сюда привязать код Маши
    return


#функция, которая закрашивает клетки по указанному маршруту
def paint(crossword, route):
    for i in route:
        crossword[int(i / crossword.height)][i % crossword.width] = -1

#функиця, которая находит первый элемент с единственным вариантом заполнения и заполняет кроссворд этим вариантом
def paintFirstOneVariants(crossword):
    size = crossword.width * crossword.height

    for i in range(size):
        if not len(crossword.variants[int(i / crossword.height)][i % crossword.width]) == 1:
            continue

        paint(crossword, crossword.variants[int(i / crossword.height)][i % crossword.width][0])
        return True
    return False

#рекурсивная функция, основная
def solveLinkAPix(crossword):
    newcrossword = linkapix()
    newcrossword.condition = deepcopy(crossword.condition)
    newcrossword.height = deepcopy(crossword.height)
    newcrossword.width = deepcopy(crossword.width)
    #назаполняем варианты с единственными решениями
    again = True
    while again:
        again = False
        #позовём функцию, которая заполнит newcrossword.variants, если она для какого то элемента не нашла варианты,
        #комбинация ошибочна и возвращаем рекурсию на один уровень вверх
        if not getVariants(newcrossword):
            return False

        #пока заполняется, заполняем варианты с единственным решением, по одному за итерацию цикла
        if paintFirstOneVariants(newcrossword):
            again = True
    #WARNING!!! функция недописана

crossword = linkapix()
#читаем входной файл и парсим данные из него
crossword.init('sample1.txt')
#пытаемся решить
solved = solveLinkAPix(crossword)
