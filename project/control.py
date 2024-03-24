import tkinter as tk
import paho.mqtt.client as mqtt

# khởi tạo GUI
root = tk.Tk()
root.title("MAINTENANCE DASHBOARD")
root.geometry('400x300')
main_frame = tk.Frame(root)
main_frame.pack(expand=True, fill="both")

# Khởi tạo biến Tkinter
temperature_var = tk.StringVar(value="Temperature: --°C")
humidity_var = tk.StringVar(value="Humidity: --%")
# khai báo thông tin MQTT server
MQTT_SERVER = "mqtt.ohstem.vn"
MQTT_PORT = 1883
MQTT_USERNAME = "mse14-group2"
MQTT_PASSWORD = "1234"
MQTT_TOPIC_PUB = [f"{MQTT_USERNAME}/feeds/temperature", f"{MQTT_USERNAME}/feeds/moisture"]
MQTT_TOPIC_SUB = [f"{MQTT_USERNAME}/feeds/relay02", f"{MQTT_USERNAME}/feeds/relay03", f"{MQTT_USERNAME}/feeds/relay04"]

#temperature_index = 0
#moisture_index = 1
#sensors_and_actuators = SensorsAndActuators()

def mqtt_connected(client, userdata, flags, rc):
    print("Connected successfully with result code " + str(rc))
    # Assuming you want to subscribe to temperature and moisture feeds for updates
    client.subscribe(f"{MQTT_USERNAME}/feeds/temperature")
    client.subscribe(f"{MQTT_USERNAME}/feeds/moisture")

def mqtt_subscribed(client, userdata, mid, granted_qos):
    print("Subscribed to Topic with QOS", granted_qos)

def message(client, userdata, msg):
    payload = msg.payload.decode('utf-8')
    print(f"Received message '{payload}' on topic '{msg.topic}'")
    # Update temperature or humidity based on the topic
    if msg.topic == f"{MQTT_USERNAME}/feeds/temperature":
        temperature = float(payload) / 100
        temperature_var.set(f"{temperature}°C")
    elif msg.topic == f"{MQTT_USERNAME}/feeds/moisture":
        humidity_var.set(f"{payload}%")
# Cập nhật hàm control_relay để đảo trạng thái của relay
relay_states = {"relay02": False, "relay03": False, "relay04": False}

def control_relay(relay):
    # Đảo trạng thái relay
    relay_states[relay] = not relay_states[relay]
    state = relay_states[relay]
    topic = f"{MQTT_USERNAME}/feeds/{relay}"
    message = "ON" if state else "OFF"
    mqttClient.publish(topic, message)
    print(f"Published '{message}' to '{topic}'")
    # Cập nhật text của nút tương ứng
    if relay == "relay02":
        relay1_button.config(text=f"Relay 1 {'ON' if state else 'OFF'}")
    elif relay == "relay03":
        relay2_button.config(text=f"Relay 2 {'ON' if state else 'OFF'}")
    elif relay == "relay04":
        relay3_button.config(text=f"Relay 3 {'ON' if state else 'OFF'}")

mqttClient = mqtt.Client()
mqttClient.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
mqttClient.on_connect = mqtt_connected
mqttClient.on_message = message
mqttClient.connect(MQTT_SERVER, MQTT_PORT, 60)
mqttClient.loop_start()

# Tạo GUI
temperature_frame = tk.LabelFrame(root, text="Temperature", padx=10, pady=10)
temperature_frame.pack(padx=10, pady=10, fill="both", expand=True)
tk.Label(temperature_frame, textvariable=temperature_var, font=("Arial", 16)).pack()

humidity_frame = tk.LabelFrame(root, text="Humidity", padx=10, pady=10)
humidity_frame.pack(padx=10, pady=10, fill="both", expand=True)
tk.Label(humidity_frame, textvariable=humidity_var, font=("Arial", 16)).pack()
#Butoon Relay Control
# Tạo và định cấu hình các nút
button_frame = tk.Frame(root)
button_frame.pack(fill='x', pady=20)

relay1_button = tk.Button(button_frame, text="Relay 1 OFF", command=lambda: control_relay("relay02"))
relay1_button.pack(side='left', expand=True, padx=5)

relay2_button = tk.Button(button_frame, text="Relay 2 OFF", command=lambda: control_relay("relay03"))
relay2_button.pack(side='left', expand=True, padx=5)

relay3_button = tk.Button(button_frame, text="Relay 3 OFF", command=lambda: control_relay("relay04"))
relay3_button.pack(side='left', expand=True, padx=5)


root.mainloop()

