from indicators import IndicatorsApply

class ConditionsApply():
    def __init__(self):
        pass
    def conditions(self, symbol, sf, df):
        filtered_data = []
        buy_date = []
        sell_date = []
        for i in range(200, len(sf)):
            if sf['Close'][i]<sf['ema200'][i] and sf['High'][i] >= sf['high_higher'][i-4:i-1].max() and sf['rsi'][i]<sf['rsi_max'][i-4:i-1].max() and sf['rsi_max'][i-4:i-1].max() >=70 and (sf['high_higher'].iloc[i]-sf['Close'].iloc[i])/sf['high_higher'].iloc[i] < 0.006 and sf['mfi_max'].iloc[i]>80:
                for j in range(len(df)):
                    if sf.index[i] <= df.index[j]:
                        if df['Close'][j]<df['ema200'][j] and df['High'][j] >= df['high_higher'][j-4:j-1].max() and df['rsi'][j]<df['rsi_max'][j-4:j-1].max() and df['rsi_max'][j-4:j-1].max() >=70 and (df['high_higher'].iloc[j]-df['Close'].iloc[j])/df['high_higher'].iloc[j] < 0.006 and df['mfi_max'].iloc[j]>80:
                            if df.index[j].strftime("%Y-%m-%d") not in  sell_date:
                                sell_date.append(sf.index[i].strftime("%Y-%m-%d"))
                                filtered_data.append([symbol, sf.index[i].strftime("%Y-%m-%d %H:%M"), "Sell", round((sf['High'].iloc[i]+sf['Low'].iloc[i])/2,1), round(sf['Close'].iloc[i],1), round(sf['Close'].iloc[i]*.994,1), round(sf['Close'].iloc[i]*.99,1),round(sf['high_higher'].iloc[i],1)])

            elif sf['Close'][i]>sf['ema200'][i] and sf['Low'][i] <= sf['low_lower'][i-4:i-1].min() and sf['rsi'][i]>sf['rsi_min'][i-4:i-1].min() and sf['rsi_min'][i-4:i-1].min() <= 30 and (sf['Close'].iloc[i]-sf['low_lower'].iloc[i])/sf['low_lower'].iloc[i] < 0.006 and sf['mfi_min'].iloc[i]<20:
                for j in range(200, len(df)):
                    if sf.index[i] <= df.index[j]:
                        if df['Close'][j]>df['ema200'][j] and df['Low'][j] <= df['low_lower'][j-4:j-1].min() and df['rsi'][j]>df['rsi_min'][j-4:j-1].min() and df['rsi_min'][j-4:j-1].min() <= 30 and (df['Close'].iloc[j]-df['low_lower'].iloc[j])/df['low_lower'].iloc[j] < 0.006 and df['mfi_min'].iloc[j]<20:
                            if df.index[j].strftime("%Y-%m-%d") not in  buy_date:
                                buy_date.append(sf.index[i].strftime("%Y-%m-%d"))
                                filtered_data.append([symbol, sf.index[i].strftime("%Y-%m-%d %H:%M"), "Buy", round(sf['Close'].iloc[i],1), round((sf['High'].iloc[i]+sf['Low'].iloc[i])/2,1), round(sf['Close'].iloc[i]*1.004,1), round(sf['Close'].iloc[i]*1.01,1), round(sf['low_lower'].iloc[i],1)])
        return filtered_data


if __name__ == "__main__":
    ca = ConditionsApply()
