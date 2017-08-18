#include <LWiFi.h>

#define SITE_URL "66a264af.ngrok.io"
#define LED 7

String data ;
char buffer_sensor[4];

bool flag = false;
int count, last_count;
int v, last_v;
char _lwifi_ssid[] = "BecPC";
char _lwifi_pass[] = "ilovebec";

WiFiClient c;

void setup() {
  Serial.begin(9600);
  while (!Serial);
  Serial.println("Start");
  Serial.print("Connect to WIFI");
  while (WiFi.begin(_lwifi_ssid, _lwifi_pass) != WL_CONNECTED) {
    delay(1000);
  }
  Serial.println("wifi connect");
  // put your setup code here, to run once:

  pinMode(LED, OUTPUT);

}

void loop() {
  // put your main code here, to run repeatedly:
  int i = 0;
  ConnectToWEB();
  while (c.available())
  {
    last_v = v;
    v = c.read();
    if (v != -1)
    {
      Serial.print(char(v));

    }
  }
  Serial.println();

  if (v == '1')
    digitalWrite(7, HIGH);
  else
    digitalWrite(7, LOW);
  delay(3000);
}
void ConnectToWEB()
{
  c.stop();
  //Serial.println("Connecting to WebSite");
  while (0 == c.connect(SITE_URL, 80))
  {
    Serial.println("Re-Connecting to WebSite");
    delay(1000);
  }

  // send HTTP request, ends with 2 CR/LF
  //Serial.println("send HTTP GET request");
  c.println("GET / HTTP/1.1");
  c.println("Host: " SITE_URL);
  c.println("Connection: close");
  c.println();

  // waiting for server response
  //Serial.println("waiting HTTP response:");
  while (!c.available())
  {
    delay(100);
  }

}
