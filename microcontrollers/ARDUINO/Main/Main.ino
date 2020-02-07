//======== ПИНЫ ========
#define MQ135_ANALOG A0
#define MQ135_HEATER 4

#define DHT11_PIN 2

#define GY_65 0x77
#define GY_30 0x23
      //Общий анод
#define red   9
#define green 10
#define blue  11
//===== КОНСТАНТЫ ======

//===== БИБЛИОТЕКИ =====
#include "GyverRGB.h"
#include "GyverButton.h"
#include "TroykaDHT.h"
#include "TroykaMQ.h"
#include "BH1750-HD.h"
#include "Adafruit_BMP085.h"
#include "Wire.h"
//======= ОБЪЕКТЫ =======
Adafruit_BMP085 bmp;
GRGB led(red, green, blue);
DHT dht(DHT11_PIN);
MQ135 mq(MQ135_ANALOG, MQ135_HEATER);
BH1750 light(GY_30);

//======= ГЛОБАЛЫ =======
int rt=millis();
int color=0;


void setup()
{
  led.setDirection(REVERSE);
  led.setBrightness(10); 
  
  uart.begin(9600);

  bmp.begin();
  light.begin(BH1750_AUTO_MODE);
  
  dht.begin();
  while(dht.getState()!=DHT_OK)
  {
    dht.read();
  }

  mq.heaterPwrHigh();
  while(!mq.heatingCompleted()) {;}
  mq.calibrate(100);
  
  led.colorWheel(color);
}

void loop()
{
//===== RGB =========
    color = (color+50)%1531;
    led.colorWheel(color);
  
  String json="{";
//===== DHT ==========
  json += "'temperature':";
  dht.read();
  json += (String) dht.getTemperatureC();
  json += ", 'humidity':";
  json += (String) dht.getHumidity();
  
//===== BMP ============
  json += ", 'pressure':";
  json += (String) bmp.readPressure();

//===== GY-30 ===========
  json += ", 'light':";
  json += (String)light.readLightLevel();

//===== MQ-135 ==========
  json += ", 'CO2':";
  json += (String)mq.readCO2(dht.getTemperatureC(), dht.getHumidity());

  json += "};";

  uart.println(json);
  delay(1000);
}
