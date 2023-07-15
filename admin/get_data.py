import yfinance as yf

class DataGain():
    def __init__(self):
        pass
        
    def data_rec(self, symbol, period, interval):
        df = yf.download(symbol, period='60d', interval='15m')
        return df
    
if __name__ == "__main""":
    dg = DataGain()
