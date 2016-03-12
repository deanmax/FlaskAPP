FROM rwang/centos-flask

MAINTAINER Ruiyu Wang "deanmax@gmail.com"

COPY . /FlaskAPP
WORKDIR /FlaskAPP
CMD ["export", "LD_LIBRARY_PATH=/usr/local/lib"]

ENTRYPOINT ["python", "run.py"]
