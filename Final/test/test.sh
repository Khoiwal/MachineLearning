for counter in 1 3 5 7 9 11 13 15
do
	for distance in `cat dist.txt`
	do
		for weights in {0..4}
		do
				timbl -f "train.test.tsv" -t "test.test.tsv" 	-k $counter -m $distance -w $weights > $counter"_"$distance"_"$weights"_output.out"; 
				#tail -5  $counter"_accent_output.out" > $counter"_accent_output.tsv";	
		done;
	done;
done;            

grep "overall accuracy:" *_output.out > overall_accuracies_3words.tsv;

grep "accent" overall_accuracies_3words.tsv > overall_accuracies_accent.tsv;


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
					timbl -f "train.test.tsv" -t "test.test.tsv" 	-a $algo  -w $weights	-d $w_n_f_d	--Treeorder=$TO	> $algo"_""_"$weights"_"$w_n_f_d"_"$TO"test_output.out";	

				done;
			done;
		done;
	done;	
done;	
