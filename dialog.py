from PyQt5 import QtWidgets, uic


class ImageFuctionDialog(QtWidgets.QDialog):
    def __init__(self, params=None):
        super(ImageFuctionDialog, self).__init__()            
        uic.loadUi("imageFuctionDialog.ui", self)
        
        
        if params:
            self.params = params
        else:
            self.params = {}
            
        self.setupUi()
        
        
    def setupUi(self):
        self.setWindowTitle("Input image function")
        
        # Input fields
        self.uInput = self.findChild(QtWidgets.QLineEdit, "uInput")
        self.vInput = self.findChild(QtWidgets.QLineEdit, "vInput")
        self.fInput = self.findChild(QtWidgets.QLineEdit, "fInput")
        
        if "u" in self.params:
            self.uInput.setText(self.params["u"])
        if "v" in self.params:
            self.vInput.setText(self.params["v"])
        if "f" in self.params:
            self.fInput.setText(self.params["f"])
        
        
    def exec_(self):
        res = super(ImageFuctionDialog, self).exec_()
        if res:
            res = self.uInput.text(), self.vInput.text(), self.fInput.text()
        return res
    