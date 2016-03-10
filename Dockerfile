FROM rwang/centos-flask

MAINTAINER Ruiyu Wang "deanmax@gmail.com"

COPY . /FlaskAPP
WORKDIR /FlaskAPP

ENTRYPOINT ["python", "run.py"]
