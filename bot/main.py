#!/bin/bash
import pandas as pd
import numpy as np
from getdata import *
from prediction import *
from readfile import *
from datatraitement import *
import datetime as datetime
#import datetime
import time

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
temps_min_ask = datetime.datetime.now()
temps_min_bid = datetime.datetime.now()
temps_max_ask = datetime.datetime.now()
temps_max_bid = datetime.datetime.now()
temps_coupure = datetime.datetime.now()
trade = False
status_file = "OkTrade.txt"
account_file = "AccountId.txt"
nb_position_file = "NombrePosition.txt"
con = ''
max_position = 10
connected = False
compteur = 0
compteur_limite = 1000

def SetTakeProfit(tp):
    global tp_encours
    tp_encours = tp
    return True

def SetStopLoss(sl):
    global sl_encours
    sl_encours = sl
    return True

# fonction ahafahana manao ny calcul ny nombre de lot tokony azo atao trade
def SetNombreLot():
    global lot_test
    lot_test = 1
    return True

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
                for pairs in pairs_list:
                    max_position = GetPositionMax()
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
                            print(">>> Nombre de position acutelle :", GetNombrePosition())
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
  