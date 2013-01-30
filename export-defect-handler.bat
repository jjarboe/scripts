@ECHO OFF

rem SCRIPT_DIR contains the absolute path to the directory where the
rem export-defect-handler.py script is located.

SET SCRIPT_DIR=

rem Set these values to something appropriate for your installation.

SET USER=admin
SET PASSWORD=coverity
SET HOST=localhost
SET PORT=8651

cd %SCRIPT_DIR%
python export-defect-handler.py --inputfile=%1 --user=%USER% --password=%PASSWORD% --host=%HOST% --port=%PORT%
