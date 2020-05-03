FROM tiangolo/uvicorn-gunicorn:python3.8-alpine3.10

LABEL maintainer="Sebastian Ramirez <tiangolo@gmail.com>"

COPY . /app

RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.aliyun.com/g' /etc/apk/repositories && apk add linux-headers musl-dev zlib-dev jpeg-dev gcc tiff-dev && pip install --upgrade pip -i https://mirrors.aliyun.com/pypi/simple/ 

RUN pip install -r /app/requirements.txt -i https://mirrors.aliyun.com/pypi/simple/

VOLUME /tmp/upload