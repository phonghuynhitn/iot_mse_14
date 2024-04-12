import tkinter as tk
import paho.mqtt.client as mqtt
import re

# Initialize the GUI
root = tk.Tk()
root.title("MAINTENANCE DASHBOARD")
root.geometry('800x400')
main_frame = tk.Frame(root)
main_frame.pack(expand=True, fill="both")

# Initialize Tkinter variables
temperature_var = tk.StringVar(value="Temperature: --°C")
humidity_var = tk.StringVar(value="Humidity: --%")
predict_var = tk.StringVar(value="Prediction: --")

# MQTT server information
MQTT_SERVER = "mqtt.ohstem.vn"
MQTT_PORT = 1883
MQTT_USERNAME = "mse14-group2"
MQTT_PASSWORD = "1234"
MQTT_TOPIC_PUB = [
    f"{MQTT_USERNAME}/feeds/temperature",
    f"{MQTT_USERNAME}/feeds/moisture",
    f"{MQTT_USERNAME}/feeds/predict_temperature_content"
]
MQTT_TOPIC_SUB = [
    f"{MQTT_USERNAME}/feeds/relay02",
    f"{MQTT_USERNAME}/feeds/relay03",
    f"{MQTT_USERNAME}/feeds/relay04"
]
def extract_prediction(payload):
    temp_match = re.search(r'\d+\.?\d*', payload)  # Search for the first number in the payload
    temperature = temp_match.group(0) if temp_match else "N/A"
    status_start = payload.find('Status:')  # Find the start of the status message
    status = payload[status_start + 7:].strip() if status_start != -1 else "Unknown status"
    return temperature, status

def mqtt_connected(client, userdata, flags, rc):
    print("Connected successfully with result code " + str(rc))
    client.subscribe([(topic, 0) for topic in MQTT_TOPIC_PUB])

def mqtt_subscribed(client, userdata, mid, granted_qos):
    print("Subscribed to Topic with QOS", granted_qos)
def message(client, userdata, msg):
    payload = msg.payload.decode('utf-8')
    print(f"Received message '{payload}' on topic '{msg.topic}'")

    # Check if the message is a prediction message
    if "Dự báo nhiệt độ trong thời gian tới" in payload:
        # It's a prediction message; display it in the Prediction frame
        predict_var.set(payload)
    elif msg.topic == f"{MQTT_USERNAME}/feeds/temperature":
        # It's a regular temperature message; process and display it
        try:
            match = re.search(r"[-+]?\d*\.\d+|\d+", payload)
            if match:
                temperature = float(match.group()) / 100
                temperature_var.set(f"{temperature:.2f}°C")
            else:
                temperature_var.set("Temperature: Error")
        except ValueError:
            temperature_var.set("Temperature: Error")
    elif msg.topic == f"{MQTT_USERNAME}/feeds/moisture":
        try:
            humidity = int(payload)
            humidity_var.set(f"{humidity}%")
        except ValueError:
            humidity_var.set("Humidity: Error")

relay_states = {"relay02": False, "relay03": False, "relay04": False}

def control_relay(relay):
    relay_states[relay] = not relay_states[relay]
    mqttClient.publish(f"{MQTT_USERNAME}/feeds/{relay}", "1" if relay_states[relay] else "0")
    update_relay_buttons()

def update_relay_buttons():
    relay1_button.config(text=f"Relay 1 {'ON' if relay_states['relay02'] else 'OFF'}")
    relay2_button.config(text=f"Relay 2 {'ON' if relay_states['relay03'] else 'OFF'}")
    relay3_button.config(text=f"Relay 3 {'ON' if relay_states['relay04'] else 'OFF'}")

mqttClient = mqtt.Client()
mqttClient.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
mqttClient.on_connect = mqtt_connected
mqttClient.on_message = message
mqttClient.connect(MQTT_SERVER, MQTT_PORT, 60)
mqttClient.loop_start()

# GUI Layout
temperature_frame = tk.LabelFrame(root, text="Temperature", padx=10, pady=10)
temperature_frame.pack(padx=10, pady=10, fill="both", expand=True)
tk.Label(temperature_frame, textvariable=temperature_var, font=("Arial", 16)).pack()

humidity_frame = tk.LabelFrame(root, text="Humidity", padx=10, pady=10)
humidity_frame.pack(padx=10, pady=10, fill="both", expand=True)
tk.Label(humidity_frame, textvariable=humidity_var, font=("Arial", 16)).pack()

predict_frame = tk.LabelFrame(root, text="Predict", padx=10, pady=10)
predict_frame.pack(padx=10, pady=10, fill="both", expand=True)
tk.Label(predict_frame, textvariable=predict_var, font=("Arial", 16)).pack()

# Button Relay Control
button_frame = tk.Frame(root)
button_frame.pack(fill='x', pady=20)


relay1_button = tk.Button(button_frame, text="Relay 1 OFF", command=lambda: control_relay("relay02"))
relay1_button.pack(side='left', expand=True, padx=5)

relay2_button = tk.Button(button_frame, text="Relay 2 OFF", command=lambda: control_relay("relay03"))
relay2_button.pack(side='left', expand=True, padx=5)

relay3_button = tk.Button(button_frame, text="Relay 3 OFF", command=lambda: control_relay("relay04"))
relay3_button.pack(side='left', expand=True, padx=5)

root.mainloop()
