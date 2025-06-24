import sounddevice as sd
import numpy as np

def get_audio_sample(duration_ms=1000, sample_rate=16000):
    """
    Records a short audio clip from the microphone.

    Args:
        duration_ms (int): Duration in milliseconds
        sample_rate (int): Sampling rate in Hz

    Returns:
        np.ndarray: Flattened int16 audio sample
    """
    duration = duration_ms / 1000.0  # Convert ms to seconds
    audio = sd.rec(int(sample_rate * duration), samplerate=sample_rate, channels=1, dtype='int16')
    sd.wait()  # Wait until recording is done
    return audio.flatten()