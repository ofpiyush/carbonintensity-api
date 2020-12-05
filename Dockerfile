FROM python:3.7.0

ADD . /root

WORKDIR /root

RUN pip install -r /root/requirements.txt
RUN git submodule update --init --recursive
RUN pip install -r /root/electricitymapcontrib/parsers/requirements.txt

ENTRYPOINT ["gunicorn", "--config", "gunicorn_config.py", "app:app"]