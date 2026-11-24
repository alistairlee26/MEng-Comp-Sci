#pragma once

#include <Arduino.h>

namespace Config {
// Board labels, not raw ESP32 GPIO numbers.
constexpr uint8_t thermistorPin = A0;
constexpr uint8_t heaterPin = D5;
constexpr uint32_t serialBaud = 115200;
constexpr uint32_t sampleIntervalMs = 1000;
constexpr uint8_t averagingSamples = 16;
constexpr bool csvOutput = false;  // false: readable Celsius; true: CSV logging

// Wiring: 3V3 -> fixed resistor -> A0 junction -> NTC -> GND.
// Replace these nominal values with measured values when calibrating.
constexpr float dividerSupplyMv = 3300.0f;
constexpr float fixedResistorOhms = 10000.0f;

// Course-kit AVX ND06P00103K: R25 = 10 kohm, material P beta = 4220 K.
// Datasheet: https://www.farnell.com/datasheets/86133.pdf (ND06 table, page 3).
// Nominal coefficients give an estimate until compared with a thermometer.
constexpr float thermistorReferenceOhms = 10000.0f;
constexpr float thermistorReferenceC = 25.0f;
constexpr float thermistorBetaKelvin = 4220.0f;
constexpr float temperatureOffsetC = 0.0f;  // leave zero until calibrated

// Diagnostic limits, not calibrated temperature limits. The ESP32-S3 ADC
// measures roughly up to 3.1 V with 11 dB attenuation; do not apply >3.3 V.
constexpr float minimumValidMv = 50.0f;
constexpr float maximumValidMv = 3000.0f;
}

static_assert(Config::averagingSamples > 0, "At least one ADC sample is required");
static_assert(Config::fixedResistorOhms > 0.0f, "Fixed resistor must be positive");
static_assert(Config::maximumValidMv < Config::dividerSupplyMv,
              "Valid sensor voltage must stay below the divider supply");
static_assert(Config::thermistorReferenceOhms > 0.0f, "Reference resistance must be positive");
static_assert(Config::thermistorBetaKelvin > 0.0f, "Thermistor beta must be positive");
static_assert(Config::thermistorReferenceC > -273.15f, "Reference must exceed absolute zero");
