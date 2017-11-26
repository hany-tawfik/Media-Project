import time
import mido
import threading

def shutdownbutton():
    global stop_flag_startup
    print "thread started"
    for msg in inport:
        
        if msg.note == Stop_loop_startup.note:            
            inport.close()
            print "Shutting down in 5 seconds"
            print msg
            #time.sleep(3)
            stop_flag_startup = False
            break
            
def setup_chords_startup(note):
    """this bypass the last saved midi value """
    global Stop_loop_startup
    if note != Stop_loop_startup.note:
        return True
    else:
        return False
    
def shutdown():
    command = "/usr/bin/sudo /sbin/shutdown -h now"
    import subprocess
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    output = process.communicate()[0]
    print output
 

if __name__ == "__main__":

    '''MIDI INPUT PORTS SETUP'''
    inputs = mido.get_input_names()
    midi_start25 = inputs[1].encode('ascii')
    inport = mido.open_input(midi_start25)
    Stop_loop_startup = mido.Message('note_on', note=84) #C6
    stop_flag_startup = True
    note_startup = inport.receive()
    Tonic_startup = note_startup.copy()

    while True:
            if setup_chords_startup(Tonic_startup.note):
                break
            else:
                msg = inport.receive()
                break

    """ MIDI THREAD"""

    midi_thread = threading.Thread(target=shutdownbutton)
    midi_thread.start()


    while stop_flag_startup: 
        execfile("Media_Project.py")
        #execfile("printing.py")
        print "stop_flag_startup: ", stop_flag_startup
        time.sleep(3)



    print "shutting down"
    time.sleep(2)
    #shutdown()
