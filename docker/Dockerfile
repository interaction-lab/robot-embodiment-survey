
FROM ubuntu:18.10

ENV TZ=US/Pacific
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN apt update && apt install -y \
	curl build-essential gnupg tzdata
RUN curl -sL https://deb.nodesource.com/setup_10.x | bash - && \
	apt update && \
	apt install -y \
		nodejs git tar nginx postgresql postgresql-contrib python3 python3-pip \
		&& \
	npm install -g bower

WORKDIR /deployment
COPY repo.tar.gz ./
RUN tar xzf repo.tar.gz
COPY database.ini ./

RUN pip3 install -r requirements.txt
RUN bower --allow-root update
