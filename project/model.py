import time
import datetime
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import random

class TemperaturePredictor:
    def __init__(self, file_path):
        self.file_path = file_path
        self.model = LinearRegression()

    def write_temperature_to_file(self, temperature):
        with open(self.file_path, "a") as file:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            file.write(f"{timestamp}, {temperature}\n")

    def read_temperature_data(self):
        timestamps = []
        temperatures = []
        with open(self.file_path, "r") as file:
            for line in file:
                timestamp, temperature = line.strip().split(", ")
                if float(temperature) > 0:
                    timestamps.append(datetime.datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S"))
                    temperatures.append(float(temperature))
        return timestamps, temperatures

    def train_model(self):
        timestamps, temperatures = self.read_temperature_data()
        X_train, X_test, y_train, y_test = train_test_split(np.array(range(len(timestamps))).reshape(-1, 1), temperatures, test_size=0.2, random_state=42)
        self.model.fit(X_train, y_train)

    def predict_next_temperature(self):
        timestamps, temperatures = self.read_temperature_data()
        next_minute = len(temperatures) + 1
        predicted_temperature = self.model.predict([[next_minute]])
        return predicted_temperature[0]

    def simulate_temperature_measurement(self):
        while True:
            temperature = random.randint(20, 40)

            if temperature is not None:
                print("Nhiệt độ: {:.1f}°C".format(temperature))

                self.write_temperature_to_file(temperature)

                self.train_model()

                predicted_temperature = self.predict_next_temperature()
                print("Dự đoán nhiệt độ cho phút {}: {:.1f}°C".format(next_minute, predicted_temperature))
            else:
                print("Không thể đọc dữ liệu từ cảm biến. Thử lại sau.")

            time.sleep(60)

if __name__ == "__main__":
    file_path = "temperature_data.txt"
    predictor = TemperaturePredictor(file_path)
    predictor.simulate_temperature_measurement()
