import sys
from typing import List, Optional, Dict, Tuple

from prettytable import PrettyTable

from command_selection import CommandSelection, Command
from dataset import Dataset
from datasets_manager import DatasetsManager
from rule import Rule


def show_rules(rules: List[Rule]):
    print("Rules:")
    for r in rules:
        print(f"{r.query()}  -->  {r.cl}")
    print()


def show_rules_eval(rules_eval):
    print(f" Precision | Coverage | Rule")
    print(f"-----------+----------+-----")
    for rule, precision, coverage in rules_eval:
        print(f"    {precision:3.2f}   |   {coverage:3.2f}   | {rule}")


def welcome_page():
    print("+-------+\n| PRISM |\n+-------+   ... rule-based classifier")
    print("How to use:")
    print_ind("1) select dataset to work on")
    print_ind("2) extract new rules / load rules")
    print_ind("3) analyse rules")
    horizontal_line()


def select_dataset(manager: DatasetsManager):
    table = PrettyTable()
    table.field_names = ["index", "name", "# instances", "# attributes", "# targets", "rules available"]

    for i, d in enumerate(manager.datasets_list):
        table.add_row([i + 1, d.name, d.num_inst, d.num_att, d.num_targ, d.rules_available])

    print("Available datasets:")
    print(table)
    selected = input_number("Index of the selected dataset: ", 1, len(manager.datasets_list))
    while not selected:
        selected = input_number(f"Index of the selected dataset (a number from 1 to {len(manager.datasets_list)}): ",
                                1, len(manager.datasets_list))
    return manager.datasets_list[selected - 1]


def should_load_rules(dataset: Dataset):
    if dataset.rules_available:
        answer = input("This dataset has pre-computed rules, do you want to load them "
                       "(otherwise the rules will be computed again from the dataset)? [yes/no] ")
        answer = answer.lower()
        while answer not in ["yes", "no"]:
            answer = input("Do you want to load the pre-computed rules? Please, type \"yes\" or \"no\": ")
            answer = answer.lower()
        if answer == "yes":
            return True
    return False


def select_command(header: str, command_sel: CommandSelection) -> Command:
    horizontal_line()
    print(header + ":")
    for i, c in enumerate(command_sel.commands):
        print(f"{i + 1}) {c.name} = {c.description}")
    choice = input_number(f"Select action (number from 1 to {len(command_sel.commands)}): ",
                          1, len(command_sel.commands))
    while not choice:
        choice = input_number(f"Select action (number from 1 to {len(command_sel.commands)}): ",
                              1, len(command_sel.commands))
    return command_sel.commands[choice - 1]


def show_model_evaluation(accuracy: float):
    horizontal_line()
    print("Rules evaluation:")
    print(f"Accuracy: {accuracy}")


def loading_rules():
    print("Loading rules...")


def computing_rules():
    print("Computing rules from the dataset...")


def input_number(prompt, min_val, max_val) -> Optional[int]:
    selected = input(prompt)
    try:
        selected = int(selected)
    except ValueError:
        return None
    if selected not in range(min_val, max_val + 1):
        return None
    return selected


class ProgressBar:
    """
    Call in a loop to create terminal progress bar
    source: https://stackoverflow.com/questions/3173320/text-progress-bar-in-terminal-with-block-characters (modified)

    iteration   - Required  : current iteration (Int)
    total       - Required  : total iterations (Int)
    prefix      - Optional  : prefix string (Str)
    suffix      - Optional  : suffix string (Str)
    decimals    - Optional  : positive number of decimals in percent complete (Int)
    length      - Optional  : character length of bar (Int)
    fill        - Optional  : bar fill character (Str)
    printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """

    def __init__(self, total, prefix='', suffix='', decimals=1, length=100, fill='█', printEnd="\r"):
        self.iteration = 0
        self.total = total
        self.prefix = prefix
        self.suffix = suffix
        self.decimals = decimals
        self.length = length
        self.fill = fill
        self.printEnd = printEnd

    def update(self, iteration=None):
        if iteration is None:
            self.iteration += 1
        else:
            self.iteration = iteration
        percent = ("{0:." + str(self.decimals) + "f}").format(100 * (self.iteration / float(self.total)))
        filledLength = int(self.length * self.iteration // self.total)
        bar = self.fill * filledLength + '-' * (self.length - filledLength)
        print(f'\r{self.prefix} |{bar}| {percent}% {self.suffix}', end=self.printEnd, flush=True)
        # Print New Line on Complete
        if self.iteration == self.total:
            print()


def horizontal_line():
    print("----------------------------------------------------")


def print_ind(s: str, indent=2):
    """
    Print string with indent
    """
    print((' ' * indent) + s)
