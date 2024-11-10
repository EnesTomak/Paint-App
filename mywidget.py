import sys
import math
from PyQt5.QtWidgets import QApplication, QWidget, QMenuBar, QVBoxLayout, QAction, QColorDialog, QMessageBox, QMenu
from PyQt5.QtGui import QPainter, QPolygonF, QIcon, QColor
from PyQt5.QtCore import Qt, QPointF

class MyWidget(QWidget):
    class Shape:
        NoneShape, Line, Circle, Triangle, Rectangle, Ellipse, Hexagon, Star = range(8)

    def __init__(self, parent=None):
        super(MyWidget, self).__init__(parent)
        self.drawing = False
        self.shape = MyWidget.Shape.NoneShape
        self.shapeFillColors = {}

        # Shape icon paths
        self.shapeIcons = {
            MyWidget.Shape.Line: QIcon(":/icons/line_icon.ico"),
            MyWidget.Shape.Circle: QIcon(":/icons/circle_icon.ico"),
            MyWidget.Shape.Triangle: QIcon(":/icons/triangle_icon.ico"),
            MyWidget.Shape.Rectangle: QIcon(":/icons/rectangle_icon.ico"),
            MyWidget.Shape.Ellipse: QIcon(":/icons/ellipse_icon.ico"),
            MyWidget.Shape.Hexagon: QIcon(":/icons/hexagon_icon.ico"),
            MyWidget.Shape.Star: QIcon(":/icons/star_icon.ico")
        }

        self.shapeMenu = QMenu("Shapes", self)

        # Create actions for each shape
        self.createAction("Line", self.shapeIcons[MyWidget.Shape.Line], self.setShapeToLine)
        self.createAction("Circle", self.shapeIcons[MyWidget.Shape.Circle], self.setShapeToCircle)
        self.createAction("Triangle", self.shapeIcons[MyWidget.Shape.Triangle], self.setShapeToTriangle)
        self.createAction("Rectangle", self.shapeIcons[MyWidget.Shape.Rectangle], self.setShapeToRectangle)
        self.createAction("Ellipse", self.shapeIcons[MyWidget.Shape.Ellipse], self.setShapeToEllipse)
        self.createAction("Hexagon", self.shapeIcons[MyWidget.Shape.Hexagon], self.setShapeToHexagon)
        self.createAction("Star", self.shapeIcons[MyWidget.Shape.Star], self.setShapeToStar)

        operationMenu = QMenu("Operation", self)
        chooseIcon = QIcon(":/icons/choose_icon.ico")
        deleteIcon = QIcon(":/icons/delete_icon.ico")

        chooseAction = QAction(chooseIcon, "Choose", self)
        chooseAction.triggered.connect(self.handleOption1)
        operationMenu.addAction(chooseAction)

        deleteAction = QAction(deleteIcon, "Delete", self)
        deleteAction.triggered.connect(self.handleOption2)
        operationMenu.addAction(deleteAction)

        self.shapeMenu.addMenu(operationMenu)

        # Menu bar
        menuBar = QMenuBar(self)
        menuBar.addMenu(self.shapeMenu)

        layout = QVBoxLayout(self)
        layout.setMenuBar(menuBar)
        self.setLayout(layout)

    def createAction(self, name, icon, handler):
        action = QAction(icon, name, self)
        action.triggered.connect(handler)
        self.shapeMenu.addAction(action)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.startPoint = event.pos()
            self.drawing = True

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton and self.drawing:
            self.endPoint = event.pos()
            self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        if self.drawing and self.shape != MyWidget.Shape.NoneShape:
            fillColor = self.shapeFillColors.get(self.shape, QColor())
            painter.setBrush(fillColor)

            if self.shape == MyWidget.Shape.Line:
                painter.drawLine(self.startPoint, self.endPoint)
            elif self.shape == MyWidget.Shape.Circle:
                radius = int(math.sqrt((self.endPoint.x() - self.startPoint.x()) ** 2 +
                                       (self.endPoint.y() - self.startPoint.y()) ** 2))
                painter.drawEllipse(self.startPoint, radius, radius)
            elif self.shape == MyWidget.Shape.Triangle:
                 self.drawTriangle(painter)
            elif self.shape == MyWidget.Shape.Rectangle:
                painter.drawRect(self.startPoint.x(), self.startPoint.y(), self.endPoint.x() - self.startPoint.x(),
                                 self.endPoint.y() - self.startPoint.y())
            elif self.shape == MyWidget.Shape.Ellipse:
                painter.drawEllipse(self.startPoint.x(), self.startPoint.y(), self.endPoint.x() - self.startPoint.x(),
                                    self.endPoint.y() - self.startPoint.y())
            elif self.shape == MyWidget.Shape.Hexagon:
                 self.drawHexagon(painter)
            elif self.shape == MyWidget.Shape.Star:
                 self.drawStar(painter)

    def drawTriangle(self, painter):
        # Draw an equilateral triangle
        sideLength = max(abs(self.endPoint.x() - self.startPoint.x()), abs(self.endPoint.y() - self.startPoint.y()))
        height = math.sqrt(3) / 2 * sideLength
        p1 = QPointF(self.startPoint.x(), self.startPoint.y() - height)
        p2 = QPointF(self.startPoint.x() - sideLength / 2, self.startPoint.y() + height / 2)
        p3 = QPointF(self.startPoint.x() + sideLength / 2, self.startPoint.y() + height / 2)
        triangle = QPolygonF([p1, p2, p3])
        painter.drawPolygon(triangle)

    def drawHexagon(self, painter):
        # Draw a hexagon
        angle = 2 * math.pi / 6
        radius = min(abs(self.endPoint.x() - self.startPoint.x()), abs(self.endPoint.y() - self.startPoint.y()))
        hexagon = QPolygonF()
        for i in range(6):
            currentAngle = i * angle
            x = self.startPoint.x() + radius * math.cos(currentAngle)
            y = self.startPoint.y() + radius * math.sin(currentAngle)
            hexagon << QPointF(x, y)
        painter.drawPolygon(hexagon)

    def drawStar(self, painter):
        # Draw a star with 5 points
        angle = 2 * math.pi / 5
        outerRadius = min(abs(self.endPoint.x() - self.startPoint.x()), abs(self.endPoint.y() - self.startPoint.y()))
        innerRadius = outerRadius / 2
        starPolygon = QPolygonF()
        for i in range(5):
            currentAngle = i * angle - math.pi / 2
            xOuter = self.startPoint.x() + outerRadius * math.cos(currentAngle)
            yOuter = self.startPoint.y() + outerRadius * math.sin(currentAngle)
            xInner = self.startPoint.x() + innerRadius * math.cos(currentAngle + angle / 2)
            yInner = self.startPoint.y() + innerRadius * math.sin(currentAngle + angle / 2)
            starPolygon << QPointF(xOuter, yOuter) << QPointF(xInner, yInner)
        painter.drawPolygon(starPolygon)

    def setShapeToRectangle(self):
        self.shape = MyWidget.Shape.Rectangle
        self.update()

    def setShapeToEllipse(self):
        self.shape = MyWidget.Shape.Ellipse
        self.update()

    def setShapeToLine(self):
        self.shape = MyWidget.Shape.Line
        self.update()

    def setShapeToCircle(self):
        self.shape = MyWidget.Shape.Circle
        self.update()

    def setShapeToTriangle(self):
        self.shape = MyWidget.Shape.Triangle
        self.update()

    def setShapeToHexagon(self):
        self.shape = MyWidget.Shape.Hexagon
        self.update()

    def setShapeToStar(self):
        self.shape = MyWidget.Shape.Star
        self.update()

    def shapeToString(self, shape):
        shape_names = {
            MyWidget.Shape.Line: "Line",
            MyWidget.Shape.Circle: "Circle",
            MyWidget.Shape.Triangle: "Triangle",
            MyWidget.Shape.Rectangle: "Rectangle",
            MyWidget.Shape.Ellipse: "Ellipse",
            MyWidget.Shape.Hexagon: "Hexagon",
            MyWidget.Shape.Star: "Star"
        }
        return shape_names.get(shape, "None")

    def handleOption1(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.shapeFillColors[self.shape] = color
            self.update()
        else:
            QMessageBox.information(self, "Fill Color Change Canceled", "Fill color change canceled")

    def handleOption2(self):
        if self.shape != MyWidget.Shape.NoneShape:
            self.shape = MyWidget.Shape.NoneShape
            QMessageBox.information(self, "Shape Deleted", "Selected shape has been deleted.")
            self.update()
        else:
            QMessageBox.information(self, "No Shape Selected", "No shape selected to delete.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = MyWidget()
    widget.show()
    sys.exit(app.exec_())