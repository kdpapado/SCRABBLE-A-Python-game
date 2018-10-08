import random
import pickle
import itertools

class SakClass:
    def __init__(self):
        self.lets = {'Α':[12,1],'Β':[1,8],'Γ':[2,4],'Δ':[2,4],'Ε':[8,1],
        'Ζ':[1,10],'Η':[7,1],'Θ':[1,10],'Ι':[8,1],'Κ':[4,2],
        'Λ':[3,3],'Μ':[3,3],'Ν':[6,1],'Ξ':[1,10],'Ο':[9,1],
        'Π':[4,2],'Ρ':[5,2],'Σ':[7,1],'Τ':[8,1],'Υ':[4,2],
        'Φ':[1,8],'Χ':[1,8],'Ψ':[1,10],'Ω':[3,3]
        }
        self.letlist = []
        self.randomize_sak()
        
    def randomize_sak(self):
        self.letlist=[]
        for i in self.lets:
            for k in range(self.lets[i][0]):
                self.letlist.append(i)
            random.shuffle(self.letlist)
            
    def getletters(self,N):
        getlets = random.sample(self.letlist,N)
        #subtracting in self.lets
        for i in getlets:
            if self.lets[i][0] > 0:
                self.lets[i][0] -= 1
        self.randomize_sak()
        return getlets
    
    def putbackletters(self,backlets):
        #adding in self.lets
        for i in backlets:
            self.lets[i][0] += 1
        self.randomize_sak()

    def remainedletters(self):
        remained = 0
        for i in self.lets:
            remained+=self.lets[i][0]
        return remained

    def completeLets(self,getlets,word):
        available=getlets[:]
        
        wordsplit=list(word)
        for i in wordsplit:
            flag=0
            for j in available:
                if i==j:
                    flag=1
                    break
            if flag==1:
                available.remove(j)
        self.randomize_sak()
        newLets = self.getletters(7-len(available))
        for letter in newLets:
            available.append(letter)
        return available

    def showAvLets(self,letters):
        for i,lett in enumerate(letters):
            if i!=6:
                print(lett,self.lets[lett][1],sep=',',end=' - ')
            else:
                print(lett,self.lets[lett][1],sep=',',end='')

class PlayersGame:
    def __init__(self):
        self.score=0

    def checkWord(self,word,getlets):
        available = getlets[:]
        wordsplit=list(word)
        for i in wordsplit:
            flag=0
            for j in available:
                if i==j:
                    flag=1
                    break
            if flag==1:
                available.remove(j)
            if flag==0:
                #Η λέξη είχε γράμματα που δεν είναι διαθέσιμα
                tag = 1
                break
        if flag!=0:    
            my_file = open('greek7.txt','r')
            exist=0
            for line in my_file:
                if word==line.strip():
                    #Αποδεκτή λέξη
                    exist=1
                    tag = 2
                    break
            my_file.close()
            if exist==0:
                tag = 3
                available = getlets[:]
                
        return tag
    def getScores(self,player,pc):
        print('\n-Το τελικό σου σκορ: ', player.score)
        print('\n-Το τελικό σκορ του Η/Υ: ', pc.score)


class PCGameAlgor:
    def __init__(self,choice):
        self.choice = choice
    
    def minLetters(self,pcPlayer,available,sak):
        endIt = 0
        with open('greek7.pkl','rb') as g7pkl:
            degreeDict = pickle.load(g7pkl)
        found = 0
        for i in range(2, len(available)+1):
            for subset in itertools.permutations(available,i):
                string = ''.join(subset)
                if string in degreeDict:
                    degree = degreeDict[string]
                    pcPlayer.score += degree
                    print('Λέξη Η/Υ: ',string,', Βαθμοί: ', degree,'- Σκορ Η/Υ: ',pcPlayer.score)
                    found = 1
                    break
            if found == 1:
                break
 
        if found == 1:
            remained = SakClass.remainedletters(sak)
            if remained >= 7:
                available = SakClass.completeLets(sak,available,string)
            else:
                print('\nΓράμματα στο σακουλάκι:',remained)
                print('\nΤο σακουλάκι δεν έχει αρκετά γράμματα.\nΤΕΛΟΣ ΠΑΙΧΝΙΔΙΟΥ!')
                endIt = 1
        else:
            print('\nΟ Η/Υ δεν βρήκε καμία αποδεκτή λέξη.\nΤΕΛΟΣ ΠΑΙΧΝΙΔΙΟΥ!')
            endIt = 1
        return found,endIt,available
    
    def maxLetters(self,pcPlayer,available,sak):
        endIt = 0
        with open('greek7.pkl','rb') as g7pkl:
            degreeDict = pickle.load(g7pkl)
        found = 0
        for i in range(len(available),1,-1):
            for subset in itertools.permutations(available,i):
                string = ''.join(subset)
                if string in degreeDict:
                    degree = degreeDict[string]
                    pcPlayer.score += degree
                    print('Λέξη Η/Υ: ',string,', Βαθμοί: ', degree,'- Σκορ Η/Υ: ',pcPlayer.score)
                    found = 1
                    break
            if found == 1:
                break
        if found == 1:
            remained = SakClass.remainedletters(sak)
            if remained >= 7:
                available = SakClass.completeLets(sak,available,string)
            else:
                print('\nΓράμματα στο σακουλάκι:',remained)
                print('\nΤο σακουλάκι δεν έχει αρκετά γράμματα.\nΤΕΛΟΣ ΠΑΙΧΝΙΔΙΟΥ!')
                endIt = 1
        else:
            print('\nΟ Η/Υ δεν βρήκε καμία αποδεκτή λέξη.\nΤΕΛΟΣ ΠΑΙΧΝΙΔΙΟΥ!')
            endIt = 1
        return found,endIt,available

        
    def smartLetters(self,pcPlayer,available,sak):
        endIt = 0
        acceptable = []
        found = 0

        with open('greek7.pkl','rb') as g7pkl:
            degreeDict = pickle.load(g7pkl)

        found = 0
        maxDegree = 0
        for i in range(2, len(available)+1):
            for subset in itertools.permutations(available,i):
                string = ''.join(subset)
                if string in degreeDict:
                    found = 1
                    degree = degreeDict[string]
                    if (degree > maxDegree):
                        maxDegree = degree
                        maxWord = string   
        if found == 1:
            pcPlayer.score += maxDegree
            print('Λέξη Η/Υ: ',maxWord,', Βαθμοί: ', maxDegree,'- Σκορ Η/Υ: ',pcPlayer.score)
            
            remained = SakClass.remainedletters(sak)
            if remained >= 7:
                available = SakClass.completeLets(sak,available,maxWord)
            else:
                print('\nΓράμματα στο σακουλάκι:',remained)
                print('\nΤο σακουλάκι δεν έχει αρκετά γράμματα.\nΤΕΛΟΣ ΠΑΙΧΝΙΔΙΟΥ!')
                endIt = 1
        else:
            print('\nΟ Η/Υ δεν βρήκε καμία αποδεκτή λέξη.\nΤΕΛΟΣ ΠΑΙΧΝΙΔΙΟΥ!')
            endIt = 1
        return found,endIt,available
    
