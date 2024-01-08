#!/usr/bin/env bash
# Arthur: NyboMønster

SN=FlaskIAM

cd
pwd
sleep 1
cd /home/Gruppe2PI/Projekts/IOHTProjekt/
pwd
sleep 1
. FlaskEnviroment/FlaskEnviroment/bin/activate 
sleep 1
cd
sleep 1
cd /home/Gruppe2PI/Projekts/IOHTProjekt/Hjemmeside
sleep 1

if (flask run --host=192.168.29.116 --port=2916 & sleep 5 && screen -S $SN -X sessionname $SN) & then
	echo "Flask application started successfully on host 192.168.29.116"
else
	if (flask run --host=192.168.57.54 --port=2916 & sleep 5 && screen -S $SN -X sessionname $SN) & then
		echo "Flask Application started successfully on host 192.168.57.54"
	else
		echo "Failed to host webpage"
	fi
fi

