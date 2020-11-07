## problem
given an mp4 file
## solver
playing the file, we get rapid flahes of black and white. try not to get a seisure.  
create a script
- read the file with opencv
- iterate all frames
- we see uniform (i.e. solid color) with 3 colors: white=[250, 253, 251], grey=[95, 98, 96], black=[0, 0, 0]
- for all non-grey frames, append the pixel value of each frame to the result data
- brute-force the image dimensions using all integer divisors of the data length

