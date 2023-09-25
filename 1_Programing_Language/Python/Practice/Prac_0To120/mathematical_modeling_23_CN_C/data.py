import os 
import json
import functools

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from scipy import optimize
from statsmodels.tsa.arima.model import ARIMA 

from common import clock, DEFAULT_FMT_TIME

plt.rcParams['font.sans-serif'] = ['SimHei'] 
plt.rcParams['axes.unicode_minus'] = False 

CLS_NAME = ('花叶类', '花菜类', '水生根茎类', '茄类', '辣椒类', '食用菌')
CLS_NAME_EN = ('flower_leaf', 'flower_cauliflower', 'water_root', 'eggplant', 'pepper', 'mushroom')


# set current file path as root
root = os.path.dirname(os.path.abspath(__file__))
os.chdir(root)


@clock(DEFAULT_FMT_TIME)
def calculate_predict_data():
    with open('./C/data/sv_grey.json', 'r') as f:
        sv_grey = json.load(f)
    with open('./C/data/profit_grey.json', 'r') as f:
        profit_grey = json.load(f)
    with open('./C/data/cost_grey.json', 'r') as f:
        cost_grey = json.load(f)
    with open('./C/data/data4.json', 'r') as f:
        data4 = json.load(f)
    
    # code -- [sv * profit, cost + profit]
    # save in predict.xlsx
    code2predict = {}
    for code in sv_grey.keys():
        code2predict[code] = [sv_grey[code] * profit_grey[code], cost_grey[code] + profit_grey[code], 
                                sv_grey[code] / float(1 - data4[code][1] / 100)]
    df = pd.DataFrame(code2predict).T
    df.columns = ['单品利润x销量', '预测定价', '预测进货量']
    df.to_excel('./C/data/predict.xlsx')


@clock(DEFAULT_FMT_TIME)
def grey_prediction_sv():
    if not os.path.exists('./C/data/data2_last7days.json'):
        select_last7days()
    with open('./C/data/data2_last7days.json', 'r') as f:
        data2_last7days = json.load(f)

    code_set = set() 
    for code2msg_list in data2_last7days.values():
        code_set_tmp = set()
        for code in code2msg_list.keys():
            code_set_tmp.add(code) 
        if len(code_set) == 0:
            code_set = code_set_tmp
        code_set = code_set & code_set_tmp
    
    codeT7daysSv = dict.fromkeys(code_set)
    for code in codeT7daysSv.keys():
        codeT7daysSv[code] = []
    for code in code_set:
        for date in data2_last7days.keys():

            msg = data2_last7days[date][code]
            sv = sum([msg[i][0] for i in range(len(msg))]) 
            codeT7daysSv[code].append(sv)

    # calculate the grey prediction
    code2grey = dict.fromkeys(code_set)
    for code in code2grey.keys():
        code2grey[code] = None

    num = 8
    for code, sv_list in codeT7daysSv.items():
        n = len(sv_list)
        accumulation = np.cumsum(sv_list)
        mean_acc = (accumulation[1:] + accumulation[:-1]) / 2

        X = np.column_stack((-mean_acc, np.ones(n - 1)))
        Y = sv_list[1:]
        a, b = np.linalg.lstsq(X, Y, rcond=None)[0]

        predict_accmulation = (sv_list[0] - b / a) * np.exp(-a * np.arange(1, num + n))

        prediction = np.zeros(num)
        prediction[0] = sv_list[0]
        for i in range(1, num):
            prediction[i] = predict_accmulation[i] - predict_accmulation[i - 1]

        code2grey[code] = prediction[-1]
    
    with open('./C/data/sv_grey.json', 'w') as f:
        json.dump(code2grey, f)

    # draw the grey prediction
    # draw  the sales volume of each code in the last 7 days and the grey prediction of the next day    
    # then circle the grey prediction
    for code in code_set:
        codeT7daysSv[code].append(code2grey[code])
        plt.figure()
        plt.plot(range(8), codeT7daysSv[code], label=code)
        plt.scatter(7, code2grey[code], s=100, c='r', marker='o')
        plt.legend(loc='upper left')
        plt.xticks(range(8), [i for i in range(1, 8)] + ['grey'])
        if not os.path.exists('./C/img/grey_prediction/sv'):
            os.mkdir('./C/img/grey_prediction/sv')
        plt.savefig('./C/img/grey_prediction/sv/' + code + '.png')
        plt.close()

    print()


@clock(DEFAULT_FMT_TIME)
def grey_prediction_profit():
    if not os.path.exists('./C/data/data3_last7days.json') or not os.path.exists('./C/data/data2_last7days.json'):
        select_last7days()
    with open('./C/data/data3_last7days.json', 'r') as f:
        data3_last7days = json.load(f)
    with open('./C/data/data2_last7days.json', 'r') as f:
        data2_last7days = json.load(f)

    if not os.path.exists('./C/data/cost_grey.json'):
        grey_prediction_purchase_price()
    with open('./C/data/cost_grey.json', 'r') as f:
        cost_grey = json.load(f)

    code_set = set() 
    for code2msg_list in data2_last7days.values():
        code_set_tmp = set()
        for code in code2msg_list.keys():
            code_set_tmp.add(code) 
        if len(code_set) == 0:
            code_set = code_set_tmp
        code_set = code_set & code_set_tmp
    
    codeT7daysPrice = dict.fromkeys(code_set)
    for code in codeT7daysPrice.keys():
        codeT7daysPrice[code] = []
    for code in code_set:
        for date in data2_last7days.keys():

            msg = data2_last7days[date][code]
            price_sum = sum([msg[i][1] for i in range(len(msg))])
            price = price_sum / len(msg)
            # for i in range(len(msg)):
            #     if not msg[i][3]:
            #         price = msg[i][1]
            #         break
            codeT7daysPrice[code].append(price)


    date2code2cost = dict.fromkeys(data3_last7days.keys())
    for date in date2code2cost.keys():
        date2code2cost[date] = dict.fromkeys(code_set)
    for date, codeAcost_list in data3_last7days.items():
        for code, cost in codeAcost_list:
            if code in code_set:
                date2code2cost[date][code] = cost
    codeTo7daysCost = dict.fromkeys(code_set)
    for code in codeTo7daysCost.keys():
        codeTo7daysCost[code] = []
    for code in code_set:
        for date in data3_last7days.keys():
            codeTo7daysCost[code].append(date2code2cost[date][code])

    codeT7daysProfit = dict.fromkeys(code_set)
    for code in codeT7daysProfit.keys():
        codeT7daysProfit[code] = []
    for code in code_set:
        for i in range(7):
            codeT7daysProfit[code].append(codeT7daysPrice[code][i] - codeTo7daysCost[code][i])


    # calculate the grey prediction
    code2grey = dict.fromkeys(code_set)
    for code in code2grey.keys():
        code2grey[code] = None

    num = 8
    for code, profit_list in codeT7daysProfit.items():
        n = len(profit_list)
        accumulation = np.cumsum(profit_list)
        mean_acc = (accumulation[1:] + accumulation[:-1]) / 2

        X = np.column_stack((-mean_acc, np.ones(n - 1)))
        Y = profit_list[1:]
        a, b = np.linalg.lstsq(X, Y, rcond=None)[0]

        predict_accmulation = (profit_list[0] - b / a) * np.exp(-a * np.arange(1, num + n))

        prediction = np.zeros(num)
        prediction[0] = profit_list[0]
        for i in range(1, num):
            prediction[i] = predict_accmulation[i] - predict_accmulation[i - 1]

        code2grey[code] = prediction[-1]
    
    with open('./C/data/profit_grey.json', 'w') as f:
        json.dump(code2grey, f)

    # draw the grey prediction
    # draw the profit of each code in the last 7 days and the grey prediction of the next day
    # then circle the grey prediction
    for code in code_set:
        codeT7daysProfit[code].append(code2grey[code])
        plt.figure()
        plt.plot(range(8), codeT7daysProfit[code], label=code)
        plt.scatter(7, code2grey[code], s=100, c='r', marker='o')
        plt.legend(loc='upper left')
        plt.xticks(range(8), [i for i in range(1, 8)] + ['grey'])
        if not os.path.exists('./C/img/grey_prediction/profit'):
            os.mkdir('./C/img/grey_prediction/profit')
        plt.savefig('./C/img/grey_prediction/profit/' + code + '.png')
        plt.close()

    print()


