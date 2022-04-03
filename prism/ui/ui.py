from abc import abstractmethod

from command_abs import CommandSelection, Command
from datasets.dataset import Dataset
from datasets.datasets_manager import DatasetsManager
from prism import Prism, FitProgressSubscriber


class UserInterface(FitProgressSubscriber):
    TITLE = "PRISM"
    SUBTITLE = "rule-based classifier"
    SELECT_DATASET_TITLE = "Select a dataset you want to work with:"
    SHOULD_LOAD_DATASET = "This dataset has pre-computed rules, do you want to load them?\n" \
                          "(otherwise the rules will be computed again from the dataset)"
    FIT_RULES_TEXT = "Extracting rules from the dataset..."
    RULES_ANALYSIS_TITLE = "Rules analysis"

    @abstractmethod
    def welcome_page(self, command_selection: CommandSelection) -> Command:
        pass

    @abstractmethod
    def select_dataset(self, manager: DatasetsManager) -> Dataset:
        pass

    @abstractmethod
    def should_load_rules(self) -> bool:
        pass

    @abstractmethod
    def analyse_dataset(self, prism: Prism, dataset: Dataset):
        pass

    @abstractmethod
    def fit_rules(self):
        pass

    @abstractmethod
    def upload_dataset(self, top_dir: str) -> Dataset:
        pass
