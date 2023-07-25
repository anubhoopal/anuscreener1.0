import pandas as pd

#start_time = pd.Timestamp('09:15', tz='Asia/Kolkata')
start_time = pd.Timestamp('09:15')

class DataConvert():
    def __init__(self):
        pass
      
    def data_rec(df):
        df.index = pd.to_datetime(df.index)
        df_30min = df.groupby(pd.Grouper(freq='30T', origin=start_time, closed='right'), observed=True, dropna=True).agg({
        'Open': 'first',
        'High': 'max',
        'Low': 'min',
        'Close': 'last',
        'Volume': 'sum'
        })
        df_30min=df_30min.dropna()
        return df_30min

if __name__ == "__main__":
    DataConvert()
