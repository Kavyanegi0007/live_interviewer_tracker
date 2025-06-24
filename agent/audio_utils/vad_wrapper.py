import webrtcvad

class VADDetector:
    def __init__(self, aggressiveness: int = 2):
        """
        aggressiveness: 0 (least aggressive) to 3 (most aggressive)
        Higher means fewer false positives (only louder, clearer speech passes).
        """
        self.vad = webrtcvad.Vad(aggressiveness)

    def is_speech(self, audio_bytes: bytes, sample_rate: int = 16000) -> bool:
        """
        audio_bytes must be 16-bit PCM mono audio.
        It should be at least 10ms and at most 30ms long.
        """
        return self.vad.is_speech(audio_bytes, sample_rate)
