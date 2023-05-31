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

# fonction ahafahana manao ny calcul ny nombre de lot tokony azo atao trade
def SetNombreLot():
    global lot_test
    try:
        lot_test = 1
    except Exception as e:
        print(">>> Erreur de la modification du nombre de lot, source d'erreur :", e)
        return False
    return True


"""
def GetInfoTrade():
    global con
    global info
    info = con.get_accounts().T
    print(info)
"""

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