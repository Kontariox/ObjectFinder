from picamera2 import Picamera2
import threading
import time

picam2 = None
_latest_frame = None
_lock = threading.Lock()
_started = False


def start_camera():
    global picam2, _started

    if _started:
        return

    picam2 = Picamera2()

    picam2.configure(
        picam2.create_preview_configuration(
            main={"format": "RGB888", "size": (640, 480)}
        )
    )

    # Stabilne parametry obrazu
    picam2.set_controls(
        {
            "AeEnable": False,
            "AwbEnable": False,
            "ExposureTime": 10000,
            "AnalogueGain": 1.5,
        }
    )

    picam2.start()

    threading.Thread(target=_capture_frames, daemon=True).start()

    _started = True


def _capture_frames():
    global _latest_frame

    while True:
        frame = picam2.capture_array()

        with _lock:
            _latest_frame = frame

        time.sleep(0.01)


def get_frame_copy():
    if not _started:
        start_camera()

    with _lock:
        if _latest_frame is None:
            return None

        return _latest_frame.copy()