@clock(DEFAULT_FMT_TIME)
def grey_prediction_purchase_price():
    if not os.path.exists('./C/data/data3_last7days.json'):
        select_last7days()
    with open('./C/data/data3_last7days.json', 'r') as f:
        data3_last7days = json.load(f)

    code_set = set()
    for codeAcost_list in data3_last7days.values():
        code_set_tmp = set(code for code, _ in codeAcost_list)
        if len(code_set) == 0:
            code_set = code_set_tmp
        code_set = code_set & code_set_tmp

    date2code2cost = dict.fromkeys(data3_last7days.keys())
    for date in date2code2cost.keys():
        date2code2cost[date] = dict.fromkeys(code_set)

    for date, codeAcost_list in data3_last7days.items():
        for code, cost in codeAcost_list:
            if code in code_set:
                date2code2cost[date][code] = cost
        
    codeTo7daysCost = dict.fromkeys(code_set)
    for code in codeTo7daysCost.keys():
        codeTo7daysCost[code] = []
    for code in code_set:
        for date in date2code2cost.keys():
            codeTo7daysCost[code].append(date2code2cost[date][code])


    # calculate the grey prediction
    code2grey = dict.fromkeys(code_set)
    for code in code2grey.keys():
        code2grey[code] = None
    
    num = 8
    for code, cost_list in codeTo7daysCost.items():
        n = len(cost_list)
        accumulation = np.cumsum(cost_list)
        mean_acc = (accumulation[1:] + accumulation[:-1]) / 2

        X = np.column_stack((-mean_acc, np.ones(n - 1)))
        Y = cost_list[1:]
        a, b = np.linalg.lstsq(X, Y, rcond=None)[0]

        predict_accmulation = (cost_list[0] - b / a) * np.exp(-a * np.arange(1, num + n))

        prediction = np.zeros(num)
        prediction[0] = cost_list[0]
        for i in range(1, num):
            prediction[i] = predict_accmulation[i] - predict_accmulation[i - 1]

        code2grey[code] = prediction[-1]
    
    with open('./C/data/cost_grey.json', 'w') as f:
        json.dump(code2grey, f)
        

    # draw the grey prediction
    # draw the cost of each code in the last 7 days and the grey prediction of the next day
    # then circle the grey prediction
    for code in code_set:
        codeTo7daysCost[code].append(code2grey[code])
        plt.figure()
        plt.plot(range(8), codeTo7daysCost[code], label=code)
        plt.scatter(7, code2grey[code], s=100, c='r', marker='o')
        plt.legend(loc='upper left')
        plt.xticks(range(8), [i for i in range(1, 8)] + ['grey'])
        if not os.path.exists('./C/img/grey_prediction/cost'):
            os.mkdir('./C/img/grey_prediction/cost')
        plt.savefig('./C/img/grey_prediction/cost/' + code + '.png')
        plt.close()

    print()


@clock(DEFAULT_FMT_TIME)
def select_last7days():
    if not os.path.exists('./C/data/data3.json') or not os.path.exists('./C/data/data2.json'):
        changeAllExcel2Json()
    with open('./C/data/data3.json', 'r') as f:
        data3 = json.load(f)
    with open('./C/data/data2.json', 'r') as f:
        data2 = json.load(f)

    data3_last7days = {}
    date_last7days = list(data3.keys())[-7:]
    for date in date_last7days:
        data3_last7days[date] = data3[date]
    with open('./C/data/data3_last7days.json', 'w') as f:
        json.dump(data3_last7days, f)

    data2_last7days = {}
    date_last7days = list(data2.keys())[-7:]
    for date in date_last7days:
        data2_last7days[date] = data2[date]
    with open('./C/data/data2_last7days.json', 'w') as f:
        json.dump(data2_last7days, f)


@clock(DEFAULT_FMT_TIME)
def cal_proportion():
    cls_weight = dict.fromkeys(CLS_NAME_EN)
    for cls in cls_weight.keys():
        cls_weight[cls] = 0
    pur_nxt_week = predict_sv_sum_week(156)
    pur_nxt_day = pur_nxt_week / 7
    search_proportion = 0.15 


    if not os.path.exists('./C/data/cls/cls.json'):
        classify_data()
    with open('./C/data/cls/cls.json', 'r') as f:
        vegetable_class = json.load(f)
    code2cls = {}
    for cls, code in vegetable_class.items():
        for code_one in code:
            code2cls[str(code_one)] = cls

    if not os.path.exists('./C/data/date2code2price.json'):
        date2cls2code2profitAcost()
    with open('./C/data/date2code2price.json', 'r') as f:
        date2code2price = json.load(f)

    
    # calculate the price of each class of each day
    date2cls2price = dict.fromkeys(date2code2price.keys())
    for date in date2cls2price.keys():
        date2cls2price[date] = dict.fromkeys(CLS_NAME_EN)
        for cls in date2cls2price[date].keys():
            date2cls2price[date][cls] = 0

    for date, code2price in date2code2price.items():
        for code, price in code2price.items():
            cls = code2cls[code]
            date2cls2price[date][cls] += price

    cls2newestPrice = dict.fromkeys(CLS_NAME_EN)
    all_date = list(date2cls2price.keys())
    last_date = all_date[-1]
    sorted(all_date)
    cls_count = dict.fromkeys(CLS_NAME_EN)
    for cls in cls_count.keys():
        cls_count[cls] = 0
    code2price_lst = date2code2price[last_date]
    for code, _ in code2price_lst.items():
        cls = code2cls[code]
        cls_count[cls] += 1
    
    for cls in cls2newestPrice.keys():
        cls2newestPrice[cls] = date2cls2price[last_date][cls] / cls_count[cls]



    if not os.path.exists('./C/data/cls2pridictOfProACos.json'):
        timeSequencePridict_WeekProACos()
    with open('./C/data/cls2pridictOfProACos.json', 'r') as f:
        cls2pridictOfProACos = json.load(f)

    # if not os.path.exists('./C/data/weekavg_cls2proAcos.json'):
    #     creJsonAImg_weekavg_cls2proAcos()
    # with open('./C/data/weekavg_cls2proAcos.json', 'r') as f:
    #     weekavg_cls2proAcos = json.load(f)

    if not os.path.exists('./C/data/date2cls2code2profitAcost.json'):
        creimg_profit_cls()
    with open('./C/data/date2cls2code2profitAcost.json', 'r') as f:
        date2cls2code2profitAcost = json.load(f)

    data_len = len(date2cls2code2profitAcost)
    search_num = int(data_len * search_proportion)

    # power = [0.1 * i for i in range(1, len(CLS_NAME_EN) + 1)]

    search_cls2code2profitAcost = list(date2cls2code2profitAcost.values())[-search_num:]

    for cls2code2profitAcost1d in search_cls2code2profitAcost:
        cls2proAcost1d = dict.fromkeys(CLS_NAME_EN)
        for cls in cls2proAcost1d.keys():
            cls2proAcost1d[cls] = {
                'profit': 0,
                'cost': 0
            }
        for cls, code2profitAcost in cls2code2profitAcost1d.items():
            for code, profitAcost in code2profitAcost.items():
                cls2proAcost1d[cls]['profit'] += profitAcost[0]
                cls2proAcost1d[cls]['cost'] += profitAcost[1]

        # sort the cls2proAcost1d by profit
        cls2proAcost1d = sorted(cls2proAcost1d.items(), key=lambda x: x[1]['profit'], reverse=True)
        for cls, proAcost in cls2proAcost1d:
            cls_weight[cls] += proAcost['profit'] / 1000

    # pridict one week

    cls_percent_avg = dict.fromkeys(CLS_NAME_EN)
    for cls in cls_percent_avg.keys():
        cls_percent_avg[cls] = 0

    for day in range(7):

        for cls, weight in cls_weight.items():
            cls_percent_avg[cls] += weight / sum(cls_weight.values()) / 7

        profit_sum = 0

        cls_pur = dict.fromkeys(CLS_NAME_EN)
        for cls in cls_pur.keys():
            cls_pur[cls] = 0
        for cls in CLS_NAME_EN:
            cls_pur[cls] = cls_weight[cls] / sum(cls_weight.values()) * pur_nxt_day

        # calculate the profit and cost of each class
        for cls in CLS_NAME_EN:
            cls_profit =  cls_pur[cls] * cls2newestPrice[cls] - cls2pridictOfProACos[cls]['cost'][0]
            # update the cls_weight : decrease the oldest day and increase the newest day

            cls_weight_oldest = 0
            cls2code2profitAcost_oldest = search_cls2code2profitAcost[0]
            for code, profitAcost in cls2code2profitAcost_oldest[cls].items():
                cls_weight_oldest += profitAcost[0]
            cls_weight[cls] -= cls_weight_oldest / 1000
            cls_weight[cls] += cls_profit / 1000
            profit_sum += cls_profit
        
        search_cls2code2profitAcost.pop(0)

        print(f'day {day + 1}:' + ' ' * 10 + f'profit: {profit_sum}')

    for cls, percent in cls_percent_avg.items():
        print(f'{cls}: {percent * 100}%')


