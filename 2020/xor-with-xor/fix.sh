rename 's/([0-9]).([0-9]).([0-9])\.dat/$1$2$3.dat/s' *.dat
for i in $(seq 0 999); do cat $i.dat >> all.gz; done
