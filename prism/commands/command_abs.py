from abc import abstractmethod, ABC
from typing import List


class Command(ABC):
    def __init__(self, name, description):
        self.name = name
        self.description = description

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
    def run(self):
        return False
