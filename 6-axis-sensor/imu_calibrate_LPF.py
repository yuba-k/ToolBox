"""
オフセットの除去と一次LPF
"""
import board
from adafruit_lsm6ds.lsm6ds33 import LSM6DS33
from adafruit_lsm6ds import Rate, GyroRange
import time
import math
import threading

class GYRO():
    def __init__(self):
        i2c = board.I2C()
        self.sensor = LSM6DS33(i2c, address=0x6B)

        self.sensor.gyro_data_rate = Rate.RATE_416_HZ
        self.sensor.gyro_range = GyroRange.RANGE_250_DPS

        self.offset = self._calibrate()
        self.alpha = 0.2
        self.filtered = 0.0

    def _calibrate(self):
        total = 0.0
        for _ in range(1000):
            total += math.degrees(self.sensor.gyro[2])
            time.sleep(1/416)
        return total / 1000

    def _load(self):
        old = time.perf_counter()
        while self.running:
            now = time.perf_counter()
            dt = now - old
            gyro_z = math.degrees(self.sensor.gyro[2])-self.offset
            self.filtered = self.alpha * gyro_z + (1-self.alpha) * self.filtered
            self.angle_z += self.filtered * dt
            old = now
            time.sleep(1/416)

    def start(self):
        self.angle_z = 0.0
        self.offset = self._calibrate()
        self.running = True
        self.threadLoad = threading.Thread(target = self._load, daemon = True)
        self.threadLoad.start()

    def stop(self):
        self.running = False
        self.threadLoad.join()

    def read(self):
        return self.angle_z

def main():
    try:
        gyro = GYRO()
        gyro.start()
        while True:
            print(gyro.read())
    except Exception:
        if gyro is not None:
            gyro.stop()

if __name__ == "__main__":
    main()