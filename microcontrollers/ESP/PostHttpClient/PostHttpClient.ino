/**
   PostHTTPClient.ino

    Created on: 21.11.2016

*/

#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>

#define USE_SERIAL Serial

extern "C" {
#include "user_interface.h"
#include "wpa2_enterprise.h"
}

/* this can be run with an emulated server on host:
        cd esp8266-core-root-dir
        cd tests/host
        make ../../libraries/ESP8266WebServer/examples/PostServer/PostServer
        bin/PostServer/PostServer
   then put your PC's IP address in SERVER_IP below, port 9080 (instead of default 80):
*/
//#define SERVER_IP "10.0.1.7:9080" // PC address with emulation on host
#define SERVER_IP "10.1.32.54:8000"

#include "passwd.h"

void setup() {

  USE_SERIAL.begin(115200);

  USE_SERIAL.println();
  USE_SERIAL.println();
  USE_SERIAL.println();

   wifi_set_opmode(STATION_MODE);
    struct station_config wifi_config;
    memset(&wifi_config, 0, sizeof(wifi_config));
    strcpy((char*)wifi_config.ssid, ssid);
    wifi_station_set_config(&wifi_config);
    wifi_station_clear_cert_key();
    wifi_station_clear_enterprise_ca_cert();
    wifi_station_set_wpa2_enterprise_auth(1);
    wifi_station_set_enterprise_identity((uint8*)username, strlen(username));
    wifi_station_set_enterprise_username((uint8*)username, strlen(username));
    wifi_station_set_enterprise_password((uint8*)password, strlen(password));
    wifi_station_connect();

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    USE_SERIAL.print(".");
  }
  USE_SERIAL.println("");
  USE_SERIAL.print("Connected! IP address: ");
  USE_SERIAL.println(WiFi.localIP());

}

void loop() {
  // wait for WiFi connection
  if ((WiFi.status() == WL_CONNECTED)) {

    WiFiClient client;
    HTTPClient http;

    USE_SERIAL.print("[HTTP] begin...\n");
    // configure traged server and url
    http.begin(client, "http://" SERVER_IP "/put_event/"); //HTTP
    http.addHeader("Content-Type", "application/json");

    USE_SERIAL.print("[HTTP] POST...\n");
    // start connection and send HTTP header and body
    int httpCode = http.POST("{\"temperature\":\"45\"}");

    // httpCode will be negative on error
    if (httpCode > 0) {
      // HTTP header has been send and Server response header has been handled
      USE_SERIAL.printf("[HTTP] POST... code: %d\n", httpCode);

      // file found at server
      if (httpCode == HTTP_CODE_OK) {
        const String& payload = http.getString();
        USE_SERIAL.println("received payload:\n<<");
        USE_SERIAL.println(payload);
        USE_SERIAL.println(">>");
      }
    } else {
      USE_SERIAL.printf("[HTTP] POST... failed, error: %s\n", http.errorToString(httpCode).c_str());
    }

    http.end();
  }

  delay(10000);
}
