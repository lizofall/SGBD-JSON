#!/bin/bash
python3 server.py > /dev/null &
sleep 5

python3 app.py