Compress-Archive * repo.zip
Move-Item -Force repo.zip docker\
docker build -t docker.vadweb.us/robot-embodiment-survey docker