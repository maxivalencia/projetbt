#!/usr/bin/python3

import fxcmpy
class fxcmapi:
    def __init__(self, pair):
        self.con = ''
        self.pair = pair

    def GetOpenPositionsSummary(self):
        try:
            self.summary = self.con.get_open_positions_summary().T
        except Exception as e:
            print(">>> Erreur lors de la récupération des récapitulations des positions ouvert, source d'erreur :", e)
            return False
        print(self.summary)
        return self.summary
        
    def GetClosedPositionsSummary(self):
        try:
            self.summary = self.con.get_closed_positions_summary().T
        except Exception as e:
            print(">>> Erreur lors de la récupération des récapitulations des positions fermer, source d'erreur :", e)
            return False
        print(self.summary)
        return self.summary
        
    def GetAccountSummary(self):
        try:
            self.summary = self.con.get_accounts_summary().T
        except Exception as e:
            print(">>> Erreur lors de la récupération des récapitulations du compte, source d'erreur :", e)
            return False
        print(self.summary)
        return self.summary
        
    def GetSummary(self):
        try:
            self.summary = self.con.get_summary().T
        except Exception as e:
            print(">>> Erreur lors de la récupération des récapitulations, source d'erreur :", e)
            return False
        print(self.summary)
        return self.summary
        
    def GetOpenOrders(self):
        try:
            self.transaction = self.con.get_orders().T
        except Exception as e:
            print(">>> Erreur lors de la récupération des ordres ouvert, source d'erreur :", e)
            return False
        print(self.transaction)
        return self.transaction
        
    def GetOrderIds(self):
        try:
            orders = self.con.get_order_ids()
        except Exception as e:
            print(">>> Erreur lors de la récupération de l'identification de l'ordre, source d'erreur :", e)
            return False
        return orders[-1]

    def SetSellOrder(self, valeur=1, tp=5, sl=-2, date_expiration=None):
        try:
            order = self.con.create_entry_order(symbol=self.pair, is_buy=False, amount=valeur, time_in_force='GTC', order_type="Entry", limit=tp, is_in_pips=True, rate=tp, stop=sl, trailing_step=1, trailing_stop_step=1, order_range=None, expiration=date_expiration, account_id=self.GetAccountId())
            #print(GetOrderIds())
            print(order)
        except Exception as e:
            print(">>> Erreur lors de la prise de position sell, source d'erreur :", e)
            return False
        return True

    def SetBuyOrder(self, valeur=1, tp=5, sl=-2, date_expiration=None):
        try:
            order = self.con.create_entry_order(symbol=self.pair, is_buy=True, amount=valeur, time_in_force='GTC', order_type="Entry", limit=tp, is_in_pips=True, rate=tp, stop=sl, trailing_step=1, trailing_stop_step=1, order_range=None, expiration=date_expiration, account_id=self.GetAccountId())
            #print(GetOrderIds())
            print(order)
        except Exception as e:
            print(">>> Erreur lors de la prise de position buy, source d'erreur :", e)
            return False
        return True
    
    def SetSellTrade(self, valeur=1, tp=5, sl=-2):
        try:
            order = self.con.open_trade(symbol=self.pair, is_buy=False, amount=valeur, time_in_force='GTC', order_type='AtMarket', rate=tp, is_in_pips=True, limit=tp, at_market=0, stop=sl, trailing_step=1, account_id=self.GetAccountId())
            print(order)
        except Exception as e:
            print(">>> Erreur lors de la prise de position sell, source d'erreur :", e)
            return False
        return True

    def SetBuyTrade(self, valeur=1, tp=5, sl=-2):
        try:
            order = self.con.open_trade(symbol=self.pair, is_buy=True, amount=valeur, time_in_force='GTC', order_type='AtMarket', rate=tp, is_in_pips=True, limit=tp, at_market=0, stop=sl, trailing_step=1, account_id=self.GetAccountId())
            print(order)
        except Exception as e:
            print(">>> Erreur lors de la prise de position buy, source d'erreur :", e)
            return False
        return True

    def SetSellPosition(self, valeur=1, tp=5, sl=-2):
        try:
            #order = con.create_market_sell_order(symbol=pair, amount=valeur, is_in_pips=True, stop_loss=sl, take_profit=tp)
            order = self.con.create_market_sell_order(symbol=self.pair, amount=valeur)
            trade_id = self.con.get_open_trade_ids()[-1]
            self.con.change_trade_stop_limit(trade_id, is_stop=False, rate=tp, is_in_pips=True, trailing_step=0)
            self.con.change_trade_stop_limit(trade_id, is_stop=True, rate=sl, is_in_pips=True, trailing_step=0)
            self.con.change_trade_stop_limit(trade_id, is_stop=False, rate=tp, is_in_pips=True, trailing_step=0)
            self.con.change_trade_stop_limit(trade_id, is_stop=True, rate=sl, is_in_pips=True, trailing_step=0)
            self.con.change_trade_stop_limit(trade_id, is_stop=False, rate=tp, is_in_pips=True, trailing_step=0)
            self.con.change_trade_stop_limit(trade_id, is_stop=True, rate=sl, is_in_pips=True, trailing_step=0)
            print(order)
            print("Trade id :", trade_id)
        except Exception as e:
            print(">>> Erreur lors de la prise de position sell, source d'erreur :", e)
            return False
        return True
        
    def SetBuyPosition(self, valeur=1, tp=5, sl=-2):
        try:
            #order = con.create_market_buy_order(symbol=pair, amount=valeur, is_in_pips=True, stop_loss=sl, take_profit=tp)
            order = self.con.create_market_buy_order(symbol=self.pair, amount=valeur)
            trade_id = self.con.get_open_trade_ids()[-1]
            self.con.change_trade_stop_limit(trade_id, is_stop=False, rate=tp, is_in_pips=True, trailing_step=0)
            self.con.change_trade_stop_limit(trade_id, is_stop=True, rate=sl, is_in_pips=True, trailing_step=0)
            self.con.change_trade_stop_limit(trade_id, is_stop=False, rate=tp, is_in_pips=True, trailing_step=0)
            self.con.change_trade_stop_limit(trade_id, is_stop=True, rate=sl, is_in_pips=True, trailing_step=0)
            self.con.change_trade_stop_limit(trade_id, is_stop=False, rate=tp, is_in_pips=True, trailing_step=0)
            self.con.change_trade_stop_limit(trade_id, is_stop=True, rate=sl, is_in_pips=True, trailing_step=0)
            print(order)
            print("Trade id :", trade_id)
        except Exception as e:
            print(">>> Erreur lors de la prise de position buy, source d'erreur :", e)
            return False
        return True

    def SetStopLimite(self, trade_id, tp=5, sl=-2):
        try:
            self.con.change_trade_stop_limit(trade_id, is_stop=False, rate=tp, is_in_pips=True, trailing_step=0)
            self.con.change_trade_stop_limit(trade_id, is_stop=True, rate=sl, is_in_pips=True, trailing_step=0)
            self.con.change_trade_stop_limit(trade_id, is_stop=False, rate=tp, is_in_pips=True, trailing_step=0)
            self.con.change_trade_stop_limit(trade_id, is_stop=True, rate=sl, is_in_pips=True, trailing_step=0)
        except Exception as e:
            print(">>> Erreur lors de la modification des stop loss et take profit, source d'erreur :", e)
            return False

    def GetTradeIds(self):
        try:
            return self.con.get_open_trade_ids()
        except Exception as e:
            print(">>> Erreur de la récupératoin des identifications des trades, source d'erreur :", e)
            return False

    def GetOrderId(self, numero):
        try:
            order_id = self.con.get_order_ids()[numero]
            print(order_id)
        except Exception as e:
            print(">>> Erreur de la récupératoin de l'identifications de l'ordre, source d'erreur :", e)
            return False
        return order_id

    def GetOrderDelete(self, order_id):
        try:
            order_id = self.con.delete_order(order_id)
            print(order_id)
        except Exception as e:
            print(">>> Erreur lors de la suppression de l'ordre, source d'erreur :", e)
            return False
        return order_id

    def SetOrderLimit(self, order_id, sl):
        try:
            order = self.con.change_order_stop_limit(order_id=order_id, is_stop_in_pips=True, is_limit_in_pips=True, limit=sl, stop=-1)
            print(order)
        except Exception as e:
            print(">>> Erreur lors de la récupératoin des identifications des trades, source d'erreur :", e)
            return False
        return order

    def SetOrderChange(self, order_id, valeur, tp):
        try:
            order = self.con.change_order(order_id=order_id, amount=valeur, rate=tp)
            print(order)
        except Exception as e:
            print(">>> Erreur lors de la modification de l'ordre, source d'erreur :", e)
            return False
        return order

    def GetBalance(self):
        try:
            account = self.con.get_accounts().T
            print("Balance actuelle :", account[0][3])
        except Exception as e:
            print(">>> Erreur lors de la récupératoin de la balance, source d'erreur :", e)
            return False
        return account[0][3]
