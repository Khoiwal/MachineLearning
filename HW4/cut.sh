for f in arm.newtrain.txt interest.newtrain.txt difficulty.newtrain.txt 
do
 echo "Processing $f"
 # cut features and class
 # note: update ranges after new context feature vector is added
 cut -f 1-7 $f > $f.features.txt
 cut -f 8 $f > $f.classes.txt
done
