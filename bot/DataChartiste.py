#!/usr/bin/python3

class DataChartiste:
    def __init__(self, pair, data, con, timeframe5m, timeframe15m):
        self.data = data
        self.con = con
        self.timeframe5m = timeframe5m
        self.timeframe15m = timeframe15m
        self.pair = pair

    def EtudeChartiste(self):
        global data, data5m, data15m, con
        global sl_test
        global tp_test
        global operation
        global tendance_ascendant
        global tendance_descendant
        tendance_ascendant = False
        tendance_descendant = False
        tendance_ascendant_5m = False
        tendance_descendant_5m = False
        # teste de support
        # atao 20 ny nombre de bougie aloha
        nb_bougie = 20
        nb_bougie_espacement = 5
        espacement = 0
        numero_case = 0
        numero_case_max = 3
        support_bute = [0, 0, 0]
        resistance_bute = [0, 0, 0]
        support_bute_5m = [0, 0, 0]
        resistance_bute_5m = [0, 0, 0]
        support_bute_15m = [0, 0, 0]
        resistance_bute_15m = [0, 0, 0]
        marge_difference = 0.1
        support_ascendant = False
        support_descendant = False
        support_ascendant_5m = False
        support_descendant_5m = False
        support_ascendant_15m = False
        support_descendant_15m = False
        support_horizontal = False
        resistance_ascendant = False
        resistance_descendant = False
        resistance_ascendant_5m = False
        resistance_descendant_5m = False
        resistance_ascendant_15m = False
        resistance_descendant_15m = False
        resistance_horizontal = False
        canaux_ascendant = False
        canaux_descendant = False
        canaux_horizontal = False
        triangle_ascendant = False
        triangle_descendant = False
        triangle_asymetrique = False
        elargissement_ascendant = False
        elargissement_descendant = False
        elargissement_asymetrique = False
        double_top = False
        double_bottom = False
        triple_top = False
        triple_bottom = False
        epaule_tete_epaule = False
        epaule_tete_epaule_inverse = False
        marteau_retournement_haussier = False
        marteau_retournement_baissier = False
        avalement_haussier = False
        avalement_baissier = False
        try:
            data5m = self.con.get_candles(self.pair, period=self.timeframe5m, number=10000)
            data15m = self.con.get_candles(self.pair, period=self.timeframe15m, number=10000)
            for nb in range(nb_bougie):
                if(support_bute[numero_case] <= 0):
                    support_bute[numero_case] = data["askhigh"].iloc[(nb - 1) * (-1)]
                if(support_bute[numero_case] > data["askhigh"].iloc[(nb - 1) * (-1)]):
                    support_bute[numero_case] = data["askhigh"].iloc[(nb - 1) * (-1)]
                    espacement = 0
                else:
                    espacement += 1
                if(espacement >= nb_bougie_espacement):
                    numero_case += 1
                    espacement = 0
                if(numero_case >= numero_case_max):
                    espacement = 0
                    numero_case = 0
                    break
            for nb in range(nb_bougie):
                if(support_bute_5m[numero_case] <= 0):
                    support_bute_5m[numero_case] = data5m["askhigh"].iloc[(nb - 1) * (-1)]
                if(support_bute_5m[numero_case] > data5m["askhigh"].iloc[(nb - 1) * (-1)]):
                    support_bute_5m[numero_case] = data5m["askhigh"].iloc[(nb - 1) * (-1)]
                    espacement = 0
                else:
                    espacement += 1
                if(espacement >= nb_bougie_espacement):
                    numero_case += 1
                    espacement = 0
                if(numero_case >= numero_case_max):
                    espacement = 0
                    numero_case = 0
                    break
            for nb in range(nb_bougie):
                if(support_bute_15m[numero_case] <= 0):
                    support_bute_15m[numero_case] = data15m["askhigh"].iloc[(nb - 1) * (-1)]
                if(support_bute_15m[numero_case] > data15m["askhigh"].iloc[(nb - 1) * (-1)]):
                    support_bute_15m[numero_case] = data15m["askhigh"].iloc[(nb - 1) * (-1)]
                    espacement = 0
                else:
                    espacement += 1
                if(espacement >= nb_bougie_espacement):
                    numero_case += 1
                    espacement = 0
                if(numero_case >= numero_case_max):
                    espacement = 0
                    numero_case = 0
                    break
            for nb in range(nb_bougie):
                if(resistance_bute[numero_case] >= 0):
                    resistance_bute[numero_case] = data["asklow"].iloc[(nb - 1) * (-1)]
                if(resistance_bute[numero_case] < data["asklow"].iloc[(nb - 1) * (-1)]):
                    resistance_bute[numero_case] = data["asklow"].iloc[(nb - 1) * (-1)]
                    espacement = 0
                else:
                    espacement += 1
                if(espacement >= nb_bougie_espacement):
                    numero_case += 1
                    espacement = 0
                if(numero_case >= numero_case_max):
                    espacement = 0
                    numero_case = 0
                    break
            for nb in range(nb_bougie):
                if(resistance_bute_5m[numero_case] >= 0):
                    resistance_bute_5m[numero_case] = data5m["asklow"].iloc[(nb - 1) * (-1)]
                if(resistance_bute_5m[numero_case] < data5m["asklow"].iloc[(nb - 1) * (-1)]):
                    resistance_bute_5m[numero_case] = data5m["asklow"].iloc[(nb - 1) * (-1)]
                    espacement = 0
                else:
                    espacement += 1
                if(espacement >= nb_bougie_espacement):
                    numero_case += 1
                    espacement = 0
                if(numero_case >= numero_case_max):
                    espacement = 0
                    numero_case = 0
                    break
            for nb in range(nb_bougie):
                if(resistance_bute_15m[numero_case] >= 0):
                    resistance_bute_15m[numero_case] = data15m["asklow"].iloc[(nb - 1) * (-1)]
                if(resistance_bute_15m[numero_case] < data15m["asklow"].iloc[(nb - 1) * (-1)]):
                    resistance_bute_15m[numero_case] = data15m["asklow"].iloc[(nb - 1) * (-1)]
                    espacement = 0
                else:
                    espacement += 1
                if(espacement >= nb_bougie_espacement):
                    numero_case += 1
                    espacement = 0
                if(numero_case >= numero_case_max):
                    espacement = 0
                    numero_case = 0
                    break
            if((support_bute[0] <= (support_bute[1] - (support_bute[1] * marge_difference))) and (support_bute[1] <= (support_bute[2] - (support_bute[2] * marge_difference)))):
                support_ascendant = True
                if((support_bute_5m[0] <= (support_bute_5m[1] - (support_bute_5m[1] * marge_difference))) and (support_bute_5m[1] <= (support_bute_5m[2] - (support_bute_5m[2] * marge_difference)))):
                    support_ascendant_5m = True
                    tendance_ascendant_5m = True
                    if((support_bute_15m[0] <= (support_bute_15m[1] - (support_bute_15m[1] * marge_difference))) and (support_bute_15m[1] <= (support_bute_15m[2] - (support_bute_15m[2] * marge_difference)))):
                        support_ascendant_15m = True
                        tendance_ascendant = True
            if((support_bute_5m[0] <= (support_bute_5m[1] - (support_bute_5m[1] * marge_difference))) and (support_bute_5m[1] <= (support_bute_5m[2] - (support_bute_5m[2] * marge_difference)))):
                support_ascendant_5m = True
            if((support_bute_15m[0] <= (support_bute_15m[1] - (support_bute_15m[1] * marge_difference))) and (support_bute_15m[1] <= (support_bute_15m[2] - (support_bute_15m[2] * marge_difference)))):
                support_ascendant_15m = True
            if((support_bute[0] >= (support_bute[1] + (support_bute[1] * marge_difference))) and (support_bute[1] >= (support_bute[2] + (support_bute[2] * marge_difference)))):
                support_descendant = True
            if((support_bute_5m[0] >= (support_bute_5m[1] + (support_bute_5m[1] * marge_difference))) and (support_bute_5m[1] >= (support_bute_5m[2] + (support_bute_5m[2] * marge_difference)))):
                support_descendant_5m = True
            if((support_bute_15m[0] >= (support_bute_15m[1] + (support_bute_15m[1] * marge_difference))) and (support_bute_15m[1] >= (support_bute_15m[2] + (support_bute_15m[2] * marge_difference)))):
                support_descendant_15m = True
            if(((support_bute[0] > (support_bute[1] - (support_bute[1] * marge_difference))) and (support_bute[0] < (support_bute[1] + (support_bute[1] * marge_difference)))) and ((support_bute[1] > (support_bute[2] - (support_bute[1] * marge_difference))) and (support_bute[1] < (support_bute[1] + (support_bute[2] * marge_difference))))):
                support_horizontal = True
            
            if((resistance_bute[0] <= (resistance_bute[1] - (resistance_bute[1] * marge_difference))) and (resistance_bute[1] <= (resistance_bute[2] - (resistance_bute[2] * marge_difference)))):
                resistance_ascendant = True
            if((resistance_bute_5m[0] <= (resistance_bute_5m[1] - (resistance_bute_5m[1] * marge_difference))) and (resistance_bute_5m[1] <= (resistance_bute_5m[2] - (resistance_bute_5m[2] * marge_difference)))):
                resistance_ascendant_5m = True
            if((resistance_bute_15m[0] <= (resistance_bute_15m[1] - (resistance_bute_15m[1] * marge_difference))) and (resistance_bute_15m[1] <= (resistance_bute_15m[2] - (resistance_bute_15m[2] * marge_difference)))):
                resistance_ascendant_15m = True
            if((resistance_bute[0] >= (resistance_bute[1] + (resistance_bute[1] * marge_difference))) and (resistance_bute[1] >= (resistance_bute[2] + (resistance_bute[2] * marge_difference)))):
                resistance_descendant = True
                if((resistance_bute_5m[0] >= (resistance_bute_5m[1] + (resistance_bute_5m[1] * marge_difference))) and (resistance_bute_5m[1] >= (resistance_bute_5m[2] + (resistance_bute_5m[2] * marge_difference)))):
                    resistance_descendant_5m = True
                    tendance_descendant_5m = True
                    if((resistance_bute_15m[0] >= (resistance_bute_15m[1] + (resistance_bute_15m[1] * marge_difference))) and (resistance_bute_15m[1] >= (resistance_bute_15m[2] + (resistance_bute_15m[2] * marge_difference)))):
                        resistance_ascendant_15m = True
                        tendance_descendant = True
            if((resistance_bute_5m[0] >= (resistance_bute_5m[1] + (resistance_bute_5m[1] * marge_difference))) and (resistance_bute_5m[1] >= (resistance_bute_5m[2] + (resistance_bute_5m[2] * marge_difference)))):
                resistance_descendant_5m = True
            if((resistance_bute_15m[0] >= (resistance_bute_15m[1] + (resistance_bute_15m[1] * marge_difference))) and (resistance_bute_15m[1] >= (resistance_bute_15m[2] + (resistance_bute_15m[2] * marge_difference)))):
                resistance_descendant_15m = True
            if(((resistance_bute[0] > (resistance_bute[1] - (resistance_bute[1] * marge_difference))) and (resistance_bute[0] < (resistance_bute[1] + (resistance_bute[1] * marge_difference)))) and ((resistance_bute[1] > (resistance_bute[2] - (resistance_bute[1] * marge_difference))) and (resistance_bute[1] < (resistance_bute[1] + (resistance_bute[2] * marge_difference))))):
                resistance_horizontal = True
            
            # teste canaux
            if(support_ascendant == True and resistance_ascendant == True):
                canaux_ascendant = True
                if(support_ascendant_5m == True and resistance_ascendant_5m == True):
                    tendance_ascendant_5m = True
                    if(support_ascendant_15m == True and resistance_ascendant_15m == True):
                        tendance_ascendant = True
            if(support_descendant == True and resistance_descendant == True):
                canaux_descendant = True
                if(support_descendant_5m == True and resistance_descendant_5m == True):
                    tendance_descendant_5m = True
                    if(support_descendant_15m == True and resistance_descendant_15m == True):
                        tendance_descendant = True
            if(support_horizontal == True and resistance_horizontal == True):
                canaux_horizontal = True
            
            # teste triangle
            if(support_horizontal == True and resistance_ascendant == True):
                triangle_ascendant = True
                #tendance_ascendant = True
            if(support_descendant == True and resistance_horizontal == True):
                triangle_descendant = True
                #tendance_descendant = True
            if(support_descendant == True and resistance_ascendant == True):
                triangle_asymetrique = True

            # teste elargissement
            if(support_ascendant == True and resistance_horizontal == True):
                elargissement_ascendant = True
            if(support_horizontal == True and resistance_descendant == True):
                elargissement_descendant = True
            if(support_ascendant == True and resistance_descendant == True):
                elargissement_asymetrique = True

            # double triple top bottom
            if(support_horizontal):
                double_bottom = True
                triple_bottom = True
                epaule_tete_epaule_inverse = True
            if(resistance_horizontal):
                triple_bottom = True
                double_bottom = True
                epaule_tete_epaule = True

            # avalement de retournement haussier et baissier
            if(data["askclose"].iloc[-3] >= data["askclose"].iloc[-2] and data["askopen"].iloc[-3] <= data["askopen"].iloc[-2] and data["askopen"].iloc[-2] > data["askclose"].iloc[-2] and (abs(data["askopen"].iloc[-3] - data["askclose"].iloc[-3]) < abs(data["askopen"].iloc[-2] - data["askclose"].iloc[-2]))):
                avalement_baissier = True
            if(data["askclose"].iloc[-3] <= data["askclose"].iloc[-2] and data["askopen"].iloc[-3] >= data["askopen"].iloc[-2] and data["askopen"].iloc[-2] < data["askclose"].iloc[-2] and (abs(data["askopen"].iloc[-3] - data["askclose"].iloc[-3]) < abs(data["askopen"].iloc[-2] - data["askclose"].iloc[-2]))):
                avalement_haussier = True
            
            # marteau de retournement haussier et baissier
            if(abs(data["askclose"].iloc[-2] - data["askopen"].iloc[-2]) < ((data["askhigh"].iloc[-2] - data["asklow"].iloc[-2])/4) and (abs(data["askhigh"].iloc[-2] - data["askclose"].iloc[-2]) > abs((data["askclose"].iloc[-2] - data["asklow"].iloc[-2]) * 3))):
                marteau_retournement_baissier = True
            if(abs(data["askclose"].iloc[-2] - data["askopen"].iloc[-2]) < ((data["askhigh"].iloc[-2] - data["asklow"].iloc[-2])/4) and (abs(data["askclose"].iloc[-2] - data["asklow"].iloc[-2]) > abs((data["askhigh"].iloc[-2] - data["askclose"].iloc[-2]) * 3))):
                marteau_retournement_haussier = True

            # buy position
            """ if(avalement_haussier == True or marteau_retournement_haussier == True or triple_bottom == True or double_bottom == True or epaule_tete_epaule_inverse == True):
                operation = -1
                SetStopLoss(-2)
                SetTakeProfit(10) """
            # sell position
            """ if(avalement_baissier == True or marteau_retournement_baissier == True or triple_top == True or double_top == True or epaule_tete_epaule == True):
                operation = 1
                SetStopLoss(-2)
                SetTakeProfit(10) """
            return True
        except Exception as e:
            print(">>> Erreur durant l'étude des figures chartiste', source d'erreur :", e)
            return False
        