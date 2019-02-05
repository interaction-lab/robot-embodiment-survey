#!/bin/bash

echo $(pwd)
tar -czf docker/repo.tar.gz .
docker build -t docker.vadweb.us/robot-embodiment-survey docker
