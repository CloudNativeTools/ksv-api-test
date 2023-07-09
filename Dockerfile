FROM docker.io/qiaoshilu/devops-python

MAINTAINER qiaoshilu@yunify.com

RUN mkdir -p /data/autotest

ADD . /data/autotest

WORKDIR /data/autotest

RUN pip install -r requirements.txt