#!/usr/bin/python3

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

#import datetime as dt
import time as tm
from datetime import timedelta, date, time
import calendar

import os.path
import os

#from fxcmpy import fxcmpy
import fxcmpy

### ------ Quelque donnée utile ------ ###
timeframe = "m1" #  ‘m1’, ‘m5’, ‘m15’, ‘m30’, ‘H1’, ‘H2’, ‘H3’, ‘H4’, ‘H6’, ‘H8’, ‘D1’, ‘W1’, or ‘M1’.
timeframe5m = "m5"
timeframe15m = "m15"
nom_fichier = "data"
type_fichier = "csv"
#pair = "EURUSD=X"
max_windows = 10000 #  périod de calcul en jours
data = pd.DataFrame()
data5m = pd.DataFrame()
data15m = pd.DataFrame()
capital_test = 20000
sl_test = -2
tp_test = 5
encours = False
operation = 0
operation_chartiste = 0
sl_encours = 0.0
tp_encours = 0.0
risque_test = 0.02
roi_min_test = 0.05
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
nb_position_file = "NombrePosition.txt"
taille_lot_file = "TailleLot.txt"
source_file_name = "type_source.txt"
con = ''
max_position = 10
connected = False
compteur = 0
compteur_limite = 10
#aujourdhui = date.today()
aujourdhui = datetime.now()
tendance_ascendant = False
tendance_descendant = False
tendance_ascendant_5m = False
tendance_descendant_5m = False

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
    try:
        summary = con.get_open_positions_summary().T
    except Exception as e:
        print(">>> Erreur lors de la récupération des récapitulations des positions ouvert, source d'erreur :", e)
        return False
    print(summary)
    return summary
    
def GetClosedPositionsSummary():
    global con, summary
    try:
        summary = con.get_closed_positions_summary().T
    except Exception as e:
        print(">>> Erreur lors de la récupération des récapitulations des positions fermer, source d'erreur :", e)
        return False
    print(summary)
    return summary
    
def GetAccountSummary():
    global con, summary
    try:
        summary = con.get_accounts_summary().T
    except Exception as e:
        print(">>> Erreur lors de la récupération des récapitulations du compte, source d'erreur :", e)
        return False
    print(summary)
    return summary
    
def GetSummary():
    global con, summary
    try:
        summary = con.get_summary().T
    except Exception as e:
        print(">>> Erreur lors de la récupération des récapitulations, source d'erreur :", e)
        return False
    print(summary)
    return summary
    
def GetOpenOrders():
    global con, transaction
    try:
        transaction = con.get_orders().T
    except Exception as e:
        print(">>> Erreur lors de la récupération des ordres ouvert, source d'erreur :", e)
        return False
    print(transaction)
    return transaction
    
def GetOrderIds():
    global con
    try:
        orders = con.get_order_ids()
    except Exception as e:
        print(">>> Erreur lors de la récupération de l'identification de l'ordre, source d'erreur :", e)
        return False
    return orders[-1]

def SetSellOrder(pair, valeur=1, tp=5, sl=-2, date_expiration=None):
    global con
    try:
        order = con.create_entry_order(symbol=pair, is_buy=False, amount=valeur, time_in_force='GTC', order_type="Entry", limit=tp, is_in_pips=True, rate=tp, stop=sl, trailing_step=1, trailing_stop_step=1, order_range=None, expiration=date_expiration, account_id=GetAccountId())
        #print(GetOrderIds())
        print(order)
    except Exception as e:
        print(">>> Erreur lors de la prise de position sell, source d'erreur :", e)
        return False
    return True

def SetBuyOrder(pair, valeur=1, tp=5, sl=-2, date_expiration=None):
    global con
    try:
        order = con.create_entry_order(symbol=pair, is_buy=True, amount=valeur, time_in_force='GTC', order_type="Entry", limit=tp, is_in_pips=True, rate=tp, stop=sl, trailing_step=1, trailing_stop_step=1, order_range=None, expiration=date_expiration, account_id=GetAccountId())
        #print(GetOrderIds())
        print(order)
    except Exception as e:
        print(">>> Erreur lors de la prise de position buy, source d'erreur :", e)
        return False
    return True
 
def SetSellTrade(pair, valeur=1, tp=5, sl=-2):
    global con
    try:
        order = con.open_trade(symbol=pair, is_buy=False, amount=valeur, time_in_force='GTC', order_type='AtMarket', rate=tp, is_in_pips=True, limit=tp, at_market=0, stop=sl, trailing_step=1, account_id=GetAccountId())
        print(order)
    except Exception as e:
        print(">>> Erreur lors de la prise de position sell, source d'erreur :", e)
        return False
    return True

def SetBuyTrade(pair, valeur=1, tp=5, sl=-2):
    global con
    try:
        order = con.open_trade(symbol=pair, is_buy=True, amount=valeur, time_in_force='GTC', order_type='AtMarket', rate=tp, is_in_pips=True, limit=tp, at_market=0, stop=sl, trailing_step=1, account_id=GetAccountId())
        print(order)
    except Exception as e:
        print(">>> Erreur lors de la prise de position buy, source d'erreur :", e)
        return False
    return True

def SetSellPosition(pair, valeur=1, tp=5, sl=-2):
    global con
    try:
        #order = con.create_market_sell_order(symbol=pair, amount=valeur, is_in_pips=True, stop_loss=sl, take_profit=tp)
        order = con.create_market_sell_order(symbol=pair, amount=valeur)
        trade_id = con.get_open_trade_ids()[-1]
        con.change_trade_stop_limit(trade_id, is_stop=False, rate=tp, is_in_pips=True, trailing_step=0)
        con.change_trade_stop_limit(trade_id, is_stop=True, rate=sl, is_in_pips=True, trailing_step=0)
        con.change_trade_stop_limit(trade_id, is_stop=False, rate=tp, is_in_pips=True, trailing_step=0)
        con.change_trade_stop_limit(trade_id, is_stop=True, rate=sl, is_in_pips=True, trailing_step=0)
        con.change_trade_stop_limit(trade_id, is_stop=False, rate=tp, is_in_pips=True, trailing_step=0)
        con.change_trade_stop_limit(trade_id, is_stop=True, rate=sl, is_in_pips=True, trailing_step=0)
        print(order)
        print("Trade id :", trade_id)
    except Exception as e:
        print(">>> Erreur lors de la prise de position sell, source d'erreur :", e)
        return False
    return True
    
