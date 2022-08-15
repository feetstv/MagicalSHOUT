from lib2to3.pytree import convert
from random import randint, random, shuffle
from dataclasses import dataclass, field
import os
import json
from pykakasi import Kakasi
from ShoutObject import ShoutObject
from ShoutSettingsWindow import ShoutSettingsWindow
from ShoutWindow import ShoutWindow
from PySide6.QtWidgets import *
from PySide6.QtCore import QTimer
from PySide6.QtGui import QAction

@dataclass
class ShoutController:
    window: ShoutWindow = field(default_factory=ShoutWindow, init=True)
    settings_window: ShoutSettingsWindow = field(default_factory=ShoutSettingsWindow, init=True)

    inventory: list[ShoutObject] = field(default_factory=list, init=True)
    active: list[ShoutObject] = field(default_factory=list, init=True)
    randomized: list[ShoutObject] = field(default_factory=list, init=True)
    
    shout_mode: int = 0
    instructions_mode: int = 1
    reading_mode: int = 10
    speed_mode: int = 5000

    def __post_init__(self):
        # Connect signals to widgets
        self.window.start_button.clicked.connect(self.start_button_clicked)
        self.window.play_button.clicked.connect(self.play)

        self.window.open_action.triggered.connect(self.open_action_triggered)
        self.window.save_action.triggered.connect(self.save_action_triggered)
        self.window.settings_action.triggered.connect(self.settings_action_triggered)

        self.settings_window.inventory_list_widget.currentRowChanged.connect(self.inventory_list_currentRowChanged)
        self.settings_window.active_list_widget.currentRowChanged.connect(self.active_list_currentRowChanged)

        self.settings_window.add_button.clicked.connect(self.add_button_clicked)
        self.settings_window.inventory_list_widget.itemDoubleClicked.connect(self.add_button_clicked)

        self.settings_window.add_all_button.clicked.connect(self.add_all_button_clicked)
        
        self.settings_window.remove_button.clicked.connect(self.remove_button_clicked)
        self.settings_window.active_list_widget.itemDoubleClicked.connect(self.remove_button_clicked)

        self.settings_window.inventory_list_widget.addItems([x.character for x in self.inventory])
        self.settings_window.inventory_list_widget.setCurrentRow(0)


    def reveal_reading(self):
        shout = self.randomized.pop(0)

        reading = ""
        match self.shout_mode:
            case 0:
                reading = shout.onyomi_string
            case 1:
                reading = shout.kunyomi_string
            case 2:
                reading = shout.yomi

        if self.reading_mode in range(10, 20):
            converter = Kakasi()
            variants = converter.convert(reading)[0]
            match self.reading_mode:
                case 11:
                    reading = variants['hira']
                case 12:
                    reading = variants['kana']
                case 13:
                    reading = variants['hepburn']

        self.window.reading_label.setText(reading)

        self.window.play_button.setDisabled(False)
        self.window.play_button.setFocus()


    def refresh_settings(self):
        # Instructions
        match self.window.instructions_actions.checkedAction():
            case self.window.instructions_kanji_action:
                self.instructions_mode = 0
            case self.window.instructions_kana_action:
                self.instructions_mode = 1
            case self.window.instructions_romaji_action:
                self.instructions_mode = 2
        
        # Reading
        match self.window.reading_actions.checkedAction():
            case self.window.reading_hiragana_action:
                self.reading_mode = 11
            case self.window.reading_kana_action:
                self.reading_mode = 12
            case self.window.reading_romaji_action:
                self.reading_mode = 13

        # Speed
        match self.window.speed_actions.checkedAction():
            case self.window.speed_slow_action:
                self.speed_mode = 7000
            case self.window.speed_medium_action:
                self.speed_mode = 6000
            case self.window.speed_fast_action:
                self.speed_mode = 5000

        print(self.instructions_mode)
        print(self.reading_mode)
        print(self.speed_mode)


    def play(self, checked: bool):
        self.refresh_settings()

        if len(self.randomized) == 0:
            self.randomized = self.active.copy()
            shuffle(self.randomized)

        self.window.play_button.setDisabled(True)
        self.window.character_label.setText("")
        self.window.reading_label.setText("")

        shout = self.randomized[0]
        shout_modes = [x for x in [
            0 if shout.onyomi_string else -1,
            1 if shout.kunyomi_string else -1,
            2 if shout.yomi else -1
        ] if x > -1]
        self.shout_mode = shout_modes[randint(0, len(shout_modes) - 1)]

        instruction = ""
        match self.shout_mode:
            case 0:
                instruction = "音読み"
            case 1:
                instruction = "訓読み"
            case 2:
                instruction = "言葉を読んでください"

        if self.instructions_mode in range(1, 3):
            converter = Kakasi()
            variants = converter.convert(instruction)[0]
            match self.instructions_mode:
                case 1:
                    instruction = variants['hira']
                case 2:
                    instruction = variants['hepburn']
                
        self.window.instruction_label.setText(instruction)

        QTimer.singleShot(1500, lambda: self.window.character_label.setText(shout.character))
        QTimer.singleShot(self.speed_mode, self.reveal_reading)


    def inventory_list_currentRowChanged(self, row: int):
        shout = self.inventory[row]
        self.settings_window.sample_character_label.setText(shout.character)
        self.settings_window.sample_reading_label.setText(
            (shout.onyomi_string if shout.onyomi_string else "")
            + "\n"
            + (shout.kunyomi_string if shout.kunyomi_string else "")
            + "\n"
            + (shout.yomi if shout.yomi else "")
        )


    def active_list_currentRowChanged(self, row: int):
        shout = self.active[row]
        self.settings_window.sample_character_label.setText(shout.character)
        self.settings_window.sample_reading_label.setText(
            (shout.onyomi_string if shout.onyomi_string else "")
            + "\n"
            + (shout.kunyomi_string if shout.kunyomi_string else "")
            + "\n"
            + (shout.yomi if shout.yomi else "")
        )


    def refresh_lists(self):
        self.settings_window.inventory_list_widget.clear()
        self.settings_window.inventory_list_widget.addItems([x.character for x in self.inventory])
        self.settings_window.active_list_widget.clear()
        self.settings_window.active_list_widget.addItems([x.character for x in self.active])

        if len(self.active) < 1:
            self.window.play_button.setDisabled(True)
        else:
            self.window.play_button.setDisabled(False)


    def romaji_mode_checkbox_clicked(self, checked: bool):
        self.is_romaji = checked


    def add_button_clicked(self, checked: bool):
        row = self.settings_window.inventory_list_widget.currentRow()
        shout = self.inventory[row]
        self.active.append(shout)
        self.refresh_lists()
        self.settings_window.inventory_list_widget.setCurrentRow(row)
        self.settings_window.inventory_list_widget.setFocus()

    
    def add_all_button_clicked(self, checked: bool):
        self.active = self.inventory.copy()
        self.refresh_lists()


    def remove_button_clicked(self, checked: bool):
        row = self.settings_window.active_list_widget.currentRow()
        shout = self.active.pop(row)
        self.inventory.append(shout)
        self.refresh_lists()


    def open_action_triggered(self):
        self.settings_action_triggered()
        file_path = str(QFileDialog.getOpenFileName(None, "Open Inventory…", "~", "Inventories (*.json)")[0])
        with open(file_path, 'r') as file:
            self.inventory.clear()
            data = json.load(file)
            for object in data:
                self.inventory.append(ShoutObject(
                    object["character"],
                    object["onyomi"] if "onyomi" in object.keys() else None,
                    object["kunyomi"] if "kunyomi" in object.keys() else None,
                    object["yomi"] if "yomi" in object.keys() else None
                ))
            self.refresh_lists()
            self.window.shout_tabs.setCurrentIndex(1)
            QMessageBox(QMessageBox.Information, "Inventory opened", f"Opened new inventory from {file_path}.").exec()


    def save_action_triggered(self):
        file_path = str(QFileDialog.getSaveFileName(None, "Save Inventory As…", "~", "Inventories (*.json)")[0])
        with open(file_path, 'w+') as file:
            inventory_list = []
            for object in self.inventory:
                dict = {}
                dict["character"] = object.character
                if object.onyomi_string:
                    dict["onyomi"] = [x for x in object.onyomi_string.split("•")]
                if object.kunyomi_string:
                    dict["kunyomi"] = [x for x in object.kunyomi_string.split("•")]
                if object.yomi:
                    dict["yomi"] = object.yomi
                inventory_list.append(dict)
            string = json.dumps(inventory_list)
            file.write(string)
            QMessageBox(QMessageBox.Information, "Inventory saved", f"Your inventory was saved to {file_path}.").exec()


    def start_button_clicked(self, checked: bool):
        self.open_action_triggered()


    def settings_action_triggered(self):
        self.settings_window.show()