# python-llm-docker
encapsulate llm model in a REST API in a docker container

## Local Mac Run
```sh
mkdir cache
python3 -m venv env
source ./env/bin/activate
pip3 install -r requirments-local.txt

uvicorn app:app --reload
```


## Using DOcker
On mac using docker up the memory limit of your docker containers to 8 GB in the docker desktop preferences
Docker Run
```sh
mkdir cache
bash build.sh
bash runContainer.sh
```