from src.utils import get_landmark_points

THUMB_TIP = 4
THUMB_IP = 3
THUMB_MCP = 2

INDEX_TIP = 8
MIDDLE_TIP = 12
RING_TIP = 16
PINKY_TIP = 20

INDEX_PIP = 6
MIDDLE_PIP = 10
RING_PIP = 14
PINKY_PIP = 18


def is_finger_up(points, tip_idx: int, pip_idx: int) -> bool:
    return points[tip_idx][1] < points[pip_idx][1]


def is_thumb_up(points) -> bool:
    # Simple starter rule for thumb:
    # thumb tip above thumb joint = thumb up
    return points[THUMB_TIP][1] < points[THUMB_IP][1]


def get_finger_states(hand_landmarks):
    points = get_landmark_points(hand_landmarks)

    thumb = 1 if is_thumb_up(points) else 0
    index = 1 if is_finger_up(points, INDEX_TIP, INDEX_PIP) else 0
    middle = 1 if is_finger_up(points, MIDDLE_TIP, MIDDLE_PIP) else 0
    ring = 1 if is_finger_up(points, RING_TIP, RING_PIP) else 0
    pinky = 1 if is_finger_up(points, PINKY_TIP, PINKY_PIP) else 0

    return [thumb, index, middle, ring, pinky]


def classify_gesture(hand_landmarks) -> str:
    fingers = get_finger_states(hand_landmarks)

    # [thumb, index, middle, ring, pinky]

    if fingers == [0, 0, 0, 0, 0]:
        return "Fist"

    if fingers == [0, 1, 0, 0, 0]:
        return "Pointing"

    if fingers == [0, 1, 1, 0, 0]:
        return "Peace Sign"

    if fingers == [0, 1, 1, 1, 0]:
        return "Three"

    if fingers == [0, 1, 1, 1, 1]:
        return "Four"

    if fingers == [1, 1, 1, 1, 1]:
        return "Open Palm"

    if fingers == [1, 0, 0, 0, 0]:
        return "Thumbs Up"

    return "Unknown"