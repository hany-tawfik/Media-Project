import threading
import mido

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
            
x = SendingNotes()
x.start()
