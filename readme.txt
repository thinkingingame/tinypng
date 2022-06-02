install dependencies:

pip3 install requests
pip3 install pyyaml

pip3 install ndg-httpsclient
pip3 install pyopenssl
pip3 install pyasn1

pip3 install pyinstaller

copy files:
tkdnd2.8 -> C:/Python310/tcl


build:
C:\Python310\Scripts\pyinstaller.exe -F -w main.py --add-binary "C:/Python310/tcl/tkdnd2.8;tkdnd2.8"