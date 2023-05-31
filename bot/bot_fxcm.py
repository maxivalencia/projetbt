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