
tempo = [113, 111, 110, 110, 110, 109, 108, 110, 110, 111, 110, 113]
saved_tempo= [tempo[0]]
doubtful_tempo = [0]
ave_saved_tempo = sum(saved_tempo) / len(saved_tempo)
print ave_saved_tempo


for i in tempo:
    if  ave_saved_tempo -2 <= tempo[i] <= ave_saved_tempo +2:  
        saved_tempo.append(tempo[i])
        doubtful_tempo = [tempo[i]]
        #clock_interval = update_tempo(ave_saved_tempo)
        print 'clock_interval is equivalent to:', tempo[i]
    else:
        doubtful_tempo.append(tempo[i])
        if doubtful_tempo[0] -2 <= doubtful_tempo[1] <= doubtful_tempo[0] +2:
            ''' send it,reset saved_tempo and copy doubtful_tempo[1] to it , 
                 reset doubtful_tempo and save it to saved_tempo'''
            #clock_interval = update_tempo(doubtful_tempo[1])
            saved_tempo = [doubtful_tempo[1]]
            doubtful_tempo = [0]

