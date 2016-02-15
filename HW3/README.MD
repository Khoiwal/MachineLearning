for classifier need: w+3, w-3 (in various combinations - refer to assignment
handout) sense-id
the words in question are between xml brackets <head> </head> in the train
data

use tsv for timbl input: w-2 \t w-1 \t w+1 \t w+2 \t w-2_w-1 \t w-1_w+1 \t 
w+1_w+2 \t sense-id

test data key format: arm.n /t id /t correct sense label
