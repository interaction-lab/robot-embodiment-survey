
FROM ubuntu:18.10

ENV TZ=US/Pacific
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN apt update && apt install -y \
	curl build-essential gnupg tzdata lsb-release
RUN curl -sL https://deb.nodesource.com/setup_10.x | bash - && \
	apt update && \
	apt install -y \
		nodejs \
		git \
		tar \
		zip \
		unzip \
		vim \
		nginx \
		python3 python3-pip python3-psycopg2 \
		postgresql postgresql-contrib \
		sudo \
		&& \
	npm install -g bower

WORKDIR /deployment
COPY repo.zip ./
RUN unzip repo.zip || ls
COPY database.ini ./

RUN pip3 install -r requirements.txt
RUN bower --allow-root update

COPY pg_hba.conf /etc/postgresql/10/main/
RUN chmod 640 /etc/postgresql/10/main/pg_hba.conf && \
	chown postgres:postgres /etc/postgresql/10/main/pg_hba.conf && \
	sudo service postgresql restart && sleep 5 && \
	# sudo -u postgres createdb postgres && \
	sudo -u postgres /usr/lib/postgresql/10/bin/pg_ctl -D /usr/local/var/postgres reload

COPY db_init.sql ./
RUN su postgres && psql -f=db_init.sql
# RUN sudo -u postgres createdb postgres && \
#	sudo -u postgres psql postgres ALTER USER user_name WITH PASSWORD 'postgres' \q;
