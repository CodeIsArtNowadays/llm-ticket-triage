from typing import Annotated, TypedDict, Literal

from pydantic import BaseModel
from langchain_core.messages import SystemMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import BaseMessage, add_messages

from config import settings
from src.agency.tools import get_customer_by_username, get_transactions_by_customer_id


class AgentState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]
    next_node: str

tools = [
    get_customer_by_username,
    get_transactions_by_customer_id
]

llm = ChatOpenAI(
    base_url='https://api.deepseek.com',
    model='deepseek-flash',
    api_key=settings.AI_KEY
).bind_tools(tools)


def ask_llm(state: AgentState):
    system_prompt = SystemMessage(content='asdasd')
    response = llm.invoke([system_prompt] + state['messages'])
    return {'messages': [response]}

def tool_node(state: AgentState):
    messages = state['messages']
    last_message = messages[-1]

    tool_result = []
    for tool_call in last_message.tool_calls:
        tool = next(t for t in tool_call if t.name == tool_call['name'])
        res = tool.run(tool_call['args'])
        tool_result.append(res)

    return {'messages': [tool_result]}
        
    
        