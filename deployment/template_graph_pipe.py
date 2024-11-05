"""
title: PlebChat Pipeline
author: Who, me? I'm PlebbyG!
date: 2024-11-04
version: 1.0
license: MIT
description: PlebChat gets its own graph!
requirements: langgraph_sdk
"""

# example from: https://github.com/open-webui/pipelines/blob/main/examples/pipelines/providers/aws_bedrock_claude_pipeline.py

import json
import requests
from typing_extensions import TypedDict

from typing import List, Union, Generator, Iterator, Optional
from langgraph_sdk import get_client
import asyncio

try:
    from pydantic.v1 import BaseModel
except Exception:
    from pydantic import BaseModel


########################################################################
# This is shown in the UI to the user
AGENT_NAME = "PlebChat"

# This is used to identify the approprate graph in the Langserver
# NOTE: This must match exactly with the graph_name variable in your inherited BotCommandHandler class!
GRAPH_NAME = "plebchat"

# Settings for this pipeline
HARD_DISABLE_TITLE_GENERATION = False

# Langserver endpoint
# curl --request GET --url 0.0.0.0:8123/ok
# LANGSERVE_ENDPOINT = f"http://0.0.0.0"
# LANGSERVE_ENDPOINT = f"http://localhost"
LANGSERVE_ENDPOINT = f"http://host.docker.internal"
PORT = 8123
# PORT = 8000
# PORT = 8513

#TODO - pull from the env??
PIPELINE_ENDPOINT = "/plebchattestgraph"

########################################################################


class PostRequest(TypedDict):
    user_message: str
    messages: List[dict]
    body: dict


class Pipeline:
    class Valves(BaseModel):
        pass

    def __init__(self):
        self.name = AGENT_NAME
        self.graph_name = GRAPH_NAME
        self.chat_id = None


    async def inlet(self, body: dict, user: Optional[dict] = None) -> dict:
        print(f"inlet:{__name__}")
        print(f"user: {user}")
        print(f"body: {body}")

        if body.get("task") == "title_generation":
            print("################# Title Generation #################")
            body['ignore'] = True

        # Store the chat_id from body
        self.chat_id = body.get("chat_id")
        print(f"Stored chat_id: {self.chat_id}")

        return body


    # async def on_startup(self):
    #     print(f">>> PIPELINE {self.name.upper()} IS STARTING!!! <<<")

    # async def on_shutdown(self):
    #     print(f">>> PIPELINE {self.name.upper()} IS SHUTTING DOWN!!! <<<")


    def pipe(self, user_message: str, model_id: str, messages: List[dict], body: dict
             ) -> Union[str, Generator, Iterator]:

        if body.get("task") == "title_generation" and not HARD_DISABLE_TITLE_GENERATION:
            print("################# Title Generation #################")
            yield f"Pipeline {self.name}"

        else:

            print(f">>> PIPELINE '{self.name.upper()}' RUNNING <<<")
            print("######################################")
            print("user_message: str")
            print(f"{user_message}")
            print("model_id: str")
            print(f"{model_id}")
            # print("messages: List[dict]")
            # print(f"{messages}")
            print("body: dict")
            print(f"{json.dumps(body, indent=4)}")
            print("######################################")


            url = f"{LANGSERVE_ENDPOINT}:{PORT}{PIPELINE_ENDPOINT}"
            client = get_client(url=url)


            async def new_assistants_api():
                # thread = await client.threads.create()

                # input = {
                #     "text": user_message
                # }

                async for chunk in client.runs.stream(
                    self.chat_id,
                    "plebchat_agent",
                    # messages,
                    user_message,
                    stream_mode="updates"
                ):
                    yield chunk.data
                    # yield "chunk me harder, daddy!\n"

            # yield asyncio.run(new_assistants_api)

            # return new_assistants_api()
            # return asyncio.run(new_assistants_api())
            # result = await asyncio.run(self.run_pipeline(...))


            yield asyncio.run(new_assistants_api)




            # async def get_assistants():
                # assistants = await client.assistants.search()

                # for assistant in assistants:
                #     print(assistant['assistant_id'], assistant['name'], assistant['config'], assistant['version'])

                # assistant = [assistant for assistant in assistants if assistant ['name'] == 'openai_assistant'] [0]



            # url = f"{LANGSERVE_ENDPOINT}:{PORT}{PIPELINE_ENDPOINT}"
            # url = f"{LANGSERVE_ENDPOINT}:{PORT}"
            # headers = {
                # 'accept': 'application/json',
                # 'Content-Type': 'application/json'
            # }
            # body['chat_id'] = self.chat_id
            # body['graph_name'] = self.graph_name
            # req = PostRequest(user_message=user_message, messages=messages, body=body)

            # try:
            #     response = requests.post(url, json=req, headers=headers, stream=True)
            #     response.raise_for_status()

            #     for line in response.iter_lines():
            #         if line:
            #             yield line.decode() + '\n'

            # except Exception as e:
            # # except requests.exceptions.RequestException as e:
            #     # TODO: give an ALERT to the system admin!
            #     yield f"""⛓️‍💥 uh oh!\nSomething broke.\nThe server may be down.\n{e}"""
