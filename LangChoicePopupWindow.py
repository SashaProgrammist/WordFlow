from PySide6.QtWidgets import QDialog, QMessageBox
from ui_langChoicePopup import Ui_Form


class LangChoicePopupWindow(QDialog):
    def __init__(self, languages, parent=None):
        super().__init__(parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        # Заполняем список языков
        self.languages = languages
        self.ui.languageListWidget.addItems(self.languages)

        # Подключаем кнопку OK
        self.ui.buttonEnd.clicked.connect(self.confirm_selection)

        # Выбранный язык (по умолчанию None)
        self.selected_language = None

    def confirm_selection(self):
        selected_items = self.ui.languageListWidget.selectedItems()
        if selected_items:
            self.selected_language = selected_items[0].text()
            self.accept()  # Закрываем окно с подтверждением
        else:
            QMessageBox.warning(self, "Warning", "Please select a language!")  # Предупреждение, если ничего не выбрано

