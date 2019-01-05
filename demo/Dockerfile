From ubuntu:18.04

MAINTAINER Katsuya SHIMABUKURO <katsu.generation.888@gmail.com>

RUN apt-get update && \
    apt-get install -y python3 python3-dev python3-pip python3-venv build-essential git mongodb && \
    apt-get clean

RUN ln -s /usr/bin/pip3 /usr/bin/pip

WORKDIR /var/local/
RUN git clone https://github.com/katsugeneration/chatql
WORKDIR /var/local/chatql
RUN pip3 install poetry
RUN poetry install --no-dev -v
RUN poetry run pip install wheel
RUN poetry run pip install flask flask-graphql

ADD ./ /var/local/chatql/demo/
WORKDIR /var/local/chatql/demo
RUN mkdir mongodb
RUN chmod 744 run.sh
ENTRYPOINT ["sh", "./run.sh"]
