#!/bin/bash
tshark -r davinci.pcap -T fields -e usb.capdata -Y usb.capdata | awk -F: 'function comp(v){if(v>127)v-=256;return v}{x+=comp(strtonum("0x"$3));y+=comp(strtonum("0x"$4))}$2=="81"{print x,-1*y}' > click_coordinates.txt
gnuplot -e "plot 'click_coordinates.txt'; pause -1"
