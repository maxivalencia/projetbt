#!/usr/bin/python3

import time as tm
from datetime import timedelta, date, time, datetime
import calendar
import os
import pandas as pd
import numpy as np
from ReadFileConfig import ReadFileConfig
from fxcmapi import fxcmapi
from GetData import GetData
from DataPrediction import DataPrediction
from DataChartiste import DataChartiste
from DataTraitement import DataTraitement

""" config_file_name = "FXCM.cfg"
server = 'demo' #type de serveur demo ou real """

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

while(True):
    #Connection()
    #SetAccountId(accountid)
    #GetAccountId()
    fx = fxcmapi()
    file = ReadFileConfig()
    connected = False
    try:        
        if(file.GetTradeStatus() == True):
            break
        print(">>> !!! Connexion !!!")
        connected = fx.Connection(file.GetServer(), file.GetConfigFileName())
        for td_id in fx.GetTradeIds():
            fx.SetStopLimite(td_id, file.GetTakeProfit(), file.GetStopLoss())
        while(connected == True and file.GetTradeStatus() == True):
            # forcena mampiditra sl sy tp eto fa misy fotoana tsy tafiditra ilay izy
            file.ReadConfig()
            for td_id in fx.GetTradeIds():
                fx.SetStopLimite(td_id, file.GetTakeProfit(), file.GetStopLoss())
            lot = file.GetLot()
            if(fx.GetNombrePosition() < file.GetNombrePositionMax()):
                # eto no atao ny fonction de trading no antsoina
                try:
                    print(">>> Récupération des symboles à traiter")
                    ReadFileConfig.GetPairList()
                except Exception as e:
                    print(">>> Erreur durant la récupération des symboles, source d'erreur :", e)
                    print(">>> Erreur lors de la récupération des symboles à traiter")
                    pass
                finally:
                    print(">>> Fin de la récupération des symboles à traiter")
                print(">>> Début du traitement des pairs")
                for pair in file.GetPairList():
                    lot = file.GetLot()
                    operation = 0
                    if(fx.GetNombrePosition() < file.GetNombrePositionMax()):
                        if(file.GetTradeStatus() == True):
                            break
                        print(">>> Traitement du pair", pair)
                        try:
                            fx.SetTicket(pair)
                            print(">>> !!! Connexion du symbol", pair, "!!!")
                            #if (GetTicket() == pair):
                            print(">>> Début traitement du symbole", pair)
                            gdata = GetData(fx.GetConnection() ,pair, file.GetTimeFrame1())
                            is_recup = False
                            is_recup, data, aujour = gdata.DataRecuperation()
                            # mijery ny date ahafahana manapaka ny trading week-end
                            aujourdhui = datetime.now()
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
                                tdata = DataTraitement(data)
                                is_trait = False
                                is_trait, data = tdata.GetDataTraitement()
                                if(is_trait == True):
                                    is_chart = False
                                    cdata = DataChartiste(pair, data, fx.GetConnection(), file.GetTimeFrame2(), file.GetTimeFrame3())
                                    is_chart, tendance_ascendant_1, tendance_descendant_1, tendance_ascendant_2, tendance_descendant_2 = cdata.EtudeChartiste()
                                    if(is_chart == True):
                                        is_pred = False
                                        pdata = DataPrediction(data)
                                        is_pred, operation = pdata.Preditcion(tendance_ascendant_1, tendance_descendant_1, tendance_ascendant_2, tendance_descendant_2)
                                        """ is_pred = EtudeChartiste(pair) """
                                        if(is_pred == False):
                                            print(">>> Prédiction non effectuée")
                                    else:
                                        print(">>> Sans Chartiste")
                                else:
                                    print(">>> Donnée non traiter")
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
                                if(fx.SetBuyPosition(pair, lot, file.GetTakeProfit(), file.GetStopLoss())):
                                #if(True):
                                    print("######################## Opération buy effectuée ########################")
                                else:
                                    print("######################## Opération buy échouée!!! ########################")
                                operation = 0
                            if(operation == -1):
                                if(fx.SetSellPosition(pair, lot, file.GetTakeProfit(), file.GetStopLoss())):
                                #if(True):
                                    print("######################## Opération sell effectuée ########################")
                                else:
                                    print("######################## Opération sell échouée!!! ########################")
                                operation = 0
                            print(">>> Fin traitement opération trading")
                            print(">>> Nombre de position actuelle :", fx.GetNombrePosition()) 
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
                                fx.UnSetTicket(pair)
                            except:
                                print("pair non déconnectér")                 
                            if(compteur >= file.GetCompteurLimite()):
                                compteur = 0
                                break
                            print(">>> !!! Deconnexion du symbole", pair, "!!!")  
                            max_ask = 0.0
                            max_bid = 0.0
                            min_ask = 0.0
                            min_bid = 0.0
                            tm.sleep(60) 
                            try:
                                for td_id in fx.GetTradeIds():
                                    fx.SetStopLimite(td_id, file.GetTakeProfit(), file.GetStopLoss())
                            except:
                                break
                    else:
                        tm.sleep(60)    
                        for td_id in fx.GetTradeIds():
                            fx.SetStopLimite(td_id, file.GetTakeProfit(), file.GetStopLoss())          
                if(compteur >= file.GetCompteurLimite()):
                    compteur = 0
                    break
            file.GetTradeStatus()
    except Exception as e:
        print(">>> Erreur de connexion, source d'erreur :", e)
        pass
    finally:
        for td_id in fx.GetTradeIds():
            fx.SetStopLimite(td_id, file.GetTakeProfit(), file.GetStopLoss())
        if(connected == True):
            connected = fx.Deconnection()
        else:
            print(">>> Aucun compte connecter")
        tm.sleep(60)
        max_ask = 0.0
        max_bid = 0.0
        min_ask = 0.0
        min_bid = 0.0        
        if(file.GetTradeStatus() == True):
            break