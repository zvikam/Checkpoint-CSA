## problem
given a pcap file, figure it out.
## solver
the pcap file contains USB traffic of a graphics drawing tablet.
after some investigation, we can find the structure of the data packets, which contain 2D movement data and mouse-like button state. extract all the packets and the coordinates when button is pressed, then gnuplot it.

