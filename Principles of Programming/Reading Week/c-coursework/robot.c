#include "robot.h"
#include "maze.h"
#include "drawing.h"

int atMarker(const Robot* robot, int cellGrid[MAX_GRID_WIDTH][MAX_GRID_HEIGHT]) {
    return cellGrid[robot->pos.x][robot->pos.y] == EXIT_CELL;
}

int canMoveForward(const Robot* robot, int cellGrid[MAX_GRID_WIDTH][MAX_GRID_HEIGHT], int width, int height) {
    Vec2 forwardPosition = {robot->pos.x + DIRECTION_OFFSETS[robot->dir].x, robot->pos.y + DIRECTION_OFFSETS[robot->dir].y};
    return isInsideGrid(forwardPosition, width, height) && cellGrid[forwardPosition.x][forwardPosition.y] != WALL_CELL;
}

void sleepAndRedrawRobot(const Robot* robot) {
    sleep(robot->delayMs);
    drawRobot(robot);
}

void forward(Robot* robot, int cellGrid[MAX_GRID_WIDTH][MAX_GRID_HEIGHT],
             int width, int height) {
    if (!canMoveForward(robot, cellGrid, width, height)) {
        return;
    }

    robot->pos.x += DIRECTION_OFFSETS[robot->dir].x;
    robot->pos.y += DIRECTION_OFFSETS[robot->dir].y;
    sleepAndRedrawRobot(robot);
}

void left(Robot* robot) {
    robot->dir = (robot->dir + DIRECTION_COUNT - 1) % DIRECTION_COUNT;
    sleepAndRedrawRobot(robot);
}

void right(Robot* robot) {
    robot->dir = (robot->dir + 1) % DIRECTION_COUNT;
    sleepAndRedrawRobot(robot);
}

void turn(Robot* robot, Direction newDirection) {
    int clockwiseTurns = (newDirection - robot->dir + DIRECTION_COUNT) % DIRECTION_COUNT;

    if (clockwiseTurns == DIRECTION_COUNT - 1) {
        left(robot);
    } else {
        for (int i = 0; i < clockwiseTurns; i++) {
            right(robot);
        }
    }
}