def SetBuyPosition(pair, valeur=1, tp=5, sl=-2):
    global con
    try:
        #order = con.create_market_buy_order(symbol=pair, amount=valeur, is_in_pips=True, stop_loss=sl, take_profit=tp)
        order = con.create_market_buy_order(symbol=pair, amount=valeur)
        trade_id = con.get_open_trade_ids()[-1]
        con.change_trade_stop_limit(trade_id, is_stop=False, rate=tp, is_in_pips=True, trailing_step=0)
        con.change_trade_stop_limit(trade_id, is_stop=True, rate=sl, is_in_pips=True, trailing_step=0)
        con.change_trade_stop_limit(trade_id, is_stop=False, rate=tp, is_in_pips=True, trailing_step=0)
        con.change_trade_stop_limit(trade_id, is_stop=True, rate=sl, is_in_pips=True, trailing_step=0)
        con.change_trade_stop_limit(trade_id, is_stop=False, rate=tp, is_in_pips=True, trailing_step=0)
        con.change_trade_stop_limit(trade_id, is_stop=True, rate=sl, is_in_pips=True, trailing_step=0)
        print(order)
        print("Trade id :", trade_id)
    except Exception as e:
        print(">>> Erreur lors de la prise de position buy, source d'erreur :", e)
        return False
    return True

def SetStopLimite(trade_id, tp=5, sl=-2):
    global con
    try:
        con.change_trade_stop_limit(trade_id, is_stop=False, rate=tp, is_in_pips=True, trailing_step=0)
        con.change_trade_stop_limit(trade_id, is_stop=True, rate=sl, is_in_pips=True, trailing_step=0)
        con.change_trade_stop_limit(trade_id, is_stop=False, rate=tp, is_in_pips=True, trailing_step=0)
        con.change_trade_stop_limit(trade_id, is_stop=True, rate=sl, is_in_pips=True, trailing_step=0)
    except Exception as e:
        print(">>> Erreur lors de la modification des stop loss et take profit, source d'erreur :", e)
        return False

def GetTradeIds():
    global con
    try:
        return con.get_open_trade_ids()
    except Exception as e:
        print(">>> Erreur de la récupératoin des identifications des trades, source d'erreur :", e)
        return False

def GetOrderId(numero):
    global con
    try:
        order_id = con.get_order_ids()[numero]
        print(order_id)
    except Exception as e:
        print(">>> Erreur de la récupératoin de l'identifications de l'ordre, source d'erreur :", e)
        return False
    return order_id

def GetOrderDelete(order_id):
    global con
    try:
        order_id = con.delete_order(order_id)
        print(order_id)
    except Exception as e:
        print(">>> Erreur lors de la suppression de l'ordre, source d'erreur :", e)
        return False
    return order_id

def SetOrderLimit(order_id, sl):
    global con
    try:
        order = con.change_order_stop_limit(order_id=order_id, is_stop_in_pips=True, is_limit_in_pips=True, limit=sl, stop=-1)
        print(order)
    except Exception as e:
        print(">>> Erreur lors de la récupératoin des identifications des trades, source d'erreur :", e)
        return False
    return order

def SetOrderChange(order_id, valeur, tp):
    global con
    try:
        order = con.change_order(order_id=order_id, amount=valeur, rate=tp)
        print(order)
    except Exception as e:
        print(">>> Erreur lors de la modification de l'ordre, source d'erreur :", e)
        return False
    return order

def GetBalance():
    global con
    try:
        account = con.get_accounts().T
        print("Balance actuelle :", account[0][3])
    except Exception as e:
        print(">>> Erreur lors de la récupératoin de la balance, source d'erreur :", e)
        return False
    return account[0][3]

def SetTakeProfit(tp):
    global tp_encours
    try:
        tp_encours = tp
    except Exception as e:
        print(">>> Erreur lors du changement du take profit, source d'erreur :", e)
        return False
    return True

def SetStopLoss(sl):
    global sl_encours
    try:
        sl_encours = sl
    except Exception as e:
        print(">>> Erreur lors du changement du stop loss, source d'erreur :", e)
        return False
    return True

def GetNombrePosition():
    global con
    try:
        orders = con.get_open_positions().T
        return orders.shape[1]
    except Exception as e:
        print(">>> Erreur de la récupératoin du nombre de position, source d'erreur :", e)
        return 0
    

def GetTicket():
    global con
    try:
        ticket = con.get_subscribed_symbols()
        print(ticket)
    except Exception as e:
        print(">>> Erreur de la récupératoin du symbole en cours, source d'erreur :", e)
        return False
    return ticket

def SetTicket(pair):
    global con
    try:
        con.subscribe_market_data(pair)
    except Exception as e:
        print(">>> Erreur de l'inscription du nouveau symbole, source d'erreur :", e)
        return False
    return True

def UnSetTicket(pair):
    global con
    try:
        con.unsubscribe_market_data(pair)
    except Exception as e:
        print(">>> Erreur de la desinscription du symbole en cours, source d'erreur :", e)
        return False
    return True
    
# fonction ahafahana manao ny calcul ny nombre de lot tokony azo atao trade
def SetNombreLot():
    global lot_test
    try:
        lot_test = 1
    except Exception as e:
        print(">>> Erreur de la modification du nombre de lot, source d'erreur :", e)
        return False
    return True

def Connection():
    global con
    global server, config_file_name
    try:
        con = fxcmpy.fxcmpy(config_file=config_file_name, server = server)
        print(">>> Connection effectuée avec succès")
        connected = True
    except Exception as e:
        print(">>> Erreur de la connection, source d'erreur :", e)
        return False
    return True

def Deconnection():
    global con
    try:
        con.close()
        print(">>> Deconnection effectuée avec succès")
        connected = False
    except Exception as e:
        print(">>> Erreur de la déconnection, source d'erreur :", e)
        return False
    return True

# tsy tena obligatoire fa ahafahana maka ny information mikasika ny ticket na pair iray
#def GetInfoTicket():

def GetOpenPosition():
    global con
    try:
        positions = con.get_open_positions().T
        print(positions)
    except Exception as e:
        print(">>> Erreur de la récupératoin des positions ouverts, source d'erreur :", e)
        return False
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
    try:
        position = con.get_open_position(tradeId)
        print(position)
    except Exception as e:
        print(">>> Erreur de la récupératoin des informations du trade, source d'erreur :", e)
        return False
    return position

def ClosePosition(tradeId, valeur):
    global con
    try:
        con.close_trade(trade_id = tradeId, amount = valeur)
        print(">>> Fermeture de la position", tradeId, " pour la valeur :", valeur)
    except Exception as e:
        print(">>> Erreur de la fermeture du trades, source d'erreur :", e)
        return False
    return True

def CloseAllForSymbol(pair):
    global con
    try:
        con.close_all_for_symbol(pair)
        print(">>> Fermeture de toute les positions pour le symbol:", pair)
    except Exception as e:
        print(">>> Erreur de la fermeture de tous les symboles, source d'erreur :", e)
        return False
    return True
    
