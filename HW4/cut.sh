for f in arm.test.txt interest.test.txt difficulty.test.txt 
do
 echo "Processing $f"
 # cut features class
 cut -f 1-7 $f > features.$f
 cut -f 8 $f > classes.$f
done
