

tempo = [100]
saved_tempo= [111,109,108,111,100]
ave_saved_tempo = sum(saved_tempo) / len(saved_tempo)

if  ave_saved_tempo -2 <= tempo[0] <= ave_saved_tempo +2:  
    saved_tempo.append(tempo[0])
    clock_interval = update_tempo(ave_saved_tempo)
    
