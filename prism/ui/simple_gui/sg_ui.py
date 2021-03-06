import sys
from typing import List, Optional, Dict

import PySimpleGUI as sg
import pandas as pd

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
    HINTS = [
        "You can sort the rules by a column value by clicking on the column's heading",
        f"Columns with too many values were binned,\n"
            f"if you want to see the mapping between originial values and the current numerical categories,\n"
            f"press 'Binning explanation' button",
        "'Accuracy all' = [number of correctly classified instances] / [number of all instances]\n"
            "'Accuracy classified' = [number of correctly classified instances] / [number of classified instances]\n"
            "(some instances might not fit any rule and therefore remain unclassified)"
    ]

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

        event, values = self.window.read()
        if event == sg.WIN_CLOSED:
            sys.exit()
        i = command_names.index(event)
        return command_selection.commands[i]

    def select_dataset(self, manager: DatasetsManager) -> Optional[Dataset]:
        datasets = [[i + 1, d.name, len(d.train) + len(d.test), d.num_att, d.num_targ, d.rules_available]
                    for i, d in enumerate(manager.datasets)]
        self.__switch_layout([[self.h2(self.SELECT_DATASET_TITLE)],
                              [sg.Table(headings=["index", "name", "# instances", "# attributes", "# targets",
                                                  "rules available"],
                                        values=datasets,
                                        key='-TABLE-', enable_click_events=True, font=(self.FONT, self.TEXT_SIZE))],
                              [self.text(self.FIT_RULES_TEXT, visible=False, key="-FIT-TEXT-")],
                              [self.text(f"Class: ", visible=False, key="-CLASS-TEXT-"),
                               sg.ProgressBar(100, orientation='h', size=(10, 10), visible=False, key="-PROG-", bar_color=("#6A759B", "#BDC7F1"))],
                              [self.button("Back", key="-BACK-")]])

        while True:
            event, values = self.window.read()
            if event == sg.WIN_CLOSED or event == '-BACK-':
                return
            if isinstance(event, tuple) and event[0] == "-TABLE-" and event[2][0] != -1:
                return manager.datasets[datasets[event[2][0]][0] - 1]
            if isinstance(event, tuple) and event[0] == "-TABLE-" and event[2][0] == -1:
                datasets = sorted(datasets, key=lambda d: d[event[2][1]])
                self.window['-TABLE-'].update(datasets)

    def should_load_rules(self) -> bool:
        layout = [[self.text(self.SHOULD_LOAD_DATASET)],
                  [sg.Push(), self.button("Yes", key="-YES-"), sg.Push(), self.button("No", key="-NO-"), sg.Push()]]
        pop_window = sg.Window(title="Load data", layout=layout, margins=(100, 50))
        event, values = pop_window.read()
        if event == "-YES-":
            pop_window.close()
            return True
        if event == "-NO-" or event == sg.WIN_CLOSED:
            pop_window.close()
            return False

    def analyse_dataset(self, prism: Prism, dataset: Dataset):
        self.__switch_layout([[self.h2(self.RULES_ANALYSIS_TITLE)],
                              [self.text("Accuracy: [calculating]    Coverage: [calculating]", key='-ACCURACY-'),
                               self.button("Binning explanation", key='-BINNING-'),
                               self.button("Usage hints", key='-SHOW-HINTS-')],
                              [sg.Table(headings=["Coverage", "Precision", "Rule"], enable_click_events=True,
                                        values=[["-", "-", r] for r in prism.rules], vertical_scroll_only=False,
                                        auto_size_columns=False, justification='left', expand_y=True,
                                        col_widths=[10, 10, int(max(len(repr(r)) for r in prism.rules) * 0.8)],
                                        key="-TABLE-", font=(self.FONT, self.TEXT_SIZE))],
                              [self.button("Back", key="-BACK-")]])

        self.window.perform_long_operation(lambda: prism.evaluate_dataset(dataset.X_test, dataset.y_test),
                                           '-EVAL-MODEL-DONE-')
        self.window.perform_long_operation(lambda: prism.evaluate_rules(dataset.X_train, dataset.y_train),
                                           '-EVAL-RULES-DONE-')

        hints_window, bin_window = None, None
        rules_eval = None
        hint_i = 0

        while True:
            window, event, values = sg.read_all_windows()
            if event == sg.WIN_CLOSED or event == '-BACK-':
                if window == hints_window:
                    hints_window.close()
                    hints_window = None
                elif window == bin_window:
                    bin_window.close()
                    bin_window = None
                else:
                    if hints_window is not None:
                        hints_window.close()
                    if bin_window is not None:
                        bin_window.close()
                    return
            if event == '-EVAL-MODEL-DONE-':
                d_eval = values[event]
                self.window['-ACCURACY-'].update(f"Accuracy all: {d_eval.accuracy_all:.4f}    Accuracy classified: {d_eval.accuracy_classified:.4f}    Coverage: {d_eval.coverage:.4f}")
            if event == '-EVAL-RULES-DONE-':
                rules_eval = values[event]
                self.window['-TABLE-'].update(self.__rules_eval_list(rules_eval))
                self.__save_rules_eval(rules_eval, dataset)
            if isinstance(event, tuple) and event[0] == "-TABLE-" and event[2][0] == -1 and rules_eval is not None:
                if event[2][1] == 0:
                    rules_eval = sorted(rules_eval, key=lambda r: (r.coverage, r.precision), reverse=True)
                    self.window['-TABLE-'].update(self.__rules_eval_list(rules_eval))
                elif event[2][1] == 1:
                    rules_eval = sorted(rules_eval, key=lambda r: (r.precision, r.coverage), reverse=True)
                    self.window['-TABLE-'].update(self.__rules_eval_list(rules_eval))
            if event == '-SHOW-HINTS-':
                hints_window = self.create_hints_window()
            if event == '-HINTS-NEXT-':
                hint_i = (hint_i + 1) % len(self.HINTS)
                window['-HINTS-HINT-'].update(self.HINTS[hint_i])
            if event == '-BINNING-':
                bin_window = self.create_binning_info_window(dataset.binning_info)

    def create_hints_window(self):
        hint_i = 0
        layout = [[self.h2("Hints")],
                  [self.text(self.HINTS[hint_i], key='-HINTS-HINT-')],
                  [self.button("Next hint", key="-HINTS-NEXT-")]]
        return sg.Window("Prism - Hints", layout=layout, margins=(100, 50), finalize=True)

    def create_binning_info_window(self, info: Dict):
        if len(info) == 0:
            layout = [[self.h2("Binning information")],
                      [self.text("No binning was necessary")]]
        else:
            num_cat = max(len(i) for att, i in info.items())
            layout = [[self.h2("Binning information")],
                      [self.text("Attributes with too many values were binned,\n"
                                 "here you can see a mapping between the original values and the numerical categories")],
                      [sg.Table(headings=["Attribute"] + [f"Category {c}" for c in range(num_cat)],
                                enable_click_events=True, values=[[att] + list(i.values()) for att, i in info.items()],
                                key="-BIN-TABLE-", font=(self.FONT, self.TEXT_SIZE), justification='center')]]
        return sg.Window("Prism - Binning information", layout=layout, margins=(100, 50), finalize=True)

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
                              [self.text("Dataset file [csv]: "), self.input(key="-DATA-"), self.browse("Browse")],
                              [self.text("Rules file [json] (optional): "), self.input(key="-RULES-"), self.browse("Browse")],
                              [self.text("Name of your dataset: "), self.input(key="-NAME-")],
                              [self.text("Name of the target variable: "), self.input(key="-TARGET-")],
                              [self.button("Upload", key='-UPLOAD-'), self.button("Cancel", key="-CANCEL-")]])

        while True:
            event, values = self.window.read()
            if event == sg.WIN_CLOSED or event == '-CANCEL-':
                return
            if event == '-UPLOAD-':
                try:
                    if len(values["-RULES-"]) > 0:
                        dataset = Dataset.create_from_file(values['-DATA-'], values['-TARGET-'], values['-NAME-'],
                                                           top_dir, values['-RULES-'])
                    else:
                        dataset = Dataset.create_from_file(values['-DATA-'], values['-TARGET-'], values['-NAME-'],
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

    def __save_rules_eval(self, rules_eval: List[RuleEval], dataset: Dataset):
        df = pd.DataFrame([[r.coverage, r.precision, r.rule.cl, ' ??? '.join([f"{att} = {val}" for att, val in r.rule.operands.items()])] for r in rules_eval],
                          columns=['Coverage', 'Precision', 'Class', 'Operands'])
        df.to_csv(dataset.rules_eval_filename, index=False)

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
