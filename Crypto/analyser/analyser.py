import pandas as pd
import matplotlib.pyplot as plt

def generate_dataframe_from_prices(prices_list):
    df = pd.DataFrame({'Close': prices_list})
    return df

def calculate_moving_average(df, window: int = 7):
    df[f'MovingAverage'] = df['Close'].rolling(window=window).mean()
    return df

def calculate_bollinger_bands(df, window=20):
    df['Bollinger_LOW'] = df['Close'].rolling(window=window).mean() - 2 * df['Close'].rolling(window=window).std()
    df['Bollinger_MID'] = df['Close'].rolling(window=window).mean()
    df['Bollinger_HIGH'] = df['Close'].rolling(window=window).mean() + 2 * df['Close'].rolling(window=window).std()

    print('Low: ', int(df.iloc[-1]['Bollinger_LOW']))
    print('High: ', int(df.iloc[-1]['Bollinger_HIGH']))
    # print('Current: ', int(df.iloc[-1]['Close']))

    return df

def export_plot_as_jpeg(df):
    plt.plot(df['Bollinger_LOW'], label='Bollinger Low')
    plt.plot(df[f'MovingAverage'], label=f'Simple Moving Average')
    plt.plot(df['Bollinger_MID'], label='Bollinger Mid')
    plt.plot(df['Bollinger_HIGH'], label='Bollinger High')
    plt.plot(df['Close'], label=f'Price')
    plt.legend()
    figure = plt.gcf() # get current figure
    width = 20
    height = 10
    figure.set_size_inches(width, height)
    plt.savefig('export.jpg', dpi=300)

def analyse_everything(prices_list, moving_average_window=7, bollinger_window=20):
    df = generate_dataframe_from_prices(prices_list)
    df = calculate_moving_average(df, moving_average_window)
    df = calculate_bollinger_bands(df, bollinger_window)
    export_plot_as_jpeg(df)

if(__name__ == '__main__'):
    prices = [i for i in range(500)]
    analyse_everything(prices)