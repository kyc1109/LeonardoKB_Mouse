#!/usr/bin/python3
#coding=utf-8
import serial #pip3 install pyserial for win
import datetime
import queue
import os
import sys
import time
#Pi Pin 8,10,14, Arduino Leonardo 0,1 5V, GND
class com:
    q=queue.Queue()
    s_key={"KEY_LEFT_CTRL":b"\x80",
        "KEY_LEFT_ALT":b"\x82",
        "KEY_LEFT_GUI":b"\x83", #Win key
        "KEY_RETURN":b"\xB0", #Enter key
        "KEY_ESC":b"\xB1",
    def __init__(self):
        # Initail
        self.logfile="ttyS0.txt" #for debug=
        if os.path.exists(self.logfile):
            os.system("rm "+self.logfile)
        #os.system("ls "+com)                            
        #com='/dev/serial0' # for linux. /dev/ttyUSB0, /dev/ttyS0 or /dev/serial0
        try:
            #os.system("ls /dev/ttyUSB*")
            self.port = str(input("\nWhich one COM port? just input the number of port. ex: 7 or 20: ") or 0)            
            #self.port = "3"
            self.baudrate = 9600 #115200
            self.bytesize = serial.EIGHTBITS #number of bits per bytes
            self.parity = serial.PARITY_NONE #set parity check
            self.stopbits = serial.STOPBITS_ONE #number of stop bits
            self.timeout = 0.5          #non-block read 0.5s
            self.writeTimeout = 0.5     #timeout for write 0.5s
            self.xonxoff = False    #disable software flow control
            self.rtscts = False     #disable hardware (RTS/CTS) flow control
            self.dsrdtr = False     #disable hardware (DSR/DTR) flow control        
            self.ser = serial.Serial("COM"+str(self.port), self.baudrate, self.bytesize, self.parity, self.stopbits, self.timeout, self.xonxoff, self.rtscts)        
            #ser = serial.Serial(com, 9600, timeout=2) #115200, 9600
            if self.ser.isOpen():
                print("Reading...")
                read_data=self.ser.readline().decode('utf-8').rstrip()
                print(read_data)
        except Exception as e:
            print("Init fail:", e)
    def __del__(self):
        self.ser.close()
    def special_key(self,key):
        if self.s_key.get(key): #KEY_LEFT_CTRL
            cmd=self.s_key[key]
            print("special_key", cmd)
            self.ser.write(cmd)
            return True
        else:    
            return False
    def delay_check(self,str_send): #delay by send lengh
        len_str=len(str_send)
        sec= len_str /30 #float, 30 per sec is ok.
        print("delay "+str(sec)+"sec")
        time.sleep(sec)

    def pi_com(self):
        while True:
            cmd = input("\nCmd input:")
            if self.special_key(cmd):
                pass
            else:
                self.ser.write(cmd.encode())
            com_read = self.ser.readline().decode("utf-8", 'ignore')
            print("Input:",cmd)
            if len(com_read) >0:
                logtxt = str("echo "+str(datetime.datetime.now())+", "+com_read.replace("\r\n","")+" >>"+self.logfile)
                print(logtxt)
                os.system(logtxt)
            self.ser.flush()
        #self.ser.close()        
    
    def kbWrite(self,str_send): #v1
        #cmd = input("\nCmd input:")
        if self.special_key(str_send): #is special key
            pass
        else:
            self.ser.write(str_send.encode()) #is string
        com_read = self.ser.readline().decode("utf-8", 'ignore') #feedback
        print("\nInput("+str(len(str_send))+"):", str_send) #show input
        if len(com_read) >0:
            logtxt = str("echo "+str(datetime.datetime.now())+", "+com_read.replace("\r\n","")+" >>"+self.logfile)
            #print(logtxt)
            os.system(logtxt)
        print(self.ser.readline().decode("utf-8", 'ignore'))            
        time.sleep(1.2) #delay 1.2s is the best fast.
        ser.flush()
        #ser.close()
        
    def kbWrite2(self,str_send): #current used. v2
        if self.special_key(str_send): #is special key
            pass
        elif isinstance(str_send,int): #is int
            self.ser.write(str_send) 
            str_send=str(str_send)
        else:
            self.ser.write(str_send.encode()) #string to byte
        com_read = self.ser.readline().decode("utf-8", 'ignore') #feedback
        print("\nInput("+str(len(str_send))+"):", str_send) #show input
        if len(com_read) >0:
            logtxt = str("echo "+str(datetime.datetime.now())+", "+com_read.replace("\r\n","")+" >>"+self.logfile)
        self.delay_check(str_send) #wait USB output
        self.ser.flush()
        
    def run_kb(self,send_key):
        self.q.put(send_key) #add queue to avoid interrupt
        while not self.q.empty():
            self.kbWrite2(self.q.get())

    def read(self):
        read_data=self.ser.readline().decode('utf-8').rstrip()
        print(read_data) #remove b"" by utf-8, remove newline by restrip()        
        self.kbWrite2("str")

    def test_str(self): #OK
        self.ser.write(b"\xF1\x31\x00\x00") #1
        time.sleep(1)
        self.ser.write(b"\xF1\x41\x00\x00") #A
        #self.run_kb("A") #
        time.sleep(1)
        self.ser.write(b"\xF1\x83\x00\x00") # win 
        time.sleep(1)
        self.ser.write(b"\xF1\x83\x00\x00") #win
           
    def test_cmd(self): #OK
        self.ser.write(b"\xF3\x80\x00\x00") #F3 press  
        self.ser.write(b"\xF3\x82\x00\x00") #F3 press
        self.ser.write(b"\xF3\xD4\x00\x00") #F3 press
        self.ser.write(b"\xF4\xD4\x00\x00") #F4 release

    def test_power(self): #OK
        self.ser.write(b"\xF2\x0A\x00\x00") #delay 9s. 0x0A=10s

    def test_mos(self): #OK. sign int. >0x80 is -x,-y, <0x80 is x,y 
        self.ser.write(b"\xF5\x70\x70\x00") # move
        self.ser.write(b"\xF6\x00\x80\x00") # MOUSE_LEFT 
        self.ser.write(b"\xF6\x01\x80\x00") # MOUSE_RIGHT
        
    def test_sel_item(self):
        print(self.ser.readline()) #remove b"" by utf-8, remove newline by restrip()         
        sel = input("\nCmd input: s,c,p,m: ")or "1"
        if sel == "1" or sel.lower() == "s":
            self.test_str()
        elif sel == "2"or sel.lower() == "c":
            self.test_cmd()
        elif sel == "3"or sel.lower() == "p":
            self.test_power()
        elif sel == "4"or sel.lower() == "m":
            self.test_mos()
        else:
            print(sel)   
        self.ser.flush() #remove buffer
        self.test_sel_item()
if __name__ == '__main__':
    os.system('mode con: cols=80 lines=12')
    pi = com()
    pi.test_sel_item()
    pi.ser.close() 
