import cv2
import numpy as np
from camera import get_frame_copy

# HSV zakres (dynamiczny)
dolny = np.array([15, 120, 120], dtype=np.uint8)
gorny = np.array([55, 255, 255], dtype=np.uint8)


def generate_frames():
    while True:
        frame = get_frame_copy()
        if frame is None:
            continue

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, dolny, gorny)

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
    """Set HSV range based on pixel at (x, y). Returns a dict with status."""
    global dolny, gorny

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

    return {"status": "ok", "dolny": dolny.tolist(), "gorny": gorny.tolist()}
