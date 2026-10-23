
#include <WiFi.h>
#include <time.h>
#include <TFT_eSPI.h>
#include <math.h>

TFT_eSPI tft = TFT_eSPI();

const int clockX = 120;
const int clockY = 94;
const int clockR = 32;

void drawHand(float angle, int length, uint16_t colour, int width = 1) {
    float radians = (angle - 90) * PI / 180.0;
    int x = clockX + cos(radians) * length;
    int y = clockY + sin(radians) * length;

    tft.drawLine(clockX, clockY, x, y, colour);
}

void drawClock(struct tm *timeInfo) {
    tft.fillCircle(clockX, clockY, clockR, TFT_BLACK);
    tft.drawCircle(clockX, clockY, clockR, TFT_CYAN);

    for (int i = 0; i < 12; i++) {
        float angle = i * 30 * PI / 180.0;
        int inner = (i % 3 == 0) ? clockR - 7 : clockR - 4;

        int x1 = clockX + cos(angle - PI / 2) * inner;
        int y1 = clockY + sin(angle - PI / 2) * inner;
        int x2 = clockX + cos(angle - PI / 2) * (clockR - 2);
        int y2 = clockY + sin(angle - PI / 2) * (clockR - 2);

        tft.drawLine(x1, y1, x2, y2, TFT_WHITE);
    }

    float seconds = timeInfo->tm_sec;
    float minutes = timeInfo->tm_min + seconds / 60.0;
    float hours = (timeInfo->tm_hour % 12) + minutes / 60.0;

    drawHand(hours * 30, 15, TFT_WHITE, 3);
    drawHand(minutes * 6, 22, TFT_CYAN, 2);
    drawHand(seconds * 6, 27, TFT_RED);

    tft.fillCircle(clockX, clockY, 2, TFT_YELLOW);
}


void setup() {
    Serial.begin(115200);

    tft.init();
    tft.setRotation(1);
    tft.fillScreen(TFT_BLACK);

    tft.setTextColor(TFT_CYAN, TFT_BLACK);
    tft.drawCentreString("ESP32 CLOCK", 120, 4, 2);
    tft.drawFastHLine(8, 25, 224, TFT_DARKGREY);

    tft.setTextColor(TFT_WHITE, TFT_BLACK);
    tft.drawString("Connecting...", 5, 55, 2);

    WiFi.begin(
        "eduroam",
        WPA2_AUTH_PEAP,
        "zcabtal@ucl.ac.uk",
        "zcabtal@ucl.ac.uk",
        "Qazxcde123!@#$"
    );

    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.print(".");
    }

    Serial.println("\nWiFi connected");

    configTzTime(
        "GMT0BST,M3.5.0/1,M10.5.0/2",
        "pool.ntp.org",
        "time.nist.gov"
    );

    tft.fillScreen(TFT_BLACK);
    tft.setTextColor(TFT_CYAN, TFT_BLACK);
    tft.drawCentreString("ESP32 CLOCK", 120, 4, 2);
    tft.drawFastHLine(8, 25, 224, TFT_DARKGREY);
}

void loop() {
    struct tm timeInfo;

    if (getLocalTime(&timeInfo, 1000)) {
        char timeString[20];
        char dateString[20];

        strftime(timeString, sizeof(timeString), "%H:%M:%S", &timeInfo);
        strftime(dateString, sizeof(dateString), "%a, %d %b", &timeInfo);

        Serial.println(timeString);

        tft.fillScreen(TFT_BLACK);

        tft.setTextColor(TFT_CYAN, TFT_BLACK);
        tft.drawCentreString("ESP32 CLOCK", 120, 5, 2);
        tft.drawFastHLine(20, 26, 200, TFT_DARKGREY);

        tft.setTextColor(TFT_WHITE, TFT_BLACK);
        tft.drawCentreString(timeString, 120, 34, 4);

        tft.setTextColor(TFT_CYAN, TFT_BLACK);
        tft.drawCentreString(dateString, 120, 65, 2);

        drawClock(&timeInfo);

        tft.setTextColor(TFT_GREEN, TFT_BLACK);
        tft.drawCentreString("NTP SYNC", 120, 132 - 12, 1);
    } else {
        Serial.println("Waiting for time synchronisation");
    }

    delay(1000);
}
