from functools import lru_cache
from get_data import DataGain, yf

@lru_cache(maxsize=128, typed=False)
class IndicatorsApply():
    
    def __init__(self):
        pass
    
    def indicators(self, df):
        df['rsi'] = tb.RSI(df.Close, 9)
        df['macd'], df['signal'], df['hist'] = tb.MACD(df.Close, 8, 21, 5)
        df['sma20'] = df.Close.rolling(20).mean()
        df['high_higher'] = df.High.rolling(5).max()
        df['low_lower'] = df.Low.rolling(5).min()
        df['rsi_max'] = df['rsi'].rolling(5).max()
        df['rsi_min'] = df['rsi'].rolling(5).min()
        df['higher_20'] = df['high_higher'].rolling(20).max()
        df['lower_20'] = df['low_lower'].rolling(20).min()
        df['rsi_max_20'] = df['rsi_max'].rolling(20).max()
        df['rsi_min_20'] = df['rsi_min'].rolling(20).min()
        df['ema200'] = tb.EMA(df.Close, 200)
        df['mfi_min'] = tb.MFI(df.High, df.Low, df.Close, df.Volume, 14).rolling(5).min()
        df['mfi_max'] = tb.MFI(df.High, df.Low, df.Close, df.Volume, 14).rolling(5).max()
        return df

if __name__ == "__main__":
    ia = IndicatorsAplly()
    
    
