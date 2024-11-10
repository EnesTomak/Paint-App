from PyQt5.QtCore import Qt, QRect, QSize, QPoint
from PyQt5.QtGui import QPainter, QImage, QPen, QColor, QMouseEvent, QPaintEvent
from PyQt5.QtWidgets import QWidget

class DrawingArea(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_StaticContents)
        self.changed = False
        self.drawing = False
        self.myPWidth = 1
        self.myPColor = Qt.black
        self.image = QImage(640, 480, QImage.Format_RGB32)  # Initialize with default size
        self.image.fill(Qt.white)
        self.lastPoint = QPoint()

    def drawText(self, text, position):
        painter = QPainter(self.image)
        painter.setPen(QPen(self.myPColor, self.myPWidth, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
        painter.drawText(position, text)
        self.changed = True
        self.update()

    def openImage(self, fileName):
        loadedImage = QImage(fileName)
        if loadedImage.isNull():
            return False

        newSize = loadedImage.size().expandedTo(self.size())
        self.resizeImage(loadedImage, newSize)
        self.image = loadedImage
        self.changed = False
        self.update()
        return True

    def saveImage(self, fileName, fileFormat):
        visibleImage = self.image
        self.resizeImage(visibleImage, self.size())
        if visibleImage.save(fileName, fileFormat):
            self.changed = False
            return True
        else:
            return False

    def setPenColor(self, newColor):
        self.myPColor = newColor

    def setPenWidth(self, newWidth):
        self.myPWidth = newWidth

    def clearImage(self):
        self.image.fill(Qt.white)
        self.changed = True
        self.update()

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self.lastPoint = event.pos()
            self.drawing = True

    def mouseMoveEvent(self, event: QMouseEvent):
        if event.buttons() & Qt.LeftButton and self.drawing:
            self.drawLine(event.pos())

    def mouseReleaseEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton and self.drawing:
            self.drawLine(event.pos())
            self.drawing = False

    def paintEvent(self, event: QPaintEvent):
        painter = QPainter(self)
        nastyRect = event.rect()
        painter.drawImage(nastyRect, self.image, nastyRect)

    def resizeEvent(self, event):
        if self.width() > self.image.width() or self.height() > self.image.height():
            newWidth = max(self.width(), self.image.width() + 128)
            newHeight = max(self.height(), self.image.height() + 128)
            self.resizeImage(self.image, QSize(newWidth, newHeight))
            self.update()
        super().resizeEvent(event)

    def drawLine(self, endPoint):
        try:
            if self.image.isNull():
                return
            painter = QPainter(self.image)
            painter.setPen(QPen(self.myPColor, self.myPWidth, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
            painter.drawLine(self.lastPoint, endPoint)
            self.changed = True
            rad = int((self.myPWidth / 2) + 2)  # Ensure rad is an integer
            self.update(QRect(self.lastPoint, endPoint).normalized().adjusted(-rad, -rad, rad, rad))
            self.lastPoint = endPoint
        except Exception as e:
            print(f"An error occurred: {e}")

    def resizeImage(self, image, newSize):
        if image.size() == newSize:
            return
        newImage = QImage(newSize, QImage.Format_RGB32)
        newImage.fill(Qt.white)
        painter = QPainter(newImage)
        painter.drawImage(QPoint(0, 0), image)
        image.swap(newImage)

    def penColor(self):
        return self.myPColor

    def penWidth(self):
        return self.myPWidth

    def isChanged(self):
        return self.changed
