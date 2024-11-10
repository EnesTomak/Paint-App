import sys
from PyQt5.QtWidgets import QApplication
from mainwindow import MainWindow
from mywidget import MyWidget

if __name__ == "__main__":
    # The main application
    app = QApplication(sys.argv)

    # Create and open the main window
    window = MainWindow()
    window.show()

    my_widget = MyWidget()
    my_widget.show()

    # Display the main window
    sys.exit(app.exec_())
