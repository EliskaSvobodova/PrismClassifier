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
                                        values=[[i+1, d.name, d.num_inst, d.num_att, d.num_targ, d.rules_available]
                                                for i, d in enumerate(manager.datasets)],
                                        key='-TABLE-', enable_click_events=True)],
                              [sg.Text(self.FIT_RULES_TEXT, visible=False, key="-FIT-TEXT-")],
                              [sg.Text(f"Class: ", visible=False, key="-CLASS-TEXT-"),
                               sg.ProgressBar(100, orientation='h', size=(10, 10), visible=False, key="-PROG-")]])
        self.window['-PROG-'].expand(expand_x=True)
        while True:
            event, values = self.window.read()
            if event == sg.WIN_CLOSED:
                sys.exit()
            if isinstance(event, tuple) and event[0] == "-TABLE-" and event[2][0] != -1:
                return manager.datasets[event[2][0]]

    def should_load_rules(self) -> bool:
        layout = [[sg.Text(self.SHOULD_LOAD_DATASET)], [sg.Button("Yes", key="-YES-"), sg.Button("No", key="-NO-")]]
        pop_window = sg.Window(title="Load data", layout=layout, margins=(100, 50))
        while True:
            event, values = pop_window.read()
            if event == sg.WIN_CLOSED:
                sys.exit()
            if event == "-YES-":
                pop_window.close()
                return True
            if event == "-NO-":
                pop_window.close()
                return False

    def analyse_dataset(self, prism: Prism, dataset: Dataset):
        # TODO: list of rules, evaluate rules, evaluate model
        pass

    def fit_rules(self):
        self.window['-FIT-TEXT-'].update(visible=True)
        self.window['-CLASS-TEXT-'].update(visible=True)
        self.window['-PROG-'].update(visible=True)

    def update_progress(self, state: int):
        self.window['-PROG-'].update(state)

    def update_class(self, class_name: str, class_num: int, num_classes: int, total_num_it: int):
        self.window['-CLASS-TEXT-'].update(f"Class: {class_name} ({class_num}/{num_classes})")
        self.window['-PROG-'].update_bar(0, total_num_it)

    def __switch_layout(self, layout):
        self.layout = layout
        self.window.close()
        self.window = sg.Window(title="Prism", layout=self.layout, margins=(100, 50)).finalize()
