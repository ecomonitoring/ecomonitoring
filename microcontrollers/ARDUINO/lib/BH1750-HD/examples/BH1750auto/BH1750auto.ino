#include <BH1750-HD.h>
/*

  Advanced BH1750 library usage example

  This example had some comments about advanced usage features.

  Connection:

    VCC -> 5V (3V3 on Arduino Due, Zero, MKR1000, etc)
    GND -> GND
    SCL -> SCL (A5 on Arduino Uno, Leonardo, etc or 21 on Mega and Due)
    SDA -> SDA (A4 on Arduino Uno, Leonardo, etc or 20 on Mega and Due)
    ADD -> GND or VCC (see below)

  ADD pin uses to set sensor I2C address. If it has voltage greater or equal to
  0.7VCC voltage (as example, you've connected it to VCC) - sensor address will be
  0x5C. In other case (if ADD voltage less than 0.7 * VCC) - sensor address will
  be 0x23 (by default).

*/

#include <Wire.h>

/*

  BH1750 can be physically configured to use two I2C addresses:
    - 0x23 (most common) (if ADD pin had < 0.7VCC voltage)
    - 0x5C (if ADD pin had > 0.7VCC voltage)

  Library use 0x23 address as default, but you can define any other address.
  If you had troubles with default value - try to change it to 0x5C.
*/

BH1750 lightMeter(0x23);

void setup(){
  Serial.begin(9600);

  /*
    BH1750_AUTO_MODE automatically selects measurement mode and measurement time
    for maximum accuracy and maximum range.  
  */

  lightMeter.begin(BH1750_AUTO_MODE);
  Serial.println(F("BH1750 Test"));

}


void loop() {
  float lux = lightMeter.readLightLevel();
  Serial.print("Light: ");
  Serial.print(lux);
  Serial.println(" lx");

  delay(500);

}
