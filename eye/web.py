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



@app.route('/set_mode', methods=['POST'])
def set_mode_route():
    data = request.json
    mode = data.get('mode')
    res = processing.set_mode(mode)
    return jsonify(res)


@app.route('/detect_floor', methods=['POST'])
def detect_floor_route():
    res = processing.detect_floor()
    return jsonify(res)


@app.route('/')
def index():
    return '''
    <html>
        <body>
            <h1>Kliknij w obraz, aby wybrać kolor</h1>
            <p>Po kliknięciu zakres HSV ustawi się automatycznie</p>

            <div>
                <label><input type="radio" name="mode" value="mark_selected" checked> Zaznacz wybrany kolor</label>
                <label><input type="radio" name="mode" value="mark_floor"> Zaznacz podłogę</label>
                <label><input type="radio" name="mode" value="mark_non_floor"> Zaznacz wszystko poza podłogą</label>
                <button id="detectFloor">Wykryj podłogę</button>
            </div>

            <img id="video" src="/video" style="cursor: crosshair; max-width: 100%; display:block; margin-top:10px;">

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
                }).then(()=>{
                    // switch mode to selected
                    document.querySelector('input[value="mark_selected"]').checked = true;
                    fetch('/set_mode', {method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({mode:'mark_selected'})});
                });
            });

            document.querySelectorAll('input[name="mode"]').forEach(r=>{
                r.addEventListener('change', ()=>{
                    fetch('/set_mode', {method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({mode: r.value})});
                });
            });

            document.getElementById('detectFloor').addEventListener('click', ()=>{
                fetch('/detect_floor', {method:'POST'}).then(()=>{
                    document.querySelector('input[value="mark_floor"]').checked = true;
                    fetch('/set_mode', {method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({mode:'mark_floor'})});
                });
            });
            </script>
        </body>
    </html>
    '''
