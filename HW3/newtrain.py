###########################################################################################
#This script collects sense information from a set of training data                       #
#it has a built in basic XML parser to avoid reading the entire data set into memory      # 
#the available xml parser for python also made extracting multiple instances of the same  #
#head in a single context difficult due to the nature of the created object               #
#                                                                                         #
#it's ugl, but I need to use it for future assignments so I'm storing it for now          #
#-Zac Branson 02/16/2016                                                                  #
###########################################################################################

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



for line in open('EnglishLS.train', 'r'):
    
    #checks for correct lexical item before parsing lines
    if line.startswith("<lexelt item=\"arm.n\">"):
        parsing = True
    elif line.startswith("</lexelt>"):
        parsing = False
    if parsing:
        #adds instance id as first entry in list and triggers instance flag
        if line.startswith("<instance id="):
            instance = True
            subline = line[14:32]
            #print(subline)
            sublist.append(subline)
        # closes the current instance, appends instance sublist of id, words, and sense to features list 
        elif line.startswith("</instance>"):
            instance = False
            #appends sublist to features matrix
            if sublist:
                features.append(sublist)
                sublist = []
        # if we are in an instance, collects sense id
        if instance:
            if line.startswith("<answer"):
	        # this part has to be hardcoded depending on the length of the word.tag combination
                # could be fixed in future version with a boolean flag to turn colletion of characters
                # on and off
                senseid = line[-17:-4]
                # if senseid is unknown in training it's labeled 'U'
                if senseid[-1] == 'U':
                    senseid = 'U'
                sublist.append(senseid)
                print(senseid)
            #appends words from context to list by instance id
            if line.startswith("<context>"):
                context = True
                
            elif line.startswith("</context>"):
                context = False

            if context:
                words = line.split()
                for word in words:
                    sublist.append(word)                  
                    
#this collects words, senseid, and instnace id into the appropriate format for timbl
#takes from features matrix and puts into outlist matrix              
for l in features:
    # checks for empty lists and ignores them.  this should be functionalized or included when
    #appending list to features. update: included above now so redundant  
    if l:
        count = -1
        for word in l:
            #print(word)
            #print('xxxxxxxx')
            contexts = [None]*8
            count += 1
            #triggers collection of nearby words if current word is tagged as an instance
            if word.startswith("<head>"):
                #print('yyyyyyyyy')
                #print(l[count])
                contexts[0] = l[count-2]
                contexts[1] = l[count-1]
                contexts[4] = l[count-2]+ '_' + l[count-1]
                if l[count+2]:
                    contexts[2] = l[count+1]
                    contexts[3] = l[count+2]
                    contexts[5] = l[count-1] + '_' + l[count+1]
                    contexts[6] = l[count+1] + '_' + l[count+2]
                elif l[count+1]:
                    contexts[2] = l[count+1]
                    contexts[3] = ''
                    contexts[5] = l[count-1] + '_' + l[count+1]
                    contexts[6] = l[count+1] + '_' + '' 
                else:
                    contexts[2] = ''
                    contexts[3] = ''
                    contexts[5] = l[count-1] + '_' + ''
                    contexts[6] = '' + '_' + '' 
                contexts[7] = l[1]
                outlist.append(contexts)
                #for item in contexts:
                    #print(item)     

#writes to a tsv for TIMBL input
with open('arm.train.txt', 'w') as out: 
    for lis in outlist:
        for item in lis:
            out.write(str(item)+'\t')
        out.write('\n')


        