def CloseAll():
    global con
    try:
        con.close_all()
        print(">>> Fermeture de toute les positions ouverte")
    except Exception as e:
        print(">>> Erreur de la fermeture de toute les positions, source d'erreur :", e)
        return False
    return True

def ChangeStopLoss(valeur, tdId):
    global con, tradeId
    try:
        con.change_trade_stop_limit(tdId, is_in_pips = False, is_stop = False, rate = valeur)
        print(">>> Modification stoploss pour la valeur :", valeur)
    except Exception as e:
        print(">>> Erreur du changement de stop loss, source d'erreur :", e)
        return False
    return True

def ChangeTakeProfit(valeur, tdId):
    global con, tradeId
    try:
        con.change_order(order_id=tdId, amount=valeur)
        print(">>> Modification takeprofit pour la valeur :", valeur)
    except Exception as e:
        print(">>> Erreur du changement du take profit, source d'erreur :", e)
        return False
    return True

def GetOpenTradeIds():
    global con, tradeId
    try:
        tradeId = con.get_open_trade_ids()
        print(">>> Liste des Identifications Ouverte :", tradeId)
    except Exception as e:
        print(">>> Erreur de la récupératoin des identifications des trades ouvert, source d'erreur :", e)
        return False
    return tradeId

def GetClosedTradeIds():
    global con, tradeId
    try:
        tradeId = con.get_closed_trade_ids()
        print(">>> Liste des Identifications Clôturer :", tradeId)
    except Exception as e:
        print(">>> Erreur de la récupératoin des identifications des trades fermer, source d'erreur :", e)
        return False
    return tradeId

def GetClosedPosition():
    global con
    try:
        closed = con.get_closed_positions().T
        print(">>> Liste des positions Clôturer:", closed)
    except Exception as e:
        print(">>> Erreur de la récupératoin des trades fermer, source d'erreur :", e)
        return False
    return closed
    
def GetAllTradeIds():
    global con, tradeId
    try:
        tradeId = con.get_All_trade_ids()
        print(">>> Liste des identifications des trades:", tradeId)
    except Exception as e:
        print(">>> Erreur de la récupératoin des identifications des trades, source d'erreur :", e)
        return False
    return tradeId

# récupération des pairs à traiter
def GetPairList():
    global pairs_list, list_file_name, source_file_name
    source = 'File'
    try:
        fichier = open(source_file_name, "r")
        source = fichier.read()
        fichier.close()
    except:
        source = 'File'
    if(source == 'File'):
        try:
            file = open(list_file_name, "r")
            pair_list = file.read()
            pairs_list = pair_list.split(",")
            file.close()
            print(">>> Liste des symboles récupérer avec succès !!!")
            print(pairs_list)
            return pairs_list
        except Exception as e:
            print(">>> !!! Erreur de la récupération de la liste des symboles dépuis le fichier !!!")
            print(">>> Erreur de la récupératoin des symboles, source d'erreur :", e)
            return False
    else:
        try:
            pairs_list = con.get_instruments()
            print(">>> Liste des symboles récupérer avec succès !!!")
            print(pairs_list)
            return pairs_list
        except Exception as e:
            print(">>> !!! Erreur de la récupération de la liste des symboles dépuis le réseau !!!")
            print(">>> Erreur de la récupératoin des symboles, source d'erreur :", e)
            return False

def GetAccountInfo():
    global con
    try:
        account = con.get_accounts().T
        print(">>> Info compte :")
        print(account)
    except Exception as e:
        print(">>> Erreur de la récupératoin des information sur le compte, source d'erreur :", e)
        return False
    return account

def GetAccountId(): 
    global accountid
    global con
    try:
        accountid = con.get_default_account()
        print(">>> Récupération du compte numéro :", accountid)
    except Exception as e:
        print(">>> Erreur de la récupération de l'id du compte, source d'erreur :", e)
        return False
    return accountid

def SetAccountId(accountid):
    global con
    try:
        con.set_default_account(accountid)
        print(">>> Activiation du compte numéro :", accountid)
    except Exception as e:
        print(">>> Erreur de l'enregistrement de l'id du compte, source d'erreur :", e)
        return False
    return True
        
### ------ Fonction de récupération des données ------ ###
### ------ Fonction de récupération des données ------ ###
def GetDataFromFile(pair, timeframe):
    global data
    try:
        pairs = pair.split('/')
        pair = pairs[0] + pairs[1]
        fichier = pair + "_" + timeframe + ".csv"
        filename = './Data/' + fichier
        if os.path.isfile(filename):
            data = pd.read_csv(filename, sep=';')
            #data = pd.to_datetime(data.set_index(['date']))  
            data = data.set_index(['date'])
            data.index = pd.to_datetime(data.index)
            #print(data.head())
            #data = data.drop(['DateTime'])
        else:
            return False
        return True
    except Exception as e:
        print(">>> Erreur lors de lecture des données depuis le fichier, source d'erreur :", e)
        return False

def SetDataToFile(pair, timeframe):
    global data
    try:
        pairs = pair.split('/')
        pair = pairs[0] + pairs[1]
        fichier = pair + "_" + timeframe + ".csv"
        dossier = './Data/'
        filename = dossier + fichier
        if os.path.isdir(dossier):
            if os.path.isfile(filename):
                os.remove(filename)
            data.to_csv(filename, sep=';', encoding='utf-8')
        else:
            os.mkdir(dossier, mode = 0o777)
            data.to_csv(filename, sep=';', encoding='utf-8')
        return True
    except Exception as e:
        print(">>> Erreur lors de l'enregistrement des données dans un fichier, source d'erreur :", e)
        return False
    
def DataRecuperation(pair, timeframe):
    # donnée global
    global data
    global isdata, con, aujourdhui
    try:
        data1 = GetDataFromFile(pair, timeframe)
        if(con.is_subscribed(pair)):
            print(">>> Début de la récupération des données du symbol", pair)
            #mbola amboarina rehefa milamina ny code
            #data1 = False
            if (data1 == True):
                start = data.index[-1] # + timedelta(minutes = 1)
                end = datetime.now()
                #data2 = con.get_candles(pair, period=timeframe, start=start, end=end)
                data = data.drop(start, axis=0)
                data2 = con.get_candles(pair, period=timeframe, start=start, end=end)
                data3 = pd.concat([data, data2])
                data = data3
            else:
                start = datetime.now() - timedelta(minutes = max_windows)
                #end = datetime.now()
                #data2 = con.get_candles(pair, period=timeframe, start=start, end=end)
                data2 = con.get_candles(pair, period=timeframe, number=10000)
                data = data2
            length_data_save = max_windows * 10
            last = data.index[-1] - timedelta(minutes = length_data_save)            
            for dt in data.index:
                if(dt < last):
                    data = data.drop(dt, axis=0)
            save = SetDataToFile(pair, timeframe)
            #data = con.get_candles(pair, period=timeframe) #, number=2500)
            #data = con.get_candles(pair, period=timeframe, number=2500)
            isdata = save
            aujourdhui = data.index[-1]
            print(">>> Fin de la récupération des données")
            return True
    except Exception as e:
        print(">>> !!! Erreur lors de la récupération des données !!!")
        print(">>> Source d'erreur :", e)
    return False
    # les colonnes du tableau : date, bidopen, bidclose, bidhigh, bidlow, askopen, askclose, askhigh, asklow, tickqty
    # ask ambonin'ny bid
    #print(data.head())
    #data = yf.download(pair, start=start, end=end, interval=timeframe)

