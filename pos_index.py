# pos_index.py - Be sure to run in python 3.6.3^
# Author: Joe Williams

import sys
import pickle # For serializing data
import os.path # For checking whether a file exist

from nltk.stem import PorterStemmer as ps # For stemming and word tokenization
#from nltk.tokenize import sent_tokenize, word_tokenize # 

# Takes a file that has a list of files
def getInputFiles(filelist):
    with open(filelist) as f:
        return [a for a in f.read().split("\n") if a != ""]

files = getInputFiles("input-files.txt")

# Removes most special characters and caps
def preprocess(data):
    for p in "!.,:@#$%^&?<>*()[}{]-=;/\"\\\t\n":
        if p in '\n;?:!.,.':
            data = data.replace(p,' ')
        else: data = data.replace(p,'')
    return data.lower()

# For each file, opens and adds it to the hashmap
def createPositionalIndex(files):
    index = {}
    for i in range(len(files)):
        with open(files[i]) as f:
            doc = [a for a in preprocess(f.read()).split(' ') if a != ""]
        for idx, word in enumerate(doc):
            stemmed = ps().stem(word)
            if not stemmed in index:
                index[stemmed] = [(i,idx)]
            else: index[stemmed].append((i,idx))
    return index

# shows a preview based on the positions and the how 
# much text to show around the data found
def showPreview(positions,radius):
    for i, (doc_id, word_index) in enumerate(positions):
        docArr = getInputFiles("input-files.txt")
        with open(docArr[doc_id]) as f:
            wordArr = [a for a in preprocess(f.read()).split(' ') if a != ""]
            result = " ".join(wordArr[word_index-radius:word_index+radius])
            print(str(i+1)+": ..."+result+"- "+files[doc_id].split("/")[-1]+"... :"+str(word_index))
        print()

# Serialization/Positional Index
pi = {}
if os.path.isfile("index_data"):
    print("Loading data...")
    with open("index_data","rb") as f:
        pi = pickle.load(f)
else:
    print("Processing and serializing data for future use...")
    pi = createPositionalIndex(files)
    with open("index_data","wb") as f:
        pickle.dump(pi,f)

# User interface and positional index querying
while 1:
    print("Enter Query: 'word word <int>'")
    sys.stdout.write("'/exit' to close > ")
    q = [a for a in input().lower().split(' ') if a != ""]
    matches = []
    if len(q) == 1 and q[0] == '/exit':
        exit()
    elif len(q) == 2:
        word1, word2 = q
        word1 = ps().stem(preprocess(word1).replace(' ',''))
        word2 = ps().stem(preprocess(word2).replace(' ',''))
        print(word1)
        print("Loading... \n")
        for doc1, index1 in pi[word1]:
            for doc2, index2 in pi[word2]:
                if doc1 != doc2: continue
                if index1 == (index2 - 1): matches.append( (doc1,index1) )
        showPreview(matches,5)
    elif len(q) == 3:
        word1, word2, l = q
        rad = int(l)
        for doc1, index1 in pi[word1]:
            for doc2, index2 in pi[word2]:
                if doc1 != doc2: continue
                abs_pos = abs(index1 - index2)
                # when abs_pos is 0, the word is itself
                if abs_pos <= rad and abs_pos != 0: matches.append( (doc1,index1) )
        showPreview(matches, 5 if rad <= 5 else rad)
    else: print("Needs to have 2 or 3 args")