@clock(DEFAULT_FMT_TIME)
@functools.lru_cache()
def timeSequencePridict_WeekProACos():
    if not os.path.exists('./C/data/weekavg_cls2proAcos.json'):
        creJsonAImg_weekavg_cls2proAcos()
    
    with open('./C/data/weekavg_cls2proAcos.json', 'r') as f:
        weekavg_cls2proAcos = json.load(f)

    cls2pridictOfProAcos = dict.fromkeys(CLS_NAME_EN)
    for cls in cls2pridictOfProAcos.keys():
        cls2pridictOfProAcos[cls] = {
            'profit': None,
            'cost': None
        }
    for cls in CLS_NAME_EN:
        profit_model = ARIMA(weekavg_cls2proAcos[cls]['profit'], order=(0, 0, 1))
        profit_model_fit = profit_model.fit()
        # cls2pridictOfProAcos[cls]['profit'] = profit_model_fit.forecast()[0][0]
        data_len = len(weekavg_cls2proAcos[cls]['profit'])
        cls2pridictOfProAcos[cls]['profit'] = profit_model_fit.predict(data_len, data_len)

        cost_model = ARIMA(weekavg_cls2proAcos[cls]['cost'], order=(0, 0, 1))
        cost_model_fit = cost_model.fit()
        data_len = len(weekavg_cls2proAcos[cls]['cost'])
        cls2pridictOfProAcos[cls]['cost'] = cost_model_fit.predict(data_len, data_len)

    for cls in CLS_NAME_EN:
        cls2pridictOfProAcos[cls]['profit'] = list(cls2pridictOfProAcos[cls]['profit'])
        cls2pridictOfProAcos[cls]['cost'] = list(cls2pridictOfProAcos[cls]['cost'])
    with open('./C/data/cls2pridictOfProACos.json', 'w') as f:
        json.dump(cls2pridictOfProAcos, f)

    # draw the profit and cost of each class 
    #  and the predict value in different color (circle it)

    x_week = range(1, len(weekavg_cls2proAcos[CLS_NAME_EN[0]]['profit']) + 2)
    for cls in CLS_NAME_EN:
                
        plt.figure()
    
        fig, ax = plt.subplots(figsize=(16, 7))
    
        y_profit = weekavg_cls2proAcos[cls]['profit']
        # append the predict value
        y_profit.append(cls2pridictOfProAcos[cls]['profit'][0])
        y_cost = weekavg_cls2proAcos[cls]['cost']
        # append the predict value
        y_cost.append(cls2pridictOfProAcos[cls]['cost'][0])
    
        ax.plot(x_week, y_profit, label=cls + '_profit')
        ax.legend(loc='upper left')
        ax.set_ylabel('profit')
    
        ax2 = ax.twinx()
        ax2.plot(x_week, y_cost, 'r', label=cls + '_cost')
        ax2.legend(loc='upper right')
        ax2.set_ylabel('cost')


        # circle the predict value
        ax.scatter(x_week[-1], y_profit[-1], s=100, c='b', marker='o')
        ax2.scatter(x_week[-1], y_cost[-1], s=100, c='b', marker='o')

        plt.xticks(np.linspace(0, len(x_week) - 1, 6), [x_week[int(i)] for i in np.linspace(0, len(x_week) - 1, 6)])
        
    
    
        if not os.path.exists('./C/img/pridict_week'):
            os.mkdir('./C/img/pridict_week')
        if not os.path.exists('./C/img/pridict_week/timeSequencePridict'):
            os.mkdir('./C/img/pridict_week/timeSequencePridict')
        plt.savefig('./C/img/pridict_week/timeSequencePridict/' + cls + '.png')
        plt.close() 


   

    return cls2pridictOfProAcos


@clock(DEFAULT_FMT_TIME)
@functools.lru_cache()
def creJsonAImg_weekavg_cls2proAcos():
    if not os.path.exists('./C/data/cls/cls.json'):
        classify_data()
    with open('./C/data/cls/cls.json', 'r') as f:
        vegetable_class = json.load(f)
    code2cls = {}
    for cls, code in vegetable_class.items():
        for code_one in code:
            code2cls[str(code_one)] = cls
    if not os.path.exists('./C/data/date2cls2code2profitAcost.json'):
        creimg_profit_cls()
    with open('./C/data/date2cls2code2profitAcost.json', 'r') as f:
        date2cls2code2profitAcost = json.load(f)
    
    if not os.path.exists('./C/data/weekavg_cls2proAcos.json'):
        day = 0
        week_count = 0
        cur_date = None
        weekavg_cls2proAcos = dict.fromkeys(CLS_NAME_EN)
        for cls in weekavg_cls2proAcos.keys():
            weekavg_cls2proAcos[cls] = {
                'profit': [],
                'cost': []
            }
        cls2proAcos_1W = dict.fromkeys(CLS_NAME_EN)
        for cls in cls2proAcos_1W.keys():
            cls2proAcos_1W[cls] = {
                'profit': 0,
                'cost': 0
            }
        for date, cls2code2profitAcost in date2cls2code2profitAcost.items():
            if cur_date is None:
                cur_date = date
            if cur_date != date:
                day += 1
                cur_date = date
                if day % 7 == 0:
                    week_count += 1
                    for cls, code2profitAcost in cls2proAcos_1W.items():
                        weekavg_cls2proAcos[cls]['profit'].append(code2profitAcost['profit'] / 7)
                        weekavg_cls2proAcos[cls]['cost'].append(code2profitAcost['cost'] / 7)
                        cls2proAcos_1W[cls]['profit'] = 0
                        cls2proAcos_1W[cls]['cost'] = 0

            for cls, code2profitAcost in cls2code2profitAcost.items():
                cls2proAcos_1W[cls]['profit'] += sum([profitAcost[0] for profitAcost in code2profitAcost.values()])
                cls2proAcos_1W[cls]['cost'] += sum([profitAcost[1] for profitAcost in code2profitAcost.values()])

        with open('./C/data/weekavg_cls2proAcos.json', 'w') as f:
            json.dump(weekavg_cls2proAcos, f)
    else:
        with open('./C/data/weekavg_cls2proAcos.json', 'r') as f:
            weekavg_cls2proAcos = json.load(f)

    # draw the profit and cost of each class
    x_week = range(1, len(weekavg_cls2proAcos[CLS_NAME_EN[0]]['profit']) + 1)
    for cls in CLS_NAME_EN:
            
        plt.figure()
    
        fig, ax = plt.subplots(figsize=(16, 7))
    
        y_profit = weekavg_cls2proAcos[cls]['profit']
        y_cost = weekavg_cls2proAcos[cls]['cost']
    
        ax.plot(x_week, y_profit, label=cls + '_profit')
        ax.legend(loc='upper left')
        ax.set_ylabel('profit')
    
        ax2 = ax.twinx()
        ax2.plot(x_week, y_cost, 'r', label=cls + '_cost')
        ax2.legend(loc='upper right')
        ax2.set_ylabel('cost')
    
        plt.xticks(np.linspace(0, len(x_week) - 1, 6), [x_week[int(i)] for i in np.linspace(0, len(x_week) - 1, 6)])
    
        if not os.path.exists('./C/img/weekavg'):
            os.mkdir('./C/img/weekavg')
        plt.savefig('./C/img/weekavg/' + cls + '.png')
        plt.close()


