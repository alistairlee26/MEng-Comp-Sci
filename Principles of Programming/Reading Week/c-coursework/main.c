#include "maze.h"
#include "robot.h"
#include "drawing.h"
#include "solver.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

int main(int argc, char* argv[]) {
    int width = DEFAULT_GRID_WIDTH;
    int height = DEFAULT_GRID_HEIGHT;
    int robotDelay = DEFAULT_ROBOT_DELAY_MS;
    int generationDelay = DEFAULT_GENERATION_DELAY_MS;
    unsigned int seed = (unsigned int)time(NULL);

    // Read optional --name value pairs
    for (int i = 1; i < argc; i += 2) {
        // Parse string to int
        unsigned int value = atoi(argv[i + 1]);
        if (strcmp(argv[i], "--seed") == 0) {
            seed = value;
            continue;
        }
        
        if (strcmp(argv[i], "--width") == 0) { 
            width = value;
        } else if (strcmp(argv[i], "--height") == 0) {
            height = value;
        } else if (strcmp(argv[i], "--robot-delay") == 0){
            robotDelay = value;
        } else if (strcmp(argv[i], "--generation-delay") == 0) { 
            generationDelay = value;
        } else {
            printf("Unknown argument: %s\n", argv[i]);
            return 1;
        }
    }

    if (width < MIN_GRID_SIZE || width > MAX_GRID_WIDTH ||
        height < MIN_GRID_SIZE || height > MAX_GRID_HEIGHT) {
        printf("Width must be %d-%d cells and height %d-%d cells.\n",
                MIN_GRID_SIZE, MAX_GRID_WIDTH, MIN_GRID_SIZE, MAX_GRID_HEIGHT);
        return 1;
    }

    // Reserve the maximum grid size; only width by height cells are used.
    int cellGrid[MAX_GRID_WIDTH][MAX_GRID_HEIGHT];

    int windowWidth = width * CELL_SIZE;
    int windowHeight = height * CELL_SIZE;
    setWindowSize(windowWidth, windowHeight);
    background();
    setColour(black);
    fillRect(0, 0, windowWidth, windowHeight);

    srand(seed);
    createMaze(cellGrid, width, height, generationDelay);

    Robot robot = {{0, 1}, RIGHT, robotDelay};
    drawRobot(&robot);

    // An invalid parent position on the grid indicates the root of the search tree
    int solved = explore(&robot, cellGrid, (Vec2){-1, -1}, width, height);
    if (!solved) {
        fprintf(stderr, "The robot could not reach the exit.\n");
        return EXIT_FAILURE;
    }
    return EXIT_SUCCESS;
}
