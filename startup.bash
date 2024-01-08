#!/usr/bin/env bash
# Arthur: NyboMønster

SN=FlaskIAM

cd || exit 1
. /home/Gruppe2PI/Projekts/IOHTProjekt/FlaskEnviroment/FlaskEnviroment/bin/activate || exit 1
cd || exit 1
cd /home/Gruppe2PI/Projekts/IOHTProjekt/Hjemmeside || exit 1

pkill -f "flask run --host=192.168.57.54 --port=2916" && pkill -f "flask run --host=192.168.29.116 --port=2916"

hostip=$(hostname -I | awk '{print $1}')
echo $hostip
if screen -list | grep -q "$SN"; then
	echo "Screen session $SN already exists"
else
	if [ "$hostip" == "192.168.29.116" ]; then  
		screen -dmS $SN bash -c "flask run --host=192.168.29.116 --port=2916 && sleep 5; screen -X detach"
		# echo "Flask application started successfully on host 192.168.29.116"
	else
		if [ "$hostip" == "192.168.57.54" ]; then
			screen -dmS $SN bash -c "flask run --host=192.168.57.54 --port=2916 && sleep 5; screen -X detach" 
			# echo "Flask Application started successfully on host 192.168.57.54"
		else
			echo "Failed to host webpage"
		fi
	fi
fi

