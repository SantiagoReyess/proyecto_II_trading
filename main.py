from data_treatment import download_data
from signals import calculate_signals
from backtest import backtesting
from metrics import calculate_metrics

import optuna
import numpy as np


def main():

    def objective(trial):
        # Suggest Parameters
        rsi_window = trial.suggest_int("rsi_window", 7, 21)
        rsi_lower = trial.suggest_float("rsi_lower", 15, 30)
        rsi_upper = trial.suggest_float("rsi_upper", 70, 85)
        macd_window_slow = trial.suggest_int("macd_window_slow", 20, 28)
        macd_window_fast = trial.suggest_int("macd_window_fast", 7, 19)
        macd_window_sign = trial.suggest_int("macd_window_sign", 3, 12)
        adx_window = trial.suggest_int("adx_window", 10, 25)
        stop_loss = trial.suggest_float("stop_loss", .05, .15)
        take_profit = trial.suggest_float("take_profit", .05, .20)
        n_shares = trial.suggest_float("n_shares", 1, 20, step=0.1)

        dataframe = download_data("Binance_BTCUSDT_1h.csv")

        n_splits = 7
        len_data = len(dataframe)
        calmars = []
        size = len_data // n_splits

        for i in range(n_splits):

            calmar_i = 0
            startidx = i * size
            endidx = (i + 1) * size
            slice = dataframe.iloc[startidx:endidx, :]


            slice = calculate_signals(dataframe=slice,
                                      rsi_window=rsi_window,
                                      rsi_lower=rsi_lower, rsi_upper=rsi_upper,
                                      macd_window_slow=macd_window_slow, macd_window_fast=macd_window_fast, macd_window_sign=macd_window_sign,
                                      adx_window=adx_window)

            portfolio_historic = backtesting(dataframe=slice, stop_loss=stop_loss, take_profit=take_profit, n_shares=n_shares)

            metrics = calculate_metrics(portfolio_historic=portfolio_historic)

            calmar_i = metrics["Calmar_Ratio"]

            calmars.append(calmar_i)

        mean_calmar = sum(calmars) / n_splits
        return mean_calmar

    study = optuna.create_study(direction="maximize")
    study.optimize(objective, n_trials=10)

    return study.best_params

if __name__ == "__main__":
    main()