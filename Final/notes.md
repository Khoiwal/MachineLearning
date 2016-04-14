semisupervised approach:

timbl will output distances for unlabled calssified examples
take the 10 smallest distances from unlabled set
add those with their senseids to the training data
retrain the model
run on test for results
rinse repeat 