### ------ Fonction de traitement ------ ### 
def DataTraitement():
    # donnée global
    global data
    try:
        rsi_sell = 70
        rsi_buy = 30
        rsi_mediane = 50
        cci_sell = 100
        cci_buy = -100
        cci_mediane = 0
        # traitement
        print(">>> Début du traitement des données récupérer")
        df = data
        df['EMA_10_ASK'] = EMAIndicator(df['askclose'], 5).ema_indicator()
        df['EMA_10_BID'] = EMAIndicator(df['bidclose'], 5).ema_indicator()
        df['EMA_30_ASK'] = EMAIndicator(df['askclose'], 15).ema_indicator()
        df['EMA_30_BID'] = EMAIndicator(df['bidclose'], 15).ema_indicator()
        df['RSI_ASK'] = RSIIndicator(df['askclose'], 10).rsi() 
        df['RSI_BID'] = RSIIndicator(df['bidclose'], 10).rsi() 
        df['CCI_ASK'] = CCIIndicator(df['askhigh'], df['asklow'], df['askclose'], 10, 0.015).cci()
        df['CCI_BID'] = CCIIndicator(df['bidhigh'], df['bidlow'], df['bidclose'], 10, 0.015).cci()
        #macd_ask = MACD(df['askclose'], 20, 10, 9)
        #macd_bid = MACD(df['bidclose'], 20, 10, 9)
        macd_ask = MACD(df['askclose'], 10, 20, 10)
        macd_bid = MACD(df['bidclose'], 10, 20, 10)
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
        ''' df['RSI_Signal_buy'] = np.where(df['RSI_BID'] < rsi_buy, 1, 0)
        df['RSI_Signal_sell'] = np.where(df['RSI_ASK'] > rsi_sell, 1, 0) '''
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
    except Exception as e:
        print(">>> Erreur lors du traitement des indicateurs techniques, source d'erreur :", e)
        return False
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
    global operation_chartiste
    global tendance_ascendant, tendance_descendant, tendance_ascendant_5m, tendance_descendant_5m
    try:
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
        #print(XX.head())
        #print(XXs.head())
        yy_ask = df.askclose
        yy_bid = df.bidclose
        #print(yy_ask.head())
        XX_ask = df.drop(['askclose'], axis=1)
        XX_bid = df.drop(['bidclose'], axis=1)  
        # nasiana an'ito ilay declaration hijerevana ny résultat fit_intercept = True      
        try:
            XX_train_ask, XX_test_ask, yy_train_ask, yy_test_ask = train_test_split(df.index.values.reshape(-1, 1), yy_ask, test_size=0.2, random_state=0)
            models_ask = LinearRegression(fit_intercept = True)
            #models_ask.fit(XX_train_ask, yy_train_ask)
            # teste model asiana to_frame ny eto
            models_ask.fit(df.index.values.reshape(-1, 1), yy_ask)
            #poly_ask = np.polyfit(x=df.index, y=yy_ask)
            #models_ask.fit(df.index.values.reshape(-1, 1), yy_ask)
        except Exception as e:
            print(">>> Erreur du traitement de la regréssion linéaire du ask, source d'erreur :", e)
        
        try:
            XX_train_bid, XX_test_bid, yy_train_bid, yy_test_bid = train_test_split(df.index.values.reshape(-1, 1), yy_bid, test_size=0.2, random_state=0)
            models_bid = LinearRegression(fit_intercept = True)
            #models_bid.fit(XX_train_bid, yy_train_bid) 
            # teste model asiana to_frame ny eto
            models_bid.fit(df.index.values.reshape(-1, 1), yy_bid) 
            #models_bid.fit(df.index.values.reshape(-1, 1), yy_bid) 
        except Exception as e:
            print(">>> Erreur du traitement de la regréssion linéaire du bid, source d'erreur :", e)
            
        Xyy = df.index
        #print(df.index.values.reshape(-1, 1))
        # test fijerevana ny contenue 
        #print(XX_test_ask.head())
        #print(yy_test_ask.head())
        """
        XX = np.array(df.index).reshape(-1, 1)
        yy_ask = np.array(yy_ask).reshape(-1, 1)
        yy_bid = np.array(yy_bid).reshape(-1, 1)
        models_ask = LinearRegression()
        models_bid = LinearRegression()
        models_ask.fit(XX, yy_ask)
        models_bid.fit(XX, yy_bid)
        #models_bid.fit(XX, yy)
        """
        currTime = Xyy[-1]
        #floored = pd.to_datetime(currTime).ceil('H').to_pydatetime()
        heure_pred = currTime
        #yy_pred_ask = models_ask.predict([[heure_pred]])
        #yy_pred_bid = models_bid.predict([[heure_pred]])
        #calcul max et min bid et ask sur 15mn future
        
        # miandry etude manao kajy valeur objectif amin'ny prédiction
        for i in range(15):
            i = i + 1
            heure_test = heure_pred + timedelta(minutes = i)
            temps_coupure = heure_test   
            #print("########## Tonga eto ##########")
            #print(models_ask.predict([[heure_test]]))
            """ donnee = pd.DataFrame([heure_test]) 
            print(donnee)
            donnee = pd.to_datetime(donnee[:, 0])  """     
            #donnee = donnee.set_index(["0"])
            #donnee.index = pd.to_datetime(donnee.index)
            #print(models_ask.predict(df.index.values.reshape(-1, 1) ))
            donnee = pd.DataFrame([heure_test])
            test_data = donnee.loc["0":]
            X_test = test_data.index.values.reshape(-1, 1)
            ''' valeur_max = models_ask.predict(X_test)
            print(yy_ask.tail())
            print(heure_test)
            print(valeur_max[0]) '''
            if(max_ask < models_ask.predict(X_test)):
                max_ask = models_ask.predict(X_test)[0]
                temps_max_ask = heure_test
                print(">>> max ask :", max_ask)
                print(">>> temps max ask :", temps_max_ask)
            if(min_ask > models_ask.predict(X_test)):
                min_ask = models_ask.predict(X_test)[0]
                temps_min_ask = heure_test
                print(">>> min ask :", min_ask)
                print(">>> temps min ask :", temps_min_ask)
            if(max_bid < models_bid.predict(X_test)):
                max_bid = models_bid.predict(X_test)[0]
                temps_max_bid = heure_test
                print(">>> max bid :", max_bid)
                print(">>> temps max bid :", temps_max_bid)
            if(min_bid > models_bid.predict(X_test)):
                min_bid = models_bid.predict(X_test)[0]
                temps_min_bid = heure_test
                print(">>> min bid :", min_bid)
                print(">>> temps min bid :", temps_min_bid)
            
        valeur_actuel = df.iloc[-1, 3]
        heure = Xyy[-1]
        print('>>> Valeur actuelle : %f' % (valeur_actuel))
        print('>>> Valeur stop loss en pips : %f' % (sl_en_pips))
        print('>>> Heure :', heure)
        
        # buy signal
        if(df.iloc[-1,:].target_bid > 0):
            nb_signal_1 = 0
            nb_signal_2 = 0
            nb_signal_3 = 0
            nb_signal_4 = 0
            # if(df["RSI_Signal_buy"].iloc[-1] == 1):
            if((df["RSI_BID"].iloc[-2] < 30 or df["RSI_BID"].iloc[-3] < 30 or df["RSI_BID"].iloc[-4] < 30) and df["RSI_BID"].iloc[-1] > 30):
                nb_signal_1 = nb_signal_1 + 1
            if(df["EMA_10_EMA_30_BID"].iloc[-1] == 1):
                nb_signal_2 = nb_signal_2 + 1
            if(df["MACD_Signal_MACD_BID"].iloc[-1] == 1):
                nb_signal_1 = nb_signal_1 + 1
            if(df["Close_EMA_10_BID"].iloc[-1] == 1):
                nb_signal_2 = nb_signal_2 + 1
            # if(df["CCI_Signal_buy"].iloc[-1] == 1):
            if((df["CCI_BID"].iloc[-2] < -100 or df["CCI_BID"].iloc[-3] < -100 or df["CCI_BID"].iloc[-4] < -100) and df["CCI_BID"].iloc[-1] > -100):
                nb_signal_1 = nb_signal_1 + 1
            if(df["BB_Signal_buy"].iloc[-1] == 1):
                nb_signal_2 = nb_signal_2 + 1
            if((df["tickqty"].iloc[-1] >= df["tickqty"].iloc[-2]) and (df["tickqty"].iloc[-2] >= df["tickqty"].iloc[-3])):
                nb_signal_4 = nb_signal_4 + 1
            #if((nb_signal_1 >= 2 and nb_signal_2 >= 2) or (nb_signal_1 >= 1 and nb_signal_2 >= 2)):
            if((nb_signal_1 >= 3 and nb_signal_2 >= 1 and tendance_ascendant_5m == True) or(nb_signal_1 >= 2 and nb_signal_2 >= 1 and tendance_ascendant == True)): # and nb_signal_3 >= 1 and nb_signal_4 >= 1):
                sl = -(valeur_actuel - sl_en_pips)
                #tp = max_bid
                tp = 10
                #if(sl > min_ask and (tp - valeur_actuel) > (2 * (valeur_actuel - sl)) and df["target_bid"][-1] == 1 and df["target_ask"][-1] == 0):
                """ if(df["target_bid"][-1] == 1 and df["target_ask"][-1] == 0):
                    SetStopLoss(sl)
                    SetTakeProfit(tp)                
                    operation = 1 """
                SetStopLoss(sl)
                SetTakeProfit(tp)              
                operation = 1  
        # sell signal
        if(df.iloc[-1,:].target_ask > 0):
            nb_signal_1 = 0
            nb_signal_2 = 0
            nb_signal_3 = 0
            nb_signal_4 = 0
            if((df["RSI_ASK"].iloc[-2] > 70 or df["RSI_ASK"].iloc[-3] > 70 or df["RSI_ASK"].iloc[-4] > 70) and df["RSI_ASK"].iloc[-1] < 70):
                nb_signal_1 = nb_signal_1 + 1
            if(df["EMA_10_EMA_30_ASK"].iloc[-1] == -1):
                nb_signal_2 = nb_signal_2 + 1
            if(df["MACD_Signal_MACD_ASK"].iloc[-1] == -1):
                nb_signal_1 = nb_signal_1 + 1
            if(df["Close_EMA_10_ASK"].iloc[-1] == -1):
                nb_signal_2 = nb_signal_2 + 1
            if((df["CCI_ASK"].iloc[-2] > 100 or df["CCI_ASK"].iloc[-3] > 100 or df["CCI_ASK"].iloc[-4] > 100) and df["CCI_ASK"].iloc[-1] < 100):
                nb_signal_1 = nb_signal_1 + 1
            if(df["BB_Signal_sell"].iloc[-1] == 1):
                nb_signal_2 = nb_signal_2 + 1
            if((df["tickqty"].iloc[-1] >= df["tickqty"].iloc[-2]) and (df["tickqty"].iloc[-2] >= df["tickqty"].iloc[-3])):
                nb_signal_4 = nb_signal_4 + 1
            #if((nb_signal_1 >= 2 and nb_signal_2 >= 2) or (nb_signal_1 >= 1 and nb_signal_2 >= 2)):
            if((nb_signal_1 >= 3 and nb_signal_2 >= 1 and tendance_descendant_5m == True) or(nb_signal_1 >= 2 and nb_signal_2 >= 1 and tendance_descendant == True)): # and nb_signal_3 >= 1 and nb_signal_4 >= 1):
                sl = -(valeur_actuel + sl_en_pips)
                #tp = min_ask
                tp = 10
                #if(sl < max_bid and (valeur_actuel - tp) > (2 * (sl - valeur_actuel)) and df["target_bid"][-1] == 0 and df["target_ask"][-1] == 1):
                """ if(df["target_bid"][-1] == 0 and df["target_ask"][-1] == 1):
                    SetStopLoss(sl)
                    SetTakeProfit(tp)  
                    operation = -1 """
                SetStopLoss(sl)
                SetTakeProfit(tp)                
                operation = -1
        print(">>> Fin de la prédiction")
    except Exception as e:
        print(">>> Erreur de la prédiction, source d'erreur :", e)
        return False
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
    try:
        f = open(status_file, "r")
        if((f.read() == "True") or (f.read() == "true") or (f.read() == "TRUE") or (f.read() == "t") or (f.read() == "T")):
            trade = True
        else:
            trade = False
        f.close()
    except Exception as e:
        print(">>> Erreur de la status de trading, source d'erreur :", e)
    
