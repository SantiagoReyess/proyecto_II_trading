from data_treatment import download_data
from signals import calculate_signals
from backtest import backtesting
from metrics import calculate_metrics

import optuna

def main():

    # Read Data
    dataframe = download_data("Binance_BTCUSDT_1h.csv")#.iloc[100:300]
    # Generate trading indicators
    dataframe = calculate_signals(dataframe=dataframe,
                                  rsi_window=10,
                                  rsi_lower=35, rsi_upper=65,
                                  macd_window_slow=7, macd_window_fast=21, macd_window_sign=15,
                                  adx_window=14)

    #Backtest the strategy
    portfolio_historic = backtesting(dataframe=dataframe, stop_loss=.15, take_profit=.15, n_shares=50)

    #Obtain Metrics
    metrics = calculate_metrics(portfolio_historic=portfolio_historic)

    def objective(trial):
        # Suggest Parameters
        rsi_window = trial.suggest_float("rsi_window", 5, 25)
        rsi_lower = trial.suggest_float("rsi_lower", 10, 35)
        rsi_upper = trial.suggest_float("rsi_upper", 65, 90)
        macd_window_slow = trial.suggest_int("macd_window_slow", 3, 15)
        macd_window_fast = trial.suggest_int("macd_window_fast", 16, 25)
        macd_window_sign = trial.suggest_int("macd_window_sign", 3, 25)
        adx_window = trial.suggest_int("adx_window", 7, 30)
        stop_loss = trial.suggest_float("stop_loss", .05, .20)
        take_profit = trial.suggest_float("take_profit", .05, .20)
        n_shares = trial.suggest_float("n_shares", 1, 50, step=0.1)

        dataframe = download_data("Binance_BTCUSDT_1h.csv").iloc[100:300]

        dataframe = calculate_signals(dataframe=dataframe,
                                      rsi_window=rsi_window,
                                      rsi_lower=rsi_lower, rsi_upper=rsi_upper,
                                      macd_window_slow=macd_window_slow, macd_window_fast=macd_window_fast, macd_window_sign=macd_window_sign,
                                      adx_window=adx_window)

        portfolio_historic = backtesting(dataframe=dataframe, stop_loss=stop_loss, take_profit=take_profit, n_shares=n_shares)

        metrics = calculate_metrics(portfolio_historic=portfolio_historic)

        calmar = metrics["Calmar_Ratio"]

        return calmar

    study = optuna.create_study(direction="maximize")
    study.optimize(objective, n_trials=10)

    return study.best_params

if __name__ == "__main__":
    main()