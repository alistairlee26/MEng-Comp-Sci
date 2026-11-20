# Maze generator and robot solver

The program draws a random maze, then animates a robot exploring it. Blue lines
show the current path and red lines show branches abandoned after backtracking.

the maze solver uses DFS by recursively exploring the maze. It only remembers the previous cell it was at,
and does not utilize a visited array. This means it is limited to mazes that does not have any loops.

The maze generator is uses a random DFS and backtracking to create passages, so it does not produce a maze with loops.

To compile and run with default arguments:

```powershell
gcc -Wall -Wextra main.c maze.c robot.c drawing.c solver.c graphics.c -o drawing.exe
./drawing.exe | java -jar drawapp-5.0.jar
```

There are 5 optional arguments, use `--name value` pairs:

`--seed` allows you to set the seed for the random number generator used in maze generation, setting the same seed results in the same maze being generated. The default seed is the current time.

`--width` sets the width of the maze in cells. Default: 25 cells

`--height` sets the height of the maze in cells. Default: 25 cells

`--generation-delay` sets the delay in ms between each maze generation step. Default: 10ms

`--robot-delay` sets the delay in ms between each robot move, or robot turn. Default: 50ms

Example:
```powershell
./drawing.exe --seed 0 --width 25 --height 25 --generation-delay 10 --robot-delay 50 | java -jar drawapp-5.0.jar
```