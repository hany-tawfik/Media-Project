
from madmom.models import BEATS_LSTM
import madmom as mm
import midi_chords as miChords
import mido
import numpy as np
import pyaudio
import Queue
import struct
import threading


def callback_audio(in_data, frame_count, time_info, status):

    stream_queue.put(in_data)

    return (in_data, pyaudio.paContinue)


def setup_chords(note_set):

    if Stop_loop.note != note_set:
        return True
    else:
        return False


def send_tempo():

    global t
    outport.send(tempoMessage)

    if stop_key == False:

        t = threading.Timer(clock_interval, send_tempo)
        t.start()

    else:
        print "stop timer thread"


def stop_all_threads():

    global stop_key
    stop_key = True


def midi_msg_handler():

    for msg in inport:

        print "msg.note inside of thread: ", msg.note

        if msg.note == Stop_loop.note:  # Note C6 (72) closes the code.
            stop_all_threads()
            inport.close()
            inport2.close()
            outport.close()
            t.cancel()
            t.finished
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
    BPM = 120
    OFFSET = 7
    PPQ = 24  # Pulse per quarter note
    clock_interval = 60. / ((BPM + OFFSET) * PPQ)
    tempoMessage = mido.Message('clock')  # , time=clock_interval)

    '''THREADING DEFINITIONS'''
    midi_thread = threading.Thread(target=midi_msg_handler)
    t = threading.Timer(clock_interval, send_tempo)

    '''OBJECT DEFINITIONS'''
    RNNbeat = mm.features.beats.RNNBeatProcessor(online=True, nn_files=[BEATS_LSTM[0]])
    tempoEstimation = mm.features.tempo.TempoEstimationProcessor(min_bpm=40, max_bpm=180, fps=100)
    p = pyaudio.PyAudio()
    stream_queue = Queue.Queue()

    '''AUDIO VARIABLES DEFINITION'''
    SECONDS = 2.5
    RATE = 44100
    CHUNK = np.uint32(RATE*SECONDS)
    FORMAT = pyaudio.paInt16
    CHANNELS = 1

    stream = p.open(format=FORMAT,
                           channels=CHANNELS,
                           rate=RATE,
                           input=True,
                           frames_per_buffer=CHUNK,
                           stream_callback=callback_audio)

    '''MIDI DATA SETUP'''
    stop_key = False
    Stop_loop = mido.Message('note_on', note=72)
    note = inport.receive()
    Tonic = note.copy()

    print "Please press a key for choosing a scale"

    while True:
        if setup_chords(Tonic.note):
            break
        note = inport.receive()
        Tonic = note.copy()

    miChords.Set_Tonic_Scale(Tonic.note)
    miChords.update_chords()

    '''START OF THREADING(s)'''
    midi_thread.start()
    t.start()
    stream.start_stream()

    while True:

        samples = stream_queue.get()

        rawData = np.int16(struct.unpack('h' * CHUNK, samples))

        beats = RNNbeat(rawData)

        tempo_estimated = tempoEstimation.process(beats)

        print "tempo estimation first option: \n", tempo_estimated[0, 0]

        if stop_key:
            break

    stream.stop_stream()
    stream.close()
    p.terminate()

