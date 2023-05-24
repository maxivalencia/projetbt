#!/bin/bash

# importation des packages nécessaire
#import yahoo_fin.stock_info as si
import pandas as pd
import numpy as np
from numpy import loadtxt
#import pandas_datareader as pdr
#from pandas_datareader import data as pdr
#import matplotlib.pyplot as plt
from datetime import datetime
from ta import add_all_ta_features
from ta.momentum import RSIIndicator
from ta.trend import EMAIndicator, MACD, ADXIndicator, CCIIndicator
from ta.volatility import AverageTrueRange, BollingerBands

from sklearn.model_selection import RepeatedStratifiedKFold, StratifiedKFold
from sklearn.model_selection import KFold
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.pipeline import Pipeline
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import classification_report
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import ExtraTreesClassifier 
from sklearn.ensemble import AdaBoostClassifier 
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import accuracy_score
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import RandomizedSearchCV
from sklearn import svm
from sklearn.neural_network import MLPClassifier
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.naive_bayes import GaussianNB

import datetime as dt
import time
from datetime import timedelta
import yfinance as yf
import calendar

import os.path
import os

#from fxcmpy import fxcmpy
import fxcmpy

### ------ Quelque donnée utile ------ ###
timeframe = "m1" #  ‘m1’, ‘m5’, ‘m15’, ‘m30’, ‘H1’, ‘H2’, ‘H3’, ‘H4’, ‘H6’, ‘H8’, ‘D1’, ‘W1’, or ‘M1’.
nom_fichier = "data"
type_fichier = "csv"
#pair = "EURUSD=X"
max_windows = 60 #  périod de calcul en jours
data = pd.DataFrame()
capital_test = 20000
sl_test = 2
tp_test = 5
encours = False
operation = 0
sl_encours = 0.0
tp_encours = 0.0
risque_test = 0.02
roi_min_test = 0.05
#lot_test = 1
lot_test = 1
valeur_pip_test = 0.0001

pairs_list = []
list_file_name = "PairsListes.plt"
config_file_name = "FXCM.cfg"
server = 'demo' #type de serveur demo ou real
#accountid = "701752284"
accountid = 1825466
#accountid = 1829628
isdata = False
info = ''
transaction = ''
summary = ''
max_ask = 0.0
max_bid = 0.0
min_ask = 0.0
min_bid = 0.0
temps_min_ask = datetime.now()
temps_min_bid = datetime.now()
temps_max_ask = datetime.now()
temps_max_bid = datetime.now()
temps_coupure = datetime.now()
trade = False
status_file = "OkTrade.txt"
account_file = "AccountId.txt"
con = ''
max_position = 10
connected = False
compteur = 0
compteur_limite = 1000

### ------ Initialisation de certaine valeur ------ ###
#api = fxcmpy.fxcmpy(config_file = "fxcm.cfg")
# dans fxcm il exist période m1 => "m1"
#api.subscribe_market_data

# fonction à ajouter :
# calcul ilay mety ho ambany indrindra ahafahana manao comparaison amin'ny stop loss ao anaty periode 15mn <= ok
# calcul izay mety ho ambony indrindra ahafahana manao calcul ny take profit ao anaty periode 15mn <= ok
# fotoana mety ahatratrarana ny take profit <= ok
# fotoana mety andalovan'ny valeur ambany indrindra <= ok

# lot alaina anaty paramètre
# pair misy liste azo anovana azy automatique <= ok
# calcul lot sy ny solde en cours, hoe firy ny lot azo alaina maximum en fonction an'ny balance
# calcul nombre de lot io dynamique, en fonction pair travailler-na
# raha manana moyen ahafahana maka ny pair par minute dia alaina anaovana calcul par 15mn <= ok
# miasa amin'ny pair maro indray miaraka ilay bot <= ok
# mety ny pair rehetra dia izay ahafahany maka position <= ok
# izay position efa misy dia anaovana stop loss dynamique raha azo atao <= ok
# coupure position rehefa tsy tratra ao anatiny fotoana voafetra ny take profit nefa mba efa bénéfice ny position <= ok

# coupure position rehefa ela loatra na loss aza ny position <= rehefa tena cas extreme vao atao
# tokony misy valeur retour ny prise de position amantarana hoe ok ve ilay position sa tsy ok, dia inona no tsy naha ok azy <= mila fonction avy amin'ny api

def GetOpenPositionsSummary():
    global con, summary
    summary = con.get_open_positions_summary().T
    print(summary)
    return summary
    
def GetClosedPositionsSummary():
    global con, summary
    summary = con.get_closed_positions_summary().T
    print(summary)
    return summary
    
