from mido import MidiFile
import os,sys
pth = "D:\study\major project\scl\src"
os.chdir(pth)
c=0
print(os.path.dirname(sys.argv[0]))
#feels = MidiFile('Dream On.mid')
feels = MidiFile('Have a Nice Day.mid')
for i, track in enumerate(feels.tracks):
    #print('Track() : ()'.format(i, track.name))
    for msg in track:
    	c+=1
        #print('{}'.format(msg))
print(c)