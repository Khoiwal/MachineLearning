parsing = False
instance = False
context = False
features = [[]]
sublist = []
outlist = [[]]

#function which return sense from test key
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
    if line.startswith("<lexelt item=\"interest.n\">"):
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
                    
                
for l in features:
    
    if l:
        count = -1
        for word in l:
            #print(word)
            #print('xxxxxxxx')
            contexts = [None]*8
            count += 1
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
                for item in contexts:
                    print(item)     


with open('interest.newtest.txt', 'w') as out: 
    for lis in outlist:
        for item in lis:
            out.write(str(item)+'\t')
        out.write('\n')


        
