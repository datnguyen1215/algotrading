import uuid


class Trade:
    def __init__(
        self, symbol, size, open_price, open_time, close_price, close_time
    ) -> None:
        self.id = uuid.uuid4()
        self.symbol = symbol
        self.size = size
        self.price = open_price
        self.time = open_time
        self.close_price = close_price
        self.close_time = close_time
        self.profit = 0
        
        if (self.close_price is not None):
            self.profit = self.size * (self.close_price - self.price)
        pass

    def close(self, close_price, close_time):
        self.close_price = close_price
        self.profit = self.size * (self.close_price - self.price)
        self.close_time = close_time
        pass
