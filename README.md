# Lab_4
ME405 Lab 4

This code multitasks cooperatively and demonstrates that by running 2 motor controllers simultaneously while allowing test code to change the gain or desired location of either one without interrrupting the motion of the other.

Changing the multitasking code to run too slowly results in a less stable control system response as seen in the following step response plots.

Step Response at Task Period of 15ms:

![image](https://github.com/JoshuaTuttobene/Lab_4/assets/107731390/337aed52-4fca-443a-b4fa-6f1faad29c16)


Step Response at Task Period of 30ms:

![image](https://github.com/JoshuaTuttobene/Lab_4/assets/107731390/b8e40741-e157-43f6-b62f-ce363dafc788)


We recommend running the tasks at a period of 15ms or quicker to get smooth control on the motor.
