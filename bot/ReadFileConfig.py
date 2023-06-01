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
                if parametre == "PairList":
                    self.trade_status = valeur
                if parametre == "PairList":
                    self.account = valeur
                if parametre == "PairList":
                    self.nombre_max_position = valeur
                if parametre == "PairList":
                    self.lot = valeur
                if parametre == "PairList":
                    self.source_type = valeur
                if parametre == "PairList":
                    self.take_profit = valeur
                if parametre == "PairList":
                    self.stop_loss = valeur
                if parametre == "PairList":
                    self.pair_list = valeur
    
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
            return self.pair_list       
