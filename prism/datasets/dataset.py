import json
import os.path
import shutil
from typing import List

import pandas as pd

from datasets.preprocessing import DataPreprocessor
from rules.rule import Rule


class Dataset:
    def __init__(self, dirname: str, y_name: str, name: str, train: pd.DataFrame, test: pd.DataFrame, binning_info=None):
        self.dirname = dirname
        self.y_name = y_name
        self.name = name
        self.train, self.test = train, test
        self.num_att = len(self.train.columns) - 1
        self.num_targ = self.train[self.y_name].nunique()
        self.binning_info = binning_info

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
    def rules_eval_filename(self):
        return f"{self.dirname}/rules_eval.csv"

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
    def create_from_file(cls, source_filename: str, y_name: str, name: str, top_dir: str, rules_file: str = None):
        if not os.path.isfile(source_filename):
            raise ValueError(f"The file {source_filename} doesn't exist!")

        dirname = f"{top_dir}/{name.replace(' ', '_')}"
        if os.path.isdir(dirname):
            raise ValueError(f"Dataset directory {dirname}/ already exists! Please, select different dataset name.")
        os.mkdir(dirname)

        df = pd.read_csv(source_filename)
        if y_name not in df.columns:
            os.rmdir(dirname)
            raise ValueError(f"Target variable {y_name} not found in the dataset.")

        if rules_file is not None:
            if not os.path.isfile(rules_file):
                os.rmdir(dirname)
                raise ValueError(f"Rules file {rules_file} doesn't exist!")
            try:
                rules = []
                with open(rules_file) as f:
                    lines = json.loads(f.readline())["rules"]
                    for line in lines:
                        rules.append(Rule(line["cl"], line["operands"]))
            except Exception as e:
                os.rmdir(dirname)
                raise ValueError(f"Rules file isn't valid, error:\n{e}")
            attributes = set([att for r in rules for att in list(r.operands.keys())])
            wrong_att = [att for att in attributes if att not in df.columns]
            if len(wrong_att) > 0:
                os.rmdir(dirname)
                raise ValueError(f"Rules contain attributes that aren't present in the dataset!\n"
                                 f"Invalid attributes: {', '.join(wrong_att)}")
            shutil.copyfile(rules_file, f"{dirname}/rules.json")

        prep = DataPreprocessor(df, y_name)
        prep.apply_binning()
        train, test = prep.get_train_test()

        train.to_csv(f"{dirname}/train.csv", index=False)
        test.to_csv(f"{dirname}/test.csv", index=False)

        config = {"name": name, "y_name": y_name, "binning_info": prep.binning_info}
        with open(f"{dirname}/config", "w") as f:
            f.write(json.dumps(config))

        return cls(dirname, y_name, name, train, test, prep.binning_info)

    @classmethod
    def load_from_storage(cls, dirname: str):
        if not os.path.isdir(dirname):
            raise ValueError(f"Directory {dirname} doesn't exist!")
        if not os.path.isfile(f"{dirname}/config"):
            raise ValueError(f"Directory {dirname} isn't valid dataset repository, there is no config file.")
        if not os.path.isfile(f"{dirname}/train.csv"):
            raise ValueError(f"Directory {dirname} isn't valid dataset repository, training data are missing.")
        if not os.path.isfile(f"{dirname}/test.csv"):
            raise ValueError(f"Directory {dirname} isn't valid dataset repository, testing data are missing.")

        with open(f"{dirname}/config", "r") as f:
            config = json.loads(f.read())

        train = pd.read_csv(f"{dirname}/train.csv")
        test = pd.read_csv(f"{dirname}/test.csv")

        return cls(dirname, config["y_name"], config["name"], train, test, config["binning_info"])
