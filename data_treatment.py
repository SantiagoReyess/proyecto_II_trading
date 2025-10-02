import pandas as pd

def download_data(file_name):

    '''


    :param file_name:
    :return dataframe:
    '''

    dataframe = pd.read_csv(file_name, low_memory=False)

    return dataframe

dataframe = download_data('Binance_BTCUSDT_1h.csv')

print(dataframe)