from nltk import stem

#flags for parsing lines as they come in
parsing = False
instance = False
context = False
# feature matrix which collects all senseid, instanceid, and words in context
features = [[]]
#list of senseid, instanceid, and words in context
sublist = []
#basically a sorted version of features for easy writing to file
outlist = [[]]

def cleanWords(words):       
    punct = set([',','_','\"','\'',':','(',')','[',']','-'])  
    clean_lemmas = []
    for word in words:
        if word:          
            word = "".join([ch for ch in word if ch not in punct]).lower()
            #lemmatize = stem.snowball.RomanianStemmer(ignore_stopwords=False)
            #word = lemmatize.stem(word)
        if not word: word = "X"
        clean_lemmas.append(word)
    return(clean_lemmas)

def parse_file(infile,lex):
    #flags for parsing lines as they come in
    parsing = False
    context = False
    
    outlist = []
    sensids = []
 
    #get info from keyfile for test data
    if infile == 'RomanianLS.test':
        sensedic = {}
        with open('RomanianLS.test.key', 'r',errors='ignore') as keyfile:
            for line in keyfile.read().splitlines():
                line = line.split()
                if line[0] == lex:
                    sensedic[line[1]] = line[2]

    for line in open(infile, 'r', errors='replace'):
        test = False
        train = False
        if infile == 'RomanianLS.train':
            train = True
        if infile == 'RomanianLS.test':
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
                    end = len(lex) + 28
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
        
           
                count = -1
                for word in words:
                        
                    contexts = [None]*7
                    count += 1
                    #triggers collection of nearby words if current word is tagged as an instance
                    if word.startswith("<head>"):
                        #this part accounts for the head being the first or second word
                        if count == 0:
                            contexts[0] = ""
                            contexts[1] = ""
                            contexts[4] = ""
                        elif count == 1:
                            contexts[0] = ""
                            contexts[1] = words[count-1]
                            contexts[4] = "_" + words[count-1]
                        else:
                            contexts[0] = words[count-2]
                            contexts[1] = words[count-1]
                            contexts[4] = words[count-2]+ "_" + words[count-1]
                        #this part account for the head being the final or penultimate word
                        if words[count+2]:
                            contexts[2] = words[count+1]
                            contexts[3] = words[count+2]
                            contexts[5] = words[count-1] + "_" + words[count+1]
                            contexts[6] = words[count+1] + "_" + words[count+2]
                        elif words[count+1]:
                            contexts[2] = words[count+1]
                            contexts[3] = ""
                            contexts[5] = words[count-1] + "_" + words[count+1]
                            contexts[6] = words[count+1] + "_" 
                        else:
                            contexts[2] = ""
                            contexts[3] = ""
                            contexts[5] = words[count-1] + "_" 
                            contexts[6] = "" 
                            
                        #print("xxxxx")
                        outlist.append(cleanWords(contexts))                         
                        sensids.append(sensid)         
    return(outlist,sensids)        

lexes = ['accent.n', 'citi.v', 'delfin.n', 'oficial.a', 'val.n']
for lex in lexes:
    test_word_features = []
    train_word_features = []
    test_sensids = []
    train_sensids = []

    testin = 'RomanianLS.test'
    trainin = 'RomanianLS.train'
    #get sets of context words from file
    
    test_contexts, test_sensids = parse_file(testin, lex)
    train_contexts, train_sensids = parse_file(trainin, lex)

    test_feature_file = lex + ".words.test.tsv"
    train_feature_file = lex + ".words.train.tsv"
    
    with open(test_feature_file, 'w') as out: 
        for i in range(0,len(test_sensids)):
            for word in test_contexts[i]:
                out.write(str(word) + "\t")       
            out.write(test_sensids[i]+'\n')
  
    with open(train_feature_file, 'w') as out: 
        for i in range(len(train_sensids)):
            for word in train_contexts[i]:
                out.write(str(word) + "\t")       
            out.write(train_sensids[i]+'\n')

    
 


 


