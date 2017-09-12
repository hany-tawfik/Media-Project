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
    midi_thread = multiprocessing.Process(target=midi_msg_handler_thread)
