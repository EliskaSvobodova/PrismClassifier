import logging

from application import Application
from datasets.dataset import Dataset
from datasets.datasets_manager import DatasetsManager
from ui.cli.cli_ui import CliUi
from ui.simple_gui.sg_ui import SimpleGui


def init_datasets_manager():
    dm = DatasetsManager()
    dm.add_dataset(Dataset("data/mobile_prices", "train.csv", "price_range", "Mobile prices"))
    dm.add_dataset(Dataset("data/lenses", "data.csv", "lenses", "Lenses"))
    dm.add_dataset(Dataset("data/breast_cancer", "breast-cancer.data", "Class", "Breast cancer"))
    dm.add_dataset(Dataset("data/stress", "stress.csv", "sl", "Stress level"))
    dm.add_dataset(Dataset("data/wine", "WineQT.csv", "quality", "Wine quality"))
    return dm


if __name__ == '__main__':
    logging.basicConfig(level=logging.CRITICAL)

    # ui = CliUi()
    ui = SimpleGui()
    datasets_manager = init_datasets_manager()
    app = Application(ui, datasets_manager)
    app.run()
