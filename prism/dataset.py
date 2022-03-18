from preprocessing import get_prep_data


class Dataset:
    def __init__(self, dirname, filename, y_name):
        self.dirname = dirname
        self.filename = filename
        self.y_name = y_name
        self.X_train, self.X_test, self.y_train, self.y_test = get_prep_data(f"{self.dirname}/{self.filename}", self.y_name)

    @property
    def rules_filename(self):
        return f"{self.dirname}/rules.json"
