#include "GY_65.h"
#include "Wire.h"

GY_65::GY_65 bar(0x77);

void setup()
{  
  Serial.begin(9600);  
  Wire.begin();
  bar.begin();
}

void loop()
{
  bar.readSensor();
  Serial.print(" Pressure: ");
  Serial.println(bar.getPressure,DEC);
  delay(100);
  
}
