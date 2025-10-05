import ta

def calculate_signals(dataframe,
                      rsi_window, rsi_lower, rsi_upper,
                      macd_window_slow, macd_window_fast, macd_window_sign,
                      adx_window):

    dataframe = dataframe.copy()

    # RSI
    dataframe["RSI"] = ta.momentum.RSIIndicator(close=dataframe["Close"], window=rsi_window)
    ## Evaluate RSI
    if dataframe["RSI"] < rsi_lower:
        dataframe["Buy RSI"] = 1
    else:
        dataframe["Buy RSI"] = 0

    if dataframe["RSI"] > rsi_upper:
        dataframe["Sell RSI"] = 1
    else:
        dataframe["Sell RSI"] = 0

    # MACD
    macd = ta.trend.MACD(close=dataframe["Close"], window_slow=macd_window_slow, window_fast=macd_window_fast, window_sign=macd_window_sign)
    dataframe["MACD"] = macd.macd()
    dataframe["MACD_Signal"] = macd.macd_signal()
    dataframe["MACD_Hist"] = macd.macd_diff()

    ## Evaluate MACD
    if dataframe["MACD"] > dataframe["MACD_Signal"]:
        dataframe["Buy MACD"] = 1
    else:
        dataframe["Buy MACD"] = 0

    if dataframe["MACD"] < dataframe["MACD_Signal"]:
        dataframe["Sell MACD"] = 1
    else:
        dataframe["Sell MACD"] = 0


    # ADX
    adx = ta.trend.ADXIndicator(high=dataframe["High"], low=dataframe["Low"], close=dataframe["Close"], window=adx_window)
    dataframe["ADX"] = adx.adx()
    dataframe["+DI"] = adx.adx_pos()
    dataframe["-DI"] = adx.adx_neg()

    ## Evaluate ADX
    if (dataframe["ADX"] > 25) & (dataframe["+DI"] > dataframe["-DI"]):
        dataframe["Buy ADX"]  = 1
    else:
        dataframe["Buy ADX"] = 0

    if (dataframe["ADX"] > 25) & (dataframe["-DI"] > dataframe["+DI"]):
        dataframe["Sell ADX"]  = 1
    else:
        dataframe["Sell ADX"] = 0

    return dataframe