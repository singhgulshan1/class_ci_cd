from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
from rembg import remove
import io

app = Flask(__name__)
CORS(app) # HTML file ko API se connect hone ki permission deta hai

@app.route('/remove-bg', methods=['POST'])
def remove_background():
    # Check karein ki image aayi hai ya nahi
    if 'image' not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    file = request.files['image']
    if file.filename == '':
        return jsonify({"error": "No image selected"}), 400

    try:
        # Image ko padhein
        input_image = file.read()

        # Jadoo! Yahan background remove hota hai
        output_image = remove(input_image)

        # Process ki hui image wapas frontend ko bhejein
        return send_file(
            io.BytesIO(output_image),
            mimetype='image/png',
            as_attachment=True,
            download_name='bg_removed.png'
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    print("Background Remover Server Started! (Port 5001)")
    app.run(host='0.0.0.0', port=5001, debug=True)