#!/bin/bash 

#PBS -k o 
#PBS -l nodes=2:ppn=6,walltime=24:00:00
#PBS -M zbranson@indiana.edu
#PBS -m abe 
#PBS -N supervised_words 
#PBS -j oe 

cd /N/u/zbranson/Karst/665/final/words;
module load timbl/6.4.2;

#base case								
timbl -f accent.n.words.train.tsv -t accent.n.words.test.tsv 	> accent_output.txt; 		 	
timbl -f citi.v.words.train.tsv -t citi.v.words.test.tsv 	> citi_output.txt;
timbl -f delfin.n.words.train.tsv -t delfin.n.words.test.tsv 	> delfin_output.txt;
timbl -f oficial.a.words.train.tsv -t oficial.a.words.test.tsv 	> oficial_output.txt;
timbl -f val.n.words.train.tsv -t val.n.words.test.tsv 		> val_output.txt;

#case 1 - k-NN with different distances & feature weighing schemes for varying k values

for counter in 1 3 5 7 9 11 13 15
do
	for distance in `cat dist.txt`
	do
		for weights in {0..4}
		do
				timbl -f "accent.n.words.train.tsv" -t "accent.n.words.test.tsv" 	-k $counter -m $distance -w $weights > $counter"_"$distance"_"$weights"_accent_output.out"; 
				#tail -5  $counter"_accent_output.out" > $counter"_accent_output.tsv";	
	 	
				timbl -f "citi.v.words.train.tsv" -t "citi.v.words.test.tsv" 		-k $counter -m $distance  -w $weights  > $counter"_"$distance"_"$weights"_citi_output.out";  		
				#tail -5  $counter"_citi_output.out" > $counter"_citi_output.tsv";

				timbl -f "delfin.n.words.train.tsv" -t "delfin.n.words.test.tsv" 	-k $counter -m $distance   -w $weights > $counter"_"$distance"_"$weights"_delfin_output.out";   
				#tail -5  $counter"_delfin_output.out" > $counter"_delfin_output.tsv";

				timbl -f "oficial.a.words.train.tsv" -t "oficial.a.words.test.tsv" 	-k $counter -m $distance   -w $weights > $counter"_"$distance"_"$weights"_oficial_output.out";   
				#tail -5  $counter"_oficial_output.out" > $counter"_oficial_output.tsv";

				timbl -f "val.n.words.train.tsv" -t "val.n.words.test.tsv" 		-k $counter -m $distance   -w $weights > $counter"_"$distance"_"$weights"_val_output.out";   
				#tail -5  $counter"_val_output.out" > $counter"_val_output.tsv";

		done;
	done;
done;            


#manual one in other

for algo in {0..4}
do
	for q_val in {1..15}
	do
		for weights in {0..4}
		do
			for w_n_f_d in `cat wt_nghbr_func_dist.txt`
			do
                                COUNTER = 0
				for TO in `cat Treeorder.txt`
				do
				COUNTER=$((COUNTER + 1))
					timbl -f "accent.n.words.train.tsv" -t "accent.n.words.test.tsv" 	-a $algo  -w $weights	-d $w_n_f_d	--Treeorder=$TO	> $algo"_""_"$weights"_"$w_n_f_d"_"$COUNTER"_accent_output.out";	
					timbl -f "citi.v.words.train.tsv" -t "citi.v.words.test.tsv" 		-a $algo  -w $weights	-d $w_n_f_d	--Treeorder=$TO	> $algo"_""_"$weights"_"$w_n_f_d"_"$COUNTER"_citi_output.out";	
					timbl -f "delfin.n.words.train.tsv" -t "delfin.n.words.test.tsv" 	-a $algo  -w $weights	-d $w_n_f_d	--Treeorder=$TO	> $algo"_""_"$weights"_"$w_n_f_d"_"$COUNTER"_delfin_output.out";	
					timbl -f "oficial.a.words.train.tsv" -t "oficial.a.words.test.tsv" 	-a $algo  -w $weights	-d $w_n_f_d	--Treeorder=$TO	> $algo"_""_"$weights"_"$w_n_f_d"_"$COUNTER"_oficial_output.out";	
					timbl -f "val.n.words.train.tsv" -t "val.n.words.test.tsv" 		-a $algo  -w $weights	-d $w_n_f_d	--Treeorder=$TO	> $algo"_""_"$weights"_"$w_n_f_d"_"$COUNTER"_val_output.out";	
				done;
			done;
		done;
	done;	
done;	
	
grep "overall accuracy:" *_output.out > overall_accuracies_3words.txt;

grep "accent" overall_accuracies_3words.txt > overall_accuracies_accent.txt;
grep "citi" overall_accuracies_3words.txt > overall_accuracies_citi.txt;
grep "delfin" overall_accuracies_3words.txt > overall_accuracies_delfin.txt;
grep "oficial" overall_accuracies_3words.txt > overall_accuracies_oficial.txt;
grep "val" overall_accuracies_3words.txt > overall_accuracies_val.txt;

rm -rf *.out;
	
	
	
	
	
	
