#!/usr/bin/python3

### ------ Fonction de récupération des données ------ ###

import pandas as pd
import numpy as np
from numpy import loadtxt
import os.path
import os
import time as tm
from datetime import timedelta, date, time
from datetime import datetime
import fxcmapi

### ------ Fonction de récupération des données ------ ###
class GetData:
    def __init__(self, con, pair, timeframe = "m1", max_windows = 10000):
        self.max_windows = max_windows
        self.pair = pair
        self.timeframe = timeframe
        pairs = self.pair.split('/')
        self.pair = pairs[0] + pairs[1]
        self.fichier = self.pair + "_" + self.timeframe + ".csv"
        self.dossier = './Data/'
        self.filename = self.dossier + self.fichier
        self.con = con

    def GetDataFromFile(self):
        try:
            if os.path.isfile(self.filename):
                self.data = pd.read_csv(self.filename, sep=';')  
                self.data = self.data.set_index(['date'])
                self.data.index = pd.to_datetime(self.data.index)
            else:
                return False
            return True
        except Exception as e:
            print(">>> Erreur lors de lecture des données depuis le fichier, source d'erreur :", e)
            return False

    def SetDataToFile(self):
        try:
            if os.path.isdir(self.dossier):
                if os.path.isfile(self.filename):
                    os.remove(self.filename)
                self.data.to_csv(self.filename, sep=';', encoding='utf-8')
            else:
                os.mkdir(self.dossier, mode = 0o777)
                self.data.to_csv(self.filename, sep=';', encoding='utf-8')
            return True
        except Exception as e:
            print(">>> Erreur lors de l'enregistrement des données dans un fichier, source d'erreur :", e)
            return False
        
    def DataRecuperation(self, pair, timeframe):        
        try:
            data1 = self.GetDataFromFile(self.pair)
            if(self.con.is_subscribed(pair)):
                print(">>> Début de la récupération des données du symbol", self.pair)
                #mbola amboarina rehefa milamina ny code
                #data1 = False
                if (data1 == True):
                    start = self.data.index[-1] # + timedelta(minutes = 1)
                    end = datetime.now()
                    #data2 = con.get_candles(pair, period=timeframe, start=start, end=end)
                    self.data = self.data.drop(start, axis=0)
                    data2 = self.con.get_candles(self.pair, period=self.timeframe, start=start, end=end)
                    data3 = pd.concat([self.data, data2])
                    self.data = data3
                else:
                    start = datetime.now() - timedelta(minutes = self.max_windows)
                    #end = datetime.now()
                    #data2 = con.get_candles(pair, period=timeframe, start=start, end=end)
                    data2 = self.con.get_candles(self.pair, period=self.timeframe, number=10000)
                    self.data = data2
                length_data_save = self.max_windows * 10
                last = self.data.index[-1] - timedelta(minutes = length_data_save)            
                for dt in self.data.index:
                    if(dt < last):
                        self.data = self.data.drop(dt, axis=0)
                save = self.SetDataToFile(self.pair)
                #data = con.get_candles(pair, period=timeframe) #, number=2500)
                #data = con.get_candles(pair, period=timeframe, number=2500)
                aujourdhui = self.data.index[-1]
                print(">>> Fin de la récupération des données")
                return True, self.data, aujourdhui
        except Exception as e:
            print(">>> !!! Erreur lors de la récupération des données !!!")
            print(">>> Source d'erreur :", e)
        return False
        # les colonnes du tableau : date, bidopen, bidclose, bidhigh, bidlow, askopen, askclose, askhigh, asklow, tickqty
        # ask ambonin'ny bid
        #print(data.head())
        #data = yf.download(pair, start=start, end=end, interval=timeframe)

