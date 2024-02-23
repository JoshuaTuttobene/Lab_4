"""!
@file lab3_step_response.py
Run a motor step response based on a user inputted Kp. This program cals the
microcontroller to run and get data before plotting the closed loop PController step response.
It uses Tkinter, an old-fashioned and ugly but useful GUI library which is included in Python by
default.

This file is based loosely on an example found at
https://matplotlib.org/stable/gallery/user_interfaces/embedding_in_tk_sgskip.html

@author Aaron Escamilla, Karen Morales De Leon, Joshua Tuttobene
@date   02/22/2024 Original program, based on example from above listed source
@copyright (c) 2023 by Spluttflob and released under the GNU Public Licenes V3
"""

import time
import tkinter
import serial
import matplotlib.pyplot as plt

# Creating serial to read port
ser = serial.Serial('COM3')
ser.baudrate = 115200
ser.bytsize = 8
ser.parity = 'N'
ser.stopbits = 1
ser.timeout = 8

ser.write(b'\x04') # send ctrl-D to the serial port

time.sleep(5)
# Create empty arrays to append data from microcontroller
t_data = []
p_data = []
 # Takes user input and then sends to microcontrollerser.write(input("Enter a Kp value:").encode('ascii'))
ser.write(input("Enter a Kp value:").encode('ascii'))
ser.write(b'\r')
time.sleep(5) # sleep to give the motor time to perform response

# loop to get data from serial port until 'end' is printed, signifying the end of data
for line in range(1000):
    try:
        ser.write(b'\x02') # need, dont delete, swith out of raw-REPL mode
        pos = ser.readline().decode('utf-8')
        if not pos == 'end':
            pos = pos.split(',')
            t = float(''.join(pos[0:1]))
            p = float(''.join(pos[1:2]))
            # Append data by adding to end in array
            t_data.append(t)
            p_data.append(p)
        else:
            break

    except ValueError:     # anything that is not a data entry don't show
        #print('invalid entry')
        pass
print(p_data)   
# Draw the plot from the measured data 
plt.plot(t_data,p_data,'.', markersize=4)
plt.xlabel('Time (ms)')
plt.ylabel('Encoder Position')
plt.xlim(0, 1500)
plt.grid(True)
plt.show()