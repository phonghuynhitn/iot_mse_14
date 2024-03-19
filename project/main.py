#  pip install paho-mqtt==1.6.1
import paho.mqtt.client as mqtt
import time
from rs485 import *

MQTT_SERVER = "mqtt.ohstem.vn"
MQTT_PORT = 1883
MQTT_USERNAME = "mse14-group2"
MQTT_PASSWORD = "1234"
# MQTT_TOPIC_PUB = MQTT_USERNAME + "/feeds/V1"
# MQTT_TOPIC_SUB = MQTT_USERNAME + "/feeds/V1"
MQTT_TOPIC_PUB =  [MQTT_USERNAME + "/feeds/temperature", MQTT_USERNAME + "/feeds/moisture"]
MQTT_TOPIC_SUB = [MQTT_USERNAME + "/feeds/relay02", MQTT_USERNAME + "/feeds/relay03", MQTT_USERNAME + "/feeds/relay04"]

temperature_index = 0
moisture_index = 1


def mqtt_connected(client, userdata, flags, rc):
    for feed in MQTT_TOPIC_SUB:
        client.subscribe(feed)
    print("Connected succesfully!!")
    

def mqtt_subscribed(client, userdata, mid, granted_qos):
    print("Subscribed to Topic!!!")

def message(client , feed_id , payload):
    print("Recieved: " + str(payload.payload.decode('utf-8')))


mqttClient = mqtt.Client()
mqttClient.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
mqttClient.connect(MQTT_SERVER, int(MQTT_PORT), 60)

#Register mqtt events
mqttClient.on_connect = mqtt_connected
mqttClient.on_subscribe = mqtt_subscribed
mqttClient.on_message =  message
mqttClient.loop_start()

counter = 0
while True:
    temperature = readTemperature()
    print(f"Nhiet do:", temperature)
    if temperature > 0:
        mqttClient.publish(MQTT_TOPIC_PUB[temperature_index], temperature)

    moisture = readMoisture()
    print(f"Do am:", moisture)
    if moisture > 0:
        mqttClient.publish(MQTT_TOPIC_PUB[moisture_index], moisture)
    time.sleep(1)
