from abc import ABC, abstractmethod
from typing import List, Optional

from commands.command_abs import CommandSelection, Command
from datasets.dataset import Dataset
from datasets.datasets_manager import DatasetsManager
from prism import Prism, FitProgressSubscriber


class UserInterface(FitProgressSubscriber):
    TITLE = "PRISM"
    SUBTITLE = "rule-based classifier"
    GUIDE = "How to use:\n" \
            "1) select dataset to work on\n" \
            "2) extract new rules / load rules\n" \
            "3) analyse rules"

    @abstractmethod
    def welcome_page(self, command_selection: CommandSelection) -> Command:
        pass

    @abstractmethod
    def select_dataset(self, manager: DatasetsManager) -> Dataset:
        pass

    @abstractmethod
    def should_load_rules(self) -> bool:
        pass

    @abstractmethod
    def analyse_dataset(self, prism: Prism, dataset: Dataset):
        pass

    @abstractmethod
    def fit_rules(self):
        pass





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
