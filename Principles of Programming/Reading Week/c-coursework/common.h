#pragma once

#define EMPTY_CELL 0
#define WALL_CELL 1
#define EXIT_CELL 2

#define DEFAULT_GRID_WIDTH 25
#define DEFAULT_GRID_HEIGHT 25

#define CELL_SIZE 20

#define MIN_GRID_SIZE 3
#define MAX_GRID_WIDTH (2500 / CELL_SIZE)
#define MAX_GRID_HEIGHT (1500 / CELL_SIZE)

#define DEFAULT_GENERATION_DELAY_MS 10
#define DEFAULT_ROBOT_DELAY_MS 50

#define DIRECTION_COUNT 4

typedef struct Vec2 {
    int x;
    int y;
} Vec2;

typedef enum Direction {
    UP,
    RIGHT,
    DOWN,
    LEFT
} Direction;

static const Vec2 DIRECTION_OFFSETS[DIRECTION_COUNT] = {
    {0, -1}, // UP
    {1, 0}, // RIGHT
    {0, 1}, // DOWN
    {-1, 0} // LEFT
};

