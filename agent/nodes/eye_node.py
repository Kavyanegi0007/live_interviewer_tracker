import cv2
from agent.state_schema import AgentState

# Load pre-trained OpenCV eye detector
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_eye.xml")

def estimate_gaze_direction(eye_roi):
    # Divide eye ROI into left and right halves
    h, w = eye_roi.shape
    left_side = eye_roi[:, :w//2]
    right_side = eye_roi[:, w//2:]

    # Count dark pixels (the pupil is dark)
    left_dark = cv2.countNonZero(cv2.threshold(left_side, 50, 255, cv2.THRESH_BINARY_INV)[1])
    right_dark = cv2.countNonZero(cv2.threshold(right_side, 50, 255, cv2.THRESH_BINARY_INV)[1])

    if abs(left_dark - right_dark) < 100:
        return "center"
    elif left_dark > right_dark:
        return "right"
    else:
        return "left"

def eye_node(state: AgentState) -> AgentState:
    frame = state["frame"]
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    direction = "unknown"
    for (x, y, w, h) in faces:
        roi_gray = gray[y:y+h, x:x+w]
        eyes = eye_cascade.detectMultiScale(roi_gray)
        if len(eyes) == 0:
            direction = "unknown"
            break

        # Use only first detected eye
        (ex, ey, ew, eh) = eyes[0]
        eye_roi = roi_gray[ey:ey+eh, ex:ex+ew]
        direction = estimate_gaze_direction(eye_roi)
        break  # one face, one eye

    # Update state
    state["eye_data"]["gaze_direction_log"].append(direction)
    state["eye_data"]["total_samples"] += 1

    if direction == "blink":
        state["eye_data"]["blink_count"] += 1

    return state
