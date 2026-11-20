#include "drawing.h"

void drawCell(int cellType, Vec2 position) {
    if (cellType == WALL_CELL) {
        setColour(black);
    } else if (cellType == EXIT_CELL) {
        setColour(gray);
    } else {
        setColour(white);
    }
    fillRect(position.x * CELL_SIZE + 1, position.y * CELL_SIZE + 1,
             CELL_SIZE - 1, CELL_SIZE - 1);
}

void drawRobot(const Robot* robot) {
    Vec2 facing = DIRECTION_OFFSETS[robot->dir];
    Vec2 sideways = {-facing.y, facing.x};
    Vec2 centre = cellCentre(robot->pos);
    int halfSize = CELL_SIZE / 3;

    // The tip points forward and the rear corners lie on either side of the centre.
    int xPoints[3] = {
        centre.x + facing.x * halfSize,
        centre.x - facing.x * halfSize + sideways.x * halfSize,
        centre.x - facing.x * halfSize - sideways.x * halfSize
    };
    int yPoints[3] = {
        centre.y + facing.y * halfSize,
        centre.y - facing.y * halfSize + sideways.y * halfSize,
        centre.y - facing.y * halfSize - sideways.y * halfSize
    };

    foreground();
    clear();
    setColour(green);
    fillPolygon(3, xPoints, yPoints);
}

void drawMaze(int cellGrid[MAX_GRID_WIDTH][MAX_GRID_HEIGHT], int width, int height) {
    background();
    for (int x = 0; x < width; x++) {
        for (int y = 0; y < height; y++) {
            drawCell(cellGrid[x][y], (Vec2){x, y});
        }
    }
}

Vec2 cellCentre(Vec2 position) {
    return (Vec2){
        position.x * CELL_SIZE + CELL_SIZE / 2,
        position.y * CELL_SIZE + CELL_SIZE / 2
    };
}

void drawTrailSegment(Vec2 from, Vec2 to, colour trailColour) {
    Vec2 start = cellCentre(from);
    Vec2 end = cellCentre(to);

    // Background trails survive the foreground clear in drawRobot().
    background();
    setColour(trailColour);
    drawLine(start.x, start.y, end.x, end.y);
    foreground();
}
