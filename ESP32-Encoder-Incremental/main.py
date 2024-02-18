from machine import Pin, I2C
import machine
import time
from machine import I2C, Pin
from rotary_irq_esp import RotaryIRQ
from lcd_api import LcdApi
from pico_i2c_lcd import I2cLcd
        
# Configuracion del LCD
LCD_Addr = 39 #Poner aqui la direccion mediante 12c.scan()
LCD_NUM_ROWS = 2
LCD_NUM_COLS = 16
sda=machine.Pin(21)
scl=machine.Pin(19)
i2c=machine.I2C(0,sda=sda, scl=scl, freq=400000)
lcd = I2cLcd(i2c, LCD_Addr, LCD_NUM_ROWS, LCD_NUM_COLS)        

#Configuracion pines del motor
A = Pin(3, Pin.OUT)
B = Pin(1, Pin.OUT)
C = Pin(22, Pin.OUT)
D = Pin(23, Pin.OUT)

#Funcion que hace girar el motor
def vuelta(n,ms):
    A.value(int(Paso[n][0]))
    B.value(int(Paso[n][1]))
    C.value(int(Paso[n][2]))
    D.value(int(Paso[n][3]))
    time.sleep_ms(ms)

Paso=['1000',
       '0100',
       '0010',
       '0001']

#Configuracion del encoder
Encoder = RotaryIRQ(
       pin_num_clk = 5, 
       pin_num_dt = 17, 
       min_val = 0, 
       max_val = 1,
       reverse = True, 
       range_mode = RotaryIRQ.RANGE_BOUNDED, # RotaryIRQ.RANGE_UNBOUNDED RotaryIRQ.RANGE_WRAP  RotaryIRQ.RANGE_UNBOUNDED
       pull_up = False,
       half_step = False,
       invert = False)

Encoder.set(value = 0, min_val = -30, max_val = 30)

def DesplegarCuenta():
    lcd.clear
    i = Encoder.value()
    speed = 0
    if(i>0):
        ms = 33 - i
        speed = 30/ms
    elif(i<0):
        ms = 33 + i
        speed = -30/ms
        
    speed = "{:.4f}".format(speed)

    vel = str(speed)
    lcd.move_to(0,0)# Coloca el display en la posicion (Columna, Fila)
    lcd.putstr("Velocidad:")
    lcd.move_to(0,1)
    lcd.putstr(vel)
    lcd.putstr(" rpm")
    print(Encoder.value())
    
Encoder.add_listener(DesplegarCuenta)

while 1:
    
    i = Encoder.value()
    
    if(i>0):
        n = 0
        ms = 33 - i
        while(n<4):
            vuelta(n,ms)
            n = n+1
        
    elif(i<0):
        n = 3
        ms = 33 + i
        while(n>-1):
            vuelta(n,ms)
            n = n-1
                   
    

    
