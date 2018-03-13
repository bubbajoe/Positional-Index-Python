# indexing.py - Be sure to run in python 3.6.3^
# Author: Joe Williams
# ReadMe - the first time though the program will take a 
# while to process and serialize the data, but it wont after that
import pickle # For serializing data
import os.path # For checking whether a file exist
from nltk.stem import PorterStemmer 
from nltk.tokenize import sent_tokenize, word_tokenize
# For stemming and word tokenization
ps = PorterStemmer()

# Takes a file that has a list of files
def getInputFiles(filelist):
    stream = open(filelist)
    fileArray = stream.read().split("\n")
    stream.close()
    return fileArray

# Removes most special characters and caps
def preprocess(data):
    data = data.lower()
    for p in "!.,:@#$%^&?<>'*()[}{]-=;/\"\\\t\n":
        if p in '\n;?:!.,.':
            data = data.replace(p,' ')
        else: data = data.replace(p,'')
    return data

def createPositionalIndex(files):
    index = {}
    for i in range(len(files)):
        f = open(files[i])
        doc = preprocess(f.read()).split(' ')
        for idx, word in enumerate(doc):
            stemmed = ps.stem(word)
            if not stemmed in index:
                index[stemmed] = [(i,idx)]
            else: index[stemmed].append((i,idx))
    return index

def showPreview(positions,radius):
    for doc_id, word_index in positions:
        docArr = getInputFiles("input-files.txt")
        with open(docArr[doc_id]) as f:
            wordArr = preprocess(f.read()).split(' ')
            result = ""
            for word in wordArr[word_index-radius:word_index+radius]:
                result +=  word + " "
            print(result+" - "+doc_id+":"+ )

pi = {}
if os.path.isfile("index_data"):
    print("Loading data...")
    with open("index_data","rb") as f:
        pi = pickle.load(f)
else:
    print("Creating and serializing data for future use...")
    files = getInputFiles("input-files.txt")
    pi = createPositionalIndex(files)
    with open("index_data","wb") as f:
        pickle.dump(pi,f)

while 1:
    print("Enter Query: 'Love her 4'")
    q = input().lower().split(' ')
    matches = []
    if len(q) == 2:
        word1, word2 = q
        word1 = ps.stem(word1)
        word2 = ps.stem(word2)
        print(word1 + " " + word2)
        for doc1, index1 in pi[word1]:
            for doc2, index2 in pi[word2]:
                if doc1 != doc2: continue
                if index1 == (index2 - 1):
                    matches.append( (doc1,index1) )
        showPreview(matches,5)
    elif len(q) == 3:
        word1, word2, length = q
        for doc1, index1 in pi[word1]:
            for doc2, index2 in pi[word2]:
                if doc1 != doc2: continue
                if abs(index1 - index2) <= length:
                    matches.append( (doc1,index1) )
        showPreview(matches,5)
    elif q[0] == 'exit': exit()
    else: print("Needs to have 2 or 3 args")
