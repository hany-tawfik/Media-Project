import time
import mido
import threading

def shutdownbutton():
    global stop_flag
    
    for msg in inport:
        #print msg
        
        if msg.note == Stop_loop.note:
            msg.note = random_note.note
            inport.close()
            print "Shutting down in 5 seconds"
            print msg
            #time.sleep(3)
            stop_flag = False
            break
        
        else:
            print msg
            
def setup_chords(note):
    """this bypass the last saved midi value """
    global Stop_loop
    if note != Stop_loop.note:
        return True
    else:
        return False
    
        
        

'''MIDI INPUT PORTS SETUP'''
inputs = mido.get_input_names()
midi_start25 = inputs[1].encode('ascii')
inport = mido.open_input(midi_start25)
Stop_loop = mido.Message('note_on', note=49)
random_note = mido.Message('note_on', note=51)
stop_flag = True
note = inport.receive()
Tonic = note.copy()
print "note: ", note
#print "tonic: " , Tonic

while True:
        if setup_chords(Tonic.note):
            break
        msg = inport.receive()

""" MIDI THREAD"""

midi_thread = threading.Thread(target=shutdownbutton)
midi_thread.start()


while stop_flag:
    x=1

    
print "shuting down"
