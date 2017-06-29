import pyaudio
import wave
import numpy as np
import Queue
import struct


def callback_in_1(in_data, frame_count, time_info, status):
    stream_queue_1.put(in_data)
    return (in_data, pyaudio.paContinue)

if __name__ == '__main__':

    CHUNK = 2048
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 8000
    RECORD_SECONDS = 10
    WAVE_OUTPUT_FILENAME = "output.wav" 

    p_in_1 = pyaudio.PyAudio()

    stream_queue_1 = Queue.Queue()

    stream_1 = p_in_1.open(format=FORMAT,
                           channels=CHANNELS,
                           rate=RATE,
                           input=True,
                           frames_per_buffer=CHUNK,
                           stream_callback=callback_in_1)

    stream_1.start_stream()
    frames = []

    # Loop for the blocks:r
    # for i in range(0, 100):
    print("* recording")

    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data_1 = stream_queue_1.get()

        shorts_1 = (struct.unpack('h' * CHUNK, data_1))

        samples_L = np.array(list(shorts_1), dtype=np.uint16)

        frames.append(data_1)

        # print "iterator : \n", i
        # print "samples_L.shape : \n", samples_L.shape
        # print "samples_L : \n", samples_L
        # print "frames.shape : \n", frames.shape

    print("* STOP recording")

    stream_1.stop_stream()
    stream_1.close()
    p_in_1.terminate()

    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p_in_1.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()
