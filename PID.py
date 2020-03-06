#!/usr/bin/python

#######################################################################
#####                                                             #####
#####                     Jeferson S. Pazze                       #####
#####                 jeferson.pazze@edu.pucrs.br                 #####
#####                        10/01/2019                           #####
#####                           PID                               #####
#####                                                             #####
#######################################################################

import spidev
import time
import random
import RPi.GPIO as GPIO

from datetime import date

P    = 0
I    = 0
D    = 0
PID  = 0

erro = 0.05
tempo_decorrido = 0
current_time = None

def PID_control(Temperatura_interna, setpoint, hoje, last_time, current_time = None):
  
  KP   = 13.8
  KI   = 4
  KD   = 1

  erro = setpoint - Temperatura_interna

  ## CONTROLE PROPORCIONAL
  P = KP*erro

  total_secs = round(hoje.second - last_time)
  sample_time = 0.00
  
  current_time = current_time if current_time is not None else hoje.second#time.time()
  last_time = current_time%60

  ## CONTROLE INTEGRAL
  I = (KI*erro)*2

  ## CONTROLE DERIVATIVO
  D = (erro*KD)/2

  #PID
  PID = P+I+D
  print("PID: " , PID)

  if(PID>0):
    
    GPIO.output(31,0)
    
  else:
    GPIO.output(31,1)

print('PID inicialized')

