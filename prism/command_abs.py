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
        return "exit"

    @property
    def description(self):
        return "exit current menu and return to the previous one / exit the application"

    def run(self):
        return False
