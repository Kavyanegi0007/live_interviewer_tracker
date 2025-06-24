from agent.state_schema import AgentState

def check_time_node(state: AgentState) -> str: #we are returning a str not state (Router Node)
    """
    Decide whether enough time (>= 7 minutes) has passed since the last action.
    If yes, return 'action_node'. Else, return 'eye_node' to continue monitoring.
    """
    current_time = state["current_frame_timestamp"]
    last_action_time = state.get("last_action_timestamp", 0)

    time_elapsed = current_time - last_action_time

    if time_elapsed >= 420:  # 7 minutes = 420 seconds
        return "action_node"
    else:
        return "eye_node"
