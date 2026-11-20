#include "solver.h"
#include "maze.h"
#include "drawing.h"

// note: this DFS doesnt have a visited array so it cannot solve mazes with loops. it relies on the generator producing mazes without loops.
int explore(Robot* robot, int cellGrid[MAX_GRID_WIDTH][MAX_GRID_HEIGHT], Vec2 previousPosition, int width, int height) {
    if (isInsideGrid(previousPosition, width, height)) {
        drawTrailSegment(previousPosition, robot->pos, blue);
    }

    if (atMarker(robot, cellGrid)) {
        return 1;
    }

    Vec2 currentPosition = robot->pos;

    // If the robot sees the exit cell is adjacent to its current position it immediately should move to the exit and return success
    for (int i = 0; i < DIRECTION_COUNT; i++) {
        Vec2 offset = DIRECTION_OFFSETS[i];
        Vec2 nextPosition = {currentPosition.x + offset.x, currentPosition.y + offset.y};

        if (isInsideGrid(nextPosition, width, height) && cellGrid[nextPosition.x][nextPosition.y] == EXIT_CELL) {
            turn(robot, (Direction)i);
            forward(robot, cellGrid, width, height);
            return explore(robot, cellGrid, currentPosition, width, height);
        }
    }

    for (int i = 0; i < DIRECTION_COUNT; i++) {
        Vec2 directionOffset = DIRECTION_OFFSETS[i];
        Vec2 nextPosition = {currentPosition.x + directionOffset.x, currentPosition.y + directionOffset.y};

        if (nextPosition.x == previousPosition.x && nextPosition.y == previousPosition.y) {
            continue;
        }

        if (!isInsideGrid(nextPosition, width, height) || cellGrid[nextPosition.x][nextPosition.y] == WALL_CELL) {
            continue;
        }

        turn(robot, (Direction)i);
        forward(robot, cellGrid, width, height);

        if (explore(robot, cellGrid, currentPosition, width, height)) {
            return 1;
        }

        // A failed branch must physically return before another direction is tried.
        turn(robot, (Direction)((i + 2) % DIRECTION_COUNT));
        forward(robot, cellGrid, width, height);
        drawTrailSegment(nextPosition, currentPosition, red);
    }
    
    return 0;
}
