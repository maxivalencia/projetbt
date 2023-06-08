#!/usr/bin/python3

import fxcmpy
class DataCandle:
    def __init__(self, data):
        self.data = data

    def MarteauHaussier(self):
        if(self.data['askclose'][-2]):
            return True
        return False
    
    def MarteauBaissier(self):
        return False
    
    def AvalementHaussier(self):
        return False
    
    def AvalementBaissier(self):
        return False
    
    def HaramiHaussier(self):
        return False
    
    def HaramiBaissier(self):
        return False
    
    def InsideBarHaussier(self):
        return False
    
    def InsideBarBaissier(self):
        return False