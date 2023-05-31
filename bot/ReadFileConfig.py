#!/usr/bin/python3

import os.path
import os
class ReadFileConfig:
    def GetTradeStatus(status_file):
        global trade
        f = open(status_file, "r")
        if((f.read() == "True") or (f.read() == "true") or (f.read() == "TRUE") or (f.read() == "t") or (f.read() == "T")):
            trade = True
        else:
            trade = False
        f.close()
        
    def GetAccountIdFromFile(account_file):
        global trade
        f = open(account_file, "r")
        account = f.read()
        SetAccountId(account)
        f.close()
        
    def GetPositionMax(nb_position_file):
        #global max_position
        f = open(nb_position_file, "r")
        max_position = int(f.read())
        f.close()
        return max_position