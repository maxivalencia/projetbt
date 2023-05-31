#!/usr/bin/python3

import fxcmpy
def GetOpenPositionsSummary():
    global con, summary
    summary = con.get_open_positions_summary().T
    print(summary)
    return summary
    
def GetClosedPositionsSummary():
    global con, summary
    summary = con.get_closed_positions_summary().T
    print(summary)
    return summary
    
def GetAccountSummary():
    global con, summary
    summary = con.get_accounts_summary().T
    print(summary)
    return summary
    
def GetSummary():
    global con, summary
    summary = con.get_summary().T
    print(summary)
    return summary
    
def GetOpenOrders():
    global con, transaction
    transaction = con.get_orders().T
    print(transaction)
    return transaction
    
def GetOrderIds():
    global con
    orders = con.get_order_ids()
    return orders[-1]

def SetSellOrder(pair, valeur=1, tp=4, sl=2, date_expiration=None):
    global con
    try:
        order = con.create_entry_order(symbol=pair, is_buy=False, amount=valeur, time_in_force='GTC', order_type="Entry", limit=tp, is_in_pips=True, rate=tp, stop=sl, trailing_step=1, trailing_stop_step=1, order_range=None, expiration=date_expiration, account_id=GetAccountId())
        #print(GetOrderIds())
        print(order)
    except Exception as e:
        print(e)
        return False
    return True

def SetBuyOrder(pair, valeur=1, tp=4, sl=2, date_expiration=None):
    global con
    try:
        order = con.create_entry_order(symbol=pair, is_buy=True, amount=valeur, time_in_force='GTC', order_type="Entry", limit=tp, is_in_pips=True, rate=tp, stop=sl, trailing_step=1, trailing_stop_step=1, order_range=None, expiration=date_expiration, account_id=GetAccountId())
        #print(GetOrderIds())
        print(order)
    except Exception as e:
        print(e)
        return False
    return True
 
def SetSellTrade(pair, valeur=1, tp=4, sl=2):
    global con
    try:
        order = con.open_trade(symbol=pair, is_buy=False, amount=valeur, time_in_force='GTC', order_type='AtMarket', rate=tp, is_in_pips=True, limit=tp, at_market=0, stop=sl, trailing_step=1, account_id=GetAccountId())
        print(order)
    except Exception as e:
        print(e)
        return False
    return True

def SetBuyTrade(pair, valeur=1, tp=4, sl=2):
    global con
    try:
        order = con.open_trade(symbol=pair, is_buy=True, amount=valeur, time_in_force='GTC', order_type='AtMarket', rate=tp, is_in_pips=True, limit=tp, at_market=0, stop=sl, trailing_step=1, account_id=GetAccountId())
        print(order)
    except Exception as e:
        print(e)
        return False
    return True

def SetSellPosition(pair, valeur=1, tp=5, sl=2):
    global con
    try:
        #order = con.create_market_sell_order(symbol=pair, amount=valeur, is_in_pips=True, stop_loss=sl, take_profit=tp)
        order = con.create_market_sell_order(symbol=pair, amount=valeur)
        trade_id = con.get_open_trade_ids()[-1]
        con.change_trade_stop_limit(trade_id, is_stop=False, rate=tp, is_in_pips=True, trailing_step=0)
        con.change_trade_stop_limit(trade_id, is_stop=True, rate=sl, is_in_pips=True, trailing_step=0)
        print(order)
        print("Trade id :", trade_id)
    except Exception as e:
        print(e)
        return False
    return True
    
def SetBuyPosition(pair, valeur=1, tp=5, sl=2):
    global con
    try:
        #order = con.create_market_buy_order(symbol=pair, amount=valeur, is_in_pips=True, stop_loss=sl, take_profit=tp)
        order = con.create_market_buy_order(symbol=pair, amount=valeur)
        trade_id = con.get_open_trade_ids()[-1]
        con.change_trade_stop_limit(trade_id, is_stop=False, rate=tp, is_in_pips=True, trailing_step=0)
        con.change_trade_stop_limit(trade_id, is_stop=True, rate=sl, is_in_pips=True, trailing_step=0)
        print(order)
        print("Trade id :", trade_id)
    except Exception as e:
        print(e)
        return False
    return True

def GetOrderId(numero):
    global con
    order_id = con.get_order_ids()[numero]
    print(order_id)
    return order_id

def GetOrderDelete(order_id):
    global con
    order_id = con.delete_order(order_id)
    print(order_id)
    return order_id

