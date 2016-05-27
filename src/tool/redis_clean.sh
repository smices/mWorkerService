#!/bin/bash
sudo service redis-server stop
sudo rm /var/lib/redis/dump.rdb
sudo service redis-server start
