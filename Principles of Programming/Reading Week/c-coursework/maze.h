#pragma once

#include "common.h"

void shuffleDirections(Vec2 directions[], int size);
void createPassages(int cellGrid[MAX_GRID_WIDTH][MAX_GRID_HEIGHT], Vec2 currentPosition, int width, int height, int generationDelay);
void createMaze(int cellGrid[MAX_GRID_WIDTH][MAX_GRID_HEIGHT], int width, int height, int generationDelay);
int isInsideGrid(Vec2 position, int width, int height);

