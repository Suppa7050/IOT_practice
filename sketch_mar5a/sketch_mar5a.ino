#include <WiFi.h>
#include <WebSocketsServer.h>

#define BUZZER_PIN 12 // Define the pin connected to the buzzer

const char* ssid = "Suppa";
const char* password = "9959664388";

WebSocketsServer webSocket = WebSocketsServer(81); // Create a WebSocket server on port 81

void handleWebSocketMessage(uint8_t num, uint8_t *payload, size_t length) {
  Serial.printf("Received WebSocket message from client %u: %s\n", num, payload);

  if (strcmp((char*)payload, "buzz") == 0) {
    // Turn on the buzzer
    digitalWrite(BUZZER_PIN, HIGH);
    delay(1000); // Adjust this delay as needed
  
    // Turn off the buzzer
    digitalWrite(BUZZER_PIN, LOW);
    delay(1000); // Adjust this delay as needed
  }
}

void setup() {
  Serial.begin(115200);
  pinMode(BUZZER_PIN, OUTPUT); // Set the buzzer pin as an output

  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("Connected to WiFi");
  Serial.println(WiFi.localIP());

  webSocket.begin(); // Start WebSocket server
  webSocket.onEvent(handleWebSocketEvent); // Set callback function to handle WebSocket events

  Serial.println("WebSocket server started");
}

void loop() {
  webSocket.loop(); // Handle WebSocket events
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
