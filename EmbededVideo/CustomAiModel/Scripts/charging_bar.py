class ChargingBar:
    def __init__(self, total):
        self.total = total
        self.current = 0
        self.bar_length = 50

    def show(self):
        progress = self.current / self.total
        bar = "=" * int(progress * self.bar_length)
        space = " " * (self.bar_length - len(bar))
        print(f"\r[{bar}{space}] {progress * 100:.2f}%", end="")

    def update(self, step=1):
        self.current += step
        self.show()