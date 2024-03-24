#  pip install paho-mqtt==1.6.1
import paho.mqtt.client as mqtt
import time
from sensors_and_actuators import *
from model import *
import threading

MQTT_SERVER = "mqtt.ohstem.vn"
MQTT_PORT = 1883
MQTT_USERNAME = "mse14-group2"
MQTT_PASSWORD = "1234"
MQTT_TOPIC_PUB = [f"{MQTT_USERNAME}/feeds/temperature", f"{MQTT_USERNAME}/feeds/moisture", f"{MQTT_USERNAME}/feeds/predict_temperature_content"]
MQTT_TOPIC_SUB = [f"{MQTT_USERNAME}/feeds/relay02", f"{MQTT_USERNAME}/feeds/relay03", f"{MQTT_USERNAME}/feeds/relay04"]

temperature_index = 0
moisture_index = 1
predict_temperature_index = 0

relay02_index = 0
relay03_index = 1
relay04_index = 2

sensors_and_actuators = SensorsAndActuators()
file_path = "temperature_data.txt"
predictor = TemperaturePredictor(file_path)

def mqtt_connected(client, userdata, flags, rc):
    for feed in MQTT_TOPIC_SUB:
        client.subscribe(feed)
    print("Connected succesfully!!")
    

def mqtt_subscribed(client, userdata, mid, granted_qos):
    print("Subscribed to Topic!!!")

def message(client , feed_id , payload):
    print("Recieved: " + str(payload.payload.decode('utf-8')))
    data = str(payload.payload.decode('utf-8'))
    if feed_id == MQTT_TOPIC_SUB[relay02_index]:
        if data == '1':
            sensors_and_actuators.set_relay(2, True)
        elif data == '0':
            sensors_and_actuators.set_relay(2, False)
    if feed_id == MQTT_TOPIC_SUB[relay03_index]:
        if data == '1':
            sensors_and_actuators.set_relay(3, True)
        elif data == '0':
            sensors_and_actuators.set_relay(3, False)
    if feed_id == MQTT_TOPIC_SUB[relay04_index]:
        if data == '1':
            sensors_and_actuators.set_relay(4, True)
        elif data == '0':
            sensors_and_actuators.set_relay(4, False)
        
            

mqttClient = mqtt.Client()
mqttClient.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
mqttClient.connect(MQTT_SERVER, int(MQTT_PORT), 60)

#Register mqtt events
mqttClient.on_connect = mqtt_connected
mqttClient.on_subscribe = mqtt_subscribed
mqttClient.on_message =  message
mqttClient.loop_start()

#32*C
threshold = 3200

def process_temperature():
    global counter
    if counter <= 0:
        # temperature = sensors_and_actuators.read_temperature()
        # if temperature is not None:
        # print("Nhiệt độ: {:.1f}°C".format(temperature))
        predictor.train_model()
        predicted_temperature = predictor.predict_next_temperature()
        # mqttClient.publish(MQTT_TOPIC_PUB[predict_temperature_index], predicted_temperature)
        if float(predicted_temperature) > threshold:
            mqttClient.publish(MQTT_TOPIC_PUB[predict_temperature_index], "Dự báo nhiệt độ trong thời gian tới: {:.1f}°C. Cảnh báo nhiệt độ tăng quá cao!".format(temperature))
            print("Cảnh báo: Nhiệt độ cao!")
        else:
            mqttClient.publish(MQTT_TOPIC_PUB[predict_temperature_index], "Dự báo nhiệt độ trong thời gian tới: {:.1f}°C. Tình trạng bình thường".format(temperature))
            print("Tình trạng bình thường")
        print("Dự đoán nhiệt độ cho phút tới: {:.1f}".format(predicted_temperature))
        # else:
        #     print("Không thể đọc dữ liệu từ cảm biến. Thử lại sau.")
        counter = 60


counter = 60
while True:
    temperature = sensors_and_actuators.read_temperature()
    predictor.write_temperature_to_file(temperature)
    print(f"Nhiet do:", temperature)
    counter = counter - 1
    if counter <= 0:
        # Start the temperature processing thread
        temperature_thread = threading.Thread(target=process_temperature)
        temperature_thread.start()
        counter = 60
    # if temperature > 0:
    mqttClient.publish(MQTT_TOPIC_PUB[temperature_index], temperature, retain=True)

    moisture = sensors_and_actuators.read_moisture()
    print(f"Do am:", moisture)
    # if moisture > 0:
    mqttClient.publish(MQTT_TOPIC_PUB[moisture_index], moisture, retain=True)
    time.sleep(1)
