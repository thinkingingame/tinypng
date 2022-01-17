rd /s /Q D:\work\superpng\build
rd /s /Q D:\work\superpng\dist
C:\Python310\Scripts\pyinstaller.exe -F -w main.py --add-binary "C:/Python310/tcl/tkdnd2.8;tkdnd2.8"