FROM postgres:13-alpine

# Setting timezone to Los Angeles
RUN apk add -U tzdata
RUN ["cp", "/usr/share/zoneinfo/America/Los_Angeles", "/etc/localtime"]

# Initializing database extensions and tables
COPY create-extension.sh /docker-entrypoint-initdb.d/
COPY initdb.sql /docker-entrypoint-initdb.d/