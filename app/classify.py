#returns classification of data entry based on bag of words model data
#reference: http://www.insightsbot.com/bag-of-words-algorithm-in-python-introduction/
#Use macros to represent what each last statement is about. Categorical values.
#Family     0       keywords: Brother, Sister, Father, Mother, Son, Daughter, Uncle, Aunt, Cousin, Family, Child, Children, Dad, Mom, Parent
#Government 1       keywords: Attorney, State, Judge, Conviction, Sentence, Fair, Unfair, County, Government, Justice, Injustice, Court, Law, United States, Innocent, Guilt
#Life       2       keywords: Live, Friend, Fun, Happy, God, Allah, Christian, Muslim, Jesus, Lord
#Death      3       keywords: Spirit, Peace, Death, Dead, Lethal, Victim, Kill, Shoot, Pain, Suffer, War, Funeral, Heaven
#Take percentages for each statement. Keywords.
import csv
import string
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
stop_words = set(stopwords.words('english'))

#Training data
famKeys = ["brother", "sister", "father", "mother", "son", "daughter", "uncle", "aunt", "cousin", "family", "child", "children", "dad", "mom", "parent", "wife", "husband", "kid"]
govKeys = ["attorney", "state", "judge", "conviction", "sentence", "fair", "unfair", "warden", "government", "justice", "injustice", "court", "law", "texas", "innocent", "guilt"]
lifeKeys = ["live", "friend", "fun", "happy", "love", "god", "allah", "christian", "muslim", "jesus", "lord", "world", "amen"]
deathKeys = ["spirit", "peace", "death", "dead", "lethal", "victim", "kill", "shoot", "pain", "suffer", "war", "funeral", "heaven"]
#Iterate over each list and classify each statement in accordance to hits.
#Ex. doc_id = 1, lastStatement = "...", classification = [.25, .40, .20, .15] //family, gov, life, death

def classify():
    doc_id = 0
    doclist = list()
    parsedlist = list()
    with open('app/texasLastStatements.csv', 'r', encoding = 'utf-8', errors='ignore', newline= '') as csvfile:
        readlines = csv.DictReader(csvfile)
        for line in readlines:
            doc_id+=1
            doclist.append([[doc_id], line['FirstName'], line['LastName'], line['LastStatement']])
    parsedlist = parselist(doclist)
    classylist = findHits(parsedlist)
    return classylist

def parselist(doclist):
    ps = PorterStemmer()
    parsedlist = list()
    for [doc_id, FirstName, LastName, LastStatement] in doclist:
        lowerLStatement = ""
        for letter in LastStatement:
            if letter not in string.punctuation and 'ÿ' not in letter and '?' not in letter:
                letter = letter.lower()
                lowerLStatement += letter
        #tokenize last statement list
        statement_tokens = word_tokenize(lowerLStatement)
        #removing stop words from last statement
        for word in statement_tokens:
            if word in stop_words:
                statement_tokens.remove(word)
        #stemming words from tokens
        for w in statement_tokens:
            w = ps.stem(w)
        parsedlist.append([doc_id, FirstName, LastName, statement_tokens, LastStatement])
    return parsedlist

def findHits(parsedlist):
    classylist = list()
    for [doc_id, FirstName, LastName, statement_tokens, LastStatement] in parsedlist:
        famp = 0 #Family percentage
        govp = 0 #Government percentage
        lifp = 0 #Life percentage
        deap = 0 #Death percentage
        hitword = 0 #total num of keywords hit
        for letter in LastStatement:
            if 'ÿ' in letter or '?' in letter:
                letter = ''
        classes = [0,0,0,0]
        for token in statement_tokens:
            if token in famKeys:
                famp+=1
                hitword+=1
            elif token in govKeys:
                govp+=1
                hitword+=1
            elif token in lifeKeys:
                lifp+=1
                hitword+=1
            elif token in deathKeys:
                deap+=1
                hitword+=1
        #Future development: Add weights to words to have more accurate classifications.
            if hitword == 0:
                classes[0] = 0
                classes[1] = 0
                classes[2] = 0
                classes[3] = 0
            else:
                classes[0] = round(float(famp/hitword),2)
                classes[1] = round(float(govp/hitword),2)
                classes[2] = round(float(lifp/hitword),2)
                classes[3] = round(float(deap/hitword),2)
                dominant = max(classes[0], classes[1], classes[2], classes[3])
                if(dominant == classes[0]):
                    classification = "Family"
                elif(dominant == classes[1]):
                    classification = "Government"
                elif(dominant == classes[2]):
                    classification = "Life"
                elif(dominant == classes[3]):
                    classification = "Death"
        classylist.append([doc_id, FirstName, LastName, LastStatement, (classes[0], classes[1], classes[2], classes[3]), classification])
    return classylist
