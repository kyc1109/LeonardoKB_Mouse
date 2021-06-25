# LeonardoKB_Mouse
This repo. is serial communication between PC and Arduino, that can remote control PC by vertual KB/Mouse with Arduino Leonardo.

Pi <--GPIO--> Leonardo <--USB--> PC (remote side)

or

PC <--USB to UART--> Leonardo <--USB--> PC (remote side)

send_cmd.py is run on control side.
Leonado_Serial.ino is write on Arduino Leonardo.


