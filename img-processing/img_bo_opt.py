import os
import cv2
import random
import numpy as np
import optuna

def preparation(rawimgpath:str,maskimgpath:str) -> None:
    """_summary_

    Args:
        rawimgpath (str): 画像データ
        maskimgpath (str): 教師データ(マスク画像)
    """
    imgs = []
    names = os.listdir(rawimgpath)
    for name in names:
        imgs.append(cv2.imread(rawimgpath+name))
    #画像生データの準備
    current = os.getcwd()
    os.mkdir(current+"datasets/raw/train")
    os.mkdir(current+"datasets/raw/val")
    for img,name in zip(imgs,names):
        if random.random() < 0.8:
            cv2.imwrite(current+"datasets/raw/train/"+name,img)
        else:
            cv2.imwrite(current+"datasets/raw/va/"+name,img)
    imgs.clear()
    names.clear()
    #マスク画像データの準備
    names = os.listdir(maskimgpath)
    for name in names:
        imgs.append(cv2.imread(maskimgpath+name))
    os.mkdir(current+"datasets/mask/train/")
    os.mkdir(current+"datasets/mask/val/")
    for img,name in zip(imgs,names):
        if random.random() < 0.8:
            cv2.imwrite(current+"datasets/mask/train/"+name,img)
        else:
            cv2.imwrite(current+"datasets/mask/va/"+name,img)

def redmask_noizecut(rawimg:np.ndarray,h_min:int,h_max:int,s_min:int,s_max:int,v_min:int,v_max:int) -> np.ndarray:
    hsv = cv2.cvtColor(cv2.COLOR_BGR2HSV,rawimg)
    mask = cv2.inRange(hsv,(h_min,s_min,v_min),(h_max,s_max,v_max))

    kernel = np.array([[0,1,0],[1,1,1],[0,1,0]], np.uint8)
    mask = cv2.erode(mask, kernel, iterations=3)
    mask = cv2.dilate(mask, kernel, iterations=3)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_TC89_KCOS)
    if not contours:
        return mask
    contours = [c for c in contours if cv2.contourArea(c) > 1000]
    out = np.zeros_like(mask)
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
    rawpath = "./datasets/raw/train/"
    maskpath = "./datasets/mask/train"
    rawlist = os.listdir(rawpath)
    masklist = os.listdir(maskpath)
    rawimgs = []; maskimgs = []
    cnt = 0; fit = 0

    h_min = trial.suggest_int("h_min",0.179)
    h_max = trial.suggest_int("h_max",0,179)
    s_min = trial.suggest_int("s_min",0,255)
    s_max = trial.suggest_int("s_max",0,255)
    v_min = trial.suggest_int("v_min",0,255)
    v_max = trial.suggest_int("v_max",0,255)

    for r_name, m_name in zip(rawlist, masklist):
        rawimgs.append(cv2.imread(rawpath+r_name))
        maskimgs.append(cv2.imread(maskpath+m_name))
        cnt += 1

    for img,mask in zip(rawimgs,maskimgs):
        masked = redmask_noizecut(img,h_min,h_max,s_min,s_max,v_min,v_max)
        tp, fp, fn = calc_tp_fp_fn(mask,masked)
        recall = tp/(tp+fn)
        precision = tp/(tp+fp)
        iou = tp/(tp+fp+fn)
        fit += 0.7*recall + 0.2*precision + 0.1*iou
    return fit/cnt

if __name__ == "__main__":
    study = optuna.create_study(direction="maximize")
    study.optimize(fitness,n_trials=100)

    print("Best Trial:")
    trial = study.best_trial
    print(f"Value:{trial.value}")
    print("Parms:")
    for key, value in trial.params.items():
        print(f"{key}:{value}")