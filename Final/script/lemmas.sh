#!/bin/bash 

#PBS -k o 
#PBS -l nodes=2:ppn=6,walltime=24:00:00
#PBS -M zbranson@indiana.edu
#PBS -m abe 
#PBS -N supervised_lemmas 
#PBS -j oe 

cd /N/u/zbranson/Karst/665/final/forKarst;
module load timbl/6.4.2;

#base case
#don't forget to merge lemmass onto features									
timbl -f accent.n.lemmas.train.tsv -t accent.n.lemmas.test.tsv 	> accent_output.tsv; 		 	
timbl -f citi.v.lemmas.train.tsv -t citi.v.lemmas.test.tsv 	> citi_output.tsv;
timbl -f delfin.n.lemmas.train.tsv -t delfin.n.lemmas.test.tsv 	> delfin_output.tsv;
timbl -f oficial.a.lemmas.train.tsv -t oficial.a.lemmas.test.tsv 	> oficial_output.tsv;
timbl -f val.n.lemmas.train.tsv -t val.n.lemmas.test.tsv 		> val_output.tsv;

#case 1 - k-NN with different distances & feature weighing schemes for varying k values

rm -rf *.out;

for counter in 1 3 5 7 9 11 13 15
do
	for distance in `cat dist.txt`
	do
		for weights in {0..4}
		do
				timbl -f "accent.n.lemmas.train.tsv" -t "accent.n.lemmas.test.tsv" 	-k $counter -m $distance -w $weights > $counter"_"$distance"_"$weights"_accent.out"; 
				#tail -5  $counter"_accent_output.out" > $counter"_accent_output.tsv";	
	 	
				timbl -f "citi.v.lemmas.train.tsv" -t "citi.v.lemmas.test.tsv " 	-k $counter -m $distance  -w $weights  > $counter"_"$distance"_"$weights"_citi.out";  		
				#tail -5  $counter"_citi_output.out" > $counter"_citi_output.tsv";

				timbl -f "delfin.n.lemmas.train.tsv" -t "delfin.n.lemmas.test.tsv" 	-k $counter -m $distance   -w $weights > $counter"_"$distance"_"$weights"_delfin.out";   
				#tail -5  $counter"_delfin_output.out" > $counter"_delfin_output.tsv";

				timbl -f "oficial.a.lemmas.train.tsv" -t "oficial.a.lemmas.test.tsv" 	-k $counter -m $distance   -w $weights > $counter"_"$distance"_"$weights"_oficial.out";   
				#tail -5  $counter"_oficial_output.out" > $counter"_oficial_output.tsv";

				timbl -f "val.n.lemmas.train.tsv" -t "val.n.lemmas.test.tsv" 		-k $counter -m $distance   -w $weights > $counter"_"$distance"_"$weights"_val.out";   
				#tail -5  $counter"_val_output.out" > $counter"_val_output.tsv";

		done;
	done;
done;            

grep "overall accuracy:" *_output.out > overall_accuracies_5lemmass.tsv;

grep "accent" overall_accuracies_3lemmas.tsv > overall_accuracies_accent.tsv;
grep "citi" overall_accuracies_3lemmas.tsv > overall_accuracies_citi.tsv;
grep "delfin" overall_accuracies_3lemmas.tsv > overall_accuracies_delfin.tsv;
grep "oficial" overall_accuracies_3lemmas.tsv > overall_accuracies_oficial.tsv;
grep "val" overall_accuracies_3lemmas.tsv > overall_accuracies_val.tsv;

#manual one in other

for algo in {0..4}
do
	for q_val in {1..15}
	do
		for weights in {0..4}
		do
			for w_n_f_d in `cat wt_nghbr_func_dist.txt`
			do
				for TO in `cat Treeorder.txt`
				do
					timbl -f "accent.n.lemmas.train.tsv" -t "accent.n.lemmas.test.tsv" 	-a $algo  -w $weights	-d $w_n_f_d	--Treeorder=$TO	> $algo"_""_"$weights"_"$w_n_f_d"_"$TO"_accent_output.out";	
					timbl -f "citi.v.lemmas.train.tsv" -t "citi.v.lemmas.test.tsv" 		-a $algo  -w $weights	-d $w_n_f_d	--Treeorder=$TO	> $algo"_""_"$weights"_"$w_n_f_d"_"$TO"_citi_output.out";	
					timbl -f "delfin.n.lemmas.train.tsv" -t "delfin.n.lemmas.test.tsv" 	-a $algo  -w $weights	-d $w_n_f_d	--Treeorder=$TO	> $algo"_""_"$weights"_"$w_n_f_d"_"$TO"_delfin_output.out";	
					timbl -f "oficial.a.lemmas.train.tsv" -t "oficial.a.lemmas.test.tsv" 	-a $algo  -w $weights	-d $w_n_f_d	--Treeorder=$TO	> $algo"_""_"$weights"_"$w_n_f_d"_"$TO"_oficial_output.out";	
					timbl -f "val.n.lemmas.train.tsv" -t "val.n.lemmas.test.tsv" 	-a $algo  -w $weights	-d $w_n_f_d	--Treeorder=$TO	> $algo"_""_"$weights"_"$w_n_f_d"_"$TO"_val_output.out";	
				done;
			done;
		done;
	done;	
done;	
	
	
	
	
	
	
	
