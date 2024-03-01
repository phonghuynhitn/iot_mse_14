import sys
from Adafruit_IO import MQTTClient
import random
import time
from simple_ai import *
from uart import *

AIO_FEED_ID = ['nutnhan1', 'nutnhan2']
AIO_USERNAME = ""
AIO_KEY = ""

#new
def connected(client):
    print("Ket noi thanh cong ...")
    for feed in AIO_FEED_ID:
        client.subscribe(feed)

def subscribe(client , userdata , mid , granted_qos):
    print("Subscribe thanh cong ...")

def disconnected(client):
    print("Ngat ket noi ...")
    sys.exit (1)

def message(client , feed_id , payload):
    print("Nhan du lieu: " + payload + " tu " + feed_id)
    if feed_id == "nutnhan1":
        if payload == "0":
            writeData("0")
        else:
            writeData("1")
    if feed_id == "nutnhan2":
        if payload == "0":
            writeData("3")
        else:
            writeData("2")


client = MQTTClient(AIO_USERNAME , AIO_KEY)
client.on_connect = connected
client.on_disconnect = disconnected
client.on_message = message
client.on_subscribe = subscribe
client.connect()
client.loop_background()

last_update_time = time.time()
cambien = ['cambien1', 'cambien2', 'cambien3']
cambien_index = 0
counter_ai = 5

while True:
    # current_time = time.time()
    # if current_time - last_update_time >= 5:  # Kiểm tra nếu đã đủ 5 giây
    #     last_update_time = current_time
    #     value = random.randint(0, 100)
    #     sensor = cambien[cambien_index]
    #     print(f"{sensor} Cập nhật:", value)
    #     client.publish(sensor, value)
    #     cambien_index += 1  # Chuyển sang cảm biến tiếp theo
    #     if cambien_index >= len(cambien):  # Kiểm tra nếu đã qua hết danh sách
    #         cambien_index = 0  # Quay lại cảm biến đầu tiên
    # counter_ai = counter_ai - 1
    # if counter_ai <= 0:
    #     counter_ai = 5
    #     ai_result = image_detector()
    #     print("AI Output: ",ai_result)
    #     client.publish('ai', ai_result)

    readSerial(client)
    time.sleep(1)
