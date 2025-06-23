from typing import Literal
from collections import Counter
from agent.state_schema import AgentState

def action_node(state: AgentState) -> AgentState:
    print("\n===== Eye Movement Summary =====")
    eye_data = state["eye_data"]
    counts = Counter(eye_data["gaze_direction_log"])

    for label in ["left", "right", "center", "blink", "unknown"]:
        percent = (counts.get(label, 0) / max(eye_data["total_samples"], 1)) * 100
        print(f"{label.capitalize():<10}: {percent:.1f}%")

    print("\n===== Head Tilt Summary =====")
    head_data = state["head_data"]
    tilt_counts = head_data["tilt_counts"]
    total_head = max(head_data["total_samples"], 1)

    for direction in ["left", "right", "up", "down", "neutral"]:
        percent = (tilt_counts.get(direction, 0) / total_head) * 100
        print(f"{direction.capitalize():<10}: {percent:.1f}%")

    # Update last action timestamp
    state["last_action_timestamp"] = state["current_frame_timestamp"]

    # Optional: log action summary if needed
    state["action_log"].append("Summary generated at {:.1f}".format(state["current_frame_timestamp"]))

    

    return state
