from PyQt5 import QtWidgets, QtGui, uic
import PIL as pil
from PIL.ImageQt import ImageQt
import numpy as np
from dialog import ImageFuctionDialog


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi("imageProcessing.ui", self)
        self.setupUi()
        self.buffer = {}
        self.image = None
        
        
    def setupUi(self):
        self.setWindowTitle("Image Processing")
        
        # Menu
        self.menubar = self.findChild(QtWidgets.QMenuBar, "menubar")
        self.menuFile = self.findChild(QtWidgets.QMenu, "menuFile")
        self.menuSynthesis = self.findChild(QtWidgets.QMenu, "menuSynthesis")
        
        # Open action
        self.actionOpen = self.findChild(QtWidgets.QAction, "actionOpen")
        self.actionOpen.triggered.connect(self.openImage)
        
        # Save action
        self.actionSave = self.findChild(QtWidgets.QAction, "actionSave")
        self.actionSave.triggered.connect(self.saveImage)
        
        # Close action
        self.actionClose = self.findChild(QtWidgets.QAction, "actionClose")
        self.actionClose.triggered.connect(self.clearGraphicsView)
        
        # Quit action
        self.actionQuit = self.findChild(QtWidgets.QAction, "actionQuit")
        self.actionQuit.triggered.connect(QtWidgets.QApplication.quit)
        
        # Generate image action
        self.actionGenerateImage = self.findChild(QtWidgets.QAction, "actionGenerateImage")
        self.actionGenerateImage.triggered.connect(self.generateImage)
        
        # Kotelnikov action
        self.actionKotelnikov = self.findChild(QtWidgets.QAction, "actionKotelnikov")
        self.actionKotelnikov.triggered.connect(self.kotelnikov)
        
        # Graphics view
        self.graphicsView = self.findChild(QtWidgets.QGraphicsView, "graphicsView")
        
        
    def openImage(self):
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(
            self, "Select image...", "", "All Files (*)", options=options)
        
        pixmap = QtGui.QPixmap(fileName)
        self._displayPixmap(pixmap)
        
        
    def saveImage(self):
        if self.image is None:
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Information)
            msg.setText("No image to save. You need to either open or generate an image, first.")
            msg.setWindowTitle("Information")
            msg.exec_()
        else:
            fileName, _ = QtWidgets.QFileDialog.getSaveFileName(self, 'Save image')
            print(fileName)
            self.image.save(fileName, "PNG")
        
        
    def clearGraphicsView(self):
        self.graphicsView.setScene(None)
        self.image = None
        
    
    def generateImage(self):
        # u * x**2 + v * y**2
        # np.sqrt(10 * x**2 + 10 * y**2)
        # np.sqrt(0.1 * x**2 - 0.1 * y**2)
        # np.cos(u * x + v * y)
        
        dialog = ImageFuctionDialog(self.buffer)
        values = dialog.exec_()
        if values:
            u, v, f = values
            exec("def wrapper(x, y): return " + f.replace("u", u).replace("v", v), globals())
            self._generateImageFrFunc(wrapper)
            self.buffer["u"] = u
            self.buffer["v"] = v
            self.buffer["f"] = f
            
    
    def kotelnikov(self):
        a = 50
        b = 120
        def u(x, y): return x / 2
        def v(x, y): return 0
        
        def f(x, y):
            return a * np.cos(u(x, y) * x + v(x, y) * y) + b
        
        self._generateImageFrFunc(f)
        
        
    def _displayPixmap(self, pixmap):
        self.image = pixmap
        item = QtWidgets.QGraphicsPixmapItem(pixmap)
        scene = QtWidgets.QGraphicsScene(self)
        scene.addItem(item)
        self.graphicsView.setScene(scene)
        
        
    def _generateImageFrFunc(self, f):
        width = self.frameGeometry().width()
        height = self.frameGeometry().height()
        
        # pixels = np.random.rand(height, width, 3) * 255
        pixels = [[[f(x, y)] * 3 for x in range(width)] for y in range(height)]            
        image = pil.Image.fromarray(np.array(pixels).astype('uint8')).convert("RGB")
        
        pixmap = QtGui.QPixmap.fromImage(ImageQt(image))
        self._displayPixmap(pixmap)
    