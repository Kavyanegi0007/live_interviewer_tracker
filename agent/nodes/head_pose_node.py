import cv2
import numpy as np
from agent.state_schema import AgentState
model_path = "data/lbfmodel.yaml"



# 3D model points of facial features (nose, eyes, etc.)
MODEL_POINTS = np.array([
    (0.0, 0.0, 0.0),             # Nose tip
    (0.0, -330.0, -65.0),        # Chin
    (-225.0, 170.0, -135.0),     # Left eye left corner
    (225.0, 170.0, -135.0),      # Right eye right corner
    (-150.0, -150.0, -125.0),    # Left mouth corner
    (150.0, -150.0, -125.0)      # Right mouth corner
], dtype=np.float64)

class HeadPoseEstimator:
    def __init__(self):
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
        self.landmark_detector = cv2.face.createFacemarkLBF()
        self.landmark_detector.loadModel(model_path)  # You need this model

    def get_head_direction(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)

        if len(faces) == 0:
            return "neutral"

        ok, landmarks = self.landmark_detector.fit(gray, faces)
        if not ok:
            return "neutral"

        image_points = np.array([
            landmarks[0][0][30],     # Nose tip
            landmarks[0][0][8],      # Chin
            landmarks[0][0][36],     # Left eye left corner
            landmarks[0][0][45],     # Right eye right corner
            landmarks[0][0][48],     # Left mouth corner
            landmarks[0][0][54]      # Right mouth corner
        ], dtype="double")

        height, width = frame.shape[:2]
        focal_length = width
        center = (width // 2, height // 2)
        camera_matrix = np.array([
            [focal_length, 0, center[0]],
            [0, focal_length, center[1]],
            [0, 0, 1]
        ], dtype="double")

        dist_coeffs = np.zeros((4, 1))  # No lens distortion
        _, rotation_vector, _, _ = cv2.solvePnPRansac(MODEL_POINTS, image_points, camera_matrix, dist_coeffs)

        # Convert rotation vector to angles
        rotation_matrix, _ = cv2.Rodrigues(rotation_vector)
        angles, _, _, _, _, _ = cv2.RQDecomp3x3(rotation_matrix)

        yaw = angles[1]  # left/right
        pitch = angles[0]  # up/down

        if yaw > 15:
            return "right"
        elif yaw < -15:
            return "left"
        elif pitch > 15:
            return "down"
        elif pitch < -15:
            return "up"
        else:
            return "neutral"
estimator = HeadPoseEstimator()

def head_pose_node(state: AgentState) -> AgentState:
    frame = state["frame"]
    direction = estimator.get_head_direction(frame)

    # Update tilt counts
    if direction in state["head_data"]["tilt_counts"]:
        state["head_data"]["tilt_counts"][direction] += 1

    state["head_data"]["total_samples"] += 1
    return state