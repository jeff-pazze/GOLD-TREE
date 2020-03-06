#!/usr/bin/python

#######################################################################
#####                                                             #####
#####                     Jeferson S. Pazze                       #####
#####                 jeferson.pazze@edu.pucrs.br                 #####
#####                        10/01/2019                           #####
#####                           MAIN                              #####
#####                                                             #####
#######################################################################
 
import spidev
import time
import os
import math
import sys
import subprocess
import Adafruit_DHT
import RPi.GPIO as GPIO
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random
import signal
#import Adafruit_CharLCD as LCD

from datetime import date
from datetime import date, datetime
from time import sleep
from control import *
from grafico import *
from PID import *

#from display2 import *

# Define sensor channels
channel_0 = 0
channel_1 = 1
channel_2 = 2
channel_3 = 3
channel_4 = 4
channel_5 = 5
channel_6 = 6
channel_7 = 7

lcd_rs = 4
lcd_en = 27
lcd_d4 = 21
lcd_d5 = 20
lcd_d6 = 16
lcd_d7 = 12
lcd_backlight = 2

delay = 2

atual = date.today()

print('Data:' , atual)

hoje = datetime.now()

hoje.day
hoje.month
hoje.year

print (hoje.hour)
print (hoje.minute)
print (hoje.second)

last_time = hoje.second

GPIO.setmode(GPIO.BOARD)
GPIO.setup(31, GPIO.OUT)
GPIO.setup(33, GPIO.OUT)
GPIO.setup(35, GPIO.OUT)
GPIO.setup(37, GPIO.OUT)
time.sleep(1)

GPIO.output(31,1)
time.sleep(1)
GPIO.output(33,1)
time.sleep(1)
GPIO.output(35,1)
time.sleep(1)
GPIO.output(37,1)
time.sleep(1)

sensor = Adafruit_DHT.DHT11
gpio = 17
humidity, temperature = Adafruit_DHT.read_retry(sensor, gpio)

# Open SPI bus
spi = spidev.SpiDev()
spi.open(0,0)
spi.max_speed_hz= 115200
 
def ReadChannel(channel):
  
  adc = spi.xfer2([1,(8+channel)<<4,0])
  data = ((adc[1]&3) << 8) + adc[2]
  
  return data
 
def ConvertVolts(data,places):
  
  volts = (data * 5) / float(1023)
  volts = round(volts,places)
  
  return volts
 
def ConvertTemp(data,places):

  temp = (((data * 5)/float(1023))/0.01)-2 # 5V ref
  #5000mV/1023 = 4,88 mV/AD ... = 5000mV/10mV/C = 500
  temp = round(temp,places)
  
  return temp

plt.ion()


RO = 250 #resistencia 2.5k
coefficient_a = 22.345
coefficient_b = -0.67

contador = 0

'''
Function is used to return the ppm value of CO2 gas concentration
by using the parameter found using the function f(x) = a * ((Rs/R0) ^ b)

getPPM() =  (coefficient_A * pow(getRatio(), coefficient_B));
'''
 
