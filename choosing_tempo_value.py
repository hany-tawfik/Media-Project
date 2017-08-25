#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 25 14:43:13 2017

@author: HanyTawfik
"""


tempo = [110, 111, 110, 113, 110, 109, 108, 110, 60, 110, 111, 150, 110, 113, 50, 48, 100, 51, 51, 51, 51, 51, 51, 51, 51, 51, 51, 100, 51, 51, 51, 51, 51, 100, 51, 51, 51, 51, 51, 51, 51, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80]
saved_tempo= [tempo[0]]
doubtful_tempo = [0]
ave_saved_tempo = sum(saved_tempo) / len(saved_tempo)
#saved_tempo= []


for i in range(len(tempo)):
    
    if  ave_saved_tempo -3 <= tempo[i] <= ave_saved_tempo +3:  
        saved_tempo.append(tempo[i])
        ave_saved_tempo = sum(saved_tempo) / len(saved_tempo)
        doubtful_tempo=[0]
        
        if len(saved_tempo) >= 5:
            del saved_tempo[0]
        #clock_interval = update_tempo(ave_saved_tempo)
        #print 'Tempo detected:', tempo[i]
        print 'Tempo sent:', ave_saved_tempo, " \n"
        #print 'saved_tempo:' , saved_tempo, 
        #print 'sum of saved tempo:' , sum(saved_tempo), " \n"
        
    else:
        
        doubtful_tempo.append(tempo[i])
        print "doubtful_tempo:", doubtful_tempo
        
        
        if doubtful_tempo[len(doubtful_tempo)-2] -3 <= doubtful_tempo[len(doubtful_tempo)-1] <= doubtful_tempo[len(doubtful_tempo)-2] +3:
            print " there is a tempo change to", doubtful_tempo[len(doubtful_tempo)-1]
            # send it,reset saved_tempo and copy doubtful_tempo[1] to it , 
            # reset doubtful_tempo and save it to saved_tempo

            #clock_interval = update_tempo(len(doubtful_tempo)-1)
            saved_tempo = [doubtful_tempo[len(doubtful_tempo)-1]]
            ave_saved_tempo = sum(saved_tempo) / len(saved_tempo)
            print 'saved_tempo', saved_tempo, "\n"


'''       
if tempo1 > tempo2:
   if prob1 - prob2 >= 2:
       new_tempo = tempo1
else:
    if prob1 
'''
    
