from data_treatment import download_data
from signals import calculate_signals
from backtest import backtesting
from metrics import calculate_metrics

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



    return print(metrics)


if __name__ == "__main__":
    main()