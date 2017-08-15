import mido
import threading
import midi_chords as miChords
import numpy as np


def setup_chords(note_set):

    if Stop_loop.note != note_set:
        return True
    else:
        return False


def sendTempo():

    outport.send(tempoMessage)

    if stop_timer == False:

        t = threading.Timer(clock_interval, sendTempo)
        t.start()

    else:

        print "stop timer"
        
'''        
def sendTempo():

    global timer_counter
    outport.send(tempoMessage)

    if stop_timer == False:

        if timer_counter <= 30:

            t = threading.Timer(clock_interval, sendTempo)
            t.start()
            timer_counter += 1
            print "timer_counter: ", timer_counter

    else:
        print "stop timer"
'''
    
def stop_thread_timer():

    global stop_timer

    stop_timer = True

    return stop_timer


if __name__ == "__main__":

    inputs = mido.get_input_names()
    outputs = mido.get_output_names()

    #inport = mido.open_input('MIDISTART MUSIC 25:MIDISTART MUSIC 25 MIDI 1 24:0')
    #inport2 = mido.open_input('CH345:CH345 MIDI 1 20:0')
    #outport = mido.open_output('CH345:CH345 MIDI 1 20:0')
    x = inputs[0].encode('ascii')
    y = inputs[1].encode('ascii')
    print x
    print y

    
    inport = mido.open_ioport(x)
    #inport2 = mido.open_input('CH345:CH345 MIDI 1 24:0')
    outport = mido.open_ioport(y)

    Stop_loop = mido.Message('note_on', note=72) # Maybe this is the reason why always it receives 72 when booting
    
    note = inport.receive()

    Tonic = note.copy()

    print "Tonic.note: ", Tonic.note
    print "please press a key for scale"

    while True:
        if setup_chords(Tonic.note):
            break
        note = inport.receive()
        Tonic = note.copy()

    miChords.Set_Tonic_Scale(Tonic.note)
    miChords.update_chords()

    print "Tonic.note: ", Tonic.note
    print "start receiving notes"
    
    timer_counter = 0
    stop_timer = False
    STOP_NOTE = 72
    BPM = 120
    OFFSET = 7
    clock_interval = 60. / ((BPM + OFFSET) * 24) #verify without multiplying by 24
    clock_interval = np.float16(clock_interval)
    tempoMessage = mido.Message('clock')  # , time=clock_interval)

    print "Tempo Message", tempoMessage
    print "Clock Interval", clock_interval

    t = threading.Timer(clock_interval, sendTempo)
    t.start()

    for tone in inport:

        # print "tone.note: ", tone.note
        # print "Tonic.note: ", Tonic.note

        if tone.note == Stop_loop.note: #Note C6 (72) closes the code.
            #inport.close()
            #inport2.close()
            #outport.close()
            #t.cancel()
            stop_thread_timer()
            print "closing program"
            break
        else:
            # miChords.Set_Current_Chord(tone)
            miChords.Send_Chord(tone)
            # mido.Message('note_on', note=tone.note)
            
t.cancel()
t.finished
inport.close()
inport2.close()
outport.close()

