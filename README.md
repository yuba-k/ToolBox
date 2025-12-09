# 雑多なプログラム
## 1. picamera-scripts
この中にはPiCamera関連のプログラムを置いています．
ディレクトリ構造は以下の通りです．

    picamera-scripts
        - capture.py
        - capture_pseudo_hdr.py
        - config.yaml

### 1-1. `capture.py`
`capture.py`はRaspberryPiに接続されたPiCameraを用いて任意の画像サイズで画像を取得/保存するものです．

`.jpg`と`.png`で保存します．

使い方
1. config.yamlのpic_sizeに`[width,height]`の配列形式で画像サイズを記述
2. 画像保存先のファイルパスを`config.yaml`のsave_pathに記述
3. `capture.py`を実行

``` 
python3 capture.py
```
4. 指定したファイルパス直下に"/jpg"と"/png"ディレクトリが作成される．その中に，`[weidth]x[height][YYYYmmdd_HHMMSS].[画像フォーマット]`の名前で画像が保存．

**注意**

+ 実行テストはRaspberryPiZERO2W，PiCamera V2.1で行っています 

### 1-2.`capture_pseudo_hdr.py`
`capture_pseudo_hdr.py`はRaspberryPiに接続されたPiCameraを用いて擬似的なHDR画像を撮影するものです．サイズ指定や保存ディレクトリ等の指定は`capture.py`と同様です．<br>
異なる露出を設定することで，OpenCVの関数によって擬似的なHDR画像を生成しています．<br>
~~**2025/11/04段階で未テストです**~~<br>
**2025/11/15段階テスト実施済み**です．動作自体はしますが，通常の画像と同様の出力結果(十分な擬似HDR画像を生成できていない)

## 2. img-processing
### 2-1.`img_bo_opt.py`
ベイズ最適化による色検出HSV範囲最適化システム．
### 2-2.`current_mask.py`
Yolo形式の正解データと画像から，`img_bo_opt.py`利用する正解データを生成するプログラム．

## 3. 6-axis-sensor
### 3-1. `gyro_angle.py`
6軸センサ(lsm6ds33)からのデータを取得し，変化角度[°]を求めるプログラム．lsm6ds33のテスト用途で開発．