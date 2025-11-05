from picamera2 import Picamera2
from libcamera import controls
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

    def capture_pseudo_hdr_image(self,h,w,mode):
        if mode == 0:
            self.picam.set_controls({"AeExposureMode":controls.AeExposureModeEnum.Short})
        elif mode == 1:
            self.picam.set_controls({"AeExposureMode":controls.AeExposureModeEnum.Normal})
        else:
            self.picam.set_controls({"AeExposureMode":controls.AeExposureModeEnum.Long})
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
        for i, img in enumerate(im):
            if i == 0:
                cv2.imwrite(f"{path}/jpg/{dis + '_short_' + now.strftime('%Y%m%d_%H%M%S')}.jpg",img)
                cv2.imwrite(f"{path}/png/{dis + '_short_' + now.strftime('%Y%m%d_%H%M%S')}.png",img)
            elif i == 1:
                cv2.imwrite(f"{path}/jpg/{dis + '_normal_' + now.strftime('%Y%m%d_%H%M%S')}.jpg",img)
                cv2.imwrite(f"{path}/png/{dis + '_normal_' + now.strftime('%Y%m%d_%H%M%S')}.png",img)
            elif i == 2:
                cv2.imwrite(f"{path}/jpg/{dis + '_long_' + now.strftime('%Y%m%d_%H%M%S')}.jpg",img)
                cv2.imwrite(f"{path}/png/{dis + '_long_' + now.strftime('%Y%m%d_%H%M%S')}.png",img)
            else:
                cv2.imwrite(f"{path}/jpg/{dis + '_hsv_' + now.strftime('%Y%m%d_%H%M%S')}.jpg",img)
                cv2.imwrite(f"{path}/png/{dis + '_hsv_' + now.strftime('%Y%m%d_%H%M%S')}.png",img)

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
    img_list = []
    merge_mertens = cv2.createMergeMertens()
    while True:
        dis = input("距離：")+"m"

        for v in config["pic_size"]:
            img_list.clear()#画像リストの開放
            path = fr"{config['save_path'][0]}{v[0]}x{v[1]}"
            #PiCameraの設定
            camera.picam.configure(camera.picam.create_still_configuration(main={"format":"RGB888","size":(int(v[0]),int(v[1]))}))
            for i in range(3):
                img = camera.capture_pseudo_hdr_image(w = int(v[0]), h = int(v[1]), mode = i)
                img_list.append(img)
            # Mertensを用いて露光を統合
            res_mertens = merge_mertens.process(img_list)
            img_list.append(np.clip(res_mertens*255, 0, 255).astype('uint8'))
            camera.save(img_list,path,dis)
        ans = input("続けて撮影しますか?<Y ro N>")
        if ans == "y" or ans == "Y":
            input("写真を撮ります")
        else:
            camera.disconnect()
            print("終了")
            break

if __name__ == "__main__":
    main()
