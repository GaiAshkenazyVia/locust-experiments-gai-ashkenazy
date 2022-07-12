## Docs for running by Gai Ashkenazy

# Run a stand alone against a client side that runs in localhost:3000
1. cd to docker-image dir
2. build the docker image. run `docker build -t gaiashkenazy/locust-old:latest .`
3. edit the locustfile.py in the locust directory to match the load testing that you need
4. run the docker container. run 
`docker run --name standalone --hostname standalone -e ATTACKED_HOST=http://host.docker.internal:3000 -v /Users/gai.ashkenazy/workspace/locust-sandbox/locust-experiments-gai-ashkenazy/docker-image/locust:/locust -p 8089:8089 --add-host=host.docker.internal:host-gateway --rm -d gaiashkenazy/locust-old`
5. open the locust ui in this url: `http://127.0.0.1:8089/` and see the stats

# Run master with 2 slave against a client side that runs in localhost:3000
1. use the same docker image as above
2. cd to docker-image dir
3. build the docker image. run `docker build -t gaiashkenazy/locust-old:latest .`
4. edit the locustfile.py in the locust directory to match the load testing that you need
5. run the master docker container. run 
`docker run --name master --hostname master -p 8089:8089 -p 5557:5557 -p 5558:5558 -v /Users/gai.ashkenazy/workspace/locust-sandbox/locust-experiments-gai-ashkenazy/docker-image/locust:/locust -e ATTACKED_HOST=http://host.docker.internal:3000 -e LOCUST_MODE=master --add-host=host.docker.internal:host-gateway --rm -d gaiashkenazy/locust-old`
6. run the slave 1 docker container. run
`docker run --name slave0 --link master --env NO_PROXY=master -v /Users/gai.ashkenazy/workspace/locust-sandbox/locust-experiments-gai-ashkenazy/docker-image/locust:/locust -e ATTACKED_HOST=http://host.docker.internal:3000 -e LOCUST_MODE=slave -e LOCUST_MASTER=master --rm -d gaiashkenazy/locust-old`
7. run the slave 2 docker container. run
`docker run --name slave1 --link master --env NO_PROXY=master -v /Users/gai.ashkenazy/workspace/locust-sandbox/locust-experiments-gai-ashkenazy/docker-image/locust:/locust -e ATTACKED_HOST=http://host.docker.internal:3000 -e LOCUST_MODE=slave -e LOCUST_MASTER=master --rm -d gaiashkenazy/locust-old`
8. And so on for more slaves (be sure to export more ports - this will require to build the docker image again)
`docker run --name slave2 --link master --env NO_PROXY=master -v /Users/gai.ashkenazy/workspace/locust-sandbox/locust-experiments-gai-ashkenazy/docker-image/locust:/locust -e ATTACKED_HOST=http://host.docker.internal:3000 -e LOCUST_MODE=slave -e LOCUST_MASTER=master --rm -d gaiashkenazy/locust-old`
`docker run --name slave3 --link master --env NO_PROXY=master -v /Users/gai.ashkenazy/workspace/locust-sandbox/locust-experiments-gai-ashkenazy/docker-image/locust:/locust -e ATTACKED_HOST=http://host.docker.internal:3000 -e LOCUST_MODE=slave -e LOCUST_MASTER=master --rm -d gaiashkenazy/locust-old`
`docker run --name slave4 --link master --env NO_PROXY=master -v /Users/gai.ashkenazy/workspace/locust-sandbox/locust-experiments-gai-ashkenazy/docker-image/locust:/locust -e ATTACKED_HOST=http://host.docker.internal:3000 -e LOCUST_MODE=slave -e LOCUST_MASTER=master --rm -d gaiashkenazy/locust-old`
11. open the locust ui in this url: `http://127.0.0.1:8089/` and see the stats


    Recently a new version of Locust was released so I decided to use this as an excuse to refresh the docker image and show information on how to use it.
    
    I decided to create a dedicated repository for the project. If you visit https://github.com/karol-brejna-i/docker-locust, you’ll notice that the repo is organized so it can maintain many versions of the image.

### Please, visit https://github.com/karol-brejna-i/docker-locust for the latest version of the docker image.


