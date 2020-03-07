//===== КОНСТАНТЫ ======
#define BOX_ID "'001'"
//======== ПИНЫ ========
#define MQ135_ANALOG A0
#define MQ135_HEATER 5

#define DHT11_PIN 8

#define GY_65 0x77
#define GY_30 0x23
//Общий анод
/*#define red   9
#define green 10
#define blue  11
*/
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
//GRGB led(red, green, blue);
DHT dht(DHT11_PIN);
MQ135 mq(MQ135_ANALOG, MQ135_HEATER);
BH1750 light(GY_30);

//======= ГЛОБАЛЫ =======
unsigned long int rt=millis();
//int color=0;


void setup()
{
  //led.setDirection(REVERSE);
  //led.setBrightness(10); 
  
  uart.begin(115200);

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
  
  //led.colorWheel(color);
}

void loop()
{
/*/===== RGB =========
    color = (color+50)%1531;
    led.colorWheel(color);
*/
//===== DHT ==========
  dht.read();
  if(dht.getState()==DHT_OK)
  {
    uart.print(F("{'sensor':'temperature', 'value':"));
    uart.print(dht.getTemperatureC());
    uart.print(F(", 'id':"));
    uart.print(BOX_ID);
    uart.print(F("}"));
    uart.print(F("{'sensor':'humidity', 'value':"));
    uart.print(dht.getHumidity());
    uart.print(F(", 'id':"));
    uart.print(BOX_ID);
    uart.print(F("}"));
  }
  
//===== BMP ============
  uart.print(F("{'sensor':'pressure', 'value':"));
  uart.print(bmp.readPressure());
  uart.print(F(", 'id':"));
  uart.print(BOX_ID);
  uart.print(F("}"));
//===== GY-30 ===========
  uart.print(F("{'sensor':'illumination', 'value':"));
  uart.print(light.readLightLevel());
  uart.print(F(", 'id':"));
  uart.print(BOX_ID);
  uart.print(F("}"));
  
//===== MQ-135 ==========
  uart.print(F("{'sensor':'gases', 'value':"));
  uart.print((String)mq.readCO2(dht.getTemperatureC(), dht.getHumidity()));
  uart.print(F(", 'id':"));
  uart.print(BOX_ID);
  uart.print(F("}"));
//  uart.print();
  uart.println(F("END"));
  delay(1000);
}
