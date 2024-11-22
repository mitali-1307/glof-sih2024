from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
from flask_socketio import SocketIO, emit
import logging

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/sendData', methods=['POST'])
def post_data():
    try:
        data = request.get_json()

        # Extract sensor data
        temperature = data.get('temperature')
        humidity = data.get('humidity')
        pressure = data.get('pressure')
        wind_speed = data.get('wind_speed')
        wind_direction = data.get('wind_direction')
        altitude = data.get('altitude')

        weather_data = {
            'temperature': temperature,
            'humidity': humidity,
            'pressure': pressure,
            'wind_speed': wind_speed,
            'wind_direction': wind_direction,
            'altitude': altitude
        }

        # Log received data
        app.logger.info(f"Weather data received: {weather_data}")

        # Send data to WebSocket clients
        socketio.emit('weather_data', weather_data)

        return jsonify({'message': 'Data received successfully'}), 200

    except Exception as e:
        app.logger.error(f"Error in /sendData endpoint: {e}")
        return jsonify({'error': str(e)}), 500

@socketio.on('connect')
def handle_connect():
    app.logger.info("Client connected")

@socketio.on('disconnect')
def handle_disconnect():
    app.logger.info("Client disconnected")

if __name__ == '_main_':
    socketio.run(app, debug=True,port=5002)
