#!/usr/bin/env bash
# Arthur: NyboMønster

if screen -list | grep -q "flaskInterActiveMenu"; then
	screen -S flaskInterActiveMenu -X quit
else
	echo 'no session in that name'
fi

screen -S flaskInterActiveMenu -dm bash -c 'export FLASK_APP=app.py; export FLASK_RUN_HOST=192.168.29.116; export FLASK_RUN_PORT=2916; flask run'
