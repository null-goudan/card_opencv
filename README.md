# card_opencv

## 识别银行卡卡号 （opencv的基本图像处理+模板匹配）

### 一些过程 ：

模板预处理

![屏幕截图 2022-01-11 145519](https://user-images.githubusercontent.com/74131166/148895472-6ec4b3f7-6a1a-4262-ad6d-1bde2595385c.png)

轮廓检测
![image](https://user-images.githubusercontent.com/74131166/148895500-30829b51-97b5-49bc-ac70-2300efd10038.png)

目标图像的缩小和灰度处理
![image](https://user-images.githubusercontent.com/74131166/148895579-65de12bd-fbd6-458b-bb7d-8e2f3ee8919d.png)

二值化
![image](https://user-images.githubusercontent.com/74131166/148895609-3d72c8b9-2b5b-46fe-9870-b5f153241f1a.png)

礼帽处理和闭运算处理
![image](https://user-images.githubusercontent.com/74131166/148895648-c9d017e1-f5c4-4852-a7a3-d34a69d73de2.png)
![image](https://user-images.githubusercontent.com/74131166/148895651-ad921e51-ce0a-4b97-9a41-2f5c3b1d26d8.png)

获得想要的区域 感兴趣区（roi）
![image](https://user-images.githubusercontent.com/74131166/148895709-7cc46ca3-d790-4997-8003-fe07a449ae23.png)
![image](https://user-images.githubusercontent.com/74131166/148895722-4b566d95-f115-4949-9214-c54bd389158c.png)
![image](https://user-images.githubusercontent.com/74131166/148895732-f544c002-c032-4c84-a476-efdc8bf3e6b1.png)
![image](https://user-images.githubusercontent.com/74131166/148895744-e049eb66-87d6-4ef1-9b3e-df4fdf134c2c.png)

### 结果
![image](https://user-images.githubusercontent.com/74131166/148895774-e3c18151-3624-49dc-b6fe-b2e56154ea97.png)
