#!/bin/bash
# launcher.sh
sudo apt-get install nginx supervisor
python3 -m venv venv
. venv/bin/activate
pip install -r requirements.txt
pip install gunicorn
sudo cp supervisor_conf.conf /etc/supervisor/conf.d/azan_app.conf
sudo supervisorctl reread
sudo service supervisor restart