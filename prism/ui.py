from typing import List

from prettytable import PrettyTable

from dataset import Dataset
from datasets_manager import DatasetsManager
from rule import Rule


def print_rules(rules: List[Rule]):
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
    return manager.datasets_list[int(selected) - 1]


def should_load_rules(dataset: Dataset):
    if dataset.rules_available:
        answer = input("This dataset has pre-computed rules, do you want to load them "
                       "(otherwise the rules will be computed again from the dataset)? [yes/no]")
        answer = answer.lower()
        while answer not in ["yes", "no"]:
            answer = input("Do you want to load the pre-computed rules? Please, type \"yes\" or \"no\": ")
            answer = answer.lower()
        if answer == "yes":
            return True
    return False


def loading_rules():
    print("Loading rules...")


def computing_rules():
    print("Computing rules from the dataset...")


def input_number(prompt, min_val, max_val):
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
