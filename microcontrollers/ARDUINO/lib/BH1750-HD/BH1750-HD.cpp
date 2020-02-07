/*

  This is a library for the BH1750FVI Digital Light Sensor
  breakout board.

  The board uses I2C for communication. 2 pins are required to
  interface to the device.

  Written by Christopher Laws, March, 2013.

  Сhanged by Evtomax (evtomax@cxem.net), January, 2017:
    Result type of readLightLevel() function changed from uint16_to to float. 
    Added setMeasurementTime function.
    Improved lux calculation to consider measurement mode and measurement time.
    Added auto mode that automatically selects measurement mode and measurement time 
    for maximum accuracy and maximum range.  
*/

#include "BH1750-HD.h"

// Define milliseconds delay for ESP8266 platform
#if defined(ESP8266)

  #include <pgmspace.h>
  #define _delay_ms(ms) delayMicroseconds((ms) * 1000)

// Use _delay_ms from utils for AVR-based platforms
#elif defined(__avr__)
  #include <util/delay.h>

// Use Wiring's delay for compability with another platforms
#else
  #define _delay_ms(ms) delay(ms)
#endif


// Legacy Wire.write() function fix
#if (ARDUINO >= 100)
  #define __wire_write(d) Wire.write(d)
#else
  #define __wire_write(d) Wire.send(d)
#endif


// Legacy Wire.read() function fix
#if (ARDUINO >= 100)
  #define __wire_read() Wire.read()
#else
  #define __wire_read() Wire.receive()
#endif


/**
 * Constructor
 * @params addr Sensor address (0x76 or 0x72, see datasheet)
 *
 * On most sensor boards, it was 0x76
 */
BH1750::BH1750(byte addr) {

  BH1750_I2CADDR = addr;

}


/**
 * Begin I2C and configure sensor
 * @param mode Measurment mode
 */
void BH1750::begin(uint8_t mode) {

  // Initialize I2C
  Wire.begin();

  // Configure sensor in specified mode
  configure(mode);

}


/**
 * Configurate BH1750 with specified working mode
 * @param mode Measurment mode
 */
void BH1750::configure(uint8_t newMode) {

  // Check, is measurment mode exist
  switch (newMode) {

    case BH1750_CONTINUOUS_HIGH_RES_MODE:
    case BH1750_CONTINUOUS_HIGH_RES_MODE_2:
    case BH1750_CONTINUOUS_LOW_RES_MODE:
    case BH1750_ONE_TIME_HIGH_RES_MODE:
    case BH1750_ONE_TIME_HIGH_RES_MODE_2:
    case BH1750_ONE_TIME_LOW_RES_MODE:

      // Send mode to sensor
      Wire.beginTransmission(BH1750_I2CADDR);
      __wire_write((uint8_t)newMode);
      Wire.endTransmission();
      

      // Wait few moments for waking up
      _delay_ms(10);
      mode = newMode;
      autoMode = false;
      break;

    case BH1750_AUTO_MODE:
      BH1750::autoConfigure();
      break;
    
    default:

      // Invalid measurement mode
      #ifdef BH1750_DEBUG
        Serial.println(F("BH1750: Invalid measurment mode"));
      #endif

      break;

  }

}

/**
 * Configurate BH1750 automaticaly
 */
void BH1750::autoConfigure(){
      uint16_t newMeasurementTime;
      if ((lastRawLevel<32767)&&(mode!=BH1750_CONTINUOUS_HIGH_RES_MODE_2)) 
        BH1750::configure(BH1750_CONTINUOUS_HIGH_RES_MODE_2);
      else if (lastRawLevel==65535){
        setMeasurementTime(BH1750_MIN_MTREG);
        BH1750::configure(BH1750_CONTINUOUS_HIGH_RES_MODE);
      }else{
        if (measurementTime<BH1750_MAX_MTREG){
          newMeasurementTime = measurementTime*(65535/(lastRawLevel+1));
          if (newMeasurementTime>BH1750_MAX_MTREG) newMeasurementTime = BH1750_MAX_MTREG;
          else if (newMeasurementTime<BH1750_MIN_MTREG) newMeasurementTime = BH1750_MIN_MTREG;
          setMeasurementTime(newMeasurementTime);
        }
      }
      
      autoMode = true;     
}

/**
 * Set measurement time
 * @param newTime New MTreg value 31 ~ 254
 */
void BH1750::setMeasurementTime(uint8_t newTime) {
  Wire.beginTransmission(BH1750_I2CADDR);
  __wire_write((uint8_t)BH1750_SET_MTREG_HIGH|(newTime>>5));
  Wire.endTransmission();
  Wire.beginTransmission(BH1750_I2CADDR);
  __wire_write((uint8_t)BH1750_SET_MTREG_LOW|(newTime&BH1750_MTREG_LOW_MASK));
  Wire.endTransmission();
  measurementTime = newTime;
  _delay_ms(10);
}

/**
 * Read light level from sensor
 * @return  Lightness in lux (0 ~ 120000)
 */
float BH1750::readLightLevel(void) {
  uint16_t currentMillis = millis();

  // Measurment result will be stored here
  uint16_t raw_level;
  float level;

  if ((currentMillis-lastMillis)>
      (BH1750_DEFAULT_MTREG_MS*measurementTime/BH1750_DEFAULT_MTREG+50)){
      // Read two bytes from sensor
      Wire.requestFrom(BH1750_I2CADDR, 2);

      // Read two bytes, which are low and high parts of sensor value
      raw_level = __wire_read();
      raw_level <<= 8;
      raw_level |= __wire_read();

      // Send raw value if debug enabled
      #ifdef BH1750_DEBUG
        Serial.print(F("[BH1750] Raw value: "));
        Serial.println(raw_level);
      #endif

      // Convert raw value to lux
      level = (float)raw_level/1.2*((float)BH1750_DEFAULT_MTREG/measurementTime);
      switch (mode){
        case BH1750_CONTINUOUS_HIGH_RES_MODE_2:
        case BH1750_ONE_TIME_HIGH_RES_MODE_2:
          level/=2;
        break; 
      }

      // Send converted value, if debug enabled
      #ifdef BH1750_DEBUG
        Serial.print(F("[BH1750] Converted value: "));
        Serial.println(level);
      #endif
      lastMillis = currentMillis;
      lastLevel = level;
      lastRawLevel = raw_level;
      if (autoMode){
        BH1750::autoConfigure();
      }
  }else{
    level = lastLevel;
  }

  return level;

}
