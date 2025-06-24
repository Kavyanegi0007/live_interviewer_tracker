from langgraph.graph import StateGraph
from agent.state_schema import AgentState
from agent.nodes.voice_router_node import voice_router_node
from agent.nodes.action_node import action_node

graph = StateGraph(AgentState)

graph.add_node("voice_router_node", voice_router_node)
graph.add_node("action_node", action_node)

graph.set_entry_point("voice_router_node")

graph.add_conditional_edges(
    "voice_router_node",
    lambda state: "anomaly" if state["audio_data"]["anomaly_detected"] else "normal",
    {
        "anomaly": "action_node",
        "normal": "voice_router_node"
    }
)

agent_graph_audio = graph.compile()
