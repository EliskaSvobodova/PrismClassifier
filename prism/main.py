import logging

from dataset import Dataset
from prism import Prism
from visualization import print_rules


if __name__ == '__main__':
    logging.basicConfig(level=logging.WARNING)

    # data = Dataset("data/lenses", "data.csv", "lenses")
    data = Dataset("data/mobile_prices", "train.csv", "price_range")
    logging.info("Data obtained\n\n")

    prism = Prism()
    # prism.fit(data.X_train, data.y_train)
    # prism.save_rules(data.rules_filename)
    prism.load_rules(data.rules_filename)
    print_rules(prism.rules)
    y_obt = prism.classify(data.X_test)
    diff = data.y_test.compare(y_obt)
    print(f"\nAccuracy: {(len(data.X_test) - len(diff)) / len(data.X_test)}")
