from agent.state_schema import AgentState


def check_time_router_function(state: AgentState) -> str:
    """
    Decide whether enough time (>= 7 minutes) has passed since the last action.
    If yes, return 'action_node'. Else, return 'eye_node' to continue monitoring.
    """
    current_time = state["current_frame_timestamp"]
    last_action_time = state.get("last_action_timestamp", 0)
    
    time_elapsed = current_time - last_action_time
    
    # Add debugging output
    print(f"⏱️  ROUTER CHECK: Current={current_time:.1f}, Last={last_action_time:.1f}, Elapsed={time_elapsed:.1f}s")
    
    if time_elapsed >= 420:  # 7 minutes = 420 seconds
        print(f"✅ 7+ minutes elapsed, routing to ACTION")
        return "action_node"
    else:
        remaining = 420 - time_elapsed
        print(f"⏳ Continuing monitoring, {remaining:.1f}s remaining")
        return "eye_node"
