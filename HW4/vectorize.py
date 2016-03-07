#!/usr/bin/env python3
###########################################################################################
#This script collects sense information from a set of training data                       #
#it has a built in basic XML parser to avoid reading the entire data set into memory.     # 
#The available xml parsers for python also made extracting multiple instances of the same #
#head in a single context difficult due to the nature of the created object.              #
#-Zac Branson 03/02/2016                                                                  #
###########################################################################################
import sys

#determines if the word is the lexical item in question (between head tags in XML)
def isHead(word):
    beg = word[0:5]
    end = word[-5:]
    if beg != '<head':
        return False
    else:
        if end != 'head>':
            return False
        else:
            return True
#this takes in a list of words, removes punctuation, lowercases, and returns a set of
#unique clean words
def cleanWords(words):       
    punct = set([',','.','?','!','_','"',':',';',])  
    clean_word_list = []
    for word in words:
        word = "".join([ch for ch in word if ch not in punct]).lower()
        if not isHead(word):
            if word != '':
                clean_word_list.append(word)
    clean_wordset = set(clean_word_list)
    return(clean_wordset)
#this parses the input file to extract context words, it returns sets of words for each instance of the lexical item in question
def parse_file(infile,lex):
    #flags for parsing lines as they come in
    parsing = False
    context = False
    wordsets = []

    for line in open(infile, 'r'):
    
        #checks for correct lexical item before parsing lines
        if line.startswith("<lexelt item=\""+ lex + "\">"):
            parsing = True
        elif line.startswith("</lexelt>"):
            parsing = False
        if parsing:      
            #appends words from context to list 
            if line.startswith("<context>"):
                context = True            
            elif line.startswith("</context>"):
                context = False
            if context:
                words = line.split()
                wordlist = []
                for word in words:
                    wordlist.append(word)
                wordset = cleanWords(wordlist)               
                if '<context>' not in wordset:    
                    wordsets.append(wordset)
    return(wordsets)              

#creates a set of unique words for creating the context vector
def uniqueWords(wordsets): 
    words = []
    for wordset in wordsets:
        for word in wordset:
            words.append(word)
    unique_words = set(words)
    return(unique_words)
        
#creates a context vector                        
def vectorize(words,unique_words):
    word_vec = []
    for word in unique_words:
        if word in words:
            word_vec.append(1)
        else: word_vec.append(0)
    return(word_vec)

args = len(sys.argv)
#get sets of context words from file
try:
    contexts = parse_file(sys.argv[1],sys.argv[2])
except:
    print('vectorize.py <inputfile> <lexical_item>')
#makes set of unique words
uniq_set = uniqueWords(contexts)

#this makes vectors for each set of context words and puts them in a 2d list
word_vecs = []
for word_set in contexts:
    print(word_set)
    word_vec = vectorize(word_set, uniq_set)
    word_vecs.append(word_vec)    
#print(word_vecs[0])

#writes to a tsv for TIMBL input
if sys.argv[1] == 'EnglishLS.train':
    outfile = sys.argv[2] + ".vectors.train.tsv"
if sys.argv[1] == 'EnglishLS.test':
    outfile = sys.argv[2] + ".vectors.test.tsv"

with open(outfile, 'w') as out: 
    
    for vec in word_vecs:
        ones = 0
        for val in vec:
            if val == 1:
                ones +=1
            out.write(str(val) + "\t")
        print(ones)   
        out.write("\n")
    



        
