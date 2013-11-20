class linkapix():
    condition = [[]]
    variants = [[[]]]

    def init(self, filename):
        #read data
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

        #init variants array
        tempdata = [[]]
        for i in range(len(self.condition)):
            for ii in range(len(self.condition[0]) - 1):
                tempdata.append([])
            self.variants.append(tempdata)
            tempdata = [[]]
        self.variants.remove(self.variants[0])

test = linkapix()
test.init('sample1.txt')



print(test.variants)

