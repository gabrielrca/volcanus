#include<EEPROM.h>
int EEPROM_Address = 0;/*Variable to store the address of EEPROM*/
void setup() {
pinMode(LED_BUILTIN, OUTPUT);
  for (EEPROM_Address = 0; EEPROM_Address < EEPROM.length() ; EEPROM_Address++) {
		/* This for-block is used clean the EEPROM: it stores zeros on all EEPROM memory positions */
		EEPROM.write(EEPROM_Address, 0);
	}
EEPROM_Address = 0;/*Reseting to zero the address of EEPROM*/
digitalWrite(LED_BUILTIN, HIGH);
int data[500]={ 69 , 87 , 104 , 112 , 78 , 112 , 116 , 111 , 103 , 59 , 94 , 57 , 98 , 113 , 95 , 98 , 103 , 81 , 138 , 91 , 107 , 117 , 115 , 89 , 114 , 57 , 110 , 96 , 98 , 116 , 77 , 93 , 95 , 117 , 94 , 81 , 58 , 71 , 82 , 81 , 90 , 109 , 65 , 105 , 76 , 60 , 101 , 69 , 96 , 88 , 100 , 90 , 117 , 78 , 104 , 89 , 87 , 58 , 98 , 99 , 120 , 96 , 102 , 77 , 93 , 102 , 82 , 135 , 94 , 77 , 105 , 70 , 110 , 103 , 86 , 57 , 93 , 84 , 116 , 91 , 93 , 55 , 104 , 58 , 113 , 115 , 104 , 91 , 75 , 70 , 99 , 95 , 110 , 95 , 59 , 113 , 96 , 71 , 65 , 98 , 97 , 78 , 73 , 119 , 93 , 103 , 100 , 91 , 117 , 94 , 56 , 91 , 102 , 60 , 103 , 86 , 93 , 106 , 84 , 75 , 85 , 100 , 79 , 87 , 88 , 120 , 71 , 141 , 91 , 93 , 79 , 91 , 61 , 76 , 75 , 94 , 97 , 80 , 113 , 101 , 118 , 95 , 85 , 113 , 103 , 58 , 91 , 120 , 70 , 80 , 95 , 77 , 91 , 78 , 88 , 86 , 124 , 109 , 108 , 101 , 125 , 117 , 70 , 90 , 80 , 103 , 72 , 130 , 83 , 66 , 59 , 103 , 78 , 69 , 108 , 86 , 109 , 91 , 86 , 81 , 99 , 139 , 64 , 101 , 139 , 95 , 127 , 70 , 111 , 107 , 69 , 78 , 82 , 87 , 81 , 121 , 84 , 109 , 112 , 111 , 80 , 93 , 94 , 87 , 100 , 108 , 105 , 103 , 89 , 104 , 59 , 99 , 118 , 70 , 96 , 108 , 77 , 115 , 93 , 84 , 115 , 88 , 90 , 124 , 112 , 109 , 112 , 78 , 76 , 118 , 110 , 116 , 74 , 83 , 97 , 74 , 72 , 95 , 93 , 74 , 74 , 89 , 115 , 104 , 95 , 102 , 69 , 101 , 101 , 67 , 119 , 106 , 120 , 104 , 118 , 90 , 131 , 62 , 97 , 64 , 106 , 75 , 80 , 80 , 129 , 82 , 99 , 62 , 71 , 70 , 69 , 98 , 71 , 66 , 70 , 95 , 101 , 88 , 96 , 93 , 90 , 113 , 78 , 100 , 84 , 91 , 95 , 116 , 100 , 95 , 84 , 77 , 95 , 91 , 112 , 70 , 81 , 88 , 113 , 88 , 71 , 80 , 100 , 88 , 100 , 74 , 79 , 103 , 75 , 115 , 77 , 75 , 61 , 98 , 84 , 98 , 94 , 112 , 91 , 70 , 69 , 59 , 147 , 91 , 89 , 102 , 122 , 90 , 120 , 105 , 82 , 95 , 79 , 131 , 73 , 115 , 72 , 90 , 108 , 102 , 87 , 46 , 83 , 98 , 98 , 118 , 93 , 89 , 96 , 78 , 81 , 108 , 117 , 79 , 77 , 91 , 94 , 73 , 79 , 64 , 81 , 83 , 90 , 59 , 68 , 93 , 93 , 115 , 104 , 74 , 106 , 89 , 139 , 100 , 71 , 106 , 79 , 102 , 65 , 76 , 99 , 107 , 75 , 73 , 131 , 106 , 83 , 89 , 81 , 108 , 81 , 98 , 117 , 76 , 112 , 75 , 84 , 67 , 124 , 95 , 97 , 90 , 100 , 77 , 83 , 76 , 76 , 90 , 85 , 118 , 109 , 92 , 107 , 81 , 67 , 120 , 103 , 98 , 81 , 98 , 83 , 91 , 83 , 73 , 101 , 96 , 125 , 84 , 79 , 89 , 91 , 86 , 97 , 43 , 115 , 140 , 79 , 107 , 105 , 100 , 99 , 76 , 90 , 113 , 90 , 96 , 110 , 87 , 77 , 83 , 61 , 98 , 49 , 69 , 78 , 103 , 52 , 81 , 76 , 98 , 116 , 78 , 55 , 90 , 90 , 75 , 116 , 101 , 92 , 100 , 66 , 83 , 93 , 104 , 95 , 93 , 108 , 97 , 68 , 66 , 109 , 72 , 92 , 48 , 104 , 95 , 91 , 84 , 90 , 83 , 79 , 79 , 83 , 81 , 95 , 100 , 95 , 117 , 126 , 82 }; 
delay(1000);
for (EEPROM_Address = 0; EEPROM_Address < 500 ; EEPROM_Address++) {
   /* This for-block is used clean the EEPROM: it stores zeros on all EEPROM memory positions */
   EEPROM.write(EEPROM_Address, data[EEPROM_Address]);
  }
digitalWrite(LED_BUILTIN, LOW);
}

void loop() {}
