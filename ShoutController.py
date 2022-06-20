from lib2to3.pytree import convert
from random import randint, random, shuffle
from dataclasses import dataclass, field
import os
import json
from pykakasi import Kakasi
from ShoutObject import ShoutObject
from ShoutWindow import ShoutWindow
from PySide6.QtWidgets import *
from PySide6.QtCore import QTimer

@dataclass
class ShoutController:
    window: ShoutWindow

    inventory: list[ShoutObject] = field(default_factory=list, init=True)
    active: list[ShoutObject] = field(default_factory=list, init=True)
    randomized: list[ShoutObject] = field(default_factory=list, init=True)
    
    shout_mode: int = 0
    instructions_mode: int = 1
    reading_mode: int = 10
    speed_mode: int = 5000

    def __post_init__(self):
        # Load inventory
        script_dir = os.path.dirname(__file__)
        file_path = os.path.join(script_dir, 'inventory.json')
        with open(file_path, 'r') as file:
            data = json.load(file)
            for object in data:
                self.inventory.append(ShoutObject(
                    object["character"],
                    object["onyomi"] if "onyomi" in object.keys() else None,
                    object["kunyomi"] if "kunyomi" in object.keys() else None,
                    object["yomi"] if "yomi" in object.keys() else None
                ))

        # Connect signals to widgets
        self.window.play_button.clicked.connect(self.play)

        # self.window.romaji_mode_checkbox.clicked.connect(self.romaji_mode_checkbox_clicked)

        self.window.inventory_list_widget.currentRowChanged.connect(self.inventory_list_currentRowChanged)
        self.window.active_list_widget.currentRowChanged.connect(self.active_list_currentRowChanged)

        self.window.settings_alphabet_widget.instructions_button_group.idClicked.connect(self.button_group_clicked)
        self.window.settings_alphabet_widget.reading_button_group.idClicked.connect(self.button_group_clicked)
        self.window.settings_alphabet_widget.speed_button_group.idClicked.connect(self.button_group_clicked)

        self.window.add_button.clicked.connect(self.add_button_clicked)
        self.window.inventory_list_widget.itemDoubleClicked.connect(self.add_button_clicked)
        
        self.window.remove_button.clicked.connect(self.remove_button_clicked)
        self.window.active_list_widget.itemDoubleClicked.connect(self.remove_button_clicked)

        self.window.inventory_list_widget.addItems([x.character for x in self.inventory])
        self.window.inventory_list_widget.setCurrentRow(0)


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


    def play(self, checked: bool):
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
        self.window.sample_character_label.setText(shout.character)
        self.window.sample_reading_label.setText(shout.onyomi_string + "\n" + shout.kunyomi_string)


    def active_list_currentRowChanged(self, row: int):
        shout = self.active[row]
        self.window.sample_character_label.setText(shout.character)
        self.window.sample_reading_label.setText(shout.onyomi_string + "\n" + shout.kunyomi_string)


    def refresh_lists(self):
        self.window.active_list_widget.clear()
        self.window.active_list_widget.addItems([x.character for x in self.active])

        if len(self.active) < 1:
            self.window.play_button.setDisabled(True)
        else:
            self.window.play_button.setDisabled(False)


    def romaji_mode_checkbox_clicked(self, checked: bool):
        self.is_romaji = checked

    
    def button_group_clicked(self, id: int):
        if id >= 0 and id <= 9:
            # Instructions
            self.instructions_mode = id
        elif id >= 10 and id <= 19:
            # Reading
            self.reading_mode = id
        elif id >= 3000:
            # Speed
            self.speed_mode = id


    def add_button_clicked(self, checked: bool):
        row = self.window.inventory_list_widget.currentRow()
        shout = self.inventory[row]
        self.active.append(shout)
        self.refresh_lists()
        self.window.inventory_list_widget.setCurrentRow(row)
        self.window.inventory_list_widget.setFocus()


    def remove_button_clicked(self, checked: bool):
        row = self.window.active_list_widget.currentRow()
        shout = self.active.pop(row)
        self.inventory.append(shout)
        self.refresh_lists()