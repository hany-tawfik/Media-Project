import mido
import time

'''SETTING INPORTs/OUTPORTs'''

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


'''SETTING NOTES/CHORDS'''

Tonic_Scale = 0
Temp_scale = 0
Play_Chord = 0

''' 
C = 48
D = 50
E = 52
F = 53
G = 55
A = 57
B = 59
C = 60
C major scale :
    First octave main chords :      C      - Dm - Em - F   - G     - Am - Bdim
    Second octave secondary chords: Csus4  - D7 - E7 - Fm6 - Gsus4 - A7 - B7
 '''

# Main octave.
Second = Tonic_Scale + 2
Third_major = Tonic_Scale + 4
Fourth = Tonic_Scale + 5
Fifth = Tonic_Scale + 7
Sixth_major = Tonic_Scale + 9
Seventh_major = Tonic_Scale + 11

# Octave down.
Tonic_octaveDOWN = Tonic_Scale - 12
Second_octaveDOWN = Second - 12
Third_major_octaveDOWN = Third_major - 12
Fourth_octaveDOWN = Fourth - 12
Fifth_octaveDOWN = Fifth - 12
Sixth_major_octaveDOWN = Sixth_major - 12
Seventh_major_octaveDOWN = Seventh_major - 12

# Octave up.
Tonic_octaveUP = Tonic_Scale + 12
Second_octaveUP = Second + 12
Third_major_octaveUP = Third_major + 12
Fourth_octaveUP = Fourth + 12
Fifth_octaveUP = Fifth + 12
Sixth_major_octaveUP = Sixth_major + 12
Seventh_major_octaveUP = Seventh_major + 12


def Set_Tonic_Scale(chord):

    global Tonic_Scale
    Tonic_Scale = chord

def update_chords():

    global Second, Third_major, Fourth, Fifth, Sixth_major, Seventh_major
    global Tonic_octaveDOWN, Second_octaveDOWN, Third_major_octaveDOWN, Fourth_octaveDOWN, Fifth_octaveDOWN, \
        Sixth_major_octaveDOWN, Seventh_major_octaveDOWN
    global Tonic_octaveUP, Second_octaveUP, Third_major_octaveUP, Fourth_octaveUP, Fifth_octaveUP, \
        Sixth_major_octaveUP, Seventh_major_octaveUP

    # Main octave.
    Second = Tonic_Scale + 2
    Third_major = Tonic_Scale + 4
    Fourth = Tonic_Scale + 5
    Fifth = Tonic_Scale + 7
    Sixth_major = Tonic_Scale + 9
    Seventh_major = Tonic_Scale + 11

    # Octave down.
    Tonic_octaveDOWN = Tonic_Scale - 12
    Second_octaveDOWN = Second - 12
    Third_major_octaveDOWN = Third_major - 12
    Fourth_octaveDOWN = Fourth - 12
    Fifth_octaveDOWN = Fifth - 12
    Sixth_major_octaveDOWN = Sixth_major - 12
    Seventh_major_octaveDOWN = Seventh_major - 12

    # Octave up.

    Tonic_octaveUP = Tonic_Scale + 12
    Second_octaveUP = Second + 12
    Third_major_octaveUP = Third_major + 12
    Fourth_octaveUP = Fourth + 12
    Fifth_octaveUP = Fifth + 12
    Sixth_major_octaveUP = Sixth_major + 12
    Seventh_major_octaveUP = Seventh_major + 12


def Set_Current_Chord(current_chord):
    global Play_Chord
    Play_Chord = current_chord.copy()


def Major_Chord(output_chord):

    # Tonic
    print "Major chord 1: ", output_chord.note
    outport.send(output_chord)
    time.sleep(1e-3)
    # Major third.
    output_chord.note += 4
    time.sleep(1e-3)
    print "Major chord 3: ", output_chord.note
    outport.send(output_chord)
    # Fifth
    output_chord.note += 3
    time.sleep(1e-3)
    print "Major chord 5: ", output_chord.note
    outport.send(output_chord)
    time.sleep(1e-3)
    mido.Message('note_off', note=output_chord.note)


