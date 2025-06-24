from agent.agent_graph import agent_graph

from agent.agent_graph_audio import agent_graph_audio
import time
import cv2

state = {
    "eye_data": {
        "eye_contact_log": [], # List[bool]
        "gaze_direction_log": [],  # List[str] like ["left", "neutral", "right"]
        "blink_count": 0,
        "total_samples": 0
    },
    "head_data": {
        "tilt_counts": {
            "left": 0,
            "right": 0,
            "up": 0,
            "down": 0,
            "neutral": 0
        },
        "total_samples": 0
    },

        "audio_data": {
        "anomaly_detected": False,
        "noise_levels": [],
        "total_samples": 0
    },
    "current_frame_timestamp": time.time(),
    "last_action_timestamp": 0.0,
    "action_log": []
}
import threading
#run this seperately 
def run_vision_graph():
    cap = cv2.VideoCapture(0)
    last_graph_run = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            continue
        state["frame"] = frame
        state["current_frame_timestamp"] = time.time()
        if state["current_frame_timestamp"] - last_graph_run >= 60:
            print(f"🔍 Running analysis... {time.strftime('%H:%M:%S')}")
            agent_graph.invoke(state)
            last_graph_run = state["current_frame_timestamp"]
        
        cv2.imshow("Live Feed", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
        time.sleep(0.5)
    cap.release()
    cv2.destroyAllWindows()

def run_audio_graph():
    while True:
        agent_graph_audio.invoke(state)
        time.sleep(0.5)
vision_thread = threading.Thread(target=run_vision_graph)
audio_thread = threading.Thread(target=run_audio_graph)

vision_thread.start()
audio_thread.start()

vision_thread.join()
audio_thread.join()
