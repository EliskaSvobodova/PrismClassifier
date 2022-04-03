from abc import ABC

from command_abs import Command
from datasets.datasets_manager import DatasetsManager
from prism import Prism
from ui.ui import UserInterface


class WelcomePageCommand(Command, ABC):
    def __init__(self, ui: UserInterface, datasets_manager: DatasetsManager):
        super().__init__()
        self.ui = ui
        self.d_manager = datasets_manager


class SelectDatasetCommand(WelcomePageCommand):
    @property
    def name(self):
        return "select dataset"

    @property
    def description(self):
        return "select a dataset from the list and perform analysis of prism on it"

    def __init__(self, prism: Prism, ui: UserInterface, datasets_manager: DatasetsManager):
        super().__init__(ui, datasets_manager)
        self.prism: Prism = prism

    def run(self) -> bool:
        dataset = self.ui.select_dataset(self.d_manager)
        if dataset is None:
            return True
        if dataset.rules_available and self.ui.should_load_rules():
            self.prism.rules = dataset.load_rules()
        else:
            self.ui.fit_rules()
            self.prism.subscribe(self.ui)
            self.prism.fit(dataset.X_train, dataset.y_train)
            dataset.save_rules(self.prism.rules)

        self.ui.analyse_dataset(self.prism, dataset)
        return True


class UploadDatasetCommand(WelcomePageCommand):
    @property
    def name(self):
        return "upload dataset"

    @property
    def description(self):
        return "upload new dataset"

    def run(self) -> bool:
        dataset = self.ui.upload_dataset(self.d_manager.top_dir)
        self.d_manager.add_dataset(dataset)
        return True