@clock(DEFAULT_FMT_TIME)
@functools.lru_cache()
def creimg_profit_cls():

    # if I want to calculate the profit of each class, I should know the cost first, of course.
    # cost = cost_per * purchase quantity
    # and purchase quantity = sales volume / (1 - loss%)
    # then profit = sales volume * price - cost

    # Cause I have to draw a picture of the profit and cost of each class, and use the date as the x-axis,
    # so I suppose to create a map from date to class to profit and cost.
    # dict { date : { cls : (profit, cost) } }

    # get the class tabel then create a map from code to class
    if not os.path.exists('./C/data/cls/cls.json'):
        classify_data()
    with open('./C/data/cls/cls.json', 'r') as f:
        vegetable_class = json.load(f)
    code2cls = {}
    for cls, code in vegetable_class.items():
        for code_one in code:
            code2cls[str(code_one)] = cls

    if not os.path.exists('./C/data/date2codeAsvh.json'):
        sv_sum_everyWeek_linefitting()
    with open('./C/data/date2codeAsvh.json', 'r') as f:
        date2codeAsvh = json.load(f)

    # why not create a map from date to class to price? And then create a map from date to class to sales volume?
    # That's COOL!
    # dist { date : { cls : price } } ps: a good's price won't change in a day
    # dist { date : { cls : sales volume } } ps: you should know one type of goods not only
    # sell one in a day, so you should calculate the sum of sales volume of one type of goods in a day.
    if not os.path.exists('./C/data/date2code2price.json') or not os.path.exists('./C/data/date2code2sv.json'):
        # load the data from extral2.xlsx
        # Well, I think I should change the excel to a json file first,
        # so that I won't need to load the data from excel every time. (THAT'S TOO SLOW!)
        # But since I have already done this, I won't change it.
        # (I will change it in the function after this function (probably...))
        data2 = pd.read_excel('./C/extral2.xlsx')

        date2code2price = dict.fromkeys(date2codeAsvh.keys())
        for date in date2code2price.keys():
            date2code2price[date] = {}

        date2code2sv = dict.fromkeys(date2codeAsvh.keys())
        for date in date2code2sv.keys():
            date2code2sv[date] = {}

        for date, code, sv, price in data2[['销售日期', '单品编码', '销量(千克)', '销售单价(元/千克)']].values:
            date = str(date)[:10]
            code = str(int(code))

            # cause the key is from date2codeAsvh,
            # so I'm not sure whether all date is contained in date2code2price and date2code2sv.
            # However, I'm sure that just a few date won't influence the result. So I just ignore it.
            if date2code2price.get(date) is None:
                continue

            date2code2price[date][code] = price

            try: # if the date->code->sales volume is already exist, then add the sales volume
                date2code2sv[date][code] += sv
            except: # if not, then create a new one
                date2code2sv[date][code] = sv

        with open('./C/data/date2code2price.json', 'w') as f:
            json.dump(date2code2price, f)
        with open('./C/data/date2code2sv.json', 'w') as f:
            json.dump(date2code2sv, f)
    else:
        with open('./C/data/date2code2price.json', 'r') as f:
            date2code2price = json.load(f)
        with open('./C/data/date2code2sv.json', 'r') as f:
            date2code2sv = json.load(f)

    # And, the same as the above, create a map from date to class to purchase quantity.
    # dict { date : { cls : purchase quantity } }
    if not os.path.exists('./C/data/date2code2purchase.json'):
        date2code2purchase = dict.fromkeys(date2codeAsvh.keys())
        for date in date2code2purchase.keys():
            date2code2purchase[date] = {}
        for date, codeApur in date2codeAsvh.items():
            for code_one, pur_one in codeApur:
                try:
                    date2code2purchase[date][str(int(code_one))] += pur_one
                except:
                    date2code2purchase[date][str(code_one)] = pur_one

        with open('./C/data/date2code2purchase.json', 'w') as f:
            json.dump(date2code2purchase, f)
    else:
        with open('./C/data/date2code2purchase.json', 'r') as f:
            date2code2purchase = json.load(f)
        
    # Finally! This map is the main target of this function!
    # dict { date : { cls : code : (profit, cost) } }
    # Yep, I know it's a little bit complex, but, there is the end of matter...
    if not os.path.exists('./C/data/date2cls2code2profitAcost.json'):

        # build a blank map: dict { date : { cls : code : {} } }
        date2cls2code2profitAcost = dict.fromkeys(date2codeAsvh.keys())
        for date in date2cls2code2profitAcost.keys():
            date2cls2code2profitAcost[date] = dict.fromkeys(CLS_NAME_EN)
            for cls in date2cls2code2profitAcost[date].keys():
                date2cls2code2profitAcost[date][cls] = {}

        # calculate the profit and cost of each class of each day  
        data3 = pd.read_excel('./C/extral3.xlsx')
        for date, code, cost_per in data3[['日期', '单品编码', '批发价格(元/千克)']].values:
            date = str(date)[:10]
            try:
                cls = code2cls[str(int(code))]
            except:
                cls = code2cls[int(code)]
            
            # the same reason as above, just ignore the date which is not in date2cls2code2profitAcost
            if date2cls2code2profitAcost.get(date) is None:
                continue

            purchase, sv, price = 0, 0, 0
            try:
                purchase = date2code2purchase[date][str(int(code))]
            except:
                try:
                    purchase = date2code2purchase[date][str(code)]
                except:
                    continue
            try:
                sv = date2code2sv[date][str(int(code))]
            except:
                try:
                    sv = date2code2sv[date][str(code)]
                except:
                    continue
            try:
                price = date2code2price[date][str(int(code))]
            except:
                try:
                    price = date2code2price[date][str(code)]
                except:
                    continue
            if purchase == 0 or price == 0:
                continue
            cost = cost_per * purchase
            profit = sv * price - cost


            date2cls2code2profitAcost[date][cls][str(int(code))] = (profit, cost)

        with open('./C/data/date2cls2code2profitAcost.json', 'w') as f:
            json.dump(date2cls2code2profitAcost, f)
    else:
        with open('./C/data/date2cls2code2profitAcost.json', 'r') as f:
            date2cls2code2profitAcost = json.load(f)

    # draw the profit and cost of each class
    x_date, cls2code2profitAcost = tuple(date2cls2code2profitAcost.keys()), date2cls2code2profitAcost.values()

    for cls in CLS_NAME_EN:

        plt.figure()

        fig, ax = plt.subplots(figsize=(16, 7))

        y_profit = []
        y_cost = []
        for cls2code2profitAcost_1d in cls2code2profitAcost:
            try:
                code2proAcos = cls2code2profitAcost_1d[cls]
                profit = sum([profitAcost[0] for profitAcost in code2proAcos.values()])
                cost = sum([profitAcost[1] for profitAcost in code2proAcos.values()])
            except:
                profit = 0
                cost = 0
            y_profit.append(profit)
            y_cost.append(cost)

        ax.plot(range(len(x_date)), y_profit, label=cls + '_profit')
        ax.legend(loc='upper left')
        ax.set_ylabel('profit')

        ax2 = ax.twinx()
        ax2.plot(range(len(x_date)), y_cost, 'r', label=cls + '_cost')
        ax2.legend(loc='upper right')
        ax2.set_ylabel('cost')

        plt.xticks(np.linspace(0, len(x_date) - 1, 6), [x_date[int(i)] for i in np.linspace(0, len(x_date) - 1, 6)], rotation=30)

        if not os.path.exists('./C/img/profit'):
            os.mkdir('./C/img/profit')
        plt.savefig('./C/img/profit/' + cls + '.png')
        plt.close()


# DONE
@clock(DEFAULT_FMT_TIME)
@functools.lru_cache()
def predict_sv_sum_week(week) -> float:
    if not os.path.exists('./C/data/sv_sum_everyWeek_linefitting.json'):
        sv_sum_everyWeek_linefitting()
    with open('./C/data/sv_sum_everyWeek_linefitting.json', 'r') as f:
        z7 = json.load(f)
    return np.polyval(z7, week)


