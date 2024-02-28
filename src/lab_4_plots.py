"""!
@file lab_4_plots.py
Run a motor step response for two motors based on user inputted Kps and setpoints. 
This program calls the microcontroller to run and get get data before plotting 
the closed loop PController step response for both motors.

@author Aaron Escamilla, Karen Morales De Leon, Joshua Tuttobene
@date   02/29/2024 Original program, based on example from above listed source
"""

import serial
import matplotlib.pyplot as plt

# Creating serial to read port
ser = serial.Serial('COM3')
ser.baudrate = 115200
ser.bytsize = 8
ser.parity = 'N'
ser.stopbits = 1
ser.timeout = 8

ser.write(b'\03') # send ctrl-C to serial port to interupt any ongoing processes
ser.write(b'\x04') # send ctrl-D to the serial port to reboot microcontroller
ser.write(b'\02') # send ctrl-B to the serial port to exit raw-repl mode

# Create empty arrays to append data from microcontroller
t_data = []
p_data = []
t2_data = []
p2_data = []

    
 # Takes user input for Kp and setpoint and then sends to microcontroller
while True:
    try:
        kp_1 = input("Enter a Kp_1 value:")
        kp_1_t = float(kp_1)
        if kp_1_t <= 0:
            raise ValueError
        sp_1 = input("Enter setpoint 1:")
        sp_1_t = float(sp_1)
        if sp_1_t <= 0:
            raise ValueError
        kp_2 = input("Enter a Kp_2 value:")
        kp_2_t = float(kp_2)
        if kp_2_t <= 0:
            raise ValueError
        sp_2 = input("Enter setpoint 2:")
        sp_2_t = float(sp_2)
        if sp_2_t <= 0:
            raise ValueError
        break
    except (ValueError, TypeError):
        print('enter a positive numerical value')
ser.write(kp_1.encode('Ascii'))#bytes(kp_1,'utf-8')) # Kp for motor 1
ser.write(b'\r')

ser.write(bytes(sp_1,'utf-8')) # setpoint for motor 1
ser.write(b'\r')

ser.write(bytes(kp_2,'utf-8')) # Kp for motor 2
ser.write(b'\r')

ser.write(bytes(sp_2,'utf-8')) # setpoint for motor 2
ser.write(b'\r')

# loop to get data from serial port for encoder 1 until 'end' is printed, signifying the end of data
while True:
    try:
        pos = ser.readline().decode('utf-8')
        if pos.strip() == 'end':    # if reaches end break out of loop
            break
        pos_s = pos.split(',')
        t = float(''.join(pos_s[0:1]))
        p = float(''.join(pos_s[1:2]))
        # Append data by adding to end in array
        t_data.append(t)
        p_data.append(p)

    except ValueError:     # anything that is not a data entry don't show
        pass
# loop to get data from serial port for encoder 2 until 'end' is printed, signifying the end of data
while True:
    try:
        pos = ser.readline().decode('utf-8')
        if pos.strip() == 'end': # if reaches end break out of loop
            break
        pos_s = pos.split(',')
        t = float(''.join(pos_s[0:1]))
        p = float(''.join(pos_s[1:2]))
        # Append data by adding to end in array
        t2_data.append(t)
        p2_data.append(p)

    except ValueError:     # anything that is not a data entry don't show
        pass
# Draw the plot from the measured data 

plt.plot(t_data,p_data,'+', markersize=4)
plt.plot(t2_data,p2_data,'.', markersize=4)
plt.xlabel('Time (ms)')
plt.ylabel('Encoder Position')
plt.legend(['motor 1', 'motor 2'])
plt.xlim(0, 1200)
plt.grid(True)
plt.show()
ser.write(b'\x03')