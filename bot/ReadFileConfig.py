#!/usr/bin/python3

import os.path
import os
class ReadFileConfig:
    def __init__(self, filename="config.tcf"):
        self.filename = filename
        self.pair_list = []
        self.lot = 1
        self.nombre_max_position = 10
        self.timeframe1 = ""
        self.timeframe2 = ""
        self.timeframe3 = ""
        self.trade_status = False
        self.source_type = "File"
        self.take_profit = 5
        self.stop_loss = 2
        self.account = ""
        self.compteur_limite = 10
        self.server = "demo"
        self.config_file_name = "FXCM.cfg"
        self.window = 20

    def ReadConfig(self):
        with open(self.filename, "r") as f:
            lines = f.readlines()
            for line in lines:
                ls = line.split("=", 1)
                parametre = ls[0].strip()
                valeur = ls[1].strip()
                if parametre == "IsTrade":
                    if(valeur == "True"):
                        self.trade_status = True
                    else:
                        self.trade_status = False
                if parametre == "AccountId":
                    self.account = valeur
                if parametre == "NombrePosition":
                    self.nombre_max_position = int(valeur)
                if parametre == "Lot":
                    self.lot = int(valeur)
                if parametre == "SourceType":
                    self.source_type = valeur
                if parametre == "TakeProfit":
                    self.take_profit = int(valeur)
                if parametre == "StopLoss":
                    self.stop_loss = int(valeur)
                if parametre == "Pairlist":
                    self.pair_list = valeur.split(",") 
                if parametre == "TimeFrame1":
                    self.timeframe1 = valeur
                if parametre == "TimeFrame2":
                    self.timeframe2 = valeur
                if parametre == "TimeFrame3":
                    self.timeframe3 = valeur
                if parametre == "CompteurLimite":
                    self.compteur_limite = int(valeur)
                if parametre == "Server":
                    self.server = valeur
                if parametre == "ConfigFileName":
                    self.config_file_name = valeur
                if parametre == "Window":
                    self.window = int(valeur)
    
    def GetTradeStatus(self):
        return self.trade_status
        
    def GetAccountId(self):
        return self.account
        
    def GetNombrePositionMax(self):
        return self.nombre_max_position
    
    def GetLot(self):
        return self.lot

    def GetSourceType(self):
        return self.source_type

    def GetTakeProfit(self):
        return self.take_profit

    def GetStopLoss(self):
        return self.stop_loss
    
    # récupération des pairs à traiter
    def GetPairList(self):
        #if(self.source_type == 'File'):
        return self.pair_list 

    def GetTimeFrame1(self):
        return self.timeframe1

    def GetTimeFrame2(self):
        return self.timeframe2

    def GetTimeFrame3(self):
        return self.timeframe3   

    def GetCompteurLimite(self):
        return self.compteur_limite

    def GetServer(self):
        return self.server

    def GetConfigFileName(self):
        return self.config_file_name

    def GetWindow(self):
        return self.window
