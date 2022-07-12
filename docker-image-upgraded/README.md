
## Upgrade to the latest locust with python 3.9

# Run a stand alone against a client side that runs in localhost:3000
1. cd to docker-image-upgraded dir
2. build the docker image. run `docker build -t gaiashkenazy/locust:latest .`
3. edit the locustfile.py in the locust directory to match the load testing that you need
4. run the docker container. run 
`docker run --name standalone --hostname standalone -e ATTACKED_HOST=http://host.docker.internal:3000 -v /Users/gai.ashkenazy/workspace/locust-sandbox/locust-experiments-gai-ashkenazy/docker-image-upgraded/locust:/locust -p 8089:8089 --add-host=host.docker.internal:host-gateway --rm -d gaiashkenazy/locust`
5. open the locust ui in this url: `http://127.0.0.1:8089/` and see the stats

# Run master with 2 slave against a client side that runs in localhost:3000
1. use the same docker image as above
2. cd to docker-image dir
3. build the docker image. run `docker build -t gaiashkenazy/locust:latest .`
4. edit the locustfile.py in the locust directory to match the load testing that you need
5. run the master docker container. run 
`docker run --name master --hostname master -p 8089:8089 -p 5557-5577:5557-5577 -v /Users/gai.ashkenazy/workspace/locust-sandbox/locust-experiments-gai-ashkenazy/docker-image-upgraded/locust:/locust -e ATTACKED_HOST=http://host.docker.internal:3000 -e LOCUST_MODE=master -e LOCUST_OPTS="--expect-workers=2" --add-host=host.docker.internal:host-gateway --rm -d gaiashkenazy/locust`
6. run the slave 1 docker container. run
`docker run --name slave0 --link master --env NO_PROXY=master -v /Users/gai.ashkenazy/workspace/locust-sandbox/locust-experiments-gai-ashkenazy/docker-image-upgraded/locust:/locust -e ATTACKED_HOST=http://host.docker.internal:3000 -e LOCUST_MODE=slave -e LOCUST_MASTER=master -e LOCUST_OPTS="" -d gaiashkenazy/locust`
7. run the slave 2 docker container. run
`docker run --name slave1 --link master --env NO_PROXY=master -v /Users/gai.ashkenazy/workspace/locust-sandbox/locust-experiments-gai-ashkenazy/docker-image-upgraded/locust:/locust -e ATTACKED_HOST=http://host.docker.internal:3000 -e LOCUST_MODE=slave -e LOCUST_MASTER=master -e LOCUST_OPTS="" --rm -d gaiashkenazy/locust`
8. And so on for more slaves (be sure to export more ports - this will require to build the docker image again)
`docker run --name slave2 --link master --env NO_PROXY=master -v /Users/gai.ashkenazy/workspace/locust-sandbox/locust-experiments-gai-ashkenazy/docker-image-upgraded/locust:/locust -e ATTACKED_HOST=http://host.docker.internal:3000 -e LOCUST_MODE=slave -e LOCUST_MASTER=master -e LOCUST_OPTS="" --rm -d gaiashkenazy/locust`
`docker run --name slave3 --link master --env NO_PROXY=master -v /Users/gai.ashkenazy/workspace/locust-sandbox/locust-experiments-gai-ashkenazy/docker-image-upgraded/locust:/locust -e ATTACKED_HOST=http://host.docker.internal:3000 -e LOCUST_MODE=slave -e LOCUST_MASTER=master -e LOCUST_OPTS="" --rm -d gaiashkenazy/locust`
`docker run --name slave4 --link master --env NO_PROXY=master -v /Users/gai.ashkenazy/workspace/locust-sandbox/locust-experiments-gai-ashkenazy/docker-image-upgraded/locust:/locust -e ATTACKED_HOST=http://host.docker.internal:3000 -e LOCUST_MODE=slave -e LOCUST_MASTER=master -e LOCUST_OPTS="" --rm -d gaiashkenazy/locust`
11. open the locust ui in this url: `http://127.0.0.1:8089/` and see the stats
