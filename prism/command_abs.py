from abc import abstractmethod, ABC
from typing import List


class Command(ABC):
    @property
    @abstractmethod
    def name(self):
        pass

    @property
    @abstractmethod
    def description(self):
        pass

    @abstractmethod
    def run(self) -> bool:
        """
        Execute command, return bool value whether the command selection loop should continue
        """
        pass


class CommandSelection:
    def __init__(self):
        self.commands: List[Command] = []

    def add_command(self, command: Command):
        self.commands.append(command)


class ExitCommand(Command):
    @property
    def name(self):
        return "Exit"

    @property
    def description(self):
        return "exit the application"

    def run(self):
        return False


class BackCommand(Command):
    @property
    def name(self):
        return "Back"

    @property
    def description(self):
        return "return to the previous menu"

    def run(self) -> bool:
        return False
