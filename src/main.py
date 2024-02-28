"""!
@file basic_tasks.py
    This file contains a demonstration program that runs some tasks, an
    inter-task shared variable, and a queue. The tasks don't really @b do
    anything; the example just shows how these elements are created and run.

@author JR Ridgely
@date   2021-Dec-15 JRR Created from the remains of previous example
@copyright (c) 2015-2021 by JR Ridgely and released under the GNU
    Public License, Version 2. 
"""

import gc
import pyb
import cotask
import task_share

import motor_driver as MD
import encoder_reader as ER
import CL_Proportional_Control as CLPC
import utime
import cqueue
import pyb


def task1_fun(shares):
    """!
    Task which puts things into a share and a queue.
    @param shares A list holding the share and queue used by this task
    """
    init = utime.ticks_ms()
    while True:
        if time.full() == False:
            pwm = CL.run(encoder.read())  # set return from controller as pwm for motor
            time.put(utime.ticks_ms()-init)   # put time into queue
            pos.put(encoder.read())          # put position into queue
            motor.set_duty_cycle(pwm)     # set new pwm
        else:
            motor.disable()
            break
        yield
    return
            
#     # Get references to the share and queue which have been passed to this task
#     my_share, my_queue = shares
# 
#     counter = 0
#     while True:
#         my_share.put(counter)
#         my_queue.put(counter)
#         counter += 1
# 
    


def task2_fun(shares):
    """!
    Task which takes things out of a queue and share and displays them.
    @param shares A tuple of a share and queue from which this task gets data
    """
    init_2 = utime.ticks_ms()
    while True:
        if time_2.full() == False:
            pwm = CL_2.run(encoder_2.read())  # set return from controller as pwm for motor
            time_2.put(utime.ticks_ms()-init_2)   # put time into queue
            pos_2.put(encoder_2.read())          # put position into queue
            motor_2.set_duty_cycle(pwm)     # set new pwm
        else:
            motor_2.disable()
            break
        yield
    return

# This code creates a share, a queue, and two tasks, then starts the tasks. The
# tasks run until somebody presses ENTER, at which time the scheduler stops and
# printouts show diagnostic information about the tasks, share, and queue.
#if __name__ == "__main__":
print("Testing ME405 stuff in cotask.py and task_share.py\r\n"
      "Press Ctrl-C to stop and show diagnostics.")

# init queue
time = cqueue.FloatQueue(250)
pos = cqueue.FloatQueue(250)

# second init queue
time_2 = cqueue.FloatQueue(250)
pos_2 = cqueue.FloatQueue(250)

print('queue intialized')

# Motor init
enable_pin = pyb.Pin(pyb.Pin.board.PA10, pyb.Pin.OUT_PP)
in1pin = pyb.Pin.cpu.B4
in2pin = pyb.Pin.cpu.B5
tim3 = pyb.Timer(3, freq=20000)
motor = MD.MotorDriver(enable_pin, in1pin, in2pin, tim3)
motor.enable()

# Motor init 2
enable_pin_2 = pyb.Pin(pyb.Pin.board.PC1, pyb.Pin.OUT_PP)
in1pin_2 = pyb.Pin.cpu.A0
in2pin_2 = pyb.Pin.cpu.A1
tim5 = pyb.Timer(5, freq=20000)
motor_2 = MD.MotorDriver(enable_pin_2, in1pin_2, in2pin_2, tim5)
motor_2.enable()
print('motors initialized')

# Encoder init
pin_A = pyb.Pin.cpu.C6
pin_B = pyb.Pin.cpu.C7
tim8 = pyb.Timer(8, prescaler = 0, period = 2**16-1)
encoder = ER.Encoder(pin_A, pin_B, tim8)

# Encoder init 2
pin_A = pyb.Pin.cpu.B6
pin_B = pyb.Pin.cpu.B7
tim4 = pyb.Timer(4, prescaler = 0, period = 2**16-1)
encoder_2 = ER.Encoder(pin_A, pin_B, tim4)
print('encoder intialized')

# run for 1
kp = float(input("Enter a Kp value for 1:"))  # input for Kp
CL = CLPC.ClosedLoop_P(kp,50000) # use small Kp
encoder.zero()  # zero encoder before using


# run for 2
kp_2 = float(input("Enter a Kp value for 2:"))  # input for Kp
CL_2 = CLPC.ClosedLoop_P(kp_2,50000) # use small Kp
encoder_2.zero()  # zero encoder before using

print('kps set')

# Create a share and a queue to test function and diagnostic printouts
share0 = task_share.Share('h', thread_protect=False, name="Share 0")
q0 = task_share.Queue('L', 16, thread_protect=False, overwrite=False,
                      name="Queue 0")

# Create the tasks. If trace is enabled for any task, memory will be
# allocated for state transition tracing, and the application will run out
# of memory after a while and quit. Therefore, use tracing only for 
# debugging and set trace to False when it's not needed
task1 = cotask.Task(task1_fun, name="Task_1", priority=1, period=15,
                    profile=True, trace=False, shares=(share0, q0))
task2 = cotask.Task(task2_fun, name="Task_2", priority=1, period=15,
                    profile=True, trace=False, shares=(share0, q0))
cotask.task_list.append(task1)
cotask.task_list.append(task2)

# Run the memory garbage collector to ensure memory is as defragmented as
# possible before the real-time scheduler is started
gc.collect()

# Run the scheduler with the chosen scheduling algorithm. Quit if ^C pressed
while True:
    #try:
    if not time.full() == True:
        cotask.task_list.pri_sched()
    else:
    #except KeyboardInterrupt:
        break
motor.disable()
motor_2.disable()
# Print a table of task data and a table of shared information data
while True:  # for loop to print and empty queue
    print(f"{time.get()}, {pos.get()}")
    if time.any() == False:
        print("end")     # print end to indicate completion of data
        motor.disable()   # turn off motor once data has been collected
        break
while True:
    print(f"{time_2.get()}, {pos_2.get()}")
    if time_2.any() == False:
        print("end")     # print end to indicate completion of data
        motor_2.disable() # turn off motor once data has been collected
        break

print('\n' + str (cotask.task_list))
print(task_share.show_all())
print(task1.get_trace())
print('')

