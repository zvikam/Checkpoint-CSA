#!/bin/bash

V_VALUES=(+ -)

for py in $(seq 0 9); do
    for px in $(seq 0 6); do
        for vy in "${!V_VALUES[@]}"; do
            for vx in "${!V_VALUES[@]}"; do
                ./pinball.elf transform msg.enc ${py}_${px}_${vy}_${vx}.out ${py} ${px} ${V_VALUES[vy]} ${V_VALUES[vx]};
            done;
        done;
    done;
done

file *.out | grep " ASCII text" | awk -F ':' '{print $1}' | while read rr; do echo ${rr}; cat ${rr}; echo ""; done
