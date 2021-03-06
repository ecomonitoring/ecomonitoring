#include "MQ135.h"

MQ135::MQ135(uint8_t pin, uint8_t pinHeater)
  : BaseMQ(pin, pinHeater) {
}

unsigned long MQ135::readCO2(float temperature, float humidity) {
  return readScaled(-0.42 , 1.92, temperature, humidity);
}
