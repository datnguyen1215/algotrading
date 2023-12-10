import uuid

class Trade:
    def __init__(self, symbol, side, size, price, time) -> None:
        self.id = uuid.uuid4()
        self.symbol = symbol
        self.side = side
        self.size = size
        self.price = price
        self.time = time
        pass