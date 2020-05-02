import numpy.random as np #Random samples generator
import numpy
import random

#Parameters of the gaussian that generates data for Overhead Power Line
OPL_Mean=50
OPL_StdDev=4
situation=2
#Parameters for the gaussian that generates abnormal data
Abnormal_Mean=10.0
Abnormal_StdDev=1

#Size of the vector that will be used to store data on Arduino EEPROM (1 kb of data)
vectorSize=500

#Starting to create the Arduino code
print("#include<EEPROM.h>")
print("int EEPROM_Address = 0;/*Variable to store the address of EEPROM*/")
print("void setup() {")
print("pinMode(LED_BUILTIN, OUTPUT);")

print("  for (EEPROM_Address = 0; EEPROM_Address < EEPROM.length() ; EEPROM_Address++) {")
print("		/* This for-block is used clean the EEPROM: it stores zeros on all EEPROM memory positions */")
print("		EEPROM.write(EEPROM_Address, 0);")
print("	}")
print("EEPROM_Address = 0;/*Reseting to zero the address of EEPROM*/")
print("digitalWrite(LED_BUILTIN, HIGH);")

print('int data[500]={'),
#Printing the vector

for x in range(0, vectorSize):
	if(situation==1):
		
		print(int(numpy.random.normal(92,18))),
	elif(situation==2):
		
		print(int(numpy.random.normal(92,18))),
	elif(situation==3):
		
		print(int(numpy.random.normal(155,2))),
	elif(situation==4):
		
		print(int(numpy.random.normal(155,2))),


	if(x == 499):
		print('};'),
	else:
		print(','),

print('')

print("delay(1000);");
print("for (EEPROM_Address = 0; EEPROM_Address < 500 ; EEPROM_Address++) {")
print("   /* This for-block is used clean the EEPROM: it stores zeros on all EEPROM memory positions */")
print("   EEPROM.write(EEPROM_Address, data[EEPROM_Address]);")
print("  }")
print("digitalWrite(LED_BUILTIN, LOW);")
print("}")
print("")
print("void loop() {}")

