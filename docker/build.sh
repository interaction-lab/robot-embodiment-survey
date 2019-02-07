#!/bin/bash

echo $(pwd)
zip -r docker/repo.zip .
docker build -t docker.vadweb.us/robot-embodiment-survey docker
