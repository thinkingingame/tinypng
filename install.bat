cd %cd%
rd /s /Q .\build
rd /s /Q .\dist
C:\Python310\Scripts\pyinstaller.exe -F -w main.py -n tinypng --add-binary "C:/Python310/tcl/tkdnd2.8;tkdnd2.8"