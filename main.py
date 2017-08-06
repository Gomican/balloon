# -*- coding: utf-8 -*-
import cv2
cv2.__version__
import numpy as np



#親画像の閾値
HIGHER_COLOR = 195
LOWER_COLOR  = 110


#親画像の切り取り範囲
X_START = 175
Y_START = 185

X_END = 375
Y_END = 370


#サンプル画像の使用範囲
X_S = 150
Y_S = 150

X_E = 400
Y_E = 400

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
    tmp_origin = origin
    tmp_sample = sample

    ## 画像の切り取り ##
    origin = origin[Y_START:Y_END, X_START:X_END]
    sample = sample[Y_S:Y_E, X_S:X_E]

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

    ## 評価範囲の設定 ##
    origin_height,origin_width,channels = Get_ImgSize(origin_edge)
    sample_height,sample_width,channels = Get_ImgSize(sample_edge)

    sample_height = sample_height - origin_height
    sample_width  = sample_width  - origin_width


    ## 親画像を元にして一番距離の近い特徴点を求める ##
    point = [0]*2
    least = 0
    h = 0
    w = 0
    while h < sample_height:
        w = 0
        while w < sample_width:
            length = [0]*len(origin_keypoints)
            for i in range(0,len(origin_keypoints)):
                origin_keypoint = origin_keypoints[i]
                for j in range(0,len(sample_keypoints)):
                    sample_keypoint = sample_keypoints[j]
                    # 距離を求める
                    a = np.array([origin_keypoint.pt[0],origin_keypoint.pt[1]])
                    b = np.array([h,w])
                    u = b-a
                    l = np.linalg.norm(u)
                    if ((j == 0) or (l < length[i])):
                        length[i] = l
                    else:
                        length[i] = length[i]
            ave = np.average(length)
            if ((least > ave) or ((h==0) and (w==0))):
                point[0] = w
                point[1] = h
                least = ave
            w = w + 30
        h = h + 30

    ########### 親画像をサンプル画像から引く ###########
    ## 親画像の精度誤差を打ち消すために膨張処理を施す ##
    kernel = np.ones((5,5),np.uint8)
    dilation_origin = cv2.dilate(tmp_origin,kernel,iterations = 1)
    dilation_origin = cv2.dilate(dilation_origin,kernel,iterations = 1)

    for i in range(point[0],X_END):
        for j in range(point[1],Y_END):
            if (dilation_origin[i][j] != 0):
                tmp_sample[i][j] = 0


    cv2.circle(sample,(point[0],point[1]),10,(255,0,0),-1)

    sample_keypoints = Get_Keypoints(tmp_sample)
    #out = cv2.drawKeypoints(tmp_sample, sample_keypoints, None)
    fout = open("sample_point.txt","w")
    heder = open("heder.txt","w")

    for i in range(0,len(sample_keypoints)):
        sample_keypoint = sample_keypoints[i]

        fout.writelines(str(int(sample_keypoint.pt[0])) + " ")
        fout.writelines(str(int(sample_keypoint.pt[1])) + "\n")

    heder.writelines(str(len(sample_keypoints))+" ")
    heder.writelines(str(point[0]) + " ")
    heder.writelines(str(point[1]))

    heder.close()
    fout.close()
    #cv2.imshow("DIFF", out)
    #cv2.imshow("SAMPLE", sample)

    cv2.waitKey(0)
    cv2.destroyAllWindows()
## __endOfMain__ ##
