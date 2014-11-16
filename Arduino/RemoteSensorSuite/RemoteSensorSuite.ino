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

//Define Deadzones for the control system
#define DZ_TEMP 0.5
#define DZ_HUMIDITY 5.0

//Define system enumeration (These should be tied to the GPIO)
#define TEMP 0
#define HUMIDITY 1

void setup() 
{
  Serial.begin(57600); // open serial comes to host through USB
  Serial.println("Serial Coms Open...");
  mpl115a2.begin(); // Start MPL115a2 transmitting data 
  mySerial.begin(9600); //Comms to XBEE
  
  //Control Interface (Requires two digital pins)
  //pinMode(TEMP, OUTPUT);
  //digitalWrite(TEMP, LOW);
  //pinMode(HUMIDITY, OUTPUT);
  //digitalWrite(HUMIDITY, LOW);
}
//MAKE STRUCTS OF SENSOR VALUES (Data, Set Point, Control State)

void loop() 
{

  //Measured values from sensor suit
  float temp_c_SHT; //SHT1x temperature
  float temp_c_mpl; //MPL115a2 temperature
  float temp; //Averaged temperature (Celcius)
  float humidity; //humidity from SHT15 (Realtive %)
  float pressure; // pressure from MPL115a2 (kPa)
//  bool  light; // Light measurement (binary)
  
  //Manufacturer values
  char device_id[8] = "H43B01";
  char request = 'A';
  
  //Poll the sensors once to set the default sensor values
  //Default values for control software
  float temp_set;
  float humidity_set; 
//  bool  light_set;
  
  temp_c_SHT = sht1x.readTemperatureC();
  temp_c_mpl = mpl115a2.getTemperature();
  
  humidity_set = sht1x.readHumidity();
  temp_set = (temp_c_SHT+temp_c_mpl)/2.0;
//  light_set = are the lights on?
  
  
//Main Program Loop
//Poll the sensor values
//Adjust control state depending on inputs
//Wait for requests from the Raspberry Pi
  while(1) 
  {
    //The arduino is continuously reading to see if any requests have been generated
    //by the Raspberry Pi Server
    request = mySerial.read();
    
    //SHT15 readings
    temp_c_SHT = sht1x.readTemperatureC();
    humidity = sht1x.readHumidity();
    
    //MPL115A2 readings
    temp_c_mpl = mpl115a2.getTemperature();
    pressure = mpl115a2.getPressure();
    
    //Average the temperature coming from the two sensors
    temp = (temp_c_SHT+temp_c_mpl)/2.0;
    
    delay(10);

    //Check Sensor values against set values   
    if (temp < (temp_set - DZ_TEMP)) 
    {
      control(TEMP,1);
    }
    
    if (temp > (temp_set + DZ_TEMP))
    {
      control(TEMP,0);
    }
        
    if (humidity < (humidity_set - DZ_HUMIDITY) )
    {
      control(HUMIDITY,0);    
    }  
    if (humidity > (humidity_set + DZ_HUMIDITY))
    {
      control(HUMIDITY,1);
    }
       
    //The Server sends '$' to request a data update
    if (request == '$')
    {
      // Send data along USB through serial for local monitoring
      Serial.print("Data Request Made");
      Serial.print("\r\n");
      Serial.print(temp_c_mpl,2); 
      Serial.print(" ");
      Serial.print(temp_c_SHT,2);
      Serial.print(" ");
      Serial.print(humidity, 2);
      Serial.print(" ");
      Serial.println(pressure);
      
      //Call the data transmission routine to relay data to the Raspberry Pi
      transmit_data(temp, humidity, pressure, device_id);
      
      request = 'A';
    }
        
    //The Raspberry Pi send '@' to set control values.
    if (request == '@')
    {
      Serial.print("Control Loop Entered");
      Serial.print("\r\n");
      
      mySerial.write('@');
      
     
      //parse_data();
      
      //Need to parse data from Jason
      //Feed it into a function to update the set points
      
      request = 'A';
    } 
      
  } 
}

void transmit_data(float temp, float humidity, float pressure, char device_id[8])
 {
     static char outstr[15];
     
    //Send all collected data along XBEE. Comma delimited string with identifier for each variable. 
    mySerial.write("device_id:");
    mySerial.write(device_id);
    mySerial.write(",");
    mySerial.write("temp:");
    dtostrf(temp, 6, 3, outstr);
    mySerial.write(outstr);
    mySerial.write(",");
    mySerial.write("humidity:");
    dtostrf(humidity, 6, 3, outstr);
    mySerial.write(outstr);
    mySerial.write(",");
    mySerial.write("pressure:");
    dtostrf(pressure, 7, 3, outstr);
    mySerial.write(outstr);
    mySerial.write("\n");
 }
 
 void parse_data()
 {
 }
 
 void control(int system, bool state)
 {
   digitalWrite(system, state);
 }
