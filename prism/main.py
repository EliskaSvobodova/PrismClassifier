import logging

from application import Application
from datasets.datasets_manager import DatasetsManager
from ui.cli.cli_ui import CliUi
from ui.simple_gui.sg_ui import SimpleGui


if __name__ == '__main__':
    logging.basicConfig(level=logging.CRITICAL)

    # TODO: switch between CLI and GUI
    # ui = CliUi()
    ui = SimpleGui()
    datasets_manager = DatasetsManager()
    app = Application(ui, datasets_manager)
    app.run()
