#include <WiFi.h>
#include <WebSocketsServer.h>
#include <NewPing.h>
#include <ArduinoJson.h>

#define TRIGGER_PIN        16  
#define ECHO_PIN           15  
#define MAX_DISTANCE_CM    8   
#define MAX_DISTANCE_PERCENT 100 
#define MOTOR_PIN          17  
#define BUZZER_PIN         18  
#define BUZZER_THRESHOLD   5    
#define MOTOR_THRESHOLD    3    

const char* ssid = "Rohit";
const char* password = "apar1234";
int distance_cm=0;
WebSocketsServer webSocket = WebSocketsServer(81);
NewPing sonar(TRIGGER_PIN, ECHO_PIN, MAX_DISTANCE_CM);

void handleWebSocketMessage(uint8_t num, uint8_t *payload, size_t length) {
  // Serial.printf("Received WebSocket message from client %u: %s\n", num, payload);
  // String allowHeader = "Access-Control-Allow-Origin: *\r\n";
  // webSocket.sendTXT(num, allowHeader.c_str());
    // webSocket.sendTXT(num, String((distance_cm * 100) / MAX_DISTANCE_CM).c_str());
    StaticJsonDocument<128> doc;
    doc["headers"]="Access-Control-Allow-Origin: *\r\n";
  doc["waterLevel"] = (distance_cm * 100) / MAX_DISTANCE_CM;

  // Serialize the JSON object to a string
  char jsonBuffer[128];
  serializeJson(doc, jsonBuffer);
}

void handleWebSocketEvent(uint8_t num, WStype_t type, uint8_t *payload, size_t length) {
  switch (type) {
    case WStype_DISCONNECTED:
      Serial.printf("Client %u disconnected\n", num);
      break;
    case WStype_TEXT:
      handleWebSocketMessage(num, payload, length);
      break;
    case WStype_BIN:
      break;
    case WStype_ERROR:
      Serial.printf("Error from client %u\n", num);
      break;
    case WStype_FRAGMENT_TEXT_START:
    case WStype_FRAGMENT_BIN_START:
    case WStype_FRAGMENT:
    case WStype_FRAGMENT_FIN:
      break;
  }
}

void setup() {
  Serial.begin(9600);
  pinMode(TRIGGER_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);
  pinMode(BUZZER_PIN, OUTPUT);
  pinMode(MOTOR_PIN, OUTPUT);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("Connected to WiFi");
  Serial.println(WiFi.localIP());

  webSocket.begin(); 
  webSocket.onEvent(handleWebSocketEvent); 

  Serial.println("WebSocket server started");
}

void loop() {
  distance_cm = sonar.ping_cm();
  distance_cm=MAX_DISTANCE_CM - distance_cm;
  Serial.println(distance_cm);

  if (distance_cm >= BUZZER_THRESHOLD) {
    digitalWrite(BUZZER_PIN, HIGH);
  } else {
    digitalWrite(BUZZER_PIN, LOW);
  }

  if (distance_cm <= MOTOR_THRESHOLD) {
    digitalWrite(MOTOR_PIN, HIGH);
  } 
  if (distance_cm >= BUZZER_THRESHOLD) {
    digitalWrite(MOTOR_PIN, LOW);
  }
  webSocket.loop();
  delay(2000);
}