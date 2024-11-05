"""Define a custom Reasoning and Action agent.

Works with a chat model with tool calling support.
"""

from datetime import datetime, timezone
from typing import Dict, List, Literal, cast

from langchain_core.messages import AIMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableConfig
from langgraph.graph import StateGraph
from langchain_ollama import ChatOllama


from react_agent.configuration import Configuration
from react_agent.state import InputState, State
# from react_agent.tools import TOOLS
# from react_agent.utils import load_chat_model


async def call_model2(
    state: State, config: RunnableConfig
) -> Dict[str, List[AIMessage]]:
    """Call ollama.

    Args:
        state (State): The current state of the conversation.
        config (RunnableConfig): Configuration for the model run.

    Returns:
        dict: A dictionary containing the model's response message.
    """

    configuration = Configuration.from_runnable_config(config)

    # Create a prompt template. Customize this to change the agent's behavior.
    prompt = ChatPromptTemplate.from_messages(
        [("system", configuration.system_prompt), ("placeholder", "{messages}")]
    )

    # Initialize the model with tool binding. Change the model or add more tools here.
    # model = load_chat_model(configuration.model).bind_tools(TOOLS)


    # Prepare the input for the model, including the current system time
    message_value = await prompt.ainvoke(
        {
            "messages": state.messages,
            "system_time": datetime.now(tz=timezone.utc).isoformat(),
        },
        config,
    )

    MODEL = "phi3:latest"
    model = ChatOllama(
        model=MODEL,
        base_url="http://host.docker.internal:11434",

        # keep_alive="-1"
        # NOTE: the above causes an error:
        # event: error
        # data: {"error":"ResponseError","message":"time: missing unit in duration \"-1\""}
    )

    # Get the model's response
    # response = cast(AIMessage, await model.ainvoke(message_value, config))
    # response = cast(AIMessage, await model.ainvoke(state.messages, base_url="http://host.docker.internal"))

    res = await model.ainvoke(state.messages)
    response = cast(AIMessage, res)

    return {"messages": [response]}


# Define a new graph
workflow = StateGraph(State, input=InputState, config_schema=Configuration)


workflow.add_node(call_model2)

workflow.add_edge("__start__", "call_model2")
workflow.add_edge("call_model2", "__end__")

# Compile the workflow into an executable graph
# You can customize this by adding interrupt points for state updates
graph = workflow.compile(
    interrupt_before=[],  # Add node names here to update state before they're called
    interrupt_after=[],  # Add node names here to update state after they're called
)
graph.name = "plebchat_test"
