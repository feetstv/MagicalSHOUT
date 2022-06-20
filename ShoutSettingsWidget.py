from dataclasses import dataclass, field
from PySide6.QtWidgets import *

@dataclass
class ShoutSettingsWidget(QWidget):
    _instructions_group_box: QGroupBox = field(default_factory=lambda: QGroupBox("Show instructions as:"))
    _reading_group_box: QGroupBox = field(default_factory=lambda: QGroupBox("Show reading as:"))
    _speed_group_box: QGroupBox = field(default_factory=lambda: QGroupBox("Reading reveal speed:"))

    _instructions_button_group: QButtonGroup = field(default_factory=QButtonGroup, init=True)
    _reading_button_group: QButtonGroup = field(default_factory=QButtonGroup, init=True)
    _speed_button_group: QButtonGroup = field(default_factory=QButtonGroup, init=True)

    _instructions_kanji_radio_button: QRadioButton = field(default_factory=lambda: QRadioButton("Kanji"))
    _instructions_kana_radio_button: QRadioButton = field(default_factory=lambda: QRadioButton("Hiragana"))
    _instructions_romaji_radio_button: QRadioButton = field(default_factory=lambda: QRadioButton("Romaji"))

    _reading_kana_radio_button: QRadioButton = field(default_factory=lambda: QRadioButton("Kana"))
    _reading_hiragana_radio_button: QRadioButton = field(default_factory=lambda: QRadioButton("Hiragana only"))
    _reading_katakana_radio_button: QRadioButton = field(default_factory=lambda: QRadioButton("Katakana only"))
    _reading_romaji_radio_button: QRadioButton = field(default_factory=lambda: QRadioButton("Romaji"))

    _speed_slow_radio_button: QRadioButton = field(default_factory=lambda: QRadioButton("Slow"))
    _speed_medium_radio_button: QRadioButton = field(default_factory=lambda: QRadioButton("Medium"))
    _speed_fast_radio_button: QRadioButton = field(default_factory=lambda: QRadioButton("Fast"))

    def __post_init__(self):
        super(ShoutSettingsWidget, self).__init__()
        
        self._instructions_button_group.addButton(self._instructions_kanji_radio_button, 0)
        self._instructions_button_group.addButton(self._instructions_kana_radio_button, 1)
        self._instructions_button_group.addButton(self._instructions_romaji_radio_button, 2)
        self._instructions_kana_radio_button.setChecked(True)
        self._instructions_group_box.setLayout(QVBoxLayout())
        for button in self._instructions_button_group.buttons():
            self._instructions_group_box.layout().addWidget(button)

        self._reading_button_group.addButton(self._reading_kana_radio_button, 10)
        self._reading_button_group.addButton(self._reading_hiragana_radio_button, 11)
        self._reading_button_group.addButton(self._reading_katakana_radio_button, 12)
        self._reading_button_group.addButton(self._reading_romaji_radio_button, 13)
        self._reading_kana_radio_button.setChecked(True)
        self._reading_group_box.setLayout(QVBoxLayout())
        for button in self._reading_button_group.buttons():
            self._reading_group_box.layout().addWidget(button)

        self._speed_button_group.addButton(self._speed_slow_radio_button,7000)
        self._speed_button_group.addButton(self._speed_medium_radio_button, 5000)
        self._speed_button_group.addButton(self._speed_fast_radio_button, 3000)
        self._speed_medium_radio_button.setChecked(True)
        self._speed_group_box.setLayout(QVBoxLayout())
        for button in self._speed_button_group.buttons():
            self._speed_group_box.layout().addWidget(button)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self._instructions_group_box)
        main_layout.addStretch()
        main_layout.addWidget(self._reading_group_box)
        main_layout.addStretch()
        main_layout.addWidget(self._speed_group_box)
        self.setLayout(main_layout)


    @property
    def instructions_button_group(self) -> QButtonGroup:
        return self._instructions_button_group

    
    @property
    def reading_button_group(self) -> QButtonGroup:
        return self._reading_button_group


    @property
    def speed_button_group(self) -> QButtonGroup:
        return self._speed_button_group
