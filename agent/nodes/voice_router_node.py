import numpy as np
import sounddevice as sd
import webrtcvad
from agent.state_schema import AgentState

vad = webrtcvad.Vad(2)  #

def voice_router_node(state: AgentState) -> str:
    """Acts as both a voice processor and router node."""
    audio_chunk = record_audio_chunk(duration=1.0)  # Capture 1 second
    is_voice = detect_voice(audio_chunk)            # webrtcvad wrapper

    # Update state
    state["audio_data"]["anomaly_detected"] = is_voice

    time.sleep(0.5)  # Wait before next round
    return "anomaly" if is_voice else "normal"