# DONE
@clock(DEFAULT_FMT_TIME)
@functools.lru_cache()
def sv_sum_everyWeek_linefitting():

    # get the class tabel then create a map from code to class
    if not os.path.exists('./C/data/cls/cls.json'):
        classify_data()
    with open('./C/data/cls/cls.json', 'r') as f:
        vegetable_class = json.load(f)
    code2cls = {}
    for cls, code in vegetable_class.items():
        for code_one in code:
            code2cls[str(code_one)] = cls

    # create a map from class to code and loss : dict{ cls : [(code, loss), ...] }
    cls2codeAloss = dict.fromkeys(CLS_NAME_EN)
    for cls in cls2codeAloss.keys():
        cls2codeAloss[cls] = []

    # save as a json file
    if not os.path.exists('./C/data/cls2codeAloss.json'):
        data4 = pd.read_excel('./C/extral4.xlsx')
        for code, loss in data4[['单品编码', '损耗率(%)']].values:
            code = str(int(code))
            try:
                cls = code2cls[code]
            except:
                cls = code2cls[int(code)]
            cls2codeAloss[cls].append((code, loss))
        with open('./C/data/cls2codeAloss.json', 'w') as f:
            json.dump(cls2codeAloss, f)
    else:
        with open('./C/data/cls2codeAloss.json', 'r') as f:
            cls2codeAloss = json.load(f)

    # create a map from date to code and purchase quantity : dict{ date : [(code, purchase), ...] }
    if not os.path.exists('./C/data/date2codeAsvh.json'):
        data2 = pd.read_excel('./C/extral2.xlsx')
        date2codeAsvh = {}
        for date, code, sv in data2[['销售日期', '单品编码', '销量(千克)']].values:
            date = str(date)[:10]
            if date2codeAsvh.get(date) is None:
                date2codeAsvh[date] = []
            cls = code2cls[str(code)]
            loss = 0
            for code_one, loss in cls2codeAloss[cls]:
                if code_one == str(code):
                    loss = float(loss)
                    break
            if loss == 0:
                continue
            date2codeAsvh[date].append((code, sv / (1 - loss / 100))) # purchase quantity = sales volume / (1 - loss%)
        with open('./C/data/date2codeAsvh.json', 'w') as f:
            json.dump(date2codeAsvh, f)
    else:
        with open('./C/data/date2codeAsvh.json', 'r') as f:
            date2codeAsvh = json.load(f)
    
    # calculate the purchase quantity of each week
    pur_sum_everyWeek = []
    pur_sum_1W = 0
    day = 0
    for _, svh in date2codeAsvh.items():
        pur_sum_1W += sum([sv for _, sv in svh])
        day += 1
        if day % 7 == 0:
            pur_sum_everyWeek.append(pur_sum_1W)
            pur_sum_1W = 0

    # draw the purchase quantity of each week
    plt.figure()
    plt.xlabel('week')
    plt.ylabel('purchase quantity')
    plt.title('purchase quantity of each week')
    plt.plot(range(1, len(pur_sum_everyWeek) + 1), pur_sum_everyWeek)
    plt.savefig('./C/img/pur_sum_everyWeek_original.png')
    plt.close()

    # polynomial fitting: y = a0 + a1 * x + a2 * x^2 + ... + a7 * x^7
    x = np.array(range(1, len(pur_sum_everyWeek) + 1))
    y = np.array(pur_sum_everyWeek)
    z7 = np.polyfit(x, y, 7)
    p7 = np.poly1d(z7)
    yvals = p7(x)
    plt.figure()
    plt.xlabel('week')
    plt.ylabel('purchase quantity')
    plt.title('purchase quantity of each week')
    plt.plot(x, y, label='original values')
    plt.plot(x, yvals, label='polyfit values')
    plt.legend()
    plt.savefig('./C/img/sv_sum_everyWeek_linefitting.png')
    plt.close()

    # save the polynomial fitting result to a txt file
    with open('./C/data/sv_sum_everyWeek_linefitting.txt', 'w') as f:
        # polynomial fitting function
        f.write('polyfit function:\n' + str(z7) + '\n') 
        f.write('corrcoef: ' + str(np.corrcoef(y, yvals)[0][1]))

    # save the polynomial fitting function to a json file
    with open('./C/data/sv_sum_everyWeek_linefitting.json', 'w') as f:
        json.dump(list(z7), f)

    print('polyfit function:\n' + str(p7))


# DONE
@clock(DEFAULT_FMT_TIME)
@functools.lru_cache()
def corrcoef_goods():
       
    data1 = pd.read_excel('./C/extral1.xlsx')

    if not os.path.exists('./C/data'):
        os.mkdir('./C/data')

    # create a map to save the goods which have different types : dict{ type-name : [(code, name), ...] }
    if not os.path.exists('./C/data/same_type.json') or not os.path.exists('./C/data/same_type.txt'):
        code_name_dict = {}
        name_code_dict = {}

        for code, name in data1[['单品编码', '单品名称']].values:
            name_code_dict[code] = name
            # process the name
            if name.find('(') != -1:
                name = name[:name.find('(')]
            if code_name_dict.get(name) is None:
                code_name_dict[name] = []
            code_name_dict[name].append(code)

        same_type = {}
        for name, code in code_name_dict.items():
            if len(code) > 1:
                same_type[name] = []
                same_type[name].extend( [(code_one, name_code_dict[code_one]) for code_one in code] ) 

        with open('./C/data/same_type.json', 'w') as f:
            json.dump(same_type, f) 

        with open('./C/data/same_type.txt', 'w') as f:
            for name, code in same_type.items():
                f.write(name + '\n')
                for code_tmp, name_tmp in code:
                    f.write(str(code_tmp) + ' ' + name_tmp + '\n')
                f.write('\n')
    else:
        with open('./C/data/same_type.json', 'r') as f:
            same_type = json.load(f)

    # create a map from code to sales volume : dict{ code : [(date, sales volume), ...] } 
    # (only contain the goods which have different types)
    if not os.path.exists('./C/data/same_type_goods_code2msg.json'):
        data2 = pd.read_excel('./C/extral2.xlsx')
        code2msg = {}
        for code in same_type.values():
            for code_one, _ in code:
                code2msg[code_one] = []
        for data2_date, data2_code, data2_sv in data2[['销售日期', '单品编码', '销量(千克)']].values:
            data2_date = str(data2_date)[:10] # get rid of the time
            if code2msg.get(data2_code) is None:
                continue
            else:
                code2msg[data2_code].append((data2_date, data2_sv))

        with open('./C/data/same_type_goods_code2msg.json', 'w') as f:
            json.dump(code2msg, f)
    else:
        with open('./C/data/same_type_goods_code2msg.json', 'r') as f:
            code2msg = json.load(f)
        
    # draw the sales volume of each goods which have different types
    if not os.path.exists('./C/img/same_type/'):
        os.mkdir('./C/img/same_type/')
    for name, code in same_type.items():
        plt.figure()
        plt.xlabel('date')
        plt.ylabel('sales volume')
        plt.title(name)
        date1day = []
        sv1day = []
        max_len = 0
        longest_date = None
        for code_one, name_one in code:
            try:
                msg = code2msg[code_one]
            except:
                msg = code2msg[str(code_one)]
            if len(msg) == 0:
                continue
            for date, sv in msg:
                date = date[:10]

                if date not in date1day:
                    date1day.append(date)
                    sv1day.append(sv)
                else:
                    sv1day[date1day.index(date)] += sv

            plt.scatter(range(len(date1day)), sv1day, s=1, label=name_one)
            if len(date1day) > max_len:
                max_len = len(date1day)
                longest_date = date1day
            date1day = []
            sv1day = []

        plt.xticks(np.linspace(0, len(longest_date) - 1, 6), [longest_date[int(i)] for i in np.linspace(0, len(longest_date) - 1, 6)], rotation=30)
        plt.legend()
        plt.savefig('./C/img/same_type/' + name + '.png')
        plt.close()

    # count the correlation coefficient of each pair of goods which have different types
    with open('./C/data/same_type_goods_corrcoef.txt', 'w') as f:
        for name, code in same_type.items():
            f.write(name + '\n')
            for i in range(len(code)):
                for j in range(i + 1, len(code)):
                    name1, name2 = code[i][1], code[j][1]
                    f.write(name1 + ' ' + name2 + ' ')
                    try:
                        code1, code2 = code[i][0], code[j][0]
                        msg1, msg2 = code2msg[code1], code2msg[code2]
                    except:
                        code1, code2 = str(code[i][0]), str(code[j][0])
                        msg1, msg2 = code2msg[code1], code2msg[code2]

                    try:
                        date_start = max(msg1[0][0], msg2[0][0])
                        date_end = min(msg1[-1][0], msg2[-1][0])
                    except:
                        f.write('0\n')
                        continue

                    _msg1, _msg2 = [], []
                    for msg in msg1:
                        if msg[0] >= date_start and msg[0] <= date_end:
                            _msg1.append(msg)
                    for msg in msg2:
                        if msg[0] >= date_start and msg[0] <= date_end:
                            _msg2.append(msg)
                    msg1, msg2 = _msg1, _msg2

                    date1 = [msg[0] for msg in msg1]
                    date2 = [msg[0] for msg in msg2]

                    date_set = set(date1) | set(date2)
                    if len(date_set) <= 2:
                        f.write('0\n')
                        continue

                    sv1, sv2 = [], []

                    for date in date_set:
                        if date in date1:
                            sum_date_sv1 = 0
                            for msg in msg1:
                                if msg[0] == date:
                                    sum_date_sv1 += msg[1]
                            sv1.append(sum_date_sv1)
                        else:
                            sv1.append(0)
                        if date in date2:
                            sum_date_sv2 = 0
                            for msg in msg2:
                                if msg[0] == date:
                                    sum_date_sv2 += msg[1]
                            sv2.append(sum_date_sv2)
                        else:
                            sv2.append(0)
                    f.write(str(np.corrcoef(sv1, sv2)[0][1]) + '\n')
            f.write('\n')


