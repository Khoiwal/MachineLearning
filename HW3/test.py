from bs4 import BeautifulSoup

arm = {}
#parses input file into a tree object
soup = BeautifulSoup(open("./EnglishLS.test"))

#function which return sense from test key
def getSense(insid):
    with open('EnglishLS.test.key', 'r') as test:
        data = test.readlines()
        for line in data:
            line = line.split()
            if line[1] == insid:
                return(line[2])

lexitems = soup.find_all('lexelt')
for lexitem in lexitems:
    if lexitem['item'] == "arm.n":
        instances = lexitem.find_all('instance')
        for instance in instances:
            arm[instance['id']] = [None]*8
            #arm[instance['id']][7] = instance.answer['senseid']
            arm[instance['id']][7] = getSense(instance['id'])
            texts = instance.context
            for text in texts:
                words = text.lower().split()
                count = 0
                while(count < len(words)):
                                    
                    if words[count] == 'arm' or words[count] == 'arms':
                        arm[instance['id']][0] = words[count-2] 
                        arm[instance['id']][1] = words[count-1]
                        arm[instance['id']][4] = words[count-2] + '_' + words[count-1]
                        if (len(words) - count) >= 3:
                            arm[instance['id']][2] = words[count+1]
                            arm[instance['id']][3] = words[count+2]
                            arm[instance['id']][5] = words[count-1] + '_' + words[count+1]
                            arm[instance['id']][6] = words[count+1] + '_' + words[count+2]
                        elif (len(words) - count) == 2:   
                            arm[instance['id']][2] = words[count+1]
                            arm[instance['id']][3] = ''
                            arm[instance['id']][5] = words[count-1] + '_' + words[count+1]
                            arm[instance['id']][6] = words[count+1] + '_' + ''
                        else:
                            arm[instance['id']][2] = ''
                            arm[instance['id']][3] = ''
                            arm[instance['id']][5] = words[count-1] + '_' + ''
                            arm[instance['id']][6] = '' + '_' + ''

                    count += 1

with open("arm.test.txt" , "w") as out:
    for contexts in arm:
        for context in arm[contexts]:
            out.write(str(context)+'\t')
        out.write('\n')   

	

