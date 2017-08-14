import mido
import time

'''SETTING INPORTs/OUTPORTs'''

inputs = mido.get_input_names()
outputs = mido.get_output_names()
inport = mido.open_input('MIDISTART MUSIC 25:MIDISTART MUSIC 25 MIDI 1 24:0')
inport2 = mido.open_input('CH345:CH345 MIDI 1 20:0')
outport = mido.open_output('CH345:CH345 MIDI 1 20:0')


'''SETTING NOTES/CHORDS'''

Tonic_Scale = 0
Temp_scale = 0

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


def Set_Tonic_Chord(chord):

    global Tonic_Scale
    global Temp_scale
    Tonic_Scale = chord
    Temp_scale = Tonic_Scale


def Major_Chord():
    
    global Tonic_Scale
    # Tonic
    outport.send(Tonic_Scale)
    time.sleep(1e-3)
    # Major third.
    Tonic_Scale.note += 4
    time.sleep(1e-3)
    outport.send(Tonic_Scale)
    # Fifth
    Tonic_Scale.note += 3
    time.sleep(1e-3)
    outport.send(Tonic_Scale)
    time.sleep(1e-3)
    mido.Message('note_off', note=Tonic_Scale.note)
    Tonic_Scale = Temp_scale


def Minor_Chord():
    
    global Tonic_Scale
    # Tonic
    outport.send(Tonic_Scale)
    time.sleep(1e-3)
    # Minor third.
    Tonic_Scale.note += 3
    time.sleep(1e-3)
    outport.send(Tonic_Scale)
    # Fifth
    Tonic_Scale.note += 4
    time.sleep(1e-3)
    outport.send(Tonic_Scale)
    time.sleep(1e-3)
    mido.Message('note_off', note=Tonic_Scale.note)
    Tonic_Scale = Temp_scale

def Dim_Chord():

    global Tonic_Scale
    # Tonic
    outport.send(Tonic_Scale)
    time.sleep(1e-3)

    # Minor third.
    Tonic_Scale.note += 3
    time.sleep(1e-3)
    outport.send(Tonic_Scale)

    # flat fifth
    Tonic_Scale.note += 3
    time.sleep(1e-3)
    outport.send(Tonic_Scale)

    # flat Minor sixth
    Tonic_Scale.note += 4
    outport.send(Tonic_Scale)
    time.sleep(1e-3)
    mido.Message('note_off', note=Tonic_Scale.note)
    Tonic_Scale = Temp_scale


def Sus4_Chord():
    
    global Tonic_Scale
    # Tonic
    outport.send(Tonic_Scale)
    time.sleep(1e-3)

    # Fourth.
    Tonic_Scale.note += 5
    time.sleep(1e-3)
    outport.send(Tonic_Scale)
    # Fifth
    Tonic_Scale.note += 2
    time.sleep(1e-3)
    outport.send(Tonic_Scale)
    time.sleep(1e-3)
    mido.Message('note_off', note=Tonic_Scale.note)
    Tonic_Scale = Temp_scale


def Minor_6th():
    
    global Tonic_Scale
    # Tonic
    outport.send(Tonic_Scale)
    time.sleep(1e-3)
    # Minor third.
    Tonic_Scale.note += 3
    time.sleep(1e-3)
    outport.send(Tonic_Scale)
    # Sixth
    Tonic_Scale.note += 6
    time.sleep(1e-3)
    outport.send(Tonic_Scale)
    time.sleep(1e-3)
    mido.Message('note_off', note=Tonic_Scale.note)
    Tonic_Scale = Temp_scale


def Major_Dominant_7th_Chord():
    
    global Tonic_Scale
    # Tonic
    outport.send(Tonic_Scale)
    time.sleep(1e-3)
    # Major third.
    Tonic_Scale.note += 4
    time.sleep(1e-3)
    outport.send(Tonic_Scale)

    # Fifth
    Tonic_Scale.note += 6
    time.sleep(1e-3)
    outport.send(Tonic_Scale)
    # Minor seventh
    # naghama.note += 10
    # time.sleep(1e-3)
    # outport.send(naghama)

    time.sleep(1e-3)
    mido.Message('note_off', note=Tonic_Scale.note)
    Tonic_Scale = Temp_scale


def Tonic_Fifth():

    global Tonic_Scale
    # Tonic
    outport.send(Tonic_Scale)
    time.sleep(1e-3)

    # Fifth
    Tonic_Scale.note += 7
    time.sleep(1e-3)
    outport.send(Tonic_Scale)
    time.sleep(1e-3)
    mido.Message('note_off', note=Tonic_Scale.note)
    Tonic_Scale = Temp_scale


def Send_Chord(output_chord):

    # Mapping a dictionary

    switcher = {

        Tonic_Scale or Fourth or Fifth: Major_Chord,
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
    print "Tonic: ", Tonic_Scale.tone
    

