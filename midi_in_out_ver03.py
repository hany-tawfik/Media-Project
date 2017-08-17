'''
import mido
import threading
import midi_chords as miChords


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


def stop_thread_timer():

    global stop_timer

    stop_timer = True

    return stop_timer


def test_message():

    print "Its ALIVE..... its ALIVE"
    
    global inport
    
    for msg in inport:

        print "msg.note inside of thread: ", msg.note

        if msg.note == Stop_loop.note: #Note C6 (72) closes the code.
            stop_thread_timer()
            inport.close()
            inport2.close()
            outport.close()
            t.cancel()
            t.finished
            print "closing thread"
            break
        else:
            miChords.Send_Chord(msg)


if __name__ == "__main__":

    inputs = mido.get_input_names()

    korg = inputs[0].encode('ascii')
    midi_start25 = inputs[1].encode('ascii')

    inport = mido.open_input(midi_start25)
    inport2 = mido.open_input(korg)
    outport = mido.open_output(korg)

    Stop_loop = mido.Message('note_on', note=72) # Maybe this is the reason why always it receives 72 when booting

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

    stop_timer = False
    STOP_NOTE = 72
    BPM = 120
    OFFSET = 7
    clock_interval = 60. / ((BPM + OFFSET) * 24) #verify without multiplying by 24
    tempoMessage = mido.Message('clock')  # , time=clock_interval)
    
    t = threading.Timer(clock_interval, sendTempo)

    midi_thread = threading.Thread(target=test_message)

    midi_thread.start()
    t.start()
'''

import mido
import threading
import midi_chords as miChords


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


def stop_thread_timer():

    global stop_timer

    stop_timer = True

    return stop_timer


def test_message():

    for msg in inport:

        print "msg.note inside of thread: ", msg.note

        if msg.note == Stop_loop.note:  # Note C6 (72) closes the code.
            stop_thread_timer()
            inport.close()
            inport2.close()
            outport.close()
            t.cancel()
            t.finished
            print "closing thread"
            break
        else:
            miChords.Send_Chord(msg)


if __name__ == "__main__":

    inputs = mido.get_input_names()

    korg = inputs[0].encode('ascii')
    midi_start25 = inputs[1].encode('ascii')

    inport = mido.open_input(midi_start25)
    inport2 = mido.open_input(korg)
    outport = mido.open_output(korg)

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

    stop_timer = False
    BPM = 120
    OFFSET = 7
    PPQ = 24  # Pulse per quarter note
    clock_interval = 60. / ((BPM + OFFSET) * PPQ)  # verify without multiplying by 24
    tempoMessage = mido.Message('clock')  # , time=clock_interval)

    midi_thread = threading.Thread(target=test_message)
    t = threading.Timer(clock_interval, sendTempo)

    midi_thread.start()
    t.start()

