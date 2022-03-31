import json
import os.path
from typing import List

from datasets.preprocessing import get_prep_data
from rules.rule import Rule


class Dataset:
    def __init__(self, dirname, filename, y_name, name):
        self.dirname = dirname
        self.filename = filename
        self.y_name = y_name
        self.X_train, self.X_test, self.y_train, self.y_test = get_prep_data(f"{self.dirname}/{self.filename}", self.y_name)
        self.name = name
        self.num_inst = len(self.X_train) + len(self.X_test)
        self.num_att = len(self.X_train.columns)
        self.num_targ = self.y_train.nunique()

    @property
    def rules_filename(self):
        return f"{self.dirname}/rules.json"

    @property
    def rules_available(self):
        if os.path.isfile(self.rules_filename):
            return True
        else:
            return False

    def save_rules(self, rules: List[Rule]):
        with open(self.rules_filename, "w") as f:
            f.write("{\"rules\": [" + ','.join([r.toJson() for r in rules]) + "]}")

    def load_rules(self) -> List[Rule]:
        rules = []
        with open(self.rules_filename, "r") as f:
            lines = json.loads(f.readline())["rules"]
            for line in lines:
                rules.append(Rule(line["cl"], line["operands"]))
        return rules