# DONE 
@clock(DEFAULT_FMT_TIME)
@functools.lru_cache()
def corrcoef_clsAcls_year():

    if not os.path.exists('./C/data/sv_cls_year.json'):
        crejsonAimg_sv_cls_year()
    with open('./C/data/sv_cls_year.json', 'r') as f:
        cls_sales_each_week = json.load(f)
    
    # count the correlation coefficient of each pair of classes
    with open('./C/data/corrcoef_clsAcls_year.txt', 'w') as f:
        for i in range(len(CLS_NAME_EN)):
            for j in range(i + 1, len(CLS_NAME_EN)):
                cls1, cls2 = CLS_NAME_EN[i], CLS_NAME_EN[j]
                cls1_sales = cls_sales_each_week[cls1]
                cls2_sales = cls_sales_each_week[cls2]
                f.write(cls1 + ' ' + cls2 + ' ' + str(np.corrcoef(cls1_sales, cls2_sales)[0][1]) + '\n')


# DONE 
@clock(DEFAULT_FMT_TIME)
@functools.lru_cache()
def corrcoef_clsAcls_month():
    if not os.path.exists('./C/data/month'):
        crejsonAimg_sv_cls_month()
    if len(os.listdir('./C/data/month')) == 0:
        crejsonAimg_sv_cls_month()
    json_files = os.listdir('./C/data/month')

    # count the correlation coefficient of each pair of classes of each month
    with open('./C/data/corrcoef_clsAcls_month.txt', 'w') as f:
        for json_file in json_files:
            f.write(json_file.split('.')[0] + '\n')
            with open('./C/data/month/' + json_file, 'r') as f1:
                sv_cls_month = json.load(f1)
            for i in range(len(CLS_NAME_EN)):
                for j in range(i + 1, len(CLS_NAME_EN)):
                    cls1, cls2 = CLS_NAME_EN[i], CLS_NAME_EN[j]
                    cls1_sales = sv_cls_month[cls1]
                    cls2_sales = sv_cls_month[cls2]
                    f.write(cls1 + ' ' + cls2 + ' ' + str(np.corrcoef(cls1_sales, cls2_sales)[0][1]) + '\n')
    
    count_corrcoef_month_ov06()


# DONE
@clock(DEFAULT_FMT_TIME)
@functools.lru_cache()
def creimg_svAprice():
    if not os.path.exists('./C/data/cls/cls.json'):
        classify_data()
    with open('./C/data/cls/cls.json', 'r') as f:
        vegetable_class = json.load(f)
    code2cls = {}
    for cls, code in vegetable_class.items():
        for code_one in code:
            code2cls[str(code_one)] = cls

    if not os.path.exists('./C/data/cls_svAprice.json'):
        data2 = pd.read_excel('./C/extral2.xlsx')
        # data2 = pd.read_excel('./C/test.xlsx')
        cls_svAprice = dict.fromkeys(CLS_NAME_EN)
        for cls in cls_svAprice.keys():
            cls_svAprice[cls] = ([], []) # (price, sv)
        avg_cls_sv_1day = [0 for _ in range(len(CLS_NAME_EN))]
        avg_cls_price_1day = [0 for _ in range(len(CLS_NAME_EN))]
        count_day = 0
        cur_date = None
        for date, code, sv, price in data2[['销售日期', '单品编码', '销量(千克)', '销售单价(元/千克)']].values:
            count_day += 1
            date = str(date)[:10]
            if cur_date is None:
                cur_date = date
            if cur_date != date:
                avg_cls_price_1day = [avg_cls_price_1day[i] / count_day for i in range(len(CLS_NAME_EN))]
                avg_cls_sv_1day = [avg_cls_sv_1day[i] / count_day for i in range(len(CLS_NAME_EN))]
                for i in range(len(CLS_NAME_EN)):
                    cls_svAprice[CLS_NAME_EN[i]][0].append(avg_cls_price_1day[i])
                    cls_svAprice[CLS_NAME_EN[i]][1].append(avg_cls_sv_1day[i])
                avg_cls_sv_1day = [0 for _ in range(len(CLS_NAME_EN))]
                avg_cls_price_1day = [0 for _ in range(len(CLS_NAME_EN))]
                count_day = 0
                cur_date = date
            try:
                cls = code2cls[str(code)]
            except:
                continue

            avg_cls_price_1day[CLS_NAME_EN.index(cls)] += price
            avg_cls_sv_1day[CLS_NAME_EN.index(cls)] += sv

        for i in range(len(CLS_NAME_EN)):
            avg_cls_price_1day[i] /= count_day
            avg_cls_sv_1day[i] /= count_day
            cls_svAprice[CLS_NAME_EN[i]][0].append(avg_cls_price_1day[i])
            cls_svAprice[CLS_NAME_EN[i]][1].append(avg_cls_sv_1day[i])
        
        with open('./C/data/cls_svAprice.json', 'w') as f:
            json.dump(cls_svAprice, f)
    else:
        with open('./C/data/cls_svAprice.json', 'r') as f:
            cls_svAprice = json.load(f)

    # calculate the correlation coefficient between price and sv of each class
    with open('./C/data/corrcoef_clsAcls_svAprice.txt', 'w') as f:
        for cls, svAprice in cls_svAprice.items():
            f.write(cls + ' ' + str(np.corrcoef(svAprice[0], svAprice[1])[0][1]) + '\n')

    # draw the price and sv of each class 
    for cls, svAprice in cls_svAprice.items():
        plt.figure()
        # draw price line and sv line

        fig, ax = plt.subplots(figsize=(16, 7))

        ax.plot(range(1, len(svAprice[0]) + 1), svAprice[0], label='price')
        ax.legend(loc='upper left')
        ax.set_ylabel('price')

        ax2 = ax.twinx()
        ax2.plot(range(1, len(svAprice[1]) + 1), svAprice[1], 'r', label='sv')
        ax2.legend(loc='upper right')
        ax2.set_ylabel('sv')

        ax.set_xlabel('day')
        ax.set_title(cls)

        # plt.plot(range(1, len(svAprice[0]) + 1), svAprice[0], label='price')
        # plt.plot(range(1, len(svAprice[1]) + 1), svAprice[1], label='sv')
        # plt.legend()
        # plt.xlabel('day')
        # plt.ylabel('price/sv')
        # plt.title(cls)
        
        if not os.path.exists('./C/img/svAprice'):
            os.mkdir('./C/img/svAprice')
        plt.savefig('./C/img/svAprice/' + cls + '.png')
        plt.close()

    for cls, svAprice in cls_svAprice.items():
        plt.figure()
        plt.scatter(svAprice[0], svAprice[1], s=1)
        plt.xlabel('price')
        plt.ylabel('sv')
        plt.title(cls)
        if not os.path.exists('./C/img/svAprice_scatter'):
            os.mkdir('./C/img/svAprice_scatter')
        plt.savefig('./C/img/svAprice_scatter/' + cls + '.png')
        plt.close()

    # I
    if not os.path.exists('./C/data/svAprice_polyfit.txt'):
        os.remove('./C/data/svAprice_polyfit.txt')
    # linear regression
    for cls, svAprice in cls_svAprice.items():
        x = np.array(svAprice[0])
        y = np.array(svAprice[1])
        z3 = np.polyfit(x, y, 3)
        p3 = np.poly1d(z3)
        yvals = p3(x)
        plt.figure()
        plt.xlabel('price')
        plt.ylabel('sv')
        plt.title(cls)
        plt.scatter(x, y, s=1, label='original values')
        plt.plot(x, yvals, 'r', label='polyfit values')
        plt.legend()
        if not os.path.exists('./C/img/svAprice_polyfit'):
            os.mkdir('./C/img/svAprice_polyfit')
        plt.savefig('./C/img/svAprice_polyfit/' + cls + '.png')
        plt.close()

        # save the polynomial fitting result to a txt file
        with open('./C/data/svAprice_polyfit.txt', 'a') as f:
            # polynomial fitting function
            f.write(cls + ':\n' + str(z3) + '\n') 
            f.write('corrcoef: ' + str(np.corrcoef(y, yvals)[0][1]) + '\n')
        

