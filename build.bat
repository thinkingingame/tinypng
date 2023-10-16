cd %cd%
rd /s /Q .\build
rd /s /Q .\dist
C:\Python3\Scripts\pyinstaller.exe -F -w main.py -n tinypng --add-binary "C:/Python3/tcl/tkdnd2.9.2;tkdnd2.9.2"

echo build success: %cd%\dist\tinypng.exe
pause