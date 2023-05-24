# importation des packages nécessaire
#import yahoo_fin.stock_info as si
import pandas as pd
import numpy as np
#import pandas_datareader as pdr
#from pandas_datareader import data as pdr
#import matplotlib.pyplot as plt
from datetime import datetime
from ta import add_all_ta_features
from ta.momentum import RSIIndicator
from ta.trend import EMAIndicator, MACD, ADXIndicator, CCIIndicator
from ta.volatility import AverageTrueRange, BollingerBands

from sklearn.model_selection import RepeatedStratifiedKFold, StratifiedKFold
from sklearn.model_selection import KFold
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.pipeline import Pipeline
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import classification_report
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import ExtraTreesClassifier 
from sklearn.ensemble import AdaBoostClassifier 
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import accuracy_score
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import RandomizedSearchCV
from sklearn import svm
from sklearn.neural_network import MLPClassifier
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.naive_bayes import GaussianNB

import datetime as dt
import time
from datetime import timedelta
import yfinance as yf
import calendar

import os.path
import os

#from fxcmpy import fxcmpy
#import fxcmpy
from deriv_api import DerivAPI

### ------ Quelque donnée utile ------ ###
timeframe = "5m"
nom_fichier = "data"
type_fichier = "csv"
pair = "EURUSD=X"
max_windows = 60 #  périod de calcul en jours
data = pd.DataFrame()
capital_test = 10
sl_test = 0.0
tp_test = 0.0
encours = False
operation = 0
sl_encours = 0.0
tp_encours = 0.0
risque_test = 0.02
roi_min_test = 0.05
lot_test = 0.1
valeur_pip_test = 0.0001

pair_list = []
list_file_name = "PairsListes.plt"
config_file_name = "Config.cfg"
token = "o4UgUbbepd0VuFr"
name = "kaira"

### ------ Initialisation de certaine valeur ------ ###
#api = fxcmpy.fxcmpy(config_file = "fxcm.cfg")
# dans fxcm il exist période m1 => "m1"
#api.subscribe_market_data

# fonction à ajouter :
# calcul ilay mety ho ambany indrindra ahafahana manao comparaison amin'ny stop loss ao anaty periode 15mn
# calcul izay mety ho ambony indrindra ahafahana manao calcul ny take profit ao anaty periode 15mn
# fotoana mety ahatratrarana ny take profit
# fotoana mety andalovan'ny valeur ambany indrindra
# lot alaina anaty paramètre
# pair misy liste azo anovana azy automatique
# calcul lot sy ny solde en cours, hoe firy ny lot azo alaina maximum en fonction an'ny balance
# calcul nombre de lot io dynamique, en fonction pair travailler-na
# raha manana moyen ahafahana maka ny pair par minute dia alaina anaovana calcul par 15mn
# miasa amin'ny pair maro indray miaraka ilay bot
# mety ny pair rehetra dia izay ahafahany maka position
# izay position efa misy dia anaovana stop loss dynamique raha azo atao
# coupure position rehefa tsy tratra ao anatiny fotoana voafetra ny take profit nefa mba efa bénéfice ny position

# coupure position rehefa ela loatra na loss aza ny position <= rehefa tena cas extreme vao atao
# tokony misy valeur retour ny prise de position amantarana hoe ok ve ilay position sa tsy ok, dia inona no tsy naha ok azy <= mila fonction avy amin'ny api

def GetProfitTable():
    profit_table = await api.profit_table({"profit_table": 1, "description": 1, "sort": "ASC"})
    print(profit_table)
    
def GetTransactionStatement():
    statement = await api.statement({"statement": 1, "description": 1, "limit": 100, "offset": 25})
    print(statement)
 
def SetSell():
    contract_id = buy.get('buy').get('contract_id')
    sell = await api.sell({"sell": contract_id, "price": 40})
    print(sell)

def SetBuy():
    proposal_id = proposal.get('proposal').get('id')
    buy = await api.buy({"buy": proposal_id, "price": 100})
    print(buy)

