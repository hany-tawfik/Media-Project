import time
import mido
import threading

def shutdownbutton():
    global stop_flag
    
    for msg in inport:
        print msg
        
        if msg.note == Stop_loop.note:
            msg = random_note
            inport.close()
            print "Shutting down in 5 seconds"
            print msg
            time.sleep(3)
            stop_flag = False
            break
        
        else:
            print msg
        
        

'''MIDI INPUT PORTS SETUP'''
inputs = mido.get_input_names()
midi_start25 = inputs[1].encode('ascii')
inport = mido.open_input(midi_start25)
Stop_loop = mido.Message('note_on', note=49)
random_note = mido.Message('note_on', note=51)
stop_flag = True

""" MIDI THREAD"""

#midi_thread = threading.Thread(target=shutdownbutton)
#midi_thread.start()

for msg in inport:
    print msg

"""while stop_flag:
    x=1
"""
    
print "shuting down"
