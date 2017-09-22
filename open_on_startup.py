#import os 
#os.system('printing.py')
import time


def shutdown():
    command = "/usr/bin/sudo /sbin/shutdown -h now"
    import subprocess
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    output = process.communicate()[0]
    print output
 
print "Pi will shutdown, you have 5 seconds to  ctrl+c"
time.sleep(5)
#shutdown()
    
#while True:
    execfile("Media_Project.py")
    #execfile("printing.py")
    print " That was open on startup file"
    time.sleep(5)
    print "You will be prompted to choose a new scale"


