# -*- coding: utf-8 -*-
"""
Spyder Editor
This is a temporary script file.
"""

#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 25 13:44:09 2017
@author: HanyTawfik
"""

import mido
import time

def setup_chords(note):
        
    if 72 != note:    
        return True
    else:
        return False

def Major_Chord(naghama):
        #Tonic
        outport.send(naghama)
        time.sleep(1e-3)
        #Major third.
        naghama.note += 4
        time.sleep(1e-3)
        outport.send(naghama)
        #Fifth
        naghama.note += 3
        time.sleep(1e-3)
        outport.send(naghama)
        time.sleep(1e-3)
        mido.Message('note_off', note=naghama.note)
        
        
        return
    
def Minor_Chord(naghama):
        
        #Tonic
        outport.send(naghama)
        time.sleep(1e-3)
        #Minor third.
        naghama.note += 3
        time.sleep(1e-3)
        outport.send(naghama)
        #Fifth
        naghama.note += 4
        time.sleep(1e-3)
        outport.send(naghama)
        time.sleep(1e-3)
        mido.Message('note_off', note=naghama.note)
        return

def Dim_Chord(naghama):
        #Tonic
        outport.send(naghama)
        time.sleep(1e-3)
        
        #Minor third.
        naghama.note += 3
        time.sleep(1e-3)
        outport.send(naghama)
        
        #flat fifth
        naghama.note += 3
        time.sleep(1e-3)
        outport.send(naghama)
        
        #flat Minor sixth
        naghama.note += 4
        outport.send(naghama)
        time.sleep(1e-3)
        mido.Message('note_off', note=naghama.note)
        return

def Major_Dominant_7th_Chord(naghama):
        #Tonic
        outport.send(naghama)
        time.sleep(1e-3)
        #Major third.
        naghama.note += 4
        time.sleep(1e-3)
        outport.send(naghama)
        
        #Fifth
        naghama.note += 6
        time.sleep(1e-3)
        outport.send(naghama)
        #Minor seventh
        #naghama.note += 10
        #time.sleep(1e-3)
        #outport.send(naghama)
        
        time.sleep(1e-3)
        mido.Message('note_off', note=naghama.note)
        return
    
def Sus4_Chord(naghama):
        #Tonic
        outport.send(naghama)
        time.sleep(1e-3)
        
        #Fourth.
        naghama.note += 5
        time.sleep(1e-3)
        outport.send(naghama)
        #Fifth
        naghama.note += 2
        time.sleep(1e-3)
        outport.send(naghama)
        time.sleep(1e-3)
        mido.Message('note_off', note=naghama.note)
        return
    
def Minor_6th(naghama):
        #Tonic
        outport.send(naghama)
        time.sleep(1e-3)
        #Minor third.
        naghama.note += 3
        time.sleep(1e-3)
        outport.send(naghama)
        #Sixth
        naghama.note += 6
        time.sleep(1e-3)
        outport.send(naghama)
        time.sleep(1e-3)
        mido.Message('note_off', note=naghama.note)
        return
def Tonic_Fifth(naghama):
        #Tonic
        outport.send(naghama)
        time.sleep(1e-3)
        
        #Fifth
        naghama.note += 7
        time.sleep(1e-3)
        outport.send(naghama)
        time.sleep(1e-3)
        mido.Message('note_off', note=naghama.note)
        return

    
if __name__ == "__main__":

    inputs = mido.get_input_names()
    
    outputs = mido.get_input_names()
    
    inport = mido.open_input('MIDISTART MUSIC 25:MIDISTART MUSIC 25 MIDI 1 24:0')
    inport2 = mido.open_input('CH345:CH345 MIDI 1 20:0')
    outport = mido.open_output('CH345:CH345 MIDI 1 20:0')
    
    #delete later
    #outport2 = mido.open_output('USB2.0-MIDI Port 1')
    
    #just for testing
    #outport.send(mido.Message('note_on', note=72))
    #time.sleep(1)
    #outport.send(mido.Message('note_off', note=72))
    
    
    Stop_loop = mido.Message('note_on', note=72)
    
    
    
    naghama = inport.receive()
    
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
    
    
    #Main octave.
    
    Tonic = naghama.copy()

    print "Tonic.note: ", Tonic.note
    print "please press a key for scale"     
    
    while True:
      if setup_chords(Tonic.note):
        break
      naghama = inport.receive()
      Tonic = naghama.copy()        
    
    Second = Tonic.note + 2
    Third_major = Tonic.note + 4
    Fourth = Tonic.note + 5
    Fifth = Tonic.note + 7
    Sixth_major = Tonic.note + 9
    Seventh_major = Tonic.note + 11
    
    #Octave down.
    Tonic_octaveDOWN = Tonic.note - 12
    Second_octaveDOWN = Second - 12
    Third_major_octaveDOWN = Third_major - 12
    Fourth_octaveDOWN = Fourth - 12
    Fifth_octaveDOWN = Fifth - 12
    Sixth_major_octaveDOWN = Sixth_major - 12
    Seventh_major_octaveDOWN = Seventh_major - 12
    
    #Octave up.
    Tonic_octaveUP = Tonic.note + 12
    Second_octaveUP = Second + 12
    Third_major_octaveUP = Third_major + 12
    Fourth_octaveUP = Fourth + 12
    Fifth_octaveUP = Fifth + 12
    Sixth_major_octaveUP = Sixth_major + 12
    Seventh_major_octaveUP = Seventh_major + 12
    
    print "Tonic.note: ", Tonic.note
    print "start receiving notes"
        
        
    clock_interval = 60. / ((150 + 3) * 24)
    tempoMessage = mido.Message('clock')#, time=clock_interval)
    #mido.bpm2tempo(120)
    print tempoMessage
    print clock_interval    
    print "Send message 1"
    outport.send(tempoMessage)
    time.sleep(clock_interval)
    print "Send message 2"
    outport.send(tempoMessage)
    time.sleep(clock_interval)
    print "Send message 3"
    outport.send(tempoMessage)
    time.sleep(clock_interval)
    print "Send message 4"
    outport.send(tempoMessage)
    time.sleep(clock_interval)
        
    while True:
        print "Send now further messages"
        outport.send(tempoMessage)
        time.sleep(clock_interval)
        
     
    for naghama in inport:
        
        print "naghama.note: ", naghama.note
        print "Tonic.note: ", Tonic.note
        outport.send(tempoMessage)
        
        if naghama.note == Stop_loop.note: # Note C6 (72) closes the code.
            inport.close()
            inport2.close()
            outport.close()
            print "closing program"    
            break
        #Main octave
        elif naghama.note == Tonic.note:
            Major_Chord(naghama)
            
        elif naghama.note == Second:
            Minor_Chord(naghama)
            
        elif naghama.note == Third_major:
            Minor_Chord(naghama)
            
        elif naghama.note == Fourth:
            Major_Chord(naghama)
        
        elif naghama.note == Fifth:  
            Major_Chord(naghama)
            
        elif naghama.note == Sixth_major:
            Minor_Chord(naghama)
        
        elif naghama.note == Seventh_major:
            Dim_Chord(naghama)
            
        #Octave up
        elif naghama.note == Tonic_octaveUP : #or Fifth_octaveUP  
            Sus4_Chord(naghama)
        elif naghama.note == Fifth_octaveUP : # This should be written OR with Csus4 
            Sus4_Chord(naghama)
        elif naghama.note == Fourth_octaveUP:
            Minor_6th(naghama)
        elif naghama.note == Second_octaveUP or Third_major_octaveUP or Sixth_major_octaveUP or Seventh_major_octaveUP:
            Major_Dominant_7th_Chord(naghama)
        else:
            Tonic_Fifth(naghama)
            #mido.Message('note_on', note=naghama.note)
            
            
            
            
