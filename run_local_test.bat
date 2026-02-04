@echo off
cd /d "%~dp0"
REM Local MQTT test: run mosquitto -p 1883 first, then run this bat
set REFEREE_MQTT_HOST=127.0.0.1
set REFEREE_MQTT_PORT=1883
python -m rm_client.main
pause
