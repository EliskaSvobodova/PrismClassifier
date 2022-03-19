from typing import List

from dataset import Dataset


class DatasetsManager:
    def __init__(self):
        self.datasets: List[Dataset] = []

    def add_dataset(self, dataset: Dataset):
        self.datasets.append(dataset)

    @property
    def datasets_list(self):
        return self.datasets
