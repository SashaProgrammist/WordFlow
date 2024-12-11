# This Python file uses the following encoding: utf-8
import sys
from math import sin, pi

from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox, QSlider
from PySide6.QtCore import Slot, QTimer

# Important:
# You need to run the following command to generate the ui_form.py file
#     pyside6-uic form.ui -o ui_form.py, or
#     pyside2-uic form.ui -o ui_form.py
from ui_form import Ui_MainWindow

from WordSeed import WordSeed
from FlowControl import FlowControl
from LangChoicePopupWindow import LangChoicePopupWindow

STANDARD_DELAY = 1000

class ConvertSliderValue:
    def __init__(self, slider: QSlider, amplitude: float):
        self.slider = slider
        self.amplitude = amplitude

    def transform(self, value):
        value = 1 - (
              (value - self.slider.minimum())
            / (self.slider.maximum() - self.slider.minimum()))

        value = (value
            - (1 - 1 / self.amplitude) / (self.amplitude - 1 / self.amplitude)
            * sin(pi * value))

        value = value * (self.amplitude - 1 / self.amplitude) + 1 / self.amplitude

        return value * STANDARD_DELAY


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.buttonApdateDB.clicked.connect(self.abdateDB)
        self.ui.buttonChoiceLeng.clicked.connect(self.open_popup)
        self.ui.buttonContinue.clicked.connect(self.mainProcess)
        self.ui.speedSlider.valueChanged.connect(self.cangeSpeed)

        self.timerDisplay = QTimer(self)
        self.timerDisplay.timeout.connect(self.gradualDisplay)
        self.timerBreforeShow = QTimer(self)
        self.timerBreforeShow.timeout.connect(self.breforeShow)


        self.wordSead = WordSeed("data/test.db")
        self.flowControl = FlowControl("data/test.db")
        self.convertSliderValue = ConvertSliderValue(self.ui.speedSlider, 3)

        self.curLeng = None
        self.curPhrase = None
        self.curTrans = None
        self.speedDisplay = STANDARD_DELAY

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

        if self.timerDisplay.isActive() or self.timerBreforeShow.isActive():
            return

        self.curPhrase = self.flowControl.getAnyPhrase(self.curLeng)

        self.ui.labelOriginalText.setText(self.curPhrase["phrase"])

        self.curTrans = self.flowControl.getAnyTranslate(self.curLeng, self.curPhrase["phrase_set_id"])

        self.curTrans["phrase"] = list(self.curTrans["phrase"].split())[::-1]

        self.ui.labelTranslationText.setText("")

        self.timerBreforeShow.start(2000)

    @Slot()
    def gradualDisplay(self):
        if self.curTrans is None or not self.curTrans["phrase"]:
            self.timerDisplay.stop()
            return

        text_new = (self.ui.labelTranslationText.text()
                    + " " + self.curTrans["phrase"][-1])

        self.ui.labelTranslationText.setText(text_new)

        self.curTrans["phrase"].pop()

    @Slot(int)
    def cangeSpeed(self, sliderValue):
        self.speedDisplay = self.convertSliderValue.transform(sliderValue)

        if self.timerDisplay.isActive():
            self.timerDisplay.setInterval(self.speedDisplay)

    @Slot()
    def breforeShow(self):
        self.timerBreforeShow.stop()
        self.timerDisplay.start(self.speedDisplay)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = MainWindow()
    widget.show()
    sys.exit(app.exec())
