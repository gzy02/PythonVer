
from PIC.Pic import myImage
from OTSU.PrefixSum import PrefixSum
path = "4.jpg"
savepath = "test.jpg"


def Main():
    myimg = myImage(path)
    mysum = PrefixSum(myimg.pic)
    print(mysum.fitness([65, 67]))
    '''
    plt.subplot(131)
    plt.imshow(img.pic, cmap='gray')
    plt.subplot(132)
    plt.hist(img.pic.ravel(), 256)
    plt.subplot(133)
    plt.plot(hist, color='red')
    plt.show()

    '''


if __name__ == "__main__":
    Main()
