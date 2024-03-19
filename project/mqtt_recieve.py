import paho.mqtt.client as mqtt
import time

MQTT_SERVER = "mqtt.ohstem.vn"
MQTT_PORT = 1883
MQTT_USERNAME = "group2"
MQTT_PASSWORD = "123"
MQTT_TOPIC_PUB = MQTT_USERNAME + "/feeds/V2"
MQTT_TOPIC_SUB = MQTT_USERNAME + "/feeds/V1"


def mqtt_connected(client, userdata, flags, rc):
    print("Connected succesfully!!")
    client.subscribe(MQTT_TOPIC_SUB)

def mqtt_subscribed(client, userdata, mid, granted_qos):
    print("Subscribed to Topic!!!")

def mqtt_recv_message(client, userdata, message):
    #print("Received: ", message.payload.decode("utf-8"))
    print(" Received message " + message.payload.decode("utf-8")
          + " on topic '" + message.topic
          + "' with QoS " + str(message.qos))
    mqttClient.publish(MQTT_TOPIC_PUB, 1)
    # status = 3
    # counter = 30

mqttClient = mqtt.Client()
mqttClient.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
mqttClient.connect(MQTT_SERVER, int(MQTT_PORT), 60)

#Register mqtt events
mqttClient.on_connect = mqtt_connected
mqttClient.on_subscribe = mqtt_subscribed
mqttClient.on_message = mqtt_recv_message

mqttClient.loop_start()

# counter = 0
# status = 0
# sensor_temp = 1
# re_send = 0
while True:
    pass
    # if status == 0:
    #     sensor_temp += 1
    #     mqttClient.publish(MQTT_TOPIC_PUB, sensor_temp)
    #     counter = 5
    #     status = 1

    # elif status == 1:
    #     counter -= 1
    #     if counter <= 0:
    #         status = 2

    # elif status == 2:
    #     print("Gửi lại dữ liệu")
    #     mqttClient.publish(MQTT_TOPIC_PUB, sensor_temp)
    #     counter = 5
    #     status = 1
    #     re_send += 1
    #     if re_send >=3:
    #         status = 3
    #         counter = 30
    #         re_send = 0

    # elif status == 3:
    #     counter -= 1
    #     if counter <= 0:
    #         status = 0

    # else:
    #     pass

    # time.sleep(1)