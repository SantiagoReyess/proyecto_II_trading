from data_treatment import download_data
from signals import calculate_signals

def main():

    # Read Data
    dataframe = download_data("Binance_BTCUSDT_1h.csv")
    # Generate trading indicators
    dataframe = calculate_signals(dataframe=dataframe,
                                  rsi_window=10,
                                  rsi_lower=35, rsi_upper=65,
                                  macd_window_slow=7, macd_window_fast=21, macd_window_sign=15,
                                  adx_window=14)

    return print(dataframe)


if __name__ == "__main__":
    main()