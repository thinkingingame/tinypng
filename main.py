#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
import sys
import multiprocessing

from ui import *

# class _Popen(multiprocessing.Popen):
#     def __init__(self, *args, **kw):
#         if hasattr(sys, 'frozen'):
#             # We have to set original _MEIPASS2 value from sys._MEIPASS
#             # to get --onefile mode working.
#             os.putenv('_MEIPASS2', sys._MEIPASS)
#         try:
#             super(_Popen, self).__init__(*args, **kw)
#         finally:
#             if hasattr(sys, 'frozen'):
#                 # On some platforms (e.g. AIX) 'os.unsetenv()' is not
#                 # available. In those cases we cannot delete the variable
#                 # but only set it to the empty string. The bootloader
#                 # can handle this case.
#                 if hasattr(os, 'unsetenv'):
#                     os.unsetenv('_MEIPASS2')
#                 else:
#                     os.putenv('_MEIPASS2', '')

# class Process(multiprocessing.Process):
#     _Popen = _Popen

def main():
    pass

if __name__ == "__main__":
    if sys.platform.startswith('win'):
        # On Windows calling this function is necessary.
        multiprocessing.freeze_support()
    main()
    init_event()
    init_ui()