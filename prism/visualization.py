from typing import List

from rule import Rule


def print_rules(rules: List[Rule]):
    print("Rules:")
    for r in rules:
        print(f"{r.query()}  -->  {r.cl}")
    print()
