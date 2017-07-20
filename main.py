# -*- coding: utf-8 -*-
import cv2
import numpy as np


#親画像の閾値
HIGHER_COLOR = 195
LOWER_COLOR  = 110


################ 画像のサイズを取得する関数(カラー,グレー対応) ################
## 引数 　　- img 画像ファイル
## 戻り値   - height,width,channels
def Get_ImgSize(img):
    if len(img.shape) == 3:
        height, width, channels = img.shape[:3]
    else:
        height, width = img.shape[:2]
        channels = 1
    return height,width,channels
## ___endOfFunction___ ##



################特定の範囲の色を抽出する関数(gray scale)################
## 引数    - img:画像ファイル
## 戻り値  - 特定の色以外除去された画像データ
def Get_AnyColor(img):
    # 画像サイズの取得
    height,width,channels = Get_ImgSize(img)

    # 特定色以外の除去
    for h in range(0,height):
        for w in range(0,width):
            if img[h,w] > HIGHER_COLOR:
                img[h,w] = 0
            elif img[h,w] < LOWER_COLOR:
                img[h,w] = 0
            else:
                img[h,w] = img[h,w]

    return img
## ___endOfFunction___ ##



################輪郭を抽出する関数################
## 引数   - img:画像ファイル
## 戻り値 - 輪郭抽出された画像データ
def Get_OutLine(img):
    img_tmp = cv2.Laplacian(img, cv2.CV_32F, 8)
    img_lap = cv2.convertScaleAbs(img_tmp)

    return img_lap
## ___endOfFunction___ ##



################ノイズを除去する関数################
## 引数   - img:画像ファイル
##      　  neiborhood  :4または8近傍の選択
##                       4 - neiborhood4
##                       8 - neiborhood8
## 戻り値 - ノイズ除去された画像データ

# 4近傍の定義
neiborhood4 = np.array([[0, 1, 0],
                        [1, 1, 1],
                        [0, 1, 0]],
                        np.uint8)

# 8近傍の定義
neiborhood8 = np.array([[1, 1, 1],
                        [1, 1, 1],
                        [1, 1, 1]],
                        np.uint8)

def Remove_Noise(img, neiborhood):
    ##オープニング
    img_dst = cv2.morphologyEx(img, cv2.MORPH_OPEN, neiborhood)
    ##クロージング
    img_dst = cv2.morphologyEx(img_dst, cv2.MORPH_CLOSE, neiborhood)

    return img_dst
## ___endOfFunction___ ##


################特徴点抽出する関数################
## 引数   - img       :画像データ
## 戻り値 - keypoints :特徴量
# pt	ポイント（x, y）
# size	特徴点の直径
# angle	[0, 360) の範囲の角度。y軸が下方向で右回り。計算不能な場合は-1。
# response	特徴点の強度
# octave	特徴点を検出したピラミッドレイヤー
# class_id	特徴点が属するクラスのID
def Get_Keypoints(img):
    detector = cv2.ORB_create()
    keypoints = detector.detect(img)
    return keypoints
## ___endOfFunction___ ##



if __name__ == '__main__':

    # 画像の読み込み
    origin = cv2.imread("origin.jpg", 0)
    sample = cv2.imread("output_disp2.png",0)

    ## 親画像の任意の色抽出 ##
    origin = Get_AnyColor(origin)

    ## 比較画像と親画像のノイズ除去 ##
    origin_clean   = Remove_Noise(origin, neiborhood8)
    sample_clean   = Remove_Noise(sample, neiborhood8)

    ## 比較画像と親画像の輪郭抽出 ##
    origin_edge = Get_OutLine(origin_clean)
    sample_edge = Get_OutLine(sample_clean)

    ## 比較画像と親画像の特徴量抽出 ##
    origin_keypoints = Get_Keypoints(origin_edge)
    sample_keypoints = Get_Keypoints(sample_edge)

    # 表示

    origin = cv2.drawKeypoints(origin, origin_keypoints, None)
    sample = cv2.drawKeypoints(sample, sample_keypoints, None)

    cv2.imshow("ORIGIN", origin)
    cv2.imshow("SAMPLE", sample)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
## __endOfMain__ ##
