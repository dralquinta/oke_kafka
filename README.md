# oke_kafka
The following is an example that uses Oracle Kubernetes Engine to process a kafka stream and then push the processing to another stream




- Config Map: 

kubectl create configmap app-settings --from-file=config.properties
kubectl get configmaps app-settings -o yaml > ../../kubernetes/configMap.yaml


- Docker image build: 
Flush images:

```shell
(venv) [opc@dalquintdevhubscl oke_kafka]$ docker system prune -a
WARNING! This will remove:
  - all stopped containers
  - all networks not used by at least one container
  - all images without at least one container associated to them
  - all build cache

Are you sure you want to continue? [y/N] y
Deleted Containers:
5791be8076e7e34cb16297594d369bc4d7a0625ff1177a4ef64daf98508d1e45
9e203595b66625e207be8ccd21efd185f835b5f1523338de455bd8c2bb7a07a9

Deleted Networks:
okekafka_default

Deleted Images:
deleted: sha256:fec344c5e110360b19cd993f0d003a68501b60a73d477cab7062b882c1bec9fd
deleted: sha256:cbacce507902048fb2222d448bfdd2820b07f4f8e6798d2323bc26703dadf482
deleted: sha256:74f1c7b6026a405a047dbfe522b76bec1ee7bdb5890c7e0b880f86f82e34eb86
deleted: sha256:c3663e60c0cd7990a8ed8b075f79632836b539bbabe91e699bbc51726336c672
deleted: sha256:501eca722f3b113c5a5a5ae442075eb133fbb4d0e03f4ae68593872dad360245
deleted: sha256:b8978f5e2019594f66ed5d36bb294317d7d52923ddab0507a69ca759f72860a0
deleted: sha256:fd9ba20bc2d8ae8238a8c3d7a27f44e1d8ec4480be6b2f887b047e471200a9a1
deleted: sha256:076bbc04d848f187502d0e0872ee148163dc343803f540e34315ee040cf354ac
untagged: python:3.9.7-slim
untagged: python@sha256:aef632387d994b410de020dfd08fb1d9b648fc8a5a44f332f7ee326c8e170dba
deleted: sha256:013406e15fb6dea65901d774caa29e5913512f2b31fc01332c63f4fecad1ca81
deleted: sha256:676903663a05c292588c21173c3e16dac15d474cfa38f7e3de53c5fb1dc6f620
...
...
...
deleted: sha256:ccd065bd50c50a46a4635ea0cb19f41cc1184c8a8d7fcfd7a6c653fd9ea00fea
deleted: sha256:53f782cf0ec703c9e1d2cf0b80770ea413ceb5291829eade145442883c1293aa
deleted: sha256:6d0ea9a3064149382faca8ee30244a658622c27a622beb17961f352ffa207876
deleted: sha256:406b405cf76370f20a3fd89d83ae7f19a5ceb17a30081f37c1d1aee04f90dff1
deleted: sha256:31e94ca6991c65358987a2bc276c62a1912bdd6dff0fcb12490b29376de9c66a
deleted: sha256:e8b689711f21f9301c40bf2131ce1a1905c3aa09def1de5ec43cf0adf652576e

Total reclaimed space: 3.532GB
```


Building: 

```shell
(venv) [opc@dalquintdevhubscl oke_kafka]$ docker-compose up --build
Creating network "okekafka_default" with the default driver
Building consumer
Step 1/7 : FROM --platform=linux/amd64 python:3.9.7-slim
Trying to pull repository docker.io/library/python ... 
3.9.7-slim: Pulling from docker.io/library/python
7d63c13d9b9b: Pull complete
6ad2a11ca37b: Pull complete
e9edbe81a001: Extracting [>                                                  ]  131.1kB/11.02MB
36629b83aba2: Download complete
3baebd9b1d65: Download complete
...
...
...


```

- Create OCIR Repo (in this case okestreams)

- Generate OCIR Secret

`kubectl create secret docker-registry ocirsecret --docker-server=sa-santiago-1.ocir.io --docker-username='idhkis4m3p5e/oracleidentitycloudservice/denny.alquinta@oracle.com' --docker-password='YOUR_AUTH_TOKEN' --docker-email='denny.alquinta@oracle.com'`
- Login into OCIR: 

```shell
(venv) opc@dalquintdevhubscl oke_kafka]$ docker login sa-santiago-1.ocir.io
Username: idhkis4m3p5e/oracleidentitycloudservice/denny.alquinta@oracle.com
Password: 
WARNING! Your password will be stored unencrypted in /home/ubuntu/.docker/config.json.
Configure a credential helper to remove this warning. See
https://docs.docker.com/engine/reference/commandline/login/#credentials-store

Login Succeeded

```

- Get the built image tag: 

```shell
(venv) [opc@dalquintdevhubscl oke_kafka]$ docker image ls
REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
consumer            latest              d86c8873cf68        5 minutes ago       600MB
python              3.9.7-slim          ccd065bd50c5        5 months ago        122MB
```

- Retag the image: 

`docker tag consumer:latest sa-santiago-1.ocir.io/idhkis4m3p5e/okestreams:latest`

It'll look like this: 

```shell
(venv) [opc@dalquintdevhubscl oke_kafka]$ docker image ls
REPOSITORY                                               TAG                 IMAGE ID            CREATED             SIZE
consumer                                                 latest              d86c8873cf68        8 minutes ago       600MB
sa-santiago-1.ocir.io/idhkis4m3p5e/okestreams            latest              d86c8873cf68        8 minutes ago       600MB
python                                                   3.9.7-slim          ccd065bd50c5        5 months ago        122MB
```

- Push the image: 

`docker push sa-santiago-1.ocir.io/idhkis4m3p5e/okestreams:latest`

```shell
(venv) [opc@dalquintdevhubscl oke_kafka]$ docker push sa-santiago-1.ocir.io/idhkis4m3p5e/okestreams:latest
The push refers to repository [sa-santiago-1.ocir.io/idhkis4m3p5e/okestreams]
804a47a9fd07: Pushed 
6a4aee43f09d: Pushed 
3de586dc45fa: Pushed 
88e936553a21: Pushed 
b52b205045a6: Pushed 
284a6c64b82c: Pushed 
388eedeb736e: Pushed 
2feece0964b8: Pushed 
e8b689711f21: Pushed 
latest: digest: sha256:9acf796ca6bb362b58657a650de12a95b5e5521e5a844e8904a8d2d937e9c842 size: 2209
```

