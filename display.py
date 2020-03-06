#######################################################################
#####                                                             #####
#####                     Jeferson S. Pazze                       #####
#####                 jeferson.pazze@edu.pucrs.br                 #####
#####                        10/01/2019                           #####
#####                          Display                            #####
#####                                                             #####
#######################################################################

#!/usr/bin/python
# Example using a character LCD connected to a Raspberry Pi
import time
import Adafruit_CharLCD as LCD

# Raspberry Pi pin setup
lcd_rs = 4
lcd_en = 27
lcd_d4 = 21
lcd_d5 = 20
lcd_d6 = 16
lcd_d7 = 12
lcd_backlight = 2

# Define LCD column and row size for 16x2 LCD.
lcd_columns = 8
lcd_rows = 2

lcd = LCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns, lcd_rows, lcd_backlight)

lcd.message('WELCOME!')
time.sleep(2.0)
lcd.clear()

lcd.message('GOOD \n   TREE!')
time.sleep(2.0)
lcd.clear()

lcd.message('GOODBYE!')
time.sleep(2.0)
lcd.clear()

print("inicializou display")

def display(ppm, Temperatura_fluido, humidity, Temperatura_interna):
    #lcd = LCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns, lcd_rows, lcd_backlight)
    lcd.clear()
    lcd.message('Hello\ndisp!')
    time.sleep(2.0)
    


    
    
