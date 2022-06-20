from dataclasses import dataclass, field
from PySide6.QtWidgets import *
from PySide6.QtCore import Qt

from ShoutSettingsWidget import ShoutSettingsWidget

@dataclass
class ShoutWindow(QMainWindow):
    _tabs: QTabWidget = field(default_factory=QTabWidget, init=True)

    _shout_widget: QWidget = field(default_factory=QWidget, init=True)
    _settings_widget: QWidget = field(default_factory=QWidget, init=True)
    _inventory_widget: QWidget = field(default_factory=QWidget, init=True)
    _control_widget: QWidget = field(default_factory=QWidget, init=True)
    _active_widget: QWidget = field(default_factory=QWidget, init=True)

    _shout_layout: QVBoxLayout = field(default_factory=QVBoxLayout, init=True)
    _settings_layout: QHBoxLayout = field(default_factory=QHBoxLayout, init=True)
    _inventory_layout: QVBoxLayout = field(default_factory=QVBoxLayout, init=True)
    _control_layout: QVBoxLayout = field(default_factory=QVBoxLayout, init=True)
    _active_layout: QVBoxLayout = field(default_factory=QVBoxLayout, init=True)

    _instruction_label: QLabel = field(default_factory=QLabel, init=True)
    _character_label: QLabel = field(default_factory=QLabel, init=True)
    _reading_label: QLabel = field(default_factory=QLabel, init=True)
    _inventory_label: QLabel = field(default_factory=QLabel, init=True)
    _sample_character_label: QLabel = field(default_factory=QLabel, init=True)
    _sample_reading_label: QLabel = field(default_factory=QLabel, init=True)
    _active_label: QLabel = field(default_factory=QLabel, init=True)

    _settings_alphabet_widget: ShoutSettingsWidget = field(default_factory=ShoutSettingsWidget)

    _play_button: QPushButton = field(default_factory=QPushButton, init=True)
    _add_button: QPushButton = field(default_factory=QPushButton, init=True)
    _remove_button: QPushButton = field(default_factory=QPushButton, init=True)

    _inventory_list_widget: QListWidget = field(default_factory=QListWidget, init=True)
    _active_list_widget: QListWidget = field(default_factory=QListWidget, init=True)


    def __post_init__(self):
        super(ShoutWindow, self).__init__()
        self.setWindowTitle("Magical SHOUT!")
        self.setStyleSheet("""
        QListWidget {
            font-size: 64pt;
        }
        """)
        self.setCentralWidget(self._tabs)

        # Main page
        self._shout_widget.setLayout(self._shout_layout)
        self.play_button.setDefault(True)
        self.play_button.setDisabled(True)
        self.play_button.setText("Play")
        self._instruction_label.setStyleSheet("font-size: 64pt;")
        self._instruction_label.setAlignment(Qt.AlignHCenter)
        self._character_label.setStyleSheet("font-size: 384pt;")
        self._character_label.setAlignment(Qt.AlignHCenter)
        self._reading_label.setStyleSheet("font-size: 64pt;")
        self._reading_label.setAlignment(Qt.AlignHCenter)

        self._shout_layout.addWidget(self._instruction_label)
        self._shout_layout.addStretch()
        self._shout_layout.addWidget(self._character_label)
        self._shout_layout.addStretch()
        self._shout_layout.addWidget(self.reading_label)
        self._shout_layout.addWidget(self.play_button)

        # Settings page
        self._settings_widget.setLayout(self._settings_layout)
        self._control_widget.setLayout(self._control_layout)
        self._inventory_widget.setLayout(self._inventory_layout)
        self._active_widget.setLayout(self._active_layout)

        self._control_widget.setFixedWidth(300)
        self._sample_character_label.setAlignment(Qt.AlignHCenter)
        self._sample_character_label.setStyleSheet("font-size: 48pt;")
        self._sample_reading_label.setAlignment(Qt.AlignHCenter)
        self._sample_reading_label.setStyleSheet("font-size: 24pt;")
        self._add_button.setText("Add character ->")
        self._remove_button.setText("<- Remove character")

        self._settings_layout.addWidget(self._inventory_widget)
        self._inventory_layout.addWidget(QLabel("Inventory"))
        self._inventory_layout.addWidget(self._inventory_list_widget)
        self._settings_layout.addWidget(self._control_widget)
        self._control_layout.addWidget(self._sample_character_label)
        self._control_layout.addSpacing(24)
        self._control_layout.addWidget(self._sample_reading_label)
        self._control_layout.addStretch()
        self._control_layout.addWidget(self._add_button)
        self._control_layout.addWidget(self._remove_button)
        self._control_layout.addStretch()
        self._control_layout.addWidget(self._settings_alphabet_widget)
        self._settings_layout.addWidget(self._active_widget)
        self._active_layout.addWidget(QLabel("Active characters"))
        self._active_layout.addWidget(self._active_list_widget)

        # Set up tabs
        self._tabs.addTab(self._shout_widget, "SHOUT!")
        self._tabs.addTab(self._settings_widget, "Settings")

        self.resize(1280, 720)

    @property
    def inventory_list_widget(self) -> QListWidget:
        return self._inventory_list_widget

    @property
    def active_list_widget(self) -> QListWidget:
        return self._active_list_widget

    @property
    def instruction_label(self) -> QLabel:
        return self._instruction_label

    @property
    def character_label(self) -> QLabel:
        return self._character_label

    @property
    def reading_label(self) -> QLabel:
        return self._reading_label

    @property
    def settings_alphabet_widget(self) -> ShoutSettingsWidget:
        return self._settings_alphabet_widget

    @property
    def sample_character_label(self) -> QLabel:
        return self._sample_character_label

    @property
    def sample_reading_label(self) -> QLabel:
        return self._sample_reading_label

    @property
    def play_button(self) -> QPushButton:
        return self._play_button

    @property
    def add_button(self) -> QPushButton:
        return self._add_button

    @property
    def remove_button(self) -> QPushButton:
        return self._remove_button