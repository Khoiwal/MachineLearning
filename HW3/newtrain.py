parsing = False
instance = False
context = False
features = [[]]
sublist = []
outlist = [[]]



for line in open('EnglishLS.train', 'r'):
    
    #checks for correct lexical item before parsing lines
    if line.startswith("<lexelt item=\"arm.n\">"):
        parsing = True
    elif line.startswith("</lexelt>"):
        parsing = False
    if parsing:
        #adds instance id as first entry in list
        if line.startswith("<instance id="):
            instance = True
            subline = line[14:32]
            #print(subline)
            sublist.append(subline)
         
        elif line.startswith("</instance>"):
            instance = False
            features.append(sublist)
            sublist = []
        if instance:
            if line.startswith("<answer"):
	
                senseid = line[-17:-4]
                if senseid[-1] == 'U':
                    senseid = 'U'
                sublist.append(senseid)
                print(senseid)
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


with open('arm.train.txt', 'w') as out: 
    for lis in outlist:
        for item in lis:
            out.write(str(item)+'\t')
        out.write('\n')


        
