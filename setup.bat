@echo off
echo Starting setup...

echo Installing virtual environment...

python -m venv venv

echo Installing packages...

%cd%\venv\Scripts\pip install -r requirements.txt

echo Imported required packages.

echo Done, process finished.

PAUSE
