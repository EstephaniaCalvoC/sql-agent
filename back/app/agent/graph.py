from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver

from app.agent.states import OverallState, InputState, OutputState


def get_sql_agent_graph(nodes: dict, routers: dict):
    builder = StateGraph(OverallState, input=InputState, output=OutputState)
    builder.add_node(nodes["select_relevant_schemas"], "select_relevant_schemas")
    builder.add_node(nodes["generate_query"], "generate_query")
    builder.add_node(nodes["excute_query"], "excute_query")
    builder.add_node(nodes["gen_answer"], "gen_answer")

    builder.add_edge(START, "select_relevant_schemas")
    builder.add_conditional_edges("select_relevant_schemas", routers["check_question"])
    builder.add_edge("generate_query", "excute_query")
    builder.add_conditional_edges("excute_query", routers["router"])
    builder.add_edge("gen_answer", END)

    memory = MemorySaver()
    graph = builder.compile(checkpointer=memory)
    
    return graph
