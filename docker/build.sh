#!/bin/bash

echo $(pwd)
cp requirements.txt docker
cp bower.json docker
cp database.ini docker
zip -r docker/repo.zip .
docker build -t docker.vadweb.us/robot-embodiment-survey docker
