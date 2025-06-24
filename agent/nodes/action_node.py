from typing import Literal
from collections import Counter
from agent.state_schema import AgentState

def action_node(state: AgentState) -> AgentState:
    print("\n================== ACTION SUMMARY ==================")

    # EYE MOVEMENT SUMMARY
    print("\n Eye Movement Summary")
    eye_data = state["eye_data"]
    eye_counts = Counter(eye_data["gaze_direction_log"])
    total_eye = max(eye_data["total_samples"], 1)

    for label in ["left", "right", "center", "blink", "unknown"]:
        percent = (eye_counts.get(label, 0) / total_eye) * 100
        print(f"{label.capitalize():<10}: {percent:.1f}%")

    # HEAD MOVEMENT SUMMARY
    print("\n Head Tilt Summary")
    head_data = state["head_data"]
    head_counts = head_data["tilt_counts"]
    total_head = max(head_data["total_samples"], 1)

    for direction in ["left", "right", "up", "down", "neutral"]:
        percent = (head_counts.get(direction, 0) / total_head) * 100
        print(f"{direction.capitalize():<10}: {percent:.1f}%")

    # AUDIO ANOMALY INFO
    print("\n Audio Anomaly Check")
    if state["audio_data"]["anomaly_detected"]:
        print("⚠️  Voice anomaly detected during silent period.")
        state["action_log"].append("Voice anomaly detected at {:.1f}".format(state["current_frame_timestamp"]))
    else:
        print(" No audio anomaly detected.")

    # TIMESTAMP + LOGGING
    state["last_action_timestamp"] = state["current_frame_timestamp"]
    state["action_log"].append("Summary generated at {:.1f}".format(state["current_frame_timestamp"]))

    print("\n====================================================\n")

    return state
