import sys

import PySimpleGUI as sg

from command_abs import CommandSelection, Command
from datasets.dataset import Dataset
from datasets.datasets_manager import DatasetsManager
from prism import Prism
from ui.ui import UserInterface


class SimpleGui(UserInterface):
    def __init__(self):
        self.layout = [[sg.Text(self.TITLE, key="-TITLE-")], [sg.Text(self.SUBTITLE, key="-SUBTITLE-")]]
        self.window = sg.Window(title="Prism", layout=self.layout, margins=(100, 50))

    def welcome_page(self, command_selection: CommandSelection) -> Command:
        self.__switch_layout([[sg.Text(self.TITLE, key="-TITLE-")], [sg.Text(self.SUBTITLE, key="-SUBTITLE-")],
                              *[[sg.Button(c.name)] for c in command_selection.commands]])
        command_names = [c.name for c in command_selection.commands]

        while True:
            event, values = self.window.read()
            if event == sg.WIN_CLOSED:
                sys.exit()
            try:
                i = command_names.index(event)
                return command_selection.commands[i]
            except ValueError:
                continue

    def select_dataset(self, manager: DatasetsManager) -> Dataset:
        self.__switch_layout([[sg.Text(self.SELECT_DATASET_TITLE)],
                              [sg.Table(headings=["index", "name", "# instances", "# attributes", "# targets", "rules available"],
                                        values=[[i+1, d.name, d.num_inst, d.num_att, d.num_targ, d.rules_available] for i, d in enumerate(manager.datasets)],
                                        key='-TABLE-', enable_click_events=True)]])
        while True:
            event, values = self.window.read()
            if event == sg.WIN_CLOSED:
                sys.exit()
            if isinstance(event, tuple) and event[0] == "-TABLE-" and event[2][0] != -1:
                return manager.datasets[event[2][0]]

    def should_load_rules(self) -> bool:
        pass

    def analyse_dataset(self, prism: Prism, dataset: Dataset):
        pass

    def fit_rules(self):
        pass

    def update_progress(self, state: int):
        pass

    def update_class(self, class_name: str, class_num: int, num_classes: int, total_num_it: int):
        pass

    def __switch_layout(self, layout):
        self.layout = layout
        self.window.close()
        self.window = sg.Window(title="Prism", layout=self.layout, margins=(100, 50))
