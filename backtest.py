import numpy as np
import pandas as pd

from dataclasses import dataclass


def backtesting(dataframe, stop_loss, take_profit, n_shares):

    cash = 1000000
    COM =  0.125/100

    @dataclass
    class Operation:
        time: str
        price: float
        sl: float
        tp: float
        n_shares: int
        type: str

    active_long_positions = []
    active_short_positions = []

    portfolio_historic = [cash]

    data = dataframe.copy()

    for i, row in data.iterrows():

        # Close Long Positions
        for pos in active_long_positions.copy():

            if (pos.sl > row.Close) or (pos.tp < row.Close):
                cash += row.Close * n_shares * (1 - COM)
                active_long_positions.remove(pos)

        # Close Short Positions
        for pos in active_short_positions.copy():

            if (pos.sl < row.Close) or (pos.tp > row.Close):
                cash += (pos.price * pos.n_shares) + (pos.price - row.Close) * n_shares * (1 - COM)
                active_short_positions.remove(pos)

        # Open Long Positions
        if row.buy_signal == 1:
            cost = row.Close * n_shares * (1+ COM)

            if cash > cost:
                cash -= cost

                active_long_positions.append(Operation
                                             (price = row.Close,
                                              n_shares = n_shares,
                                              sl = row.Close * (1 - stop_loss),
                                              tp = row.Close * (1 + take_profit)))

        # Open Short Positions
        if row.sell_signal == 1:
            cost = row.Close * n_shares * (1 + COM)

            if cash > cost:
                cash -= cost
                active_short_positions.append(Operation
                                              (price = row.Close,
                                               n_shares = n_shares,
                                               sl = row.Close * (1 + stop_loss),
                                               tp = row.Close * (1 -  take_profit)))

        # Value Portfolio for each row
        portfolio_val = 0
        portfolio_val += cash

        ## Value Long positions
        for pos in active_long_positions.copy():
            portfolio_val += row.Close * pos.n_shares

        ## Value Short Positions
        for pos in active_short_positions.copy():
            portfolio_val += (pos.price * pos.n_shares) + (pos.price * pos.n_shares - row.Close * pos.n_shares)

        # Add portfolio value to historic
        portfolio_historic.append(portfolio_val)

    return portfolio_historic



