
class Price:
    def __init__(self, value, timestamp,symbol):
        self.value = value
        self.timestamp = timestamp
        self.symbol = symbol

    def __str__(self):
        return f'{self.symbol},{self.timestamp},{self.value}'