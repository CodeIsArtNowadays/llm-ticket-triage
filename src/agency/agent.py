import asyncio
from typing import Annotated, TypedDict

from langchain_core.messages import SystemMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import BaseMessage, add_messages
from langgraph.prebuilt import ToolNode

from config import settings
from src.agency.tools import get_customer_by_username, get_transactions_by_customer_id
from src.agency.prompts import system_prompt


class AgentState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

tools = [
    get_customer_by_username,
    get_transactions_by_customer_id
]

llm = ChatOpenAI(
    base_url='https://api.deepseek.com',
    model='deepseek-flash',
    api_key=settings.AI_KEY
).bind_tools(tools)


async def ask_llm(state: AgentState):
    response = await llm.ainvoke([system_prompt] + state['messages'])
    return {'messages': [response]}

async def decider_node(state: AgentState):
    messages = state['messages']
    last_message = messages[-1]

    if not last_message.tool_calls:
        return 'end'
    return 'continue'

graph = StateGraph(AgentState)
tool_node = ToolNode(tools=tools)
graph.add_node('tools', action=tool_node)
graph.add_node('agent', action=ask_llm)

graph.add_edge(START, 'agent')
graph.add_conditional_edges(
    source='agent',
    path=decider_node,
    path_map={
        'continue': 'tools',
        'end': END
    }
)
graph.add_edge('tools', 'agent')        

app = graph.compile()

async def run_graph(user_data):
    init_message = f"USERNAME: {user_data['user']} \n QUESTION: {user_data['message']}"
    init_state = AgentState({'messages': init_message})
    res = await app.ainvoke(init_state)
    return res['messages'][-1].content

if __name__ == '__main__':
    john_duplicate_charge_request = {
        'user': 'John',
        'message': 'I see two charges of 1500 on October 28, 2026, around 10:00. Can you check whether these could be duplicate charges?'
    }
    res = asyncio.run(run_graph(john_duplicate_charge_request))
    print(res)