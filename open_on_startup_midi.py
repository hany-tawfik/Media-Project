import time
import mido
import threading

def shutdownbutton():
    global stop_flag_midi
    print "thread started"
    for msg in inport:
        #print msg
        
        if msg.note == Stop_loop.note:
            #msg.note = random_note.note
            inport.close()
            print "Shutting down in 5 seconds"
            print msg
            #time.sleep(3)
            stop_flag_midi = False
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
    
def shutdown():
    command = "/usr/bin/sudo /sbin/shutdown -r now"
    import subprocess
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    output = process.communicate()[0]
    print output
        

'''MIDI INPUT PORTS SETUP'''
inputs = mido.get_input_names()
midi_start25 = inputs[1].encode('ascii')
inport = mido.open_input(midi_start25)
Stop_loop = mido.Message('note_on', note=49)
random_note = mido.Message('note_on', note=51)
stop_flag_midi = True
note = inport.receive()
Tonic = note.copy()
print "note: ", note
#print "tonic: " , Tonic




while True:
        if setup_chords(Tonic.note):
            print "inside if inside while"
            break
        else:
            msg = inport.receive()
            print 'msg in while : ' , msg
            break

""" MIDI THREAD"""

midi_thread = threading.Thread(target=shutdownbutton)
midi_thread.start()


while stop_flag_midi:
    x=1
    #execfile("printing.py")
    execfile("Media_Project.py")
    print stop_flag_midi
    time.sleep(4)
    

    
print "shutting down"
time.sleep(3)
#shutdown()
