import time
import mido
import threading

def shutdownbutton():
    """THis function waits for C#4 to be pressed to shutdown the Pi"""
    global stop_flag
    
    for msg in inport:
        print msg
        if setup_chords(msg.note):
            Print "Fixing the wrong note works"
            break
        msg = inport.receive()
        if msg.note == Stop_loop.note:
            inport.close()
            print "Shutting down in 5 seconds"
            time.sleep(3)
            stop_flag = False
            break
    return


def shutdown():
    command = "/usr/bin/sudo /sbin/shutdown -h now"
    import subprocess
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    output = process.communicate()[0]
    print output
    
def setup_chords(note_set):
    """this bypass the last saved midi value """
    global Stop_loop
    if note_set != Stop_loop.note:
        return True
    else:
        return False
    
    
    
'''MIDI INPUT PORTS SETUP'''
inputs = mido.get_input_names()
midi_start25 = inputs[0].encode('ascii')
inport = mido.open_input(midi_start25)
Stop_loop = mido.Message('note_on', note=49)
stop_flag = True
msg = inport.receive()

""" MIDI THREAD"""
midi_thread = threading.Thread(target=shutdownbutton)
midi_thread.start()
    
"""MAIN SCRIPT"""
while stop_flag:
#for i in range(1):
    
    #execfile("Media_Project.py")
    execfile("printing.py")
    print " That was open on startup file"
    time.sleep(5)
    print "You will be prompted to choose a new scale"

print "Shutting doooooooooooooooooown"
time.sleep(5)
#shutdown()

