FROM python:3.7.2-slim-stretch

RUN apt-get update
RUN apt-get -y install locales && \
    localedef -f UTF-8 -i ja_JP ja_JP.UTF-8
ENV LANG ja_JP.UTF-8
ENV LANGUAGE ja_JP:ja
ENV LC_ALL ja_JP.UTF-8
ENV TZ JST-9
RUN apt-get -y install default-libmysqlclient-dev
RUN apt-get -y install mysql-client
RUN apt-get -y install build-essential
RUN mkdir -p /var/run/mysqld
RUN touch /var/run/mysqld/mysqld.sock

RUN pip install --upgrade pip
RUN pip install --upgrade setuptools

WORKDIR /opt/anigiri-crawler
COPY src/ /opt/anigiri-crawler/
RUN pip install -r ./requirements.txt

