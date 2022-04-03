import os.path
from typing import List

from datasets.dataset import Dataset

# TODO: detect saved datasets


class DatasetsManager:
    def __init__(self, top_dir: str = "data"):
        self.datasets: List[Dataset] = []
        self.top_dir = top_dir
        if not os.path.isdir(self.top_dir):
            os.mkdir(self.top_dir)

    def add_dataset(self, dataset: Dataset):
        self.datasets.append(dataset)

    @property
    def datasets_list(self):
        return self.datasets
