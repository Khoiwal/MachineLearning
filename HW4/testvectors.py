###########################################################################################
#This script collects sense information from a set of test data                           #
#it has a built in basic XML parser to avoid reading the entire data set into memory      # 
#the available xml parser for python also made extracting multiple instances of the same  #
#head in a single context difficult due to the nature of the created object               #
#                                                                                         #
#it's ugl, but I need to use it for future assignments so I'm storing it for now          #
#-Zac Branson 02/16/2016                                                                  #
#where theis script is the same as newtrain.py, the documentation is not repeated here    #
###########################################################################################


parsing = False
instance = False
context = False
features = [[]]
sublist = []

def vectorize(words):
    word_dict = {}
    for word in word_set:
        word_dict[word] = 0
    for word in words:
        word_dict[word] = 1
    return(word_dict)

#function which return sense from a test key file
def getSense(insid):
    with open('EnglishLS.test.key', 'r') as test:
        data = test.readlines()
        for line in data:
            line = line.split()
            if line[1] == insid:
                print(line[2])
                return(line[2])

for line in open('EnglishLS.test', 'r'):
    
    #checks for correct lexical item before parsing lines
    if line.startswith("<lexelt item=\"arm.n\">"):
        parsing = True
    elif line.startswith("</lexelt>"):
        parsing = False
    if parsing:
        #adds instance id as first entry in list
        if line.startswith("<instance id="):
            instance = True
            subline = line[14:37]
            print(subline)
            sublist.append(subline)
            senseid = getSense(subline)
            if not senseid:
                senseid = 'U'
            else:
                if senseid[-1] == 'U':
                    senseid = 'U'
            sublist.append(senseid)
            #print(senseid)
         
        elif line.startswith("</instance>"):
            instance = False
            features.append(sublist)
            sublist = []
        if instance:


            #gets context, puts into string and appends to appropriate list item by instance id
            if line.startswith("<context>"):
                context = True
                #initializes words as an empty list here so it resets when on a new context
            elif line.startswith("</context>"):
                context = False

            if context:
                words = line.split()
                for word in words:
                    sublist.append(word)                  
                    
                
#this generates a set of context words     
punct = set([',','.','?','!','_','"',':',';'])  
word_list = []  
for l in features:
    for word in l:
        word = "".join([ch for ch in word if ch not in punct]).lower()
        if word:
            word_list.append(word)
word_set = set(word_list)
#print(word_set)
word_vecs = [[]]
#this makes vectors for each set of context words and puts them in a 2d list
for l in features[1:]:
    word_dict = vectorize(l)
    word_vec = []
    for item in word_dict:
        word_vec.append(word_dict[item])
    word_vecs.append(word_vec)    
word_vecs = word_vecs[1:]
#print(word_vecs[0])

#writes to a tsv for TIMBL input
with open('arm.test.context_vectors.tsv', 'w') as out: 
    
    for vec in word_vecs:
        ones = 0
        for val in vec:
            if val == 1:
                ones +=1
            out.write(str(val) + "\t")
        print(ones)   
        out.write("\n")
        
