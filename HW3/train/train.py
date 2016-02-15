from bs4 import BeautifulSoup

difficulty = {}
#parses input file into a tree object
soup = BeautifulSoup(open("./EnglishLS.train"))

lexitems = soup.find_all('lexelt')
for lexitem in lexitems:
    if lexitem['item'] == "difficulty.n":
        instances = lexitem.find_all('instance')
        for instance in instances:
            difficulty[instance['id']] = [None]*8
            difficulty[instance['id']][7] = instance.answer['senseid']
            texts = instance.context
            for text in texts:
                words = text.lower().split()
                count = 0
                while(count < len(words)):
                                    
                    if words[count] == 'difficulty' or words[count] == 'difficulties':
                        difficulty[instance['id']][0] = words[count-2] 
                        difficulty[instance['id']][1] = words[count-1]
                        difficulty[instance['id']][4] = words[count-2] + '_' + words[count-1]
                        if (len(words) - count) >= 3:
                            difficulty[instance['id']][2] = words[count+1]
                            difficulty[instance['id']][3] = words[count+2]
                            difficulty[instance['id']][5] = words[count-1] + '_' + words[count+1]
                            difficulty[instance['id']][6] = words[count+1] + '_' + words[count+2]
                        elif (len(words) - count) == 2:   
                            difficulty[instance['id']][2] = words[count+1]
                            difficulty[instance['id']][3] = ''
                            difficulty[instance['id']][5] = words[count-1] + '_' + words[count+1]
                            difficulty[instance['id']][6] = words[count+1] + '_' + ''
                        else:
                            difficulty[instance['id']][2] = ''
                            difficulty[instance['id']][3] = ''
                            difficulty[instance['id']][5] = words[count-1] + '_' + ''
                            difficulty[instance['id']][6] = '' + '_' + ''

                    count += 1

with open("difficulty.timblin.txt" , "w") as out:
    for contexts in difficulty:
        for context in difficulty[contexts]:
            out.write(context+'\t')
        out.write('\n')   

	

