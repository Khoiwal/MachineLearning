#!/usr/bin/env python3
######################################################################
#This script converts sense IDs to integer values for classification #
#purposes                                                            #
######################################################################

files = [['arm.n.class.test.txt','arm.n.class.train.txt'],['interest.n.class.test.txt','interest.n.class.train.txt'],['difficulty.n.class.test.txt','difficulty.n.class.train.txt']]

for pair in files:
    test = pair[0]
    train = pair[1]
    test_classes = []
    train_classes = [] 
    
    with open(test, 'r') as testfile:
        test_classes = testfile.read().splitlines()

    with open(train, 'r') as trainfile:
        train_classes = trainfile.read().splitlines()  

    uniq_classes = set(test_classes+train_classes)
    class_dict = {}
    count = 1
    for item in uniq_classes:
        class_dict[item] = count
        count +=1
    test_out = 'num.' + pair[0]
    train_out = 'num.' + pair[1]
    with open(test_out, 'w') as teout:
        for line in test_classes:
            teout.write(str(class_dict[line]) + '\n')
            print(class_dict[line])
    with open(train_out, 'w') as trout:
        for line in train_classes:
            trout.write(str(class_dict[line]) + '\n')
            print(class_dict[line])

