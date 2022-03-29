from typing import Dict, List

import pandas as pd

from command_abs import Command
from prism import Prism
from rules.RuleEval import RuleEval
from rules.rule import Rule
from ui.ui import show_rules, show_model_evaluation, show_rules_eval


class ShowRulesCommand(Command):
    """
    Show a list of all rules
    """

    def __init__(self, args: Dict, name, description):
        super().__init__(name, description)
        self.rules: List[Rule] = args['rules']

    def run(self):
        show_rules(self.rules)
        return True


class EvaluateModelCommand(Command):
    """
    Make a classification on test dataset and show the accuracy
    """

    def __init__(self, args: Dict, name, description):
        super().__init__(name, description)
        self.X_test: pd.DataFrame = args['X_test']
        self.y_test: pd.Series = args['y_test']
        self.prism: Prism = args['prism']

    def run(self):
        y_obt = self.prism.classify(self.X_test)
        diff = self.y_test.compare(y_obt)
        show_model_evaluation((len(self.X_test) - len(diff)) / len(self.X_test))
        return True


class EvaluateRulesCommand(Command):
    """
    Show list of rules with their coverages and accuracies on test dataset (apply each rule on the test dataset)
    """

    def __init__(self, args: Dict, name, description):
        super().__init__(name, description)
        self.X_test: pd.DataFrame = args['X_test']
        self.y_test: pd.Series = args['y_test']
        self.prism: Prism = args['prism']

    def run(self) -> bool:
        y_val_counts = self.y_test.value_counts()
        results = []
        for rule in self.prism.rules:
            X_match = rule.match(self.X_test)
            match = X_match.join(self.y_test, how='inner')
            correct_match = match[match[self.y_test.name] == rule.cl]
            coverage = len(correct_match) / y_val_counts[rule.cl] if y_val_counts[rule.cl] != 0 else 0
            precision = (len(correct_match) / len(match)) if len(match) != 0 else 0
            results.append(RuleEval(precision, coverage, rule))
        show_rules_eval(results)
        return True


class ExitCommand(Command):
    def run(self):
        return False
