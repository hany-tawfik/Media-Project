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



if __name__ == "__main__":

    inputs = mido.get_input_names()
    outputs = mido.get_output_names()

    #inport = mido.open_input('MIDISTART MUSIC 25:MIDISTART MUSIC 25 MIDI 1 24:0')
    #inport2 = mido.open_input('CH345:CH345 MIDI 1 20:0')
    #outport = mido.open_output('CH345:CH345 MIDI 1 20:0')
    
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
    BPM = 100
    OFFSET = 6
    clock_interval = 60. / ((BPM + OFFSET) * 24) #verify without multiplying by 24
    tempoMessage = mido.Message('clock')  # , time=clock_interval)

    t = threading.Timer(clock_interval, sendTempo)
    t.start()

    for tone in inport:

        # print "tone.note: ", tone.note
        # print "Tonic.note: ", Tonic.note

        if tone.note == Stop_loop.note: #Note C6 (72) closes the code.
            stop_thread_timer()
            print "closing program"
            break
        else:            
            miChords.Send_Chord(tone)

t.cancel()
inport.close()
inport2.close()
outport.close()
