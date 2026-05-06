from flask import request, jsonify

# globalne zakresy (będą zmieniane dynamicznie)
dolny_pomarancz = np.array([15, 120, 120])
gorny_pomarancz = np.array([55, 255, 255])

@app.route('/set_color', methods=['POST'])
def set_color():
    global dolny_pomarancz, gorny_pomarancz

    data = request.json
    x = int(data['x'])
    y = int(data['y'])

    frame = picam2.capture_array()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    pixel = hsv[y, x]

    h, s, v = pixel

    # tolerancja (możesz zmienić)
    tol_h = 10
    tol_s = 80
    tol_v = 80

    dolny_pomarancz = np.array([
        max(h - tol_h, 0),
        max(s - tol_s, 0),
        max(v - tol_v, 0)
    ])

    gorny_pomarancz = np.array([
        min(h + tol_h, 179),
        min(s + tol_s, 255),
        min(v + tol_v, 255)
    ])

    return jsonify({"status": "ok"})