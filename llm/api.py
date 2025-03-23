import os
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage, AIMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import START, MessagesState, StateGraph
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import BaseMessage, SystemMessage, trim_messages
from langgraph.graph.message import add_messages
import streamlit as st

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

Your task is to generate tolvera code according to the user's query.

Example Tolvera code - 
import taichi as ti
from tolvera import Tolvera, run

def main(**kwargs):
    tv = Tolvera(**kwargs)

    @ti.kernel
    def draw():
        w = 100
        tv.px.rect(tv.x/2-w/2, tv.y/2-w/2, w, w, ti.Vector([1., 0., 0., 1.]))

    @tv.render
    def _():
        tv.p()
        draw()
        return tv.px

if __name__ == '__main__':
    run(main)""",
                ),
                MessagesPlaceholder(variable_name="messages"),
            ]
        )

        self.trimmer = trim_messages(
            max_tokens=10000,
            strategy="last",
            token_counter=self.model,
            include_system=True,
            allow_partial=False,
            start_on="human",
        )


    def call_model(self, state: State):
        trimmed_messages = self.trimmer.invoke(state["messages"])
        # trimmed_messages = state["messages"]
        prompt = self.prompt_template.invoke(
            {"messages": trimmed_messages}
        )
        response = self.model.invoke(prompt)
        return {"messages": [response]}
    

    def generate_response(self, query: str):
        input_messages = [HumanMessage(query)]

        for chunk, metadata in self.app.stream(
            {"messages": input_messages},
            self.config,
            stream_mode="messages",
        ):
            if isinstance(chunk, AIMessage):
                yield chunk.content
    

# example usage testing
if __name__ == "__main__":
    llm = LLM()
    query = "What is Tolvera?"
    response = "".join(llm.generate_response(query))
    print(response)