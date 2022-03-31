from commands.command_abs import CommandSelection, ExitCommand
from commands.welcome_page import SelectDatasetCommand, EvaluateCommand, UploadDatasetCommand
from datasets.datasets_manager import DatasetsManager
from prism import Prism
from ui.ui import UserInterface


class Application:
    def __init__(self, ui: UserInterface, datasets_manager: DatasetsManager):
        self.prism = Prism()
        self.ui = ui
        self.datasets_manager = datasets_manager
        self.welcome_page_cs = CommandSelection()
        self.welcome_page_cs.add_command(SelectDatasetCommand(self.prism, self.ui, self.datasets_manager,
                                                              "select_dataset", "select a dataset from the list and perform analysis of prism on it"))
        self.welcome_page_cs.add_command(EvaluateCommand(self.ui, self.datasets_manager,
                                                         "evaluate", "run classification on all test parts of the datasets and show result metrics"))
        self.welcome_page_cs.add_command(UploadDatasetCommand(self.ui, self.datasets_manager,
                                                              "upload_dataset", "upload new dataset"))
        self.welcome_page_cs.add_command(ExitCommand("exit", "exit the application"))

    def run(self):
        running = True
        while running:
            command = self.ui.welcome_page(self.welcome_page_cs)
            running = command.run()