def Minor_Chord(output_chord):

    print "Minor_Chord"
    # Tonic
    outport.send(output_chord)
    time.sleep(1e-3)
    # Minor third.
    output_chord.note += 3
    time.sleep(1e-3)
    outport.send(output_chord)
    # Fifth
    output_chord.note += 4
    time.sleep(1e-3)
    outport.send(output_chord)
    time.sleep(1e-3)
    mido.Message('note_off', note=output_chord.note)

def Dim_Chord(output_chord):

    print "Dim_Chord"
    # Tonic
    outport.send(output_chord)
    time.sleep(1e-3)

    # Minor third.
    output_chord.note += 3
    time.sleep(1e-3)
    outport.send(output_chord)

    # flat fifth
    output_chord.note += 3
    time.sleep(1e-3)
    outport.send(output_chord)

    # flat Minor sixth
    output_chord.note += 4
    outport.send(output_chord)
    time.sleep(1e-3)
    mido.Message('note_off', note=output_chord.note)


def Sus4_Chord(output_chord):

    print "Sus4_Chord"
   # Tonic
    outport.send(output_chord)
    time.sleep(1e-3)

    # Fourth.
    output_chord.note += 5
    time.sleep(1e-3)
    outport.send(output_chord)
    # Fifth
    output_chord.note += 2
    time.sleep(1e-3)
    outport.send(output_chord)
    time.sleep(1e-3)
    mido.Message('note_off', note=output_chord.note)


def Minor_6th(output_chord):

    print "Minor_6th"
    # Tonic
    outport.send(output_chord)
    time.sleep(1e-3)
    # Minor third.
    output_chord.note += 3
    time.sleep(1e-3)
    outport.send(output_chord)
    # Sixth
    output_chord.note += 6
    time.sleep(1e-3)
    outport.send(output_chord)
    time.sleep(1e-3)
    mido.Message('note_off', note=output_chord.note)


def Major_Dominant_7th_Chord(output_chord):

    print "Major_Dominant_7th_Chord"
    # Tonic
    outport.send(output_chord)
    time.sleep(1e-3)
    # Major third.
    output_chord.note += 4
    time.sleep(1e-3)
    outport.send(output_chord)

    # Fifth
    output_chord.note += 6
    time.sleep(1e-3)
    outport.send(output_chord)
    # Minor seventh
    # naghama.note += 10
    # time.sleep(1e-3)
    # outport.send(naghama)

    time.sleep(1e-3)
    mido.Message('note_off', note=output_chord.note)

def Tonic_Fifth(output_chord):

    print "Tonic Fifth"

    # Tonic
    outport.send(output_chord)
    time.sleep(1e-3)

    # Fifth
    output_chord.note += 7
    time.sleep(1e-3)
    outport.send(output_chord)
    time.sleep(1e-3)
    mido.Message('note_off', note=output_chord.note)


def Send_Chord(output_chord):

    # Mapping a dictionary

    temp = output_chord.copy()
    temp = temp.note

    print "temp: ", temp
    print "Tonic Scale : ", Tonic_Scale

    switcher = {

        Tonic_Scale: Major_Chord,
        Fourth: Major_Chord,
        Fifth: Major_Chord,
        Second: Minor_Chord,
        Third_major: Minor_Chord,
        Sixth_major: Minor_Chord,
        Seventh_major: Dim_Chord,
        Tonic_octaveUP: Sus4_Chord,
        Fifth_octaveUP: Sus4_Chord,
        Fourth_octaveUP: Minor_6th,
        Second_octaveUP: Major_Dominant_7th_Chord,
        Third_major_octaveUP: Major_Dominant_7th_Chord,
        Sixth_major_octaveUP: Major_Dominant_7th_Chord,
        Seventh_major_octaveUP: Major_Dominant_7th_Chord,
    }

    # Get the function from switcher dictionary
    func = switcher.get(temp, Tonic_Fifth)
    print "second: ", Second
    print "output_chord.note: ", output_chord.note
    print "Output Chord: ", output_chord
    # Execute the function
    func(output_chord)


