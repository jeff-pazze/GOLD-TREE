#######################################################################
#####                                                             #####
#####                     Jeferson S. Pazze                       #####
#####                 jeferson.pazze@edu.pucrs.br                 #####
#####                        10/01/2019                           #####
#####                          Grafico                            #####
#####                                                             #####
#######################################################################

import matplotlib.pyplot as plt
import numpy as np
import os

x = []
y = []

temperature = []
humidity = []

tempF = []

tempS = []

plt.ion()
cnt=0

def plotNow():
    plt.clf()
    plt.ylim(20,40)
    plt.title('Raspberry Pi core temperture')
    plt.grid(True)
    plt.ylabel('Temp C')
    plt.plot(tempS, 'rx-', label='Degrees C')
    plt.plot(tempF, 'rx-', label='Degrees C')
    plt.legend(loc='upper right')
    plt.plot(tempF)
    plt.plot(tempS)
    plt.show()


#pre-load dummy data
for i in range(0,26):
    tempF.append(0)
    tempS.append(0)


'''
    
while True:
    ostemp = os.popen('vcgencmd measure_temp').readline()
    temp = (ostemp.replace("temp=", "").replace("'C\n", ""))
    print(temp)
    tempC.append(temp)
    tempC.pop(0)
    plotNow()
    plt.pause(.5)
'''

'''

def plotNow(humidity, temperature):
    plt.clf()
    print("tempe funcao :", temperature)
    plt.ylim(0,100)
    plt.xlim(0,10000)
    plt.title('Temperatura_interna')
    plt.grid(True)
    plt.ylabel('Value')
    plt.xlabel('Time(ms)')
    plt.plot(humidity, 'r-', label='humidity')
    plt.plot(temperature, 'b-', label='temperature')
    plt.legend(loc='upper right')
    plt.pause(0.001)
    plt.show()
'''
print('Grafico inicialized')

