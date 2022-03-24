import logging

from command_selection import CommandSelection
from dataset import Dataset
from datasets_manager import DatasetsManager
from prism import Prism
from rules_analysis_cs import ShowRulesCommand, EvaluateCommand, ExitCommand
from ui import welcome_page, select_dataset, should_load_rules, loading_rules, computing_rules, select_command


def init_datasets_manager():
    dm = DatasetsManager()
    dm.add_dataset(Dataset("data/mobile_prices", "train.csv", "price_range", "Mobile prices"))
    dm.add_dataset(Dataset("data/lenses", "data.csv", "lenses", "Lenses"))
    dm.add_dataset(Dataset("data/breast_cancer", "breast-cancer.data", "Class", "Breast cancer"))
    dm.add_dataset(Dataset("data/stress", "stress.csv", "sl", "Stress level"))
    dm.add_dataset(Dataset("data/wine", "WineQT.csv", "quality", "Wine quality"))
    return dm


def init_rules_analysis_com_sel():
    cs = CommandSelection()
    cs.add_command(ShowRulesCommand({'rules': prism.rules},
                                    "show_rules", "show a list of obtained rules"))
    cs.add_command(EvaluateCommand({'X_test': dataset.X_test, 'y_test': dataset.y_test, 'prism': prism},
                                   "evaluate_rules", "run classification on the test dataset and show result metrics"))
    cs.add_command(ExitCommand("exit", "exit the rules analysis"))
    return cs


if __name__ == '__main__':
    logging.basicConfig(level=logging.CRITICAL)

    welcome_page()
    datasets_manager = init_datasets_manager()
    dataset = select_dataset(datasets_manager)

    prism = Prism()
    if should_load_rules(dataset):
        loading_rules()
        prism.load_rules(dataset.rules_filename)
    else:
        computing_rules()
        prism.fit(dataset.X_train, dataset.y_train)
        prism.save_rules(dataset.rules_filename)

    rules_analysis_cs = init_rules_analysis_com_sel()

    command = select_command("Rules analysis", rules_analysis_cs)
    while command.run():
        command = select_command("Rules analysis", rules_analysis_cs)
