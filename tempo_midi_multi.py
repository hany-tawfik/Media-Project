from madmom.models import BEATS_LSTM
import madmom as mm
import midi_chords as miChords
import mido
import multiprocessing
import numpy as np
import pyaudio
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
    stop_key_flag.value = 1


def callback_audio(in_data, frame_count, time_info, status):

    global clock_interval, tempoMessage

    if stop_key is False:
        frames.append(in_data)
        raw_data = np.fromstring(in_data, dtype=np.int16)
        beats = RNNBeat(raw_data)
        tempo = tempoEstimation.process(beats)
        tempo_integer = map(np.int16, tempo[:, 0])
        clock_interval = update_tempo(tempo_integer[0])
        clock_value.put(clock_interval)
        tempoMessage = mido.Message('clock', time=clock_interval)
        print("new tempo: ", tempo_integer[0])

    return in_data, pyaudio.paContinue


def send_clock_process(clock_interval, stop_key_flag, clock_value):

    interval = clock_interval

    while True:
        if clock_value.empty() is False:
            interval = clock_value.get()
        if stop_key_flag.value == 1:
            print ("closing child process")
            break
        outport.send(tempoMessage)
        time.sleep(interval)


def midi_msg_handler_thread():

    global start_stop_flag

    for msg in inport:

        if msg.note == Stop_loop.note:  # Note C6 (72) closes the code.

            outport.send(stopMessage)
            time.sleep(1e-3)
            stop_all_threads()
            inport.close()
            inport2.close()
            outport.close()
            print ("Closing midi_msg_handler thread")
            break

        elif msg.note == Start_msg.note:

            if start_stop_flag is False:
                outport.send(stopMessage)
                time.sleep(1e-3)
                outport.send(startMessage)
                time.sleep(1e-3)
                start_stop_flag = True
            else:
                start_stop_flag = False
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
    DEFAULT_BPM = 100
    OFFSET = 2
    PPQ = 24  # Pulse per quarter note
    clock_interval = 60. / ((DEFAULT_BPM + OFFSET) * PPQ)
    clock_interval = np.float16(clock_interval)
    tempoMessage = mido.Message('clock', time=clock_interval)
    startMessage = mido.Message('start')
    stopMessage = mido.Message('stop')

    '''THREADING DEFINITIONS'''
    midi_thread = threading.Thread(target=midi_msg_handler_thread)

    '''OBJECT DEFINITIONS'''
    RNNBeat = mm.features.beats.RNNBeatProcessor(online=True, nn_files=[BEATS_LSTM[0]])
    tempoEstimation = mm.features.tempo.TempoEstimationProcessor(min_bpm=40, max_bpm=180, fps=100)
    p = pyaudio.PyAudio()

    '''AUDIO VARIABLES DEFINITION'''
    SECONDS = 4
    RATE = 44100
    CHUNK = np.uint32(RATE * SECONDS)
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

    '''START OF THREADS'''
    midi_thread.start()
    stream.start_stream()

    '''MULTIPROCESS SHARED MEMORIES'''
    clock_value = multiprocessing.Queue()
    stop_key_flag = multiprocessing.Value('i', 0)

    '''CHILD PROCESS'''
    ext_clock = multiprocessing.Process(target=send_clock_process, args=(clock_interval, stop_key_flag, clock_value))

    '''MIDI DATA SETUP'''
    print ("Please press a key for choosing a music scale")
    stop_key = False
    start_stop_flag = False
    Stop_loop = mido.Message('note_on', note=72)
    Start_msg = mido.Message('note_on', note=71)
    note = inport.receive()
    Tonic = note.copy()
    
    while True:
        if setup_chords(Tonic.note):
            break
        note = inport.receive()
        Tonic = note.copy()

    miChords.Set_Tonic_Scale(Tonic.note)
    miChords.update_chords()

    '''START OF CHILD PROCESS'''
    ext_clock.start()
    ext_clock.join()

    '''RUNNING TIME'''

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

    print ("Closed audio channels and created wav file")
