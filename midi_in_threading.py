import threading
import mido
import time

class SendingNotes(threading.Thread):
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
        self._stop_event.set()
        inport.close()
        inport2.close()
        outport.close()
            
x = SendingNotes()
x.start()

while True:
    print "It is working :) "
    time.sleep(1)
    counter +=1
    if counter >= 30:
        x.stop()
        print "closing program"
        break
       
        
        
    
