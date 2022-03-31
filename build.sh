#!/bin/sh

docker system prune -a
docker-compose up --build 


docker tag consumer:latest sa-santiago-1.ocir.io/idhkis4m3p5e/okestreams:latest
docker push sa-santiago-1.ocir.io/idhkis4m3p5e/okestreams:latest