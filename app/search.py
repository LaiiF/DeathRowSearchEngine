#Returns info to results page
#Reference: https://towardsdatascience.com/tfidf-for-piece-of-text-in-python-43feccaa74f8
import csv
import re
import string
import nltk
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer, WordNetLemmatizer
import math
import time
from operator import itemgetter
import pickle
PUNCTUATION = re.compile('[~`!@#$%^&*()+={\[}\]|\\:;"\',<.>/?]')
stop_words = set(stopwords.words('english'))
#computes tf-idf and displays results page
#main searching method
#Term Frequency(TF) * Inverse Document Frequency (IDF) = TF-IDF
#t = term (word)
#d = document (set of words)
#N = count of docs
#TF = count of t in d / num words in d
#DF = occurence of t in documents
#IDF = log(N/(DF +1))
#TF-IDF = TF * IDF
def search(query):
    doclist = list()
    totaldocs = 0
    query_token ={}#list of query tokens
    parsedlist = list()#parsed doclist removed of punctuation and stop words
    totalwords = 0#N value
    freqDictlist = list()
    doc_info = []
    TFvals = []
    IDFvals = []
    TFIDFvals = None
    stemmer = PorterStemmer()
    ranking = []
    ii = 0#index
    display = []
    #clears punctuation from query
    query = PUNCTUATION.sub(' ', query)
    #query tokenize
    for qtoken in query.split(" "):
        qtoken = qtoken.lower().strip()
        if qtoken in stop_words:
            del qtoken
            continue
        qtoken = stemmer.stem(qtoken)
        if qtoken not in query_token:
            query_token[qtoken] = 1
        else:
            query_token[qtoken] += 1
    #open csv file
    with open('app/texasLastStatements.csv', 'r', encoding = 'utf-8', errors='ignore', newline= '') as csvfile:
        readlines = csv.DictReader(csvfile)
        for line in readlines:
            ii +=1
            doclist.append([ii, line['TDCJNumber'], line['FirstName'], line['LastName'], line['LastStatement']])
            totaldocs += 1
    #parses document of stop words and punctuation
    parsedlist = parseddoc(doclist)
    #counts total words in all docs
    for [TDCJNumber, FirstName, LastName, LastStatement] in parsedlist:
        for words in LastStatement:
            if words != 'none':
                totalwords +=1
    freqDictlist = freqdict(parsedlist, freqDictlist)#returns doc_id, index, word count for each doc
    doc_info = get_doc(parsedlist)#gets 'doc_id' , 'doc_length'
    start = time.time()
    try: #if TFIDF values are saved, do not compute.
        TFIDFvals = loadTFIDF(TFIDFvals, 'TFIDFDRS')
    except:
        if TFIDFvals is None:
            print("TFIDFvals is None")
        else:
            print(TFIDFvals)
    if TFIDFvals is None:#if TFIDF values are not saved, compute
        TFvals = TFCompute(freqDictlist, doc_info)
        IDFvals = IDFCompute(freqDictlist, doc_info)
        TFIDFvals = TFIDFCompute(TFvals, IDFvals)
    end = time.time()
    timetaken = end - start
    ranking = rank(TFIDFvals, query_token, totaldocs, freqDictlist)
    display = output(ranking, doclist)
    return query_token, display, totaldocs, totalwords, timetaken, TFIDFvals
#takes ranking of docs and displays full docs to user
def output(ranking, doclist):
    display = []
    temp = {}
    for num in ranking:
        for docs in doclist:
            id = docs[0]
            if num['doc_id'] == id:
                temp = {'doc_id' : id, 'FirstName' : docs[2], 'LastName' : docs[3], 'LastStatement' : docs[4]}
        display.append(temp)
        if(len(display) == 10):
            break
    for letter in display[0]['LastStatement']:
        if 'ÿ' in letter or '\\' in letter or string.punctuation in letter:
            letter = ''
    return display
