#! /usr/bin/python


import wave, numpy, sys,pickle, os
import alsaaudio
from pydub import AudioSegment
from math import floor
from datetime import timedelta

frameRate = 44100
channelCnt = 2



def start_file(filename):
  w = wave.open(filename, 'w')
  w.setnchannels(channelCnt)
  w.setsampwidth(2)
  w.setframerate(frameRate) 
  return w


#from initTrackInfos.py import *
#tracks = loadTrackInfos("tarja.txt",5)

if __name__ == "__main__":
  if len(sys.argv) == 1:
    print 'Usage  ./record.py foo.pkl'
    print 'to start recording or'
    print './record.py foo.pkl test'
    print 'to print next track from playlist to record and exit'
    exit()
    
  
  filename = sys.argv[1]
  short_name = os.path.splitext(filename)[0]  
    
  infile = open(short_name+'.pkl', 'r')
  tracks = pickle.load(infile)
  infile.close()
  
  # read current position of recording (e.g. after break)
  infile = open(short_name+'_counter.pkl', 'r')
  trackNumber = pickle.load(infile)
  infile.close()  

  print "Reading file Nr.",trackNumber
  
  if len(sys.argv) == 3: # and sys.argv[2] == "test":
    print 'please start playlist at:', tracks[trackNumber][0] ,"(by",  tracks[trackNumber][1],")"
    print 'exiting'
    exit() 


  # location of intermediate file
  current_name = 'current_recording.wav'
  
  inp = alsaaudio.PCM(alsaaudio.PCM_CAPTURE, alsaaudio.PCM_NORMAL)
  inp.setchannels(channelCnt)
  inp.setrate(frameRate)
  inp.setformat(alsaaudio.PCM_FORMAT_S16_LE)
  inp.setperiodsize(1024)

  store_folder = os.path.expanduser('~')+'/Music'
  
  current_name = 'current_recording.wav'
  
  
  w = start_file(current_name)
  
  is_silent = False
  
  silence_threshold = 50 # minimal volume accepted as silence
  min_silence_duration = 0.7 # minimal duration of silence between songs
  silence_duration = 0   # duration of last silent period
  
  
  length = 0
  
  while True:
    l, data = inp.read()
    a = numpy.fromstring(data, dtype='int16')
    sound = numpy.abs(a).mean()
  
    # read track info and length from pickled list
    track_name = tracks[trackNumber][0]
    artist = tracks[trackNumber][1]
    album = tracks[trackNumber][2]
    dt  = tracks[trackNumber][3].split(':')
    duration = timedelta(minutes = int(dt[0]), seconds = int(dt[1]))
    
    # create folder path from artist and album
    folder = store_folder+'/'+artist.replace(" ","_")+'/'+album.replace(" ","_")
      
    # ensure that folder (artist/album) exists
    if not os.path.exists(folder):
      print "creating"
      os.makedirs(folder)
    
    # append new sound to intermediate file
    w.writeframes(data)
    
    # get length of current recording
    length = round(w.tell()*1.0/frameRate,2)
    
    
    print "Recording: %s (%s) %.2f / %i" % (track_name, artist, length, duration.total_seconds()),"              \r",
    
    # register start of silent phase or update duration of silent phase
    if sound < silence_threshold:
      if not is_silent:
        is_silent = True
        
        start = w.tell()*1.0/frameRate
      else:
        now = w.tell()*1.0/frameRate 
        silence_duration = now-start
        print 'silence', round(silence_duration,2),"                   \r",
    else:
      is_silent = False
      
    # react to long silent phase (probably end of track)
    if is_silent and silence_duration >= min_silence_duration:
    
      print 'Detected Pause at time:',length,'s'
      
      # ignore silent phases inside of track
      if (abs(duration.total_seconds()-length) > 10):
        print "Pause ignored during Track"
        continue
  
      # close intermediate wav file
      w.close()
      
      # create file name for mp3
      new_file = folder+'/'+track_name.replace(" ","_").replace("/","")+'.mp3'
  
      print 'Converting:', new_file
      song = AudioSegment.from_wav(current_name)        
      no_silence = song[:-floor(silence_duration*1000)] # remove last silent seconds
      # export to mp3 with right id3 tags (could be done in different thread)
      no_silence.export(new_file, format="mp3", tags={'title':track_name, 'artist': artist, 'album': album}) 
      print 'Saved.'    
      trackNumber += 1
      
      if trackNumber >= len(tracks):
        print "recorded all files from", filename
        exit()
      
      # write new next song into counter-file
      output = open(short_name+'_counter.pkl', 'w')
      pickle.dump(trackNumber, output)
      output.close()
        
      # open new temporary file
      silence_duration = 0
      w = start_file(current_name)
      
      
      
