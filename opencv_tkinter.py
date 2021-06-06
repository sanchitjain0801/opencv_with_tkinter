from tkinter import *
from PIL import Image
from PIL import ImageTk
from tkinter import filedialog
import cv2
import numpy as np
import scipy.ndimage


def download(cartoon, sketch, baw):
    path = filedialog.askdirectory()
    if len(path) > 0:
        cartoon_path = path + '/cartoon.jpg'
        cv2.imwrite(cartoon_path, cartoon)
        sketch_path = path + '/sketch.jpg'
        cv2.imwrite(sketch_path, sketch)
        baw_path = path + '/vintage.jpg'
        cv2.imwrite(baw_path, baw)

    return


def rgb2gray(rgb):
    return np.dot(rgb[..., :3], [0.3, 0.6, .1])


def dodge(front, back):
    final_sketch = front*255/(255-back)
    final_sketch[final_sketch > 255] = 255
    final_sketch[back == 255] = 255
    return final_sketch.astype('uint8')


def select_image():
    global panelA, panelB, panelC, panelD, download_btn
    path = filedialog.askopenfilename()
    print(path)
    if len(path) > 0:
        image_real = cv2.imread(path)
        gray = rgb2gray(image_real)
        i = 255-gray
        blur = scipy.ndimage.filters.gaussian_filter(i, sigma=20)
        sketch_real = dodge(blur, gray)
        sketch = cv2.resize(sketch_real, (300, 300))
        g = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
        ret, thresh = cv2.threshold(g, 125, 200, cv2.THRESH_BINARY)
        baw_real = thresh
        baw = cv2.resize(baw_real, (300, 300))
        blur = cv2.GaussianBlur(image_real, (5, 5), cv2.BORDER_DEFAULT)
        canny = cv2.Canny(blur, 100, 10)
        cartoonImage_real = cv2.dilate(canny, (7, 7), iterations=3)
        cartoonImage = cv2.resize(cartoonImage_real, (300, 300))
        image = cv2.cvtColor(image_real, cv2.COLOR_BGR2RGB)
        image = cv2.resize(image, (300, 300))
        image = Image.fromarray(image)
        sketch = Image.fromarray(sketch)
        baw = Image.fromarray(baw)
        cartoonImage = Image.fromarray(cartoonImage)
        image = ImageTk.PhotoImage(image)
        baw = ImageTk.PhotoImage(baw)
        sketch = ImageTk.PhotoImage(sketch)
        cartoonImage = ImageTk.PhotoImage(cartoonImage)
        if panelA is None or panelB is None or panelC is None or panelD is None:
            panelA = Label(image=image)
            panelA.image = image
            panelA.pack(side="left", padx=10, pady=10)
            panelB = Label(image=sketch)
            panelB.image = sketch
            panelB.pack(side="right", padx=10, pady=10)
            panelC = Label(image=baw)
            panelC.image = baw
            panelC.pack(side="right", padx=10, pady=10)
            panelD = Label(image=cartoonImage)
            panelD.image = cartoonImage
            panelD.pack(side="left", padx=10, pady=10)
            btn = Button(root, text="Download", command=lambda: download(
                cartoonImage_real, sketch_real, baw_real))
            btn.pack(side="bottom", fill="both",
                     padx="10", pady="10")
        else:
            panelA.configure(image=image)
            panelA.image = image
            panelB.configure(image=sketch)
            panelB.image = sketch
            panelC.configure(image=baw)
            panelC.image = baw
            panelD.configure(image=cartoonImage)
            panelD.image = cartoonImage
            btn = Button(root, text="Download", command=lambda: download(
                cartoonImage_real, sketch_real, baw_real))
            btn.pack(side="bottom", fill="both",
                     padx="10", pady="10")


root = Tk()
panelA = None
panelB = None
panelC = None
panelD = None
download_btn = None
btn = Button(root, text="Select an image", command=select_image)
btn.pack(side="top", fill="both", padx="10", pady="10")

root.mainloop()
