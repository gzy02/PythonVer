import cv2


class myImage():
    "预处理图片"

    def __init__(self, path):
        "输入参数为字符串，表示打开路径+文件名"
        self.pic = cv2.imread(path, cv2.IMREAD_GRAYSCALE)

    def ShowPic(self, windowname):
        "输入参数为字符串，表示打开的窗口名"
        cv2.imshow(windowname, self.pic)
        print("光标移到图像处按任意键退出")
        # 等待键盘输入，单位为毫秒，即等待指定的毫秒数看是否有键盘输入，若在等待时间内按下任意键则返回按键的ASCII码，程序继续运行。
        cv2.waitKey(0)
        # 若没有按下任何键，超时后返回-1。参数为0表示无限等待。不调用waitKey的话，窗口会一闪而逝，看不到显示的图片。

    def SavePic(self, path):
        "输入参数为字符串，表示保存路径+文件名"
        cv2.imwrite(path, self.pic)
