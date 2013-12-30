#! /usr/bin/python

from datetime import timedelta
import pickle
import sys
from os import path


def createTrackFile(filename, row_count):

  f = open(filename, 'r') 

  short_name = path.splitext(filename)[0]

  # read list of lines while ignoring empty lines
  l = []
  for line in f:
    s = line.strip()
    if len(s)>0:
      l.append(s) 

  f.close()
  
  assert( len(l) % row_count == 0)


  tracks = []
  total = timedelta(0)
  for i in range(0,len(l),row_count):
    tracks.append( (l[i],l[i+1],l[i+2],l[i+3]) )
    # TODO: read timedelta from mm:ss representation
    dt = l[i+3].split(':')
    new_delta = timedelta(minutes = int(dt[0]), seconds = int(dt[1]))
    total = total + new_delta
    
    
  #print tracks  
  
  # write info on all tracks in file
  output = open(short_name+'.pkl', 'w')
  pickle.dump(tracks, output)
  output.close()
  
  # create second file with current position of recording
  output = open(short_name+'_counter.pkl', 'w')
  i = 0
  pickle.dump(i, output)
  output.close()
  
    
  print "Found",len(tracks), "tracks in", filename
  print "total duration", str(total)
  
  #return tracks
  
if __name__ == "__main__":
  if len(sys.argv) == 1:
    print 'Usage  ./initTrackInfos.py foo.txt'
    exit()
  
  filename = sys.argv[1]
  createTrackFile(filename,5)