def GetBalance():
    account = await api.balance()
    print(account) 

def SetTakeProfit():

def SetStopLoss():

def GetNombrePosition():

def GetTicket():
    # active symboles from online
    active_symbols = await api.active_symbols({"active_symbols": "full"})
    print(active_symbols)
    # active symboles from cache
    active_symbols = await api.cache.active_symbols({"active_symbols": "full"})
    print(active_symbols)

def SetTicket():

def SetVolumeLot():

def SetNombreLot():

def Connection():
    authorize = await api.authorize(api_token)
    print(authorize)

def Deconnection():

def GetInfoTicket():

def GetInfoTrade():
    # info sur les actifs from online
    assets = await api.asset_index({"asset_index": 1})
    print(assets)
    # info sur les actifs from cache
    assets = await api.cache.asset_index({"asset_index": 1})
    print(assets)

def GetInfoPosition():
    contract_id = buy.get('buy').get('contract_id')
    poc = await api.proposal_open_contract(
        {"proposal_open_contract": 1, "contract_id": contract_id })
    print(poc)
    # flux info position
    source_poc: Observable = await api.subscribe({"proposal_open_contract": 1, "contract_id": contract_id})
    source_poc.subscribe(lambda poc: print(poc)

def ClosePosition():

def ChangeStopLoss():

def ChangeTakeProfit():

# récupération des pairs à traiter
def GetPairList():
    global pair_list
    try:
        f = open(list_file_name, 'r')
        pair_list = f.readlines()
    except:
        print(">>> Erreur de lecture de fichier de pair liste")
    finally:
        f.close()
        
# lecture du token
def GetTokenInfo():
    global token
    global timeframe
    try:
        f = open(config_file_name, 'r')
        configuration = f.readlines()
        #mila traitement amin'ilay liste azo eo avy eo
    except:
        print(">>> Erreur de lecture de fichier de configuration")
    finally:
        f.close()
 
### ------ Fonction de récupération des données ------ ###
def DataRecuperation(pair, nom_fichier, timeframe, type_fichier):
    # donnée global
    global data
    # donnée local
    data1 = pd.DataFrame()
    data2 = pd.DataFrame()
    # lecture des données locals
    fichier = nom_fichier + "_" + pair + "_" + timeframe + "." + type_fichier
    path = './' + fichier
    #if os.path.isfile(path):
        #data1 = pd.read_csv(fichier)
    # lecture des données en ligne
    
    
    if data1 is not None and not data1.empty:
        start = data1.index[-1]
        end = dt.datetime.now()
        data2 = yf.download(pair, start=start, end=end, interval=timeframe)
    else:
        start = dt.datetime.now() - timedelta(days = max_windows)
        end = dt.datetime.now()
        data2 = yf.download(pair, start=start, end=end, interval=timeframe)
    
    # additionnement des données
    if data1 is not None and not data1.empty:
        data = [data1, data2]
    else:
        data = data2
    #print(data.head())
    #data = yf.download(pair, start=start, end=end, interval=timeframe)
    """
    # suppression des données obsolète
    #data = pd.DataFrame(data, index=datetime)
    windows_actuel = data.index[-1].day - data.index[0].day
    if windows_actuel > max_windows:
        i = windows_actuel
        while i > 0:
            index = data.loc[df.index[0]]
            data2 = data.drop([index])
            i -= 1
    # enregistrement des nouvelles données
    data.to_csv(fichier, sep='\t', encoding='utf-8')
    """

### ------ Fonction de traitement ------ ### 
def DataTraitement():
    # donnée global
    global data
    rsi_sell = 70
    rsi_buy = 30
    cci_sell = 100
    cci_buy = -100
    # traitement
    df = data
    df['EMA_10'] = EMAIndicator(data['Close'], 5).ema_indicator()
    df['EMA_30'] = EMAIndicator(data['Close'], 15).ema_indicator()
    df['RSI'] = RSIIndicator(data['Close'], 10).rsi() 
    macd = MACD(data['Close'], 20, 10, 9)
    df['CCI'] = CCIIndicator(data['High'], data['Low'], data['Close'], 9, 0.015)
    df['MACD'] = macd.macd()
    df['MACDsignal'] = macd.macd_signal()
    bollinger_band = BollingerBands(data["Close"], 10, 2)
    df['bb_bbm'] = bollinger_band.bollinger_mavg()
    df['bb_bbh'] = bollinger_band.bollinger_hband()
    df['bb_bbl'] = bollinger_band.bollinger_lband()
    
    df['Close_EMA_10'] = np.where(data['Close'].values > df['EMA_10'].values, 1, -1)
    df['EMA_10_EMA_30'] = np.where(df['EMA_10'].values > df['EMA_30'].values, 1, -1)
    df['MACD_Signal_MACD'] = np.where(df['MACDsignal'] > df['MACD'], 1, -1)
    df['RSI_Signal_buy'] = np.where(df['RSI'] < rsi_buy, 1, 0)
    df['RSI_Signal_sell'] = np.where(df['RSI'] > rsi_sell, 1, 0)
    df['CCI_Signal_buy'] = np.where(df['RSI'] < cci_buy, 1, 0)
    df['CCI_Signel_sell'] = np.where(df['RSI'] > cci_sell, 1, 0)
    df['BB_Signal_buy'] = np.where(df['Close'] > df['bb_bbh'], 1, 0)
    df['BB_Signal_sell'] = np.where(df['Close'] < df['bb_bbl'], 1, 0)

    df['return'] = np.log(data['Close']/data['Close'].shift(1))
    df['target'] = np.where(data['return'] > 0, 1, 0)

    df = df.dropna()
    data = df


### ------ Fonction de prévision ------ ### 
def Preditcion():
    # variable global
    global data
    global capital_test
    global sl_test
    global tp_test
    global operation
    global risque_test
    global roi_min_test
    global lot_test
    global valeur_pip_test
    # traitement
    df = data
    capital = capital_test
    risque = risque_test
    gain = roi_min_test
    lot = lot_test
    valeur_pip = valeur_pip_test
    sl_en_dollar = capital * risque
    sl_en_pips = (sl_en_dollar * valeur_pip)    
    XXs = []
    for t in pd.DataFrame(df.index).values:
        XXs.append(t[0].timestamp())
    XX = pd.DataFrame(XXs)
    yy = pd.DataFrame(df.Close)
    XX_train, XX_test, yy_train, yy_test = train_test_split(XX, yy, test_size=0.2, random_state=0)
    Xyy = pd.DataFrame(df.index)
    models = LinearRegression()
    models.fit(XX, yy)
    currTime = Xyy.iloc[-1, -1]
    floored = pd.to_datetime(currTime).ceil('H').to_pydatetime()
    heure_pred = floored.timestamp()
    yy_pred = models.predict([[heure_pred]])
    valeur_actuel = df.iloc[-1, 3]
    heure = Xyy.iloc[-1, :-1]
    print('>>> Valeur actuelle : %f' % (valeur_actuel))
    print('>>> Valeur stop loss en pips : %f' % (sl_en_pips * 10000))
    print('>>> Heure :', heure)
    
    # buy signal
    if(df.iloc[-1,:].target > 0):
        nb_signal = 0
        if(df["RSI_Signal_buy"].iloc[-1] == 1):
            nb_signal = nb_signal + 1
        if(df["EMA_10_EMA_30"].iloc[-1] == 1):
            nb_signal = nb_signal + 1
        if(df["MACD_Signal_MACD"].iloc[-1] == 1):
            nb_signal = nb_signal + 1
        if(df["Close_EMA_10"].iloc[-1] == 1):
            nb_signal = nb_signal + 1
        if(df["CCI_Signal_buy"].iloc[-1] == 1):
            nb_signal = nb_signal + 1
        if(df["BB_Signal_buy"].iloc[-1] == 1):
            nb_signal = nb_signal + 1
        if(nb_signal >= 3):
            sl = valeur_actuel - sl_en_pips
            tp = yy_pred
            pro = tp - valeur_actuel
            if(pro < (2 * sl_en_pips)):
                pro = 2 * sl_en_pips
            if(pro > (4 * sl_en_pips)):
                pro = 4 * sl_en_pips
            print(">>> profit :",pro)
            if(pro >= (2 * sl_en_pips) and pro <= (4 * sl_en_pips) and sl < valeur_actuel and (valeur_actuel + pro) > sl):
                print('>>> Buy')
                print('>>> Stop loss : %f' % (sl))
                print('>>> Take profit : %f' % (valeur_actuel + pro))
                sl_test = sl
                tp_test = valeur_actuel + pro
                operation = 1
    # sell signal
    if(df.iloc[-1,:].target == 0):
        nb_signal = 0
        if(df["RSI_Signal_sell"].iloc[-1] == 1):
            nb_signal = nb_signal + 1
        if(df["EMA_10_EMA_30"].iloc[-1] == -1):
            nb_signal = nb_signal + 1
        if(df["MACD_Signal_MACD"].iloc[-1] == -1):
            nb_signal = nb_signal + 1
        if(df["Close_EMA_10"].iloc[-1] == -1):
            nb_signal = nb_signal + 1
        if(df["CCI_Signel_sell"].iloc[-1] == 1):
            nb_signal = nb_signal + 1
        if(df["BB_Signal_sell"].iloc[-1] == 1):
            nb_signal = nb_signal + 1
        if(nb_signal >= 3):
            sl = valeur_actuel + sl_en_pips
            tp = yy_pred
            pro = valeur_actuel - tp
            if(pro < (2 * sl_en_pips)):
                pro = 2 * sl_en_pips
            if(pro > (4 * sl_en_pips)):
                pro = 4 * sl_en_pips
            if(pro >= (2 * sl_en_pips) and pro <= (4 * sl_en_pips) and sl > valeur_actuel and (valeur_actuel - pro) < sl):
                print('>>> Sell')
                print('>>> Stop loss : %f' % (sl))
                print('>>> Take profit : %f' % (valeur_actuel - pro))
                sl_test = sl
                tp_test = valeur_actuel - pro
                operation = -1


while True:
    try:
        """
        data = yahoodata.history(start=start, end=end, interval=period)
        #data = yahoodata.history(start=start, end=end, period ='1d', interval=period)
        trade(data)
        time.sleep(300)
        """
        DataRecuperation(pair, nom_fichier, timeframe, type_fichier)
        DataTraitement()
        Preditcion()
        if not encours:
            if operation != 0:
                sl_encours = sl_test
                tp_encours = tp_test
                encours = True
        if operation == 1:
            if tp_encours < tp_test:
                capital_test = capital_test + ((tp_encours - 1) * 10000)
                encours = False
                print(">>> gain de :", ((tp_encours - 1) * 10000))
            if sl_encours > sl_test:
                capital_test = capital_test - ((sl_encours - 1) * 10000)
                encours = False
                print(">>> perte de :", ((sl_encours - 1) * 10000))
        if operation == -1:
            if tp_encours > tp_test:
                capital_test = capital_test + ((tp_encours - 1) * 10000)
                encours = False
                print(">>> gain de :", ((tp_encours - 1) * 10000))
            if sl_encours < sl_test:
                capital_test = capital_test - ((sl_encours - 1) * 10000)
                encours = False
                print(">>> perte de :", ((sl_encours - 1) * 10000))
        print("###########################################")
        print(">>> Capital en cours :", capital_test)
        print("###########################################")
        time.sleep(240)
    except:
        print("!!! Une erreur s'est produite durant le traitement !!!")
        pass
        #break
    
    