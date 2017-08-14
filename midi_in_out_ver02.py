import mido
import threading
import midi_chords as miChords


def setup_chords(note_set):

    if STOP_NOTE != note_set:
        return True
    else:
        return False


def sendTempo():

    outport.send(tempoMessage)
    t = threading.Timer(clock_interval, sendTempo)
    t.start()


if __name__ == "__main__":

    inputs = mido.get_input_names()
    outputs = mido.get_output_names()

    inport = mido.open_input('MIDISTART MUSIC 25:MIDISTART MUSIC 25 MIDI 1 24:0')
    inport2 = mido.open_input('CH345:CH345 MIDI 1 20:0')
    outport = mido.open_output('CH345:CH345 MIDI 1 20:0')

    #Stop_loop = mido.Message('note_on', note=72) Maybe this is the reason why always it receives 72 when booting

    note = inport.receive()

    Tonic = note.copy()

    print "Tonic.note: ", Tonic.note
    print "please press a key for scale"

    while True:
        if setup_chords(Tonic.note):
            break
        note = inport.receive()
        Tonic = note.copy()

    miChords.Set_Tonic_Chord(Tonic)

    print "Tonic.note: ", Tonic.note
    print "start receiving notes"

    STOP_NOTE = 72
    BPM = 150
    OFFSET = 10
    clock_interval = 60. / ((BPM + OFFSET) * 24) #verify without multiplying by 24
    tempoMessage = mido.Message('clock')  # , time=clock_interval)

    print "Tempo Message", tempoMessage
    print "Clock Interval", clock_interval

    t = threading.Timer(clock_interval, sendTempo)
    t.start()

    for tone in inport:

        print "tone.note: ", tone.note
        print "Tonic.note: ", Tonic.note

        if tone.note == STOP_NOTE: #Stop_loop.note: Note C6 (72) closes the code.
            inport.close()
            inport2.close()
            outport.close()
            t.cancel()
            print "closing program"
            break
        else:
            miChords.Send_Chord(tone)
            # mido.Message('note_on', note=tone.note)