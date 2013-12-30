SoundRecorder
=============

Python Scripts to record music

Useful scripts to record music from the audio output (headphones). 
Can be used to record streamed music. Automatic track seperation
by detecting silence at end of track. 

Can be used e.g. to record a Deezer playlist.
- create a Deezer Playlist
- Apply a copy&paste on the website and save the result in a file (foo.txt)
- remove the first 30 ( or so) lines, until you only have lines as 

Title
Artist
Album
Duration
time since added to playlist

e.g.

False Awakening Suite
	
Dream Theater
	
Dream Theater
	
02:42
	
3 hours ago
		
	
	
	
The Enemy Inside
	
Dream Theater
	
Dream Theater
	
06:17
	
3 hours ago
		
	
	
- apply ./initTrackInfos.py foo.txt
   this will create foo.pkl and foo_counter.pkl
-> foo.pkl consists a list of the tracks and foo_counter.pkl contains the position of the currently recorded file
   in the list.
   
- to record the playlist, start ./record.py foo.pkl  and at the moment start the playlist. Don't change the volume but
just enjoy the music (or go for a walk). 
- the sound is first stored in current_recording.wav and exported to an mp3 after a moment of silence at the end of
the track was recogized. The mp3 (with id3 Tags) is then copied into the ~/Music/Artist/Album Folder (which is created
if it didn't exist yet)

- If you have to stop the recording, just call 
> ./record.py foo.pkl test
to see at which point you have to start the playlist again

> Reading file Nr. 22
> please start playlist at: The Best Of Times (by Dream Theater )

So just call ./record foo.pkl again and start the playlist at this position. 


Requirements:

Currently only tested with Ubuntu 12.10

