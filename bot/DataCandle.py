#!/usr/bin/python3

import fxcmpy
class DataCandle:
    def __init__(self, data):
        self.data = data

    def MarteauHaussier(self):
        if((((abs(self.data['askclose'][-2] - self.data['askopen'][-2])) * 3) <= (self.data['askhigh'][-2] - self.data['asklow'][-2])) and (((abs(self.data['askclose'][-2] - self.data['askopen'][-2])) >= ((self.data['askhigh'][-2] - self.data['askclose'][-2]) * 4)) or ((abs(self.data['askclose'][-2] - self.data['askopen'][-2])) >= ((self.data['askhigh'][-2] - self.data['askopen'][-2]) * 4)))):
            return True
        return False
    
    def MarteauBaissier(self):
        if((((abs(self.data['askclose'][-2] - self.data['askopen'][-2])) * 3) <= (self.data['askhigh'][-2] - self.data['asklow'][-2])) and (((abs(self.data['askclose'][-2] - self.data['askopen'][-2])) >=((self.data['askclose'][-2] - self.data['asklow'][-2]) * 4)) or ((abs(self.data['askclose'][-2] - self.data['askopen'][-2])) >= ((self.data['askopen'][-2] - self.data['asklow'][-2]) * 4)))):
            return True
        return False
    
    def AvalementHaussier(self):
        if(self.data['askclose'][-3] <= self.data['askclose'][-2] and self.data['askopen'][-3] >= self.data['askopen'][-2] and self.data['askclose'][-3] <= self.data['askopen'][-3] and self.data['askclose'][-2] >= self.data['askopen'][-2] and abs(self.data['askopen'][-3] - self.data['askclose'][-3]) < abs(self.data['askopen'][-2] - self.data['askclose'][-2])):
            return True
        return False
    
    def AvalementBaissier(self):
        if(self.data['askclose'][-3] >= self.data['askclose'][-2] and self.data['askopen'][-3] <= self.data['askopen'][-2] and self.data['askclose'][-3] >= self.data['askopen'][-3] and self.data['askclose'][-2] <= self.data['askopen'][-2] and abs(self.data['askopen'][-3] - self.data['askclose'][-3]) < abs(self.data['askopen'][-2] - self.data['askclose'][-2])):
            return True
        return False
    
    def HaramiHaussier(self):
        if(self.data['askclose'][-3] <= self.data['askclose'][-2] and self.data['askopen'][-2] <= self.data['askopen'][-3] and self.data['askclose'][-2] >= self.data['askopen'][-2] and self.data['askclose'][-3] <= self.data['askopen'][-3] and abs(self.data['askopen'][-2] - self.data['askclose'][-2]) < abs(self.data['askopen'][-3] - self.data['askclose'][-3])):
            return True
        return False
    
    def HaramiBaissier(self):
        if(self.data['askclose'][-3] >= self.data['askclose'][-2] and self.data['askopen'][-2] >= self.data['askopen'][-3] and self.data['askclose'][-2] <= self.data['askopen'][-2] and self.data['askclose'][-3] >= self.data['askopen'][-3] and abs(self.data['askopen'][-2] - self.data['askclose'][-2]) < abs(self.data['askopen'][-3] - self.data['askclose'][-3])):
            return True
        return False
    
    def InsideBarHaussier(self):
        if(self.data['askhigh'][-3] > self.data['askhigh'][-2] and self.data['asklow'][-3] < self.data['asklow'][-2] and self.data['askclose'][-2] > self.data['askopen'][-2]):
            return True
        return False
    
    def InsideBarBaissier(self):
        if(self.data['askhigh'][-3] > self.data['askhigh'][-2] and self.data['asklow'][-3] < self.data['asklow'][-2] and self.data['askclose'][-2] < self.data['askopen'][-2]):
            return True
        return False