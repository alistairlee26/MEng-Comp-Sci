/*
  Nano ESP32 thermistor acquisition starter.

  Serial Monitor: 115200 baud. Output is readable Celsius once per second.
  Set Config::csvOutput to true for CSV logging instead.
  No third-party libraries are needed.
  D5 is held LOW: this sketch never enables or PWM-drives the heater.
  Keep the external heater supply disconnected during sensor development.
*/
#include <Arduino.h>
#include "Config.h"
#include "ThermistorMath.h"

#if !defined(ARDUINO_NANO_ESP32)
#error "Select Arduino Nano ESP32 (esp32:esp32:nano_nora), not the AVR Arduino Nano."
#endif

uint32_t lastSampleMs = 0;
bool serialWasConnected = false;

void setup() {
  digitalWrite(Config::heaterPin, LOW);
  pinMode(Config::heaterPin, OUTPUT);

  pinMode(Config::thermistorPin, INPUT);
  analogReadResolution(12);
  analogSetPinAttenuation(Config::thermistorPin, ADC_11db);
  Serial.begin(Config::serialBaud);
}

void printMeasurement(uint32_t now) {
  uint32_t rawTotal = 0;
  uint32_t millivoltTotal = 0;
  for (uint8_t i = 0; i < Config::averagingSamples; ++i) {
    // These are separate ADC conversions, averaged over the same short window.
    rawTotal += analogRead(Config::thermistorPin);
    millivoltTotal += analogReadMilliVolts(Config::thermistorPin);
  }

  const float raw = static_cast<float>(rawTotal) / Config::averagingSamples;
  const float mv = static_cast<float>(millivoltTotal) / Config::averagingSamples;
  const char* status = "OK";
  if (mv <= Config::minimumValidMv || raw <= 5.0f) {
    status = "LOW_OR_SHORT";
  } else if (mv >= Config::maximumValidMv || raw >= 4090.0f) {
    status = "HIGH_OR_OPEN";
  }
  bool valid = mv > Config::minimumValidMv &&
               mv < Config::maximumValidMv && raw > 5.0f && raw < 4090.0f;
  float resistance = NAN;
  float temperatureC = NAN;
  if (valid) {
    resistance = Config::fixedResistorOhms * mv / (Config::dividerSupplyMv - mv);
    temperatureC = thermistorCelsius(resistance, Config::thermistorReferenceOhms,
                                    Config::thermistorBetaKelvin,
                                    Config::thermistorReferenceC,
                                    Config::temperatureOffsetC);
    if (!isfinite(temperatureC)) {
      valid = false;
      status = "CONVERSION_ERROR";
    }
  }

  if (!Config::csvOutput) {
    if (valid) {
      Serial.print("Temperature: ");
      Serial.print(temperatureC, 1);
      Serial.println(" C");
    } else {
      Serial.print("Temperature unavailable: ");
      Serial.print(status);
      Serial.print(" (A0: ");
      Serial.print(mv, 0);
      Serial.println(" mV)");
    }
    return;
  }

  Serial.print(now);
  Serial.print(',');
  if (valid) {
    Serial.print(temperatureC, 2);
  }
  Serial.print(',');
  Serial.print(raw, 1);
  Serial.print(',');
  Serial.print(mv, 1);
  Serial.print(',');
  if (valid) {
    Serial.print(resistance, 1);
  }
  Serial.print(',');
  Serial.println(status);
}

void loop() {
  digitalWrite(Config::heaterPin, LOW);

  // USB serial can be opened later. Do not block startup waiting for a PC.
  if (!Serial) {
    serialWasConnected = false;
    return;
  }
  if (!serialWasConnected) {
    if (Config::csvOutput) {
      Serial.println("time_ms,temperature_C,raw_adc,voltage_mV,resistance_ohm,status");
    } else {
      Serial.println("Temperature in Celsius (nominal thermistor values; not yet calibrated).");
    }
    serialWasConnected = true;
  }

  const uint32_t now = millis();
  if (static_cast<uint32_t>(now - lastSampleMs) >= Config::sampleIntervalMs) {
    lastSampleMs = now;
    printMeasurement(now);
  }
}