def GetAccountIdFromFile():
    global trade
    try:
        f = open(account_file, "r")
        account = f.read()
        SetAccountId(account)
        f.close()
    except Exception as e:
        print(">>> Erreur de récupération d'id depuis le fichier, source d'erreur :", e)
    
def GetPositionMax():
    global max_position
    try:
        f = open(nb_position_file, "r")
        max_position = int(f.read())
        f.close()
    except Exception as e:
        print(">>> Erreur lors de la récupération nombre de position maximal, source d'erreur :", e)

def GetTailleLot():
    global lot_test
    try:
        f = open(taille_lot_file, "r")
        lot_test = int(f.read())
        f.close()
    except Exception as e:
        print(">>> Erreur lors de la récupération nombre de la taille du lot, source d'erreur :", e)

"""
Connection()
print("Nombre de position :",GetNombrePosition())
Deconnection()
"""

def EtudeChartiste(pair):
    global data, data5m, data15m, con
    global sl_test
    global tp_test
    global operation
    global tendance_ascendant
    global tendance_descendant
    tendance_ascendant = False
    tendance_descendant = False
    tendance_ascendant_5m = False
    tendance_descendant_5m = False
    # teste de support
    # atao 20 ny nombre de bougie aloha
    nb_bougie = 20
    nb_bougie_espacement = 5
    espacement = 0
    numero_case = 0
    numero_case_max = 3
    support_bute = [0, 0, 0]
    resistance_bute = [0, 0, 0]
    support_bute_5m = [0, 0, 0]
    resistance_bute_5m = [0, 0, 0]
    support_bute_15m = [0, 0, 0]
    resistance_bute_15m = [0, 0, 0]
    marge_difference = 0.1
    support_ascendant = False
    support_descendant = False
    support_ascendant_5m = False
    support_descendant_5m = False
    support_ascendant_15m = False
    support_descendant_15m = False
    support_horizontal = False
    resistance_ascendant = False
    resistance_descendant = False
    resistance_ascendant_5m = False
    resistance_descendant_5m = False
    resistance_ascendant_15m = False
    resistance_descendant_15m = False
    resistance_horizontal = False
    canaux_ascendant = False
    canaux_descendant = False
    canaux_horizontal = False
    triangle_ascendant = False
    triangle_descendant = False
    triangle_asymetrique = False
    elargissement_ascendant = False
    elargissement_descendant = False
    elargissement_asymetrique = False
    double_top = False
    double_bottom = False
    triple_top = False
    triple_bottom = False
    epaule_tete_epaule = False
    epaule_tete_epaule_inverse = False
    marteau_retournement_haussier = False
    marteau_retournement_baissier = False
    avalement_haussier = False
    avalement_baissier = False
    try:
        data5m = con.get_candles(pair, period=timeframe5m, number=10000)
        data15m = con.get_candles(pair, period=timeframe15m, number=10000)
        for nb in range(nb_bougie):
            if(support_bute[numero_case] <= 0):
                support_bute[numero_case] = data["askhigh"].iloc[(nb - 1) * (-1)]
            if(support_bute[numero_case] > data["askhigh"].iloc[(nb - 1) * (-1)]):
                support_bute[numero_case] = data["askhigh"].iloc[(nb - 1) * (-1)]
                espacement = 0
            else:
                espacement += 1
            if(espacement >= nb_bougie_espacement):
                numero_case += 1
                espacement = 0
            if(numero_case >= numero_case_max):
                espacement = 0
                numero_case = 0
                break
        for nb in range(nb_bougie):
            if(support_bute_5m[numero_case] <= 0):
                support_bute_5m[numero_case] = data5m["askhigh"].iloc[(nb - 1) * (-1)]
            if(support_bute_5m[numero_case] > data5m["askhigh"].iloc[(nb - 1) * (-1)]):
                support_bute_5m[numero_case] = data5m["askhigh"].iloc[(nb - 1) * (-1)]
                espacement = 0
            else:
                espacement += 1
            if(espacement >= nb_bougie_espacement):
                numero_case += 1
                espacement = 0
            if(numero_case >= numero_case_max):
                espacement = 0
                numero_case = 0
                break
        for nb in range(nb_bougie):
            if(support_bute_15m[numero_case] <= 0):
                support_bute_15m[numero_case] = data15m["askhigh"].iloc[(nb - 1) * (-1)]
            if(support_bute_15m[numero_case] > data15m["askhigh"].iloc[(nb - 1) * (-1)]):
                support_bute_15m[numero_case] = data15m["askhigh"].iloc[(nb - 1) * (-1)]
                espacement = 0
            else:
                espacement += 1
            if(espacement >= nb_bougie_espacement):
                numero_case += 1
                espacement = 0
            if(numero_case >= numero_case_max):
                espacement = 0
                numero_case = 0
                break
        for nb in range(nb_bougie):
            if(resistance_bute[numero_case] >= 0):
                resistance_bute[numero_case] = data["asklow"].iloc[(nb - 1) * (-1)]
            if(resistance_bute[numero_case] < data["asklow"].iloc[(nb - 1) * (-1)]):
                resistance_bute[numero_case] = data["asklow"].iloc[(nb - 1) * (-1)]
                espacement = 0
            else:
                espacement += 1
            if(espacement >= nb_bougie_espacement):
                numero_case += 1
                espacement = 0
            if(numero_case >= numero_case_max):
                espacement = 0
                numero_case = 0
                break
        for nb in range(nb_bougie):
            if(resistance_bute_5m[numero_case] >= 0):
                resistance_bute_5m[numero_case] = data5m["asklow"].iloc[(nb - 1) * (-1)]
            if(resistance_bute_5m[numero_case] < data5m["asklow"].iloc[(nb - 1) * (-1)]):
                resistance_bute_5m[numero_case] = data5m["asklow"].iloc[(nb - 1) * (-1)]
                espacement = 0
            else:
                espacement += 1
            if(espacement >= nb_bougie_espacement):
                numero_case += 1
                espacement = 0
            if(numero_case >= numero_case_max):
                espacement = 0
                numero_case = 0
                break
        for nb in range(nb_bougie):
            if(resistance_bute_15m[numero_case] >= 0):
                resistance_bute_15m[numero_case] = data15m["asklow"].iloc[(nb - 1) * (-1)]
            if(resistance_bute_15m[numero_case] < data15m["asklow"].iloc[(nb - 1) * (-1)]):
                resistance_bute_15m[numero_case] = data15m["asklow"].iloc[(nb - 1) * (-1)]
                espacement = 0
            else:
                espacement += 1
            if(espacement >= nb_bougie_espacement):
                numero_case += 1
                espacement = 0
            if(numero_case >= numero_case_max):
                espacement = 0
                numero_case = 0
                break
        if((support_bute[0] <= (support_bute[1] - (support_bute[1] * marge_difference))) and (support_bute[1] <= (support_bute[2] - (support_bute[2] * marge_difference)))):
            support_ascendant = True
            if((support_bute_5m[0] <= (support_bute_5m[1] - (support_bute_5m[1] * marge_difference))) and (support_bute_5m[1] <= (support_bute_5m[2] - (support_bute_5m[2] * marge_difference)))):
                support_ascendant_5m = True
                tendance_ascendant_5m = True
                if((support_bute_15m[0] <= (support_bute_15m[1] - (support_bute_15m[1] * marge_difference))) and (support_bute_15m[1] <= (support_bute_15m[2] - (support_bute_15m[2] * marge_difference)))):
                    support_ascendant_15m = True
                    tendance_ascendant = True
        if((support_bute_5m[0] <= (support_bute_5m[1] - (support_bute_5m[1] * marge_difference))) and (support_bute_5m[1] <= (support_bute_5m[2] - (support_bute_5m[2] * marge_difference)))):
            support_ascendant_5m = True
        if((support_bute_15m[0] <= (support_bute_15m[1] - (support_bute_15m[1] * marge_difference))) and (support_bute_15m[1] <= (support_bute_15m[2] - (support_bute_15m[2] * marge_difference)))):
            support_ascendant_15m = True
        if((support_bute[0] >= (support_bute[1] + (support_bute[1] * marge_difference))) and (support_bute[1] >= (support_bute[2] + (support_bute[2] * marge_difference)))):
            support_descendant = True
        if((support_bute_5m[0] >= (support_bute_5m[1] + (support_bute_5m[1] * marge_difference))) and (support_bute_5m[1] >= (support_bute_5m[2] + (support_bute_5m[2] * marge_difference)))):
            support_descendant_5m = True
        if((support_bute_15m[0] >= (support_bute_15m[1] + (support_bute_15m[1] * marge_difference))) and (support_bute_15m[1] >= (support_bute_15m[2] + (support_bute_15m[2] * marge_difference)))):
            support_descendant_15m = True
        if(((support_bute[0] > (support_bute[1] - (support_bute[1] * marge_difference))) and (support_bute[0] < (support_bute[1] + (support_bute[1] * marge_difference)))) and ((support_bute[1] > (support_bute[2] - (support_bute[1] * marge_difference))) and (support_bute[1] < (support_bute[1] + (support_bute[2] * marge_difference))))):
            support_horizontal = True
        
        if((resistance_bute[0] <= (resistance_bute[1] - (resistance_bute[1] * marge_difference))) and (resistance_bute[1] <= (resistance_bute[2] - (resistance_bute[2] * marge_difference)))):
            resistance_ascendant = True
        if((resistance_bute_5m[0] <= (resistance_bute_5m[1] - (resistance_bute_5m[1] * marge_difference))) and (resistance_bute_5m[1] <= (resistance_bute_5m[2] - (resistance_bute_5m[2] * marge_difference)))):
            resistance_ascendant_5m = True
        if((resistance_bute_15m[0] <= (resistance_bute_15m[1] - (resistance_bute_15m[1] * marge_difference))) and (resistance_bute_15m[1] <= (resistance_bute_15m[2] - (resistance_bute_15m[2] * marge_difference)))):
            resistance_ascendant_15m = True
        if((resistance_bute[0] >= (resistance_bute[1] + (resistance_bute[1] * marge_difference))) and (resistance_bute[1] >= (resistance_bute[2] + (resistance_bute[2] * marge_difference)))):
            resistance_descendant = True
            if((resistance_bute_5m[0] >= (resistance_bute_5m[1] + (resistance_bute_5m[1] * marge_difference))) and (resistance_bute_5m[1] >= (resistance_bute_5m[2] + (resistance_bute_5m[2] * marge_difference)))):
                resistance_descendant_5m = True
                tendance_descendant_5m = True
                if((resistance_bute_15m[0] >= (resistance_bute_15m[1] + (resistance_bute_15m[1] * marge_difference))) and (resistance_bute_15m[1] >= (resistance_bute_15m[2] + (resistance_bute_15m[2] * marge_difference)))):
                    resistance_ascendant_15m = True
                    tendance_descendant = True
        if((resistance_bute_5m[0] >= (resistance_bute_5m[1] + (resistance_bute_5m[1] * marge_difference))) and (resistance_bute_5m[1] >= (resistance_bute_5m[2] + (resistance_bute_5m[2] * marge_difference)))):
            resistance_descendant_5m = True
        if((resistance_bute_15m[0] >= (resistance_bute_15m[1] + (resistance_bute_15m[1] * marge_difference))) and (resistance_bute_15m[1] >= (resistance_bute_15m[2] + (resistance_bute_15m[2] * marge_difference)))):
            resistance_descendant_15m = True
        if(((resistance_bute[0] > (resistance_bute[1] - (resistance_bute[1] * marge_difference))) and (resistance_bute[0] < (resistance_bute[1] + (resistance_bute[1] * marge_difference)))) and ((resistance_bute[1] > (resistance_bute[2] - (resistance_bute[1] * marge_difference))) and (resistance_bute[1] < (resistance_bute[1] + (resistance_bute[2] * marge_difference))))):
            resistance_horizontal = True
        
        # teste canaux
        if(support_ascendant == True and resistance_ascendant == True):
            canaux_ascendant = True
            if(support_ascendant_5m == True and resistance_ascendant_5m == True):
                tendance_ascendant_5m = True
                if(support_ascendant_15m == True and resistance_ascendant_15m == True):
                    tendance_ascendant = True
        if(support_descendant == True and resistance_descendant == True):
            canaux_descendant = True
            if(support_descendant_5m == True and resistance_descendant_5m == True):
                tendance_descendant_5m = True
                if(support_descendant_15m == True and resistance_descendant_15m == True):
                    tendance_descendant = True
        if(support_horizontal == True and resistance_horizontal == True):
            canaux_horizontal = True
        
        # teste triangle
        if(support_horizontal == True and resistance_ascendant == True):
            triangle_ascendant = True
            #tendance_ascendant = True
        if(support_descendant == True and resistance_horizontal == True):
            triangle_descendant = True
            #tendance_descendant = True
        if(support_descendant == True and resistance_ascendant == True):
            triangle_asymetrique = True

        # teste elargissement
        if(support_ascendant == True and resistance_horizontal == True):
            elargissement_ascendant = True
        if(support_horizontal == True and resistance_descendant == True):
            elargissement_descendant = True
        if(support_ascendant == True and resistance_descendant == True):
            elargissement_asymetrique = True

        # double triple top bottom
        if(support_horizontal):
            double_bottom = True
            triple_bottom = True
            epaule_tete_epaule_inverse = True
        if(resistance_horizontal):
            triple_bottom = True
            double_bottom = True
            epaule_tete_epaule = True

        # avalement de retournement haussier et baissier
        if(data["askclose"].iloc[-3] >= data["askclose"].iloc[-2] and data["askopen"].iloc[-3] <= data["askopen"].iloc[-2] and data["askopen"].iloc[-2] > data["askclose"].iloc[-2] and (abs(data["askopen"].iloc[-3] - data["askclose"].iloc[-3]) < abs(data["askopen"].iloc[-2] - data["askclose"].iloc[-2]))):
            avalement_baissier = True
        if(data["askclose"].iloc[-3] <= data["askclose"].iloc[-2] and data["askopen"].iloc[-3] >= data["askopen"].iloc[-2] and data["askopen"].iloc[-2] < data["askclose"].iloc[-2] and (abs(data["askopen"].iloc[-3] - data["askclose"].iloc[-3]) < abs(data["askopen"].iloc[-2] - data["askclose"].iloc[-2]))):
            avalement_haussier = True
        
        # marteau de retournement haussier et baissier
        if(abs(data["askclose"].iloc[-2] - data["askopen"].iloc[-2]) < ((data["askhigh"].iloc[-2] - data["asklow"].iloc[-2])/4) and (abs(data["askhigh"].iloc[-2] - data["askclose"].iloc[-2]) > abs((data["askclose"].iloc[-2] - data["asklow"].iloc[-2]) * 3))):
            marteau_retournement_baissier = True
        if(abs(data["askclose"].iloc[-2] - data["askopen"].iloc[-2]) < ((data["askhigh"].iloc[-2] - data["asklow"].iloc[-2])/4) and (abs(data["askclose"].iloc[-2] - data["asklow"].iloc[-2]) > abs((data["askhigh"].iloc[-2] - data["askclose"].iloc[-2]) * 3))):
            marteau_retournement_haussier = True

        # buy position
        """ if(avalement_haussier == True or marteau_retournement_haussier == True or triple_bottom == True or double_bottom == True or epaule_tete_epaule_inverse == True):
            operation = -1
            SetStopLoss(-2)
            SetTakeProfit(10) """
        # sell position
        """ if(avalement_baissier == True or marteau_retournement_baissier == True or triple_top == True or double_top == True or epaule_tete_epaule == True):
            operation = 1
            SetStopLoss(-2)
            SetTakeProfit(10) """
        return True
    except Exception as e:
        print(">>> Erreur durant l'étude des figures chartiste', source d'erreur :", e)
        return False
    

