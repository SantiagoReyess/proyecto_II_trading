import ta

def calculate_signals(dataframe,
                      rsi_window, rsi_lower, rsi_upper,
                      macd_window_slow, macd_window_fast, macd_window_sign,
                      adx_window):
    """
    Calcula indicadores técnicos y genera señales de compra/venta basadas en RSI, MACD y ADX.
    Luego combina los resultados para emitir señales finales de compra o venta

    Parameters
    ----------
    dataframe :
        DataFrame con al menos las columnas `Open`, `High`, `Low`, `Close`.

    rsi_window : int
        Número de periodos para calcular el RSI.
    rsi_lower : float
        Umbral inferior del RSI para generar una señal de compra (sobreventa).
    rsi_upper : float
        Umbral superior del RSI para generar una señal de venta (sobrecompra).
    macd_window_slow : int
        Ventana lenta para el cálculo del MACD.
    macd_window_fast : int
        Ventana rápida para el cálculo del MACD.
    macd_window_sign : int
        Ventana de la señal del MACD.
    adx_window : int
        Ventana para el cálculo del ADX.

    Returns
    -------
    pandas.DataFrame
        DataFrame original con columnas adicionales:

            - `RSI`: Índice de fuerza relativa.
            - `MACD`, `MACD_Signal`, `MACD_Hist`: Componentes del MACD.
            - `ADX`, `+DI`, `-DI`: Componentes del ADX.

            - `Buy RSI`, `Sell RSI`
            - `Buy MACD`, `Sell MACD`
            - `Buy ADX`, `Sell ADX`

            - `buy_signal`
            - `sell_signal`

    """


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

    #Dropping Nans
    signal_cols = ["Buy RSI", "Sell RSI", "Buy MACD", "Sell MACD", "Buy ADX", "Sell ADX"]
    dataframe[signal_cols] = dataframe[signal_cols].fillna(False)
    return dataframe