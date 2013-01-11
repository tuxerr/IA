import sys

from cx_Freeze import setup, Executable

base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
        name = "IA",
        version = "0.1",
        description = "IA",
        options = {"build_exe" : {"includes" : ["atexit","re"],"include_files":["resources"]}},
        executables = [Executable("main.py", base = base)])
