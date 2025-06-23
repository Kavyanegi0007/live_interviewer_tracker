from agent.agent_graph import agent_graph
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
    "current_frame_timestamp": time.time(),
    "last_action_timestamp": 0.0,
    "action_log": []
}
cap = cv2.VideoCapture(0)
while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame")
        break

    state["frame"] = frame
    state["current_frame_timestamp"] = time.time()
    state = agent_graph.invoke(state)

    # Optional: display live frame
    cv2.imshow("Live Feed", frame)

    # Press q to exit
    if cv2.waitKey(1) & 0xFF == ord("q"):
        print("Exiting loop...")
        break

    time.sleep(0.5)

cap.release()
cv2.destroyAllWindows()
