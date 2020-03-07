/* in HardwareSerial.cpp
 *  void HardwareSerial::clear()
    {
      _rx_buffer_head = _rx_buffer_tail;
    }

 *  in HardvareSerial.h
 *      virtual void clear(void);

 * 
 */
#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#include <ESPAsyncWebServer.h>
#include <ESPAsyncTCP.h>
//#include <CRC32.h>  
#include <EEPROM.h>

extern "C" {
  #include "user_interface.h"
  #include "wpa2_enterprise.h"
}

#define connectime 5

static const char *APssid = "ECOBOX_ID_001";
#include "passwd.h"

int stat=0;
unsigned long timing;
#define RS 0
#define CONF 1
#define INAP 2

//static const char* TJ="{"id":"001", "sensor":"temperature", "value":0}";

struct Config
{
  char ssid[20];  
  char username[20];
  char password[20];
  char host[20];
  //uint32_t sum;
};
Config data;


void handleGet (AsyncWebServerRequest *request);
void handleRoot(AsyncWebServerRequest *request);

//String SERVER_IP="10.1.32.54:8000";

bool ReadConfig()
{
  EEPROM.get(0, data);
  //uint32_t sum=CRC32::calculate(&data, offsetof(Config,sum));
  //data.ssid="SMSU-EDU";
  //data.host=""
  //if(sum!=data.sum)return false;
  //else {
  //  return true;
  //}
  data.ssid[sizeof(data.ssid)-1] = 0;
  data.host[sizeof(data.host)-1] = 0;
  data.username[sizeof(data.username)-1] = 0;
  data.password[sizeof(data.password)-1] = 0;
  
  return true;
}
void WriteConfig()
{
  //data.sum = CRC32::calculate(&data, offsetof(Config,sum));
  EEPROM.put(0, data);
  EEPROM.commit();
  Serial.println(F("CONFIG IS WRITTEN"));
}


/*static const char index_html[] /*PROGMEM = R"rawliteral(
<!DOCTYPE HTML><html><head>
<meta charset="utf-8">
<title>ECO BOX CONFIGURE</title>
<meta name='viewport' content='width=device-width, initial-scale=1'>
</head><body>
<form action='/get'>
<label>Введите IP:порт сервера:</label>
<input type='text' name='host' value='%s'>
<br>
<label>Введите SSID сети, к которой нужно подключиться:</label>
<input type='text' name='ssid' value='%s'>
<br>
<label>Введите имя пользователя для подключения к сети:</label>
<input type='text' name='username' value='%s'>
<br>
<label>Введите пароль для подключения к сети:</label>
<input type='text' name='password' value='%s'>
<br>
<input type='hidden' name='end'>
<input type='submit' value='Сохранить и выйти'>
</form>
</body></html>)rawliteral";*/

char index_html[] /*PROGMEM*/ = R"rawliteral(
<!DOCTYPE HTML><html><head>
<title>ECO BOX CONFIGURE</title>
<meta name='viewport' content='width=device-width, initial-scale=1'>
</head><body>
{                                                                           }
<form action='/get'>
<label>Insert IP:port of server:</label>
<input type='text' name='host'>
<br>
<label>Insert network ssid:</label>
<input type='text' name='ssid'>
<br>
<label>Insert username for network:</label>
<input type='text' name='username'>
<br>
<label>Insert password for username:</label>
<input type='text' name='password'>
<br>
<input type='hidden' name='end'>
<input type='submit' value='Submit & reboot'>
</form>
</body></html>)rawliteral";




void APCreate()
{
  WiFi.mode(WIFI_AP);
  WiFi.softAPConfig(IPAddress(192,168,0,1), IPAddress(192,168,1,1), IPAddress(255, 255, 255, 0));
  WiFi.softAP(APssid);
  delay(1000);
  stat=INAP;
  timing=millis();
}


struct station_config wifi_config;
bool WiFiConnect()
{
//WPA2 ENTERPRISE CONNECTION BEGIN
  //wifi_set_opmode(STATION_MODE);
  WiFi.mode(WIFI_STA);
  memset(&wifi_config, 0, sizeof(wifi_config));
  strcpy((char*)wifi_config.ssid, data.ssid);

  Serial.println("IN CONNECTION " + String(strlen(data.username)) + " " + String(strlen(data.password)));
  
  ETS_UART_INTR_DISABLE();
  wifi_station_set_config(&wifi_config);
  wifi_station_clear_cert_key();
  wifi_station_clear_enterprise_ca_cert();
  wifi_station_set_wpa2_enterprise_auth(1);
  wifi_station_set_enterprise_identity((uint8*)data.username, strlen(data.username));
  wifi_station_set_enterprise_username((uint8*)data.username, strlen(data.username));
  wifi_station_set_enterprise_password((uint8*)data.password, strlen(data.password));
  wifi_station_connect();
  ETS_UART_INTR_ENABLE();
  Serial.println("IN CONNECTION WHILE");
  
  timing=millis();
  while (WiFi.status() != WL_CONNECTED && millis()-timing<connectime*60*1000) { delay(50);}
  //Serial.println("OUT OF CONNECTION WHILE");
  if(WiFi.status() != WL_CONNECTED)
  {
    //Serial.println("ERROR"):
    delay(100);
    return false;
  }
  stat=RS;
  //Serial.println("CONNECTED");
  delay(100);
//  Serial.clear();
  return true;  
}

AsyncWebServer server(80);

