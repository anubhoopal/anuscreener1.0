from functools import lru_cache
#import talib as tb
import ta
from ta.momentum import (
    AwesomeOscillatorIndicator,
    KAMAIndicator,
    PercentagePriceOscillator,
    PercentageVolumeOscillator,
    ROCIndicator,
    RSIIndicator,
    StochasticOscillator,
    StochRSIIndicator,
    TSIIndicator,
    UltimateOscillator,
    WilliamsRIndicator,
)
from ta.others import (
    CumulativeReturnIndicator,
    DailyLogReturnIndicator,
    DailyReturnIndicator,
)
from ta.trend import (
    MACD,
    ADXIndicator,
    AroonIndicator,
    CCIIndicator,
    DPOIndicator,
    EMAIndicator,
    IchimokuIndicator,
    KSTIndicator,
    MassIndex,
    PSARIndicator,
    SMAIndicator,
    STCIndicator,
    TRIXIndicator,
    VortexIndicator,
)
from ta.volatility import (
    AverageTrueRange,
    BollingerBands,
    DonchianChannel,
    KeltnerChannel,
    UlcerIndex,
)
from ta.volume import (
    AccDistIndexIndicator,
    ChaikinMoneyFlowIndicator,
    EaseOfMovementIndicator,
    ForceIndexIndicator,
    MFIIndicator,
    NegativeVolumeIndexIndicator,
    OnBalanceVolumeIndicator,
    VolumePriceTrendIndicator,
    VolumeWeightedAveragePrice,
)

@lru_cache(maxsize=128, typed=False)
class IndicatorsApply():
    def __init__(self):
        pass
    def indicators(df):        
        EMA = EMAIndicator(df.Close, 200)
        RSI = RSIIndicator(df.Close, 9)
        MFI = MFIIndicator(df.High, df.Low, df.Close, df.Volume, 14)
        df['rsi'] = RSI.rsi()
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
        df['ema200'] = EMA.ema_indicator()
        df['mfi_min'] = MFI.money_flow_index().rolling(5).min()
        df['mfi_max'] = MFI.money_flow_index().rolling(5).max()
        return df
##    def indicators(df):
##        df['rsi'] = tb.RSI(df.Close, 9)
##        df['macd'], df['signal'], df['hist'] = tb.MACD(df.Close, 8, 21, 5)
##        df['sma20'] = df.Close.rolling(20).mean()
##        df['high_higher'] = df.High.rolling(5).max()
##        df['low_lower'] = df.Low.rolling(5).min()
##        df['rsi_max'] = df['rsi'].rolling(5).max()
##        df['rsi_min'] = df['rsi'].rolling(5).min()
##        df['higher_20'] = df['high_higher'].rolling(20).max()
##        df['lower_20'] = df['low_lower'].rolling(20).min()
##        df['rsi_max_20'] = df['rsi_max'].rolling(20).max()
##        df['rsi_min_20'] = df['rsi_min'].rolling(20).min()
##        df['ema200'] = tb.EMA(df.Close, 200)
##        df['mfi_min'] = tb.MFI(df.High, df.Low, df.Close, df.Volume, 14).rolling(5).min()
##        df['mfi_max'] = tb.MFI(df.High, df.Low, df.Close, df.Volume, 14).rolling(5).max()
##        return df

if __name__ == "__main__":
    IndicatorsApply()
