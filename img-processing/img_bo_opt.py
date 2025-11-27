import os
import cv2
import random
import numpy as np
import optuna
import optuna.samplers as sampler
import logging

logger = logging.getLogger(__name__)

logging.basicConfig(
    filename="img-processing/myapp.log", # 出力したいファイル名
    format="{asctime} [{levelname}] {name}: {message}", # ログのフォーマット
    datefmt="%Y-%m-%d %H:%M:%S", # 日時のフォーマット
    style="{", # formatの変数埋め込みのスタイル 他にも $ や % を使った表記あり
    level=logging.INFO, # 指定したレベル以上のログのみ出力
    encoding="utf-8",
)



def preparation(rawimgpath:str,maskimgpath:str) -> None:
    """_summary_

    Args:
        rawimgpath (str): 画像データ
        maskimgpath (str): 教師データ(マスク画像)
    """
    imgs = []
    names = os.listdir(rawimgpath)
    for name in names:
        imgs.append(cv2.imread(rawimgpath+"/"+name))
    #画像生データの準備
    current = os.getcwd()
    base_dir = os.path.join(current, "img-processing", "datasets")
    
    # ディレクトリ作成
    os.makedirs(os.path.join(base_dir, "raw", "train"), exist_ok=True)
    os.makedirs(os.path.join(base_dir, "raw", "val"), exist_ok=True)
    
    # 生画像データの準備
    for img, name in zip(imgs, names):
        if random.random() < 0.8:
            cv2.imwrite(os.path.join(base_dir, "raw", "train", name), img)
        else:
            # val に修正
            cv2.imwrite(os.path.join(base_dir, "raw", "val", name), img) 
            
    # ... 中略（リストクリア） ...
    
    # マスク画像データの準備
    # ディレクトリ作成
    os.makedirs(os.path.join(base_dir, "mask", "train"), exist_ok=True)
    os.makedirs(os.path.join(base_dir, "mask", "val"), exist_ok=True)
    
    for img, name in zip(imgs, names):
        if random.random() < 0.8:
            cv2.imwrite(os.path.join(base_dir, "mask", "train", name), img)
        else:
            # val に修正
            cv2.imwrite(os.path.join(base_dir, "mask", "val", name), img)

def redmask_noizecut(rawimg:np.ndarray,h1_min:int,h1_max:int,h2_min:int,h2_max:int,s_min:int,s_max:int,v_min:int,v_max:int,it_erode:int,area_thresh:int) -> np.ndarray:
    hsv = cv2.cvtColor(rawimg, cv2.COLOR_BGR2HSV)
    mask1 = cv2.inRange(hsv,(h1_min,s_min,v_min),(h1_max,s_max,v_max))
    mask2 = cv2.inRange(hsv,(h2_min,s_min,v_min),(h2_max,s_max,v_max))
    
    # mask1 = cv2.inRange(hsv,(0,100,100),(10,255,255))
    # mask2 = cv2.inRange(hsv,(170,100,100),(180,255,255))
    
    mask = cv2.bitwise_or(mask1, mask2)
    #cv2.imshow("show",mask);cv2.waitKey(0)
    kernel = np.array([[0,1,0],[1,1,1],[0,1,0]], np.uint8)
    mask = cv2.erode(mask, kernel, iterations=it_erode)
    mask = cv2.dilate(mask, kernel, iterations=it_erode)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_TC89_KCOS)
    if not contours:
        return mask
    contours = [c for c in contours if cv2.contourArea(c) > area_thresh]
    out = np.zeros_like(mask)
    if not contours:
        return mask
    cv2.drawContours(out, [max(contours, key=cv2.contourArea)], -1, 255, -1)
    return out


def calc_tp_fp_fn(gt_mask, pred_mask):
    """
    gt_mask_path  : 正解マスク（0 or 255 の2値画像）
    pred_mask_path: 抽出マスク（HSV → inRange の結果）
    """

    # --- 2. 0/1 に正規化 ---
    gt_bin = (gt_mask > 0).astype(np.uint8)
    pred_bin = (pred_mask > 0).astype(np.uint8)

    # --- 3. ピクセル比較 ---
    TP = np.sum((gt_bin == 1) & (pred_bin == 1))
    FP = np.sum((gt_bin == 0) & (pred_bin == 1))
    FN = np.sum((gt_bin == 1) & (pred_bin == 0))

    return TP, FP, FN

def fitness(trial):
    rawpath = "img-processing/datasets/raw/train/"
    maskpath = "img-processing/datasets/mask/train/"
    rawlist = os.listdir(rawpath)
    masklist = os.listdir(maskpath)
    rawlist.sort()
    masklist.sort()
    rawimgs = []; maskimgs = []
    cnt = 0; fit = 0
    tp, fp, fn = 0,0,0

    it_erode = trial.suggest_int("it_erode",1,4)
    area_thresh = trial.suggest_int("area_thresh",100,3000)
    h1_min = trial.suggest_int("h1_min",0,15)
    h1_max = trial.suggest_int("h1_max",16,30)
    h2_min = trial.suggest_int("h2_min",150,165)
    h2_max = trial.suggest_int("h2_max",166,179)
    s_min = trial.suggest_int("s_min",0,150)
    s_max = trial.suggest_int("s_max",151,255)
    v_min = trial.suggest_int("v_min",0,150)
    v_max = trial.suggest_int("v_max",151,255)

    for r_name, m_name in zip(rawlist, masklist):
        rawimgs.append(cv2.imread(rawpath+r_name))
        maskimgs.append(cv2.imread(maskpath+m_name, cv2.IMREAD_GRAYSCALE))
        cnt += 1
    for img,mask in zip(rawimgs,maskimgs):

        masked = redmask_noizecut(img,h1_min,h1_max,h2_min,h2_max,s_min,s_max,v_min,v_max,it_erode,area_thresh)

        tmp_tp, tmp_fp, tmp_fn = calc_tp_fp_fn(mask,masked)
        tp += tmp_tp
        fp += tmp_fp
        fn += tmp_fn

    recall = tp/(tp+fn)
    precision = tp/(tp+fp+1.0*10**(-10))#NaN回避
    iou = tp/(tp+fp+fn)
    fit = 0.7*recall + 0.2*precision + 0.1*iou
    logger.info(f"tp:{tp}\tfp:{fp}\tfn:{fn}")
    logger.info(f"nrecall:{recall}\tprecision:{precision}\tiou:{iou}")
    logger.info(f"fit:{fit}")
    return fit

if __name__ == "__main__":
    #preparation(rawimgpath="img-processing/currentdatasets/raw",maskimgpath="img-processing/currentdatasets/mask/")
    sample = sampler.CmaEsSampler()
    study = optuna.create_study(direction="maximize",sampler=sample)
    while True:
        study.optimize(fitness,n_trials=50)
        best_value = study.best_value
        print(f"Current Best Value: {best_value:.4f}")
        if best_value > 0.85:
            print("SUCCESFULL!!")
            break

    print("Best Trial:")
    trial = study.best_trial
    print(f"Value:{trial.value}")
    logger.info(f"value:{trial.value}")
    print("Parms:")
    for key, value in trial.params.items():
        print(f"{key}:{value}")
        logger.info(f"{key}:{value}")