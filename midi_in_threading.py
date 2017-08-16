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
        global inport, inport2, outport, stop_now

        inport = mido.open_input(midi_start25)
        inport2 = mido.open_input(korg)
        outport = mido.open_output(korg)
        
        stop_now = False
        
    def run(self):
        
        msg = inport.receive()
        msg = 0
        global stop_now
        
        for msg in inport:
            if msg.note == 72:
                print "closing program"
                stop_now = True
                break
            outport.send(msg)
            print msg.note
            
    def stop_receiving():
    
        global stop_now
        return stop
    
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
    if x.stop_receiving:
        break    

x.stop()
x.join()
        
        
    
