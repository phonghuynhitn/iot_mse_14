import tkinter as tk
from tkinter import ttk
import paho.mqtt.client as mqtt
import time
from sensors_and_actuators import *
sensors_and_actuators = SensorsAndActuators()
# MQTT settings
# MQTT_SERVER = "mqtt.ohstem.vn"
# MQTT_PORT = 1883
# MQTT_USERNAME = "mse14-group2"
# MQTT_PASSWORD = "1234"
# MQTT_TOPIC_PUB = [f"{MQTT_USERNAME}/feeds/temperature", f"{MQTT_USERNAME}/feeds/moisture"]
# MQTT_TOPIC_SUB = [f"{MQTT_USERNAME}/feeds/relay02", f"{MQTT_USERNAME}/feeds/relay03", f"{MQTT_USERNAME}/feeds/relay04"]

# # Indices for MQTT topics
# temperature_index = 0
# moisture_index = 1
# relay02_index = 0
# relay03_index = 1
# relay04_index = 2

# # Initialize MQTT client
# mqttClient = mqtt.Client()
# mqttClient.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
# mqttClient.connect(MQTT_SERVER, MQTT_PORT, 60)

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Control Panel")

        # Labels for temperature and humidity
        self.temperature_label = ttk.Label(self, text="Temperature:")
        self.temperature_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.temperature_entry = ttk.Entry(self)
        self.temperature_entry.grid(row=0, column=1, padx=10, pady=5)

        self.humidity_label = ttk.Label(self, text="Humidity:")
        self.humidity_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.humidity_entry = ttk.Entry(self)
        self.humidity_entry.grid(row=1, column=1, padx=10, pady=5)

        # Buttons for relays
        self.relay2_button = ttk.Button(self, text="Relay 2: OFF", command=lambda: self.toggle_relay(2))
        self.relay2_button.grid(row=2, column=0, padx=10, pady=5)
        self.relay3_button = ttk.Button(self, text="Relay 3: OFF", command=lambda: self.toggle_relay(3))
        self.relay3_button.grid(row=2, column=1, padx=10, pady=5)
        self.relay4_button = ttk.Button(self, text="Relay 4: OFF", command=lambda: self.toggle_relay(4))
        self.relay4_button.grid(row=2, column=2, padx=10, pady=5)

        # Register MQTT events
        # mqttClient.on_message = self.message
        # mqttClient.on_connect = self.mqtt_connected
        # mqttClient.on_subscribe = self.mqtt_subscribed
        # mqttClient.loop_start()

        # Start sending sensor data
        # self.send_sensor_data()

    # def mqtt_connected(self, client, userdata, flags, rc):
    #     for feed in MQTT_TOPIC_SUB:
    #         client.subscribe(feed)
    #     print("Connected successfully!!")

    # def mqtt_subscribed(self, client, userdata, mid, granted_qos):
    #     print("Subscribed to Topic!!!")

    # def message(self, client, userdata, msg):
    #     data = msg.payload.decode('utf-8')
    #     if msg.topic == MQTT_TOPIC_SUB[relay02_index]:
    #         self.update_relay_button(self.relay1_button, data)
    #     elif msg.topic == MQTT_TOPIC_SUB[relay03_index]:
    #         self.update_relay_button(self.relay2_button, data)
    #     elif msg.topic == MQTT_TOPIC_SUB[relay04_index]:
    #         self.update_relay_button(self.relay3_button, data)

    def update_relay_button(self, button, data):
        if data == '1':
            button["text"] = button["text"].replace("OFF", "ON")
        elif data == '0':
            button["text"] = button["text"].replace("ON", "OFF")

    def toggle_relay(self, relay_num):
        button = None
        if relay_num == 2:
            button = self.relay2_button
        elif relay_num == 3:
            button = self.relay3_button
        elif relay_num == 4:
            button = self.relay4_button
        print(button["text"])
        if "OFF" in button["text"]:
            button["text"] = button["text"].replace("OFF", "ON")
        else:
            button["text"] = button["text"].replace("ON", "OFF")
        
        if "ON" in button["text"]:
            # mqttClient.publish(MQTT_TOPIC_SUB[relay_num - 2], "0", retain=True)
            sensors_and_actuators.set_relay(relay_num, True)
        else:
            # mqttClient.publish(MQTT_TOPIC_SUB[relay_num - 2], "1", retain=True)
            sensors_and_actuators.set_relay(relay_num, False)


    # def send_sensor_data(self):
    #     while True:
    #         temperature = sensors_and_actuators.read_temperature()
    #         print(f"Nhiet do:", temperature)
    #         if temperature > 0:
    #             mqttClient.publish(MQTT_TOPIC_PUB[temperature_index], temperature, retain=True)

    #         moisture = sensors_and_actuators.read_moisture()
    #         print(f"Do am:", moisture)
    #         if moisture > 0:
    #             mqttClient.publish(MQTT_TOPIC_PUB[moisture_index], moisture, retain=True)
    #         time.sleep(1)

if __name__ == "__main__":
    app = Application()
    app.mainloop()
