from data_treatment import download_data
from signals import calculate_signals
from backtest import backtesting
from metrics import calculate_metrics

import optuna
import numpy as np
import matplotlib.pyplot as plt

def main():

    def objective(trial):
        # Suggest Parameters
        rsi_window = trial.suggest_int("rsi_window", 7, 18)
        rsi_lower = trial.suggest_float("rsi_lower", 15, 25)
        rsi_upper = trial.suggest_float("rsi_upper", 70, 80)
        macd_window_slow = trial.suggest_int("macd_window_slow", 20, 25)
        macd_window_fast = trial.suggest_int("macd_window_fast", 7, 15)
        macd_window_sign = trial.suggest_int("macd_window_sign", 3, 9)
        adx_window = trial.suggest_int("adx_window", 9, 18)
        stop_loss = trial.suggest_float("stop_loss", .05, .15)
        take_profit = trial.suggest_float("take_profit", .05, .20)
        n_shares = trial.suggest_float("n_shares", 1, 15, step=0.1)

        train = download_data("Binance_BTCUSDT_1h.csv")
        train_length = round(len(train) * 0.6)
        train = train.iloc[0:train_length]

        n_splits = 10
        len_data = len(train)
        calmars = []
        size = len_data // n_splits

        for i in range(n_splits):

            calmar_i = 0
            startidx = i * size
            endidx = (i + 1) * size
            slice = train.iloc[startidx:endidx, :]


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

        # Penalización para evitar overfitting
        if mean_calmar > 2:
            penalty = (mean_calmar - 3) ** 2
            mean_calmar -= penalty

        return mean_calmar


    study = optuna.create_study(direction="maximize", pruner=optuna.pruners.MedianPruner())
    study.optimize(objective, n_trials=20)

    params = study.best_trial.params

    # Corremos los parámetros en el train

    full_data = download_data("Binance_BTCUSDT_1h.csv")
    train_length = round(len(full_data) * 0.6)
    train = full_data.copy().iloc[:train_length]

    train = calculate_signals(dataframe=train.copy(),
                             rsi_window=params["rsi_window"],
                             rsi_lower=params["rsi_lower"], rsi_upper=params["rsi_upper"],
                             macd_window_slow=params["macd_window_slow"], macd_window_fast=params["macd_window_fast"],
                             macd_window_sign=params["macd_window_sign"],
                             adx_window=params["adx_window"])

    portfolio_historic_train = backtesting(dataframe=train, stop_loss=params["stop_loss"],
                                          take_profit=params["take_profit"], n_shares=params["n_shares"])

    metrics_train = calculate_metrics(portfolio_historic=portfolio_historic_train)

    calmar_train = metrics_train["Calmar_Ratio"]

    # Corremos los parámetros en el test

    test_length = round(len(full_data) * 0.8)
    test = full_data.copy().iloc[train_length:test_length]

    test = calculate_signals(dataframe=test.copy(),
                              rsi_window=params["rsi_window"],
                              rsi_lower=params["rsi_lower"], rsi_upper=params["rsi_upper"],
                              macd_window_slow=params["macd_window_slow"], macd_window_fast=params["macd_window_fast"],
                              macd_window_sign=params["macd_window_sign"],
                              adx_window=params["adx_window"])

    portfolio_historic_test = backtesting(dataframe=test, stop_loss=params["stop_loss"],
                                     take_profit=params["take_profit"], n_shares=params["n_shares"])

    metrics_test = calculate_metrics(portfolio_historic=portfolio_historic_test)

    calmar_test = metrics_test["Calmar_Ratio"]

    # Corremos los parámetros en el validation

    validation = full_data.copy().iloc[test_length:]

    validation = calculate_signals(dataframe=validation.copy(),
                             rsi_window=params["rsi_window"],
                             rsi_lower=params["rsi_lower"], rsi_upper=params["rsi_upper"],
                             macd_window_slow=params["macd_window_slow"], macd_window_fast=params["macd_window_fast"],
                             macd_window_sign=params["macd_window_sign"],
                             adx_window=params["adx_window"])

    portfolio_historic_validation = backtesting(dataframe=validation, stop_loss=params["stop_loss"],
                                          take_profit=params["take_profit"], n_shares=params["n_shares"])

    metrics_validation = calculate_metrics(portfolio_historic=portfolio_historic_validation)

    calmar_validation = metrics_validation["Calmar_Ratio"]

    print(metrics_train)
    print(calmar_train)
    print(metrics_test)
    print(calmar_test)
    print(metrics_validation)
    print(calmar_validation)

    serie1 = portfolio_historic_train.copy()
    serie2 = portfolio_historic_test.copy()
    serie3 = portfolio_historic_validation.copy()

    plt.plot(range(len(serie1)), serie1, color="darkred")
    plt.plot(range(len(serie1), len(serie1) + len(serie2)), serie2, color="darkblue")
    plt.plot(range(len(serie1) + len(serie2), len(serie1) + len(serie2) + len(serie3)), serie3, color="darkgreen")
    plt.ylabel("Portfolio value")
    plt.xlabel("Time")
    plt.grid()

    plt.title("Valor del Portafolio a lo largo del Tiempo")
    plt.show()

    return study.best_params

if __name__ == "__main__":
    main()