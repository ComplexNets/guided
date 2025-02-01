@echo off
echo Starting Journal Project Setup...

REM Activate conda environment
call C:\Users\X1\miniconda3\Scripts\activate.bat journal

REM Run Django development server
echo Starting Django development server...
python manage.py runserver

REM Keep window open if there's an error
pause
