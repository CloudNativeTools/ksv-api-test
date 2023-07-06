FROM docker.io/ben950128/python3.9.13-slim_psycopg2

MAINTAINER qiaoshilu@yunify.com

RUN mkdir -p /data/autotest

ADD . /data/autotest

WORKDIR /data/autotest

RUN pip install -r requirements.txt -i https://4kt7dp2z.mirror.aliyuncs.com