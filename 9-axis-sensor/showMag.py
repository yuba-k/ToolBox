import serial
import time
import math

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

ser = serial.Serial(
    port="com8",
    baudrate=115200,
    timeout=1
)

fig, ax = plt.subplots(figsize=(5,5))
ax.set_aspect('equal', adjustable='box')


mag_x = []
mag_y = []
offset_x, offset_y = 0, 0

scatter = ax.scatter([],[])

def parse(line):
    parts = line.split(",")
    x = int(parts[0].split(":")[1])
    y = int(parts[1].split(":")[1])
    return x, y

def update(frm):
    line = ser.readline().decode("utf-8",errors="ignore").strip()
    if line.startswith("x:") and "," in line:
        try:
            x, y = parse(line)
            print(math.degrees(math.atan2(y,x)))
            mag_x.append(x-offset_x)
            mag_y.append(y-offset_y)


            # 座標データ更新
            scatter.set_offsets(list(zip(mag_x, mag_y)))

            x_min = min(mag_x)
            x_max = max(mag_x)

            y_min = min(mag_y)
            y_max = max(mag_y)

            x_center = (x_max + x_min) / 2
            y_center = (y_max + y_min) / 2

            radius = max(
                (x_max - x_min) / 2,
                (y_max - y_min) / 2
            )

            margin = 100

            ax.set_xlim(
                x_center - radius - margin,
                x_center + radius + margin
            )

            ax.set_ylim(
                y_center - radius - margin,
                y_center + radius + margin
            )

        except KeyboardInterrupt as e:
            print(e)
    return []

def calibrate():
    global offset_x, offset_y
    print("キャリブレーション開始")
    time.sleep(5)
    x_sum, y_sum = [], []
    for i in range(100):
        line = ser.readline().decode("utf-8",errors="ignore").strip()
        if line.startswith("x:") and "," in line:
            x, y = parse(line)
            x_sum.append(x)
            y_sum.append(y)
        time.sleep(0.1)
    offset_x = (max(x_sum)+min(x_sum))/2
    offset_y = (max(y_sum)+min(y_sum))/2

calibrate()

ani = FuncAnimation(
    fig,
    update,
    interval=100,
    cache_frame_data=False
)

plt.show()

ser.close()