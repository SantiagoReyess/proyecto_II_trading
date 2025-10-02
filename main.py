from data_treatment import download_data

def main():

    # Establishing constants
    COM = 0.00125

    # Read Data
    dataframe = download_data("Binance_BTCUSDT_1h.csv")

    return


if __name__ == "main":
    main()