def SetOrderLimit(order_id, sl):
    global con
    order = con.change_order_stop_limit(order_id=order_id, is_stop_in_pips=True, is_limit_in_pips=True, limit=sl, stop=-1)
    print(order)
    return order

def SetOrderChange(order_id, valeur, tp):
    global con
    order = con.change_order(order_id=order_id, amount=valeur, rate=tp)
    print(order)
    return order

def GetBalance():
    global con
    account = con.get_accounts().T
    print("Balance actuelle :", account[0][3])
    return account[0][3]

def GetNombrePosition():
    global con
    orders = con.get_orders().T
    return len(orders)

def GetTicket():
    global con
    ticket = con.get_subscribed_symbols()
    print(ticket)
    return ticket

def SetTicket(pair):
    global con
    con.subscribe_market_data(pair)
    return True

def UnSetTicket(pair):
    global con
    con.unsubscribe_market_data(pair)
    return True

def Connection():
    global con
    global server, config_file_name
    con = fxcmpy.fxcmpy(config_file=config_file_name, server = server)
    print(">>> Connection effectuée avec succès")
    connected = True
    return True

def Deconnection():
    global con
    con.close()
    print(">>> Deconnection effectuée avec succès")
    connected = False
    return True    

def GetOpenPosition():
    global con
    positions = con.get_open_positions().T
    print(positions)
    return positions

def GetInfoPosition(tradeId):
    global con
    position = con.get_open_position(tradeId)
    print(position)
    return position

def ClosePosition(tradeId, valeur):
    global con
    con.close_trade(trade_id = tradeId, amount = valeur)
    print(">>> Fermeture de la position", tradeId, " pour la valeur :", valeur)
    return True

def CloseAllForSymbol(pair):
    global con
    con.close_all_for_symbol(pair)
    print(">>> Fermeture de toute les positions pour le symbol:", pair)
    return True
    
def CloseAll():
    global con
    con.close_all()
    print(">>> Fermeture de toute les positions ouverte")
    return True

def ChangeStopLoss(valeur, trId):
    global con, tradeId
    con.change_trade_stop_limit(trId, is_in_pips = False, is_stop = False, rate = valeur)
    print(">>> Modification stoploss pour la valeur :", valeur)
    return True

def ChangeTakeProfit(valeur, trId):
    global con, tradeId
    con.change_order(order_id=trId, amount=valeur)
    print(">>> Modification takeprofit pour la valeur :", valeur)
    return True

def GetOpenTradeIds():
    global con, tradeId
    tradeId = con.get_open_trade_ids()
    print(">>> Liste des Identifications Ouverte :", tradeId)
    return tradeId

def GetClosedTradeIds():
    global con, tradeId
    tradeId = con.get_closed_trade_ids()
    print(">>> Liste des Identifications Clôturer :", tradeId)
    return tradeId

def GetClosedPosition():
    global con
    closed = con.get_closed_positions().T
    print(">>> Liste des positions Clôturer:", closed)
    return closed
    
def GetAllTradeIds():
    global con, tradeId
    tradeId = con.get_All_trade_ids()
    print(">>> Liste des identifications des trades:", tradeId)
    return tradeId

# récupération des pairs à traiter
def GetPairList():
    global pairs_list
    try:
        pairs_list = con.get_instruments()
        #file = open(list_file_name, "r")
        #pair_list = file.read()
        #pairs_list = pair_list.split(",")
        print(">>> Liste des symboles récupérer avec succès !!!")
        print(pairs_list)
        #file.close()
        return pairs_list
    except:
        print(">>> !!! Erreur de la récupération de la liste des symboles !!!")
        return False

def GetAccountInfo():
    global con
    account = con.get_accounts().T
    print(">>> Info compte :")
    print(account)
    return account

def GetAccountId(): 
    global accountid
    global con
    accountid = con.get_default_account()
    print(">>> Récupération du compte numéro :", accountid)
    return accountid

def SetAccountId(accountid):
    global con
    con.set_default_account(accountid)
    print(">>> Activiation du compte numéro :", accountid)
    return True
    
def DataRecuperation(pair, timeframe):
    # donnée global
    global data
    global isdata, con
    try:
        if(con.is_subscribed(pair)):
            print(">>> Début de la récupération des données du symbol", pair)
            #data = con.get_candles(pair, period=timeframe) #, number=2500)
            data = con.get_candles(pair, period=timeframe, number=2500)
            isdata = True
            print(">>> Fin de la récupération des données")
            return True
        else:
            print(">>> !!! Pair non souscrit !!!")
    except:
        print(">>> !!! Erreur lors de la récupération des données !!!")
    return False