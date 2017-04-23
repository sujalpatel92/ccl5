#!/bin/sh
python main_daemon.py &
sleep 2
python gps_from_phone.py &
python rpm_simulator.py &
python airflow_simulator.py &
python Messaging.py &
