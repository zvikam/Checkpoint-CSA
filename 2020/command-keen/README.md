## problem
given modified source code of commander keen - keen dreams and a set of movement recordings.
## solver
diff the code from the "official" code.  
note that the level hints have changed and contain letters.  
we need to replay each recording in order to see which level keen _walks_ to and note the hints.  
  
setup a DOSBOX instance with Borland C++ 3.1 and build the game from source.  
the game contains a _demo_Playback_ feature, so we adjust the code to read our recording format.  
we also patch the game's initial state so that all levels are marked as _solved_ which allows us to freely move around in the main map.  
then write a batch file to _replay_ the recordings in order.  

