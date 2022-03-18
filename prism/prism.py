import json
import logging
from typing import List

import pandas as pd

from rule import Rule


class Prism:
    def __init__(self):
        self.rules: List[Rule] = []
        self.classes = []

    def fit(self, X: pd.DataFrame, y: pd.Series):
        X_y = X.copy()
        X_y['y'] = y
        self.rules = []
        self.classes = y.unique()

        for i, cl in enumerate(self.classes):
            cl_inst = X_y[y == cl]
            inst = X_y
            while len(cl_inst) > 0:
                rule = Rule(cl)
                while len(rule.available_attributes(X_y)) > 0 and not rule.is_perfect(X_y):
                    rule.add_operand(inst)
                logging.info(f"Final rule: {rule}\n")
                cl_inst = rule.not_matched_inst(cl_inst)
                inst = rule.not_matched_inst(inst)
                self.rules.append(rule)
                logging.warning(f"Class: {cl} ({i+1}/{len(self.classes)}), {len(cl_inst)} remaining")
            logging.info(f"Class {cl} completed\n")

    def classify(self, X: pd.DataFrame):
        classes = {cl: [] for cl in self.classes}
        y = {idx: [] for idx in X.index}
        for r in self.rules:
            match = r.match(X)
            classes[r.cl].extend(match.index)
            for idx, m in match.iterrows():
                y[idx].append(r.cl)

        def get_y(row):
            y_list = y[row.name]
            if len(y_list) == 0:
                return None
            return max(set(y[row.name]), key=y[row.name].count)
        return X.apply(get_y, axis=1)

    def save_rules(self, filename: str):
        with open(filename, "w") as f:
            f.write("{\"rules\": [" + ','.join([r.toJson() for r in self.rules]) + "]}")

    def load_rules(self, filename: str):
        self.rules = []
        with open(filename, "r") as f:
            lines = json.loads(f.readline())["rules"]
            for line in lines:
                cl = line["cl"]
                op = line["operands"]
                r = Rule(line["cl"], line["operands"])
                self.rules.append(Rule(line["cl"], line["operands"]))
        self.classes = set(r.cl for r in self.rules)
