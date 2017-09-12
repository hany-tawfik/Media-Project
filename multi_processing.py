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
import multiprocessing

def setup_chords(note_set):

    if Stop_loop.note != note_set:
        return True
    else:
        return False
    
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
            
def stop_all_threads():

    global stop_key
    stop_key = True            
            
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
    
    '''MULTIPROCESSING DEFINITIONS'''
    #midi_thread = multiprocessing.Process(target=midi_msg_handler_thread)
    midi_thread = threading.Thread(target=midi_msg_handler_thread)
    
    '''MIDI DATA SETUP'''
    print "Please press a key for choosing a music scale"
    stop_key = False
    Stop_loop = mido.Message('note_on', note=72)
    
    while True:
        note = inport.receive()
        Tonic = note.copy()
    
        while True:
            if setup_chords(Tonic.note):
                break
            note = inport.receive()
            Tonic = note.copy()
            
            if msg.note == Stop_loop.note:  # Note C6 (72) closes the code.
                break

        miChords.Set_Tonic_Scale(Tonic.note)
        miChords.update_chords()

        '''START OF MULTIPROCESSES'''   
        midi_thread.start()
        midi_thread.join()
