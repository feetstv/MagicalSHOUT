from dataclasses import dataclass, field
from email.policy import default
from PySide6.QtWidgets import *
from PySide6.QtCore import Qt
from PySide6.QtGui import QAction, QActionGroup, QIcon

@dataclass
class ShoutSettingsWindow(QDialog):
    window_layout: QVBoxLayout = field(default_factory=QVBoxLayout, init=True)
    settings_layout: QHBoxLayout = field(default_factory=QHBoxLayout, init=True)
    inventory_layout: QVBoxLayout = field(default_factory=QVBoxLayout, init=True)
    control_layout: QVBoxLayout = field(default_factory=QVBoxLayout, init=True)
    active_layout: QVBoxLayout = field(default_factory=QVBoxLayout, init=True)

    inventory_label: QLabel = field(default_factory=QLabel, init=True)
    sample_character_label: QLabel = field(default_factory=QLabel, init=True)
    sample_reading_label: QLabel = field(default_factory=QLabel, init=True)
    active_label: QLabel = field(default_factory=QLabel, init=True)

    add_button: QPushButton = field(default_factory=lambda: QPushButton("Add →"))
    add_all_button: QPushButton = field(default_factory=lambda: QPushButton("Add All →"))
    remove_button: QPushButton = field(default_factory=lambda: QPushButton("← Remove"))
    play_button: QPushButton = field(default_factory=lambda: QPushButton("Play"))

    inventory_list_widget: QListWidget = field(default_factory=QListWidget, init=True)
    active_list_widget: QListWidget = field(default_factory=QListWidget, init=True)

    button_box: QDialogButtonBox = field(default_factory=lambda: QDialogButtonBox(QDialogButtonBox.Ok))


    def __post_init__(self):
        super(ShoutSettingsWindow, self).__init__()
        self.setWindowTitle("Settings")
        self.setStyleSheet("""
        QListWidget {
            font-size: 64pt;
        }
        """)
        self.setLayout(self.window_layout)

        self.window_layout.addLayout(self.settings_layout)

        self.sample_character_label.setAlignment(Qt.AlignHCenter)
        self.sample_character_label.setStyleSheet("font-size: 48pt;")
        self.sample_reading_label.setAlignment(Qt.AlignHCenter)
        self.sample_reading_label.setStyleSheet("font-size: 24pt;")
        self.sample_reading_label.setMinimumWidth(300)
        self.add_button.setText("Add character ->")
        self.remove_button.setText("<- Remove character")

        self.settings_layout.addLayout(self.inventory_layout)
        self.inventory_layout.addWidget(QLabel("Inventory"))
        self.inventory_layout.addWidget(self.inventory_list_widget)
        self.settings_layout.addLayout(self.control_layout)
        self.control_layout.addWidget(self.sample_character_label)
        self.control_layout.addSpacing(24)
        self.control_layout.addWidget(self.sample_reading_label)
        self.control_layout.addStretch()
        self.settings_layout.addLayout(self.active_layout)
        self.active_layout.addWidget(QLabel("Active characters"))
        self.active_layout.addWidget(self.active_list_widget)

        add_layout = QHBoxLayout()
        add_layout.addWidget(self.add_button)
        add_layout.addWidget(self.add_all_button)
        self.inventory_layout.addLayout(add_layout)
        self.active_layout.addWidget(self.remove_button)

        self.window_layout.addWidget(self.button_box)

        self.resize(800, 600)