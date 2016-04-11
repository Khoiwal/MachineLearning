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
    punct = set([',','_','\"','\'',':','(',')','[',']'])  
    clean_word_list = []
    for word in words:
        if not word:
            clean_word_list.append(str(word))
        else:
            word = "".join([ch for ch in word if ch not in punct]).lower()
            clean_word_list.append(word)
    return(clean_word_list)

def parse_file(infile,lex):
    #flags for parsing lines as they come in
    parsing = False
    context = False
    
    outlist = []
    sensids = []
 
    #get info from keyfile for test data
    if infile == 'RomanianLS.pos.test':
        sensedic = {}
        with open('RomanianLS.test.key', 'r',errors='ignore') as keyfile:
            for line in keyfile.read().splitlines():
                line = line.split()
                if line[0] == lex:
                    sensedic[line[1]] = line[2]

    for line in open(infile, 'r', errors='replace'):
        test = False
        train = False
        if infile == 'RomanianLS.pos.train':
            train = True
        if infile == 'RomanianLS.pos.test':
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
                        
                    contexts = [None]*8
                    count += 1
                    #triggers collection of nearby words if current word is tagged as an instance
                    if word.startswith("<head>"):

                        contexts[0] = words[count-2].split('/')[-1]
                        contexts[1] = words[count-1].split('/')[-1]
                        contexts[4] = words[count-2].split('/')[-1]+ '_' + words[count-1].split('/')[-1]
                        if words[count+2]:
                            contexts[2] = words[count+1].split('/')[-1]
                            contexts[3] = words[count+2].split('/')[-1]
                            contexts[5] = words[count-1].split('/')[-1] + '_' + words[count+1].split('/')[-1]
                            contexts[6] = words[count+1].split('/')[-1] + '_' + words[count+2].split('/')[-1]
                        elif words[count+1]:
                            contexts[2] = words[count+1].split('/')[-1]
                            contexts[3] = ''
                            contexts[5] = words[count-1].split('/')[-1] + '_' + words[count+1].split('/')[-1]
                            contexts[6] = words[count+1].split('/')[-1] + '_' + '' 
                        else:
                            contexts[2] = ''
                            contexts[3] = ''
                            contexts[5] = words[count-1].split('/')[-1] + '_' + ''
                            contexts[6] = '' + '_' + '' 
                            contexts[7] = words[1].split('/')[-1]
    
                        #print("xxxxx")
                        outlist.append(contexts)                         
                        sensids.append(sensid)         
    return(outlist,sensids)        

lexes = ['accent.n', 'citi.v', 'delfin.n', 'oficial.a', 'val.n']
for lex in lexes:
    test_word_features = []
    train_word_features = []
    test_sensids = []
    train_sensids = []

    testin = 'RomanianLS.pos.test'
    trainin = 'RomanianLS.pos.train'
    #get sets of context words from file
    
    test_contexts, test_sensids = parse_file(testin, lex)
    train_contexts, train_sensids = parse_file(trainin, lex)

    test_feature_file = lex + ".pos.features.test.tsv"
    test_class_file = lex + ".class.test.txt"

    train_feature_file = lex + ".pos.features.train.tsv"
    train_class_file = lex + ".class.train.txt"

    with open(test_feature_file, 'w') as out: 
        for word_list in test_contexts:
            for word in word_list:
                out.write(str(word) + "\t")       
            out.write("\n")

    with open(test_class_file, 'w') as out:
        for sensid in test_sensids:
            #print(sensid)
            out.write(sensid + '\n')
    
    with open(train_feature_file, 'w') as out: 
        for word_list in train_contexts:
            for word in word_list:
                out.write(str(word) + "\t")       
            out.write("\n")


    with open(train_class_file, 'w') as out:
        for sensid in train_sensids:
            #print(sensid)
            out.write(sensid + '\n')


 


