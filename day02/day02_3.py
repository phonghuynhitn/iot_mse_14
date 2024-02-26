import sys
from Adafruit_IO import MQTTClient
import random
import time

AIO_FEED_ID = ['nutnhan1', 'nutnhan2']
AIO_USERNAME = ""
AIO_KEY = ""

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
    print("Nhan du lieu: " + payload)

client = MQTTClient(AIO_USERNAME , AIO_KEY, secure=False)
client.on_connect = connected
client.on_disconnect = disconnected
client.on_message = message
client.on_subscribe = subscribe
client.connect()
client.loop_background()

last_update_time = time.time()
cambien = ['cambien1', 'cambien2', 'cambien3']
cambien_index = 0

while True:
    current_time = time.time()
    if current_time - last_update_time >= 5:  # Kiểm tra nếu đã đủ 5 giây
        last_update_time = current_time
        value = random.randint(0, 100)
        sensor = cambien[cambien_index]
        print(f"{sensor} Cập nhật:", value)
        client.publish(sensor, value)
        cambien_index += 1  # Chuyển sang cảm biến tiếp theo
        if cambien_index >= len(cambien):  # Kiểm tra nếu đã qua hết danh sách
            cambien_index = 0  # Quay lại cảm biến đầu tiên
    time.sleep(1)
