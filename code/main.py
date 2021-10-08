import time
import myImage
import OTSU
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from matplotlib import cm
import cv2

path = "3.jpg"
savepath = "test.jpg"


def Main():
    myimg = myImage.myImage(path)
    # print(type(myimg.pic))
    mysum = OTSU.PrefixSum(myimg.pic)

    print("fitness函数测试")
    print("[120, 121]对应的方差为", mysum.fitness([120, 121]))
    print("[165, 88]对应的方差为", mysum.fitness([165, 88]))
    '''
    num = int(input("请输入阈值个数:"))
    print("DLL测试")
    time_start = time.time()
    print("Python OTSU:", mysum.OtsuSolve(num))
    time_end = time.time()
    print('totally cost:%fs' % (time_end - time_start))
    print("C++ OTSU:", mysum.CppOtsuSolve(num)[0])
    time_end2 = time.time()
    print('totally cost:%fs' % (time_end2 - time_end))
    print("C++ GA:", mysum.CppGASolve(num)[0])
    time_end3 = time.time()
    print('totally cost:%fs' % (time_end3 - time_end2))
    cv2.imshow("ret", mysum.CppGASolve(num)[1])
    cv2.imwrite(savepath, mysum.CppGASolve(num)[1])
    cv2.waitKey(0)
    # 绘图
    plt.subplot(131)
    plt.imshow(myimg.pic, cmap='gray')
    plt.title("Original picture")
    plt.subplot(132)
    plt.hist(myimg.pic.flatten(), 256, [0, 256])
    plt.title("Gray histogram")
    if num == 1:
        oneth = []
        for i in range(256):
            k = [i]
            oneth.append(mysum.fitness(k))
        # print(oneth)
        plt.subplot(133)
        plt.plot(range(256), oneth)
        plt.title("Variance\n(threshold=1)")
    if num == 2:
        fig = plt.figure()
        ax = Axes3D(fig)
        ax.set_xlim(0, 255)
        ax.set_ylim(0, 255)
        X, Y = np.arange(0, 256, 1), np.arange(0, 256, 1)
        X, Y = np.meshgrid(X, Y)
        Z = np.zeros((256, 256))
        for i in range(256):
            for j in range(256):
                Z[i][j] = mysum.fitness([X[i][j], Y[i][j]])
        ax.plot_surface(X, Y, Z, rstride=5, cstride=5, cmap=cm.rainbow)
        plt.title("Variance\n(threshold=2)")
    plt.subplots_adjust(wspace=0.6, hspace=0.6)  # 调整各子绘图区的间隔
    plt.show()
    '''


if __name__ == "__main__":
    Main()
