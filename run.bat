@echo off
cd /d "%~dp0"
REM If ModuleNotFoundError: pip install -r requirements.txt
python -m rm_client.main
pause
