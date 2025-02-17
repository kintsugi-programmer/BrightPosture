from flask import Flask, request, jsonify
import subprocess

app = Flask(__name__)

def set_brightness_xrandr(brightness):
    try:
        display = subprocess.check_output("xrandr --listmonitors | grep '+' | awk '{print $4}'", shell=True).decode().strip()
        brightness_level = min(max(0.1, brightness / 100), 1.0)  # Convert to xrandr scale (0.1 - 1.0)
        subprocess.run(f"xrandr --output {display} --brightness {brightness_level}", shell=True, check=True)
        return True
    except Exception as e:
        return str(e)

@app.route('/', methods=['POST'])
def update_data():
    try:
        data = request.get_json()
        print(data)
        distance = int(data.get("distance", 0))  # Convert to integer
        light = int(data.get("light", 0))      # Convert to integer

        # linear
        brightness = min(max(5, light), 140)



        # expo
        # brightness = min(max(5, (light / 100) ** 1.5 * 100), 100)
        result = set_brightness_xrandr(int(brightness))

        if result is not True:
            return jsonify({"error": f"Failed to update brightness: {result}"}), 500

        response = {
            "message": "Brightness updated",
            "brightness": int(brightness),
            "distance": distance,
            "light": light
        }
        return jsonify(response), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
