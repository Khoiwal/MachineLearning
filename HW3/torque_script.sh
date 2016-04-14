#!/bin/bash 

PBS -k o 
PBS -l nodes=2:ppn=6,walltime=24:00:00
PBS -M zbranson@indiana.edu
PBS -m abe 
PBS -N supervised_words 
#PBS -j oe 

#this should be a call to timbl
#mpiexec -np 12 -machinefile $PBS_NODEFILE ~/bin/binaryname
