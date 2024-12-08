from PySide6.QtWidgets import QDialog
from ui_langChoicePopup import Ui_Form


class LangChoicePopupWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)

