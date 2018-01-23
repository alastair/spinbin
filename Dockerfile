FROM python:2.7

RUN wget -O /usr/local/bin/dumb-init https://github.com/Yelp/dumb-init/releases/download/v1.2.0/dumb-init_1.2.0_amd64 \
    && chmod +x /usr/local/bin/dumb-init

RUN mkdir /code
WORKDIR /code

ADD requirements /code
RUN pip install --no-cache-dir -r requirements

ADD . /code/
