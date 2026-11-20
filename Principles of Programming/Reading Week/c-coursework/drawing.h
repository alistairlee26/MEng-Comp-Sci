#pragma once

#include "graphics.h"
#include "robot.h"

void drawCell(int cellType, Vec2 position);
void drawRobot(const Robot* robot);
void drawMaze(int cellGrid[MAX_GRID_WIDTH][MAX_GRID_HEIGHT], int width, int height);
Vec2 cellCentre(Vec2 position);
void drawTrailSegment(Vec2 from, Vec2 to, colour trailColour);

