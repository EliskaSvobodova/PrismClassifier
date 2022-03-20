from typing import List, Optional

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
        print(f"{i+1}) {c.name} = {c.description}")
    choice = input_number(f"Select action (number from 1 to {len(command_sel.commands)}): ",
                          1, len(command_sel.commands))
    while not choice:
        choice = input_number(f"Select action (number from 1 to {len(command_sel.commands)}): ",
                              1, len(command_sel.commands))
    return command_sel.commands[choice - 1]


def show_rules_evaluation(accuracy: float):
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


def horizontal_line():
    print("----------------------------------------------------")


def print_ind(s: str, indent=2):
    """
    Print string with indent
    """
    print((' ' * indent) + s)