def GetAccountSummary():
    global con, summary
    summary = con.get_accounts_summary().T
    print(summary)
    return summary
    
def GetSummary():
    global con, summary
    summary = con.get_summary().T
    print(summary)
    return summary
    
def GetOpenOrders():
    global con, transaction
    transaction = con.get_orders().T
    print(transaction)
    return transaction
    
def GetOrderIds():
    global con
    orders = con.get_order_ids()
    return orders[-1]

def SetSellOrder(pair, valeur=1, tp=4, sl=2, date_expiration=None):
    global con
    try:
        order = con.create_entry_order(symbol=pair, is_buy=False, amount=valeur, time_in_force='GTC', order_type="Entry", limit=tp, is_in_pips=True, rate=tp, stop=sl, trailing_step=1, trailing_stop_step=1, order_range=None, expiration=date_expiration, account_id=GetAccountId())
        #print(GetOrderIds())
        print(order)
    except Exception as e:
        print(e)
        return False
    return True

def SetBuyOrder(pair, valeur=1, tp=4, sl=2, date_expiration=None):
    global con
    try:
        order = con.create_entry_order(symbol=pair, is_buy=True, amount=valeur, time_in_force='GTC', order_type="Entry", limit=tp, is_in_pips=True, rate=tp, stop=sl, trailing_step=1, trailing_stop_step=1, order_range=None, expiration=date_expiration, account_id=GetAccountId())
        #print(GetOrderIds())
        print(order)
    except Exception as e:
        print(e)
        return False
    return True
 
def SetSellTrade(pair, valeur=1, tp=4, sl=2):
    global con
    try:
        order = con.open_trade(symbol=pair, is_buy=False, amount=valeur, time_in_force='GTC', order_type='AtMarket', rate=tp, is_in_pips=True, limit=tp, at_market=0, stop=sl, trailing_step=1, account_id=GetAccountId())
        print(order)
    except Exception as e:
        print(e)
        return False
    return True

def SetBuyTrade(pair, valeur=1, tp=4, sl=2):
    global con
    try:
        order = con.open_trade(symbol=pair, is_buy=True, amount=valeur, time_in_force='GTC', order_type='AtMarket', rate=tp, is_in_pips=True, limit=tp, at_market=0, stop=sl, trailing_step=1, account_id=GetAccountId())
        print(order)
    except Exception as e:
        print(e)
        return False
    return True

def SetSellPosition(pair, valeur=1, tp=5, sl=2):
    global con
    try:
        #order = con.create_market_sell_order(symbol=pair, amount=valeur, is_in_pips=True, stop_loss=sl, take_profit=tp)
        order = con.create_market_sell_order(symbol=pair, amount=valeur)
        trade_id = con.get_open_trade_ids()[-1]
        con.change_trade_stop_limit(trade_id, is_stop=False, rate=tp, is_in_pips=True, trailing_step=0)
        con.change_trade_stop_limit(trade_id, is_stop=True, rate=sl, is_in_pips=True, trailing_step=0)
        print(order)
        print("Trade id :", trade_id)
    except Exception as e:
        print(e)
        return False
    return True
    
def SetBuyPosition(pair, valeur=1, tp=5, sl=2):
    global con
    try:
        #order = con.create_market_buy_order(symbol=pair, amount=valeur, is_in_pips=True, stop_loss=sl, take_profit=tp)
        order = con.create_market_buy_order(symbol=pair, amount=valeur)
        trade_id = con.get_open_trade_ids()[-1]
        con.change_trade_stop_limit(trade_id, is_stop=False, rate=tp, is_in_pips=True, trailing_step=0)
        con.change_trade_stop_limit(trade_id, is_stop=True, rate=sl, is_in_pips=True, trailing_step=0)
        print(order)
        print("Trade id :", trade_id)
    except Exception as e:
        print(e)
        return False
    return True

def GetOrderId(numero):
    global con
    order_id = con.get_order_ids()[numero]
    print(order_id)
    return order_id

def GetOrderDelete(order_id):
    global con
    order_id = con.delete_order(order_id)
    print(order_id)
    return order_id

def SetOrderLimit(order_id, sl):
    global con
    order = con.change_order_stop_limit(order_id=order_id, is_stop_in_pips=True, is_limit_in_pips=True, limit=sl, stop=-1)
    print(order)
    return order

def SetOrderChange(order_id, valeur, tp):
    global con
    order = con.change_order(order_id=order_id, amount=valeur, rate=tp)
    print(order)
    return order

def GetBalance():
    global con
    account = con.get_accounts().T
    print("Balance actuelle :", account[0][3])
    return account[0][3]

