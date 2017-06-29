import pyaudio
import wave
import array
import numpy as np
import madmom as mm
import Queue
import struct
import cv2


p = pyaudio.PyAudio()

print p.get_device_info_by_index(0)['defaultSampleRate']

CHUNK = 2048
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 8000
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "output.wav"

stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

stream.start_stream()

print("* recording")
# print np.int(RATE / CHUNK)
# print "ratio: ", np.round(RATE / CHUNK * RECORD_SECONDS)

frames = []
cv2.imshow('+++recording+++',0)


data = array.array('h')
while True:
    samples = stream.read(CHUNK)
    frames.append(samples)
    data.fromstring(samples)
    decoded = np.array(data, dtype=np.uint16)
    print "decoded shape :\n", decoded.shape
    # print "decoded :\n", decoded

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


stream.stop_stream()
stream.close()
p.terminate()
wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(p.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(frames))
wf.close()
cv2.destroyAllWindows()

