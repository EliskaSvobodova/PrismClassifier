from abc import ABC

from commands.command_abs import Command
from datasets.datasets_manager import DatasetsManager
from prism import Prism
from ui.ui import UserInterface


class WelcomePageCommand(Command, ABC):
    def __init__(self, ui: UserInterface, datasets_manager: DatasetsManager, name, description):
        super().__init__(name, description)
        self.ui = ui
        self.d_manager = datasets_manager


class SelectDatasetCommand(WelcomePageCommand):
    def __init__(self, prism: Prism, ui: UserInterface, datasets_manager: DatasetsManager, name, description):
        super().__init__(ui, datasets_manager, name, description)
        self.prism: Prism = prism

    def run(self) -> bool:
        dataset = self.ui.select_dataset(self.d_manager)
        if dataset.rules_available and self.ui.should_load_rules():
            self.prism.rules = dataset.load_rules()
        else:
            self.ui.fit_rules()
            self.prism.subscribe(self.ui)
            self.prism.fit(dataset.X_train, dataset.y_train)
            dataset.save_rules(self.prism.rules)

        self.ui.analyse_dataset(self.prism, dataset)
        return True


class EvaluateCommand(WelcomePageCommand):
    def run(self) -> bool:
        pass


class UploadDatasetCommand(WelcomePageCommand):
    def run(self) -> bool:
        pass