def SetTakeProfit(tp):
    global tp_encours
    tp_encours = tp
    return True

def SetStopLoss(sl):
    global sl_encours
    sl_encours = sl
    return True

def GetNombrePosition():
    global con
    orders = con.get_orders().T
    return len(orders)

def GetTicket():
    global con
    ticket = con.get_subscribed_symbols()
    print(ticket)
    return ticket

def SetTicket(pair):
    global con
    con.subscribe_market_data(pair)
    return True

def UnSetTicket(pair):
    global con
    con.unsubscribe_market_data(pair)
    return True
    
# fonction ahafahana manao ny calcul ny nombre de lot tokony azo atao trade
def SetNombreLot():
    global lot_test
    lot_test = 1
    return True

def Connection():
    global con
    global server, config_file_name
    con = fxcmpy.fxcmpy(config_file=config_file_name, server = server)
    print(">>> Connection effectuée avec succès")
    connected = True
    return True

def Deconnection():
    global con
    con.close()
    print(">>> Deconnection effectuée avec succès")
    connected = False
    return True

# tsy tena obligatoire fa ahafahana maka ny information mikasika ny ticket na pair iray
#def GetInfoTicket():

def GetOpenPosition():
    global con
    positions = con.get_open_positions().T
    print(positions)
    return positions

"""
def GetInfoTrade():
    global con
    global info
    info = con.get_accounts().T
    print(info)
"""

def GetInfoPosition(tradeId):
    global con
    position = con.get_open_position(tradeId)
    print(position)
    return position

def ClosePosition(tradeId, valeur):
    global con
    con.close_trade(trade_id = tradeId, amount = valeur)
    print(">>> Fermeture de la position", tradeId, " pour la valeur :", valeur)
    return True

def CloseAllForSymbol(pair):
    global con
    con.close_all_for_symbol(pair)
    print(">>> Fermeture de toute les positions pour le symbol:", pair)
    return True
    
def CloseAll():
    global con
    con.close_all()
    print(">>> Fermeture de toute les positions ouverte")
    return True

def ChangeStopLoss(valeur, trId):
    global con, tradeId
    con.change_trade_stop_limit(tdId, is_in_pips = False, is_stop = False, rate = valeur)
    print(">>> Modification stoploss pour la valeur :", valeur)
    return True

def ChangeTakeProfit(valeur, trId):
    global con, tradeId
    con.change_order(order_id=tdId, amount=valeur)
    print(">>> Modification takeprofit pour la valeur :", valeur)
    return True

def GetOpenTradeIds():
    global con, tradeId
    tradeId = con.get_open_trade_ids()
    print(">>> Liste des Identifications Ouverte :", tradeId)
    return tradeId

def GetClosedTradeIds():
    global con, tradeId
    tradeId = con.get_closed_trade_ids()
    print(">>> Liste des Identifications Clôturer :", tradeId)
    return tradeId

def GetClosedPosition():
    global con
    closed = con.get_closed_positions().T
    print(">>> Liste des positions Clôturer:", closed)
    return closed
    
def GetAllTradeIds():
    global con, tradeId
    tradeId = con.get_All_trade_ids()
    print(">>> Liste des identifications des trades:", tradeId)
    return tradeId

# récupération des pairs à traiter
def GetPairList():
    global pairs_list
    try:
        pairs_list = con.get_instruments()
        #file = open(list_file_name, "r")
        #pair_list = file.read()
        #pairs_list = pair_list.split(",")
        print(">>> Liste des symboles récupérer avec succès !!!")
        print(pairs_list)
        #file.close()
        return pairs_list
    except:
        print(">>> !!! Erreur de la récupération de la liste des symboles !!!")
        return False

def GetAccountInfo():
    global con
    account = con.get_accounts().T
    print(">>> Info compte :")
    print(account)
    return account

def GetAccountId(): 
    global accountid
    global con
    accountid = con.get_default_account()
    print(">>> Récupération du compte numéro :", accountid)
    return accountid

def SetAccountId(accountid):
    global con
    con.set_default_account(accountid)
    print(">>> Activiation du compte numéro :", accountid)
    return True
        
### ------ Fonction de récupération des données ------ ###
def DataRecuperation(pair, timeframe):
    # donnée global
    global data
    global isdata, con
    try:
        if(con.is_subscribed(pair)):
            print(">>> Début de la récupération des données du symbol", pair)
            #data = con.get_candles(pair, period=timeframe) #, number=2500)
            data = con.get_candles(pair, period=timeframe, number=2500)
            isdata = True
            print(">>> Fin de la récupération des données")
            return True
        else:
            print(">>> !!! Pair non souscrit !!!")
    except:
        print(">>> !!! Erreur lors de la récupération des données !!!")
    return False
    # les colonnes du tableau : date, bidopen, bidclose, bidhigh, bidlow, askopen, askclose, askhigh, asklow, tickqty
    # ask ambonin'ny bid
    #print(data.head())
    #data = yf.download(pair, start=start, end=end, interval=timeframe)

