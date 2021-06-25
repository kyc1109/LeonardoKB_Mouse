#include "Keyboard.h"
#include "Mouse.h"
/* 4bytes, 
 *  F1=kb
 *  F2=power
 *  F3=press key
 *  F4=release key
 *  F5=mouse
 *  F6=click
 *  Serial.readBytes(buffer, length)
 */
int count = 0;


// the setup function runs once when you press reset or power the board
void setup() {
  // initialize digital pin LED_BUILTIN as an output.
  pinMode(LED_BUILTIN, OUTPUT);
  Serial.begin(9600); //USB
  Serial1.begin(9600); //RxTx
  // initialize mouse control:
  Mouse.begin();
  Keyboard.begin();
  establishContact();  // send a byte to establish contact until receiver responds
}
void establishContact() {
  while (Serial1.available() <= 0) {
    digitalWrite(LED_BUILTIN, HIGH);
    Serial1.print("Leonardo.");   // send an initial string to USB com port
    Serial1.println(random(0,999));
    digitalWrite(LED_BUILTIN, LOW);
    delay(300);
  }
}
void combine_key_CAD(){ // 0xE0 == 224
  Keyboard.press(0x80); //L-Ctrl
  Keyboard.press(0x82); //L-Alt
  Keyboard.press(0xD4); //Del 
  delay(100);
  Keyboard.releaseAll();
}
void mycount() {
  byte i_buffer[] = {}; //reset buffer
  int b_len = 4;    
  if (Serial1.available()) {  // If anything comes in Serial1 (UART). Serial(USB),
    //char USB_read=Serial.read(); //char Serial.read()
    Serial1.readBytes(i_buffer,b_len); //char
    //work start
    digitalWrite(LED_BUILTIN, HIGH);   // turn the LED on (HIGH is the voltage level)
    
    //USB show
    Serial.print(count);
    //Serial.print(" USB Get: ");
    //Serial.print(USB_read,HEX);   //(USB_read,HEX). read it and send it out Serial1 (pins 0 & 1)
    Serial.print(" UART Get: ");
    Serial.print(i_buffer[0]); //(UART_read,HEX)
    Serial.print(i_buffer[1]); //(UART_read,HEX)
    Serial.print(i_buffer[2]); //(UART_read,HEX)
    Serial.println(i_buffer[3]); //(UART_read,HEX)
    /*for debug
    //COM show
    Serial1.print(count);
    Serial1.print(" USB Get: ");
    Serial1.print(USB_read,HEX);   // read it and send it out Serial1 (pins 0 & 1)
    Serial1.print(" UART Get: ");
    Serial1.println(UART_read,HEX);
    */
    //USB keyboard input
    //Keyboard.write(UART_read);
    //s,c,p,m
    if(i_buffer[0]==0xF1){ //OK. s=0x73.str ABCDabcd 
      Serial.println("kb");
      //delay(300);
      char str = i_buffer[1]; //it should be char or byte with 0 not "" for empty.
      Serial.println(str,HEX);        
      Keyboard.write(str);
      
    }else if(i_buffer[0]==0xF3){ //OK. c=0x63.cmd hotkey
      Serial.println("cmd");
      delay(300);
      char cmd=i_buffer[1];
      Serial.println(cmd,HEX);
      Keyboard.press(cmd); //CAD=0x80, 0x82, 0xD4
  
    }else if(i_buffer[0]==0xF4){ //OK. c=0x63.cmd hotkey
      char cmd=i_buffer[1];
      Serial.println("cmd");
      Serial.println(cmd,HEX);
      Keyboard.releaseAll();
        
    }else if(i_buffer[0]==0xF2){ //good. p=0x70. mot time
      Serial.println("power");
      //delay(300);
      int delay_time = int(i_buffer[1])*1000;
      int i = 0;
      Serial.println(i_buffer[1],HEX);   
      Serial.println(int(i_buffer[1]));   
      //Serial.print("before while ");
      //Serial.println(delay_time,HEX);         
      while(i<=(delay_time/1000)){
        digitalWrite(LED_BUILTIN, HIGH);
        delay(900);
        digitalWrite(LED_BUILTIN, LOW);
        delay(100);
        i++;
      }
      //Serial.println(delay_time,HEX);  
      
    }else if(i_buffer[0]==0xF5){ //is work, m = 0x6D. mos x,y 
      int x = int(i_buffer[1]);
      int y = int(i_buffer[2]);
      Serial.println("mos");
      //delay(300);
      //Serial.println(i_buffer[1],HEX);  
      //Serial.println(i_buffer[2],HEX);  
      Serial.print("x:");
      Serial.println(x);
      Serial.print("y:");
      Serial.println(y);
      Mouse.move(x,y); //x,y,wheel, x,y=0~255 byte 
    }else if(i_buffer[0]==0xF6){ //is work
      if(i_buffer[1]==0x00){
        Mouse.click();//MOUSE_LEFT
      }else if (i_buffer[1]==0x01){
        Mouse.click(MOUSE_RIGHT); //MOUSE_RIGHT
      }else{
        ;
      }
     
    }else {
      Serial.println("do nothing");
    }
    
    //work end
    count=count+1;    
    digitalWrite(LED_BUILTIN, LOW);    // turn the LED off by making the voltage LOW  
    //Serial.write("OK"); //tell USB that Leonado is done.
    //Serial1.write("OK"); //tell Pi that Leonado is done.

    //End process.
    Serial1.flush(); //removed any buffered
  }
}

// the loop function runs over and over again forever
void loop(){
  mycount();
}
