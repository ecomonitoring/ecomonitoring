/****************************************************************************/
//  Function:       Header file for TroykaDHT
//  Hardware:       DHT11, DHT21, DHT22
//  Arduino IDE:    Arduino-1.8.2
//  Author:         Igor Dementiev
//  Date:           Feb 22,2018
//  Version:        v1.0
//  by www.amperka.ru
/****************************************************************************/

#ifndef __TROYKA_DHT_H__
#define __TROYKA_DHT_H__

#include <Arduino.h>

#define DHT_OK                   0
#define DHT_ERROR_CHECKSUM      -1
#define DHT_ERROR_TIMEOUT       -2
#define DHT_ERROR_NO_REPLY      -3


class DHT
{
public:
    explicit DHT(uint8_t pin);
    void begin();
    int8_t read();
    int8_t getState() const { return _state; }
    float getTemperatureC() const { return _temperatureC; }
    float getHumidity() const { return _humidity; }
private:
    unsigned long pulseInLength(uint8_t pin, bool state, unsigned long timeout = 1000000L);
    uint8_t _pin;
    int8_t _state;
    float _temperatureC;
    float _humidity;
};
#endif  // __TROYKA_DHT_H__