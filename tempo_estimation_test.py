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
    # print "in_data: ", in_data
    # audio_data = np.fromstring(in_data, dtype=np.int16)
    # print "audio_data: ", audio_data
    # print audio_data[0:50]
    return (in_data, pyaudio.paContinue)

def tempo_comparisson(current_tempo):

    upper_threshold = previuos_tempo + 3
    lower_threshold = previuos_tempo - 3

    if (upper_threshold >= current_tempo) and (lower_threshold <= current_tempo):

        return True
    else:
        return False


def actual_tempo(current_tempo):

    l = len(current_tempo)

    for n in range(l):

        if tempo_comparisson(current_tempo):

            actual_tempo = previuos_tempo
            break

        else:
            actual_tempo = current_tempo[0, 0]

    return actual_tempo

if __name__ == '__main__':

    # print p.get_device_info_by_index(0)['defaultSampleRate']

    RNNbeat = mm.features.beats.RNNBeatProcessor(online=True, nn_files=[BEATS_LSTM[0]])
    tempoEstimation = mm.features.tempo.TempoEstimationProcessor(min_bpm=40, max_bpm=180, fps=100)

    # tempoEstimation = mm.features.onsets.OnsetPeakPickingProcessor(threshold=.05, fps=1, pre_avg=0, post_avg=0, online=True)

    previuos_tempo = 0

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
    CHUNK = np.uint32(RATE*4)
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

    N = 50
    tempo_frame_RNN = np.zeros(N, dtype=np.int16)
    tempo_frame_SpecFlux = np.zeros(N, dtype=np.int16)
    tempo_frame_SuperFlux = np.zeros(N, dtype=np.int16)


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

        spec = mm.audio.spectrogram.Spectrogram(rawData)
        # print spec
        # print "spec.dtype:", spec.dtype
        # print "spec.shape:", spec.shape

        spectralflux = mm.features.onsets.spectral_flux(spec)
        superflux = mm.features.onsets.superflux(spec)
        # print "superflux.shape :\n", sf.shape
        # print "superflux.dtype :\n", sf.dtype

        tempo_SpecFlux = tempoEstimation.process(spectralflux)
        tempo_SuperFlux = tempoEstimation.process(superflux)
        tempo_RNN = tempoEstimation.process(beats) #beats / beats.max() to normalize it, threshold need to be changed too

        t1 = time.clock()

        print "Time needed for Onset and PeakPeaking Calculation:", t1-t0

        print "tempo_SpecFlux: \n", tempo_SpecFlux[0, 0]
        print "tempo_SuperFlux: \n", tempo_SuperFlux[0, 0]
        print "tempo_RNN: \n", tempo_RNN

        tempo_integer_SpecFlux = map(np.int16, tempo_SpecFlux[:, 0])
        tempo_integer_SuperFlux = map(np.int16, tempo_SuperFlux[:, 0])
        tempo_integer_RNN = map(np.int16, tempo_RNN[:, 0])

        if nchunks < tempo_frame_RNN.shape[0]:

            tempo_frame_SpecFlux[nchunks] = tempo_integer_SpecFlux[0]
            tempo_frame_SuperFlux[nchunks] = tempo_integer_SuperFlux[0]
            tempo_frame_RNN[nchunks] = tempo_integer_RNN[0]

        elif nchunks >= tempo_frame_RNN.shape[0]:
            print "******************DONE********************"
        # print "tempo.shape: \n", len(tempo)
        # print "tempo data: \n", tempo[:,0]
        # previuos_tempo = tempo[0,0]

        nchunks += 1

        if cv2.waitKey(1) & 0xFF == ord('q'):
            stream.stop_stream()
            stream.close()
            p.terminate()
            print("* stop recording")
            break

    print "Total no.samples recorded: ", CHUNK*nchunks

    # print "frame: ", np.fromstring(''.join(frames[0:100]), np.int16)

    print "Mean value using Spectral Flux: ", np.mean(tempo_frame_SpecFlux)
    print "STD value using Spectral Flux: ", np.std(tempo_frame_SpecFlux)
    print "Mean value using Super Flux: ", np.mean(tempo_frame_SuperFlux)
    print "STD value using Super Flux: ", np.std(tempo_frame_SuperFlux)
    print "Mean value using RNNBeatProcessor: ", np.mean(tempo_frame_RNN)
    print "STD value using RNNBeatProcessor: ", np.std(tempo_frame_RNN)

    print "Tempo estimation data for Spectral Flux: \n", tempo_frame_SpecFlux
    print "Tempo estimation data for Super Flux: \n", tempo_frame_SuperFlux
    print "Tempo estimation data for RNN: \n", tempo_frame_SpecFlux
        
    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

    cv2.destroyAllWindows()

    # plt.figure()
    # plt.plot(rawData)
    # plt.xlabel("Samples in time")
    # plt.ylabel("Energy")
    # plt.title("Original audio samples")
    #
    # # plt.figure()
    # # plt.imshow(spec[:, :200].T, origin='lower', aspect='auto')
    # # plt.title("Spectogram")
    #
    # plt.figure()
    # plt.plot(spectralflux / spectralflux.max())
    # plt.xlabel("Time (4sec)")
    # plt.ylabel("Normalize energy")
    # plt.title("Detection function by SpectralFlux")
    #
    # plt.figure()
    # plt.plot(superflux / superflux.max())
    # plt.xlabel("Time (4sec)")
    # plt.ylabel("Normalize energy")
    # plt.title("Detection function by SuperFlux")
    #
    # plt.figure()
    # # plt.plot(beats)
    # plt.plot(beats / beats.max())
    # plt.xlabel("Time (4sec)")
    # plt.ylabel("Normalize energy")
    # plt.title("Detection function by RNNprocessor")

    plt.figure()
    plt.plot(tempo_frame_SpecFlux)
    plt.xlabel("Number of chunks")
    plt.ylabel("Tempo calculated")
    plt.title("Tempo Estimation using Spectral Flux")
    plt.ylim((60, 180))

    plt.figure()
    plt.plot(tempo_frame_SuperFlux)
    plt.xlabel("Number of chunks")
    plt.ylabel("Tempo calculated")
    plt.title("Tempo Estimation using Super Flux")
    plt.ylim((60, 180))

    plt.figure()
    plt.plot(tempo_frame_RNN)
    plt.xlabel("Number of chunks")
    plt.ylabel("Tempo calculated")
    plt.title("Tempo Estimation using RNN")
    plt.ylim((60, 180))

    plt.show()
