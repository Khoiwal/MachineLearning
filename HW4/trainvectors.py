###########################################################################################
#This script collects sense information from a set of training data                       #
#it has a built in basic XML parser to avoid reading the entire data set into memory      # 
#the available xml parser for python also made extracting multiple instances of the same  #
#head in a single context difficult due to the nature of the created object               #
#-Zac Branson 02/16/2016                                                                  #
###########################################################################################

def cleanWords(words):
    #this generates a set of context words     
    punct = set([',','.','?','!','_','"',':',';'])  
    clean_word_list = []
    for word in words:
        word = "".join([ch for ch in word if ch not in punct]).lower()
        if word:
            clean_word_list.append(word)
    clean_wordset = set(clean_word_list)
    return(clean_wordset)

def parse_file(filename):
    #flags for parsing lines as they come in
    parsing = False
    context = False
    word_sets = [[]]

    for line in open(infile, 'r'):
    
        #checks for correct lexical item before parsing lines
        if line.startswith("<lexelt item=\"interest.n\">"):
            parsing = True
        elif line.startswith("</lexelt>"):
            parsing = False
        if parsing:      
            #appends words from context to list 
            if line.startswith("<context>"):
                context = True            
            elif line.startswith("</context>"):
                context = False
                features.append(sublist)
            if context:
                words = line.split()
                for word in words:
                    wordlist.append(word)
                wordset = cleanWords(wordlist)    
            wordsets.append(wordset)
    return(wordsets)              

#
def uniqueWords(wordsets):
    wordlist = []
    for wordset in wordets:
        wordlist.append(wordset)
    return(set(wordlist))
        
                        
def vectorize(words):
    word_dict = {}
    for word in word_set:
        word_dict[word] = 0
    for word in words:
        word_dict[word] = 1
    return(word_dict)

#get sets of context words from file
contexts = parse_file("EnglishLS.train")

#this makes vectors for each set of context words and puts them in a 2d list
word_vecs = [[]]
for word_set in contexts:
    word_dict = vectorize(word_set)
    word_vec = []
    for item in word_dict:
        word_vec.append(word_dict[item])
    word_vecs.append(word_vec)    
word_vecs = word_vecs[1:]
#print(word_vecs[0])

#writes to a tsv for TIMBL input
with open('interest.context_vectors.tsv', 'w') as out: 
    
    for vec in word_vecs:
        ones = 0
        for val in vec:
            if val == 1:
                ones +=1
            out.write(str(val) + "\t")
        print(ones)   
        out.write("\n")
    



        
