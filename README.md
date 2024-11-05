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

# ENTER ENVIRONMENT VARIABLES
cp .env.example .env
nano .env

# build the docker image
langgraph build -t <name-your-graph-here>

# RUN!
# TODO: do we need -d?
docker compose -f plebchat-compose.yml --env-file .env up -d

# test
curl --request GET --url 0.0.0.0:8123/ok

# refer to docs at 0.0.0.0:8123/docs

```


---



```sh

curl --request POST \
 --url http://0.0.0.0:8123/threads/20573722-e04f-4243-9a8c-0b87f9cac937/runs/stream \
 --header 'Content-Type: application/json' \
 --data "{
   \"assistant_id\": \"agent\",
   \"input\": {\"messages\": [{\"role\": \"human\", \"content\": \"what's the weather in sf\"}]},
   \"stream_mode\": [
     \"events\"
   ]
 }"

curl --request POST \
  --url http://0.0.0.0:8123/assistants/search \
  --header 'Content-Type: application/json' \
  --data '{
  "metadata": {},
  "limit": 10,
  "offset": 0
}'


# THIS WORKS!!!

curl --request POST \
  --url http://0.0.0.0:8123/runs/stream \
  --header 'Content-Type: application/json' \
  --data '{
  "assistant_id": "plebchat_agent",
  "input": {"messages": [{"role": "user", "content": "what rhymes with orange?"}]},
  "metadata": {},
  "config": {
    "configurable": {}
  },
  "stream_mode": [
    "messages"
  ]
}'


# TRY THIS FOR LANGGRAPH STUDIO
curl --request POST \
  --url http://localhost:50974/runs/stream \
  --header 'Content-Type: application/json' \
  --data '{
  "assistant_id": "plebchat_agent",
  "input": {"messages": [{"role": "user", "content": "what rhymes with orange?"}]},
  "metadata": {},
  "config": {
    "configurable": {}
  },
  "stream_mode": [
    "messages"
  ]
}'

```