void setup() {
  Serial.println();
  Serial.begin(115200);
  EEPROM.begin(sizeof(Config));
  Serial.println(F("\nEEPROM BEGINNED"));
  delay(1000);
if (ReadConfig()){
    Serial.println(F("ConfigWasReadSuccess"));
  }
  else Serial.println(F("ConfigWasReadUnSuccess"));
  Serial.println(data.host);
  Serial.println(data.ssid);
  Serial.println(data.username);
  Serial.println(data.password);
  delay(1000);
  Serial.println();
  Serial.print(F("Index_html size:"));
  Serial.println(sizeof(index_html));
  if(!WiFiConnect())
  {
    APCreate();
    Serial.println(F("AP CREATED"));
  }
  else Serial.println(F("CONNECTED"));
  
  server.on("/",HTTP_GET, handleRoot);
  server.on("/get", HTTP_GET, handleGet);
  server.begin();
  
  Serial.println(F("FINISHED"));
}

void PostJson(String json)
{
  WiFiClient client;
  HTTPClient http;

  http.begin(client, "http://" +String(data.host) + "/put_event/"); //HTTP
  http.addHeader("Content-Type", "application/json");

  int httpCode = http.POST(json);

  if (httpCode > 0) {
    if (httpCode == HTTP_CODE_OK) {
      Serial.println(F("OK"));
      delay(10);
    }
    } else {
      Serial.printf("ERROR: %s\n", http.errorToString(httpCode).c_str());
    }

    http.end();
}

void loop()
{
  //server.handleClient();  ТАКОЙ ФЙНКЦИИ В async web server нет
  if(millis()<timing)timing=0;
  if(stat==RS && Serial.find("CONFIG"))
  {
    WiFi.disconnect();
    APCreate();
    return;
  }
  else if(stat==INAP && millis()-timing>300000)
  {
    WiFi.softAPdisconnect (true);
    if(!WiFiConnect())
      APCreate();
  }
  else if(stat==RS && Serial.find("END"))
  {
    String json=Serial.readStringUntil('E');
    PostJson(json);
  }
  

}

void handleGet (AsyncWebServerRequest *request)
{
  //String inputMessage;
    if (request->hasParam("host")) {
      String tmp = request->getParam("host")->value();
      strncpy(data.host, tmp.c_str(), sizeof(data.host));
      data.host[min(sizeof(data.host)-1, tmp.length())] = 0;
      //data.host[tmp.length()] = 0;
      //Serial.println(data.host);
      tmp.clear();
    }
    if (request->hasParam("ssid")) {
      String tmp = request->getParam("ssid")->value();
      strncpy(data.ssid, tmp.c_str(), sizeof(data.ssid));
      data.ssid[min(sizeof(data.ssid)-1, tmp.length())] = 0;
      //data.ssid[tmp.length()] = 0;
      //Serial.println(data.ssid);
      tmp.clear();
    }
    if (request->hasParam("username")) {
      String tmp = request->getParam("username")->value();
      strncpy(data.username, tmp.c_str(), sizeof(data.username));
      data.username[min(sizeof(data.username)-1, tmp.length())] = 0;
      //data.username[tmp.length()] = 0;
      //Serial.println(data.username);
      tmp.clear();
    }
    if (request->hasParam("password")) {
      String tmp = request->getParam("password")->value();
      strncpy(data.password, tmp.c_str(), sizeof(data.password));
      data.password[min(sizeof(data.password)-1, tmp.length())] = 0;
      //data.password[tmp.length()] = 0;
      //Serial.println(data.password);
      tmp.clear();
    }
    if (request->hasParam("end")) {
      WriteConfig();
      Serial.println(data.host);
      Serial.println(data.ssid);
      Serial.println(data.username);
      Serial.println(data.password);
      delay(500);
      request->send(200, "text/html", "<!DOCTYPE HTML><html><body><script>window.onload = function(){document.location.replace(\"/\");}</script></body></html>");
      ESP.restart();
    }
    request->send(200, "text/html", "<!DOCTYPE HTML><html><body><script>window.onload = function(){document.location.replace(\"/\");}</script></body></html>");
}


/*static const char* www_realm = "Auth Realm";
static const char* authFailResponse = "Authentication Failed";*/

char* safecopy(char* to, const char* from)
{
  while (*from) {
    if (isalnum(*from)) {
      *to++ = *from++; 
    } else {
      from++;
    }
  }

  return to;
}

void FillIndHtml()
{
  char* p = strchr(index_html, '{');
  p += 1; p = safecopy(p, data.ssid);
  p += 1;
  p = safecopy(p, data.host);
  p += 1;
  p = safecopy(p, data.username);
  p += 1;
  p = safecopy(p, data.password);
}

void handleRoot(AsyncWebServerRequest *request)
{
  if(!request->authenticate(SUser, SPass))
        return request->requestAuthentication();
  Serial.println(F("AUTH PASSED"));
  //char tmp[sizeof(index_html)+sizeof(Config)+1];
  //strcpy_P(buffer, (char*)pgm_read_dword(&(string_table[i])));
  //strcpy_P(tmp, (char*)pgm_read_dword(index_html));
  //Serial.println("GOT HTML FROM PROGMEM");
  //snprintf(index_html, sizeof(index_html)+sizeof(Config), index_html, data.host, data.ssid, data.username, data.password);
  FillIndHtml();
  request->send(200, "text/html", index_html);
  
  timing = millis();
  stat = CONF;
}
