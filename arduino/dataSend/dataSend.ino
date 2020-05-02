#include<EEPROM.h>

#define quantity_of_samples_in_EEPROM 499

#define node_id 0xF2 //Id of the node
#define tdma_window 100 //time of tdma window in miliseconds
#define quantity_of_nodes_in_tdma 4

/*
 * tdma scheme: 3 CN and 1 FN (4 nodes in total)
 * Each node has the time in tdma_window to process Hygiea and send the message
 * IDs of the CN: 0xF1, 0xF2, 0XF3
 * ID of the FN: 0xF0
 * Broadcast ID: 0xFF
 */

int EEPROM_Address = 0;
int datum;

void setup() {
  //Serial.begin(9600);
  Serial.begin(9600);
  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN, LOW);
  }

void loop() {

  //This switch statement is to define TDMA window based on node ID
  //The TDMA sequence is 
  //CN1 (id 0xF1), CN2 (id 0xF2), CN3 (id 0xF3) and FN (id 0xF0)
  switch(node_id){
    case 0xF1 :
      break;
    case 0xF2 :
      delay(tdma_window*1);
      break;
    case 0xF3 :
      delay(tdma_window*2);
      break;
    }

   //It doesnt receive data from serial, hence it should clean the received data
   //if it does no clean the serial, the serial buffer will increase until fill up
   while(Serial.available()){Serial.read();}

  //Turn on the Builtin led to inform 
  //it is operating in its desired TDMA slot  
  digitalWrite(LED_BUILTIN, HIGH);

  
  //Gets a datum from EEPROM and store it on RSW
  int Datum = EEPROM.read(EEPROM_Address);


    
  //Updates the EEPROM index  

  EEPROM_Address = EEPROM_Address + 1;
   
  Serial.write(Datum);




   
 

  //Turn off the buitin led to inform it is waiting
  digitalWrite(LED_BUILTIN, LOW);

  //This switch statement is to define TDMA window based on node ID
  //The TDMA sequence is 
  //CN1 (id 0xF1), CN2 (id 0xF2), CN3 (id 0xF3) and FN (id 0xF0)
  switch(node_id){
    case 0xF1 :
      delay(tdma_window*3);
      break;
    case 0xF2 :
      delay(tdma_window*2);
      break;
    case 0xF3 :
      delay(tdma_window*1);
      break;
    }




  if (EEPROM_Address == (quantity_of_samples_in_EEPROM + 1)) {
    //while(true){}
    EEPROM_Address = 0;
  }

}
