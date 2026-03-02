"""
オフセットの除去
"""
import board
from adafruit_lsm6ds.lsm6ds33 import LSM6DS33
from adafruit_lsm6ds import Rate, GyroRange
import time
import math
import csv

class GYRO():
    def __init__(self):
        i2c = board.I2C()
        self.sensor = LSM6DS33(i2c, address=0x6B)

        self.sensor.gyro_data_rate = Rate.RATE_416_HZ
        self.sensor.gyro_range = GyroRange.RANGE_250_DPS

        self.offset = self._calibrate()

    def _calibrate(self):
        total = 0.0
        for _ in range(1000):
            total += self.sensor.gyro[2]
            time.sleep(1/416)
        return total / 1000

    def read(self):
        return self.sensor.temperature, self.sensor.gyro[2]-self.offset

def main():
    time.sleep(5)#安定用
    gyro = GYRO()
    mem = []
    input("記録開始")
    while True:
        try:
            temp_mem, gyro_mem = gyro.read()
            mem.append([time.time(),temp_mem,gyro_mem])
        except KeyboardInterrupt:
            print("停止")
            break
        time.sleep(0.05)
    with open("temperature_gyro.csv", mode = "w") as f:
        write = csv.writer(f)
        write.writerow(["time_unix_s", "temp_C", "gyroZ_radps_corr"])
        write.writerows(mem)
    print("記録終了")

if __name__ == "__main__":
    main()