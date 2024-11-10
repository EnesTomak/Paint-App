from PyQt5.QtWidgets import QMainWindow, QFileDialog, QColorDialog, QInputDialog, QMessageBox, QAction, QMenu, qApp
from PyQt5.QtCore import QPoint
from drawingarea import DrawingArea

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.drawingArea = DrawingArea()
        self.setCentralWidget(self.drawingArea)

        self.createActions()
        self.createMenus()

        self.setWindowTitle("Draw")
        self.resize(500, 500)

    def closeEvent(self, event):
        if self.maybeSave():
            event.accept()
        else:
            event.ignore()

    def open(self):
        if self.maybeSave():
            file_name, _ = QFileDialog.getOpenFileName(self, "Open File", "", "Image Files (*.png *.jpg *.bmp)")
            if file_name:
                self.drawingArea.openImage(file_name)

    def save(self):
        action = self.sender()
        file_format = action.data()
        self.saveFile(file_format)

    def penColor(self):
        new_color = QColorDialog.getColor(self.drawingArea.penColor(), self, "Select Pen Color")
        if new_color.isValid():
            self.drawingArea.setPenColor(new_color)

    def penWidth(self):
        new_width, ok = QInputDialog.getInt(self, "Draw", "Select pen width:", self.drawingArea.penWidth(), 1, 30, 1)
        if ok:
            self.drawingArea.setPenWidth(new_width)

    def createActions(self):
        self.openAct = QAction("&Open...", self)
        self.openAct.triggered.connect(self.open)

        self.saveDuplicateAct = []
        for format in ['png', 'jpg', 'bmp']:
            text = f"{format.upper()}..."
            action = QAction(text, self)
            action.setData(format)
            action.triggered.connect(self.save)
            self.saveDuplicateAct.append(action)

        self.exitAct = QAction("E&xit", self)
        self.exitAct.triggered.connect(qApp.quit)

        self.penColorAct = QAction("&Pen Color...", self)
        self.penColorAct.triggered.connect(self.penColor)

        self.penWidthAct = QAction("Pen &Width...", self)
        self.penWidthAct.triggered.connect(self.penWidth)

        self.clearScreenAct = QAction("&Clear Screen", self)
        self.clearScreenAct.triggered.connect(self.drawingArea.clearImage)

    def createMenus(self):
        self.saveDuplicateMenu = QMenu("&Save Duplicate", self)
        for action in self.saveDuplicateAct:
            self.saveDuplicateMenu.addAction(action)

        self.fileMenu = QMenu("&File", self)
        self.fileMenu.addAction(self.openAct)
        self.fileMenu.addMenu(self.saveDuplicateMenu)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.exitAct)

        self.optionMenu = QMenu("&Options", self)
        self.optionMenu.addAction(self.penColorAct)
        self.optionMenu.addAction(self.penWidthAct)
        self.optionMenu.addSeparator()
        self.optionMenu.addAction(self.clearScreenAct)

        # Add text feature to the options menu
        addTextAction = QAction("Add Text", self)
        addTextAction.triggered.connect(self.addText)
        self.optionMenu.addAction(addTextAction)

        self.menuBar().addMenu(self.fileMenu)
        self.menuBar().addMenu(self.optionMenu)

    def addText(self):
        text, ok = QInputDialog.getText(self, "Add Text", "Text:")
        if ok and text:
            x, okX = QInputDialog.getInt(self, "X Coordinate:", "X Coordinate:", 0, -1000, 1000)
            y, okY = QInputDialog.getInt(self, "Y Coordinate:", "Y Coordinate:", 0, -1000, 1000)
            if okX and okY:
                self.drawingArea.drawText(text, QPoint(x, y))

    def maybeSave(self):
        if self.drawingArea.isChanged():
            ret = QMessageBox.warning(self, "Draw",
                                      "Changes have been made to the drawing.\n"
                                      "Would you like to save the changes?",
                                      QMessageBox.Save | QMessageBox.Ignore | QMessageBox.Cancel)
            if ret == QMessageBox.Save:
                return self.saveFile("png")
            elif ret == QMessageBox.Cancel:
                return False
        return True

    def saveFile(self, file_format):
        initial_path = f"unnamed.{file_format}"
        file_name, _ = QFileDialog.getSaveFileName(self, "Save Duplicate", initial_path, f"Image Files (*.{file_format})")
        if not file_name:
            return False
        else:
            return self.drawingArea.saveImage(file_name, file_format)
