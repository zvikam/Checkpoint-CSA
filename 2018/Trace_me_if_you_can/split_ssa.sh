#awk 'BEGIN{f="header.ssa"}{if ($0 ~ /^func /) {f=substr($0,6,match($0,/\(/)-6)}}!/^#/{gsub(/\t/, "    "); print substr($0,1,56)>>f}' ../ssa.ssa
awk 'BEGIN{f="header.ssa"}{if ($0 ~ /^func /) {f=substr($0,6,match($0,/\(/)-6)}}!/^#/{S=substr($0,1,56); sub(/[ ]+$/,"",S); print S>>f}' ../ssa.ssa

#for ff in `ls -1 ssa2 | grep -v 'header\|init'`; do for ii in `ls -1 ssa/main.${ff}.*.ssa`; do echo kompare ${ii} ssa2/${ff} \&\> /dev/null; done; done

