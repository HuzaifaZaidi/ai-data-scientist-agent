from typing import TypedDict

from langgraph.graph import StateGraph, START, END


class AgentState(TypedDict):
    message: str


def first_node(state: AgentState):
    print("First node received:", state["message"])

    return {
        "message": state["message"] + " → First node completed"
    }


def second_node(state: AgentState):
    print("Second node received:", state["message"])

    return {
        "message": state["message"] + " → Second node completed"
    }


# Create the graph
builder = StateGraph(AgentState)

# Add nodes
builder.add_node("first", first_node)
builder.add_node("second", second_node)

# Connect nodes
builder.add_edge(START, "first")
builder.add_edge("first", "second")
builder.add_edge("second", END)

# Compile the graph
graph = builder.compile()