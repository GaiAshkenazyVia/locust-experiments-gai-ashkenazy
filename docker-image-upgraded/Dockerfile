FROM python:3.9-alpine

COPY docker-entrypoint.sh /
COPY requirements.txt /

RUN    apk --no-cache add --virtual=.build-dep build-base \
    && apk --no-cache add libzmq \
    && apk --no-cache add libffi-dev \
    && apk --no-cache add librdkafka-dev \
    && python3.9 -m pip install --no-cache-dir --upgrade pip \
    && python3.9 -m pip install --no-cache-dir -r requirements.txt \
    && apk del .build-dep \
    && chmod +x /docker-entrypoint.sh

RUN  mkdir /locust
WORKDIR /locust
EXPOSE 8089 5557-5577

ENTRYPOINT ["/docker-entrypoint.sh"]
