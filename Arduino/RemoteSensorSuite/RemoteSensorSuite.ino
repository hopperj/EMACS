#include <Wire.h>
#include <Adafruit_MPL115A2.h> //MPL115A2 library (pressure, temp)
#include <SHT1x.h> //SHT15 library (humidity, temp)
#include <SoftwareSerial.h>
#include <stdlib.h>

#define dataPin 4 //SHT1x serial data pin
#define clockPin 5 //SHT1x serial clock pin
SHT1x sht1x(dataPin, clockPin);
Adafruit_MPL115A2 mpl115a2; //MPL115A2 object
SoftwareSerial mySerial(9,10); //RX, TX for software serial comms to XBEE

void setup() {
  Serial.begin(57600); // open serial comes to host through USB
  Serial.println("Serial Coms Open...");
  mpl115a2.begin(); // Start MPL115a2 transmitting data 
  mySerial.begin(9600); //Comms to XBEE
}

void loop() {

  float temp_c_SHT; //SHT1x temperature
  float temp_c_mpl; //MPL115a2 temperature
  float humidity; //humidity from SHT15
  float pressure; // pressure from MPL115a2
  char device_id[8] = "Remote1";
  static char outstr[15];
  
  while(1) {
    //SHT15 readings
    temp_c_SHT = sht1x.readTemperatureC();
    humidity = sht1x.readHumidity();
    
    //MPL115A2 readings
    temp_c_mpl = mpl115a2.getTemperature();
    pressure = mpl115a2.getPressure();
    // Send data along USB through serial for local monitoring
    Serial.print(temp_c_mpl,2); Serial.print(" ");Serial.print(temp_c_SHT,2);Serial.print(" ");Serial.print(humidity, 2);Serial.print(" ");Serial.println(pressure);
    
    //Send all collected data along XBEE. Comma delimited string with identifier for each variable. 
    mySerial.write(device_id);
    mySerial.write(",");
    mySerial.write("temp");
    mySerial.write(",");
    dtostrf((temp_c_SHT+temp_c_mpl)/2.0, 6, 3, outstr);
    mySerial.write(outstr);
    mySerial.write(",");
    mySerial.write("humidity");
    mySerial.write(",");
    dtostrf(humidity, 6, 3, outstr);
    mySerial.write(outstr);
    mySerial.write(",");
    mySerial.write("pressure");
    mySerial.write(",");
    dtostrf(pressure, 7, 3, outstr);
    mySerial.write(outstr);
    mySerial.write("\r\n");
    delay(1000);
  }
 
}
