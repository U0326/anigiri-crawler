# 親階層に存在するsrcフォルよりCOPYを行う為に、
# 01_crawlerフォルダで以下コマンドを発行する必要がある。
# build -f docker/app/Dockerfile . -t anigiri/app
FROM python:3.7.0-stretch

RUN apt-get update
RUN apt-get -y install locales && \
    localedef -f UTF-8 -i ja_JP ja_JP.UTF-8
ENV LANG ja_JP.UTF-8
ENV LANGUAGE ja_JP:ja
ENV LC_ALL ja_JP.UTF-8
ENV TZ JST-9
ENV TERM xterm

RUN pip install --upgrade pip
RUN pip install --upgrade setuptools

WORKDIR /opt/anigiri
COPY ./src/requirements.txt /opt/anigiri/
RUN pip install -r ./requirements.txt
RUN apt-get --yes install mysql-client
RUN mkdir -p /var/run/mysqld
RUN touch /var/run/mysqld/mysqld.sock