GetTradeStatus()

while(trade == True):
    #Connection()
    #SetAccountId(accountid)
    #GetAccountId()
    try:
        print(">>> !!! Connexion !!!")
        #Connection()
        connected = Connection()
        for td_id in GetTradeIds():
            SetStopLimite(td_id, tp_encours, sl_encours)
        while(connected == True and trade == True):
            # forcena mampiditra sl sy tp eto fa misy fotoana tsy tafiditra ilay izy
            for td_id in GetTradeIds():
                SetStopLimite(td_id, tp_encours, sl_encours)
            GetTailleLot()
            if(GetNombrePosition() < max_position):
                # eto no atao ny fonction de trading no antsoina
                try:
                    print(">>> Récupération des symboles à traiter")
                    GetPairList()
                except Exception as e:
                    print(">>> Erreur durant la récupération des symboles, source d'erreur :", e)
                    print(">>> Erreur lors de la récupération des symboles à traiter")
                    pass
                finally:
                    print(">>> Fin de la récupération des symboles à traiter")
                print(">>> Début du traitement des pairs")
                for pairs in pairs_list:
                    GetPositionMax()
                    GetTailleLot()
                    if(GetNombrePosition() < max_position):
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
                            # mijery ny date ahafahana manapaka ny trading week-end
                            num_jour = aujourdhui.weekday()
                            jour_ouvrable = True
                            if(num_jour == 5 or num_jour == 6):
                                jour_ouvrable = False
                            if(num_jour == 4 and aujourdhui.hour == 23):
                                jour_ouvrable = False
                            if(jour_ouvrable == False):
                                pass
                            if(is_recup == True):
                                #print(data.head())
                                is_trait = DataTraitement()
                                if(is_trait == True):
                                    is_pred = Preditcion()
                                    is_pred = EtudeChartiste(pair)
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
                            #SetTakeProfit(tp_test)
                            #SetStopLoss(sl_test)
                            if(operation == 0):
                                print(">>> Aucune trade éffectuée !!!")
                                operation = 0
                            if(operation == 1):
                                if(SetBuyPosition(pair, lot_test, tp_encours, sl_encours)):
                                #if(True):
                                    print("######################## Opération buy effectuée ########################")
                                else:
                                    print("######################## Opération buy échouée!!! ########################")
                                operation = 0
                            if(operation == -1):
                                if(SetSellPosition(pair, lot_test, tp_encours, sl_encours)):
                                #if(True):
                                    print("######################## Opération sell effectuée ########################")
                                else:
                                    print("######################## Opération sell échouée!!! ########################")
                                operation = 0
                            print(">>> Fin traitement opération trading")
                            print(">>> Nombre de position actuelle :", GetNombrePosition()) 
                            max_ask = 0.0
                            max_bid = 0.0
                            min_ask = 0.0
                            min_bid = 0.0
                        except Exception as e:
                            compteur = compteur + 1
                            print(">>> Erreur durant le traitement du pair, source d'erreur :", e)
                            print(">>> !!! Une erreur s'est produite durant le traitement du marché", pair," !!!")
                            pass
                            #break
                        finally:
                            try:
                                UnSetTicket(pair)
                            except:
                                print("pair non déconnectér")                 
                            if(compteur >= compteur_limite):
                                compteur = 0
                                break
                            print(">>> !!! Deconnexion du symbole", pair, "!!!")  
                            max_ask = 0.0
                            max_bid = 0.0
                            min_ask = 0.0
                            min_bid = 0.0
                            tm.sleep(60) 
                            try:
                                for td_id in GetTradeIds():
                                    SetStopLimite(td_id, tp_encours, sl_encours)
                            except:
                                break
                    else:
                        tm.sleep(60)    
                        for td_id in GetTradeIds():
                            SetStopLimite(td_id, tp_encours, sl_encours)          
                if(compteur >= compteur_limite):
                    compteur = 0
                    break
            GetTradeStatus()
    except Exception as e:
        print(">>> Erreur de connexion, source d'erreur :", e)
        pass
    finally:
        for td_id in GetTradeIds():
            SetStopLimite(td_id, tp_encours, sl_encours)
        if(connected == True):
            connected = Deconnection()
        else:
            print(">>> Aucun compte connecter")
        tm.sleep(60)
        GetTradeStatus() 
        max_ask = 0.0
        max_bid = 0.0
        min_ask = 0.0
        min_bid = 0.0