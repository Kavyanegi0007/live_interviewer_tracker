from langgraph.graph import StateGraph, END , START
from agent.state_schema import AgentState
from agent.nodes.eye_node import eye_node
from agent.nodes.head_pose_node import head_pose_node
from agent.nodes.action_node import action_node
from agent.nodes.check_time_node import check_time_node  # you'll create this file soon
from agent.nodes.check_time_node import check_time_router_function

graph = StateGraph(AgentState)
graph.add_node("eye_node", eye_node)
graph.add_node("head_pose_node", head_pose_node)
graph.add_node("check_time_node", check_time_node)
graph.add_node("action_node", action_node)


graph.set_entry_point("eye_node")

graph.add_edge("eye_node", "head_pose_node")
graph.add_edge("head_pose_node", "check_time_node")

graph.add_conditional_edges(
    "check_time_node",
    check_time_router_function,
    {
        "action_node": "action_node",
        "eye_node": "eye_node"
    }
)

graph.add_edge("action_node", "eye_node")

agent_graph = graph.compile()

__all__ = ["agent_graph"]