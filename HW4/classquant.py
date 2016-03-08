#!/usr/bin/env python3
######################################################################
#This script converts sense IDs to integer values for classification #
#purposes                                                            #
######################################################################

import sys

with open(sys.argv[1], 'r') as infile:
    classes = infile.read().splitlines()
    uniq_classes = set(classes)
    class_dict = {}
    count = 1
    for item in uniq_classes:
        class_dict[item] = count
        count +=1

    outfile = 'numerical.' + str(sys.argv[1])
    with open(outfile, 'w') as out:
        for line in classes:
            out.write(str(class_dict[line]) + '\n')
            print(class_dict[line])
