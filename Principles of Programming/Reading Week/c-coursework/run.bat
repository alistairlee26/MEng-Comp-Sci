@echo off
setlocal
pushd "%~dp0"

set "GCC_BIN=%LOCALAPPDATA%\Microsoft\WinGet\Packages\BrechtSanders.WinLibs.POSIX.UCRT_Microsoft.Winget.Source_8wekyb3d8bbwe\mingw64\bin"
if exist "%GCC_BIN%\gcc.exe" set "PATH=%GCC_BIN%;%PATH%"

echo Compiling...
gcc -std=c17 -Wall -Wextra -pedantic main.c maze.c robot.c drawing.c solver.c graphics.c -o drawing.exe
if errorlevel 1 goto error

echo Opening DrawApp...
drawing.exe %* | java -jar drawapp-5.0.jar
if errorlevel 1 goto error

popd
exit /b 0

:error
echo.
echo Could not compile or run the program. Check the error above.
pause
popd
exit /b 1
