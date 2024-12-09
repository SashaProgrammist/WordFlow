# This Python file uses the following encoding: utf-8
import sys

from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox
from PySide6.QtCore import Slot, QTimer

# Important:
# You need to run the following command to generate the ui_form.py file
#     pyside6-uic form.ui -o ui_form.py, or
#     pyside2-uic form.ui -o ui_form.py
from ui_form import Ui_MainWindow

from WordSeed import WordSeed
from FlowControl import FlowControl
from LangChoicePopupWindow import LangChoicePopupWindow

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.buttonApdateDB.clicked.connect(self.abdateDB)
        self.ui.buttonChoiceLeng.clicked.connect(self.open_popup)
        self.ui.buttonContinue.clicked.connect(self.mainProcess)

        self.timer = QTimer(self)
        # self.timer.

        self.wordSead = WordSeed("data/test.db")
        self.flowControl = FlowControl("data/test.db")

        self.curLeng = None
        self.curPhrase = None
        self.curTrans = None

    @Slot()
    def abdateDB(self):
        wb_patch = QFileDialog.getOpenFileName()[0]
        self.wordSead.apdate(wb_patch)

    @Slot()
    def open_popup(self):
        popup = LangChoicePopupWindow(self.flowControl.getAllLanguages(), self)
        if popup.exec():
            self.curLeng = popup.selected_language

    @Slot()
    def mainProcess(self):
        if self.curLeng is None:
            QMessageBox.warning(self, "Warning", "Please select a language!")
            return

        self.curPhrase = self.flowControl.getAnyPhrase(self.curLeng)

        self.ui.labelOriginalText.setText(self.curPhrase["phrase"])

        self.curTrans = self.flowControl.getAnyTranslate(self.curLeng, self.curPhrase["phrase_set_id"])

        self.ui.labelTranslationText.setText(self.curTrans["phrase"])


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = MainWindow()
    widget.show()
    sys.exit(app.exec())
