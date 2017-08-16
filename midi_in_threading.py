import threading
import mido
import time

class SendingNotes(threading.Thread):
    
    def __init__(self):
        super(SendingNotes, self).__init__()
        self._stop_event = threading.Event()
        
    def run(self):
    
        inputs = mido.get_input_names()
        
        korg = inputs[0].encode('ascii')
        midi_start25 = inputs[1].encode('ascii')

        inport = mido.open_input(midi_start25)
        inport2 = mido.open_input(korg)
        outport = mido.open_output(korg)
        for msg in inport:
            outport.send(msg)
            print msg.note
            
    def stop(self):
        global inport, inport2, outport
        self._stop_event.set()
        inport.close()
        inport2.close()
        outport.close()
            
x = SendingNotes()
x.start()
counter = 0
while True:
    print "It is working :) "
    time.sleep(1)
    counter +=1
    if counter >= 10:
        x.stop()
        print "closing program"
        break
       
        
        
    
