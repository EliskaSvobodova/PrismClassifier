from command_abs import CommandSelection, ExitCommand
from welcome_page_com import SelectDatasetCommand, UploadDatasetCommand
from datasets.datasets_manager import DatasetsManager
from prism import Prism
from ui.ui import UserInterface


class Application:
    def __init__(self, ui: UserInterface, datasets_manager: DatasetsManager):
        self.prism = Prism()
        self.ui = ui
        self.datasets_manager = datasets_manager
        self.welcome_page_cs = CommandSelection()
        self.welcome_page_cs.add_command(SelectDatasetCommand(self.prism, self.ui, self.datasets_manager))
        self.welcome_page_cs.add_command(UploadDatasetCommand(self.ui, self.datasets_manager))
        self.welcome_page_cs.add_command(ExitCommand())

    def run(self):
        running = True
        while running:
            command = self.ui.welcome_page(self.welcome_page_cs)
            running = command.run()