# DONE
@clock(DEFAULT_FMT_TIME)
@functools.lru_cache()
def draw_msg_date(): # draw the sales msg according to date

    if not os.path.exists('./C/data'):
        os.mkdir('./C/data')
    
    data1 = pd.read_excel('./C/extral1.xlsx')
    data2 = pd.read_excel('./C/extral2.xlsx')

    # cls_dict: key: cls_name, value: item code
    cls_dict_clsname_code = dict.fromkeys(CLS_NAME)
    # cls_dict2: key: cls_code, value: item code 
    cls_dict_code_clsname = {}

    for code, cls_name in data1[['单品编码', '分类名称']].values:
        # create a map from cls_name to all item code in this class
        if cls_dict_clsname_code[cls_name] is None:
            cls_dict_clsname_code[cls_name] = []
        cls_dict_clsname_code[cls_name].append(code)

        # create a map from item code to cls_name
        cls_dict_code_clsname[code] = cls_name
    
    # sales volume of each class in one day based on date
    sv_cls_date = {}
    cls_name = None
    for date, code, sales_volume in data2[['销售日期', '单品编码', '销量(千克)']].values:
        date = str(date)[:10] # get rid of the time
        if sv_cls_date.get(date) is None:
            # 0 : flower_leaf, 1 : flower_cauliflower, 2 : water_root, 3 : eggplant, 4 : pepper, 5 : mushroom
            sv_cls_date[date] = [0 for _ in range(len(CLS_NAME))]
        try:
            cls_name = cls_dict_code_clsname[code]
        except:
            continue
        sv_cls_date[date][CLS_NAME.index(cls_name)] += sales_volume

    # save sv_cls_date to a json file
    with open('./C/data/sv_cls_date.json', 'w') as f:
        json.dump(sv_cls_date, f)


# DONE
@clock(DEFAULT_FMT_TIME)
@functools.lru_cache()
def classify_data():

    if not os.path.exists('./C/data/cls'):
        os.mkdir('./C/data/cls')

    data1 = pd.read_excel('./C/extral1.xlsx')
    vegetable_class = {}
    for code, cls in zip(data1['单品编码'], data1['分类名称']):
        cls_en = CLS_NAME_EN[CLS_NAME.index(cls)]
        if vegetable_class.get(cls_en) is None:
            vegetable_class[cls_en] = []
        vegetable_class[cls_en].append(code)

    for cls, value in vegetable_class.items():
        with open('./C/data/cls/' + cls + '.txt', 'w') as f:
            for code in value:
                f.write(str(code) + '\n')

    with open('./C/data/cls/cls.json', 'w') as f:
        json.dump(vegetable_class, f)


# DONE
@clock(DEFAULT_FMT_TIME)
@functools.lru_cache()
def crejsonAimg_sv_cls_month():

    jsonpath = './C/data/sv_cls_date.json'
    if not os.path.exists(jsonpath):
        draw_msg_date()
    with open(jsonpath, 'r') as f:
        sv_cls_date = json.load(f)

    # create a dict to save the sales of each class of each month
    if not os.path.exists('./C/data/month'):
        os.mkdir('./C/data/month')
    if not os.path.exists('./C/img/month'):
        os.mkdir('./C/img/month')

    sv_cls_month = dict.fromkeys(CLS_NAME_EN)
    for cls in sv_cls_month.keys():
        sv_cls_month[cls] = []

    # draw the sales of each class of each month
    cur_year_month = None
    for date, sv_d in sv_cls_date.items():
        year_month = date[:7]

        if cur_year_month is None:
            cur_year_month = year_month
            plt.figure()
            plt.xlabel('day')
            plt.ylabel('sales volume')
            plt.title(year_month)

        if cur_year_month != year_month:
            # draw the figure and save it
            for cls, sv_m in sv_cls_month.items():
                plt.plot(range(1, len(sv_m) + 1), sv_m, label=cls)
            plt.legend()
            plt.savefig('./C/img/month/' + cur_year_month + '.png')
            plt.close()

            # save the sv_cls_month to a json file
            with open('./C/data/month/' + cur_year_month + '.json', 'w') as f:
                json.dump(sv_cls_month, f)

            # reset the sv_cls_month
            for cls in sv_cls_month.keys():
                sv_cls_month[cls] = []

            # create a new figure
            cur_year_month = year_month
            plt.figure()
            plt.xlabel('day')
            plt.ylabel('sv')
            plt.title(year_month)
        
        sv_cls_month['flower_leaf'].append(sv_d[0])
        sv_cls_month['flower_cauliflower'].append(sv_d[1])
        sv_cls_month['water_root'].append(sv_d[2])
        sv_cls_month['eggplant'].append(sv_d[3])
        sv_cls_month['pepper'].append(sv_d[4])
        sv_cls_month['mushroom'].append(sv_d[5])


    # draw the last figure and save it, and save the sv_cls_month to a json file
    for cls, sv_m in sv_cls_month.items():
        plt.plot(range(1, len(sv_m) + 1), sv_m, label=cls)
    plt.legend()
    plt.savefig('./C/img/month/' + cur_year_month + '.png')
    plt.close()

    with open('./C/data/month' + cur_year_month + '.json', 'w') as f:
        json.dump(sv_cls_month, f)

            
# DONE
@clock(DEFAULT_FMT_TIME)
@functools.lru_cache()
def creimg_sv_cls_week():

    jsonpath = './C/data/sv_cls_date.json'
    if not os.path.exists(jsonpath):
        draw_msg_date()
    with open(jsonpath, 'r') as f:
        sv_cls_date = json.load(f)

    if not os.path.exists('./C/img/week'):
        os.mkdir('./C/img/week')

    sv_cls_week = dict.fromkeys(CLS_NAME_EN)
    for cls in sv_cls_week.keys():
        sv_cls_week[cls] = []

    # each month draw a figure, each figure has 6 lines
    week_count = 0
    day = 2

    plt.figure()
    plt.xlabel('day')
    plt.ylabel('sales volume')
    plt.title('week' + str(week_count))

    for _, sv_d in sv_cls_date.items():
        if day % 7 == 0:
            week_count += 1
            for cls, sv_w in sv_cls_week.items():
                plt.plot(range(1, len(sv_w) + 1), sv_w, label=cls)
            for cls, sv_w in sv_cls_week.items():
                sv_cls_week[cls] = []
            plt.legend()
            plt.savefig('./C/img/week/' + str(week_count) + '.png')
            plt.close()

            plt.figure()
            plt.xlabel('day')
            plt.ylabel('sales volume')
            plt.title('week' + str(week_count))
        try: 
            sv_cls_week['flower_leaf'].append(sv_d[0])
            sv_cls_week['flower_cauliflower'].append(sv_d[1])
            sv_cls_week['water_root'].append(sv_d[2])
            sv_cls_week['eggplant'].append(sv_d[3])
            sv_cls_week['pepper'].append(sv_d[4])
            sv_cls_week['mushroom'].append(sv_d[5])
        except:
            pass
        day += 1

    for cls, sv_w in sv_cls_week.items():
        plt.plot(range(1, len(sv_w) + 1), sv_w, label=cls)
    plt.legend()
    plt.savefig('./C/img/week/' + str(week_count) + '.png')
    plt.close()


