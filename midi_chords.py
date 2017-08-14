import mido
import time

'''SETTING INPORTs/OUTPORTs'''

inputs = mido.get_input_names()
outputs = mido.get_output_names()
inport = mido.open_input('MIDISTART MUSIC 25:MIDISTART MUSIC 25 MIDI 1 24:0')
inport2 = mido.open_input('CH345:CH345 MIDI 1 20:0')
outport = mido.open_output('CH345:CH345 MIDI 1 20:0')


'''SETTING NOTES/CHORDS'''

Tonic_Chord = 0

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
Second = Tonic_Chord + 2
Third_major = Tonic_Chord + 4
Fourth = Tonic_Chord + 5
Fifth = Tonic_Chord + 7
Sixth_major = Tonic_Chord + 9
Seventh_major = Tonic_Chord + 11

# Octave down.
Tonic_octaveDOWN = Tonic_Chord - 12
Second_octaveDOWN = Second - 12
Third_major_octaveDOWN = Third_major - 12
Fourth_octaveDOWN = Fourth - 12
Fifth_octaveDOWN = Fifth - 12
Sixth_major_octaveDOWN = Sixth_major - 12
Seventh_major_octaveDOWN = Seventh_major - 12

# Octave up.
Tonic_octaveUP = Tonic_Chord + 12
Second_octaveUP = Second + 12
Third_major_octaveUP = Third_major + 12
Fourth_octaveUP = Fourth + 12
Fifth_octaveUP = Fifth + 12
Sixth_major_octaveUP = Sixth_major + 12
Seventh_major_octaveUP = Seventh_major + 12


def Set_Tonic_Chord(chord):

    global Tonic_Chord
    Tonic_Chord = chord


def Major_Chord():
    # Tonic
    outport.send(Tonic_Chord)
    time.sleep(1e-3)
    # Major third.
    Tonic_Chord.note += 4
    time.sleep(1e-3)
    outport.send(Tonic_Chord)
    # Fifth
    Tonic_Chord.note += 3
    time.sleep(1e-3)
    outport.send(Tonic_Chord)
    time.sleep(1e-3)
    mido.Message('note_off', note=Tonic_Chord.note)


def Minor_Chord():
    # Tonic
    outport.send(Tonic_Chord)
    time.sleep(1e-3)
    # Minor third.
    Tonic_Chord.note += 3
    time.sleep(1e-3)
    outport.send(Tonic_Chord)
    # Fifth
    Tonic_Chord.note += 4
    time.sleep(1e-3)
    outport.send(Tonic_Chord)
    time.sleep(1e-3)
    mido.Message('note_off', note=Tonic_Chord.note)

def Dim_Chord():

    # Tonic
    outport.send(Tonic_Chord)
    time.sleep(1e-3)

    # Minor third.
    Tonic_Chord.note += 3
    time.sleep(1e-3)
    outport.send(Tonic_Chord)

    # flat fifth
    Tonic_Chord.note += 3
    time.sleep(1e-3)
    outport.send(Tonic_Chord)

    # flat Minor sixth
    Tonic_Chord.note += 4
    outport.send(Tonic_Chord)
    time.sleep(1e-3)
    mido.Message('note_off', note=Tonic_Chord.note)


def Sus4_Chord():
    # Tonic
    outport.send(Tonic_Chord)
    time.sleep(1e-3)

    # Fourth.
    Tonic_Chord.note += 5
    time.sleep(1e-3)
    outport.send(Tonic_Chord)
    # Fifth
    Tonic_Chord.note += 2
    time.sleep(1e-3)
    outport.send(Tonic_Chord)
    time.sleep(1e-3)
    mido.Message('note_off', note=Tonic_Chord.note)


def Minor_6th():
    # Tonic
    outport.send(Tonic_Chord)
    time.sleep(1e-3)
    # Minor third.
    Tonic_Chord.note += 3
    time.sleep(1e-3)
    outport.send(Tonic_Chord)
    # Sixth
    Tonic_Chord.note += 6
    time.sleep(1e-3)
    outport.send(Tonic_Chord)
    time.sleep(1e-3)
    mido.Message('note_off', note=Tonic_Chord.note)


def Major_Dominant_7th_Chord():
    # Tonic
    outport.send(Tonic_Chord)
    time.sleep(1e-3)
    # Major third.
    Tonic_Chord.note += 4
    time.sleep(1e-3)
    outport.send(Tonic_Chord)

    # Fifth
    Tonic_Chord.note += 6
    time.sleep(1e-3)
    outport.send(Tonic_Chord)
    # Minor seventh
    # naghama.note += 10
    # time.sleep(1e-3)
    # outport.send(naghama)

    time.sleep(1e-3)
    mido.Message('note_off', note=Tonic_Chord.note)


def Tonic_Fifth():
    # Tonic
    outport.send(Tonic_Chord)
    time.sleep(1e-3)

    # Fifth
    Tonic_Chord.note += 7
    time.sleep(1e-3)
    outport.send(Tonic_Chord)
    time.sleep(1e-3)
    mido.Message('note_off', note=Tonic_Chord.note)


def Send_Chord(output_chord):

    # Mapping a dictionary

    switcher = {

        Tonic_Chord or Fourth or Fifth: Major_Chord,
        Second or Third_major or Sixth_major: Minor_Chord,
        Seventh_major: Dim_Chord,
        Tonic_octaveUP or Fifth_octaveUP: Sus4_Chord,
        Fourth_octaveUP: Minor_6th,
        Second_octaveUP or Third_major_octaveUP or
        Sixth_major_octaveUP or Seventh_major_octaveUP: Major_Dominant_7th_Chord,
    }

    # Get the function from switcher dictionary
    func = switcher.get(output_chord, Tonic_Fifth)
    # Execute the function
    func()
    print "Output Chord: ", output_chord
