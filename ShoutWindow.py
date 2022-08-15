from dataclasses import dataclass, field
from PySide6.QtWidgets import *
from PySide6.QtCore import Qt
from PySide6.QtGui import QAction, QActionGroup, QIcon

@dataclass
class ShoutWindow(QMainWindow):
    instructions_actions: QActionGroup = field(init=False)
    reading_actions: QActionGroup = field(init=False)
    speed_actions: QActionGroup = field(init=False)
    view_actions: list = field(init=False)

    menubar: QMenuBar = field(default_factory=QMenuBar, init=True)
    file_menu: QMenu = field(default_factory=QMenu, init=True)
    open_action: QAction = field(default_factory=QAction, init=False)
    save_action: QAction = field(default_factory=QAction, init=False)
    settings_action: QAction = field(default_factory=QAction, init=False)
    view_menu: QMenu = field(default_factory=QMenu, init=True)
    instructions_menu: QMenu = field(default_factory=lambda: QMenu("Show Instructions As"))
    instructions_kanji_action: QAction = field(default_factory=lambda: QAction("Kanji"))
    instructions_kana_action: QAction = field(default_factory=lambda: QAction("Hiragana"))
    instructions_romaji_action: QAction = field(default_factory=lambda: QAction("Romaji"))
    reading_menu: QMenu = field(default_factory=lambda: QMenu("Show Reading As"))
    reading_kana_action: QAction = field(default_factory=lambda: QAction("Hiragana and Katakana"))
    reading_hiragana_action: QAction = field(default_factory=lambda: QAction("Hiragana Only"))
    reading_romaji_action: QAction = field(default_factory=lambda: QAction("Romaji"))
    speed_menu: QMenu = field(default_factory=lambda: QMenu("Reveal Speed"))
    speed_slow_action: QAction = field(default_factory=lambda: QAction("Slow"))
    speed_medium_action: QAction = field(default_factory=lambda: QAction("Medium"))
    speed_fast_action: QAction = field(default_factory=lambda: QAction("Fast"))

    shout_tabs: QStackedWidget = field(default_factory=QStackedWidget, init=True)
    shout_widget: QWidget = field(default_factory=QWidget, init=True)
    shout_layout: QVBoxLayout = field(default_factory=QVBoxLayout, init=True)

    instruction_label: QLabel = field(default_factory=QLabel, init=True)
    character_label: QLabel = field(default_factory=QLabel, init=True)
    reading_label: QLabel = field(default_factory=QLabel, init=True)

    start_button: QPushButton = field(default_factory=lambda: QPushButton("Click to Start"))
    play_button: QPushButton = field(default_factory=QPushButton, init=True)

    def __post_init__(self):
        super(ShoutWindow, self).__init__()
        self.setWindowTitle("Magical SHOUT!")
        self.setStyleSheet("""
        QListWidget {
            font-size: 64pt;
        }
        """)
        self.setCentralWidget(self.shout_tabs)

        self.start_button.setStyleSheet("font-size: 64pt")
        self.shout_tabs.addWidget(self.start_button)
        self.shout_tabs.addWidget(self.shout_widget)

        self.instructions_actions = QActionGroup(self)
        self.instructions_actions.setExclusive(True)
        for action in [
            self.instructions_kanji_action,
            self.instructions_kana_action,
            self.instructions_romaji_action
        ]:
            self.instructions_actions.addAction(action)

        self.reading_actions = QActionGroup(self)
        self.reading_actions.setExclusive(True)
        for action in [
            self.reading_kana_action,
            self.reading_hiragana_action,
            self.reading_romaji_action
        ]:
            self.reading_actions.addAction(action)

        self.speed_actions = QActionGroup(self)
        self.speed_actions.setExclusive(True)
        for action in [
            self.speed_slow_action,
            self.speed_medium_action,
            self.speed_fast_action
        ]:
            self.speed_actions.addAction(action)

        self._view_actions = [
            self.instructions_kanji_action,
            self.instructions_kana_action,
            self.instructions_romaji_action,
            self.reading_kana_action,
            self.reading_hiragana_action,
            self.reading_romaji_action,
            self.speed_slow_action,
            self.speed_medium_action,
            self.speed_fast_action
        ]

        # Menu
        self.menubar = QMenuBar()
        # File
        self.file_menu = QMenu("File")
        self.open_action = QAction("&Open Inventory…")
        self.save_action = QAction("&Save Inventory As…")
        self.settings_action = QAction("&Settings…")
        self.file_menu.addAction(self.open_action)
        self.file_menu.addAction(self.save_action)
        self.file_menu.addSeparator()
        self.file_menu.addAction(self.settings_action)
        # View
        self.view_menu = QMenu("View")
        self.instructions_menu.addActions(self.instructions_actions.actions())
        self.reading_menu.addActions(self.reading_actions.actions())
        self.speed_menu.addActions(self.speed_actions.actions())
        for action in self._view_actions:
            action.setCheckable(True)
        self.instructions_kanji_action.setChecked(True)
        self.reading_hiragana_action.setChecked(True)
        self.speed_slow_action.setChecked(True)
        self.view_menu.addSeparator()
        # Add menus
        self.menubar.addMenu(self.file_menu)
        self.menubar.addMenu(self.view_menu)
        self.view_menu.addMenu(self.instructions_menu)
        self.view_menu.addMenu(self.reading_menu)
        self.view_menu.addMenu(self.speed_menu)
        self.setMenuBar(self.menubar)

        # Main page
        self.shout_widget.setLayout(self.shout_layout)
        self.play_button.setDefault(True)
        self.play_button.setDisabled(True)
        self.play_button.setText("Play")
        self.instruction_label.setStyleSheet("font-size: 64pt;")
        self.instruction_label.setAlignment(Qt.AlignHCenter)
        self.character_label.setStyleSheet("font-size: 384pt;")
        self.character_label.setAlignment(Qt.AlignHCenter)
        self.reading_label.setStyleSheet("font-size: 64pt;")
        self.reading_label.setAlignment(Qt.AlignHCenter)

        self.shout_layout.addWidget(self.instruction_label)
        self.shout_layout.addStretch()
        self.shout_layout.addWidget(self.character_label)
        self.shout_layout.addStretch()
        self.shout_layout.addWidget(self.reading_label)
        self.shout_layout.addWidget(self.play_button)

        self.resize(1280, 800)
        self.move(0, 0)
