from langgraph.graph import StateGraph, START, END, MessagesState
from langgraph.prebuilt import ToolNode

from app.llm import llm
from app.analytics_tools import (
    run_sql_query,
    analyze_dataframe,
    create_chart
)

tools = [
    run_sql_query,
    analyze_dataframe,
    create_chart
]

llm_with_tools = llm.bind_tools(tools)


class AgentState(MessagesState):
    pass


def agent_node(state: AgentState):
    response = llm_with_tools.invoke(state["messages"])

    return {
        "messages": [response]
    }


def should_continue(state: AgentState):
    last_message = state["messages"][-1]

    if last_message.tool_calls:
        return "tools"

    return "end"


tool_node = ToolNode(tools)


builder = StateGraph(AgentState)

builder.add_node("agent", agent_node)
builder.add_node("tools", tool_node)

builder.add_edge(START, "agent")

builder.add_conditional_edges(
    "agent",
    should_continue,
    {
        "tools": "tools",
        "end": END
    }
)

builder.add_edge("tools", "agent")

graph = builder.compile()