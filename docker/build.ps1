Compress-Archive * repo.zip
Move-Item -Force repo.zip docker\
Copy-Item -Force requirements.txt docker\
Copy-Item -Force bower.json docker\
docker build -t docker.vadweb.us/robot-embodiment-survey docker