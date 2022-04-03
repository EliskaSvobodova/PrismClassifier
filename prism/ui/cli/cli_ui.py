from typing import Optional

from prettytable import PrettyTable

from command_abs import CommandSelection, Command, ExitCommand
from datasets.dataset import Dataset
from datasets.datasets_manager import DatasetsManager
from prism import Prism
from ui.cli.cli_analysis_com import ShowRulesCliCom, EvaluateModelCliCom, EvaluateRulesCliCom
from ui.cli.cli_progress_bar import ProgressBar
from ui.ui import UserInterface


class CliUi(UserInterface):
    def __init__(self):
        self.fit_progress_bar: Optional[ProgressBar] = None

    def welcome_page(self, command_selection: CommandSelection) -> Command:
        print(f"\n+{'-' * (len(self.TITLE) + 2)}+")
        print(f"| {self.TITLE} |")
        print(f"+{'-' * (len(self.TITLE) + 2)}+   ... {self.SUBTITLE}")
        return self.__select_command("Main menu", command_selection)

    def select_dataset(self, manager: DatasetsManager) -> Dataset:
        table = PrettyTable()
        table.field_names = ["index", "name", "# instances", "# attributes", "# targets", "rules available"]

        for i, d in enumerate(manager.datasets_list):
            table.add_row([i+1, d.name, d.num_inst, d.num_att, d.num_targ, d.rules_available])

        print(self.SELECT_DATASET_TITLE)
        print(table)
        selected = self.__input_number("Index of the selected dataset: ", 1, len(manager.datasets_list))
        while not selected:
            selected = self.__input_number(
                f"Index of the selected dataset (a number from 1 to {len(manager.datasets_list)}): ",
                1, len(manager.datasets_list))
        return manager.datasets_list[selected - 1]

    def should_load_rules(self) -> bool:
        answer = input(self.SHOULD_LOAD_DATASET + "\n[yes/no] : ")
        answer = answer.lower()
        while answer not in ["yes", "no"]:
            answer = input(self.SHOULD_LOAD_DATASET + " Please, type \"yes\" or \"no\": ")
            answer = answer.lower()
        if answer == "yes":
            return True
        return False

    def analyse_dataset(self, prism: Prism, dataset: Dataset):
        command_selection = self.__init_rules_analysis_com_sel(prism, dataset)
        command = self.__select_command(self.RULES_ANALYSIS_TITLE, command_selection)
        while command.run():
            self.__horizontal_line()
            command = self.__select_command(self.RULES_ANALYSIS_TITLE, command_selection)

    def fit_rules(self):
        print(self.FIT_RULES_TEXT)

    def update_progress(self, state: int):
        self.fit_progress_bar.update(state)

    def update_class(self, class_name: str, class_num: int, num_classes: int, total_num_it: int):
        self.fit_progress_bar = ProgressBar(total_num_it, f"Class: {class_name} ({class_num}/{num_classes})")

    def upload_dataset(self, top_dir: str) -> Dataset:
        # TODO: do this
        pass

    def __init_rules_analysis_com_sel(self, prism, dataset):
        cs = CommandSelection()
        cs.add_command(ShowRulesCliCom(prism.rules))
        cs.add_command(EvaluateModelCliCom(prism, dataset.X_test, dataset.y_test))
        cs.add_command(EvaluateRulesCliCom(prism, dataset.X_test, dataset.y_test))
        cs.add_command(ExitCommand())
        return cs

    def __select_command(self, header: str, command_sel: CommandSelection) -> Command:
        self.__horizontal_line()
        print(header + ":")
        for i, c in enumerate(command_sel.commands):
            print(f"{i + 1}) {c.name} = {c.description}")
        choice = self.__input_number(f"Select action (number from 1 to {len(command_sel.commands)}): ",
                                     1, len(command_sel.commands))
        while not choice:
            choice = self.__input_number(f"Select action (number from 1 to {len(command_sel.commands)}): ",
                                         1, len(command_sel.commands))
        return command_sel.commands[choice - 1]

    def __print_ind(self, s: str, indent=2):
        """
        Print string with indent
        """
        print((' ' * indent) + s)

    def __horizontal_line(self):
        print("----------------------------------------------------")

    def __input_number(self, prompt, min_val, max_val) -> Optional[int]:
        selected = input(prompt)
        try:
            selected = int(selected)
        except ValueError:
            return None
        if selected not in range(min_val, max_val + 1):
            return None
        return selected
