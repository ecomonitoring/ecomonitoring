/*

  This is a library for the BH1750FVI Digital Light Sensor
  breakout board.

  The board uses I2C for communication. 2 pins are required to
  interface to the device.

  Datasheet: http://rohmfs.rohm.com/en/products/databook/datasheet/ic/sensor/light/bh1750fvi-e.pdf

  Written by Christopher Laws, March, 2013.
  
  Сhanged by Evtomax (evtomax@cxem.net), January, 2017:
    Result type of readLightLevel() function changed from uint16_to to float. 
    Added setMeasurementTime function.
    Improved lux calculation to consider measurement mode and measurement time.
    Added auto mode that automatically selects measurement mode and measurement time 
    for maximum accuracy and maximum range.  

*/

#ifndef BH1750_h
#define BH1750_h

#if (ARDUINO >= 100)
  #include <Arduino.h>
#else
  #include <WProgram.h>
#endif

#include "Wire.h"

// Uncomment, to enable debug messages
// #define BH1750_DEBUG

// No active state
#define BH1750_POWER_DOWN B0000000

// Wating for measurment command
#define BH1750_POWER_ON B00000001

// Reset data register value - not accepted in POWER_DOWN mode
#define BH1750_RESET B00000111

// Start measurement at 1lx resolution. Measurement time is approx 120ms.
#define BH1750_CONTINUOUS_HIGH_RES_MODE  B00010000

// Start measurement at 0.5lx resolution. Measurement time is approx 120ms.
#define BH1750_CONTINUOUS_HIGH_RES_MODE_2  B00010001

// Start measurement at 4lx resolution. Measurement time is approx 16ms.
#define BH1750_CONTINUOUS_LOW_RES_MODE  B00010011

// Start measurement at 1lx resolution. Measurement time is approx 120ms.
// Device is automatically set to Power Down after measurement.
#define BH1750_ONE_TIME_HIGH_RES_MODE  B00100000

// Start measurement at 0.5lx resolution. Measurement time is approx 120ms.
// Device is automatically set to Power Down after measurement.
#define BH1750_ONE_TIME_HIGH_RES_MODE_2  B00100001

// Start measurement at 1lx resolution. Measurement time is approx 120ms.
// Device is automatically set to Power Down after measurement.
#define BH1750_ONE_TIME_LOW_RES_MODE  B00100011

// Auto mode that automatically selects measurement mode and measurement time
#define BH1750_AUTO_MODE B00100100

// Change measurement time (High bit) 01000_MT[7,6,5]
#define BH1750_SET_MTREG_HIGH B01000000
#define BH1750_MTREG_HIGH_MASK B00000111

// Change measurement time (Low bit) 011_MT[4,3,2,1,0]
#define BH1750_SET_MTREG_LOW B01100000
#define BH1750_MTREG_LOW_MASK B00011111

#define BH1750_DEFAULT_MTREG 69
#define BH1750_DEFAULT_MTREG_MS 120
#define BH1750_MAX_MTREG 254
#define BH1750_MIN_MTREG 31

class BH1750 {

  public:
    BH1750 (byte addr = 0x23);
    void begin (uint8_t mode = BH1750_CONTINUOUS_HIGH_RES_MODE);
    void configure (uint8_t mode);
    void setMeasurementTime (uint8_t time);
    float readLightLevel(void);

  private:
    int BH1750_I2CADDR;
    uint8_t measurementTime = BH1750_DEFAULT_MTREG;
    uint8_t mode;
    boolean autoMode;
    uint16_t lastMillis = 0;
    float lastLevel = 0;
    uint16_t lastRawLevel = 0;
    void autoConfigure();

};

#endif