# DONE
@clock(DEFAULT_FMT_TIME)
@functools.lru_cache()
def crejsonAimg_sv_cls_year():

    jsonpath = './C/data/sv_cls_date.json'
    if not os.path.exists(jsonpath):
        draw_msg_date()
    with open(jsonpath, 'r') as f:
        sv_cls_date = json.load(f)

    if not os.path.exists('./C/data'):
        os.mkdir('./C/data')
    if not os.path.exists('./C/img'):
        os.mkdir('./C/img')

    sv_cls_year = dict.fromkeys(CLS_NAME_EN)
    for cls in sv_cls_year.keys():
        sv_cls_year[cls] = []

    day = 0
    plt.figure()
    flower_leaf_sv_week, flower_cauliflower_sv_week, water_root_sv_week, eggplant_sv_week, pepper_sv_week, mushroom_sv_week = 0, 0, 0, 0, 0, 0
    for _, sv_d in sv_cls_date.items():
        try:
            flower_leaf_sv_week += sv_d[0]
            flower_cauliflower_sv_week += sv_d[1]
            water_root_sv_week += sv_d[2]
            eggplant_sv_week += sv_d[3]
            pepper_sv_week += sv_d[4]
            mushroom_sv_week += sv_d[5]
        except:
            pass
        day += 1

        if day % 7 == 0:
            sv_cls_year['flower_leaf'].append(flower_leaf_sv_week)
            sv_cls_year['flower_cauliflower'].append(flower_cauliflower_sv_week)
            sv_cls_year['water_root'].append(water_root_sv_week)
            sv_cls_year['eggplant'].append(eggplant_sv_week)
            sv_cls_year['pepper'].append(pepper_sv_week)
            sv_cls_year['mushroom'].append(mushroom_sv_week)
            flower_leaf_sv_week, flower_cauliflower_sv_week, water_root_sv_week, eggplant_sv_week, pepper_sv_week, mushroom_sv_week = 0, 0, 0, 0, 0, 0

    with open('./C/data/sv_cls_year.json', 'w') as f:
        json.dump(sv_cls_year, f)

    for cls, sv_y in sv_cls_year.items():
        plt.plot(range(1, len(sv_y) + 1), sv_y, label=cls)
    plt.legend()
    plt.savefig('./C/img/' + 'year' + '.png')
    plt.close()
   
    
# DONE
@clock(DEFAULT_FMT_TIME)
@functools.lru_cache()
def crejsonAimgAtxt_goods_codeAsv():
    data1 = pd.read_excel('./C/extral1.xlsx')
    data2 = pd.read_excel('./C/extral2.xlsx')

    if not os.path.exists('./C/data'):
        os.mkdir('./C/data')
    if not os.path.exists('./C/img'):
        os.mkdir('./C/img')

    # from data1: load the item code colume and save as the key of dict
    goods = dict.fromkeys(data1['单品编码'])
    for key in goods.keys():
        goods[key] = 0
    for code, sv in zip(data2['单品编码'], data2['销量(千克)']):
        try:
            goods[code] += sv
        except:
            continue

    # save the dict to a json file
    with open('./C/data/goods_codeAsv.json', 'w') as f:
        json.dump(goods, f)

    # draw the sales of each item
    plt.figure()
    plt.xlabel('code')
    plt.ylabel('sales volume')
    plt.scatter(range(len(goods.keys())), goods.values(), s=1)
    plt.savefig('./C/img/goods_codeAsv.png')
    plt.close()

    # save the dict to a txt file
    with open('./C/data/goods_codeAsv.txt', 'w') as f:
        for code, sv in goods.items():
            f.write(str(code) + ' ' + str(sv) + '\n')


# DONE
@clock(DEFAULT_FMT_TIME)
@functools.lru_cache()
def count_corrcoef_month_ov06():

    if not os.path.exists('./C/data/corrcoef_clsAcls_month.txt'):
        corrcoef_clsAcls_month()
        return

    with open('./C/data/count_corrcoef_clsAcls_month_over06.txt', 'w') as f:
        count = {}
        with open('./C/data/corrcoef_clsAcls_month.txt', 'r') as f1:
            lines = f1.readlines()
        for line in lines:
            try:
                if float(line.split()[2]) > 0.6:
                    try:
                        count[line.split()[0]] += 1
                    except:
                        count[line.split()[0]] = 1
            except:
                continue
        for key, value in count.items(): 
            f.write(key + ' ' + str(value) + '\n')


# DONE
@clock(DEFAULT_FMT_TIME)
def changeAllExcel2Json():

    if not os.path.exists('./C/data'):
        os.mkdir('./C/data')

    if not os.path.exists('./C/data/data1.json'):
        data1 = pd.read_excel('./C/extral1.xlsx')
        data1_dist = {}
        for code, name, cls_code, cls_name in data1[['单品编码', '单品名称', '分类编码', '分类名称']].values:
            code = str(int(code))
            data1_dist[code] = (name, cls_code, cls_name)
        with open ('./C/data/data1.json', 'w') as f:
            json.dump(data1_dist, f)

    if not os.path.exists('./C/data/data2.json'):
        data2 = pd.read_excel('./C/extral2.xlsx')
        data2_dist = {}
        for date, code, sv, price, sell_type, discount in data2[['销售日期', '单品编码', '销量(千克)', '销售单价(元/千克)', '销售类型', '是否打折销售']].values:
            date = str(date)[:10]
            code = str(int(code))
            discount = True if discount == '是' else False
            if data2_dist.get(date) is None:
                data2_dist[date] = {}
            if data2_dist[date].get(code) is None:
                data2_dist[date][code] = []
            data2_dist[date][code].append((sv, price, sell_type, discount))
        with open ('./C/data/data2.json', 'w') as f:
            json.dump(data2_dist, f)

    if not os.path.exists('./C/data/data3.json'):
        data3 = pd.read_excel('./C/extral3.xlsx')
        data3_dist = {}
        for date, code, cost in data3[['日期', '单品编码', '批发价格(元/千克)']].values:
            date = str(date)[:10]
            code = str(int(code))
            if data3_dist.get(date) is None:
                data3_dist[date] = []
            data3_dist[date].append((code, cost))
        with open ('./C/data/data3.json', 'w') as f:
            json.dump(data3_dist, f)

    if not os.path.exists('./C/data/data4.json'):
        data4 = pd.read_excel('./C/extral4.xlsx')
        data4_dist = {}
        for code, name, loss in data4[['单品编码', '单品名称', '损耗率(%)']].values:
            code = str(int(code))
            data4_dist[code] = (name, loss)
        with open ('./C/data/data4.json', 'w') as f:
            json.dump(data4_dist, f)


# ABANDONED
def draw_data(file_name):
    # scatter plot
    code, sales = [], []
    with open('./C/' + file_name, 'r') as f:
        for line in f.readlines():
            try:
                code_one= line.split()[0]
                sales_one = float(line.split()[1])
            except:
                continue
            code.append(code_one)
            sales.append(sales_one)
            
    plt.figure()
    plt.xlabel('code')
    plt.ylabel('sales')
    plt.scatter(code, sales, s=1)
    plt.savefig('./C/img/' + file_name.split('.')[0] + '.png')
    plt.close()


# ABANDONED
@clock(DEFAULT_FMT_TIME)
@functools.lru_cache()
def linear_programming():
    if not os.path.exists('./C/data/cls2pridictOfProACos.json'):
        creimg_profit_cls()
    with open('./C/data/cls2pridictOfProACos.json', 'r') as f:
        cls2code2price = json.load(f)
    pridict_pur = predict_sv_sum_week(156)
    
    C = []
    for cls in CLS_NAME_EN:
        C.append(cls2code2price[cls]['profit'][0])
    C = np.array(C)

    AEQ = np.ones((1, len(C)))
    BEQ = np.array([pridict_pur])

    res = optimize.linprog(-C, A_eq=AEQ, b_eq=BEQ)
    return res.x, -res.fun
   

@clock(DEFAULT_FMT_TIME)
@functools.lru_cache()
def main():

    if not os.path.exists('./C/'):
        raise Exception('No such file or directory: ./C/')

    # find extral1.xlsx, extral2.xlsx, extral3.xlsx, extral4.xlsx in ./C/
    for i in range(1, 5):
        if not os.path.exists('./C/extral' + str(i) + '.xlsx'):
            raise Exception('No such file or directory: ./C/extral' + str(i) + '.xlsx')

    # changeAllExcel2Json()

    # draw_msg_date()
    # classify_data()
    # crejsonAimgAtxt_goods_codeAsv()

    # creimg_sv_cls_week()
    # crejsonAimg_sv_cls_month()
    # crejsonAimg_sv_cls_year()

    # corrcoef_clsAcls_month()
    # corrcoef_clsAcls_year()
    # corrcoef_goods()

    # creimg_svAprice()

    # sv_sum_everyWeek_linefitting()

    # print(predict_sv_sum_week(156))

    # creimg_profit_cls()

    # creJsonAImg_weekavg_cls2proAcos()

    # timeSequencePridict_WeekProACos()

    # linear_programming()

    # cal_proportion()

    # select_last7days()

    # grey_prediction_purchase_price()

    # grey_prediction_profit()

    # grey_prediction_sv()

    calculate_predict_data()

if __name__ == '__main__':
    main()