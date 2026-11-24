#pragma once

#include <math.h>

// Beta equation; arguments keep this independent of the board and ADC APIs.
inline float thermistorCelsius(float resistanceOhms, float referenceOhms,
                              float betaKelvin, float referenceC,
                              float offsetC = 0.0f) {
  if (!isfinite(resistanceOhms) || resistanceOhms <= 0.0f ||
      !isfinite(referenceOhms) || referenceOhms <= 0.0f ||
      !isfinite(betaKelvin) || betaKelvin <= 0.0f ||
      !isfinite(referenceC) || referenceC <= -273.15f ||
      !isfinite(offsetC)) {
    return NAN;
  }
  const float inverseKelvin = 1.0f / (referenceC + 273.15f) +
                              logf(resistanceOhms / referenceOhms) / betaKelvin;
  if (!isfinite(inverseKelvin) || inverseKelvin <= 0.0f) {
    return NAN;
  }
  return 1.0f / inverseKelvin - 273.15f + offsetC;
}
