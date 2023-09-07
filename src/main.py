import os, sys

# Get the absolute path of the current script file
script_path = os.path.abspath(__file__)

# Get the root directory by going up one level from the script directory
project_root = os.path.dirname(os.path.dirname(script_path))

sys.path.insert(0, project_root)
sys.path.insert(0, os.getcwd())  # Add the current directory as well


from PyQt5.QtCore import QThread, QCoreApplication
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QMainWindow, QApplication

from chatWidget import *
from script import run_suggestion

QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
QCoreApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)  # HighDPI support

QApplication.setFont(QFont('Arial', 12))


class Thread(QThread):
    afterGenerated = pyqtSignal(str, bool)

    def __init__(self, query):
        super(Thread, self).__init__()
        self.__query = query

    def run(self):
        try:
            self.__response = run_suggestion(self.__query)
            self.afterGenerated.emit(self.__response, False)
        except Exception as e:
            raise Exception(e)


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.__initUi()

    def __initUi(self):
        self.setWindowTitle('Intellisense')

        self.__browser = ChatBrowser()
        prompt = Prompt()
        self.__lineEdit = prompt.getTextEdit()
        self.__lineEdit.returnPressed.connect(self.__generateResponse)
        self.__lineEdit.setPlaceholderText('Write some text...')

        lay = QVBoxLayout()
        lay.addWidget(self.__browser)
        lay.addWidget(prompt)
        lay.setAlignment(Qt.AlignTop)

        mainWidget = QWidget()
        mainWidget.setLayout(lay)

        self.setCentralWidget(mainWidget)

    def __generateResponse(self):
        query = self.__lineEdit.toPlainText()

        self.__lineEdit.setEnabled(False)
        question = self.__lineEdit.toPlainText().strip()
        self.__browser.showText(question, True)

        self.__t = Thread(query)
        self.__t.started.connect(self.__started)
        self.__t.afterGenerated.connect(self.__browser.showText)
        self.__t.finished.connect(self.__finished)
        self.__t.start()

    def __afterGenerated(self, response):
        print(response)

    def __started(self):
        print('started')

    def __finished(self):
        print('finished')
        self.__lineEdit.setEnabled(True)


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec())