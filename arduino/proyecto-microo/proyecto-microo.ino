#include <DHT.h>

#define DHTPIN 2
#define DHTTYPE DHT11

#define TRIG_PIN 3
#define ECHO_PIN 4
#define MQ2_PIN A0

DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(9600);
  dht.begin();
  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);
}

float leerDistanciaCM() {
  digitalWrite(TRIG_PIN, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG_PIN, LOW);

  long duracion = pulseIn(ECHO_PIN, HIGH);
  float distancia = duracion * 0.034 / 2;  // cm
  return distancia;
}

void loop() {
  float temp = dht.readTemperature();
  float hum = dht.readHumidity();
  float dist = leerDistanciaCM();
  int gas = analogRead(MQ2_PIN);

  // Validaciones mínimas
  if (isnan(temp) || isnan(hum)) {
    Serial.println("0,0,0,0");
  } else {
    Serial.print(temp); Serial.print(",");
    Serial.print(hum); Serial.print(",");
    Serial.print(dist); Serial.print(",");
    Serial.println(gas);
  }

  delay(1000);
}