#ranks the documents in accordance to the user query
def rank(TFIDFvals, query_token, totaldocs, freqDictlist):
    TFIDFvals = sorted(TFIDFvals, key = itemgetter('TFIDFval'), reverse = True)
    freqlist = []
    for docs in freqDictlist:
        id = docs['doc_id']
        for v in docs.values():
            freq = 0
            if type(v) == int: continue
            for key in v.keys():
                for term in query_token:
                    if(term == key):
                        freq +=1
                temp = {'doc_id': id,'freq': freq, 'key': key}
            freqlist.append(temp)
    freqlist = sorted(freqlist, key = itemgetter('freq'), reverse = True)
    return freqlist
#removes punctuation and stop words in doclist
def parseddoc(doclist):
    stop_words = set(stopwords.words('english'))
    parsedlist = list()
    ps = PorterStemmer()#Stemmatization variable
    lt = WordNetLemmatizer()#Lemmatization variable
    for [ii, TDCJNumber, FirstName, LastName, LastStatement] in doclist:
        lowerFName = ""
        #lowercasing all words in first name and rebuilding it
        for letter in FirstName:
            if letter not in string.punctuation:
                letter = letter.lower()
                lowerFName += letter
        lowerLName = ""
        #lowercasing all words in last name and rebuilding it
        for letter in LastName:
            if letter not in string.punctuation:
                letter = letter.lower()
                lowerLName += letter
        lowerLStatement = ""
        #lowercasing all words in last statement and rebuilding it
        for letter in LastStatement:
            if letter not in string.punctuation and 'ÿ' not in letter and '?' not in letter:  #and letter not in STOP_WORDS:
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
        #lemmatizing words from tokens
        for strings in statement_tokens:
            strings = lt.lemmatize(strings)
        parsedlist.append([int(TDCJNumber), lowerFName, lowerLName, statement_tokens])

    return parsedlist

def freqdict(parsedlist, freqDictlist):#creates freq dictionary using parsedlist
    ii = 0
    for [TDCJNumber, FirstName, LastName, LastStatement] in parsedlist:
        ii +=1
        freq_dict = {}
        for word in LastStatement:
            if word in freq_dict:
                freq_dict[word] += 1
            else:
                freq_dict[word] = 1
            temp = {'doc_id' : ii, 'freq_dict': freq_dict}
        freqDictlist.append(temp)
    return freqDictlist

def get_doc(parsedlist):
    doc_info = []
    i = 0
    for [TDCJNumber, FirstName, LastName, LastStatement] in parsedlist:
        count = 0
        i += 1
        for word in LastStatement:
            count +=1
        temp = {'doc_id' : i, 'doc_length' : count}
        doc_info.append(temp)
    return doc_info
#TF = count of t in d / num words in d
def TFCompute(freqDictlist, doc_info):
    TFvals = []
    for tempDict in freqDictlist:
        id = tempDict['doc_id']
        for keys in tempDict['freq_dict']:
            temp = {'doc_id' : id, 'TFval' : tempDict['freq_dict'][keys]/doc_info[id-1]['doc_length'], 'key' : keys}
            TFvals.append(temp)
    return TFvals

#IDF = log(N/(DF +1))
def IDFCompute(freqDictlist, doc_info):
    IDFvals = []
    count = 0
    for dict in freqDictlist:
        count +=1
        for keys in dict['freq_dict'].keys():
            counter = sum([keys in tempDict['freq_dict'] for tempDict in freqDictlist])
            temp = {'doc_id' : count, 'IDFval' : math.log(len(doc_info)/counter), 'key' : keys}
            IDFvals.append(temp)
    return IDFvals

def TFIDFCompute(TFvals, IDFvals):
    TFIDFvals = []
    for j in IDFvals:
        for i in TFvals:
            if j['key'] == i['key'] and j['doc_id'] == i['doc_id']:
                temp = {'doc_id' : j['doc_id'], 'TFIDFval' : j['IDFval']*i['TFval'], 'key' : i['key']}
        TFIDFvals.append(temp)
    saveTFIDF(TFIDFvals, 'TFIDFDRS')
    return TFIDFvals

def saveTFIDF(TFIDFvals, name):
    with open('app/obj/'+ name + '.pkl', 'wb') as f:
        pickle.dump(TFIDFvals, f, pickle.HIGHEST_PROTOCOL)

def loadTFIDF(TFIDFvals, name):
    with open('app/obj/' + name + '.pkl', 'rb') as f:
        return pickle.load(f)