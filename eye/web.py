from flask import Flask, Response, request, jsonify
import processing

app = Flask(__name__)


@app.route('/video')
def video():
    return Response(processing.generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/set_color', methods=['POST'])
def set_color_route():
    data = request.json
    x = int(data.get('x', 0))
    y = int(data.get('y', 0))

    res = processing.set_color(x, y)
    return jsonify(res)


@app.route('/')
def index():
    return '''
    <html>
        <body>
            <h1>Kliknij w obraz, aby wybrać kolor</h1>
            <p>Po kliknięciu zakres HSV ustawi się automatycznie</p>

            <img id="video" src="/video" style="cursor: crosshair; max-width: 100%;">

            <script>
            const img = document.getElementById("video");

            img.addEventListener("click", function(event) {
                const rect = img.getBoundingClientRect();

                const scaleX = 640 / rect.width;
                const scaleY = 480 / rect.height;

                const x = Math.floor((event.clientX - rect.left) * scaleX);
                const y = Math.floor((event.clientY - rect.top) * scaleY);

                fetch('/set_color', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({x: x, y: y})
                });
            });
            </script>
        </body>
    </html>
    '''
