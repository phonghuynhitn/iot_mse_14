import time
import serial.tools.list_ports

class SensorsAndActuators:
    def __init__(self):
        self.portName = "/dev/ttyUSB0"
        self.relay2_ON  = [2, 6, 0, 0, 0, 255, 201, 185]
        self.relay2_OFF = [2, 6, 0, 0, 0, 0, 137, 249]
        self.relay3_ON  = [3, 6, 0, 0, 0, 255, 200, 104]
        self.relay3_OFF = [3, 6, 0, 0, 0, 0, 136, 40]
        self.relay4_ON  = [4, 6, 0, 0, 0, 255, 201, 223]
        self.relay4_OFF = [4, 6, 0, 0, 0, 0, 137, 159]
        self.soil_temperature = [1, 3, 0, 6, 0, 1, 100, 11]
        self.soil_moisture = [1, 3, 0, 7, 0, 1, 53, 203]
        try:
            self.ser = serial.Serial(port=self.portName, baudrate=9600)
            print("Opened successfully")
        except:
            print("Can not open the port")

    def serial_read_data(self):
        bytesToRead = self.ser.inWaiting()
        if bytesToRead > 0:
            out = self.ser.read(bytesToRead)
            data_array = [b for b in out]
            print(f"Device response data:", data_array)
            if len(data_array) >= 7:
                array_size = len(data_array)
                value = data_array[array_size - 4] * 256 + data_array[array_size - 3]
                return value
            else:
                return -1
        return 0

    def serial_write_data(self, data):
        self.ser.write(data)

    def set_relay(self, relay, state):
        if relay == 2:
            command = self.relay2_ON if state else self.relay2_OFF
        elif relay == 3:
            command = self.relay3_ON if state else self.relay3_OFF
        elif relay == 4:
            command = self.relay4_ON if state else self.relay4_OFF
        else:
            print("Invalid relay number")
            return
        self.ser.write(command)
        time.sleep(1)
        print(self.serial_read_data())

    def read_temperature(self):
        self.serial_read_data()
        self.ser.write(self.soil_temperature)
        time.sleep(1)
        return self.serial_read_data()

    def read_moisture(self):
        self.serial_read_data()
        self.ser.write(self.soil_moisture)
        time.sleep(1)
        return self.serial_read_data()
