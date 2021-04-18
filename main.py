from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QFileDialog, QListWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PIL import Image, ImageFilter
import os

app = QApplication([])
win = QWidget()
win.setWindowTitle('Easy Editor')
win.resize(700, 500)

list1 = QListWidget()
btn_dir = QPushButton("Папка")
lb_image = QLabel("Картинка")
btn_left = QPushButton('Лево')
btn_right = QPushButton('Право')
btn_mirror = QPushButton('Зеркало')
btn_sharpness = QPushButton('Резкость')
btn_bw = QPushButton('Ч/Б')

row = QHBoxLayout()
col1 = QVBoxLayout()
col2 = QHBoxLayout()
row_tools = QVBoxLayout()

col1.addWidget(btn_dir)
col1.addWidget(list1)
col2.addWidget(btn_left)
col2.addWidget(btn_right)
col2.addWidget(btn_mirror)
col2.addWidget(btn_sharpness)
col2.addWidget(btn_bw)
row_tools.addWidget(lb_image)
row_tools.addLayout(col2)

row.addLayout(col1)
row.addLayout(row_tools)

win.setLayout(row)
win.show()
workdir = ''
def filter(files, extensions):
    result = []
    for files in files:
        for extension in extensions:
            if files.endswith(extension):
                result.append(files)
    return result

def chooseWorkdir():
    global workdir
    workdir = QFileDialog.getExistingDirectory()

def showFilenamesList():
    extensions = ['.jpg', '.png', '.jpeg', '.bmp']
    chooseWorkdir()
    filenames = filter(os.listdir(workdir), extensions)
    list1.clear()
    for filename in filenames:
        list1.addItem(filename)

btn_dir.clicked.connect(showFilenamesList)
class ImageProcessor():
    def __init__(self):
        self.image = None
        self.diry = None
        self.filename = None
        self.save_dir = "Modified/"

    def loadImage(self, diry, filename):
        self.diry = diry
        self.filename = filename
        image_path = os.path.join(diry, filename)
        self.image = Image.open(image_path)

    def do_bw(self):
        self.image = self.image.convert("L")
        self.saveImage()
        image_path = os.path.join(self.diry, self.save_dir, self.filename)
        self.showImage(image_path)

    def do_flip(self):
        self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
        self.saveImage()
        image_path = os.path.join(self.diry, self.save_dir, self.filename)
        self.showImage(image_path)
    
    def do_right(self):
        self.image = self.image.transpose(Image.ROTATE_90)
        self.saveImage()
        image_path = os.path.join(self.diry, self.save_dir, self.filename)
        self.showImage(image_path)

    def do_left(self):
        self.image = self.image.transpose(Image.ROTATE_270)
        self.saveImage()
        image_path = os.path.join(self.diry, self.save_dir, self.filename)
        self.showImage(image_path)
    
    def do_sharp(self):
        self.image = self.image.filter(ImageFilter.SHARPEN)
        self.saveImage()
        image_path = os.path.join(self.diry, self.save_dir, self.filename)
        self.showImage(image_path)

    def saveImage(self):
        path = os.path.join(self.diry, self.save_dir)
        if not(os.path.exists(path) or os.path.isdir(path)):
            os.mkdir(path)
        image_path = os.path.join(path, self.filename)
        self.image.save(image_path)

    def showImage(self, path):
        lb_image.hide()
        pixmapimage = QPixmap(path)
        w, h = lb_image.width(), lb_image.height()
        pixmapimage = pixmapimage.scaled(w, h, Qt.KeepAspectRatio)
        lb_image.setPixmap(pixmapimage)
        lb_image.show()

def showChosenImage():
    if list1.currentRow() >= 0:
        filename = list1.currentItem().text()
        workimage.loadImage(workdir, filename)
        workimage.showImage(os.path.join(workdir, workimage.filename))
workimage = ImageProcessor()
list1.currentRowChanged.connect(showChosenImage)

btn_bw.clicked.connect(workimage.do_bw)
btn_mirror.clicked.connect(workimage.do_flip)
btn_left.clicked.connect(workimage.do_left)
btn_right.clicked.connect(workimage.do_right)
btn_sharpness.clicked.connect(workimage.do_sharp)

app.exec()