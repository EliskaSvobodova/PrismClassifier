class ProgressBar:
    """
    Call in a loop to create terminal progress bar
    source: https://stackoverflow.com/questions/3173320/text-progress-bar-in-terminal-with-block-characters (modified)

    iteration   - Required  : current iteration (Int)
    total       - Required  : total iterations (Int)
    prefix      - Optional  : prefix string (Str)
    suffix      - Optional  : suffix string (Str)
    decimals    - Optional  : positive number of decimals in percent complete (Int)
    length      - Optional  : character length of bar (Int)
    fill        - Optional  : bar fill character (Str)
    printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """

    def __init__(self, total, prefix='', suffix='', decimals=1, length=100, fill='█', printEnd="\r"):
        self.iteration = 0
        self.total = total
        self.prefix = prefix
        self.suffix = suffix
        self.decimals = decimals
        self.length = length
        self.fill = fill
        self.printEnd = printEnd

    def update(self, iteration=None):
        if iteration is None:
            self.iteration += 1
        else:
            self.iteration = iteration
        percent = ("{0:." + str(self.decimals) + "f}").format(100 * (self.iteration / float(self.total)))
        filledLength = int(self.length * self.iteration // self.total)
        bar = self.fill * filledLength + '-' * (self.length - filledLength)
        print(f'\r{self.prefix} |{bar}| {percent}% {self.suffix}', end=self.printEnd, flush=True)
        # Print New Line on Complete
        if self.iteration == self.total:
            print()
