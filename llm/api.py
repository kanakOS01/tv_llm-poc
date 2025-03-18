import os
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage, AIMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import START, MessagesState, StateGraph
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages

from typing import Sequence
from typing_extensions import Annotated, TypedDict

from config import settings


os.environ["OPENAI_API_KEY"] = settings.OPENAI_API_KEY


class State(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]


class LLM:
    def __init__(self):
        self.model = init_chat_model("gpt-4o-mini", model_provider="openai")
        self.workflow = StateGraph(state_schema=State)

        self.workflow.add_edge(START, "model")
        self.workflow.add_node("model", self.call_model)

        self.memory = MemorySaver()
        self.app = self.workflow.compile(checkpointer=self.memory)

        self.config = {"configurable": {"thread_id": "123"}}

        self.prompt_template = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """You are a helpful assistant with knowledge about Tolvera. Tölvera is a Python library designed for composing together and interacting with basal agencies, inspired by fields such as artificial life (ALife) and self-organising systems. It provides creative coding-style APIs that allow users to combine and compose various built-in behaviours, such as flocking, slime mold growth, and swarming, and also author their own.

                    Overview of Features : 
tv.v: a collection of "vera" (beings) including Move, Flock, Slime and Swarm, with more being continuously added. Vera can be combined and composed in various ways.
tv.p: extensible particle system. Particles are divided into multiple species, where each species has a unique relationship with every other species, including itself
tv.s: n-dimensional state structures that can be used by "vera", including built-in OSC and IML creation (see below).
tv.px: drawing library including various shapes and blend modes, styled similarly to p5.js etc.
tv.osc: Open Sound Control (OSC) via iipyper, including automated export of OSC schemas to JSON, XML, Pure Data (Pd), Max/MSP (SuperCollider TBC).
tv.iml: Interactive Machine Learning via anguilla.
tv.ti: Taichi-based simulation and rendering engine. Can be run "headless" (without graphics).
tv.cv: computer vision integration based on OpenCV and Mediapipe.

Your task is to generate tolvera code according to the user's query.""",
                ),
                MessagesPlaceholder(variable_name="messages"),
            ]
        )


    def call_model(self, state: State):
        prompt = self.prompt_template.invoke(state)
        response = self.model.invoke(prompt)
        return {"messages": [response]}
    

    def generate_response(self, query: str):
        input_messages = [HumanMessage(query)]
        output = self.app.invoke(
            {"messages": input_messages},
            self.config,
        )

        return output["messages"][-1]
    

if __name__ == "__main__":
    llm = LLM()
    query = "What is Tolvera?"
    response = llm.generate_response(query)
    print(response.content)