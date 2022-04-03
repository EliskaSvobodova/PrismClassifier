import sys
from typing import List, Optional

import PySimpleGUI as sg

from command_abs import CommandSelection, Command
from datasets.dataset import Dataset
from datasets.datasets_manager import DatasetsManager
from prism import Prism
from rules.rule_eval import RuleEval
from ui.ui import UserInterface


class SimpleGui(UserInterface):
    def __init__(self):
        self.layout = [[sg.Text(self.TITLE, key="-TITLE-")], [sg.Text(self.SUBTITLE, key="-SUBTITLE-")]]
        self.window = sg.Window(title="Prism", layout=self.layout, margins=(100, 50)).Finalize()

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

    def select_dataset(self, manager: DatasetsManager) -> Optional[Dataset]:
        self.__switch_layout([[sg.Text(self.SELECT_DATASET_TITLE)],
                              [sg.Table(headings=["index", "name", "# instances", "# attributes", "# targets",
                                                  "rules available"],
                                        values=[[i + 1, d.name, len(d.train) + len(d.test), d.num_att, d.num_targ,
                                                 d.rules_available]
                                                for i, d in enumerate(manager.datasets)],
                                        key='-TABLE-', enable_click_events=True)],
                              [sg.Text(self.FIT_RULES_TEXT, visible=False, key="-FIT-TEXT-")],
                              [sg.Text(f"Class: ", visible=False, key="-CLASS-TEXT-"),
                               sg.ProgressBar(100, orientation='h', size=(10, 10), visible=False, key="-PROG-")]])
        self.window['-PROG-'].expand(expand_x=True)
        while True:
            event, values = self.window.read()
            if event == sg.WIN_CLOSED:
                return
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
        self.__switch_layout([[sg.Text(self.RULES_ANALYSIS_TITLE)],
                              [sg.Text("Accuracy: [calculating]", key='-ACCURACY-')],
                              [sg.Table(headings=["Coverage", "Precision", "Rule"], enable_click_events=True,
                                        values=[["-", "-", r] for r in prism.rules],
                                        size=(100, 50), key="-TABLE-")]])

        self.window.perform_long_operation(lambda: prism.evaluate_dataset(dataset.X_test, dataset.y_test),
                                           '-EVAL-MODEL-DONE-')
        self.window.perform_long_operation(lambda: prism.evaluate_rules(dataset.X_test, dataset.y_test),
                                           '-EVAL-RULES-DONE-')

        rules_eval = None

        while True:
            event, values = self.window.read()
            if event == sg.WIN_CLOSED:
                return
            if event == '-EVAL-MODEL-DONE-':
                d_eval = values[event]
                self.window['-ACCURACY-'].update(f"Accuracy: {d_eval.accuracy}")
            if event == '-EVAL-RULES-DONE-':
                rules_eval = values[event]
                self.window['-TABLE-'].update(self.__rules_eval_list(rules_eval))
            if isinstance(event, tuple) and event[0] == "-TABLE-" and event[2][0] == -1 and rules_eval is not None:
                if event[2][1] == 0:
                    rules_eval = sorted(rules_eval, key=lambda r: (r.coverage, r.precision), reverse=True)
                    self.window['-TABLE-'].update(self.__rules_eval_list(rules_eval))
                elif event[2][1] == 1:
                    rules_eval = sorted(rules_eval, key=lambda r: (r.precision, r.coverage), reverse=True)
                    self.window['-TABLE-'].update(self.__rules_eval_list(rules_eval))

    def fit_rules(self):
        self.window['-FIT-TEXT-'].update(visible=True)
        self.window['-CLASS-TEXT-'].update(visible=True)
        self.window['-PROG-'].update(visible=True)

    def update_progress(self, state: int):
        self.window['-PROG-'].update(state)

    def update_class(self, class_name: str, class_num: int, num_classes: int, total_num_it: int):
        self.window['-CLASS-TEXT-'].update(f"Class: {class_name} ({class_num}/{num_classes})")
        self.window['-PROG-'].update_bar(0, total_num_it)

    def upload_dataset(self, top_dir) -> Optional[Dataset]:
        self.__switch_layout([[sg.Text("Upload new dataset")],
                              [sg.Text("Choose a csv file:"),
                               sg.Input(key="-IN-"),
                               sg.FileBrowse("Browse", target='-IN-')],
                              [sg.Text("Name of your dataset: "), sg.Input(key="-NAME-")],
                              [sg.Text("Name of the target variable: "), sg.Input(key="-TARGET-")],
                              [sg.Button("Upload", key='-UPLOAD-')]])

        while True:
            event, values = self.window.read()
            if event == sg.WIN_CLOSED:
                return
            if event == '-UPLOAD-':
                s = values['-IN-']
                name = values['-NAME-']
                y_name = values['-TARGET-']
                try:
                    dataset = Dataset.create_from_file(s, y_name, name, top_dir)
                    return dataset
                except ValueError as e:
                    layout = [[sg.Text(e.args[0])], [sg.Button("OK")]]
                    error_window = sg.Window(title="Error while uploading dataset", layout=layout, margins=(100, 50))
                    error_window.read()
                    error_window.close()

    def __switch_layout(self, layout):
        self.layout = layout
        self.window.close()
        self.window = sg.Window(title="Prism", layout=self.layout, margins=(100, 50)).finalize()

    def __rules_eval_list(self, rules_eval: List[RuleEval]) -> List[List[str]]:
        return [[f"{r.coverage:3.2f}", f"{r.precision:3.2f}", r.rule] for r in rules_eval]
