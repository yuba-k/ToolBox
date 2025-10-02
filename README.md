# 雑多なプログラム
## 1. picamera-scripts
この中にはPiCamera関連のプログラムを置いています．
ディレクトリ構造は以下の通りです．

    picamera-scripts
        -capture.py
        -config.yaml

### 1-1. capture.py
capture.pyはRaspberryPiに接続されたPiCameraを用いて任意の画像サイズで画像を取得/保存するものです．

`.jpg`と`.png`で保存します．

使い方
1. config.yamlのpic_sizeに`[width,height]`の配列形式で画像サイズを記述
2. 画像保存先のファイルパスをconfig.yamlのsave_pathに記述
3. capture.pyを実行

``` 
python3 capture.py
```
4. 指定したファイルパス直下に"/jpg"と"/png"ディレクトリが作成される．その中に，`[weidth]x[height][YYYYmmdd_HHMMSS].[画像フォーマット]`の名前で画像が保存．

**注意**

+ 実行テストはRaspberryPiZERO2W，PiCamera V2.1で行っています 