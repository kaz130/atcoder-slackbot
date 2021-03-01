FROM golang:1.16.0
ADD . /code
# ENV http_proxy
# ENV https_proxy
WORKDIR /code
ENV TZ=Asia/Tokyo

RUN apt-get update
RUN apt-get install -y busybox-static

COPY crontab /var/spool/cron/crontabs/root

CMD ["busybox", "crond", "-f", "-L", "/dev/stderr"]

