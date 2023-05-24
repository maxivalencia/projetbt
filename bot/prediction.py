#!/bin/bash
import pandas as pd
import numpy as np
from numpy import loadtxt
from sklearn.linear_model import LinearRegression
from datetime import timedelta
### ------ Fonction de prévision ------ ### 
def Preditcion():
    # variable global
    global min_ask, min_bid, max_ask, max_bid, temps_min_ask, temps_min_bid, temps_max_ask, temps_max_bid, temps_coupure
    global data
    global capital_test
    global sl_test
    global tp_test
    global operation
    global risque_test
    global roi_min_test
    global lot_test
    global valeur_pip_test
    print(">>> Début de la prédiction")
    # traitement
    df = data
    capital = capital_test
    risque = risque_test
    gain = roi_min_test
    lot = lot_test
    valeur_pip = valeur_pip_test
    sl_en_dollar = capital * risque
    sl_en_pips = (sl_en_dollar * valeur_pip)    
    XXs = []
    for t in pd.DataFrame(df.index).values:
        XXs.append(t)
    XX = pd.DataFrame(XXs)
    yy_ask = df.askclose
    yy_bid = df.bidclose
    #XX_train_ask, XX_test_ask, yy_train_ask, yy_test_ask = train_test_split(XX, yy_ask, test_size=0.2, random_state=0)
    #XX_train_bid, XX_test_bid, yy_train_bid, yy_test_bid = train_test_split(XX, yy_bid, test_size=0.2, random_state=0)
    Xyy = df.index
    XX = np.array(df.index).reshape(-1, 1)
    yy_ask = np.array(yy_ask).reshape(-1, 1)
    yy_bid = np.array(yy_bid).reshape(-1, 1)
    models_ask = LinearRegression()
    models_bid = LinearRegression()
    models_ask.fit(XX, yy_ask)
    models_bid.fit(XX, yy_bid)
    #models_bid.fit(XX, yy)
    currTime = Xyy[-1]
    #floored = pd.to_datetime(currTime).ceil('H').to_pydatetime()
    heure_pred = currTime
    #yy_pred = models.predict([[heure_pred]])
    #calcul max et min bid et ask sur 15mn future
    
    # miandry etude manao kajy valeur objectif amin'ny prédiction
    for i in range(15):
        i = i + 1
        heure_test = heure_pred + timedelta(minutes = i)
        temps_coupure = heure_test   
        """
        if(max_ask < models_ask.predict([[heure_test]])):
            max_ask = models_ask.predict([[heure_test]])
            temps_max_ask = heure_test
        if(min_ask > models_ask.predict([[heure_test]])):
            min_ask = models_ask.predict([[heure_test]])
            temps_min_ask = heure_test
        if(max_bid < models_bid.predict([[heure_test]])):
            max_bid = models_bid.predict([[heure_test]])
            temps_max_bid = heure_test
        if(min_bid > models_bid.predict([[heure_test]])):
            min_bid = models_bid.predict([[heure_test]])
            temps_min_bid = heure_test
        """
    valeur_actuel = df.iloc[-1, 3]
    heure = Xyy[-1]
    print('>>> Valeur actuelle : %f' % (valeur_actuel))
    print('>>> Valeur stop loss en pips : %f' % (sl_en_pips))
    print('>>> Heure :', heure)
    
    # buy signal
    if(df.iloc[-1,:].target_bid > 0):
        nb_signal = 0
        if(df["RSI_Signal_buy"].iloc[-1] == 1):
            nb_signal = nb_signal + 1
        if(df["EMA_10_EMA_30_BID"].iloc[-1] == 1):
            nb_signal = nb_signal + 1
        if(df["MACD_Signal_MACD_BID"].iloc[-1] == 1):
            nb_signal = nb_signal + 1
        if(df["Close_EMA_10_BID"].iloc[-1] == 1):
            nb_signal = nb_signal + 1
        if(df["CCI_Signal_buy"].iloc[-1] == 1):
            nb_signal = nb_signal + 1
        if(df["BB_Signal_buy"].iloc[-1] == 1):
            nb_signal = nb_signal + 1
        if(nb_signal >= 3):
            sl = valeur_actuel - sl_en_pips
            #tp = max_bid
            tp = 4
            """if(sl > min_ask and (tp - valeur_actuel) > (2 * (valeur_actuel - sl))):
                SetStopLoss(sl)
                SetTakeProfit(tp)                
                operation = 1"""
            #SetStopLoss(sl)
            #SetTakeProfit(tp)                
            operation = 1
    # sell signal
    if(df.iloc[-1,:].target_ask == 0):
        nb_signal = 0
        if(df["RSI_Signal_sell"].iloc[-1] == 1):
            nb_signal = nb_signal + 1
        if(df["EMA_10_EMA_30_ASK"].iloc[-1] == -1):
            nb_signal = nb_signal + 1
        if(df["MACD_Signal_MACD_ASK"].iloc[-1] == -1):
            nb_signal = nb_signal + 1
        if(df["Close_EMA_10_ASK"].iloc[-1] == -1):
            nb_signal = nb_signal + 1
        if(df["CCI_Signel_sell"].iloc[-1] == 1):
            nb_signal = nb_signal + 1
        if(df["BB_Signal_sell"].iloc[-1] == 1):
            nb_signal = nb_signal + 1
        if(nb_signal >= 3):
            sl = valeur_actuel + sl_en_pips
            #tp = min_ask
            tp = 4
            """if(sl < max_bid and (valeur_actuel - tp) > (2 * (sl - valeur_actuel))):
                SetStopLoss(sl)
                SetTakeProfit(tp)  
                operation = -1"""
            #SetStopLoss(sl)
            #SetTakeProfit(tp)                
            operation = -1
    print(">>> Fin de la prédiction")
    return True