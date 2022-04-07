import logging
import random
from typing import Dict

import pandas as pd


class Rule:
    def __init__(self, cl, operands: Dict = None):
        if operands is None:
            operands = {}
        self.operands = operands
        self.cl = cl

    def match(self, X_y: pd.DataFrame) -> pd.DataFrame:
        if len(self.operands) > 0:
            return X_y.query(self.query())
        else:
            return X_y

    def class_match(self, X_y) -> pd.DataFrame:
        return X_y[X_y['y'] == self.cl]

    def precision(self, X_y):
        match = self.match(X_y)
        class_match = self.class_match(match)
        if len(match) == 0:
            return 0
        return len(class_match) / len(match)

    def available_attributes(self, X_y):
        att = list(X_y.drop('y', axis=1).columns.values) - self.operands.keys()
        return att

    def is_perfect(self, X_y):
        match = self.match(X_y)
        num_mistakes = len(match[match['y'] != self.cl])
        logging.info(f"num of matches: {len(match)}, num of mistakes: {num_mistakes}, of {len(X_y)} instances")
        return num_mistakes == 0

    def not_matched_inst(self, X_y):
        if len(self.operands) > 0:
            return X_y.query(f"not ({self.query()})")
        else:
            return X_y

    def add_operand(self, X_y):
        new_rules = self.__generate_new_rules(X_y)
        eval_rules = [(r, r.precision(X_y), len(r.class_match(r.match(X_y)))) for r in new_rules]
        sorted_rules = sorted(eval_rules, key=lambda x: (x[1], x[2], bool(random.getrandbits(1))), reverse=True)
        eval_str = '\n'.join(f"{t[0]} : {t[1]:.2f}" for t in sorted_rules)
        logging.info(f"Add operand [rule - precision]:\n{eval_str}")
        self.operands = sorted_rules[0][0].operands

    def query(self):
        def equal(att, val):
            if type(val) is str:
                return f"`{att}` == '{val}'"
            else:
                return f"`{att}` == {val}"
        return ' & '.join(equal(att, val) for att, val in self.operands.items())

    def toJson(self):
        def encode(x):
            if type(x) is str:
                return f'"{x}"'
            else:
                return str(x)
        return '{"cl":' + encode(self.cl) + ', "operands":{' + ','.join([f'"{att}": {encode(val)}' for att, val in self.operands.items()]) + '}}'

    def __generate_new_rules(self, X_y):
        new_rules = []
        for att in self.available_attributes(X_y):
            for val in X_y[att].unique():
                new_rules.append(Rule(self.cl, {**self.operands, **{att: val}}))
        return new_rules

    def __str__(self):
        return ' ∧ '.join([f"{att} = {val}" for att, val in self.operands.items()]) + f"  ⇒  {self.cl}"

    def __repr__(self):
        return "{'cl':" + str(self.cl) + "," + str(self.operands) + "}"
