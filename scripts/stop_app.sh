#!/usr/bin/bash 

sed -i 's/\[]/\["13.201.89.221"]/' /home/ubuntu/venue-management-system/vms/settings.py

sudo service gunicorn stop
sudo service nginx stop