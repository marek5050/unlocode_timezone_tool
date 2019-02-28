# Dockerfile for example whisk docker action
FROM openwhisk/dockerskeleton

ENV FLASK_PROXY_PORT 8080
ENV REFRESHED_AT 2019-01-27T13:59:39Z

### Add source file(s)
ADD requirements.txt /action/requirements.txt

RUN apk add --no-cache mariadb-dev g++ py-mysqldb && \
    pip install --no-cache-dir -r /action/requirements.txt

ADD *.py /action/
ADD exec /action/exec


CMD ["/bin/bash", "-c", "cd actionProxy && python -u actionproxy.py"]