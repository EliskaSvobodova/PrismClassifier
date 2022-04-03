import json
import os.path
import shutil
from typing import List

import pandas as pd

from datasets.preprocessing import get_prep_data
from rules.rule import Rule


class Dataset:
    def __init__(self, dirname: str, y_name: str, name: str, train: pd.DataFrame, test: pd.DataFrame):
        self.dirname = dirname
        self.y_name = y_name
        self.name = name
        self.train, self.test = train, test
        self.num_att = len(self.train.columns) - 1
        self.num_targ = self.train[self.y_name].nunique()

    @property
    def rules_filename(self):
        return f"{self.dirname}/rules.json"

    @property
    def rules_available(self):
        if os.path.isfile(self.rules_filename):
            return True
        else:
            return False

    @property
    def X_train(self):
        return self.train.drop(self.y_name, axis=1)

    @property
    def X_test(self):
        return self.test.drop(self.y_name, axis=1)

    @property
    def y_train(self):
        return self.train[self.y_name]

    @property
    def y_test(self):
        return self.test[self.y_name]

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

    @classmethod
    def create_from_file(cls, source_filename: str, y_name: str, name: str, top_dir: str, description_file: str = None):
        if not os.path.isfile(source_filename):
            raise ValueError(f"The file {source_filename} doesn't exist!")
        if not source_filename.endswith(".csv"):
            raise ValueError(f"The file isn't in csv format!")

        dirname = f"{top_dir}/{name.replace(' ', '_')}"
        if os.path.isdir(dirname):
            raise ValueError(f"Dataset directory {dirname}/ already exists! Please, select different dataset name.")
        os.mkdir(dirname)

        if description_file is not None:
            if not os.path.isfile(description_file):
                raise ValueError(f"Description file {description_file} doesn't exist!")
            shutil.copyfile(description_file, f"{dirname}/description")

        train, test = get_prep_data(source_filename, y_name)
        train.to_csv(f"{dirname}/train.csv")
        test.to_csv(f"{dirname}/test.csv")

        return cls(dirname, y_name, name, train, test)
