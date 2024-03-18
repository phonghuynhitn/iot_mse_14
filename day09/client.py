from opcua import Client
import time
url = "opc.tcp://172.16.7.13:4840"
client = Client(url)
client.connect()
print("Client Connected")
while True:
    Temp = client.get_node ("ns=2; i=2")
    Temperature = Temp.get_value()
    print(Temperature)
    Press = client.get_node("ns=2;i=3")
    Pressure = Press.get_value()
    print(Pressure)
    TIME = client.get_node("ns=2; i=4")
    TIME_Value = TIME.get_value()
    print(TIME_Value)
    time.sleep (1)