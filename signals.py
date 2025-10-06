import ta

def calculate_signals(dataframe,
                      rsi_window, rsi_lower, rsi_upper,
                      macd_window_slow, macd_window_fast, macd_window_sign,
                      adx_window):

    dataframe = dataframe.copy()

    # RSI
    dataframe["RSI"] = ta.momentum.RSIIndicator(close=dataframe["Close"], window=rsi_window).rsi()
    ## Evaluate RSI
    dataframe["Buy RSI"] = dataframe["RSI"] < rsi_lower
    dataframe["Sell RSI"] = dataframe["RSI"] > rsi_upper

    # MACD
    macd = ta.trend.MACD(close=dataframe["Close"], window_slow=macd_window_slow, window_fast=macd_window_fast, window_sign=macd_window_sign)
    dataframe["MACD"] = macd.macd()
    dataframe["MACD_Signal"] = macd.macd_signal()
    dataframe["MACD_Hist"] = macd.macd_diff()

    ## Evaluate MACD
    dataframe["Buy MACD"] = dataframe["MACD"] > dataframe["MACD_Signal"]
    dataframe["Sell MACD"] = dataframe["MACD"] < dataframe["MACD_Signal"]

    # ADX
    adx = ta.trend.ADXIndicator(high=dataframe["High"], low=dataframe["Low"], close=dataframe["Close"], window=adx_window)
    dataframe["ADX"] = adx.adx()
    dataframe["+DI"] = adx.adx_pos()
    dataframe["-DI"] = adx.adx_neg()

    ## Evaluate ADX
    dataframe["Buy ADX"] = ((dataframe["ADX"] > 25) & (dataframe["+DI"] > dataframe["-DI"]))
    dataframe["Sell ADX"] = ((dataframe["ADX"] > 25) & (dataframe["-DI"] > dataframe["+DI"]))

    dataframe["buy_signal"] = (dataframe[['Buy RSI', 'Buy MACD', 'Buy ADX']].sum(axis=1) >= 2)
    dataframe["sell_signal"] = (dataframe[['Sell RSI', 'Sell MACD', 'Sell ADX']].sum(axis=1) >= 2)

    return dataframe