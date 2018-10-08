from mylib2399 import *
import pickle

#-------------------------------Executable file---------------------------------------------------------------------------
class createGreek7:
    def __init__(self):
        self.createGr7()
        sakouli = SakClass()
        degreeDict = self.getDegreeDict(sakouli)
        with open('greek7.pkl','wb') as g7pkl:
            pickle.dump(degreeDict,g7pkl)
        
    def createGr7(self):
        with open('greek.txt','r',encoding = "utf-8") as greek:
            with open('greek7.txt','w') as greek7:
                for line in greek:
                    if len(line) < 9 and len(line) > 2:
                        #Bαζουμε " len(line) < 9 " γιατι ο τελευταιος χαρακτηρας
                        #ειναι η αλλαγη γραμμης '\n'.
                        #Bάζουμε το " len(line) > 2 " γιατί θέλουμε
                        #να εξαιρέσουμε από τον κατάλογο των αποδεκτών λέξεων
                        #τις λέξεις με ενα μόνο γράμμα.
                        greek7.write(line)

    def getDegreeDict(self,sak):
        degreeDict = {}
        with open('greek7.txt','r') as greek7:
            for line in greek7:
                linesplit=list(line)
                degree=0
                for l in linesplit:
                    if l!='\n':
                        degree += sak.lets[l][1]
                degreeDict[line.strip()] = degree
        return degreeDict
