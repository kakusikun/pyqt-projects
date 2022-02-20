import os
os.chdir('./Timer')
import sys
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QLCDNumber, QComboBox, QDialog
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QElapsedTimer, QThread, QTimer, Qt


class HintPopUp(QDialog):
    def __init__(self, hint_text, parent) -> None:
        super().__init__(parent, Qt.WindowStaysOnTopHint)
        uic.loadUi('misc/hint.ui', self)
        self.hint_label.setText(hint_text)
        self.setWindowTitle('Hint')


class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('misc/timer.ui', self)
        self._timer = QElapsedTimer()
        self._display_timer = QTimer()
        self._remaining_secs = 0
        self._remaining_repeat = 1
        self._pop_hint = None
        self.init_timer()
        self.init_timer_btn()
        self.init_time_combo()
        self.init_timer_repeat()
        self.init_timer_lcd()

        self.setWindowTitle('Timer')
        self.show()

    def _set_remaining_repeat(self, text):
        self._remaining_repeat = int(text)

    def _enable_repeat_combo(self, checked):
        if not checked:
            self.repeat_combo.setEnabled(False)
        else:
            self.repeat_combo.setEnabled(True)

    def _display_lcd(self):
        if self._timer.hasExpired(self._remaining_secs*1000):
            if self._pop_hint is None:
                self._pop_hint = HintPopUp(self.hint_line.text(), self)
            self._pop_hint.show()
            self.init_timer_lcd()
            self._remaining_repeat -= 1
            if self.forever_radio.isChecked():
                self._timer.start()
            else:
                if self._remaining_repeat == 0:
                    self._display_timer.stop()
                    self._remaining_repeat = int(self.repeat_combo.currentText())
                    self.stop()
                else:
                    self._timer.start()
        else:
            remaining_secs = self._remaining_secs - (self._timer.elapsed() / 1000)
            hour = int(remaining_secs // (60 * 60))
            remaining_secs %= (60 * 60)
            minute = int(remaining_secs // 60)
            remaining_secs %= 60
            second = round(remaining_secs)
            time_str = f'{hour:02}:{minute:02}:{second:02}'
            self.timer_lcd.display(time_str)

    def init_timer(self):
        self._display_timer.timeout.connect(self._display_lcd)

    def init_timer_btn(self):
        self.play_pause_btn.toggled.connect(self.start)
        self.stop_btn.clicked.connect(self.stop)

    def init_timer_lcd(self):
        self.timer_lcd.display('00:00:00')

    def init_time_combo(self):
        for i in range(0, 99):
            self.hour_combo.addItem(str(i))
        for i in range(0, 60):
            self.minute_combo.addItem(str(i))
        for i in range(0, 60):
            self.second_combo.addItem(str(i))

        self.hour_combo.currentTextChanged.connect(self.set_timer_lcd_display)
        self.minute_combo.currentTextChanged.connect(
            self.set_timer_lcd_display)
        self.second_combo.currentTextChanged.connect(
            self.set_timer_lcd_display)

    def init_timer_repeat(self):
        for i in range(1, 100):
            self.repeat_combo.addItem(str(i))
        self.repeat_combo.setCurrentText('1')
        self.repeat_combo.currentTextChanged.connect(self._set_remaining_repeat)

        self.repeat_radio.setChecked(True)
        self.repeat_radio.toggled.connect(self._enable_repeat_combo)

    def set_timer_lcd_display(self):
        hour = int(self.hour_combo.currentText())
        minute = int(self.minute_combo.currentText())
        second = int(self.second_combo.currentText())
        time_str = f'{hour:02}:{minute:02}:{second:02}'
        self.timer_lcd.display(time_str)

    def start(self, checked):
        if not checked:
            self.play_pause_btn.setIcon(QIcon("misc/play-button.png"))
        else:
            hour = int(self.hour_combo.currentText())
            minute = int(self.minute_combo.currentText())
            second = int(self.second_combo.currentText())
            remaining_secs = hour * 60 * 60 + minute * 60 + second
            if remaining_secs > 0:
                self.play_pause_btn.setIcon(QIcon("misc/pause-button.png"))
                self.hour_combo.setEnabled(False)
                self.minute_combo.setEnabled(False)
                self.second_combo.setEnabled(False)
                self.repeat_radio.setEnabled(False)
                self.forever_radio.setEnabled(False)
                self._remaining_secs = remaining_secs
                self._timer.start()
                self._display_timer.start(1000)
            else:
                self.stop()
                
    def stop(self):
        self._display_timer.stop()
        self.hour_combo.setEnabled(True)
        self.minute_combo.setEnabled(True)
        self.second_combo.setEnabled(True)
        self.hour_combo.setCurrentText('0')
        self.minute_combo.setCurrentText('0')
        self.second_combo.setCurrentText('0')

        self.play_pause_btn.setIcon(QIcon("misc/play-button.png"))
        self.play_pause_btn.setChecked(False)

        self.forever_radio.setChecked(False)
        self.repeat_radio.setChecked(False)

        self.forever_radio.setEnabled(True)
        self.repeat_radio.setEnabled(True)


app = QtWidgets.QApplication(sys.argv)
window = Ui()
app.exec_()