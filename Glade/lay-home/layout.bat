rem set GLADE_USE_OPENGL=no

rem ************  Substitute your actual glade installation dir ****

set GLADE_HOME=C:\Users\rafus\Documents\Programmi microelettronica analogica\Glade\glade4_win64

rem ****************************************************************

set PYTHONHOME=%GLADE_HOME%\Python27
set PATH=%GLADE_HOME%;%PATH%
set PYTHONPATH=%PYTHONHOME%;%GLADE_HOME%;.
set GLADE_LOGFILE_DIR=.
set HOME=.

del .\*.log

start /b glade
