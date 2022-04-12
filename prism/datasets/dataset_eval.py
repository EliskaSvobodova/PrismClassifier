class DatasetEval:
    def __init__(self, accuracy_all: float, accuracy_classified: float):
        self.accuracy_all = accuracy_all  # correctly classified instances / instances
        self.accuracy_classified = accuracy_classified  # correctly classified instances / classified instances
