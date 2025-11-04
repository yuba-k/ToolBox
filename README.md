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
**2025/11/04段階で未テストです**