import pandas as pd

def download_data(file_name):

    '''
    Descargamos y acomodamos los datos en un dataframe de más antiguo a más reciente.

    '''

    dataframe = pd.read_csv(file_name)
    dataframe = dataframe.sort_index(ascending=False)
    dataframe = dataframe.drop(columns = ["Unix", "Symbol", "Volume BTC", "Volume USDT", "tradecount"])

    return dataframe

#dataframe = download_data('Binance_BTCUSDT_1h.csv')

# print(dataframe)