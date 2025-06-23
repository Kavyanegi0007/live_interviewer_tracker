from gaze_tracking import GazeTracking
from agent.state_schema import AgentState



class EyeTracker:
    def __init__(self):
        self.gaze = GazeTracking()

    def get_gaze_direction(self, frame):
        self.gaze.refresh(frame)

        if self.gaze.is_blinking():
            return "blink"
        elif self.gaze.is_right():
            return "right"
        elif self.gaze.is_left():
            return "left"
        elif self.gaze.is_center():
            return "center"
        else:
            return "unknown"
        

tracker = EyeTracker()
def eye_node(state: AgentState) -> AgentState:
    frame = state["frame"]
    direction = tracker.get_gaze_direction(frame)

    # Access eye_data
    eye_data = state["eye_data"]

    # 1. Append gaze direction
    eye_data["gaze_direction_log"].append(direction)

    # 2. Increment total samples
    eye_data["total_samples"] += 1

    # 3. If blink, increment blink count
    if direction == "blink":
        eye_data["blink_count"] += 1

    # Update back in state (optional, if needed)
    state["eye_data"] = eye_data

    return state
