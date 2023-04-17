# ライブラリのインポート
import matplotlib.pyplot as plt
import cv2

# import numpy as np
# import pandas as pd
# from google.colab.patches import cv2_imshow

img_path = "data/data004mst.png"

img_psc = cv2.imread(img_path, 1)
img_psc2 = cv2.imread(img_path, 1)
img_psg = cv2.imread(img_path, 0)
img_psa = cv2.imread(img_path, -1)

temp, img_bin = cv2.threshold(img_psg, 240, 255, cv2.THRESH_BINARY)
contours, hierarchy = cv2.findContours(
    img_bin, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE
)  # img_binaryを輪郭抽出
cv2.drawContours(
    img_psc, contours, -1, (0, 0, 255), 1
)  # 抽出した輪郭をcount+=len(contours)赤色でimg_colorに重ね書き

print(len(contours))
img_psc = cv2.cvtColor(img_psc, cv2.COLOR_BGR2RGB)
# cv2.imwrite('data/004mst_msk_c.png',img_psc)
plt.imshow(img_psc)
plt.show()

# x,y,w,h = cv2.boundingRect(img_psg)
# cv2.rectangle(img_psc2,(x,y),(x+w-1,y+h-1),(0,255,0),1)
# img_psc2 = cv2.cvtColor(img_psc2, cv2.COLOR_BGR2RGB)
# plt.imshow(img_psc2)
# plt.show()


# img_alpha = img_psa[:,:,3]
# img_alpha = cv2.cvtColor(img_alpha, cv2.COLOR_BGR2RGB)
# cv2.imwrite('004mst_msk.png',img_alpha)
# plt.imshow(img_alpha)
# plt.show()
