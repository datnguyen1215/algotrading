from simulation.trade import Trade


class Manager:
    def __init__(self) -> None:
        self.positions = []
        self.trades = []
        pass

    def open(self, trade: Trade):
        # check if already in positions
        if trade.symbol in [p.symbol for p in self.positions]:
            raise Exception("Cannot open trade that is already in positions")

        self.positions.append(trade)
        self.trades.append(trade)

    def close(self, trade: Trade):
        # check if already in positions
        if trade.symbol not in [p.symbol for p in self.positions]:
            raise Exception("Cannot close trade that is not in positions")

        # find the position
        for p in self.positions:
            if p.symbol == trade.symbol:
                self.positions.remove(p)
                self.trades.append(trade)
                break

    def get_positions(self):
        return self.positions

    def get_trades(self):
        return self.trades
