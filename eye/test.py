from flask import Flask, Response
from picamera2 import Picamera2
import cv2
import numpy as np

app = Flask(__name__)

# Inicjalizacja kamery
picam2 = Picamera2()
picam2.configure(
    picam2.create_preview_configuration(
        main={"format": "RGB888", "size": (640, 480)}
    )
)
picam2.start()

# Zakres koloru pomarańczowego (HSV)
dolny_pomarancz = np.array([0, 70, 155])
gorny_pomarancz = np.array([35, 200, 230])


def generate_frames():
    while True:
        frame = picam2.capture_array()

        # BGR → HSV
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Maska
        mask = cv2.inRange(hsv, dolny_pomarancz, gorny_pomarancz)

        # Kontury
        contours, _ = cv2.findContours(
            mask,
            cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE
        )

        # Rysowanie
        for cnt in contours:
            if cv2.contourArea(cnt) > 500:
                x, y, w, h = cv2.boundingRect(cnt)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Kodowanie do JPEG
        _, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()

        # MJPEG stream
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')


@app.route('/video')
def video():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/')
def index():
    return '''
    <html>
        <body>
            <h1>Detekcja kamery</h1>
            <img src="/video">
        </body>
    </html>
    '''


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)