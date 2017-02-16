from qstrader.strategy.base import AbstractStrategy

from qstrader.event import (SignalEvent, EventType)


class CustomStrategy(AbstractStrategy):
    """
    A testing strategy that simply purchases (longs) a set of
    assets upon first receipt of the relevant bar event and
    then holds until the completion of a backtest.
    """
    def __init__(self, tickers, events_queue):
        self.tickers = tickers
        self.events_queue = events_queue
        self.ticks = 0
        self.invested = False

    def calculate_signals(self, event):
        ticker = self.tickers[0]
        if event.type in [EventType.BAR, EventType.TICK] and event.ticker == ticker:
            if not self.invested and self.ticks == 0:
                signal = SignalEvent(ticker, "BOT")
                self.events_queue.put(signal)
                self.invested = True
            self.