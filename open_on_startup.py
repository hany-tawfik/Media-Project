import time
import mido
import threading

def shutdownbutton():
    
    for msg in inport:
        print msg
        if setup_chords(msg.note):
            break
        msg = inport.receive()
        if msg.note == Stop_loop.note:
            inport.close()
            print "Shutting down in 5 seconds"
            time.sleep(5)
            #shutdown()
    return


def shutdown():
    command = "/usr/bin/sudo /sbin/shutdown -h now"
    import subprocess
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    output = process.communicate()[0]
    print output
    
def setup_chords(note_set):
    global Stop_loop
    if note_set != Stop_loop.note:
        return True
    else:
        return False
 
inputs = mido.get_input_names()
midi_start25 = inputs[0].encode('ascii')
inport = mido.open_input(midi_start25)
Stop_loop = mido.Message('note_on', note=49)

midi_thread = threading.Thread(target=shutdownbutton)
midi_thread.start()
    
#while True:
for i in range(3):
    
    #execfile("Media_Project.py")
    execfile("printing.py")
    print " That was open on startup file"
    time.sleep(5)
    print "You will be prompted to choose a new scale"

print "Shutting down"
#time.sleep(5)
#shutdown()
inport.close()
midi_thread.join()
