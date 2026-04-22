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

INDEX_MCP = 5
MIDDLE_MCP = 9
RING_MCP = 13
PINKY_MCP = 17


def is_finger_extended(points, tip_idx: int, pip_idx: int, mcp_idx: int) -> bool:
    """
    More robust than just tip < pip.
    Finger is considered up when:
    - tip is above pip
    - pip is above mcp
    """
    return points[tip_idx][1] < points[pip_idx][1] < points[mcp_idx][1]


def is_thumb_extended(points) -> bool:
    """
    Simple thumb rule.
    This is still approximate, so we won't depend on it heavily for 3 and 4.
    """
    thumb_tip_x, thumb_tip_y = points[THUMB_TIP]
    thumb_ip_x, thumb_ip_y = points[THUMB_IP]
    thumb_mcp_x, thumb_mcp_y = points[THUMB_MCP]

    # Thumb is considered extended if it's clearly separated from the hand
    x_separation = abs(thumb_tip_x - thumb_mcp_x)
    y_separation = abs(thumb_tip_y - thumb_mcp_y)

    return x_separation > 0.08 or y_separation > 0.12


def get_finger_states(hand_landmarks):
    points = get_landmark_points(hand_landmarks)

    thumb = 1 if is_thumb_extended(points) else 0
    index = 1 if is_finger_extended(points, INDEX_TIP, INDEX_PIP, INDEX_MCP) else 0
    middle = 1 if is_finger_extended(points, MIDDLE_TIP, MIDDLE_PIP, MIDDLE_MCP) else 0
    ring = 1 if is_finger_extended(points, RING_TIP, RING_PIP, RING_MCP) else 0
    pinky = 1 if is_finger_extended(points, PINKY_TIP, PINKY_PIP, PINKY_MCP) else 0

    return {
        "thumb": thumb,
        "index": index,
        "middle": middle,
        "ring": ring,
        "pinky": pinky,
    }


def classify_gesture(hand_landmarks) -> str:
    fingers = get_finger_states(hand_landmarks)

    thumb = fingers["thumb"]
    index = fingers["index"]
    middle = fingers["middle"]
    ring = fingers["ring"]
    pinky = fingers["pinky"]

    non_thumb_count = index + middle + ring + pinky
    total_count = thumb + non_thumb_count

    # Exact patterns first for named gestures
    if non_thumb_count == 0 and thumb == 0:
        return "Fist"

    if index == 1 and middle == 0 and ring == 0 and pinky == 0:
        return "Pointing"

    if index == 1 and middle == 1 and ring == 0 and pinky == 0:
        return "Peace Sign"

    # More stable number logic
    if index == 1 and middle == 1 and ring == 1 and pinky == 0:
        return "Three"

    if index == 1 and middle == 1 and ring == 1 and pinky == 1:
        # Whether thumb is in or out, most people still mean "Four"
        return "Four"

    if total_count >= 4 and thumb == 1 and non_thumb_count == 4:
        return "Open Palm"

    if thumb == 1 and non_thumb_count == 0:
        return "Thumbs Up"

    return "Unknown"