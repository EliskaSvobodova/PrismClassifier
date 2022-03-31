from rules.rule import Rule


class RuleEval:
    def __init__(self, precision: float, coverage: float, rule: Rule):
        self.precision = precision
        self.coverage = coverage
        self.rule = rule
