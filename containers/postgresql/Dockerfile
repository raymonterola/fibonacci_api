FROM postgres:14.6-alpine
COPY ./sql/000.sql /docker-entrypoint-initdb.d/
COPY ./sql/001.sql /docker-entrypoint-initdb.d/
RUN ls /docker-entrypoint-initdb.d/