# Dockerizing Locust experiment
I wanted the image to:
* use Python 3
* use the latest version of Locust
* be as small as possible
* be simple to use
* take Locust scripts by means of mounting a volume

Most of the images found on docker hub was old (1-2 yo) so I decided to give it a try.

This one is based on python:3.6-alpine, installs `locustio` package and required dependencies. 
It weighs about 124MB.
 
# Usage 
The image doesn't include locust scripts during build. It assumes, the scripts will be supplied on runtime by mounting a volume (to `/locust` path).

## Building the image
```
docker build -t grubykarol/locust:0.8.1-py3.6 .
```
or (if behind a proxy):
```
docker build --build-arg HTTP_PROXY=$http_proxy --build-arg HTTPS_PROXY=$https_proxy -t grubykarol/locust:0.8.1-py3.6 . 
```

## Running the image
The image uses the following environment variables to configure its behavior:

| Variable | Description | Default | Example |
|----------|-------------|---------|---------|
|LOCUST_FILE   | Sets the `--locustfile` option. | locustfile.py | |
|ATTACKED_HOST | The URL to test. Required. | - | http://example.com |
|LOCUST_MODE   | Set the mode to run in. Can be `standalone`, `master` or `slave`. | standalone | master |
|LOCUST_MASTER | Locust master IP or hostname. Required for `slave` mode.| - | 127.0.0.1 |
|LOCUST_MASTER_BIND_PORT | Locust master port. Used in `slave` mode. | 5557 | 6666 |
|LOCUST_OPTS| Additional locust CLI options. | - | "-c 10 -r 10" |


### Standalone

Basic run, with folder (path in $MY_SCRIPTS) holding `locustfile.py`:
```
docker run --rm --name standalone --hostname standalone -e ATTACKED_HOST=http://standalone:8089 -p 8089:8089 -d -v $MY_SCRIPTS:/locust grubykarol/locust:0.8.1-py3.6
```
or, with additional runtime options:
```
docker run --rm --name standalone --hostname standalone -e ATTACKED_HOST=http://standalone:8089 -e "LOCUST_OPTS=--no-web" -p 8089:8089 -d -v $MY_SCRIPTS:/locust grubykarol/locust:0.8.1-py3.6
```

### Master-slave

Run master:
```
docker run --name master --hostname master \
 -p 8089:8089 -p 5557:5557 -p 5558:5558 \
 -v $MY_SCRIPTS:/locust \
 -e ATTACKED_HOST='http://master:8089' \
 -e LOCUST_MODE=master \
 --rm -d grubykarol/locust:0.8.1-py3.6
```

and some slaves:

```
docker run --name slave0 \
 --link master --env NO_PROXY=master \
 -v $MY_SCRIPTS:/locust \
 -e ATTACKED_HOST=http://master:8089 \
 -e LOCUST_MODE=slave \
 -e LOCUST_MASTER=master \
 --rm -d grubykarol/locust:0.8.1-py3.6

docker run --name slave1 \
 --link master --env NO_PROXY=master \
 -v $MY_SCRIPTS:/locust \
 -e ATTACKED_HOST=http://master:8089 \
 -e LOCUST_MODE=slave \
 -e LOCUST_MASTER=master \
 --rm -d grubykarol/locust:0.8.1-py3.6
```


For the real brave, Windows PowerShell version:

Basic run:
```
docker run --rm --name standalone `
 -e ATTACKED_HOST=http://localhost:8089 `
 -v c:\locust-scripts:/locust `
 -p 8089:8089 -d `
 grubykarol/locust:0.8.1-py3.6
```

Run master:
```
docker run --name master --hostname master `
 -p 8089:8089 -p 5557:5557 -p 5558:5558 `
 -v c:\locust-scripts:/locust `
 -e ATTACKED_HOST='http://master:8089' `
 -e LOCUST_MODE=master `
 --rm -d grubykarol/locust:0.8.1-py3.6
```

Run slave:
```
docker run --name slave0 `
 --link master --env NO_PROXY=master `
 -v c:\locust-scripts:/locust `
 -e ATTACKED_HOST=http://master:8089 `
 -e LOCUST_MODE=slave `
 -e LOCUST_MASTER=master `
 --rm -d grubykarol/locust:0.8.1-py3.6
```
