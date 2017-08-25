from madmom.models import BEATS_LSTM
import madmom as mm
import midi_chords as miChords
import mido
import numpy as np
import pyaudio
import Queue
import struct
import threading
import time
import wave


def setup_chords(note_set):

    if Stop_loop.note != note_set:
        return True
    else:
        return False


def update_tempo(new_tempo):

    new_clock = 60. / ((new_tempo + OFFSET) * PPQ)
    new_clock = np.float16(new_clock)
    return new_clock


def stop_all_threads():

    global stop_key
    stop_key = True


def callback_audio(in_data, frame_count, time_info, status):

    # stream_queue.put(in_data)

    # global rawData, clock_interval, tempoMessage
    global callback_frame, callback_counter, callback_current_samples

    if stop_key == False:

        # print "new audio chunk"
        int_data = np.fromstring(in_data, dtype=np.int16)
        callback_frame.append(int_data)
        frames.append(in_data)
        callback_counter += 1

        # 512 chunksize * 455 = 4sec chunk size
        if callback_counter >= 455:

            print "4sec audio chunk completed", callback_counter
            callback_current_samples = callback_frame
            callback_counter = 0
            callback_frame = []
            tempo_detection = threading.Thread(target=tempo_detection_thread)
            tempo_detection.start()


        # rawData = np.fromstring(in_data, dtype=np.int16)
        # beats = RNNbeat(rawData)
        # tempo = tempoEstimation.process(beats)
        # tempo_integer = map(np.int16, tempo[:, 0])
        # clock_interval = update_tempo(tempo_integer[0])
        # tempoMessage = mido.Message('clock', time=clock_interval)
        # print "new tempo: ", tempo_integer[0]
        # tempo_detection = threading.Thread(target=tempo_detection_thread)
        # tempo_detection.start()
        # frames.append(in_data)

    # else:
    #
    #     stream.stop_stream()
    #     stream.close()
    #     p.terminate()
    #     wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    #     wf.setnchannels(CHANNELS)
    #     wf.setsampwidth(p.get_sample_size(FORMAT))
    #     wf.setframerate(RATE)
    #     wf.writeframes(b''.join(frames))
    #     wf.close()
    #
    #     print "Closed audio channels and created wav file"

    return in_data, pyaudio.paContinue


def tempo_detection_thread():

    print "tempo_detection_thread"
    global rawData, clock_interval, callback_current_samples
    rawData = callback_current_samples
    # t0 = time.clock()
    beats = RNNbeat(rawData)
    tempo = tempoEstimation.process(beats)
    tempo_integer = map(np.uint8, tempo[:, 0])
    clock_interval = update_tempo(tempo_integer[0])
    print "new tempo: ", tempo_integer
    # t1 = time.clock()
    # print "Time needed for Onset and PeakPeaking Calculation:", t1 - t0


def send_tempo_thread():

    # global t
    outport.send(tempoMessage)

    if stop_key == False:

        t = threading.Timer(clock_interval, send_tempo_thread)
        t.start()

    else:
        print "stop timer thread"


def midi_msg_handler_thread():

    for msg in inport:

        # print "msg.note inside of thread: ", msg.note

        if msg.note == Stop_loop.note:  # Note C6 (72) closes the code.
            stop_all_threads()
            inport.close()
            inport2.close()
            outport.close()
            # t.cancel()
            # t.finished
            print "closing midi_msg_handler thread"
            break
        else:
            miChords.Send_Chord(msg)


if __name__ == "__main__":

    '''MIDI I/O PORTS SETUP'''
    inputs = mido.get_input_names()
    korg = inputs[0].encode('ascii')
    midi_start25 = inputs[1].encode('ascii')
    inport = mido.open_input(midi_start25)
    inport2 = mido.open_input(korg)
    outport = mido.open_output(korg)

    '''MIDI EXTERNAL CLOCK CALCULATION'''
    DEFAULT_BPM = 120
    OFFSET = 2
    PPQ = 24  # Pulse per quarter note
    clock_interval = 60. / ((DEFAULT_BPM + OFFSET) * PPQ)
    clock_interval = np.float16(clock_interval)
    tempoMessage = mido.Message('clock', time=clock_interval)

    '''THREADING DEFINITIONS'''
    midi_thread = threading.Thread(target=midi_msg_handler_thread)
    # t = threading.Timer(clock_interval, send_tempo_thread)

    '''OBJECT DEFINITIONS'''
    RNNbeat = mm.features.beats.RNNBeatProcessor(online=True, nn_files=[BEATS_LSTM[0]])
    tempoEstimation = mm.features.tempo.TempoEstimationProcessor(min_bpm=40, max_bpm=180, fps=100)
    p = pyaudio.PyAudio()
    # stream_queue = Queue.Queue()

    '''AUDIO VARIABLES DEFINITION'''
    SECONDS = 4
    RATE = 44100
    # CHUNK = np.uint32(RATE*SECONDS)
    CHUNK = 512
    FORMAT = pyaudio.paInt16
    CHANNELS = 1

    stream = p.open(format=FORMAT,
                           channels=CHANNELS,
                           rate=RATE,
                           input=True,
                           frames_per_buffer=CHUNK,
                           stream_callback=callback_audio)

    WAVE_OUTPUT_FILENAME = "frames_recorded.wav"
    frames = []
    rawData = 0

    '''Audio callback global variables'''
    callback_frame = []
    callback_counter = 0
    callback_current_samples = 0

    '''MIDI DATA SETUP'''
    print "Please press a key for choosing a music scale"
    stop_key = False
    Stop_loop = mido.Message('note_on', note=72)
    note = inport.receive()
    Tonic = note.copy()

    while True:
        if setup_chords(Tonic.note):
            break
        note = inport.receive()
        Tonic = note.copy()

    miChords.Set_Tonic_Scale(Tonic.note)
    miChords.update_chords()

    '''START OF THREADS'''
    # t.start()
    stream.start_stream()
    midi_thread.start()

    while True:
        outport.send(tempoMessage)
        time.sleep(clock_interval)
        if stop_key:
            break

    '''Closing Audio threads and creating wav file'''
    stream.stop_stream()
    stream.close()
    p.terminate()
    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

    print "Closed audio channels and created wav file"
