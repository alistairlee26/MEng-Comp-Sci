#pragma once

#include "common.h"

typedef struct Robot {
    Vec2 pos;
    Direction dir;
    int delayMs;
} Robot;

int atMarker(const Robot* robot, int cellGrid[MAX_GRID_WIDTH][MAX_GRID_HEIGHT]);
int canMoveForward(const Robot* robot, int cellGrid[MAX_GRID_WIDTH][MAX_GRID_HEIGHT], int width, int height);
void sleepAndRedrawRobot(const Robot* robot);
void forward(Robot* robot, int cellGrid[MAX_GRID_WIDTH][MAX_GRID_HEIGHT], int width, int height);
void left(Robot* robot);
void right(Robot* robot);
void turn(Robot* robot, Direction newDirection);

