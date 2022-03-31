from typing import List

import pandas as pd

from commands.command_abs import Command
from prism import Prism
from rules.rule import Rule


class ShowRulesCliCom(Command):
    """
    Show a list of all rules
    """

    def __init__(self, rules: List[Rule], name, description):
        super().__init__(name, description)
        self.rules: List[Rule] = rules

    def run(self):
        print("Rules:")
        for r in self.rules:
            print(f"{r.query()}  -->  {r.cl}")
        print()
        return True


class EvaluateModelCliCom(Command):
    """
    Make a classification on test dataset and show the accuracy
    """

    def __init__(self, prism: Prism, X_test: pd.DataFrame, y_test: pd.Series, name, description):
        super().__init__(name, description)
        self.X_test: pd.DataFrame = X_test
        self.y_test: pd.Series = y_test
        self.prism: Prism = prism

    def run(self):
        d_eval = self.prism.evaluate_dataset(self.X_test, self.y_test)
        print("Model evaluation on selected dataset:")
        print(f"Accuracy: {d_eval.accuracy}")
        return True


class EvaluateRulesCliCom(Command):
    """
    Show list of rules with their coverages and accuracies on test dataset (apply each rule on the test dataset)
    """

    def __init__(self, prism: Prism, X_test: pd.DataFrame, y_test: pd.Series, name, description):
        super().__init__(name, description)
        self.X_test: pd.DataFrame = X_test
        self.y_test: pd.Series = y_test
        self.prism: Prism = prism

    def run(self) -> bool:
        rules_eval = self.prism.evaluate_rules(self.X_test, self.y_test)
        print(f" Coverage | Precision | Rule")
        print(f"----------+-----------+-----")
        for rule_eval in sorted(rules_eval, key=lambda r: (r.coverage, r.precision), reverse=True):
            print(f"   {rule_eval.coverage:3.2f}   |    {rule_eval.precision:3.2f}   | {rule_eval.rule}")
        return True
