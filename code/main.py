from PIC.Pic import myImage
#from OTSU import fitness


def Main():
    path = "1.png"
    savepath = "2.png"
    pic = myImage(path)
    pic.ShowPic("window1")
    pic.SavePic(savepath)


if __name__ == "__main__":
    Main()
