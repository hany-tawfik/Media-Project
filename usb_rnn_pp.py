''' This code tries to calculate the peak picking using 
tempoEstimation = mm.features.tempo.TempoEstimationProcessor(min_bpm=40, max_bpm=240, fps=100)'''

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
import argparse

def callback_audio(in_data, frame_count, time_info, status):
    stream_queue.put(in_data)
    return (in_data, pyaudio.paContinue)

if __name__ == '__main__':

    # print p.get_device_info_by_index(0)['defaultSampleRate']

    RNNbeat = mm.features.beats.RNNBeatProcessor(online=True, nn_files=[BEATS_LSTM[0]])
    tempoEstimation = mm.features.tempo.TempoEstimationProcessor(min_bpm=40, max_bpm=180, fps=100)
    # tempoEstimation = mm.features.onsets.OnsetPeakPickingProcessor(threshold=.05, fps=1, pre_avg=0, post_avg=0, online=True)

    p = pyaudio.PyAudio()
    stream_queue = Queue.Queue()

    '''
    #Problems detecting the tempo with this setup, chunk to small to detect tempo
    RATE = 8000
    CHUNK = np.uint32(RATE*20) #20480
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    '''

    RATE = 44100
    CHUNK = np.uint32(RATE*2.5)
    FORMAT = pyaudio.paInt16
    CHANNELS = 1

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

        t0 = time.clock()

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

        tempo = tempoEstimation.process(beats) #beats / beats.max() to normalize it, threshold need to be changed too

        t1 = time.clock()

        print "Time needed for Onset and PeakPeaking Calculation:", t1-t0

        print "tempo: \n", tempo

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
    plt.plot(beats)
    # plt.plot(beats / beats.max())
    plt.title("Beats by RNN")

    plt.show()
