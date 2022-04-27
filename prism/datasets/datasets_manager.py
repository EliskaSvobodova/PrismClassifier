import os.path
import sys
from os import path
from typing import List

from datasets.dataset import Dataset


class DatasetsManager:
    def __init__(self, top_dir: str = "data"):
        self.datasets: List[Dataset] = []
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")
        self.top_dir = os.path.join(base_path, top_dir)
        if not os.path.isdir(self.top_dir):
            os.mkdir(self.top_dir)
        else:
            for subdir in sorted(os.listdir(self.top_dir)):
                self.datasets.append(Dataset.load_from_storage(f"{self.top_dir}/{subdir}"))

    def add_dataset(self, dataset: Dataset):
        self.datasets.append(dataset)

    @property
    def datasets_list(self):
        return self.datasets
