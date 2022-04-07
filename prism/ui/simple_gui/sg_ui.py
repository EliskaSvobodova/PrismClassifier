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
    FONT = "Noto Sans CJK TC"
    H1_SIZE = 25
    H2_SIZE = 18
    TEXT_SIZE = 13

    def __init__(self):
        sg.theme("LightBlue6")
        self.layout = []
        self.window = sg.Window("Prism")

    def welcome_page(self, command_selection: CommandSelection) -> Command:
        self.__switch_layout([[self.h1(self.TITLE, key="-TITLE-")],
                              [self.h2(self.SUBTITLE, key="-SUBTITLE-")],
                              [sg.VPush()],
                              *[[self.button(c.name, expand_x=True)] for c in command_selection.commands],
                              [sg.VPush()]])
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
        self.__switch_layout([[self.h2(self.SELECT_DATASET_TITLE)],
                              [sg.Table(headings=["index", "name", "# instances", "# attributes", "# targets",
                                                  "rules available"],
                                        values=[[i + 1, d.name, len(d.train) + len(d.test), d.num_att, d.num_targ,
                                                 d.rules_available]
                                                for i, d in enumerate(manager.datasets)],
                                        key='-TABLE-', enable_click_events=True, font=(self.FONT, self.TEXT_SIZE))],
                              [self.text(self.FIT_RULES_TEXT, visible=False, key="-FIT-TEXT-")],
                              [self.text(f"Class: ", visible=False, key="-CLASS-TEXT-"),
                               sg.ProgressBar(100, orientation='h', size=(10, 10), visible=False, key="-PROG-")]])

        while True:
            event, values = self.window.read()
            if event == sg.WIN_CLOSED:
                return
            if isinstance(event, tuple) and event[0] == "-TABLE-" and event[2][0] != -1:
                return manager.datasets[event[2][0]]

    def should_load_rules(self) -> bool:
        layout = [[self.text(self.SHOULD_LOAD_DATASET)],
                  [sg.Push(), self.button("Yes", key="-YES-"), sg.Push(), self.button("No", key="-NO-"), sg.Push()]]
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
        self.__switch_layout([[self.h2(self.RULES_ANALYSIS_TITLE)],
                              [self.text("Accuracy: [calculating]", key='-ACCURACY-')],
                              [sg.Table(headings=["Coverage", "Precision", "Rule"], enable_click_events=True,
                                        values=[["-", "-", r] for r in prism.rules], vertical_scroll_only=False,
                                        auto_size_columns=False, justification='left',
                                        col_widths=[10, 10, int(max(len(repr(r)) for r in prism.rules) * 0.8)],
                                        size=(100, 50), key="-TABLE-", font=(self.FONT, self.TEXT_SIZE))]])

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
        self.window['-PROG-'].expand(expand_x=True)

    def update_progress(self, state: int):
        self.window['-PROG-'].update(state)

    def update_class(self, class_name: str, class_num: int, num_classes: int, total_num_it: int):
        self.window['-CLASS-TEXT-'].update(f"Class: {class_name} ({class_num}/{num_classes})")
        self.window['-PROG-'].update_bar(0, total_num_it)

    def upload_dataset(self, top_dir) -> Optional[Dataset]:
        self.__switch_layout([[self.text("Upload new dataset")],
                              [self.text("Choose a csv file:"), self.input(key="-IN-"), self.browse("Browse", target='-IN-')],
                              [self.text("Choose a description file (optional):"), self.input(key="-IN-DESCR-"), self.browse("Browse", target='-IN-DESCR-')],
                              [self.text("Name of your dataset: "), self.input(key="-NAME-")],
                              [self.text("Name of the target variable: "), self.input(key="-TARGET-")],
                              [self.button("Upload", key='-UPLOAD-'), self.button("Cancel", key="-CANCEL-")]])

        while True:
            event, values = self.window.read()
            if event == sg.WIN_CLOSED or event == '-CANCEL-':
                return
            if event == '-UPLOAD-':
                try:
                    if len(values['-IN-DESCR-']) > 0:
                        dataset = Dataset.create_from_file(values['-IN-'], values['-TARGET-'], values['-NAME-'],
                                                           top_dir, values['-IN-DESCR-'])
                    else:
                        dataset = Dataset.create_from_file(values['-IN-'], values['-TARGET-'], values['-NAME-'],
                                                           top_dir)
                    return dataset
                except ValueError as e:
                    layout = [[sg.Text(e.args[0])], [sg.Button("OK")]]
                    error_window = sg.Window(title="Error while uploading dataset", layout=layout, margins=(100, 50))
                    error_window.read()
                    error_window.close()

    def __switch_layout(self, layout):
        self.layout = layout
        self.layout.append([sg.VPush()])
        self.layout.insert(0, [sg.VPush()])
        self.window.close()
        self.window = sg.Window(title="Prism", layout=self.layout, size=(1000, 800), element_justification='c',
                                finalize=True)

    def __rules_eval_list(self, rules_eval: List[RuleEval]) -> List[List[str]]:
        return [[f"{r.coverage:3.2f}", f"{r.precision:3.2f}", r.rule] for r in rules_eval]

    def button(self, text, **kwargs):
        return sg.Button(text, **kwargs, font=(self.FONT, self.TEXT_SIZE))

    def input(self, **kwargs):
        return sg.Input(**kwargs, font=(self.FONT, self.TEXT_SIZE))

    def browse(self, text="Browse", **kwargs):
        return sg.FileBrowse(text, **kwargs, font=(self.FONT, self.TEXT_SIZE))

    def h1(self, text, **kwargs):
        return sg.Text(text, **kwargs, font=(self.FONT, self.H1_SIZE))

    def h2(self, text, **kwargs):
        return sg.Text(text, **kwargs, font=(self.FONT, self.H2_SIZE))

    def text(self, text, **kwargs):
        return sg.Text(text, **kwargs, font=(self.FONT, self.TEXT_SIZE))
