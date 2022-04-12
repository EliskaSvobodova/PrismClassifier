from typing import List

import pandas as pd

from command_abs import Command
from prism import Prism
from rules.rule import Rule


class ShowRulesCliCom(Command):
    """
    Show a list of all rules
    """

    @property
    def name(self):
        return "show_rules"

    @property
    def description(self):
        return "show a list of obtained rules"

    def __init__(self, rules: List[Rule]):
        super().__init__()
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

    @property
    def name(self):
        return "evaluate model"

    @property
    def description(self):
        return "run classification on the test dataset and show result metrics"

    def __init__(self, prism: Prism, X_test: pd.DataFrame, y_test: pd.Series):
        super().__init__()
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

    @property
    def name(self):
        return "evaluate rules"

    @property
    def description(self):
        return "apply each of the rules to the test dataset and get their metrics"

    def __init__(self, prism: Prism, X_train: pd.DataFrame, y_train: pd.Series):
        super().__init__()
        self.X_train: pd.DataFrame = X_train
        self.y_train: pd.Series = y_train
        self.prism: Prism = prism

    def run(self) -> bool:
        rules_eval = self.prism.evaluate_rules(self.X_train, self.y_train)
        print(f" Coverage | Precision | Rule")
        print(f"----------+-----------+-----")
        for rule_eval in sorted(rules_eval, key=lambda r: (r.coverage, r.precision), reverse=True):
            print(f"   {rule_eval.coverage:3.2f}   |    {rule_eval.precision:3.2f}   | {rule_eval.rule}")
        return True
