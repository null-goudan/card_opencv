import cv2
import numpy as np


# 展示图片
def img_show(name, img):
    cv2.imshow(name, img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


# 轮廓排序
def contours_sort(cnts, method):
    reverse = False
    if method == 'right-to-left':
        reverse = True
    # 得到轮廓的矩形 然后 进行x坐标排序就行了
    boundingBoxes = [cv2.boundingRect(c) for c in cnts]
    (cnts, boundingBoxes) = zip(*sorted(zip(cnts, boundingBoxes),
                                        key=lambda b: b[1][0], reverse=reverse))
    return cnts, boundingBoxes


# 模板预处理
img_tem = cv2.imread('tem.png')
# img_show('template', img_tem)

ref_tem = cv2.cvtColor(img_tem, cv2.COLOR_BGR2GRAY)
# img_show('ref_tem', ref_tem)

ref_tem = cv2.threshold(ref_tem, 10, 255, cv2.THRESH_BINARY_INV)[1]
# img_show('ref_tem', ref_tem)

refCnts, hierarchy = cv2.findContours(ref_tem.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

cv2.drawContours(img_tem, refCnts, -1, (0, 0, 255), 3)
# img_show('img_cnt', img_tem)

# print(np.array(refCnts).shape)
refCnts = contours_sort(refCnts, method='left-to-right')[0]
# 构造字典拿出每个数字的模板
digits = {}

for (i, c) in enumerate(refCnts):
    x, y, w, h = cv2.boundingRect(c)
    roi = ref_tem[y:y+h, x:x+w]
    # 每个轮廓大小不一样，匹配是要求大小完全一样的，所以resize一下
    roi = cv2.resize(roi, (57, 88))
    # 每个数字对应一个模板
    digits[i] = roi
# 模板做好了

# 对目标图像进行处理 要进行处理干扰项

# 初始化卷积核
rectKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (9, 3))
sqKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (9, 9))

# 读入输入图像
img_pos = cv2.imread('pos.png')
# img_show('img_pos', img_pos)
img_pos_small = cv2.resize(img_pos, (300, 180))

img_pos_gray = cv2.cvtColor(img_pos, cv2.COLOR_BGR2GRAY)
img_pos_gray = cv2.resize(img_pos_gray, (300, 180))
# img_show('gray',img_pos_gray)

# 一个礼帽操作 拿出比较明亮的地方
tophat = cv2.morphologyEx(img_pos_gray, cv2.MORPH_TOPHAT, rectKernel)
# img_show('tophat', tophat)

# sobel 算子 拿到 x轴的梯度信息(越大越是边缘，也就是明亮)
gradx = cv2.Sobel(tophat, ddepth=cv2.CV_32F, dx=1, dy=0, ksize=-1) # 3*3的sobel算子
# 归一化
gradx = np.absolute(gradx)
(minVal, maxVal) = (np.min(gradx), np.max(gradx))
gradx = (255 * (gradx - minVal) / (maxVal - minVal))
gradx = gradx.astype('uint8')

# img_show('gradx', gradx)

# 可以看到边缘信息出来了，但是我们要过滤比较小的字体和比较大的字体
# 那么闭运算（先膨胀再腐蚀），让边缘都连在一起, 得到合适的明亮区域就行了

gradx =cv2.morphologyEx(gradx, cv2.MORPH_CLOSE, sqKernel)
# img_show('gradx', gradx)

thresh = cv2.threshold(gradx, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]  # 双峰二值化
# img_show('thresh', thresh)

# 但是还是有镂空部分 那么继续闭运算
thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, sqKernel)
# img_show('thresh', thresh)

# 计算轮廓并画出
threshCnts, hierarchy = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

cnts = threshCnts
cur_img = img_pos_small.copy()
cv2.drawContours(cur_img, cnts, -1, (0, 255, 0), 3)
# img_show('img_cur', cur_img)

locs = []

for (i, c) in enumerate(cnts):
    (x, y, w, h) = cv2.boundingRect(c)
    ar = w/float(h)

    if ar > 3.5 and ar < 5.0:
        if (w > 40 and w < 55) and (h>10 and h < 20):
            locs.append((x, y, w, h))


locs = sorted(locs, key=lambda x:x[0])
output = []

for (i, (gx, gy, gw, gh)) in enumerate(locs):
    groupOutPut = []

    group = img_pos_gray[gy-5:gy + gh + 5, gx-5:gx+gw+5]
    # img_show('group', group)
    group = cv2.threshold(group, 0, 255, cv2.THRESH_BINARY|cv2.THRESH_OTSU)[1]
    # img_show('group_threshould', group)

    digitsCnts, hierarchy = cv2.findContours(group.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    digitsCnts = contours_sort(digitsCnts, method='left-to-right')[0]

    for c in digitsCnts:
        (x, y, w, h) = cv2.boundingRect(c)
        roi = group[y:y+h, x:x+w]
        roi = cv2.resize(roi, (57, 88))
        # img_show('roi', roi)

        scores = []
        for (digit, digitROI) in digits.items():
            # img_show('tem_smll', digitROI)
            result = cv2.matchTemplate(roi, digitROI, cv2.TM_CCOEFF)
            _, score, _, _ = cv2.minMaxLoc(result)
            print(score)
            scores.append(score)

        groupOutPut.append(str(np.argmax(scores)))
        # print(groupOutPut)
        cv2.rectangle(img_pos_small, (gx-5, gy-5), (gx+gw+5, gy+gh+5), (0, 0, 255), 1)
        cv2.putText(img_pos_small, "".join(groupOutPut), (gx, gy-15),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.65, (0, 0, 255), 2)

        output.extend(groupOutPut)

print("Credit Card #: {}".format("".join(output)))

img_show("result", img_pos_small)

