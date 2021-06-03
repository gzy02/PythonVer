import matplotlib.pyplot as plt
import cv2
import numpy as np
from PIC.Pic import myImage
GrayScale = 256
w = [0 for i in range(GrayScale)]
u = [0 for i in range(GrayScale)]
utmp = [0 for i in range(GrayScale)]


class PrefixSum():
    '以下为图像的前缀和列表，用于优化计算复杂度'

    def __init__(self, pic):
        "初始化前缀和列表"
        pixPro = [0 for i in range(GrayScale)]
        self.SumpixPro = [0 for i in range(GrayScale)]
        WpixPro = [0 for i in range(GrayScale)]
        self.SumWpixPro = [0 for i in range(GrayScale)]

        hist = cv2.calcHist([pic], [0], None, [256], [0, 256])

        self.pixCount = list(map(lambda lis: int(lis[0]), hist.tolist()))

        CountSum = sum(self.pixCount)
        self.SumpixPro[0] = pixPro[0] = self.pixCount[0]/CountSum

        for i in range(1, GrayScale):
            pixPro[i] = self.pixCount[i]/CountSum
            WpixPro[i] = i*pixPro[i]
            self.SumpixPro[i] = pixPro[i]+self.SumpixPro[i-1]
            self.SumWpixPro[i] = WpixPro[i]+self.SumWpixPro[i-1]
        # print(self.pixCount)
        # print(pixPro)
        # print(self.SumpixPro)
        # print(WpixPro)
        # print(self.SumWpixPro)

    def fitness(self, thresh):
        "传入一个列表(阈值)，返回一个浮点数(方差)"
        thresh.sort()  # 升序
        deltatep = 0
        cnt = tep = 0
        for i in thresh:
            w[cnt] = self.SumpixPro[i]-self.SumpixPro[tep]
            if cnt == 0:
                w[0] += self.SumpixPro[0]  # 不该减的
            if(w[cnt] == 0):
                return -1
            u[cnt] = (self.SumWpixPro[i]-self.SumWpixPro[tep])/w[cnt]
            tep = i
            cnt += 1

        w[cnt] = 1-self.SumpixPro[tep]
        if(w[cnt] == 0):
            return -1
        u[cnt] = (self.SumWpixPro[GrayScale-1]-self.SumWpixPro[tep])/w[cnt]

        for i in range(cnt+1):
            deltatep += w[i]*pow(u[i]-self.SumWpixPro[GrayScale-1], 2)
        return deltatep


def Main():  # 测试用
    path = "4.jpg"
    savepath = "test.jpg"
    pic = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    blur = cv2.GaussianBlur(pic, (5, 5), 0)
    lis = [122]
    myfitness = PrefixSum(pic)
    print(myfitness.fitness(lis))


if __name__ == "__main__":
    Main()
