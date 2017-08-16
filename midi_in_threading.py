import threading
import mido
import time

class SendingNotes(threading.Thread):
    
    def __init__(self):
        super(SendingNotes, self).__init__()
        self._stop_event = threading.Event()
       
        inputs = mido.get_input_names()
        
        korg = inputs[0].encode('ascii')
        midi_start25 = inputs[1].encode('ascii')
        global inport, inport2, outport

        inport = mido.open_input(midi_start25)
        inport2 = mido.open_input(korg)
        outport = mido.open_output(korg)
        
    
        
    def run(self):
    
        
        for msg in inport:
            if msg.note == 72:
                break
            outport.send(msg)
            print msg.note
            
    def stop(self):
        
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
    if counter >= 5:
        x.stop()
        x.msg = 72
        
        print "closing program"
        break
x.join()
        
        
    
