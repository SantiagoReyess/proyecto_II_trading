import pandas as pd

def download_data(file_name):
    """
        Carga y limpia datos de un archivo CSV con información de mercado.

        Esta función lee un archivo CSV, invierte el orden del índice (para que los datos
        más recientes aparezcan al final) y elimina columnas irrelevantes para el análisis.

        Parameters
        ----------
        file_name : str
            Ruta o nombre del archivo CSV que contiene los datos a cargar.

        Returns
            pandas.DataFrame

        """

    dataframe = pd.read_csv(file_name)
    dataframe = dataframe.sort_index(ascending=False)
    dataframe = dataframe.drop(columns = ["Unix", "Symbol", "Volume BTC", "Volume USDT", "tradecount"])

    return dataframe
