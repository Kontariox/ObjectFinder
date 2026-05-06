from picamera2 import Picamera2
import threading

picam2 = Picamera2()
picam2.configure(
    picam2.create_preview_configuration(
        main={"format": "RGB888", "size": (640, 480)}
    )
)
picam2.start()

_latest_frame = None
_lock = threading.Lock()


def _capture_frames():
    global _latest_frame
    while True:
        frame = picam2.capture_array()
        with _lock:
            _latest_frame = frame


threading.Thread(target=_capture_frames, daemon=True).start()


def get_frame_copy():
    with _lock:
        if _latest_frame is None:
            return None
        return _latest_frame.copy()
