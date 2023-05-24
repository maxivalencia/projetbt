#!/bin/bash
import pandas as pd
import numpy as np
from numpy import loadtxt
from datetime import datetime
from ta import add_all_ta_features
from ta.momentum import RSIIndicator
from ta.trend import EMAIndicator, MACD, ADXIndicator, CCIIndicator
from ta.volatility import AverageTrueRange, BollingerBands

### ------ Fonction de traitement ------ ### 
def DataTraitement(data):
    # donnée global
    #global data
    rsi_sell = 70
    rsi_buy = 30
    cci_sell = 100
    cci_buy = -100
    # traitement
    print(">>> Début du traitement des données récupérer")
    df = data
    df['EMA_10_ASK'] = EMAIndicator(df['askclose'], 5).ema_indicator()
    df['EMA_10_BID'] = EMAIndicator(df['bidclose'], 5).ema_indicator()
    df['EMA_30_ASK'] = EMAIndicator(df['askclose'], 15).ema_indicator()
    df['EMA_30_BID'] = EMAIndicator(df['bidclose'], 15).ema_indicator()
    df['RSI_ASK'] = RSIIndicator(df['askclose'], 10).rsi() 
    df['RSI_BID'] = RSIIndicator(df['bidclose'], 10).rsi() 
    macd_ask = MACD(df['askclose'], 20, 10, 9)
    macd_bid = MACD(df['bidclose'], 20, 10, 9)
    df['CCI_ASK'] = CCIIndicator(df['askhigh'], df['asklow'], df['askclose'], 9, 0.015).cci()
    df['CCI_BID'] = CCIIndicator(df['bidhigh'], df['bidlow'], df['bidclose'], 9, 0.015).cci()
    df['MACD_ASK'] = macd_ask.macd()
    df['MACD_BID'] = macd_bid.macd()
    df['MACDsignal_ASK'] = macd_ask.macd_signal()
    df['MACDsignal_BID'] = macd_bid.macd_signal()
    bollinger_band_ask = BollingerBands(df["askclose"], 10, 2)
    bollinger_band_bid = BollingerBands(df["bidclose"], 10, 2)
    df['bb_bbm_ask'] = bollinger_band_ask.bollinger_mavg()
    df['bb_bbm_bid'] = bollinger_band_bid.bollinger_mavg()
    df['bb_bbh_ask'] = bollinger_band_ask.bollinger_hband()
    df['bb_bbh_bid'] = bollinger_band_bid.bollinger_hband()
    df['bb_bbl_ask'] = bollinger_band_ask.bollinger_lband()
    df['bb_bbl_bid'] = bollinger_band_bid.bollinger_lband()
    
    df['Close_EMA_10_ASK'] = np.where(df['askclose'].values > df['EMA_10_ASK'].values, 1, -1)
    df['Close_EMA_10_BID'] = np.where(df['bidclose'].values > df['EMA_10_BID'].values, 1, -1)
    df['EMA_10_EMA_30_ASK'] = np.where(df['EMA_10_ASK'].values > df['EMA_30_ASK'].values, 1, -1)    
    df['EMA_10_EMA_30_BID'] = np.where(df['EMA_10_BID'].values > df['EMA_30_BID'].values, 1, -1)
    df['MACD_Signal_MACD_ASK'] = np.where(df['MACDsignal_ASK'] > df['MACD_ASK'], 1, -1)
    df['MACD_Signal_MACD_BID'] = np.where(df['MACDsignal_BID'] > df['MACD_BID'], 1, -1)
    
    df['RSI_Signal_buy'] = np.where(df['RSI_BID'] < rsi_buy, 1, 0)
    df['RSI_Signal_sell'] = np.where(df['RSI_ASK'] > rsi_sell, 1, 0)
    df['CCI_Signal_buy'] = np.where(df['CCI_BID'] < cci_buy, 1, 0)
    df['CCI_Signel_sell'] = np.where(df['CCI_ASK'] > cci_sell, 1, 0)
    df['BB_Signal_buy'] = np.where(df['bidclose'] > df['bb_bbh_bid'], 1, 0)
    df['BB_Signal_sell'] = np.where(df['askclose'] < df['bb_bbl_ask'], 1, 0)

    df['return_ask'] = np.log(df['askclose']/df['askclose'].shift(1))
    df['return_bid'] = np.log(df['bidclose']/df['bidclose'].shift(1))
    df['target_ask'] = np.where(df['return_ask'] > 0, 1, 0)
    df['target_bid'] = np.where(df['return_bid'] > 0, 1, 0)

    df = df.dropna()
    #data = df
    
    print(">>> Fin du traitement des données récupérer")
    return df

