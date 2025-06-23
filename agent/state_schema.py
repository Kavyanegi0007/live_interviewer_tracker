from typing import TypedDict, List,  Dict, Literal,  Any

class EyeData(TypedDict):
    
    gaze_direction_log: List[str]
    blink_count: int
    total_samples: int


TiltDirection = Literal["left", "right", "up", "down", "neutral"]

class HeadData(TypedDict):
    tilt_counts: Dict[TiltDirection, int]
    total_samples: int

class AgentState(TypedDict):
    eye_data: EyeData
    head_data: HeadData
    current_frame_timestamp: float
    last_action_timestamp: float
    action_log: List[str]
    frame: Any            