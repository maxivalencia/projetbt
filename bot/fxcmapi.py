#!/usr/bin/python3

import fxcmpy
class fxcmapi:
    def __init__(self):
        self.con = ''
        #self.pair = pair

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

    def SetSellOrder(self, pair, valeur=1, tp=5, sl=-2, date_expiration=None):
        try:
            order = self.con.create_entry_order(symbol=pair, is_buy=False, amount=valeur, time_in_force='GTC', order_type="Entry", limit=tp, is_in_pips=True, rate=tp, stop=sl, trailing_step=1, trailing_stop_step=1, order_range=None, expiration=date_expiration, account_id=self.GetAccountId())
            #print(GetOrderIds())
            print(order)
        except Exception as e:
            print(">>> Erreur lors de la prise de position sell, source d'erreur :", e)
            return False
        return True

    def SetBuyOrder(self, pair, valeur=1, tp=5, sl=-2, date_expiration=None):
        try:
            order = self.con.create_entry_order(symbol=pair, is_buy=True, amount=valeur, time_in_force='GTC', order_type="Entry", limit=tp, is_in_pips=True, rate=tp, stop=sl, trailing_step=1, trailing_stop_step=1, order_range=None, expiration=date_expiration, account_id=self.GetAccountId())
            #print(GetOrderIds())
            print(order)
        except Exception as e:
            print(">>> Erreur lors de la prise de position buy, source d'erreur :", e)
            return False
        return True
    
    def SetSellTrade(self, pair, valeur=1, tp=5, sl=-2):
        try:
            order = self.con.open_trade(symbol=pair, is_buy=False, amount=valeur, time_in_force='GTC', order_type='AtMarket', rate=tp, is_in_pips=True, limit=tp, at_market=0, stop=sl, trailing_step=1, account_id=self.GetAccountId())
            print(order)
        except Exception as e:
            print(">>> Erreur lors de la prise de position sell, source d'erreur :", e)
            return False
        return True

    def SetBuyTrade(self, pair, valeur=1, tp=5, sl=-2):
        try:
            order = self.con.open_trade(symbol=pair, is_buy=True, amount=valeur, time_in_force='GTC', order_type='AtMarket', rate=tp, is_in_pips=True, limit=tp, at_market=0, stop=sl, trailing_step=1, account_id=self.GetAccountId())
            print(order)
        except Exception as e:
            print(">>> Erreur lors de la prise de position buy, source d'erreur :", e)
            return False
        return True

    def SetSellPosition(self, pair, valeur=1, tp=5, sl=-2):
        try:
            #order = con.create_market_sell_order(symbol=pair, amount=valeur, is_in_pips=True, stop_loss=sl, take_profit=tp)
            order = self.con.create_market_sell_order(symbol=pair, amount=valeur)
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
        
    def SetBuyPosition(self, pair, valeur=1, tp=5, sl=-2):
        try:
            #order = con.create_market_buy_order(symbol=pair, amount=valeur, is_in_pips=True, stop_loss=sl, take_profit=tp)
            order = self.con.create_market_buy_order(symbol=pair, amount=valeur)
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

    def GetNombrePosition(self):
        try:
            orders = self.con.get_open_positions().T
            return orders.shape[1]
        except Exception as e:
            print(">>> Erreur de la récupératoin du nombre de position, source d'erreur :", e)
            return 0
        

    def GetTicket(self):
        try:
            ticket = self.con.get_subscribed_symbols()
            print(ticket)
        except Exception as e:
            print(">>> Erreur de la récupératoin du symbole en cours, source d'erreur :", e)
            return False
        return ticket

    def SetTicket(self, pair):
        try:
            self.con.subscribe_market_data(pair)
        except Exception as e:
            print(">>> Erreur de l'inscription du nouveau symbole, source d'erreur :", e)
            return False
        return True

    def UnSetTicket(self, pair):
        try:
            self.con.unsubscribe_market_data(pair)
        except Exception as e:
            print(">>> Erreur de la desinscription du symbole en cours, source d'erreur :", e)
            return False
        return True
        
    def Connection(self, server, config_file_name):
        try:
            self.con = fxcmpy.fxcmpy(config_file=config_file_name, server = server)
            print(">>> Connection effectuée avec succès")
        except Exception as e:
            print(">>> Erreur de la connection, source d'erreur :", e)
            return False
        return True

    def Deconnection(self):
        try:
            self.con.close()
            print(">>> Deconnection effectuée avec succès")
        except Exception as e:
            print(">>> Erreur de la déconnection, source d'erreur :", e)
            return False
        return True

    # tsy tena obligatoire fa ahafahana maka ny information mikasika ny ticket na pair iray
    #def GetInfoTicket():

    def GetOpenPosition(self):
        try:
            positions = self.con.get_open_positions().T
            print(positions)
        except Exception as e:
            print(">>> Erreur de la récupératoin des positions ouverts, source d'erreur :", e)
            return False
        return positions


    def GetInfoPosition(self, tradeId):
        try:
            position = self.con.get_open_position(tradeId)
            print(position)
        except Exception as e:
            print(">>> Erreur de la récupératoin des informations du trade, source d'erreur :", e)
            return False
        return position

    def ClosePosition(self, tradeId, valeur):
        try:
            self.con.close_trade(trade_id = tradeId, amount = valeur)
            print(">>> Fermeture de la position", tradeId, " pour la valeur :", valeur)
        except Exception as e:
            print(">>> Erreur de la fermeture du trades, source d'erreur :", e)
            return False
        return True

    def CloseAllForSymbol(self, pair):
        try:
            self.con.close_all_for_symbol(pair)
            print(">>> Fermeture de toute les positions pour le symbol:", pair)
        except Exception as e:
            print(">>> Erreur de la fermeture de tous les symboles, source d'erreur :", e)
            return False
        return True
        
    def CloseAll(self):
        try:
            self.con.close_all()
            print(">>> Fermeture de toute les positions ouverte")
        except Exception as e:
            print(">>> Erreur de la fermeture de toute les positions, source d'erreur :", e)
            return False
        return True

    def ChangeStopLoss(self, valeur, tdId):
        try:
            self.con.change_trade_stop_limit(tdId, is_in_pips = False, is_stop = False, rate = valeur)
            print(">>> Modification stoploss pour la valeur :", valeur)
        except Exception as e:
            print(">>> Erreur du changement de stop loss, source d'erreur :", e)
            return False
        return True

    def ChangeTakeProfit(self, valeur, tdId):
        try:
            self.con.change_order(order_id=tdId, amount=valeur)
            print(">>> Modification takeprofit pour la valeur :", valeur)
        except Exception as e:
            print(">>> Erreur du changement du take profit, source d'erreur :", e)
            return False
        return True

    def GetOpenTradeIds(self, tradeId):
        try:
            tradeId = self.con.get_open_trade_ids()
            print(">>> Liste des Identifications Ouverte :", tradeId)
        except Exception as e:
            print(">>> Erreur de la récupératoin des identifications des trades ouvert, source d'erreur :", e)
            return False
        return tradeId

    def GetClosedTradeIds(self, tradeId):
        try:
            tradeId = self.con.get_closed_trade_ids()
            print(">>> Liste des Identifications Clôturer :", tradeId)
        except Exception as e:
            print(">>> Erreur de la récupératoin des identifications des trades fermer, source d'erreur :", e)
            return False
        return tradeId

    def GetClosedPosition(self):
        try:
            closed = self.con.get_closed_positions().T
            print(">>> Liste des positions Clôturer:", closed)
        except Exception as e:
            print(">>> Erreur de la récupératoin des trades fermer, source d'erreur :", e)
            return False
        return closed
        
    def GetAllTradeIds(self, tradeId):
        try:
            tradeId = self.con.get_All_trade_ids()
            print(">>> Liste des identifications des trades:", tradeId)
        except Exception as e:
            print(">>> Erreur de la récupératoin des identifications des trades, source d'erreur :", e)
            return False
        return tradeId

    def GetAccountInfo(self):
        try:
            account = self.con.get_accounts().T
            print(">>> Info compte :")
            print(account)
        except Exception as e:
            print(">>> Erreur de la récupératoin des information sur le compte, source d'erreur :", e)
            return False
        return account

    def GetAccountId(self): 
        try:
            accountid = self.con.get_default_account()
            print(">>> Récupération du compte numéro :", accountid)
        except Exception as e:
            print(">>> Erreur de la récupération de l'id du compte, source d'erreur :", e)
            return False
        return accountid

    def SetAccountId(self, accountid):
        try:
            self.con.set_default_account(accountid)
            print(">>> Activiation du compte numéro :", accountid)
        except Exception as e:
            print(">>> Erreur de l'enregistrement de l'id du compte, source d'erreur :", e)
            return False
        return True

    def GetPairsLists(self):
        try:
            pairs_list = self.con.get_instruments()
            print(">>> Liste des symboles récupérer avec succès !!!")
        except Exception as e:
            print(">>> Erreur de la récupératoin des symboles, source d'erreur :", e)
            return False
        return pairs_list
