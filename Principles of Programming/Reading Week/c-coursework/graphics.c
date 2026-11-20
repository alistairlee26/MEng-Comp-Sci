#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "graphics.h"

char* replaceNewlineWithEntity(const char* s)
{
  if (s == NULL) return NULL;

  size_t len = strlen(s);
  size_t new_len = 0;
  for (size_t i = 0; i < len; ++i)
  {
    if (s[i] == '\n')
    {
      new_len += 5;
      continue;
    }
    if (s[i] != '\r')
    {
      new_len += 1;
    }
  }

  char* out = (char*)malloc(new_len + 1);
  if (out == NULL) return NULL;

  char* p = out;
  for (size_t i = 0; i < len; ++i)
  {
    if (s[i] == '\n')
    {
      memcpy(p, "&#10;", 5);
      p += 5;
      continue;
    }
    if (s[i] != '\r')
    {
      *p++ = s[i];
    }
  }
  *p = '\0';
  return out;
}

void setLineWidth(int width)
{
  printf("LW %i\n", width);
  fflush(stdout);
}

void drawLine(int x1, int y1, int x2, int y2)
{
  printf("DL %i %i %i %i\n", x1, y1, x2, y2);
  fflush(stdout);
}

void drawRect(int x, int y, int width, int height)
{
  printf("DR %i %i %i %i\n", x, y, width, height);
  fflush(stdout);
}

void drawRectRotated(int x, int y, int width, int height, int angle)
{
  printf("DT %i %i %i %i %i\n", x, y, width, height, angle);
  fflush(stdout);
}

void fillRect(int x, int y, int width, int height)
{
  printf("FR %i %i %i %i\n", x, y, width, height);
  fflush(stdout);
}

void fillRectRotated(int x, int y, int width, int height, int angle)
{
  printf("FT %i %i %i %i %i\n", x, y, width, height, angle);
  fflush(stdout);
}

void drawOval(int x, int y, int width, int height)
{
  printf("DO %i %i %i %i\n",x,y,width,height);
  fflush(stdout);
}

void fillOval(int x, int y, int width, int height)
{
  printf("FO %i %i %i %i\n",x,y,width,height);
  fflush(stdout);
}

void drawArc(int x, int y, int width, int height, int startAngle, int arcAngle)
{
  printf("DA %i %i %i %i %i %i\n",x,y,width,height, startAngle, arcAngle);
  fflush(stdout);
}

void fillArc(int x, int y, int width, int height, int startAngle, int arcAngle)
{
  printf("FA %i %i %i %i %i %i\n",x,y,width,height, startAngle, arcAngle);
  fflush(stdout);
}

void drawPolygon(int count, int x[], int y[])
{
  printf("DP ");
  printf("%d ", count);
  for (int n = 0 ; n < count ; n++)
  {
    printf("%d %d ", x[n], y[n]);
  }
  printf("\n");
  fflush(stdout);
}

void fillPolygon(int count, int x[], int y[])
{
  printf("FP ");
  printf("%d ", count);
  for (int n = 0 ; n < count ; n++)
  {
    printf("%d %d ", x[n], y[n]);
  }
  printf("\n");
  fflush(stdout);
}

void drawString(char* s, int x, int y)
{
  printf("DS %i %i @%s\n",x,y,s);
  fflush(stdout);
}

void drawStringRotated(char* s, int x, int y, int angle)
{
  printf("SR %i %i %i @%s\n",x,y,angle,s);
  fflush(stdout);
}

void setStringTextSize(int size)
{
  printf("SZ %i\n", size);
  fflush(stdout);
}

void displayImageURL(char* url, int x, int y)
{
  printf("DU %i %i @%s\n", x, y, url);
  fflush(stdout);
}

void displayImage(char* fileName, int x, int y)
{
  printf("DI %i %i @%s\n", x, y, fileName );
  fflush(stdout);
}

void setColour(colour c)
{
  char* colourName;
  switch(c)
  {
    case black : colourName = "black"; break;
    case blue : colourName = "blue"; break;
    case cyan : colourName = "cyan"; break;
    case darkgray : colourName = "darkgray"; break;
    case gray : colourName = "gray"; break;
    case green : colourName = "green"; break;
    case lightgray : colourName = "lightgray"; break;
    case magenta : colourName = "magenta"; break;
    case orange : colourName = "orange"; break;
    case pink : colourName = "pink"; break;
    case red : colourName = "red"; break;
    case white : colourName = "white"; break;
    case yellow : colourName = "yellow"; break;
    default : colourName = "black"; break;
  }
  printf("SC %s\n", colourName);
  fflush(stdout);
}

void setRGBColour(int red, int green, int blue)
{
  printf("RG %i %i %i\n", red, green, blue);
  fflush(stdout);
}

void clear(void)
{
  printf("CL\n");
  fflush(stdout);
}

void setWindowSize(int width, int height)
{
  printf("SW %i %i\n", width, height);
  fflush(stdout);
}

void sleep(int time)
{
  printf("SL %i\n", time);
  fflush(stdout);
}

void foreground(void)
{
  printf("FG\n");
  fflush(stdout);
}

void background(void)
{
  printf("BG\n");
  fflush(stdout);
}

void message(char *s)
{
  char *formatted = replaceNewlineWithEntity(s);
  if (formatted != NULL)
  {
    printf("MS @%s\n", formatted);
    fflush(stdout);
    free(formatted);
  }
}