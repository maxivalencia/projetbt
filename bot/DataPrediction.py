#!/usr/bin/python3

import pandas as pd
import numpy as np
from numpy import loadtxt
from datetime import datetime
from sklearn.linear_model import LinearRegression
from datetime import timedelta
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

### ------ Fonction de prévision ------ ### 
class DataPrediction:
    def __init__(self, data):
        self.data = data
        self.max_ask = 0.0
        self.max_bid = 0.0
        self.min_ask = 0.0
        self.min_bid = 0.0
        self.temps_min_ask = datetime.now()
        self.temps_min_bid = datetime.now()
        self.temps_max_ask = datetime.now()
        self.temps_max_bid = datetime.now()
        self.temps_coupure = datetime.now()

    def Preditcion(self, tendance_ascendant, tendance_descendant, tendance_ascendant_5m, tendance_descendant_5m):
        operation = 0
        rsi_sell_limite = 30
        rsi_buy_limite = 70
        cci_sell_limite = -100
        cci_buy_limite = 100
        try:
            print(">>> Début de la prédiction")
            # traitement
            df = self.data
            #capital = capital_test
            #risque = risque_test
            """ gain = roi_min_test
            lot = lot_test """
            #valeur_pip = valeur_pip_test
            #sl_en_dollar = capital * risque
            #sl_en_pips = (sl_en_dollar * valeur_pip)    
            XXs = []
            for t in pd.DataFrame(df.index).values:
                XXs.append(t)
            XX = pd.DataFrame(XXs)
            #print(XX.head())
            #print(XXs.head())
            yy_ask = df.askclose
            yy_bid = df.bidclose
            #print(yy_ask.head())
            XX_ask = df.drop(['askclose'], axis=1)
            XX_bid = df.drop(['bidclose'], axis=1)  
            # nasiana an'ito ilay declaration hijerevana ny résultat fit_intercept = True      
            try:
                XX_train_ask, XX_test_ask, yy_train_ask, yy_test_ask = train_test_split(df.index.values.reshape(-1, 1), yy_ask, test_size=0.2, random_state=0)
                models_ask = LinearRegression(fit_intercept = True)
                #models_ask.fit(XX_train_ask, yy_train_ask)
                # teste model asiana to_frame ny eto
                models_ask.fit(df.index.values.reshape(-1, 1), yy_ask)
                #poly_ask = np.polyfit(x=df.index, y=yy_ask)
                #models_ask.fit(df.index.values.reshape(-1, 1), yy_ask)
            except Exception as e:
                print(">>> Erreur du traitement de la regréssion linéaire du ask, source d'erreur :", e)
            
            try:
                XX_train_bid, XX_test_bid, yy_train_bid, yy_test_bid = train_test_split(df.index.values.reshape(-1, 1), yy_bid, test_size=0.2, random_state=0)
                models_bid = LinearRegression(fit_intercept = True)
                #models_bid.fit(XX_train_bid, yy_train_bid) 
                # teste model asiana to_frame ny eto
                models_bid.fit(df.index.values.reshape(-1, 1), yy_bid) 
                #models_bid.fit(df.index.values.reshape(-1, 1), yy_bid) 
            except Exception as e:
                print(">>> Erreur du traitement de la regréssion linéaire du bid, source d'erreur :", e)
                
            Xyy = df.index
            #print(df.index.values.reshape(-1, 1))
            # test fijerevana ny contenue 
            #print(XX_test_ask.head())
            #print(yy_test_ask.head())
            """
            XX = np.array(df.index).reshape(-1, 1)
            yy_ask = np.array(yy_ask).reshape(-1, 1)
            yy_bid = np.array(yy_bid).reshape(-1, 1)
            models_ask = LinearRegression()
            models_bid = LinearRegression()
            models_ask.fit(XX, yy_ask)
            models_bid.fit(XX, yy_bid)
            #models_bid.fit(XX, yy)
            """
            currTime = Xyy[-1]
            #floored = pd.to_datetime(currTime).ceil('H').to_pydatetime()
            heure_pred = currTime
            #yy_pred_ask = models_ask.predict([[heure_pred]])
            #yy_pred_bid = models_bid.predict([[heure_pred]])
            #calcul max et min bid et ask sur 15mn future
            
            # miandry etude manao kajy valeur objectif amin'ny prédiction
            for i in range(15):
                i = i + 1
                heure_test = heure_pred + timedelta(minutes = i)
                temps_coupure = heure_test   
                #print("########## Tonga eto ##########")
                #print(models_ask.predict([[heure_test]]))
                """ donnee = pd.DataFrame([heure_test]) 
                print(donnee)
                donnee = pd.to_datetime(donnee[:, 0])  """     
                #donnee = donnee.set_index(["0"])
                #donnee.index = pd.to_datetime(donnee.index)
                #print(models_ask.predict(df.index.values.reshape(-1, 1) ))
                donnee = pd.DataFrame([heure_test])
                test_data = donnee.loc["0":]
                X_test = test_data.index.values.reshape(-1, 1)
                ''' valeur_max = models_ask.predict(X_test)
                print(yy_ask.tail())
                print(heure_test)
                print(valeur_max[0]) '''
                if(max_ask < models_ask.predict(X_test)):
                    max_ask = models_ask.predict(X_test)[0]
                    temps_max_ask = heure_test
                    print(">>> max ask :", max_ask)
                    print(">>> temps max ask :", temps_max_ask)
                if(min_ask > models_ask.predict(X_test)):
                    min_ask = models_ask.predict(X_test)[0]
                    temps_min_ask = heure_test
                    print(">>> min ask :", min_ask)
                    print(">>> temps min ask :", temps_min_ask)
                if(max_bid < models_bid.predict(X_test)):
                    max_bid = models_bid.predict(X_test)[0]
                    temps_max_bid = heure_test
                    print(">>> max bid :", max_bid)
                    print(">>> temps max bid :", temps_max_bid)
                if(min_bid > models_bid.predict(X_test)):
                    min_bid = models_bid.predict(X_test)[0]
                    temps_min_bid = heure_test
                    print(">>> min bid :", min_bid)
                    print(">>> temps min bid :", temps_min_bid)
                
            valeur_actuel = df.iloc[-1, 3]
            heure = Xyy[-1]
            print('>>> Valeur actuelle : %f' % (valeur_actuel))
            #print('>>> Valeur stop loss en pips : %f' % (sl_en_pips))
            print('>>> Heure :', heure)
            
            # buy signal
            if(df.iloc[-1,:].target_bid > 0):
                nb_signal_1 = 0
                nb_signal_2 = 0
                nb_signal_3 = 0
                nb_signal_4 = 0
                # if(df["RSI_Signal_buy"].iloc[-1] == 1):
                #if((df["RSI_BID"].iloc[-2] < rsi_buy_limite or df["RSI_BID"].iloc[-3] < rsi_buy_limite or df["RSI_BID"].iloc[-4] < rsi_buy_limite) and df["RSI_BID"].iloc[-1] > rsi_buy_limite):
                if(df["RSI_BID"].iloc[-1] < rsi_buy_limite):
                    nb_signal_1 = nb_signal_1 + 1
                if(df["EMA_10_EMA_30_BID"].iloc[-1] == 1):
                    nb_signal_2 = nb_signal_2 + 1
                if(df["MACD_Signal_MACD_BID"].iloc[-1] == 1):
                    nb_signal_1 = nb_signal_1 + 1
                if(df["Close_EMA_10_BID"].iloc[-1] == 1):
                    nb_signal_2 = nb_signal_2 + 1
                # if(df["CCI_Signal_buy"].iloc[-1] == 1):
                #if((df["CCI_BID"].iloc[-2] < cci_sell_limite or df["CCI_BID"].iloc[-3] < cci_sell_limite or df["CCI_BID"].iloc[-4] < cci_sell_limite) and df["CCI_BID"].iloc[-1] > cci_sell_limite):
                if(df["CCI_BID"].iloc[-1] < cci_sell_limite):
                    nb_signal_1 = nb_signal_1 + 1
                if(df["BB_Signal_buy"].iloc[-1] == 1):
                    nb_signal_2 = nb_signal_2 + 1
                if((df["tickqty"].iloc[-1] >= df["tickqty"].iloc[-2]) and (df["tickqty"].iloc[-2] >= df["tickqty"].iloc[-3])):
                    nb_signal_4 = nb_signal_4 + 1
                #if((nb_signal_1 >= 2 and nb_signal_2 >= 2) or (nb_signal_1 >= 1 and nb_signal_2 >= 2)):
                if((nb_signal_1 >= 3 and nb_signal_2 >= 1 and tendance_ascendant_5m == True) or(nb_signal_1 >= 2 and nb_signal_2 >= 1 and tendance_ascendant == True)): # and nb_signal_3 >= 1 and nb_signal_4 >= 1):
                    #sl = -(valeur_actuel - sl_en_pips)
                    #tp = max_bid
                    tp = 10
                    #if(sl > min_ask and (tp - valeur_actuel) > (2 * (valeur_actuel - sl)) and df["target_bid"][-1] == 1 and df["target_ask"][-1] == 0):
                    """ if(df["target_bid"][-1] == 1 and df["target_ask"][-1] == 0):
                        SetStopLoss(sl)
                        SetTakeProfit(tp)                
                        operation = 1 """
                    #SetStopLoss(sl)
                    #SetTakeProfit(tp)              
                    operation = 1  
                    print(">>> Fin de la prédiction")
                    return True, operation
            # sell signal
            if(df.iloc[-1,:].target_ask > 0):
                nb_signal_1 = 0
                nb_signal_2 = 0
                nb_signal_3 = 0
                nb_signal_4 = 0
                #if((df["RSI_ASK"].iloc[-2] > rsi_sell_limite or df["RSI_ASK"].iloc[-3] > rsi_sell_limite or df["RSI_ASK"].iloc[-4] > rsi_sell_limite) and df["RSI_ASK"].iloc[-1] < rsi_sell_limite):
                if(df["RSI_ASK"].iloc[-1] > rsi_sell_limite):
                    nb_signal_1 = nb_signal_1 + 1
                if(df["EMA_10_EMA_30_ASK"].iloc[-1] == -1):
                    nb_signal_2 = nb_signal_2 + 1
                if(df["MACD_Signal_MACD_ASK"].iloc[-1] == -1):
                    nb_signal_1 = nb_signal_1 + 1
                if(df["Close_EMA_10_ASK"].iloc[-1] == -1):
                    nb_signal_2 = nb_signal_2 + 1
                #if((df["CCI_ASK"].iloc[-2] > cci_buy_limite or df["CCI_ASK"].iloc[-3] > cci_buy_limite or df["CCI_ASK"].iloc[-4] > cci_buy_limite) and df["CCI_ASK"].iloc[-1] < cci_buy_limite):
                if(df["CCI_ASK"].iloc[-2] > cci_sell_limite):
                    nb_signal_1 = nb_signal_1 + 1
                if(df["BB_Signal_sell"].iloc[-1] == 1):
                    nb_signal_2 = nb_signal_2 + 1
                if((df["tickqty"].iloc[-1] >= df["tickqty"].iloc[-2]) and (df["tickqty"].iloc[-2] >= df["tickqty"].iloc[-3])):
                    nb_signal_4 = nb_signal_4 + 1
                #if((nb_signal_1 >= 2 and nb_signal_2 >= 2) or (nb_signal_1 >= 1 and nb_signal_2 >= 2)):
                if((nb_signal_1 >= 3 and nb_signal_2 >= 1 and tendance_descendant_5m == True) or(nb_signal_1 >= 2 and nb_signal_2 >= 1 and tendance_descendant == True)): # and nb_signal_3 >= 1 and nb_signal_4 >= 1):
                    #sl = -(valeur_actuel + sl_en_pips)
                    #tp = min_ask
                    tp = 10
                    #if(sl < max_bid and (valeur_actuel - tp) > (2 * (sl - valeur_actuel)) and df["target_bid"][-1] == 0 and df["target_ask"][-1] == 1):
                    """ if(df["target_bid"][-1] == 0 and df["target_ask"][-1] == 1):
                        SetStopLoss(sl)
                        SetTakeProfit(tp)  
                        operation = -1 """
                    #SetStopLoss(sl)
                    #SetTakeProfit(tp)                
                    operation = -1
                    print(">>> Fin de la prédiction")
                    return True, operation
            print(">>> Fin de la prédiction")
        except Exception as e:
            print(">>> Erreur de la prédiction, source d'erreur :", e)
            return False
        return True