while True:

  print("\n")

  print ('Temp: {0:0.1f} C  Humidity: {1:0.1f} %'.format(temperature, humidity))


  hoje = datetime.now()

  ad_0 =  ReadChannel(channel_0)
  ad_1 =  ReadChannel(channel_1)
  ad_2 =  ReadChannel(channel_2)
  ad_3 =  ReadChannel(channel_3)
  ad_4 =  ReadChannel(channel_4)
  ad_5 =  ReadChannel(channel_5)
  ad_6 =  ReadChannel(channel_6)
  ad_7 =  ReadChannel(channel_7)

  ad0_volts = ConvertVolts(ad_0,2)
  ad1_volts = ConvertVolts(ad_1,2)
  ad2_volts = ConvertVolts(ad_2,2)
  ad3_volts = ConvertVolts(ad_3,2)
  ad4_volts = ConvertVolts(ad_4,2)
  ad5_volts = ConvertVolts(ad_5,2)
  ad6_volts = ConvertVolts(ad_6,2)
  ad7_volts = ConvertVolts(ad_7,2)

  Temperatura_interna = ConvertTemp(ad_3,2)
  Temperatura_fluido  = ConvertTemp(ad_4,2)
  intensidade_luminosa = ad_5

  print("intensidade_luminosa:{}".format(intensidade_luminosa))
  print("Temperatura_interna C º :{}".format(Temperatura_interna))
  print("Temperatura_fluido  C º :{}".format(Temperatura_fluido))


  ostemp = os.popen('vcgencmd measure_temp').readline()
  temp = (ostemp.replace("temp=", "").replace("'C\n", ""))

  '''

  print(temp)
  tempC.append(temp)
  tempC.pop(0)

  '''
  
  tempS.append(Temperatura_interna)
  tempS.pop(0)
  
  tempF.append(Temperatura_fluido)
  tempF.pop(0)
  
  plotNow()
  plt.pause(.001)

  ph = -5.7 * ad0_volts + 21.44
  
  print("ad0 - AD:{} PH:{} Tensao:{}V".format(ad_0 , ph, ad0_volts))

  temp_ph = (3.6/ad1_volts)*25

  print("ad1 - AD:{} Cº{} Tensao:{}V".format(ad_1 , temp_ph,  ad1_volts))

  #RS = RO * (5 - ad2_volts)/ad2_volts
  RS = (5 - ad2_volts)/ad2_volts

  print("RS :{}".format(RS))

  ratio = RS/RO

  print("ratio :{}".format(ratio))

  #ppm = coefficient_a * pow(ratio, coefficient_b)

  coef = ratio/coefficient_a

  print("coef :{}".format(coef))

  ppm = pow((coef), 1/coefficient_b)

  print("ppm :{}".format(ppm))

  print("-------------------------------")
  print("ad0 - AD:{} Tensao:{}V".format(ad_0 , ad0_volts))
  print("ad1 - AD:{} Tensao:{}V".format(ad_1 , ad1_volts))
  print("ad2 - AD:{} Tensao:{}V".format(ad_2 , ad2_volts))
  print("ad3 - AD:{} Tensao:{}V".format(ad_3 , ad3_volts))
  print("ad4 - AD:{} Tensao:{}V".format(ad_4 , ad4_volts))
  print("ad5 - AD:{} Tensao:{}V".format(ad_5 , ad5_volts))
  print("ad6 - AD:{} Tensao:{}V".format(ad_6 , ad6_volts))
  print("ad7 - AD:{} Tensao:{}V".format(ad_7 , ad7_volts))
  print("-------------------------------")
  print("\n")

  if ppm >= 750:

      GPIO.output(35,0)
      print('Exastao Ligada')

  else:
    
      GPIO.output(35,1)
      print('Exastao Desligada')

  if hoje.minute >= 0 and hoje.minute <= 15:
    
      print("RECIRCULAÇÃO LIGADO")
      print("LUZ DESLIGADO")
      GPIO.output(33,1)
      GPIO.output(37,0)

      '''
      for i in range(0, 60):
        sys.stdout.write("{}".format(i))
        sys.stdout.flush()
        time.sleep(1)
        #print ("\nFim")
        #time.sleep(60)
    '''

  elif hoje.minute >= 16 and hoje.minute <= 30:
      #print("laco hora", hoje.minute)
      print("RECIRCULAÇÃO DESLIGADO")
      print("LUZ LIGADO")
      GPIO.output(33,0)
      GPIO.output(37,1)

  elif hoje.minute >= 31 and hoje.minute <= 45:
      #print("laco hora", hoje.minute)
      print("RECIRCULAÇÃO LIGADO")
      print("LUZ DESLIGADO")
      GPIO.output(33,1)
      GPIO.output(37,0)

  elif hoje.minute >= 46 and hoje.minute <= 59:
      #print("laco hora", hoje.minute)
      print("RECIRCULAÇÃO DESLIGADO")
      print("LUZ LIGADO")
      GPIO.output(33,0)
      GPIO.output(37,1)
 
  # Wait before repeating loop
  time.sleep(delay)

  '''

  arquivo.write('\n')
  arquivo.write('Data: ' +str(hoje))
  arquivo.write('\n')
  arquivo.write('T1: ' +str(Temperatura_interna))
  arquivo.write('\n')
  arquivo.write('T2: ' +str(Temperatura_fluido))
  arquivo.write('\n')
  arquivo.write('T3: ' +str(temperature))
  arquivo.write('\n')
  arquivo.write('umidade: ' +str(humidity))
  arquivo.write('\n')
  arquivo.write('ppm: ' +str(ppm))
  arquivo.write('\n')
  arquivo.write('cont: '+str(contador))
  arquivo.write('\n')
  
  arquivo.write('\n')
  arquivo.write('T1: ' +str(Temperatura_interna))
  #arquivo.write('\n')
  #arquivo.write('IL: ' +str(intensidade_luminosa))
  arquivo.write('\n')

  if(contador >150):
    arquivo.close()
    sys.exit()

  contador += 1
  print("contador: ", contador)

  '''

  #display(ppm, Temperatura_fluido, humidity, Temperatura_interna)
 
  print("\n################# PID #################")

  PID_control(Temperatura_interna, setpoint, hoje, last_time, current_time)

  print("################# PID #################")

  sleep(2)





