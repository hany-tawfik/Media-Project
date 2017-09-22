"""
import mido 

'''MIDI INPUT PORTS SETUP'''
inputs = mido.get_input_names()
midi_start25 = inputs[0].encode('ascii')
inport = mido.open_input(midi_start25)
Stop_loop = mido.Message('note_on', note=49)
stop_flag = True
#msg = inport.receive()


for msg in inport:
  print msg
"""
  
print "Hi there"
