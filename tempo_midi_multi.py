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
    global Stop_loop
    if note_set != Stop_loop.note:
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
        print("new tempo estimated: ", tempo_integer[0])
        final_tempo = tempo_fix(tempo_integer[0])
        print("sent tempo: ", final_tempo)
        clock_interval = update_tempo(final_tempo)
        clock_value.put(clock_interval)
        tempoMessage = mido.Message('clock', time=clock_interval)

    return in_data, pyaudio.paContinue


def send_clock_process(clock_interval, stop_key_flag, clock_value):

    interval = clock_interval

    while True:
        if clock_value.empty() is False:
            interval = clock_value.get()
        if stop_key_flag.value == 1:
            print ("Closing child process")
            break
        outport.send(tempoMessage)
        time.sleep(interval)


def midi_msg_handler_thread():

    global start_stop_flag, Stop_loop, Start_msg

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


def tempo_fix(estimated_tempo):

    global saved_tempo, first_current_tempo, doubtful_tempo, mean_saved_tempo
    current_tempo = estimated_tempo

    if first_current_tempo is True:

        saved_tempo.append(current_tempo)
        first_current_tempo = False
    else:

        if mean_saved_tempo - THRESHOLD < current_tempo < mean_saved_tempo + THRESHOLD:

            saved_tempo.append(current_tempo)
            doubtful_tempo = [0]

            if len(saved_tempo) >= MAX_LENGTH:
                del saved_tempo[0]

        else:

            doubtful_tempo.append(current_tempo)

            if doubtful_tempo[len(doubtful_tempo) - PREVIOUS_DOUBTFUL_TEMPO] - THRESHOLD \
                    < doubtful_tempo[len(doubtful_tempo) - CURRENT_DOUBTFUL_TEMPO] \
                    < doubtful_tempo[len(doubtful_tempo) - PREVIOUS_DOUBTFUL_TEMPO] + THRESHOLD:

                saved_tempo = [doubtful_tempo[len(doubtful_tempo) - CURRENT_DOUBTFUL_TEMPO]]

    mean_saved_tempo = np.uint8(np.mean(saved_tempo))

    return mean_saved_tempo

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

    '''TEMPO STABILIZATION PARAMETERS'''
    CURRENT_DOUBTFUL_TEMPO = 1
    PREVIOUS_DOUBTFUL_TEMPO = 2
    THRESHOLD = 3
    MAX_LENGTH = 6
    saved_tempo = []
    first_current_tempo = True
    doubtful_tempo = [0]
    mean_saved_tempo = np.uint8

    '''THREADING DEFINITIONS'''
    midi_thread = threading.Thread(target=midi_msg_handler_thread)

    '''OBJECT DEFINITIONS'''
    RNNBeat = mm.features.beats.RNNBeatProcessor(online=True, nn_files=[BEATS_LSTM[0]])
    tempoEstimation = mm.features.tempo.TempoEstimationProcessor(min_bpm=40, max_bpm=180, fps=100)
    p = pyaudio.PyAudio()

    '''AUDIO VARIABLES DEFINITION'''
    SECONDS = 2.5
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
    tempoMessage = mido.Message('clock', time=clock_interval)
    startMessage = mido.Message('start')
    stopMessage = mido.Message('stop')
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
