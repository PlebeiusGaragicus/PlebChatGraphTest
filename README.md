reference: https://langchain-ai.github.io/langgraph/how-tos/deploy-self-hosted/



```sh
# download the repo
git clone ...
cd ...


# setup the python environment
python3.10 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -U langgraph-cli


# build the docker image
langgraph build -t <name-your-graph-here>

# RUN!
# TODO: do we need -d?
docker compose -f plebgraph_compose.yml --env-file .env up -d

# test
curl --request GET --url 0.0.0.0:8123/ok

# refer to docs at 0.0.0.0:8123/docs

```
