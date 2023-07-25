
from datagain import DataGain as dg
from indicators import IndicatorsApply as ia
from data30 import DataConvert as dc

class ConditionsApply():
    def __init__(self):
        pass
    def conditions(symbol, sf):
        filtered_data = []
        sell_date = []
        buy_date = []
        #df = dc.data_rec(sf)
        #df = ia.indicators(df)
        for i in range(400, len(sf)):
            if sf['Close'][i]<sf['ema200'][i] and sf['Close'][i] < sf['Close'][i-1] and sf['High'][i-1] >= sf['high_higher'][i-10:i-1].max() and sf['rsi'][i-1]<sf['rsi_max'][i-10:i-1].max() and sf['rsi_max'][i-1].max() >=70 and (sf['high_higher'].iloc[i]-sf['Close'].iloc[i])/sf['high_higher'].iloc[i] < 0.006 and sf['mfi_max'].iloc[i]>80:
                df=dg.data_rec(symbol=symbol, period='25d', interval='30m')
                df = ia.indicators(df)
                for j in range(200, len(df)):
                    if sf.index[i] <= df.index[j]:
                        if df['Close'][j]<df['ema200'][j] and df['High'][j-1] >= df['high_higher'][j-10:j-1].max() and df['rsi'][j-1]<df['rsi_max'][j-10:j-1].max() and df['rsi'][j] >= 70 and (df['high_higher'].iloc[j]-df['Close'].iloc[j])/df['high_higher'].iloc[j] < 0.006 and df['mfi_max'].iloc[j]>80:
                            if filtered_data is None:
                                sell_date.append(df.index[j].strftime("%Y-%m-%d"))
                                filtered_data.append([symbol, df.index[j].strftime("%Y-%m-%d %H:%M"), "Sell", round((df['High'].iloc[j]+df['Low'].iloc[j])/2,1), round(df['Close'].iloc[j],1), round(df['Close'].iloc[j]*.994,1), round(df['Close'].iloc[j]*.99,1),round(df['high_higher'].iloc[j],1)])
                            elif df.index[j].strftime("%Y-%m-%d") not in  sell_date:
                                #print(filtered_data)
                                sell_date.append(df.index[j].strftime("%Y-%m-%d"))
                                filtered_data.append([symbol, df.index[j].strftime("%Y-%m-%d %H:%M"), "Sell", round((df['High'].iloc[j]+df['Low'].iloc[j])/2,1), round(df['Close'].iloc[j],1), round(df['Close'].iloc[j]*.994,1), round(df['Close'].iloc[j]*.99,1),round(df['high_higher'].iloc[j],1)])                        
                                
            elif sf['Close'][i]>sf['ema200'][i] and sf['Close'][i] > sf['Close'][i-1] and sf['Low'][i-1] <= sf['low_lower'][i-10:i-1].min() and sf['rsi'][i-1]>sf['rsi_min'][i-10:i-1].min() and sf['rsi_min'][i-1].min() <= 30 and (sf['Close'].iloc[i]-sf['low_lower'].iloc[i])/sf['low_lower'].iloc[i] < 0.006 and sf['mfi_min'].iloc[i]<20:
                df=dg.data_rec(symbol=symbol, period='25d', interval='30m')
                df = ia.indicators(df)
                for j in range(200, len(df)):
                    if sf.index[i] <= df.index[j]:
                        if df['Close'][j]>df['ema200'][j] and df['Low'][j-1] <= df['low_lower'][j-10:j-1].min() and df['rsi'][j-1]>df['rsi_min'][j-10:j-1].min() and df['rsi'][j] <=30 and (df['Close'].iloc[j]-df['low_lower'].iloc[j])/df['low_lower'].iloc[j] < 0.006 and df['mfi_min'].iloc[j]<20:
                            if filtered_data is None:
                                buy_date.append(df.index[j].strftime("%Y-%m-%d"))
                                filtered_data.append([symbol, df.index[j].strftime("%Y-%m-%d %H:%M"), "Buy", round(df['Close'].iloc[j],1), round((df['High'].iloc[j]+df['Low'].iloc[j])/2,1), round(df['Close'].iloc[j]*1.004,1), round(df['Close'].iloc[j]*1.01,1), round(df['low_lower'].iloc[j],1)])
                            elif df.index[j].strftime("%Y-%m-%d") not in  buy_date:
                                buy_date.append(df.index[j].strftime("%Y-%m-%d"))
                                filtered_data.append([symbol, df.index[j].strftime("%Y-%m-%d %H:%M"), "Buy", round(df['Close'].iloc[j],1), round((df['High'].iloc[j]+df['Low'].iloc[j])/2,1), round(df['Close'].iloc[j]*1.004,1), round(df['Close'].iloc[j]*1.01,1), round(df['low_lower'].iloc[j],1)])
        return filtered_data

if __name__ == "__main__":
    ConditionsApply()
