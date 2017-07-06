import pyaudio
import wave
import array
import numpy as np
import madmom as mm
import cv2
import matplotlib.pyplot as plt
import time
import Queue
import struct
from madmom.models import BEATS_LSTM

def callback_audio(in_data, frame_count, time_info, status):
    stream_queue.put(in_data)
    return (in_data, pyaudio.paContinue)

if __name__ == '__main__':

    # print p.get_device_info_by_index(0)['defaultSampleRate']

    ticks = time.time()
    RNNbeat = mm.features.beats.RNNBeatProcessor(online=True, nn_files=[BEATS_LSTM[0]])
    p = pyaudio.PyAudio()
    stream_queue = Queue.Queue()

    CHUNK = 2048
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 8000
    RECORD_SECONDS = 5
    WAVE_OUTPUT_FILENAME = "output_02.wav"

    stream = p.open(format=FORMAT,
                           channels=CHANNELS,
                           rate=RATE,
                           input=True,
                           frames_per_buffer=CHUNK,
                           stream_callback=callback_audio)

    nchunks = 0
    frames = []
    # data = array.array('h')

    print("* recording")
    cv2.imshow('+++recording+++', 0)

    stream.start_stream()

    while True:
        samples = stream_queue.get()

        rawData = np.int16(struct.unpack('h' * CHUNK, samples))
        # print "rawData: ", rawData
        # print "rawData.shape: ", rawData.shape
        # print "rawData.dtype: ", rawData.dtype

        frames.append(samples)
        # data.fromstring(samples)
        # # print "data: ", data
        # decoded = np.array(data, dtype=np.int16)
        # print "decoded.shape: ", decoded.shape

        ticks = time.time()
        print "Tick before Onset:", ticks

        beats = RNNbeat(rawData)
        # print "beats.shape :\n", beats.shape
        # print "beats.dtype :\n", beats.dtype

        # spec = mm.audio.spectrogram.Spectrogram(rawData)
        # print spec
        # print "spec.dtype:", spec.dtype
        # print "spec.shape:", spec.shape

        # sf = mm.features.onsets.superflux(spec)
        # print "superflux.shape :\n", sf.shape
        # print "superflux.dtype :\n", sf.dtype

        ticks = time.time()
        print "Tick after Onset:", ticks

        nchunks += 1

        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("* stop recording")
            break

    print "Total no.samples recorded: ", CHUNK*nchunks

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

    plt.figure()
    plt.plot(rawData)
    plt.title("rawData")

    # plt.figure()
    # plt.imshow(spec[:, :200].T, origin='lower', aspect='auto')
    # plt.title("Spectogram")
    #
    # plt.figure()
    # plt.plot(sf / sf.max())
    # plt.title("Super flux")

    plt.figure()
    plt.plot(beats / beats.max())
    plt.title("Beats by RNN")

    plt.show()

