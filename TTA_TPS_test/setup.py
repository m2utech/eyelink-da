import sys, os
from cx_Freeze import setup, Executable

LOCAL_TO_PYTHON = os.path.dirname(os.path.dirname(os.__file__))

os.environ['TCL_LIBRARY'] = os.path.join(LOCAL_TO_PYTHON, 'tcl', 'tcl8.6')
os.environ['TK_LIBRARY'] = os.path.join(LOCAL_TO_PYTHON, 'tcl', 'tk8.6')

buildOptions = dict(packages=["numpy"], excludes = [])
base = 'Win32GUI' if sys.platform=='win32' else None
executables = [Executable("throughput_test.py", base=base)]

setup( name = "Throughput_Test",
       version = "1.0",
       description = "Throughput test for V&V test of TTA",
       options = dict(build_exe = buildOptions),
       author = "M2U Technology",
       executables = executables
)