### ------ Fonction de traitement ------ ### 
def DataTraitement():
    # donnée global
    global data
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
    data = df
    
    print(">>> Fin du traitement des données récupérer")
    return True


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
#mbola atao anaty while ito fonction ito miaraka amin'ny paramètre de teste ohatra hoe trade=True
"""
Connection()
id = GetAccountId()
print(id)
Deconnection()
"""
def GetTradeStatus():
    global trade
    f = open(status_file, "r")
    if((f.read() == "True") or (f.read() == "true") or (f.read() == "TRUE") or (f.read() == "t") or (f.read() == "T")):
        trade = True
    else:
        trade = False
    f.close()
    
def GetAccountIdFromFile():
    global trade
    f = open(account_file, "r")
    account = f.read()
    SetAccountId(account)
    f.close()

GetTradeStatus()
while(trade == True):
    #Connection()
    #SetAccountId(accountid)
    #GetAccountId()
    try:
        print(">>> !!! Connexion !!!")
        #Connection()
        connected = Connection()
        while(connected == True and trade == True):
            # eto no atao ny fonction de trading no antsoina
            try:
                print(">>> Récupération des symboles à traiter")
                GetPairList()
            except Exception as e:
                print(e)
                print(">>> Erreur lors de la récupération des symboles à traiter")
                pass
            finally:
                print(">>> Fin de la récupération des symboles à traiter")
            print(">>> Début du traitement des pairs")
            if(GetNombrePosition() < max_position):
                print(">>> Nombre de position acutelle :", GetNombrePosition())
                for pairs in pairs_list:
                    GetTradeStatus()
                    if(trade == False):
                        break
                    pair = pairs
                    print(">>> Traitement du pair", pair)
                    try:
                        SetTicket(pair)
                        print(">>> !!! Connexion du symbol", pair, "!!!")
                        #if (GetTicket() == pair):
                        print(">>> Début traitement du symbole", pair)
                        is_recup = DataRecuperation(pair, timeframe)
                        if(is_recup == True):
                            #print(data.head())
                            is_trait = DataTraitement()
                            if(is_trait == True):
                                is_pred = Preditcion()
                                if(is_pred == False):
                                    print(">>> Prédiction non effectuée")
                                is_trait = False
                            else:
                                print(">>> Donnée non traiter")
                            is_recup = False
                        else:
                            print(">>> Donnée non récupérer")
                        print(">>> Fin du traitement du symbole", pair)
                        print(">>> Début traitement opération trading")
                        SetTakeProfit(tp_test)
                        SetStopLoss(sl_test)
                        if(operation == 0):
                            print(">>> Aucune trade éffectuée !!!")
                            operation = 0
                        if(operation == 1):
                            #SetBuyOrder(pair, lot_test, tp_encours, sl_encours, temps_coupure)
                            #SetBuyPosition(pair, lot_test, tp_encours, sl_encours)
                            if(SetBuyPosition(pair, lot_test, tp_encours, sl_encours)):
                                print("######################## Opération buy effectuée ########################")
                            else:
                                print("######################## Opération buy échouée!!! ########################")
                            operation = 0
                        if(operation == -1):
                            #SetSellOrder(pair, lot_test, tp_encours, sl_encours, temps_coupure)
                            #SetSellPosition(pair, lot_test, tp_encours, sl_encours)
                            if(SetSellPosition(pair, lot_test, tp_encours, sl_encours)):
                                print("######################## Opération sell effectuée ########################")
                            else:
                                print("######################## Opération sell échouée!!! ########################")
                            operation = 0
                        print(">>> Fin traitement opération trading")
                    except Exception as e:
                        compteur = compteur + 1
                        print(e)
                        print(">>> !!! Une erreur s'est produite durant le traitement du marché", pair," !!!")
                        pass
                        #break
                    finally:
                        UnSetTicket(pair)                
                        if(compteur >= compteur_limite):
                            compteur = 0
                            break
                        print(">>> !!! Deconnexion du symbole", pair, "!!!")                
                if(compteur >= compteur_limite):
                    compteur = 0
                    break
            GetTradeStatus()
    except Exception as e:
        print(e)
        pass
    finally:
        if(connected == True):
            connected = Deconnection()
        else:
            print(">>> Aucun compte connecter")
        GetTradeStatus()
  