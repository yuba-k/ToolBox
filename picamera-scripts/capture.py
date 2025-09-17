from picamera2 import Picamera2
import cv2
import numpy as np
import datetime
import os
import yaml

class Camera():
    def __init__(self):
        try:
            self.picam = Picamera2()
        except Exception as e:
            print("カメラの初期化中にエラーが発生しました")
            raise

    def cap(self,h,w):
        self.picam.configure(self.picam.create_still_configuration(main={"format":"RGB888","size":(w,h)}))
        try:
            self.picam.start()
            im = self.picam.capture_array()
            im = np.flipud(im)
            im = np.fliplr(im)
            self.picam.stop()
            return im
        except Exception as e:
            print("撮影中にエラーが発生")
            return None

    def save(self,im,path,dis):
        # 保存先ディレクトリが存在するか確認、なければ作成
        if not os.path.exists(f"{path}/jpg"):
            os.makedirs(f"{path}/jpg")
        if not os.path.exists(f"{path}/png"):
            os.makedirs(f"{path}/png")

        print("")
        now = datetime.datetime.now()
        cv2.imwrite(f"{path}/jpg/{dis + '_' + now.strftime('%Y%m%d_%H%M%S')}.jpg",im)
        cv2.imwrite(f"{path}/png/{dis + '_' + now.strftime('%Y%m%d_%H%M%S')}.png",im)

    def disconnect(self):
        self.picam.close()

def load_config(config_file):
    try:
        with open(config_file,'r') as f:
            return yaml.safe_load(f)
    except Exception as e:
        print("設定ファイル読み込みエラー:",e)

def main():
    camera = Camera()
    config = load_config("config.yaml")
    while True:
        dis = input("距離：")+"m"

        for v in config["pic_size"]:
            path = fr"{config['save_path'][0]}{v[0]}x{v[1]}"
            img = camera.cap(w=int(v[0]),h=int(v[1]))
            camera.save(img,path,dis)
        ans = input("続けて撮影しますか?<Y ro N>")
        if ans == "y" or ans == "Y":
            input("写真を撮ります")
        else:
            camera.disconnect()
            print("終了")
            break

if __name__ == "__main__":
    main()