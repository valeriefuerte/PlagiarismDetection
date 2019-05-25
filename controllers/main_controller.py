import os
from PyQt5.QtCore import QObject
#from tokenize import tokenize, NUMBER, STRING, NAME, OP
from controllers.tokenizer import tokenize, NUMBER, STRING, NAME, OP
from io import BytesIO
from pandas import read_csv
from scipy._lib.six import xrange


class MainController(QObject):
    def __init__(self, model):
        super().__init__()

        self._model = model
        self.tasks = list(list())
        self.tokens = list(list())

    def readFiles(self, listOfFiles, task):
        tasks = list(list())
        tokens = list(list())
        i = 0
        
        try:
            for dirTask in listOfFiles:
                directoryOfTask = dirTask + "/" + task

                if os.path.exists(directoryOfTask) and os.path.getsize(directoryOfTask) > 0:
                        with open(directoryOfTask, 'r', encoding = "latin-1") as the_file:
                            file1 = the_file.read().lower()
                            tasks.insert(i, [directoryOfTask, file1])
                            i = i + 1
        except IOError:
            print("Can't read files!")
        #print(tasks)

        for i in range(len(tasks)):
            tokens.insert(i, self.decistmt(tasks[i][1]))

        self._model.setTokens(tokens)
        return tokens

    def countDistance(self, listOfFiles, task, studentsList, dist):
        tokens = self.readFiles(listOfFiles, task)

        if dist == 0:
            print("levenstein")
            with open('distance.csv', 'w') as distanceFile:
                #distanceFile.write('1, ')
                for i in range(len(tokens)):
                    if i != len(tokens)-1:
                            distanceFile.write(studentsList[i][0] + ",")
                    else:
                        distanceFile.write(studentsList[i][0])
                distanceFile.write('\n')
                for i in range(len(tokens)):
                    #distanceFile.write(studentsList[i][0] + ";")
                    for j in range(len(tokens)):
                        strDistance = str(self.leveshtein_distance(tokens[i], tokens[j]))
                        if j != len(tokens)-1:
                            distanceFile.write(strDistance + ',')
                        else:
                            distanceFile.write(strDistance)
                    distanceFile.write('\n')

            df = read_csv('distance.csv')
            listOfDistances = df.values
            #print(listOfDistances)
            self._model.setDistance(listOfDistances)

        if dist == 1:
            print("jaccard")
            with open('distanceJaccard.csv', 'w') as distanceFile:
                #distanceFile.write(' ;')
                for i in range(len(tokens)):
                    if i != len(tokens)-1:
                        distanceFile.write(studentsList[i][0] + ",")
                    else:
                        distanceFile.write(studentsList[i][0])
                distanceFile.write('\n')
                for i in range(len(tokens)):
                    #distanceFile.write(studentsList[i][0] + ";")
                    for j in range(len(tokens)):
                        strDistance = str(self.jaccard_distance(set(tokens[i]), set(tokens[j])))
                        if j != len(tokens)-1:
                            distanceFile.write(strDistance + ',')
                        else:
                            distanceFile.write(strDistance)
                    distanceFile.write('\n')

            df = read_csv('distanceJaccard.csv')
            listOfDistances = df.values
            self._model.setDistance(listOfDistances)


    def decistmt(self, s):
        result = []
        g = tokenize(BytesIO(s.encode('utf-8')).readline)  # tokenize the string

        for toknum, tokval, _, _, _ in g:
            if toknum == NUMBER and '.' in tokval:  # replace NUMBER tokens
                result.extend([
                    (NAME, 'Decimal'),
                    (OP, '('),
                    (STRING, repr(tokval)),
                    (OP, ')')
                ])
            else:
                result.append((toknum, tokval))
        return result

    def leveshtein_distance(self, token1, token2):
        if token1 == token2:
            return 0
        else:
            # Prepare a matrix
            slen, tlen = len(token1), len(token2)
            dist = [[0 for i in range(tlen + 1)] for x in range(slen + 1)]
            for i in xrange(slen + 1):
                dist[i][0] = i
            for j in xrange(tlen + 1):
                dist[0][j] = j

            # Counting distance
            for i in xrange(slen):
                for j in xrange(tlen):
                    cost = 0 if token1[i] == token2[j] else 1
                    dist[i + 1][j + 1] = min(
                        dist[i][j + 1] + 1,  # deletion
                        dist[i + 1][j] + 1,  # insertion
                        dist[i][j] + cost  # substitution
                    )
            return dist[-1][-1]

    def jaccard_distance(self, token1, token2):
        return (len(token1.union(token2)) - len(token1.intersection(token2))) / len(token1.union(token2))
