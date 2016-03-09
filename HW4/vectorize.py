#!/usr/bin/env python3
###########################################################################################
#This script collects sense information from a set of training data                       #
#it has a built in basic XML parser to avoid reading the entire data set into memory.     # 
#The available xml parsers for python also made extracting multiple instances of the same #
#head in a single context difficult due to the nature of the created object.              #
#-Zac Branson 03/02/2016                                                                  #
###########################################################################################

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
    sensids = []
 
    #get info from keyfile for test data
    if infile == 'EnglishLS.test':
        sensedic = {}
        with open('EnglishLS.test.key', 'r') as keyfile:
            for line in keyfile.read().splitlines():
                line = line.split()
                if line[0] == lex:
                    sensedic[line[1]] = line[2]

    for line in open(infile, 'r'):
        test = False
        train = False
        if infile == 'EnglishLS.train':
            train = True
        if infile == 'EnglishLS.test':
            test = True
        #checks for correct lexical item before parsing lines
        if line.startswith("<lexelt item=\""+ lex + "\">"):
            parsing = True
        elif line.startswith("</lexelt>"):
            parsing = False
        if parsing:     
            if train:
                if line.startswith("<answer"):
                    #print(line)
                    start = -14 - (len(lex) -2)
                    sensid = line[start:-4]

                    if sensid[-1] == 'U':
                        sensid = "U"

            if test:
                if line.startswith("<instance id"):
                    #print(line)
                    end = len(lex) + 27
                    instid = line[14:end]
                    #print(instid)
                    sensid = sensedic[instid]
                    #print(sensid)
                    
            #appends words from context to list 
            if line.startswith("<context>"):
                context = True            
            elif line.startswith("</context>"):
                context = False
            if context:
                words = line.split()
                wordlist = []
                if words[0] == "<context>":
                    pass
                else:
                    for word in words:
                        wordlist.append(word)
                    wordset = cleanWords(wordlist)               
                    wordsets.append(wordset)
                    sensids.append(sensid)

    return(wordsets, sensids)              

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

lexes = ['arm.n', 'interest.n', 'difficulty.n']
for lex in lexes:
    test_word_vecs = []
    train_word_vecs = []
    test_sensids = []
    train_sensids = []

    testin = 'EnglishLS.test'
    trainin = 'EnglishLS.train'
    #get sets of context words from file
    
    test_contexts, test_sensids = parse_file(testin, lex)
    train_contexts, train_sensids = parse_file(testin, lex)

    #makes set of unique words
    uniq_set = uniqueWords(test_contexts + train_contexts)

    #this makes vectors for each set of context words   
    word_vecs = []
    for word_set in test_contexts:
        #print(word_set)
        test_word_vec = vectorize(word_set, uniq_set)
        test_word_vecs.append(test_word_vec)    
    for word_set in train_contexts:
        #print(word_set)
        train_word_vec = vectorize(word_set, uniq_set)
        train_word_vecs.append(train_word_vec) 


    test_feature_file = lex + ".vecs.test.tsv"
    test_class_file = lex + ".class.test.txt"

    train_feature_file = lex + ".vecs.train.tsv"
    train_class_file = lex + ".class.train.txt"

    with open(test_feature_file, 'w') as out: 
        for vec in test_word_vecs:
            ones = 0
            for val in vec:
                #if val == 1:
                    #ones +=1
                 out.write(str(val) + "\t")
            #print(ones)   
            out.write("\n")

    with open(test_class_file, 'w') as out:
        for sensid in test_sensids:
            #print(sensid)
            out.write(sensid + '\n')
    
    with open(train_feature_file, 'w') as out: 
        for vec in train_word_vecs:
            ones = 0
            for val in vec:
                #if val == 1:
                    #ones +=1
                out.write(str(val) + "\t")
            #print(ones)   
            out.write("\n")

    with open(train_class_file, 'w') as out:
        for sensid in train_sensids:
            #print(sensid)
            out.write(sensid + '\n')



        
