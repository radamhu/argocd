# Visualize infrastructure architect 

Diagrams lets you draw the cloud system architecture in Python code.

```
$ pip install diagrams or you can use requirements.txt
```

# Python Docker App deployed by Azure Devops pipeline to EDC development instance

## Initiate a docker based python APP development environment

```
clone repository && cd into it
create .gitignore
create .dockerignore
python -m venv .venv
.\.venv\Scripts\activate
# pip install . 
# pip install pandas 
# pip install argparse
# pip install fuzzywuzzy
# pip install python-dotenv 
pip install -r requirements.txt 
# pip freeze -l > requirements.txt 
.env
    encodeUser.py Administrator user
    for Powershell:
        $env:INFA_EDC_AUTH="Basic QWRtaW5pc3RyYXRvcjpBZG1pbmlzdHJhdG9y"

    for windows cmd:
        set INFA_EDC_AUTH=Basic QWRtaW5pc3RyYXRvcjpBZG1pbmlzdHJhdG9y

    or add to launch.json for vsvode debugging - in the configurations section
        "envFile": "${workspaceFolder}/.env",
        and add
        INFA_EDC_AUTH="Basic QWRtaW5pc3RyYXRvcjpBZG1pbmlzdHJhdG9y",
        to .env in the root folder of your project

    or add to launch.json for vscode debugging - in the configurations section
        "env" : {"INFA_EDC_AUTH" : "Basic QWRtaW5pc3RyYXRvcjpBZG1pbmlzdHJhdG9y"},

python .\edc_lineage\lineage_mapping__evaweprddls_ingress_all__synapse_evaprdsynspallservice.py -sn SHEET1 -o .\temp -u Native\Administrator -c https://edc-dev.zeiss.org:9086

python ./edc_lineage/lineage_mapping__evaweprddls_ingress_all__synapse_evaprdsynspallservice.py -sn Sheet1 -o .\temp -c https://edc-dev.zeiss.org:9086
# python change_me.py --debug run

```

## Setup Python project using Docker

- Basic project setup to use in our Docker container (app folder)
- Dockerfile

## Build our Docker Container and Run

```
sudo docker build --no-cache -t devops_lineage:v1.0 .
docker run --name devops_lineage -it -d devops_lineage:v1.0
docker exec -it devops_lineage /bin/bash
docker container inspect devops_lineage
tail -f cron_log.log
```

## Publishing the Docker image

## Bonus — Makefile

Let’s create a simple Makefile that allows us to build, run, and kill our image/container:

```
app_name = gunicorn_flask
build:
    @docker build -t $(app_name) .
run:
    docker run -d -p 8000:8000 $(app_name)
kill:
    @echo 'Killing container...'
    @docker ps | grep $(app_name) | awk '{print $1}' | xargs docker stop
```

Now we should be able to run:

```
# build Docker image
make build
# run the container
make run
# destroy it
make kill
```

## Create a python test environment from scratch

do the above steps to create a virtual environment:

```
mkdir test
```

test_hello.py

```
def test_failing():
    assert True == True
```

pytest

## Access Flask app at https://edc.zeiss.org:8000
