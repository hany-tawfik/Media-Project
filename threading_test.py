import threading
import time
def non_daemon():
    time.sleep(5)
    print 'Test non-daemon'

t = threading.Thread(name='non-daemon', target=non_daemon)

t.start()
print 'Test one'
t.join()
print 'Test two'
