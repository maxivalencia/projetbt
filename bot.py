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
from ta.trend import EMAIndicator, MACD, ADXIndicator
from ta.volatility import AverageTrueRange

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

from fxcmpy import fxcmpy
### ------ Quelque donnée utile ------ ###
timeframe = "15m"
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
        data2 = yahoodata.history(pair, start=start, end=end, interval=timeframe)
    else:
        start = dt.datetime.now() - timedelta(days = max_windows)
        end = dt.datetime.now()
        data2 = yahoodata.history(pair, start=start, end=end, interval=timeframe)
    # additionnement des données
    if data1 is not None and not data1.empty:
        data = [data1, data2]
    else:
        data = data2
    data = yahoodata.history(pair, start=start, end=end, interval=timeframe)
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
    # traitement
    #print(data.tail())
    #df = pd.DataFrame(index = data.index)
    df = data
    df['EMA_10'] = EMAIndicator(data['Close'], 5).ema_indicator()
    df['EMA_30'] = EMAIndicator(data['Close'], 15).ema_indicator()
    df['ATR'] = AverageTrueRange(data['High'], data['Low'], data['Close'], 10).average_true_range()
    df['ADX'] = ADXIndicator(data['High'], data['Low'], data['Close'], 10).adx() # mbola misy direction positif sy negatif
    df['RSI'] = RSIIndicator(data['Close'], 10).rsi() 
    macd = MACD( data['Close'], 20, 10, 9)
    df['MACD'] = macd.macd()
    df['MACDsignal'] = macd.macd_signal()
    
    df['Close_EMA_10'] = np.where(data['Close'].values > df['EMA_10'].values, 1, -1)
    df['EMA_10_EMA_30'] = np.where(df['EMA_10'].values > df['EMA_30'].values, 1, -1)
    df['MACD_Signal_MACD'] = np.where(df['MACDsignal'] > df['MACD'], 1, -1)
    df['RSI_Signal_buy'] = np.where(df['RSI'] < rsi_buy, 1, 0)
    df['RSI_Signal_sell'] = np.where(df['RSI'] > rsi_sell, 1, 0)

    df['return'] = np.log(data['Close']/data['Close'].shift(1))
    df['target'] = np.where(data['return'] > 0, 1, 0)

    df = df.dropna()
    data = df


### ------ Fonction de prévision ------ ### 
def DataPrevision():
    # donnée global
    global data
    #global capital_test = 10
    global sl_test
    global tp_test
    global operation
    # traitement    
    #df = pd.DataFrame(index = data.index)
    df = data
    #X = df[['ATR', 'ADX','RSI', 'Close_EMA_10', 'EMA_10_EMA_30', 'MACD_Signal_MACD']]
    X = df.drop('target', axis=1)
    y = df.target
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=1, stratify=y)
    model = ""
    model = svm.SVC()
    param_grid={'C': [0.5,1,10,100], 'gamma': ['scale',1,0.1,0.001,0.0001], 'kernel': ['rbf']}
    grid_search = GridSearchCV(estimator = model, param_grid = param_grid)
    grid_search.fit(X_train, y_train)
    y_pred = grid_search.predict(X_test)
    report = classification_report(y_test, y_pred)
    print(report)
    
    capital = 100
    risque = 0.02
    gain = 0.04
    lot = 0.1
    valeur_pip = 0.0001
    sl_en_dollar = capital * risque
    sl_en_pips = (sl_en_dollar * valeur_pip)
    # calcul take profit
    models = LinearRegression()
    XXs = []
    for t in pd.DataFrame(data.index).values:
        XXs.append(t[0].timestamp())
    XX = pd.DataFrame(XXs)
    yy = pd.DataFrame(data.Close)
    XX_train, XX_test, yy_train, yy_test = train_test_split(XX, yy, test_size=0.2, random_state=0)
    Xyy = pd.DataFrame(data.index)
    models.fit(XX, yy)
    print("#######################################")
    currTime = Xyy.iloc[-1, -1]
    floored = pd.to_datetime(currTime).ceil('H').to_pydatetime()
    print(XX.iloc[-1, -1])
    print(currTime)
    print(floored.timestamp())
    print("#######################################")
    heure_pred = floored.timestamp()
    yy_pred = models.predict([[heure_pred]])
    valeur_actuel = data.iloc[-1, 3]
    heure = Xyy.iloc[-1, :-1]
    print('Valeur actuelle : %f' % (valeur_actuel))
    print('Valeur stop loss en pips : %f' % (sl_en_pips * 10000))
    print('Heure :', heure)
    #print(data.tail())
    if(df.iloc[-1,:].target>0):
        sl = valeur_actuel - sl_en_pips
        tp = yy_pred
        pro = tp - valeur_actuel
        if(pro < (2 * sl_en_pips)):
            pro = 2 * sl_en_pips
        if(pro > (4 * sl_en_pips)):
            pro = 4 * sl_en_pips
        print(pro)
        if(pro >= (2 * sl_en_pips) and pro <= (4 * sl_en_pips) and sl < valeur_actuel and (valeur_actuel + pro) > sl):
            print('Buy')
            print('Stop loss : %f' % (sl))
            print('Take profit : %f' % (valeur_actuel + pro))
            sl_test = sl
            tp_test = valeur_actuel + pro
            operation = 1
    else:
        sl = valeur_actuel + sl_en_pips
        tp = yy_pred
        pro = valeur_actuel - tp
        if(pro < (2 * sl_en_pips)):
            pro = 2 * sl_en_pips
        if(pro > (4 * sl_en_pips)):
            pro = 4 * sl_en_pips
        if(pro >= (2 * sl_en_pips) and pro <= (4 * sl_en_pips) and sl > valeur_actuel and (valeur_actuel - pro) < sl):
            print('Sell')
            print('Stop loss : %f' % (sl))
            print('Take profit : %f' % (valeur_actuel - pro))
            sl_test = sl
            tp_test = valeur_actuel - pro
            operation = -1
    

