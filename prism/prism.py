import logging
from abc import abstractmethod, ABC
from typing import List

import pandas as pd

from datasets.dataset_eval import DatasetEval
from rules.rule import Rule
from rules.rule_eval import RuleEval


class FitProgressSubscriber(ABC):
    @abstractmethod
    def update_progress(self, state: int):
        pass

    @abstractmethod
    def update_class(self, class_name: str, class_num: int, num_classes: int, total_num_it: int):
        pass


class FitProgressPublisher:
    def __init__(self):
        self.subscribers: List[FitProgressSubscriber] = []

    def subscribe(self, s: FitProgressSubscriber):
        self.subscribers.append(s)

    def unsubscribe(self, s: FitProgressSubscriber):
        self.subscribers.remove(s)

    def notify_progress(self, state: int):
        for s in self.subscribers:
            s.update_progress(state)

    def notify_new_class(self, class_name: str, class_num: int, num_classes: int, total_num_it: int):
        for s in self.subscribers:
            s.update_class(class_name, class_num, num_classes, total_num_it)


class Prism(FitProgressPublisher):
    def __init__(self):
        super().__init__()
        self._rules: List[Rule] = []
        self.classes = []

    @property
    def rules(self):
        return self._rules

    @rules.setter
    def rules(self, value: List[Rule]):
        self._rules = value
        self.classes = list(set(r.cl for r in self._rules))

    def fit(self, X: pd.DataFrame, y: pd.Series):
        X_y = X.copy()
        X_y['y'] = y
        rules = []
        classes = y.unique()

        for i, cl in enumerate(classes):
            cl_inst = X_y[y == cl]
            inst = X_y
            self.notify_new_class(cl, i+1, len(classes), len(cl_inst))
            total_cl_inst = len(cl_inst)
            while len(cl_inst) > 0:
                rule = Rule(cl)
                while len(rule.available_attributes(X_y)) > 0 and not rule.is_perfect(X_y):
                    rule.add_operand(inst)
                logging.info(f"Final rule: {rule}\n")
                cl_inst = rule.not_matched_inst(cl_inst)
                inst = rule.not_matched_inst(inst)
                rules.append(rule)
                self.notify_progress(total_cl_inst - len(cl_inst))
                logging.warning(f"Class: {cl} ({i+1}/{len(classes)}), {len(cl_inst)} remaining")
            logging.info(f"Class {cl} completed\n")
        self.rules = rules

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

    def evaluate_dataset(self, X_test: pd.DataFrame, y_test: pd.Series):
        y_obt = self.classify(X_test)
        diff = y_test.compare(y_obt)
        return DatasetEval((len(X_test) - len(diff)) / len(X_test))

    def evaluate_rules(self, X_test: pd.DataFrame, y_test: pd.Series) -> List[RuleEval]:
        y_val_counts = y_test.value_counts()
        results: List[RuleEval] = []
        for rule in self.rules:
            X_match = rule.match(X_test)
            match = X_match.join(y_test, how='inner')
            correct_match = match[match[y_test.name] == rule.cl]
            coverage = len(correct_match) / y_val_counts[rule.cl] if y_val_counts[rule.cl] != 0 else 0
            precision = (len(correct_match) / len(match)) if len(match) != 0 else 0
            results.append(RuleEval(precision, coverage, rule))
        return results
