from typing import Dict, List

import pandas as pd

from command_selection import Command
from prism import Prism
from rule import Rule
from ui import show_rules, show_rules_evaluation


class ShowRulesCommand(Command):
    def __init__(self, args: Dict, name, description):
        super().__init__(name, description)
        self.rules: List[Rule] = args['rules']

    def run(self):
        show_rules(self.rules)
        return True


class EvaluateCommand(Command):
    def __init__(self, args: Dict, name, description):
        super().__init__(name, description)
        self.X_test: pd.DataFrame = args['X_test']
        self.y_test: pd.Series = args['y_test']
        self.prism: Prism = args['prism']

    def run(self):
        y_obt = self.prism.classify(self.X_test)
        diff = self.y_test.compare(y_obt)
        show_rules_evaluation((len(self.X_test) - len(diff)) / len(self.X_test))
        return True


class ExitCommand(Command):
    def run(self):
        return False
