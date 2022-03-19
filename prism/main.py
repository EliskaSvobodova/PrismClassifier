import logging

from dataset import Dataset
from datasets_manager import DatasetsManager
from prism import Prism
from ui import welcome_page, select_dataset


def init_datasets_manager():
    dm = DatasetsManager()
    dm.add_dataset(Dataset("data/mobile_prices", "train.csv", "price_range", "Mobile prices"))
    dm.add_dataset(Dataset("data/lenses", "data.csv", "lenses", "Lenses"))
    dm.add_dataset(Dataset("data/breast_cancer", "breast-cancer.data", "Class", "Breast cancer"))
    dm.add_dataset(Dataset("data/stress", "stress.csv", "sl", "Stress level"))
    dm.add_dataset(Dataset("data/wine", "WineQT.csv", "quality", "Wine quality"))
    return dm


if __name__ == '__main__':
    logging.basicConfig(level=logging.WARNING)

    welcome_page()
    datasets_manager = init_datasets_manager()
    data = select_dataset(datasets_manager)

    prism = Prism()
    # prism.fit(data.X_train, data.y_train)
    # prism.save_rules(data.rules_filename)
    # prism.load_rules(data.rules_filename)
    # print_rules(prism.rules)
    # y_obt = prism.classify(data.X_test)
    # diff = data.y_test.compare(y_obt)
    # print(f"\nAccuracy: {(len(data.X_test) - len(diff)) / len(data.X_test)}")
