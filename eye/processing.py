import cv2
import numpy as np
from camera import get_frame_copy

<<<<<<< HEAD
# Selected HSV range (from click)
dolny = np.array([15, 120, 120], dtype=np.uint8)
gorny = np.array([55, 255, 255], dtype=np.uint8)

# Floor HSV range (detected automatically)
floor_dolny = np.array([0, 0, 0], dtype=np.uint8)
floor_gorny = np.array([179, 255, 255], dtype=np.uint8)

# Modes: 'mark_selected', 'mark_floor', 'mark_non_floor'
mode = 'mark_selected'


def generate_frames():
    global dolny, gorny, floor_dolny, floor_gorny, mode

=======
# HSV zakres (dynamiczny)
dolny = np.array([15, 120, 120], dtype=np.uint8)
gorny = np.array([55, 255, 255], dtype=np.uint8)


def generate_frames():
>>>>>>> 3407950cd27d45708d08c2ffa3995018b0296dfc
    while True:
        frame = get_frame_copy()
        if frame is None:
            continue

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
<<<<<<< HEAD

        if mode == 'mark_floor':
            mask = cv2.inRange(hsv, floor_dolny, floor_gorny)
        elif mode == 'mark_non_floor':
            floor_mask = cv2.inRange(hsv, floor_dolny, floor_gorny)
            mask = cv2.bitwise_not(floor_mask)
        else:  # mark_selected
            mask = cv2.inRange(hsv, dolny, gorny)

        kernel = np.ones((5, 5), np.uint8)

        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
=======
        mask = cv2.inRange(hsv, dolny, gorny)
>>>>>>> 3407950cd27d45708d08c2ffa3995018b0296dfc

        contours, _ = cv2.findContours(
            mask,
            cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE
        )

        for cnt in contours:
            if cv2.contourArea(cnt) > 500:
                x, y, w, h = cv2.boundingRect(cnt)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        _, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')


def set_color(x: int, y: int):
<<<<<<< HEAD
    """Set HSV range based on pixel at (x, y). Switches mode to mark_selected."""
    global dolny, gorny, mode
=======
    """Set HSV range based on pixel at (x, y). Returns a dict with status."""
    global dolny, gorny
>>>>>>> 3407950cd27d45708d08c2ffa3995018b0296dfc

    frame = get_frame_copy()
    if frame is None:
        return {"status": "no frame"}

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    if y >= hsv.shape[0] or x >= hsv.shape[1]:
        return {"status": "out of bounds"}

    pixel = hsv[y, x]
    h, s, v = int(pixel[0]), int(pixel[1]), int(pixel[2])

    # tolerancja
    tol_h = 10
    tol_s = 80
    tol_v = 80

    dolny = np.array([
        max(h - tol_h, 0),
        max(s - tol_s, 0),
        max(v - tol_v, 0)
    ], dtype=np.uint8)

    gorny = np.array([
        min(h + tol_h, 179),
        min(s + tol_s, 255),
        min(v + tol_v, 255)
    ], dtype=np.uint8)

<<<<<<< HEAD
    mode = 'mark_selected'

    return {"status": "ok", "dolny": dolny.tolist(), "gorny": gorny.tolist()}


def detect_floor(bottom_fraction: float = 0.25):
    """Analyze bottom part of frame to detect dominant floor HSV range."""
    global floor_dolny, floor_gorny

    frame = get_frame_copy()
    if frame is None:
        return {"status": "no frame"}

    h = frame.shape[0]
    start_row = int(h * (1.0 - bottom_fraction))
    sample = frame[start_row:h, :, :]

    hsv = cv2.cvtColor(sample, cv2.COLOR_BGR2HSV)

    # reshape and compute median color
    pixels = hsv.reshape(-1, 3)
    med = np.median(pixels, axis=0).astype(int)
    mh, ms, mv = int(med[0]), int(med[1]), int(med[2])

    tol_h = 15
    tol_s = 80
    tol_v = 80

    floor_dolny = np.array([
        max(mh - tol_h, 0),
        max(ms - tol_s, 0),
        max(mv - tol_v, 0)
    ], dtype=np.uint8)

    floor_gorny = np.array([
        min(mh + tol_h, 179),
        min(ms + tol_s, 255),
        min(mv + tol_v, 255)
    ], dtype=np.uint8)

    return {"status": "ok", "floor_dolny": floor_dolny.tolist(), "floor_gorny": floor_gorny.tolist()}


def set_mode(new_mode: str):
    """Set processing mode. Allowed: 'mark_selected','mark_floor','mark_non_floor'"""
    global mode
    if new_mode not in ('mark_selected', 'mark_floor', 'mark_non_floor'):
        return {"status": "invalid mode"}
    mode = new_mode
    return {"status": "ok", "mode": mode}

=======
    return {"status": "ok", "dolny": dolny.tolist(), "gorny": gorny.tolist()}
>>>>>>> 3407950cd27d45708d08c2ffa3995018b0296dfc