def model_selection(X,Y):
    seed = 7
    models = []
    models.append(('LogisticRegression', LogisticRegression(random_state=seed)))
    models.append(('LinearDiscriminantAnalysis', LinearDiscriminantAnalysis()))
    models.append(('KNeighborsClassifier', KNeighborsClassifier()))
    models.append(('DecisionTreeClassifier', DecisionTreeClassifier()))
    models.append(('GaussianNB', GaussianNB()))
    models.append(('RandomForestClassifier', RandomForestClassifier()))
    models.append(('ExtraTreesClassifier',ExtraTreesClassifier(random_state=seed)))
    models.append(('AdaBoostClassifier',AdaBoostClassifier(DecisionTreeClassifier(random_state=seed),random_state=seed,learning_rate=0.1)))
    models.append(('SVM',svm.SVC(random_state=seed)))
    models.append(('GradientBoostingClassifier',GradientBoostingClassifier(random_state=seed)))
    models.append(('MLPClassifier',MLPClassifier(random_state=seed)))
    results = []
    names = []
    scoring = 'accuracy'
    mod_mean = 0.0
    mod = ""
    for name, model in models:
        kfold = KFold(n_splits=10, shuffle=True, random_state=seed) 
        cv_results = cross_val_score(model, X, Y, cv=kfold, scoring=scoring)
        results.append(cv_results)
        names.append(name)
        msg = "%s: %f (%f)" % (name, cv_results.mean(), cv_results.std())
        print(msg) 
        if mod_mean < cv_results.mean():
            mod_mean = cv_results.mean()
            mod = model
    return mod       

start = '2023-1-1'
end = dt.datetime.now()
period = "5m"
symbol = "EURUSD=X"
yahoodata = yf.Ticker(symbol)

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
        DataPrevision()
        if not encours:
            if operation != 0:
                sl_encours = sl_test
                tp_encours = tp_test
                encours = True
        if operation == 1:
            if tp_encours < tp_test:
                capital_test = capital_test + ((tp_encours - 1) * 10000)
                encours = False
            if sl_encours > sl_test:
                capital_test = capital_test - ((sl_encours - 1) * 10000)
                encours = False
        if operation == -1:
            if tp_encours > tp_test:
                capital_test = capital_test + ((tp_encours - 1) * 10000)
                encours = False
            if sl_encours < sl_test:
                capital_test = capital_test - ((sl_encours - 1) * 10000)
                encours = False
        print("###########################################")
        print(">>> Capital en cours :", capital_test)
        print("###########################################")
    except:
        print("!!! Une erreur s'est produite durant le traitement !!!")
        pass
    
    