import pyaudio
import wave
import numpy as np
#import madmom as mm


CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "output.wav"

p = pyaudio.PyAudio()


stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

print("* recording")

frames = []

for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    frames.append(data)
    decoded = np.fromstring(data, 'Float32');
    #mad = mm.audio.filters.FilterBank((decoded, 512))
    #x =mad 
    print "iterator :\n", i                            
    print "decoded shape :\n", decoded.shape
    print "decoded :\n", decoded
    

print("* done recording")

stream.stop_stream()
stream.close()
p.terminate()

wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(p.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(frames))
wf.close()



'''

import pyaudio
import struct
import matplotlib.pyplot as plt
import numpy

FORMAT = pyaudio.paFloat32
SAMPLEFREQ = 44100
FRAMESIZE = 1024
NOFFRAMES = 220
p = pyaudio.PyAudio()
print('running')

stream = p.open(format=FORMAT,channels=1,rate=SAMPLEFREQ,input=True,frames_per_buffer=FRAMESIZE)
data = stream.read(NOFFRAMES*FRAMESIZE)
decoded = numpy.fromstring(data, 'Float32');

stream.stop_stream()
stream.close()
p.terminate()
print('done')
plt.plot(decoded)
plt.show()

'''
