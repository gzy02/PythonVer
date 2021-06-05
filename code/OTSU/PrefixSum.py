import cv2
import copy
import numpy as np
import ctypes as C
GrayScale = 256
w = [0 for i in range(GrayScale)]
u = [0 for i in range(GrayScale)]

maxthre = 0
maxlist = []


def dfs(Sum, curlist, depth, cnt=0):
    if depth == 0:
        global maxthre, maxlist
        tep = Sum.fitness(curlist)
        if tep > maxthre:
            maxlist = copy.deepcopy(curlist)
            maxthre = tep
        return

    for i in range(cnt, GrayScale):
        curlist[depth-1] = i
        dfs(Sum, curlist, depth-1, i+1)


class PrefixSum():
    '以下为图像的前缀和列表，用于优化计算复杂度'
    '''
    成员：
        pixCount
        SumpixPro
        SumWpixPro
    '''

    def __init__(self, pic):
        "初始化前缀和列表"
        self.img = pic
        pixPro = [0 for i in range(GrayScale)]
        self.SumpixPro = [0 for i in range(GrayScale)]
        WpixPro = [0 for i in range(GrayScale)]
        self.SumWpixPro = [0 for i in range(GrayScale)]

        hist = cv2.calcHist([pic], [0], None, [256], [0, 256])
        self.pixCount = list(map(lambda lis: int(lis[0]), hist.tolist()))

        #(rows, cols) = (pic.shape[0], pic.shape[1])
        # CountSum=rows*cols
        CountSum = sum(self.pixCount)
        self.SumpixPro[0] = pixPro[0] = self.pixCount[0]/CountSum

        for i in range(1, GrayScale):
            pixPro[i] = self.pixCount[i]/CountSum
            WpixPro[i] = i*pixPro[i]
            self.SumpixPro[i] = pixPro[i]+self.SumpixPro[i-1]
            self.SumWpixPro[i] = WpixPro[i]+self.SumWpixPro[i-1]
        # print(self.pixCount)
        # print(self.SumpixPro)
        # print(self.SumWpixPro)

    def fitness(self, threshinit):
        "传入一个列表(阈值)，返回一个浮点数(方差)"
        thresh = copy.deepcopy(threshinit)
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
        # print(w)
        # print(u)
        for i in range(cnt+1):
            deltatep += w[i]*pow(u[i]-self.SumWpixPro[GrayScale-1], 2)
        return deltatep

    def OtsuSolve(self, thnum):
        "标准Otsu算法求解，传参为阈值个数,返回值为列表"
        global maxthre, maxlist
        maxthre = 0
        maxlist = []
        curlist = [0 for i in range(thnum)]
        dfs(self, curlist, thnum)
        return maxlist

    def CppOtsuSolve(self, N):
        dll = C.cdll.LoadLibrary("DLL_OPEN_CV.dll")
        # 声明一个数组类型
        INPUT = C.c_int * N
        # 实例化一个长度为N的整型数组
        input = INPUT()
        # 引用C语言的函数

        (rows, cols) = (self.img.shape[0], self.img.shape[1])

        ret_img = np.zeros(dtype=np.uint8, shape=(rows, cols, 1))
        dll.otsu_open_cv_dll(rows, cols, self.img.ctypes.data_as(
            C.POINTER(C.c_ubyte)), ret_img.ctypes.data_as(C.POINTER(C.c_ubyte)), input, N)
        return list(input), ret_img
        #cv2.imshow("ret", ret_img)
        # cv2.waitKey(0)

    def CppGASolve(self, N):
        dll = C.cdll.LoadLibrary("DLL_OPEN_CV.dll")
        # 声明一个数组类型
        INPUT = C.c_int * N
        # 实例化一个长度为N的整型数组
        input = INPUT()
        # 引用C语言的函数

        (rows, cols) = (self.img.shape[0], self.img.shape[1])

        ret_img = np.zeros(dtype=np.uint8, shape=(rows, cols, 1))
        dll.ga_open_cv_dll(rows, cols, self.img.ctypes.data_as(
            C.POINTER(C.c_ubyte)), ret_img.ctypes.data_as(C.POINTER(C.c_ubyte)), input, N)
        lis = list(input)
        lis.sort(reverse=True)
        return lis, ret_img
        #cv2.imshow("ret", ret_img)
        # cv2.waitKey(0)


def Main():  # 测试用
    path = "../4.jpg"
    savepath = "../test.jpg"
    pic = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    blur = cv2.GaussianBlur(pic, (5, 5), 0)
    lis = [122]
    myfitness = PrefixSum(pic)
    print(myfitness.fitness(lis))


if __name__ == "__main__":
    Main()
