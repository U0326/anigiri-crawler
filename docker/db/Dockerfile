FROM mysql:5.7
RUN apt-get update
RUN apt-get -y install locales && \
    localedef -f UTF-8 -i ja_JP ja_JP.UTF-8
ENV LANG ja_JP.UTF-8
ENV LANGUAGE ja_JP:ja
ENV LC_ALL ja_JP.UTF-8
ENV TZ JST-9
ENV TERM xterm

COPY ./ddl /docker-entrypoint-initdb.d
ENV MYSQL_ROOT_PASSWORD password
ENV MYSQL_DATABASE anigiri_db
ENV MYSQL_USER anigiri
ENV MYSQL_PASSWORD password

# データを永続化する為、ホスト側のディレクトリを以下パスにマウントすること。
VOLUME /var/lib/mysql/
