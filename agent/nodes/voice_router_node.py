import numpy as np
import sounddevice as sd
import webrtcvad
from agent.state_schema import AgentState
import time

vad = webrtcvad.Vad(2)  #

def detect_voice(audio_bytes, sample_rate=16000, frame_duration_ms=30):
    """
    Splits audio into small frames and checks if voice is detected.
    """
    num_bytes = int(sample_rate * frame_duration_ms / 1000 * 2)  # 2 bytes per sample
    for i in range(0, len(audio_bytes), num_bytes):
        frame = audio_bytes[i:i + num_bytes]
        if len(frame) == num_bytes and vad.is_speech(frame, sample_rate):
            return True
    return False


def record_audio_chunk(duration=1.0, sample_rate=16000):
    """
    Records a short audio chunk and returns it as 16-bit mono PCM bytes.
    """
    audio = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype='int16')
    sd.wait()
    return audio.tobytes()
def voice_router_node(state: AgentState) -> str:
    """Acts as both a voice processor and router node."""
    audio_chunk = record_audio_chunk(duration=1.0)  # Capture 1 second
    is_voice = detect_voice(audio_chunk)            # webrtcvad wrapper

    # Update state
    state["audio_data"]["anomaly_detected"] = is_voice

    time.sleep(0.5)  # Wait before next round
    return "anomaly" if is_voice else "normal"
