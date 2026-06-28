"""
settings_dialog.py
------------------
A small preferences dialog (reachable from the tray "Settings..." item) that
edits the persisted settings. It only collects values; main.py applies and
saves them so the live widget, hotkeys, and startup entry all update together.
"""

from PySide6.QtCore import Qt
from PySide6.QtGui import QColor
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QFormLayout, QCheckBox, QSlider, QPushButton,
    QLabel, QColorDialog, QDialogButtonBox, QSpinBox,
)

import settings


class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Tidal Widget - Settings")
        self.setMinimumWidth(340)
        cur = settings.current()
        self._accent = str(cur["accent"])

        form = QFormLayout()

        self.accent_btn = QPushButton()
        self.accent_btn.setCursor(Qt.PointingHandCursor)
        self.accent_btn.clicked.connect(self._pick_accent)
        self._style_accent_btn()
        form.addRow("Accent color", self.accent_btn)

        self.bg = QSlider(Qt.Horizontal)
        self.bg.setRange(30, 100)
        self.bg.setValue(int(round(float(cur["background_opacity"]) * 100)))
        form.addRow("Panel opacity", self.bg)

        self.win = QSlider(Qt.Horizontal)
        self.win.setRange(40, 100)
        self.win.setValue(int(round(float(cur["window_opacity"]) * 100)))
        form.addRow("Whole-widget opacity", self.win)

        self.poll = QSpinBox()
        self.poll.setRange(200, 2000)
        self.poll.setSingleStep(100)
        self.poll.setSuffix(" ms")
        self.poll.setValue(int(cur["poll_ms"]))
        form.addRow("Refresh interval", self.poll)

        self.aot = QCheckBox("Always on top")
        self.aot.setChecked(bool(cur["always_on_top"]))
        self.startexp = QCheckBox("Start expanded")
        self.startexp.setChecked(bool(cur["start_expanded"]))
        self.fallback = QCheckBox("Follow other apps when TIDAL isn't playing")
        self.fallback.setChecked(bool(cur["fallback_any"]))
        self.startup = QCheckBox("Run at Windows startup")
        self.startup.setChecked(settings.is_run_at_startup())
        self.hotkeys = QCheckBox("Global hotkeys")
        self.hotkeys.setChecked(bool(cur["hotkeys_enabled"]))

        col = QVBoxLayout(self)
        col.addLayout(form)
        for c in (self.aot, self.startexp, self.fallback, self.startup, self.hotkeys):
            col.addWidget(c)

        hint = QLabel(
            "Hotkeys: Ctrl+Alt+Space play/pause, Ctrl+Alt+Left/Right prev/next,\n"
            "Ctrl+Alt+L like, Ctrl+Alt+H show/hide.\n"
            "Refresh interval and 'start expanded' take effect on next launch.")
        hint.setStyleSheet("color:#9a9aa3; font-size:11px;")
        col.addWidget(hint)

        bb = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        bb.accepted.connect(self.accept)
        bb.rejected.connect(self.reject)
        col.addWidget(bb)

    def _pick_accent(self):
        c = QColorDialog.getColor(QColor(self._accent), self, "Accent color")
        if c.isValid():
            self._accent = c.name()
            self._style_accent_btn()

    def _style_accent_btn(self):
        self.accent_btn.setText(self._accent)
        self.accent_btn.setStyleSheet(
            f"background:{self._accent}; color:#06222a; padding:5px; font-weight:600;")

    def values(self):
        return {
            "accent": self._accent,
            "background_opacity": self.bg.value() / 100.0,
            "window_opacity": self.win.value() / 100.0,
            "poll_ms": self.poll.value(),
            "always_on_top": self.aot.isChecked(),
            "start_expanded": self.startexp.isChecked(),
            "fallback_any": self.fallback.isChecked(),
            "hotkeys_enabled": self.hotkeys.isChecked(),
            "run_at_startup": self.startup.isChecked(),
        }
