
FROM ubuntu:18.10

ENV TZ=US/Pacific
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN apt update && apt install -y \
	curl build-essential gnupg tzdata lsb-release libssl-dev libffi-dev
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
		uwsgi uwsgi-plugin-python3 \
		&& \
	npm install -g bower

WORKDIR /app
COPY requirements.txt ./
COPY bower.json ./
RUN pip3 install -r requirements.txt
RUN pip3 uninstall psycopg2 && pip3 install --no-binary :all: psycopg2
RUN bower --allow-root update

# TODO(Vadim) use only one database.ini
COPY repo.zip ./
RUN unzip repo.zip || ls
COPY database.ini ./

RUN cp deployment/nginx.conf /etc/nginx/ && cp deployment/nginx-site /etc/nginx/sites-available/default

EXPOSE 80
CMD nginx && uwsgi --ini /app/deployment/wsgi.ini

#COPY pg_hba.conf /etc/postgresql/10/main/
#RUN chmod 640 /etc/postgresql/10/main/pg_hba.conf && \
#	chown postgres:postgres /etc/postgresql/10/main/pg_hba.conf && \
#	sudo service postgresql restart && sleep 5 && \
#	# sudo -u postgres createdb postgres && \
#	sudo -u postgres /usr/lib/postgresql/10/bin/pg_ctl -D /usr/local/var/postgres reload
#
#COPY db_init.sql ./
#RUN su postgres && psql -f=db_init.sql

# RUN sudo -u postgres createdb postgres && \
#	sudo -u postgres psql postgres ALTER USER user_name WITH PASSWORD 'postgres' \q;
