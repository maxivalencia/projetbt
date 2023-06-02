#!/usr/bin/python3

import os.path
import os
class ReadFileConfig:
    def __init__(self, filename="config.tcf"):
        self.filename = filename

    def ReadConfig(self):
        with open(self.filename, "r") as f:
            lines = f.readlines()
            for line in lines:
                ls = line.split("=")
                parametre = ls[0].strip()
                valeur = ls[1].strip()
                if parametre == "IsTrade":
                    self.trade_status = valeur
                if parametre == "AccountId":
                    self.account = valeur
                if parametre == "NombrePosition":
                    self.nombre_max_position = valeur
                if parametre == "Lot":
                    self.lot = valeur
                if parametre == "SourceType":
                    self.source_type = valeur
                if parametre == "TakeProfit":
                    self.take_profit = valeur
                if parametre == "StopLoss":
                    self.stop_loss = valeur
                if parametre == "Pairlist":
                    self.pair_list = valeur
                if parametre == "TimeFrame1":
                    self.timeframe1 = valeur
                if parametre == "TimeFrame2":
                    self.timeframe2 = valeur
                if parametre == "TimeFrame3":
                    self.timeframe3 = valeur
                if parametre == "CompteurLimite":
                    self.compteur_limite = valeur
                if parametre == "Server":
                    self.server = valeur
                if parametre == "ConfigFileName":
                    self.config_file_name = valeur
    
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
        if(self.source_type == 'File'):
            return self.pair_list.split(",")  

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
