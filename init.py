
import os
import re
import sys
import signal
import math
import rsa
import time
import datetime
import json
import subprocess
import logging
import traceback
import fileinput
import itertools
import asyncio
import aiohttp
import requests
import urllib3
import urllib
import urllib.request
import hmac
import hashlib
import ssl
import pysos
import telebot
import async_timeout
import twisted.internet
from os import system, name
from sys import exc_info
from traceback import extract_tb
from colorama import init
from termcolor import cprint, colored
from threading import Thread, Lock
from binance.websockets import BinanceSocketManager
from binance.client import Client
from twisted.internet import reactor
from twisted.protocols.basic import LineReceiver
from twisted.internet.protocol import Factory
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
init()

def clear():
    try:
        if name == 'nt':
            os.system('cls')
        else:
            os.system('clear')
    except:
        pass

def delete_free_lines():
    check_line = 0
    if os.path.isfile('xbotUSDT.db'):
        for line in fileinput.input('xbotUSDT.db', inplace=True):
            if line[0] != '"' and check_line > 0:
                continue
            print(line.rstrip('\n'))
            check_line += 1

def get_count(number):
    str_number = str(number)
    if '.' not in str_number:
        return 0
    return len(number[number.index('.') + 1:])

def num_round(number):
    str_number = str(number)
    if '.0' in str_number:
        str_number = str_number.rstrip('0')
        str_number = str_number.rstrip('.')
    elif str_number.rstrip('0') and '.' in str_number:
        str_number = str_number.rstrip('0')
    return str_number

def info_rewrite(symbol, **data):
    try:
        rewrite = dict()
        for (key, value) in data.items():
            rewrite.update({str(key): str(value)})
        data_base[symbol] = rewrite
    except Exception as e:
        try:
            logging.error(str(extract_tb(exc_info()[2])[0][1]) + '\n' + str(e))
            cprint('|' + str(datetime.datetime.now().strftime('%H:%M:%S')) + '| ' + str(extract_tb(exc_info()[2])[0][1]) + colored('\x1b[K\n' + str(e), 'red'))
        except:
            logging.error(str(e))

def daily_profit(day, profit):
    try:
        daily_profit = data_base['daily_profit']
        if day not in data_base['daily_profit'].keys():
            daily_profit[day] = [profit]
        else:
            daily_profit[day].append(profit)
        data_base['daily_profit'] = daily_profit
    except Exception as e:
        try:
            logging.error(str(extract_tb(exc_info()[2])[0][1]) + '\n' + str(e))
            cprint('|' + str(datetime.datetime.now().strftime('%H:%M:%S')) + '| ' + str(extract_tb(exc_info()[2])[0][1]) + colored('\x1b[K\n' + str(e), 'red'))
        except:
            logging.error(str(e))

def canceled_order(_symbol, _orderId, _clientId, _side):
    try:
        client.cancel_order(symbol=_symbol, orderId=_orderId, newClientOrderId=_clientId)
    except Exception as e:
        if 'code' in e.__dict__:
            if str(e.__dict__['code']) == '-2011':
                try:
                    orders = client.get_open_orders()
                    for open_list in orders:
                        if open_list['symbol'] == _symbol and open_list['side'] == _side and open_list['clientOrderId'] == _clientId:
                            try:
                                client.cancel_order(symbol=_symbol, orderId=open_list['orderId'], newClientOrderId=_clientId)
                                break
                            except Exception as e:
                                try:
                                    logging.error(str(extract_tb(exc_info()[2])[0][1]) + ' ' + _symbol + ' ' + str(open_list['orderId']) + '\n' + str(e))
                                except:
                                    logging.error(str(e))
                except Exception as e:
                    try:
                        logging.error(str(extract_tb(exc_info()[2])[0][1]) + '\n' + str(e))
                        if str(e.__dict__['code']) == '-1003':
                            time.sleep(60)
                    except:
                        logging.error(str(e))
        else:
            cprint('|' + str(datetime.datetime.now().strftime('%H:%M:%S')) + '| ' + str(extract_tb(exc_info()[2])[0][1]) + _symbol + ' ' + _orderId + ' ' + _clientId + colored('\x1b[K\n' + str(e), 'red'))

def check_base():
    global min_balance, min_order, min_price, perc_down, sell_up, buy_down, max_trade_pairs, auto_trade_pairs, delta_percent, num_aver, step_aver, trailing_sell, trailing_percent, trailing_price, user_order, fiat_currencies
    try:
        sell_filled_orders = data_base['trade_info']['sell_filled_orders']
    except:
        sell_filled_orders = '0'
    try:
        sell_open_orders = data_base['trade_info']['sell_open_orders']
    except:
        sell_open_orders = '0'
    try:
        profit = data_base['trade_info']['profit']
    except:
        profit = '0'
    try:
        daily_volume = data_base['trade_info']['daily_volume']
    except:
        daily_volume = '0'
    data_base.__delitem__('trade_info')
    data_base['trade_info'] = {'sell_filled_orders': sell_filled_orders, 'sell_open_orders': sell_open_orders, 'profit': profit, 'daily_volume': daily_volume}
    try:
        min_balance = data_base['trade_params']['min_balance']
    except:
        min_balance = '0'
    try:
        min_order = data_base['trade_params']['min_order']
    except:
        min_order = '10'
    try:
        min_price = data_base['trade_params']['min_price']
    except:
        min_price = '0.05'
    try:
        perc_down = data_base['trade_params']['perc_down']
    except:
        perc_down = '-5'
    try:
        sell_up = data_base['trade_params']['sell_up']
    except:
        sell_up = '2.25'
    try:
        buy_down = data_base['trade_params']['buy_down']
    except:
        buy_down = '5'
    try:
        max_trade_pairs = data_base['trade_params']['max_trade_pairs']
    except:
        max_trade_pairs = '20'
    try:
        auto_trade_pairs = data_base['trade_params']['auto_trade_pairs']
    except:
        auto_trade_pairs = 'y'
    try:
        delta_percent = data_base['trade_params']['delta_percent']
    except:
        delta_percent = 'y'
    try:
        num_aver = data_base['trade_params']['num_aver']
    except:
        num_aver = 'y'
    try:
        step_aver = data_base['trade_params']['step_aver']
    except:
        step_aver = '1'
    try:
        trailing_sell = data_base['trade_params']['trailing_sell']
    except:
        trailing_sell = 'y'
    try:
        trailing_percent = data_base['trade_params']['trailing_percent']
    except:
        trailing_percent = '0.5'
    try:
        trailing_price = data_base['trade_params']['trailing_price']
    except:
        trailing_price = '0.25'
    try:
        user_order = data_base['trade_params']['user_order']
    except:
        user_order = 'y'
    try:
        fiat_currencies = data_base['trade_params']['fiat_currencies']
    except:
        fiat_currencies = ['USDTRUB']
    data_base.__delitem__('trade_params')
    data_base['trade_params'] = {'min_balance': min_balance, 'min_order': min_order, 'perc_down': perc_down, 'sell_up': sell_up, 'buy_down': buy_down, 'min_price': min_price, 'max_trade_pairs': max_trade_pairs, 'auto_trade_pairs': auto_trade_pairs, 'delta_percent': delta_percent, 'num_aver': num_aver, 'step_aver': step_aver, 'trailing_sell': trailing_sell, 'trailing_percent': trailing_percent, 'trailing_price': trailing_price, 'user_order': user_order, 'fiat_currencies': fiat_currencies}

class Menu:

    def continuity(self):
        clear()
        if 'trade_info' not in data_base.keys():
            Menu().trade_info()
        if 'api_key' not in data_base.keys():
            Menu().api_key()
        if 'trade_params' not in data_base.keys():
            Menu().trade_params()
        if 'white_list' not in data_base.keys():
            Menu().white_list()
        if 'trade_pairs' not in data_base.keys():
            Menu().trade_pairs()
        if 'trailing_orders' not in data_base.keys():
            Menu().trailing_orders()
        if 'daily_profit' not in data_base.keys():
            Menu().daily_profit()
        if isinstance(data_base['daily_profit'], dict) == False:
            data_base.__delitem__('daily_profit')
            Menu().continuity()
        if 'bnb_burn' not in data_base.keys():
            Menu().bnb_burn()
        check_base()

    def keys(self):
        global min_balance, min_order, min_price, perc_down, sell_up, buy_down, max_trade_pairs, auto_trade_pairs, delta_percent, num_aver, step_aver, trailing_sell, trailing_percent, trailing_price, user_order
        key = input('')
        if key == '-s':
            pass
        elif key == '-o':
            open_position = 0
            data_base_open_orders = sorted([pair for pair in data_base.items() if pair[0] not in system_key], key=lambda name: name)
            cprint('\x1b[H\x1b[J\x1b[K' + colored('    ', 'white', 'on_cyan', attrs=['bold']) + colored('\n |__', 'cyan') + colored(' -ext ', 'grey', 'on_cyan') + colored(' Выход в меню\n', 'cyan'))
            for pair in data_base_open_orders:
                if pair[1]['status'] == 'SELL_ORDER':
                    cprint(colored('SELL ', 'red') + 'LIMIT ' + colored('[' + pair[1]['allQuantity'] + ']', 'grey', 'on_white') + ' ' + colored(pair[0].replace('USDT', ''), 'magenta', attrs=['bold']) + ' for ' + colored(pair[1]['sellPrice'] + ' USDT\x1b[K', 'yellow'))
                    open_position += 1
                else:
                    if pair[1]['status'] == 'TRAILING_SELL_ORDER':
                        cprint(colored('SELL ', 'magenta') + 'TRAILING ' + colored('[' + pair[1]['allQuantity'] + ']', 'grey', 'on_white') + ' ' + colored(pair[0].replace('USDT', ''), 'magenta', attrs=['bold']) + ' for ' + colored(pair[1]['sellPrice'] + ' USDT\x1b[K', 'yellow'))
                        open_position += 1
                        cprint(colored('\nВсего позиций: ', 'cyan') + colored(str(open_position), 'yellow') + '\n')
                        key_pair = input('')
                        if key_pair == '-ext':
                            break
                        Menu().print_menu()
                    cprint(colored('SELL ', 'magenta') + 'TRAILING ' + colored('[' + pair[1]['allQuantity'] + ']', 'grey', 'on_white') + ' ' + colored(pair[0].replace('USDT', ''), 'magenta', attrs=['bold']) + ' for ' + colored(pair[1]['sellPrice'] + ' USDT\x1b[K', 'yellow'))
                    open_position += 1
            cprint(colored('\nВсего позиций: ', 'cyan') + colored(str(open_position), 'yellow') + '\n')
            key_pair = input('')
            if key_pair == '-ext':
                break
            Menu().print_menu()
        elif key == '-m':
            while key_pair == '-all' and len(data_base['trade_pairs']) != 0:
                cprint('\x1b[A\x1b[K\x1b[A')
                cprint(colored('Вы уверены, что хотите добавить все пары к USDT на бирже в разрешённый для торговли список? [y/n]:\x1b[K', 'cyan'))
                while pair == 'y':
                    cprint('\x1b[A\x1b[K\x1b[A\x1b[K\x1b[A')
                    try:
                        all_white_pairs = data_base['trade_pairs']
                        for name_pair in all_white_pairs:
                            if name_pair not in white_list:
                                white_list.append(name_pair)
                        data_base['white_list'] = white_list
                        break
                    except:
                        try:
                            logging.error(str(extract_tb(exc_info()[2])[0][1]) + '\n' + str(e))
                            cprint('|' + str(datetime.datetime.now().strftime('%H:%M:%S')) + '| ' + str(extract_tb(exc_info()[2])[0][1]) + colored('\x1b[K\n' + str(e), 'red'))
                        except:
                            logging.error(str(e))
            else:
                data_base['white_list'] = new_white_list
                break
            Menu().print_menu()
        elif key == '-k':
            while input_param == '-edt':
                pass
        elif key == '-p':
            while input_param == '-edt':
                pass
            else:
                data_base.__delitem__('trade_params')
                data_base['trade_params'] = {'min_balance': min_balance, 'min_order': min_order, 'min_price': min_price, 'perc_down': perc_down, 'sell_up': sell_up, 'buy_down': buy_down, 'max_trade_pairs': max_trade_pairs, 'auto_trade_pairs': auto_trade_pairs, 'delta_percent': delta_percent, 'num_aver': num_aver, 'step_aver': step_aver, 'trailing_sell': trailing_sell, 'trailing_percent': trailing_percent, 'trailing_price': trailing_price, 'user_order': user_order, 'fiat_currencies': fiat_currencies}
                break
        elif key == '-h':
            while True:
                cprint('\x1b[H\x1b[J\x1b[K' + colored('Вы уверены, что хотите удалить торговые данные бота по всем открытым ордерам? [y/n]', 'cyan'))
                del_trade = input('')
                if del_trade == 'y':
                    for line in data_base.items():
                        if line[0] not in system_key:
                            data_base.__delitem__(line[0])
                    trade_info = data_base['trade_info']
                    data_base.__delitem__('trade_info')
                    data_base['trade_info'] = {'sell_filled_orders': trade_info['sell_filled_orders'], 'sell_open_orders': '0', 'profit': trade_info['profit'], 'daily_volume': '0'}
                    Menu().print_menu()
                    break
                elif del_trade == 'n':
                    Menu().print_menu()
                    break
                else:
                    print('\x1b[A\x1b[K\x1b[H')
        elif key == '-i':
            while True:
                cprint('\x1b[H\x1b[J\x1b[K' + colored('Вы уверены, что хотите удалить статистику о прибыли и исполненных ордерах? [y/n]', 'cyan'))
                del_trade = input('')
                if del_trade == 'y':
                    trade_info = data_base['trade_info']
                    data_base.__delitem__('trade_info')
                    data_base['trade_info'] = {'sell_filled_orders': '0', 'sell_open_orders': trade_info['sell_open_orders'], 'profit': '0', 'daily_volume': '0'}
                    Menu().print_menu()
                    break
                elif del_trade == 'n':
                    Menu().print_menu()
                    break
                else:
                    print('\x1b[A\x1b[K\x1b[H')
        else:
            print('\x1b[A\x1b[K\x1b[A')
            Menu().keys()

    def print_menu(self):
        Menu().continuity()
        clear()
        cprint(colored("""
  *       *          * * *       * * *   * * * * *
    *   *            * """, 'cyan') + colored('*', 'green') + colored("""  *     *     *      *    
      *      * * *   * * * *   *   """, 'cyan') + colored('*', 'red') + colored("""   *     *    
    *   *            * """, 'cyan') + colored('* *', 'green') + colored("""  *   *     *      *    
  *       *          * * * *     * * *       *

""", 'cyan') + colored('Версия: ', 'cyan') + colored(version_bot, color_version) + new_version + colored('\nGitHub: ', 'cyan') + colored('github.com/xbot-dex/xbot', 'magenta', attrs=['bold']) + colored('\nTelegram: ', 'cyan') + colored('t.me/xbot_dex', 'magenta', attrs=['bold']) + colored("""
Реферальный ID разработчика: """, 'cyan') + colored('EU9YDDIX', 'magenta', attrs=['bold']))
        max_orders = 'без ограничений' if float(data_base['trade_params']['max_trade_pairs']) == -1 else 'до ' + data_base['trade_params']['max_trade_pairs']
        max_orders = 'только усреднение открытых' if float(data_base['trade_params']['max_trade_pairs']) == 0 else max_orders
        cprint(colored('\nОбщая прибыль: ', 'cyan') + colored(data_base['trade_info']['profit'] + ' USDT', 'yellow') + colored('\nУспешных сделок: ', 'cyan') + colored(int(float(data_base['trade_info']['sell_filled_orders'])), 'yellow') + colored("""
Ордеров на продажу: """, 'cyan') + colored(int(float(data_base['trade_info']['sell_open_orders'])), 'yellow') + colored("""
Ограничение позиций: """, 'cyan') + colored(max_orders, 'yellow') + colored('\n\n    ', 'white', 'on_white', attrs=['bold']) + colored(' Главное меню', 'white') + colored('\n |__', 'white', attrs=['bold']) + colored(' -s ', 'grey', 'on_green') + colored(' Запустить X-Bot', 'green') + colored('\n |__', 'white', attrs=['bold']) + colored(' -o ', 'grey', 'on_cyan') + colored(' Посмотреть открытые позиции', 'cyan') + colored('\n |__', 'white', attrs=['bold']) + colored(' -m ', 'grey', 'on_cyan') + colored(' Изменить список монет', 'cyan') + colored('\n |__', 'white', attrs=['bold']) + colored(' -k ', 'grey', 'on_yellow') + colored(' Изменить API и Telegram настройки', 'yellow') + colored('\n |__', 'white', attrs=['bold']) + colored(' -p ', 'grey', 'on_yellow') + colored(' Изменить торговые параметры бота', 'yellow') + colored('\n |__', 'white', attrs=['bold']) + colored(' -h ', 'grey', 'on_red') + colored(' Удалить информацию об ордерах', 'red') + colored('\n |__', 'white', attrs=['bold']) + colored(' -i ', 'grey', 'on_red') + colored(' Удалить торговую статистику', 'red') + '\n')
        Menu().keys()

    def trade_info(self):
        data_base['trade_info'] = {'sell_filled_orders': '0', 'sell_open_orders': '0', 'profit': '0', 'daily_volume': '0'}

    def api_key(self):
        cprint('\x1b[H\x1b[J\x1b[K' + colored('Введите API ключ от Binance:\x1b[K', 'cyan'))
        key = input('')
        cprint('\x1b[H\x1b[J\x1b[K' + colored('Введите Secret ключ от Binance:\x1b[K', 'cyan'))
        secret = input('')
        cprint('\x1b[H\x1b[J\x1b[K' + colored('Введите Ваш ID пользователя на Binance (состоит только из цифр):\x1b[K', 'cyan'))
        while True:
            try:
                referal = str(abs(int(input(''))))
                break
            except:
                print('\x1b[A\x1b[K\x1b[H')
        print('\x1b[H\x1b[J\x1b[K')
        data_base['api_key'] = {'api': key, 'secret': secret, 'referal': referal, 'tg_notification': 'n', 'tg_token': '0:A-s', 'tg_name': '@'}

    def trade_params(self):
        data_base['trade_params'] = {}

    def white_list(self):
        safe_trade_pairs = ['ADAUSDT', 'ADXUSDT', 'AGIUSDT', 'AIONUSDT', 'ALGOUSDT', 'AMBUSDT', 'ARDRUSDT', 'ARKUSDT', 'ARPAUSDT', 'ASTUSDT', 'ATOMUSDT', 'BATUSDT', 'BCHUSDT', 'BLZUSDT', 'BNTUSDT', 'CHRUSDT', 'COTIUSDT', 'CVCUSDT', 'DASHUSDT', 'DATAUSDT', 'DCRUSDT', 'DOCKUSDT', 'DUSKUSDT', 'ELFUSDT', 'ENJUSDT', 'EOSUSDT', 'ETCUSDT', 'ETHUSDT', 'GASUSDT', 'GXSUSDT', 'ICXUSDT', 'IOTAUSDT', 'IRISUSDT', 'KMDUSDT', 'KNCUSDT', 'LINKUSDT', 'LOOMUSDT', 'LRCUSDT', 'LSKUSDT', 'LTCUSDT', 'LTOUSDT', 'MANAUSDT', 'MKRUSDT', 'MTLUSDT', 'NANOUSDT', 'NASUSDT', 'NEOUSDT', 'NULSUSDT', 'OAXUSDT', 'OGNUSDT', 'OMGUSDT', 'ONTUSDT', 'PERLUSDT', 'POAUSDT', 'POLYUSDT', 'QLCUSDT', 'QSPUSDT', 'QTUMUSDT', 'RCNUSDT', 'RDNUSDT', 'RENUSDT', 'REPUSDT', 'REQUSDT', 'RLCUSDT', 'RVNUSDT', 'SNTUSDT', 'STEEMUSDT', 'STORJUSDT', 'SXPUSDT', 'THETAUSDT', 'TOMOUSDT', 'VETUSDT', 'VIAUSDT', 'VIBUSDT', 'WANUSDT', 'WAVESUSDT', 'WRXUSDT', 'WTCUSDT', 'XEMUSDT', 'XLMUSDT', 'XMRUSDT', 'XTZUSDT', 'XZCUSDT', 'ZECUSDT', 'ZENUSDT', 'ZILUSDT', 'ZRXUSDT']
        data_base['white_list'] = safe_trade_pairs

    def trade_pairs(self):
        data_base['trade_pairs'] = []

    def trailing_orders(self):
        data_base['trailing_orders'] = dict()

    def daily_profit(self):
        data_base['daily_profit'] = dict()

    def bnb_burn(self):
        data_base['bnb_burn'] = dict()

if __name__ == '__main__':
    mutex = Lock()
    version_bot = '0.19'
    logging.basicConfig(level=logging.WARNING, filename='xbot' + str(int(time.time())) + '.log', format='%(asctime)s %(levelname)s:%(message)s')
    try:
        response = requests.get('https://api.github.com/repos/xbot-dex/xbot/releases/latest')
        last_version_bot = response.json()['tag_name']
        if float(last_version_bot) > float(version_bot):
            new_version = colored("""
Доступна новая версия: """, 'cyan') + colored(last_version_bot, 'green')
        else:
            new_version = ''
    except Exception as e:
        try:
            logging.error(str(extract_tb(exc_info()[2])[0][1]) + ' ' + str(e))
            cprint('|' + str(datetime.datetime.now().strftime('%H:%M:%S')) + '| ' + colored(str(extract_tb(exc_info()[2])[0][1]) + ' ' + str(e), 'red'))
        except:
            logging.error(str(e))
    color_version = 'green' if float(last_version_bot) <= float(version_bot) else 'red'
    try:
        delete_free_lines()
        data_base = pysos.Dict('xbotUSDT.db')
        open_orders = []
        all_pairs = []
        black_asset = ['UP', 'DOWN', 'BULL', 'BEAR']
        system_key = ['trade_info', 'api_key', 'trade_params', 'white_list', 'trade_pairs', 'trailing_orders', 'daily_profit', 'bnb_burn']
        usdt_balance = '0'
        bnb_balance = '0'
        reconnect = 1
        Menu().print_menu()
        c_api = data_base.__getitem__('api_key')['api']
        c_secret = data_base.__getitem__('api_key')['secret']
        referal = data_base.__getitem__('api_key')['referal']
        tg_notification = data_base.__getitem__('api_key')['tg_notification']
        if tg_notification == 'y':
            try:
                tg_token = data_base.__getitem__('api_key')['tg_token']
                tg_name = data_base.__getitem__('api_key')['tg_name']
                bot = telebot.TeleBot(str(tg_token))
            except Exception as push_tg_error:
                try:
                    logging.error(str(extract_tb(exc_info()[2])[0][1]) + ' ' + str(push_tg_error))
                    cprint(push_tg_error, 'red')
                except:
                    logging.error(str(e))
        min_balance = str(data_base.__getitem__('trade_params')['min_balance'])
        min_order = str(data_base.__getitem__('trade_params')['min_order'])
        min_price = str(data_base.__getitem__('trade_params')['min_price'])
        perc_down = str(data_base.__getitem__('trade_params')['perc_down'])
        sell_up = str(data_base.__getitem__('trade_params')['sell_up'])
        buy_down = str(data_base.__getitem__('trade_params')['buy_down'])
        delta_percent = str(data_base.__getitem__('trade_params')['delta_percent'])
        max_trade_pairs = str(data_base.__getitem__('trade_params')['max_trade_pairs'])
        auto_trade_pairs = str(data_base.__getitem__('trade_params')['auto_trade_pairs'])
        step_aver = str(data_base.__getitem__('trade_params')['step_aver'])
        trailing_sell = str(data_base.__getitem__('trade_params')['trailing_sell'])
        trailing_percent = str(data_base.__getitem__('trade_params')['trailing_percent'])
        trailing_price = str(data_base.__getitem__('trade_params')['trailing_price'])
        user_order = str(data_base.__getitem__('trade_params')['user_order'])
        fiat_currencies = data_base.__getitem__('trade_params')['fiat_currencies']
        spinner_delta = 0
        timer_tg = 0
        timer_update = 0
        check_tg = 0
        time_ = time.time()
        start_time = _timestamp = time.time()
        license_accept = True
        trade_order = False
        filter_trade_pairs_error = True
    except Exception as e:
        try:
            logging.error(str(extract_tb(exc_info()[2])[0][1]) + ' ' + str(e))
            cprint(str(extract_tb(exc_info()[2])[0][1]) + ' ' + str(e), 'red')
        except:
            logging.error(str(e))

def signal_handler(sig, frame):
    data_base.close()
    sys.exit()

def data_base_update():
    global data_base
    data_base.close()
    delete_free_lines()
    data_base = pysos.Dict('xbotUSDT.db')

def check_keys(_symbol, _list):
    key_found = True
    keys_list = {'stepSize': 1, 'tickSize': 1, 'minNotional': 10, 'priceChangePercent': 0, 'askPrice': 0, 'averagePrice': 0, 'buyPrice': 0, 'sellPrice': 0, 'trailingPrice': 0, 'allQuantity': 0, 'free': 0, 'idOrder': 0, 'profit': 0, 'totalUSDT': 0, 'numAverage': 0, 'status': 'NO_ORDER'}
    for all_key in keys_list:
        if all_key not in _list:
            key_found = False
            if all_key == 'trailingPrice':
                try:
                    _list.update(trailingPrice=_list['averagePrice'])
                except Exception as e:
                    logging.error('def check_keys(_list) ' + str(e))
                else:
                    keys_list[all_key] = _list[all_key]
        else:
            keys_list[all_key] = _list[all_key]
    if key_found == False:
        data_base.__delitem__(_symbol)
        data_base[_symbol] = keys_list

def send_telegram(tg_symbol, tg_all_quantity, tg_average_price, tg_sell_price, tg_perc, tg_profit, **trailing_message):
    global check_tg
    try:
        if check_tg <= 3:
            for pair in data_base.items():
                if tg_symbol in data_base['trailing_orders'] and pair[0] not in system_key and pair[0] == tg_symbol:
                    tab = sorted([tab for tab in trailing_message['trailing_message'][tg_symbol]], key=lambda tab: len(tab['p']), reverse=True)
                    all_quantity = 0
                    average_sell_price = 0
                    price_words = '   Цена '
                    len_slash = len(price_words) if len(price_words) >= len(tab[0]['p']) else len(tab[0]['p'])
                    total_orders = 'Всего ордеров: ' + str(len(trailing_message['trailing_message'][tg_symbol])) + '\n' + price_words + ' '*(len_slash - len(price_words) + 4) + '| Объём'
                    for sales in trailing_message['trailing_message'][tg_symbol]:
                        average_sell_price += float(sales['p'])*float(sales['q'])
                        all_quantity += float(sales['q'])
                        total_orders = total_orders + '\n   ' + sales['p'] + ' '*(len_slash - len(sales['p']) + 1) + '| ' + sales['q']
                    average_sell_price = num_round(('{:.' + str(get_count(pair[1]['tickSize'])) + 'f}').format(average_sell_price/all_quantity))
                    all_quantity = num_round(('{:.' + str(get_count(pair[1]['stepSize'])) + 'f}').format(all_quantity))
                    total_orders = '📈 Средняя цена продажи: ' + num_round(('{:.' + str(get_count(pair[1]['tickSize'])) + 'f}').format(float(average_sell_price))) + '\n📊 ' + total_orders
                    tg_all_quantity = num_round(('{:.' + str(get_count(pair[1]['stepSize'])) + 'f}').format(float(all_quantity)))
                    tg_perc = num_round('{:.2f}'.format(float(average_sell_price)/float(tg_average_price)*100 - 100))
                    tg_profit = num_round('{:.8f}'.format(float(average_sell_price)*float(all_quantity) - float(tg_average_price)*float(all_quantity)))
                    text = """<code>📝 {}
📉 Средняя цена покупки: {}
{}
💵 Общий объём: {}
💎 Прибыль: {}% ({})</code>""".format(tg_symbol, num_round(tg_average_price), total_orders, tg_all_quantity, tg_perc, tg_profit)
                    break
                elif tg_symbol not in data_base['trailing_orders'] and pair[0] not in system_key and pair[0] == tg_symbol:
                    text = """<code>📝 {}
📉 Средняя цена покупки: {}
📈 Цена продажи: {}
💵 Объём: {}
💎 Прибыль: {}% ({})</code>""".format(tg_symbol, num_round(tg_average_price), num_round(tg_sell_price), num_round(tg_all_quantity), tg_perc, tg_profit)
                    break
            bot.send_message(chat_id=tg_name, text=text, parse_mode='HTML')
            logging.warning('Final result: ' + str(tg_all_quantity) + ' ' + str(tg_average_price) + ' ' + str(tg_sell_price) + ' ' + str(tg_perc) + ' ' + str(tg_profit))
    except Exception as e:
        logging.error('Error telegram bot.send_message: ' + str(e))
        check_tg += 1
        send_telegram(tg_symbol, tg_all_quantity, tg_average_price, tg_sell_price, tg_perc, tg_profit, trailing_message=trailing_message)
    check_tg = 0

def all_trade_pairs():
    try:
        for pairs in exchange:
            if pairs['quoteAsset'] == 'USDT' and False not in [False for x in black_asset if x in pairs['baseAsset']] and pairs['status'] == 'TRADING':
                all_pairs.append(pairs['symbol'])
        all_pairs.sort()
        return all_pairs
    except Exception as e:
        try:
            logging.error(str(extract_tb(exc_info()[2])[0][1]) + '\n' + str(e))
            cprint('|' + str(datetime.datetime.now().strftime('%H:%M:%S')) + '| ' + str(extract_tb(exc_info()[2])[0][1]) + colored('\x1b[K\n' + str(e), 'red'))
        except:
            logging.error(str(e))
        return data_base['trade_pairs']

def filter_trade_pairs():
    global usdt_balance, bnb_balance, filter_trade_pairs_error
    offline_trade = 0
    signal.signal(signal.SIGINT, signal_handler)
    data_base['trade_pairs'] = all_trade_pairs()
    try:
        cprint('|' + str(datetime.datetime.now().strftime('%H:%M:%S')) + '| ' + colored('X-Bot запускается, пожалуйста, подождите\x1b[K', 'cyan'))
        for bal in balances:
            if bal['asset'] == 'USDT':
                usdt_balance = '{:.8f}'.format(float(bal['free']))
            if bal['asset'] == 'BNB':
                bnb_balance = '{:.8f}'.format(float(bal['free']))
                if float(bnb_balance) < 0.1:
                    for pair in tickers:
                        if pair['symbol'] == 'BNBUSDT':
                            for step in exchange:
                                if step['symbol'] == pair['symbol']:
                                    while float(bnb_balance) < 0.1:
                                        try:
                                            q = ('{:.' + str(get_count(num_round(step['filters'][2]['stepSize']))) + 'f}').format(float(num_round(step['filters'][3]['minNotional']))/float(pair['askPrice']))
                                            while float(q)*float(pair['askPrice']) <= float(step['filters'][3]['minNotional']):
                                                q = ('{:.' + str(get_count(num_round(step['filters'][2]['stepSize']))) + 'f}').format(float(q) + float(step['filters'][2]['stepSize']))
                                            client.order_market_buy(symbol='BNBUSDT', quantity=q)
                                            bnb_balance = '{:.8f}'.format(float(bnb_balance) + float(q))
                                            break
                                        except Exception as e:
                                            try:
                                                logging.error(str(extract_tb(exc_info()[2])[0][1]) + 'Ошибка при покупке BNB: ' + q + '\n' + str(e))
                                                cprint('|' + str(datetime.datetime.now().strftime('%H:%M:%S')) + '| ' + str(extract_tb(exc_info()[2])[0][1]) + colored('Ошибка при покупке BNB: ' + q, 'cyan') + '\n' + colored(str(e), 'red'))
                                            except:
                                                logging.error(str(e))
        num_open_orders = 0
        for open_list in orders:
            try:
                if (open_list['symbol'] in data_base['white_list'] or open_list['symbol'] in data_base.keys()) and ('xbot_' in open_list['clientOrderId'] or open_list['symbol'] in data_base.keys()) and data_base[open_list['symbol']]['status'] == 'USER_BUY_ORDER':
                    open_orders.append(open_list['symbol'])
                    num_open_orders += 1
            except Exception as e:
                try:
                    logging.error(str(extract_tb(exc_info()[2])[0][1]) + '\n' + str(e))
                    cprint('|' + str(datetime.datetime.now().strftime('%H:%M:%S')) + '| ' + str(extract_tb(exc_info()[2])[0][1]) + colored('\x1b[K\n' + str(e), 'red'))
                except:
                    logging.error(str(e))
        info_rewrite('trade_info', sell_filled_orders=data_base['trade_info']['sell_filled_orders'], sell_open_orders=num_open_orders, profit=data_base['trade_info']['profit'], daily_volume=data_base['trade_info']['daily_volume'])
        work_pairs = list()
        for trade_pair in exchange:
            work_pairs.append(trade_pair['symbol'])
        db_update = dict()
        for lines in data_base.items():
            db_update[lines[0]] = lines[1]
        data_base_update()
        for its in db_update:
            data_base[its] = db_update.get(its)
        data_base_update()
        check_pairs = 0
        all_items_db = 0
        for item in data_base.keys():
            all_items_db += 1 if item not in system_key else 0
        delele_pairs = []
        for key in data_base.items():
            if key[0] not in system_key and key[0] not in data_base['white_list'] and key[1]['status'] == 'NO_ORDER':
                delele_pairs.append(key[0])
        for delete_coin in delele_pairs:
            data_base.__delitem__(delete_coin)
        for symbol in data_base['white_list']:
            if symbol not in data_base.keys():
                check_pairs += 1
                for pair in tickers:
                    if pair['symbol'] == symbol:
                        for step in exchange:
                            if step['symbol'] == pair['symbol'] and float(pair['askPrice']) != 0:
                                data_base[pair['symbol']] = {'stepSize': num_round(step['filters'][2]['stepSize']), 'tickSize': num_round(step['filters'][0]['tickSize']), 'minNotional': num_round(step['filters'][3]['minNotional']), 'priceChangePercent': pair['priceChangePercent'], 'askPrice': num_round(pair['askPrice']), 'averagePrice': '0', 'trailingPrice': '0', 'buyPrice': '0', 'sellPrice': '0', 'allQuantity': '0', 'free': '0', 'idOrder': '0', 'profit': '0', 'totalUSDT': '0', 'numAverage': '0', 'status': 'NO_ORDER'}
            else:
                check_pairs += 1
                for pair in data_base.items():
                    if pair[0] not in system_key:
                        check_keys(pair[0], pair[1])
                        if pair[0] not in data_base['white_list'] and pair[1]['status'] == 'NO_ORDER' or float(pair[1]['askPrice']) == 0 and symbol == pair[0]:
                            try:
                                data_base.__delitem__(pair[0])
                                if pair[0] in data_base['trailing_orders'].keys():
                                    trailing_orders = data_base['trailing_orders']
                                    trailing_orders.pop(pair[0])
                                    data_base['trailing_orders'] = trailing_orders
                            except Exception as e:
                                try:
                                    logging.error(str(extract_tb(exc_info()[2])[0][1]) + '\n' + str(e))
                                    cprint('|' + str(datetime.datetime.now().strftime('%H:%M:%S')) + '| ' + str(extract_tb(exc_info()[2])[0][1]) + colored('\x1b[K\n' + str(e), 'red'))
                                except:
                                    logging.error(str(e))
                            break
                        if pair[0] in data_base['white_list'] and pair[0] not in work_pairs and 'USDT' in pair[0]:
                            try:
                                white_list = data_base['white_list']
                                white_list.remove(pair[0])
                                data_base['white_list'] = white_list
                            except Exception as e:
                                try:
                                    logging.error(str(extract_tb(exc_info()[2])[0][1]) + '\n' + str(e))
                                    cprint('|' + str(datetime.datetime.now().strftime('%H:%M:%S')) + '| ' + str(extract_tb(exc_info()[2])[0][1]) + colored('\x1b[K\n' + str(e), 'red'))
                                except:
                                    logging.error(str(e))
                            break
                        if (pair[1]['status'] == 'NO_ORDER' or (pair[1]['averagePrice'] == 0 or pair[1]['buyPrice'] == 0) or pair[1]['sellPrice'] == 0) and pair[0] in open_orders:
                            try:
                                logging.warning('Предстартовый пересчёт ошибочных данных по ' + pair[0] + ': ' + pair[1]['status'])
                                for coin in orders:
                                    if 'xbot_' in coin['clientOrderId'] and coin['symbol'] == pair[0] and coin['side'] == 'SELL':
                                        last_orders = client.get_all_orders(symbol=pair[0])
                                        last_order = sorted([pair for pair in last_orders], key=lambda pair: pair['orderId'], reverse=True)
                                        new_average_buy_price = 0
                                        new_all_quantity = 0
                                        first_order = 0
                                        totalUSDT = '0'
                                        num_average = '0'
                                        first_buy = True
                                        for buy_order in last_order:
                                            if buy_order['side'] == 'BUY' and buy_order['status'] == 'FILLED' and 'xbot_' in buy_order['clientOrderId'] and first_buy == True:
                                                buy_price = buy_order['price']
                                                totalUSDT = '{:.8f}'.format(float(totalUSDT) + float(buy_order['cummulativeQuoteQty']))
                                                all_quantity = num_round(buy_order['origQty'])
                                                num_average = '{:.2f}'.format(float(num_average) + float(step_aver))
                                                first_buy = False
                                                first_order += 1
                                            elif buy_order['side'] == 'BUY' and buy_order['status'] == 'FILLED' and 'xbot_' in buy_order['clientOrderId'] and first_buy == False:
                                                new_average_buy_price += float(buy_price)*float(all_quantity) + float(buy_order['price'])*float(buy_order['origQty']) if first_order == 1 else float(buy_order['price'])*float(buy_order['origQty'])
                                                new_all_quantity += float(all_quantity) + float(buy_order['origQty']) if first_order == 1 else float(buy_order['origQty'])
                                                totalUSDT = '{:.8f}'.format(float(totalUSDT) + float(buy_order['cummulativeQuoteQty']))
                                                num_average = '{:.2f}'.format(float(num_average) + float(step_aver))
                                                first_order += 1
                                            elif buy_order['side'] == 'SELL' and buy_order['status'] == 'FILLED' and 'xbot_' in buy_order['clientOrderId'] and first_buy == False:
                                                break
                                        average_buy_price = ('{:.' + str(get_count(pair[1]['tickSize'])) + 'f}').format(new_average_buy_price/new_all_quantity) if new_average_buy_price != 0 and new_all_quantity != 0 else buy_price
                                        logging.warning(str(average_buy_price) + ' ' + str(coin['origQty']) + ' ' + str(totalUSDT) + ' ' + str(num_average))
                                        info_rewrite(pair[0], stepSize=pair[1]['stepSize'], tickSize=pair[1]['tickSize'], minNotional=pair[1]['minNotional'], priceChangePercent=pair[1]['priceChangePercent'], askPrice=pair[1]['askPrice'], averagePrice=num_round(average_buy_price), buyPrice=num_round(buy_price), sellPrice=num_round(coin['price']), trailingPrice=pair[1]['trailingPrice'], allQuantity=num_round(coin['origQty']), free=pair[1]['free'], idOrder=coin['orderId'], profit=pair[1]['profit'], totalUSDT=num_round(totalUSDT), numAverage=num_round(num_average), status='SELL_ORDER')
                                        break
                            except Exception as e:
                                try:
                                    logging.error(str(extract_tb(exc_info()[2])[0][1]) + '\n' + str(e))
                                except:
                                    logging.error(str(e))
                        if pair[1]['status'] == 'ERROR_ORDER' and pair[0] not in open_orders:
                            info_rewrite(pair[0], stepSize=pair[1]['stepSize'], tickSize=pair[1]['tickSize'], minNotional=pair[1]['minNotional'], priceChangePercent=pair[1]['priceChangePercent'], askPrice=0, averagePrice=0, buyPrice=0, sellPrice=0, trailingPrice=0, allQuantity=0, free=0, idOrder=0, profit=pair[1]['profit'], totalUSDT=0, numAverage=0, status='NO_ORDER')
                            break
                        if (pair[1]['status'] == 'SELL_ORDER' or pair[1]['status'] == 'TRAILING_SELL_ORDER') and pair[0] not in open_orders:
                            coin = pair[0].replace('USDT', '')
                            free_coin = True
                            if pair[1]['status'] == 'TRAILING_SELL_ORDER':
                                for bal in balances:
                                    if bal['asset'] == coin and float(bal['free']) >= float(pair[1]['allQuantity']):
                                        free_coin = False
                                        break
                            if free_coin == True:
                                offline_trade += 1
                                if offline_trade == 1:
                                    cprint('|OFF-LINE| ' + colored('Исполнено во время бездействия:\x1b[K', 'cyan'))
                                profit = '{:.8f}'.format(float(pair[1]['sellPrice'])*float(pair[1]['allQuantity']) - float(pair[1]['totalUSDT']))
                                daily_profit(str(datetime.date.today()), profit)
                                info_rewrite('trade_info', sell_filled_orders=float(data_base['trade_info']['sell_filled_orders']) + 1, sell_open_orders=float(data_base['trade_info']['sell_open_orders']) - 1, profit='{:.8f}'.format(float(data_base['trade_info']['profit']) + float(profit)), daily_volume='{:.8f}'.format(float(data_base['trade_info']['daily_volume']) + float(pair[1]['sellPrice'])*float(pair[1]['allQuantity'])))
                                perc_profit = '{:.2f}'.format(100 - float(pair[1]['averagePrice'])/float(pair[1]['sellPrice'])*100) if float(pair[1]['sellPrice']) != 0 else 0
                                if pair[1]['status'] == 'TRAILING_SELL_ORDER' and pair[0] in data_base['trailing_orders'].keys():
                                    trailing_orders = data_base['trailing_orders']
                                    trailing_orders[pair[0]].append([{'p': pair[1]['sellPrice'], 'q': pair[1]['allQuantity']}][0])
                                else:
                                    trailing_orders = dict()
                                if data_base['api_key']['tg_notification'] == 'y':
                                    send_telegram(pair[0], pair[1]['allQuantity'], pair[1]['averagePrice'], pair[1]['sellPrice'], perc_profit, profit, trailing_message=trailing_orders)
                                cprint('|OFF-LINE| ' + colored('SELL ', 'red') + '(FILLED): ' + colored('[' + pair[1]['allQuantity'] + ']', 'grey', 'on_white') + ' ' + colored(coin, 'magenta', attrs=['bold']) + ' for ' + colored(pair[1]['sellPrice'] + ' USDT\x1b[K', 'yellow'))
                                info_rewrite(pair[0], stepSize=pair[1]['stepSize'], tickSize=pair[1]['tickSize'], minNotional=pair[1]['minNotional'], priceChangePercent=pair[1]['priceChangePercent'], askPrice=0, averagePrice=0, buyPrice=0, sellPrice=0, trailingPrice=0, allQuantity=0, free=0, idOrder=0, profit=num_round('{:.8f}'.format(float(pair[1]['profit']) + float(profit))), totalUSDT=0, numAverage=0, status='NO_ORDER')
                                break
                        if (pair[1]['status'] == 'BUY_ORDER' or pair[1]['status'] == 'USER_BUY_ORDER' or pair[1]['status'] == 'AVERAGE_BUY_ORDER') and pair[0] not in open_orders:
                            ncoi = 'xbot_' + pair[0]
                            offline_trade += 1
                            if offline_trade == 1:
                                cprint('|OFF-LINE| ' + colored('Исполнено во время бездействия:\x1b[K', 'cyan'))
                            coin = pair[0].replace('USDT', '')
                            for bal in balances:
                                if bal['asset'] == coin:
                                    free_quantity = num_round(float(bal['free']))
                                    tick_size = get_count(pair[1]['tickSize'])
                                    sell_price = ('{:.' + str(tick_size) + 'f}').format(float(pair[1]['averagePrice']) + float(pair[1]['averagePrice'])/100*float(sell_up))
                                    cprint('|OFF-LINE| ' + colored('BUY  ', 'green') + '(FILLED): ' + colored('[' + free_quantity + ']', 'grey', 'on_white') + ' ' + colored(coin, 'magenta', attrs=['bold']) + ' for ' + colored(pair[1]['buyPrice'] + ' USDT\x1b[K', 'yellow'))
                                    total_usdt = '{:.8f}'.format(float(pair[1]['totalUSDT']) + float(free_quantity)*float(pair[1]['buyPrice']))
                                    num_average = float(pair[1]['numAverage']) + float(data_base['trade_params']['step_aver']) if data_base['trade_params']['num_aver'] == 'y' else float(pair[1]['numAverage'])
                                    info_rewrite(pair[0], stepSize=pair[1]['stepSize'], tickSize=pair[1]['tickSize'], minNotional=pair[1]['minNotional'], priceChangePercent=pair[1]['priceChangePercent'], askPrice=pair[1]['askPrice'], averagePrice=pair[1]['averagePrice'], buyPrice=pair[1]['buyPrice'], sellPrice=sell_price, trailingPrice=pair[1]['trailingPrice'], allQuantity=free_quantity, free=0, idOrder=pair[1]['idOrder'], profit=pair[1]['profit'], totalUSDT=total_usdt, numAverage=num_average, status='SELL_ORDER')
                                    try:
                                        client.order_limit_sell(symbol=pair[0], quantity=free_quantity, price=sell_price, newClientOrderId=ncoi)
                                        open_orders.append(pair[0])
                                        cprint('|OFF-LINE| ' + colored('SELL ', 'red') + '(PLACED): ' + colored('[' + free_quantity + ']', 'grey', 'on_white') + ' ' + colored(coin, 'magenta', attrs=['bold']) + ' for ' + colored(sell_price + ' USDT\x1b[K', 'yellow'))
                                    except Exception as e:
                                        try:
                                            logging.error(str(extract_tb(exc_info()[2])[0][1]) + ' ' + pair[0] + ' ' + free_quantity + ' ' + sell_price + '\n' + str(e))
                                            cprint('|' + str(datetime.datetime.now().strftime('%H:%M:%S')) + '| ' + str(extract_tb(exc_info()[2])[0][1]) + ' ' + pair[0] + ' ' + free_quantity + ' ' + sell_price + colored('\x1b[K\n' + str(e), 'red'))
                                            profit = '{:.8f}'.format(float(pair[1]['profit']) + float(pair[1]['sellPrice'])*float(pair[1]['allQuantity']) - float(pair[1]['totalUSDT']))
                                            info_rewrite(pair[0], stepSize=pair[1]['stepSize'], tickSize=pair[1]['tickSize'], minNotional=pair[1]['minNotional'], priceChangePercent=pair[1]['priceChangePercent'], askPrice=0, averagePrice=0, buyPrice=0, sellPrice=0, trailingPrice=0, allQuantity=0, free=0, idOrder=0, profit=profit, totalUSDT=0, numAverage=0, status='NO_ORDER')
                                        except:
                                            logging.error(str(e))
                                    break
            all_items_db = check_pairs if check_pairs > all_items_db else all_items_db
            cprint('|' + str(datetime.datetime.now().strftime('%H:%M:%S')) + '| ' + colored('Проверено торговых пар: ', 'cyan') + colored(str(check_pairs) + '/' + str(all_items_db), 'cyan') + '\x1b[K', end='\r', flush=True)
        if offline_trade > 0:
            cprint('|OFF-LINE| ' + colored('Всего ордеров исполнено: ' + str(offline_trade) + '\x1b[K', 'cyan'))
        filter_trade_pairs_error = False
    except Exception as e:
        try:
            logging.error(str(extract_tb(exc_info()[2])[0][1]) + '\n' + str(e))
        except:
            logging.error(str(e))

def search_pair(msg_sp):
    global _timestamp, license_accept, start_time, check_tg, delta_perc, timer_tg, usdt_balance, trade_order, bnb_balance, spinner_delta, time_
    mutex.acquire()
    new_time = time.time()
    if _timestamp + 1798 <= new_time:
        client.stream_keepalive(conn_start_user_socket)
        _timestamp = new_time
    if new_time > start_time + 86400:
        license_accept = False
        message = check_license()
        start_time = time.time()
        if eval(message['license_accept']) == True and float(message['time']) + 4 >= time.time():
            license_accept = True
        elif eval(message['license_accept']) == False or 'license_accept' not in message:
            clear()
            cprint(colored('|' + str(datetime.datetime.now().strftime('%H:%M:%S')) + '| ', 'white') + colored("""Аккаунт Binance, привязанный к боту, не прошёл проверку!
""", 'cyan') + colored('|' + str(datetime.datetime.now().strftime('%H:%M:%S')) + '| ', 'white') + colored('Свяжитесь с администраторами ', 'cyan') + colored(' @xbot_dex ', 'grey', 'on_white') + colored(' или ', 'cyan') + colored(' @mitagmio ', 'grey', 'on_white') + colored(' в Telegram\n', 'cyan') + colored('|' + str(datetime.datetime.now().strftime('%H:%M:%S')) + '| ', 'white') + colored("""для выяснения причин или обжалования блокировки
""", 'cyan'))
            time.sleep(86400)
    if new_time - time_ > 1 and license_accept == True:
        if len(data_base['daily_profit']) > 0:
            daily_profit = data_base['daily_profit']
            for days in daily_profit:
                if str(datetime.date.today()) != str(days):
                    try:
                        daily_profit_sells = 0
                        daily_profit_profit = 0
                        eq_fiat_currencies = []
                        for sells in daily_profit[days]:
                            daily_profit_sells += 1
                            daily_profit_profit += float(sells)
                        fiat_symbol = sorted([len(fiat_symbol.replace('USDT', '')) for fiat_symbol in fiat_currencies], reverse=True)
                        space_symbol = ' ' if fiat_symbol[0] <= 6 else ' '*(fiat_symbol[0] - 5)
                        fiat_profit = sorted([len(num_round('{:.2f}'.format(float(space_profit['b'])*daily_profit_profit))) for space_profit in msg_sp if space_profit['s'] in fiat_currencies], reverse=True)
                        len_btc = len(num_round('{:.8f}'.format(daily_profit_profit))) if len(num_round('{:.8f}'.format(daily_profit_profit))) > 7 else 7
                        longer = len_btc if len_btc >= fiat_profit[0] else fiat_profit[0]
                        space_profit = ' ' if 7 >= longer else ' '*(longer - 6)
                        eq_str = '\n   USDT   | ' + num_round('{:.8f}'.format(daily_profit_profit)) + ' '*(fiat_profit[0] - len(str(daily_profit_profit))) + ' | ' + num_round(data_base['trade_info']['daily_volume'])
                        for eq_cur in fiat_currencies:
                            for eq_coin in msg_sp:
                                if eq_cur == eq_coin['s'] and len(fiat_currencies) > 0 and eq_coin['s'] in fiat_currencies and eq_coin['s'] not in eq_fiat_currencies:
                                    space_profit = space_profit if len_btc >= len(num_round('{:.2f}'.format(float(eq_coin['b'])*daily_profit_profit))) else ' '*(len(num_round('{:.2f}'.format(float(eq_coin['b'])*daily_profit_profit))) - 6)
                                    len_btc = len_btc if len_btc >= len(num_round('{:.2f}'.format(float(eq_coin['b'])*daily_profit_profit))) else len(num_round('{:.2f}'.format(float(eq_coin['b'])*daily_profit_profit)))
                                    eq_str = eq_str + '\n   ' + eq_coin['s'].replace('USDT', '') + ' '*(6 - len(eq_coin['s'].replace('USDT', ''))) + ' | ' + num_round('{:.2f}'.format(float(eq_coin['b'])*daily_profit_profit)) + ' '*(1 + len_btc - len(num_round('{:.2f}'.format(float(eq_coin['b'])*daily_profit_profit)))) + '| ' + num_round('{:.2f}'.format(float(data_base['trade_info']['daily_volume'])*float(eq_coin['b'])))
                                    eq_fiat_currencies.append(eq_coin['s'])
                        check_tg = 0
                        if len(fiat_currencies) == len(eq_fiat_currencies):
                            while check_tg <= 3:
                                try:
                                    bnb_burn = data_base['bnb_burn']
                                    n = 0
                                    commission = ''
                                    for _N in bnb_burn:
                                        for _n in bnb_burn[_N]:
                                            n += float(_n)
                                        commission = commission + '\n' + _N + ': ' + num_round('{:.8f}'.format(n))
                                    text = '<code>Referal ID: {}{}</code>'.format(referal, commission)
                                    bnb_burn.clear()
                                    data_base['bnb_burn'] = bnb_burn
                                    break
                                except:
                                    check_tg += 1
                            check_tg = 0
                            if tg_notification == 'y':
                                while check_tg <= 3:
                                    try:
                                        text = """<code>🔔 Статистика за {}
✅ Сделок закрыто: {}
   Валюта{}| Прибыль{}| Объём{}</code>""".format(days, daily_profit_sells, space_symbol, space_profit, eq_str)
                                        tg_message = bot.send_message(chat_id=tg_name, text=text, parse_mode='HTML')
                                        check_tg = 0
                                        while check_tg <= 3:
                                            try:
                                                bot.pin_chat_message(chat_id=tg_name, message_id=tg_message.message_id)
                                                break
                                            except Exception as e:
                                                check_tg += 1
                                                logging.error(str(e))
                                        break
                                    except:
                                        check_tg += 1
                                        logging.error(str(e))
                            check_tg = 0
                            daily_profit.pop(days)
                            data_base['daily_profit'] = daily_profit
                            break
                    except Exception as e:
                        try:
                            logging.error(str(extract_tb(exc_info()[2])[0][1]) + '\n' + str(e))
                        except:
                            logging.error(str(e))
        trade_pairs = sorted([pair for pair in data_base.items() if pair[0] not in system_key], key=lambda pair: (float(pair[1]['askPrice']) - float(pair[1]['sellPrice']))/(float(pair[1]['sellPrice'])/100) if pair[1]['status'] == 'SELL_ORDER' else float(pair[1]['priceChangePercent']), reverse=False)
        delta_perc = 0
        delta_perc = float('{:.2f}'.format(sum([float(percent) for percent in [pair[1]['priceChangePercent'] if not pair[0] not in system_key and float(pair[1]['priceChangePercent']) != 0 else '1' for pair in data_base.items()]])/len([pair[1]['priceChangePercent'] if not pair[0] not in system_key and float(pair[1]['priceChangePercent']) != 0 else '1' for pair in data_base.items()])))
        all_balance = 0
        all_num_average = 0
        all_open_order = 0
        for eq_balance in trade_pairs:
            if eq_balance[1]['status'] == 'SELL_ORDER' or eq_balance[1]['status'] == 'TRAILING_SELL_ORDER':
                all_balance += float(eq_balance[1]['askPrice'])*float(eq_balance[1]['allQuantity'])
                all_num_average += float(eq_balance[1]['numAverage']) if float(eq_balance[1]['numAverage']) > 1 else 1
                all_open_order += 1
        all_balance += float(usdt_balance)
        try:
            max_trade_pairs = int(float(data_base.__getitem__('trade_params')['max_trade_pairs'])*float(usdt_balance)/all_balance*(all_open_order + delta_perc)/all_num_average) if auto_trade_pairs == 'y' and all_open_order > 0 and all_open_order != delta_perc and all_num_average > 0 and float(usdt_balance) > 0 and all_balance != float(usdt_balance) and float(data_base.__getitem__('trade_params')['max_trade_pairs']) > 0 else int(data_base.__getitem__('trade_params')['max_trade_pairs'])
            max_trade_pairs = max_trade_pairs if max_trade_pairs <= float(data_base.__getitem__('trade_params')['max_trade_pairs']) and max_trade_pairs >= 0 else float(data_base.__getitem__('trade_params')['max_trade_pairs'])
            info_delta = delta_perc
            delta_perc = 0 if delta_percent == 'n' or delta_perc < float(perc_down) or delta_perc > float(sell_up) else float('{:.2f}'.format(delta_perc/3))
            buy_down_delta = 0 if delta_perc >= 0 else delta_perc
        except Exception as e:
            try:
                logging.error(str(extract_tb(exc_info()[2])[0][1]) + '\n' + str(e))
            except:
                logging.error(str(e))
        if tg_notification == 'y':
            timer_tg -= 1
            if timer_tg <= 0:
                timer_tg = 300
                try:
                    text_description = """💼 Общий баланс: {} USDT
🔑 Свободный баланс: {} USDT
💸 Прибыль: {} USDT
📂 Открытые ордера: {}
🔥 Успешных сделок: {}
🎯 Дельта: {}%
⏳ Обновлено в {}""".format(num_round('{:.8f}'.format(all_balance)), num_round(usdt_balance), num_round(data_base['trade_info']['profit']), num_round(data_base['trade_info']['sell_open_orders']), num_round(data_base['trade_info']['sell_filled_orders']), num_round(info_delta), str(datetime.datetime.now().strftime('%H:%M:%S')))
                    bot.set_chat_description(tg_name, text_description)
                except Exception as e:
                    try:
                        logging.error(str(extract_tb(exc_info()[2])[0][1]) + '\n' + str(e))
                    except:
                        logging.error(str(e))
        try:
            checked_pairs = []
            for pair in trade_pairs:
                for coin in msg_sp:
                    if coin['s'] == pair[0] and coin['s'] not in checked_pairs and coin['s'] in data_base['white_list'] and float(bnb_balance) >= 0.1 and trade_order == False:
                        checked_pairs.append(coin['s'])
                        ncoi = 'xbot_' + pair[0]
                        ncoim = 'trailingabt_' + pair[0]
                        _step_size = pair[1]['stepSize']
                        _tick_size = pair[1]['tickSize']
                        step_size = get_count(_step_size)
                        tick_size = get_count(_tick_size)
                        multi_num_average = float(pair[1]['numAverage'])/10 if float(pair[1]['numAverage']) > 0 else 0
                        if pair[1]['status'] == 'NO_ORDER':
                            info_rewrite(pair[0], stepSize=pair[1]['stepSize'], tickSize=pair[1]['tickSize'], minNotional=pair[1]['minNotional'], priceChangePercent=coin['P'], askPrice=num_round(coin['a']), averagePrice=pair[1]['averagePrice'], buyPrice=pair[1]['buyPrice'], sellPrice=pair[1]['sellPrice'], trailingPrice=pair[1]['trailingPrice'], allQuantity=pair[1]['allQuantity'], free=pair[1]['free'], idOrder=pair[1]['idOrder'], profit=pair[1]['profit'], totalUSDT=pair[1]['totalUSDT'], numAverage=pair[1]['numAverage'], status=pair[1]['status'])
                            if float(usdt_balance) >= float(min_balance) and float(coin['P']) <= float(perc_down) + delta_perc and float(coin['b']) >= float(min_price) and (float(max_trade_pairs) < 0 or float(data_base['trade_info']['sell_open_orders']) < float(max_trade_pairs)):
                                q = float(('{:.' + str(step_size) + 'f}').format(float(min_order)/float(coin['a']) + float(_step_size)))
                                while float(q)*float(coin['a']) < float(pair[1]['minNotional']):
                                    q += float(_step_size)
                                q = ('{:.' + str(step_size) + 'f}').format(float(q))
                                if float(usdt_balance) > float(('{:.' + str(tick_size) + 'f}').format(float(q)*float(coin['a']))):
                                    usdt_balance = '{:.8f}'.format(float(usdt_balance) - float(('{:.' + str(tick_size) + 'f}').format(float(q)*float(coin['a']))))
                                    client.order_limit_buy(symbol=coin['s'], quantity=num_round(q), price=num_round(coin['a']), newClientOrderId=ncoi)
                                    trade_order = True
                                    break
                                    if pair[1]['status'] == 'BUY_ORDER' and float(coin['a']) >= float(('{:.' + str(tick_size) + 'f}').format(float(pair[1]['averagePrice'])*(1 + (float(sell_up) + delta_perc)/100))):
                                        info_rewrite(pair[0], stepSize=pair[1]['stepSize'], tickSize=pair[1]['tickSize'], minNotional=pair[1]['minNotional'], priceChangePercent=coin['P'], askPrice=num_round(coin['a']), averagePrice=pair[1]['averagePrice'], buyPrice=pair[1]['buyPrice'], sellPrice=pair[1]['sellPrice'], trailingPrice=pair[1]['trailingPrice'], allQuantity=pair[1]['allQuantity'], free=pair[1]['free'], idOrder=pair[1]['idOrder'], profit=pair[1]['profit'], totalUSDT=pair[1]['totalUSDT'], numAverage=pair[1]['numAverage'], status=pair[1]['status'])
                                        canceled_order(pair[0], pair[1]['idOrder'], ncoi, 'BUY')
                                        trade_order = True
                                        break
                                    elif pair[1]['status'] == 'SELL_ORDER':
                                        if float(usdt_balance) >= float(min_balance) and float(usdt_balance) > float(('{:.' + str(tick_size) + 'f}').format(float(pair[1]['allQuantity'])*(2 + multi_num_average)*float(coin['a']))) and float(coin['a']) <= float(('{:.' + str(tick_size) + 'f}').format(float(pair[1]['buyPrice']) - float(pair[1]['buyPrice'])/100*(float(pair[1]['numAverage']) + float(buy_down) - buy_down_delta))):
                                            usdt_balance = '{:.8f}'.format(float(usdt_balance) - float(('{:.' + str(tick_size) + 'f}').format(float(pair[1]['allQuantity'])*(2 + multi_num_average)*float(coin['a']))))
                                            canceled_order(pair[0], pair[1]['idOrder'], ncoi, 'SELL')
                                            trade_order = True
                                            break
                                        else:
                                            if trailing_sell == 'y' and float(coin['a']) >= float(pair[1]['sellPrice'])*(1 - float(trailing_percent)/100) and float(coin['b']) >= float(trailing_price):
                                                new_sell_price = pair[1]['sellPrice']
                                                while float(coin['a']) > float(new_sell_price) or float(new_sell_price) == float(pair[1]['sellPrice']):
                                                    new_sell_price = ('{:.' + str(tick_size) + 'f}').format(float(new_sell_price) + float(_tick_size))
                                                info_rewrite(pair[0], stepSize=pair[1]['stepSize'], tickSize=pair[1]['tickSize'], minNotional=pair[1]['minNotional'], priceChangePercent=coin['P'], askPrice=num_round(coin['a']), averagePrice=pair[1]['averagePrice'], buyPrice=pair[1]['buyPrice'], sellPrice=new_sell_price, trailingPrice=pair[1]['trailingPrice'], allQuantity=pair[1]['allQuantity'], free=pair[1]['free'], idOrder=pair[1]['idOrder'], profit=pair[1]['profit'], totalUSDT=pair[1]['totalUSDT'], numAverage=pair[1]['numAverage'], status='TRAILING_SELL_ORDER')
                                                canceled_order(pair[0], pair[1]['idOrder'], ncoi, 'SELL')
                                                trade_order = True
                                                break
                                            else:
                                                info_rewrite(pair[0], stepSize=pair[1]['stepSize'], tickSize=pair[1]['tickSize'], minNotional=pair[1]['minNotional'], priceChangePercent=coin['P'], askPrice=num_round(coin['a']), averagePrice=pair[1]['averagePrice'], buyPrice=pair[1]['buyPrice'], sellPrice=pair[1]['sellPrice'], trailingPrice=pair[1]['trailingPrice'], allQuantity=pair[1]['allQuantity'], free=pair[1]['free'], idOrder=pair[1]['idOrder'], profit=pair[1]['profit'], totalUSDT=pair[1]['totalUSDT'], numAverage=pair[1]['numAverage'], status=pair[1]['status'])
                                            if pair[1]['status'] == 'TRAILING_SELL_ORDER':
                                                if float(coin['a']) >= float(pair[1]['sellPrice']):
                                                    new_sell_price = pair[1]['sellPrice']
                                                    while float(coin['a']) > float(new_sell_price) or float(new_sell_price) == float(pair[1]['sellPrice']):
                                                        new_sell_price = num_round(('{:.' + str(tick_size) + 'f}').format(float(new_sell_price) + float(_tick_size)))
                                                    new_trailing_price = pair[1]['trailingPrice'] if float(pair[1]['trailingPrice']) + float(pair[1]['trailingPrice'])/100*float(sell_up)/2 > float(new_sell_price) else num_round(('{:.' + str(tick_size) + 'f}').format(float(new_sell_price) - float(pair[1]['trailingPrice'])/100*float(sell_up)/2 + float(_tick_size)))
                                                    if float(new_trailing_price) == pair[1]['trailingPrice']:
                                                        new_trailing_price = num_round(('{:.' + str(tick_size) + 'f}').format(float(new_trailing_price) + float(_tick_size)))
                                                    info_rewrite(pair[0], stepSize=pair[1]['stepSize'], tickSize=pair[1]['tickSize'], minNotional=pair[1]['minNotional'], priceChangePercent=coin['P'], askPrice=num_round(coin['a']), averagePrice=pair[1]['averagePrice'], buyPrice=pair[1]['buyPrice'], sellPrice=new_sell_price, trailingPrice=new_trailing_price, allQuantity=pair[1]['allQuantity'], free=pair[1]['free'], idOrder=pair[1]['idOrder'], profit=pair[1]['profit'], totalUSDT=pair[1]['totalUSDT'], numAverage=pair[1]['numAverage'], status=pair[1]['status'])
                                                else:
                                                    if float(coin['a']) < float(pair[1]['sellPrice'])*(1 - float(trailing_percent)/100):
                                                        new_sell_price = num_round(('{:.' + str(tick_size) + 'f}').format(float(pair[1]['sellPrice']) - float(_tick_size)))
                                                        q = num_round(('{:.' + str(step_size) + 'f}').format(float(pair[1]['minNotional'])/float(coin['b'])))
                                                        while float(pair[1]['minNotional']) > float(q)*float(coin['b']):
                                                            q = num_round(('{:.' + str(step_size) + 'f}').format(float(q) + float(_step_size)))
                                                        if ((float(pair[1]['allQuantity']) - float(q))*float(pair[1]['trailingPrice']) > float(pair[1]['minNotional']) or float(pair[1]['allQuantity']) - float(q) > float(q)*(1 + multi_num_average)) and float(coin['b']) > float(pair[1]['trailingPrice']):
                                                            try:
                                                                client.order_market_sell(symbol=pair[0], quantity=q, newClientOrderId=ncoim)
                                                                trade_order = True
                                                                break
                                                            except Exception as e:
                                                                try:
                                                                    logging.error(str(extract_tb(exc_info()[2])[0][1]) + ' ' + pair[0] + ' ' + coin['b'] + ' ' + coin['B'] + ' ' + q + '\n' + str(e))
                                                                except:
                                                                    logging.error(str(e))
                                                                time.sleep(5)
                                                        elif ((float(pair[1]['allQuantity']) - float(q))*float(pair[1]['averagePrice']) <= float(pair[1]['minNotional']) or float(coin['b']) <= float(pair[1]['trailingPrice']) or float(pair[1]['allQuantity']) - float(q) <= float(q)*(1 + multi_num_average)) and float(coin['b']) >= float(pair[1]['averagePrice']):
                                                            try:
                                                                client.order_market_sell(symbol=pair[0], quantity=pair[1]['allQuantity'], newClientOrderId=ncoi)
                                                                trade_order = True
                                                                break
                                                            except Exception as e:
                                                                try:
                                                                    logging.error(str(extract_tb(exc_info()[2])[0][1]) + ' ' + pair[0] + ' ' + coin['b'] + ' ' + coin['B'] + ' ' + pair[1]['allQuantity'] + '\n' + str(e))
                                                                except:
                                                                    logging.error(str(e))
                                                                time.sleep(5)
                                                        elif float(usdt_balance) > float(('{:.' + str(tick_size) + 'f}').format(float(pair[1]['allQuantity'])*(2 + multi_num_average)*float(coin['a']))) and float(coin['a']) <= float(('{:.' + str(tick_size) + 'f}').format(float(pair[1]['buyPrice']) - float(pair[1]['buyPrice'])/100*(float(buy_down) - buy_down_delta))):
                                                            info_rewrite(pair[0], stepSize=pair[1]['stepSize'], tickSize=pair[1]['tickSize'], minNotional=pair[1]['minNotional'], priceChangePercent=coin['P'], askPrice=num_round(coin['a']), averagePrice=pair[1]['averagePrice'], buyPrice=pair[1]['buyPrice'], sellPrice=pair[1]['sellPrice'], trailingPrice=pair[1]['trailingPrice'], allQuantity=pair[1]['allQuantity'], free=pair[1]['allQuantity'], idOrder=pair[1]['idOrder'], profit=pair[1]['profit'], totalUSDT=pair[1]['totalUSDT'], numAverage=pair[1]['numAverage'], status='CANCELED_SELL_ORDER')
                                                            break
                                                        else:
                                                            info_rewrite(pair[0], stepSize=pair[1]['stepSize'], tickSize=pair[1]['tickSize'], minNotional=pair[1]['minNotional'], priceChangePercent=coin['P'], askPrice=num_round(coin['a']), averagePrice=pair[1]['averagePrice'], buyPrice=pair[1]['buyPrice'], sellPrice=pair[1]['sellPrice'], trailingPrice=pair[1]['trailingPrice'], allQuantity=pair[1]['allQuantity'], free=pair[1]['free'], idOrder=pair[1]['idOrder'], profit=pair[1]['profit'], totalUSDT=pair[1]['totalUSDT'], numAverage=pair[1]['numAverage'], status=pair[1]['status'])
                                                    else:
                                                        info_rewrite(pair[0], stepSize=pair[1]['stepSize'], tickSize=pair[1]['tickSize'], minNotional=pair[1]['minNotional'], priceChangePercent=coin['P'], askPrice=num_round(coin['a']), averagePrice=pair[1]['averagePrice'], buyPrice=pair[1]['buyPrice'], sellPrice=pair[1]['sellPrice'], trailingPrice=pair[1]['trailingPrice'], allQuantity=pair[1]['allQuantity'], free=pair[1]['free'], idOrder=pair[1]['idOrder'], profit=pair[1]['profit'], totalUSDT=pair[1]['totalUSDT'], numAverage=pair[1]['numAverage'], status=pair[1]['status'])
                                                    if float(usdt_balance) >= float(min_balance) and pair[1]['status'] == 'CANCELED_SELL_ORDER' and float(usdt_balance) > float(('{:.' + str(tick_size) + 'f}').format(float(pair[1]['allQuantity'])*(2 + multi_num_average)*float(coin['a']))):
                                                        old_order_quantity = pair[1]['free']
                                                        new_order_quantity = num_round(('{:.' + str(step_size) + 'f}').format(float(old_order_quantity)*(2 + multi_num_average)))
                                                        usdt_balance = '{:.8f}'.format(float(usdt_balance) - float(new_order_quantity)*float(coin['a']))
                                                        average_buy_price = ('{:.' + str(tick_size) + 'f}').format((float(pair[1]['averagePrice'])*float(old_order_quantity) + float(coin['a'])*float(new_order_quantity))/(float(old_order_quantity) + float(new_order_quantity)))
                                                        average_sell_price = ('{:.' + str(tick_size) + 'f}').format(float(average_buy_price) + float(average_buy_price)/100*(float(sell_up) + delta_perc))
                                                        info_rewrite(pair[0], stepSize=pair[1]['stepSize'], tickSize=pair[1]['tickSize'], minNotional=pair[1]['minNotional'], priceChangePercent=coin['P'], askPrice=num_round(coin['a']), averagePrice=average_buy_price, buyPrice=num_round(coin['a']), sellPrice=num_round(average_sell_price), trailingPrice=average_buy_price, allQuantity=new_order_quantity, free=pair[1]['free'], idOrder=pair[1]['idOrder'], profit=pair[1]['profit'], totalUSDT=pair[1]['totalUSDT'], numAverage=pair[1]['numAverage'], status='AVERAGE_BUY_ORDER')
                                                        client.order_limit_buy(symbol=coin['s'], quantity=new_order_quantity, price=num_round(coin['a']), newClientOrderId=ncoi)
                                                        trade_order = True
                                                        break
                                                    elif pair[1]['status'] == 'CANCELED_SELL_ORDER' and float(usdt_balance) < float(('{:.' + str(tick_size) + 'f}').format(float(pair[1]['allQuantity'])*(2 + multi_num_average)*float(coin['a']))):
                                                        q = ('{:.' + str(step_size) + 'f}').format(float(pair[1]['free']))
                                                        client.order_limit_sell(symbol=pair[0], quantity=q, price=pair[1]['sellPrice'], newClientOrderId=ncoi)
                                                        info_rewrite(pair[0], stepSize=pair[1]['stepSize'], tickSize=pair[1]['tickSize'], minNotional=pair[1]['minNotional'], priceChangePercent=coin['P'], askPrice=num_round(coin['a']), averagePrice=pair[1]['averagePrice'], buyPrice=pair[1]['buyPrice'], sellPrice=pair[1]['sellPrice'], trailingPrice=pair[1]['trailingPrice'], allQuantity=pair[1]['free'], free=0, idOrder=pair[1]['idOrder'], profit=pair[1]['profit'], totalUSDT=pair[1]['totalUSDT'], numAverage=pair[1]['numAverage'], status='SELL_ORDER')
                                                        trade_order = True
                                                        break
                                                    elif pair[1]['status'] == 'AVERAGE_BUY_ORDER' and float(coin['a']) >= float(('{:.' + str(tick_size) + 'f}').format(float(pair[1]['buyPrice'])*(1 + (float(sell_up) + delta_perc)/100))):
                                                        info_rewrite(pair[0], stepSize=pair[1]['stepSize'], tickSize=pair[1]['tickSize'], minNotional=pair[1]['minNotional'], priceChangePercent=coin['P'], askPrice=num_round(coin['a']), averagePrice=pair[1]['averagePrice'], buyPrice=pair[1]['buyPrice'], sellPrice=pair[1]['sellPrice'], trailingPrice=pair[1]['trailingPrice'], allQuantity=pair[1]['allQuantity'], free=pair[1]['free'], idOrder=pair[1]['idOrder'], profit=pair[1]['profit'], totalUSDT=pair[1]['totalUSDT'], numAverage=pair[1]['numAverage'], status=pair[1]['status'])
                                                        canceled_order(pair[0], pair[1]['idOrder'], ncoi, 'BUY')
                                                        trade_order = True
                                                        break
                                                        if float(bnb_balance) < 0.1:
                                                            for pair in tickers:
                                                                if pair['symbol'] == 'BNBUSDT':
                                                                    for step in exchange:
                                                                        if step['symbol'] == 'BNBUSDT' and float(bnb_balance) < 0.1:
                                                                            try:
                                                                                q = ('{:.' + str(get_count(num_round(step['filters'][2]['stepSize']))) + 'f}').format(float(num_round(step['filters'][3]['minNotional']))/float(pair['askPrice']))
                                                                                while float(q)*float(pair['askPrice']) <= float(step['filters'][3]['minNotional']):
                                                                                    q = ('{:.' + str(get_count(num_round(step['filters'][2]['stepSize']))) + 'f}').format(float(q) + float(step['filters'][2]['stepSize']))
                                                                                client.order_market_buy(symbol='BNBUSDT', quantity=q)
                                                                                bnb_balance = '{:.8f}'.format(float(bnb_balance) + float(q))
                                                                                trade_order = True
                                                                                break
                                                                            except Exception as e:
                                                                                try:
                                                                                    logging.error(str(extract_tb(exc_info()[2])[0][1]) + ' ' + 'Ошибка при покупке BNB: ' + q + '\n' + str(e))
                                                                                    cprint('|' + str(datetime.datetime.now().strftime('%H:%M:%S')) + '| ' + str(extract_tb(exc_info()[2])[0][1]) + ' ' + colored('Ошибка при покупке BNB: ', 'cyan') + q + colored('\x1b[K\n' + str(e), 'red'), end='\r', flush=True)
                                                                                except:
                                                                                    logging.error(str(e))
                                            elif float(usdt_balance) >= float(min_balance) and pair[1]['status'] == 'CANCELED_SELL_ORDER' and float(usdt_balance) > float(('{:.' + str(tick_size) + 'f}').format(float(pair[1]['allQuantity'])*(2 + multi_num_average)*float(coin['a']))):
                                                old_order_quantity = pair[1]['free']
                                                new_order_quantity = num_round(('{:.' + str(step_size) + 'f}').format(float(old_order_quantity)*(2 + multi_num_average)))
                                                usdt_balance = '{:.8f}'.format(float(usdt_balance) - float(new_order_quantity)*float(coin['a']))
                                                average_buy_price = ('{:.' + str(tick_size) + 'f}').format((float(pair[1]['averagePrice'])*float(old_order_quantity) + float(coin['a'])*float(new_order_quantity))/(float(old_order_quantity) + float(new_order_quantity)))
                                                average_sell_price = ('{:.' + str(tick_size) + 'f}').format(float(average_buy_price) + float(average_buy_price)/100*(float(sell_up) + delta_perc))
                                                info_rewrite(pair[0], stepSize=pair[1]['stepSize'], tickSize=pair[1]['tickSize'], minNotional=pair[1]['minNotional'], priceChangePercent=coin['P'], askPrice=num_round(coin['a']), averagePrice=average_buy_price, buyPrice=num_round(coin['a']), sellPrice=num_round(average_sell_price), trailingPrice=average_buy_price, allQuantity=new_order_quantity, free=pair[1]['free'], idOrder=pair[1]['idOrder'], profit=pair[1]['profit'], totalUSDT=pair[1]['totalUSDT'], numAverage=pair[1]['numAverage'], status='AVERAGE_BUY_ORDER')
                                                client.order_limit_buy(symbol=coin['s'], quantity=new_order_quantity, price=num_round(coin['a']), newClientOrderId=ncoi)
                                                trade_order = True
                                                break
                                            elif pair[1]['status'] == 'CANCELED_SELL_ORDER' and float(usdt_balance) < float(('{:.' + str(tick_size) + 'f}').format(float(pair[1]['allQuantity'])*(2 + multi_num_average)*float(coin['a']))):
                                                q = ('{:.' + str(step_size) + 'f}').format(float(pair[1]['free']))
                                                client.order_limit_sell(symbol=pair[0], quantity=q, price=pair[1]['sellPrice'], newClientOrderId=ncoi)
                                                info_rewrite(pair[0], stepSize=pair[1]['stepSize'], tickSize=pair[1]['tickSize'], minNotional=pair[1]['minNotional'], priceChangePercent=coin['P'], askPrice=num_round(coin['a']), averagePrice=pair[1]['averagePrice'], buyPrice=pair[1]['buyPrice'], sellPrice=pair[1]['sellPrice'], trailingPrice=pair[1]['trailingPrice'], allQuantity=pair[1]['free'], free=0, idOrder=pair[1]['idOrder'], profit=pair[1]['profit'], totalUSDT=pair[1]['totalUSDT'], numAverage=pair[1]['numAverage'], status='SELL_ORDER')
                                                trade_order = True
                                                break
                                            elif pair[1]['status'] == 'AVERAGE_BUY_ORDER' and float(coin['a']) >= float(('{:.' + str(tick_size) + 'f}').format(float(pair[1]['buyPrice'])*(1 + (float(sell_up) + delta_perc)/100))):
                                                info_rewrite(pair[0], stepSize=pair[1]['stepSize'], tickSize=pair[1]['tickSize'], minNotional=pair[1]['minNotional'], priceChangePercent=coin['P'], askPrice=num_round(coin['a']), averagePrice=pair[1]['averagePrice'], buyPrice=pair[1]['buyPrice'], sellPrice=pair[1]['sellPrice'], trailingPrice=pair[1]['trailingPrice'], allQuantity=pair[1]['allQuantity'], free=pair[1]['free'], idOrder=pair[1]['idOrder'], profit=pair[1]['profit'], totalUSDT=pair[1]['totalUSDT'], numAverage=pair[1]['numAverage'], status=pair[1]['status'])
                                                canceled_order(pair[0], pair[1]['idOrder'], ncoi, 'BUY')
                                                trade_order = True
                                                break
                                                if float(bnb_balance) < 0.1:
                                                    for pair in tickers:
                                                        if pair['symbol'] == 'BNBUSDT':
                                                            for step in exchange:
                                                                if step['symbol'] == 'BNBUSDT' and float(bnb_balance) < 0.1:
                                                                    try:
                                                                        q = ('{:.' + str(get_count(num_round(step['filters'][2]['stepSize']))) + 'f}').format(float(num_round(step['filters'][3]['minNotional']))/float(pair['askPrice']))
                                                                        while float(q)*float(pair['askPrice']) <= float(step['filters'][3]['minNotional']):
                                                                            q = ('{:.' + str(get_count(num_round(step['filters'][2]['stepSize']))) + 'f}').format(float(q) + float(step['filters'][2]['stepSize']))
                                                                        client.order_market_buy(symbol='BNBUSDT', quantity=q)
                                                                        bnb_balance = '{:.8f}'.format(float(bnb_balance) + float(q))
                                                                        trade_order = True
                                                                        break
                                                                    except Exception as e:
                                                                        try:
                                                                            logging.error(str(extract_tb(exc_info()[2])[0][1]) + ' ' + 'Ошибка при покупке BNB: ' + q + '\n' + str(e))
                                                                            cprint('|' + str(datetime.datetime.now().strftime('%H:%M:%S')) + '| ' + str(extract_tb(exc_info()[2])[0][1]) + ' ' + colored('Ошибка при покупке BNB: ', 'cyan') + q + colored('\x1b[K\n' + str(e), 'red'), end='\r', flush=True)
                                                                        except:
                                                                            logging.error(str(e))
                                    elif pair[1]['status'] == 'TRAILING_SELL_ORDER':
                                        if float(coin['a']) >= float(pair[1]['sellPrice']):
                                            new_sell_price = pair[1]['sellPrice']
                                            while float(coin['a']) > float(new_sell_price) or float(new_sell_price) == float(pair[1]['sellPrice']):
                                                new_sell_price = num_round(('{:.' + str(tick_size) + 'f}').format(float(new_sell_price) + float(_tick_size)))
                                            new_trailing_price = pair[1]['trailingPrice'] if float(pair[1]['trailingPrice']) + float(pair[1]['trailingPrice'])/100*float(sell_up)/2 > float(new_sell_price) else num_round(('{:.' + str(tick_size) + 'f}').format(float(new_sell_price) - float(pair[1]['trailingPrice'])/100*float(sell_up)/2 + float(_tick_size)))
                                            if float(new_trailing_price) == pair[1]['trailingPrice']:
                                                new_trailing_price = num_round(('{:.' + str(tick_size) + 'f}').format(float(new_trailing_price) + float(_tick_size)))
                                            info_rewrite(pair[0], stepSize=pair[1]['stepSize'], tickSize=pair[1]['tickSize'], minNotional=pair[1]['minNotional'], priceChangePercent=coin['P'], askPrice=num_round(coin['a']), averagePrice=pair[1]['averagePrice'], buyPrice=pair[1]['buyPrice'], sellPrice=new_sell_price, trailingPrice=new_trailing_price, allQuantity=pair[1]['allQuantity'], free=pair[1]['free'], idOrder=pair[1]['idOrder'], profit=pair[1]['profit'], totalUSDT=pair[1]['totalUSDT'], numAverage=pair[1]['numAverage'], status=pair[1]['status'])
                                        else:
                                            if float(coin['a']) < float(pair[1]['sellPrice'])*(1 - float(trailing_percent)/100):
                                                new_sell_price = num_round(('{:.' + str(tick_size) + 'f}').format(float(pair[1]['sellPrice']) - float(_tick_size)))
                                                q = num_round(('{:.' + str(step_size) + 'f}').format(float(pair[1]['minNotional'])/float(coin['b'])))
                                                while float(pair[1]['minNotional']) > float(q)*float(coin['b']):
                                                    q = num_round(('{:.' + str(step_size) + 'f}').format(float(q) + float(_step_size)))
                                                if ((float(pair[1]['allQuantity']) - float(q))*float(pair[1]['trailingPrice']) > float(pair[1]['minNotional']) or float(pair[1]['allQuantity']) - float(q) > float(q)*(1 + multi_num_average)) and float(coin['b']) > float(pair[1]['trailingPrice']):
                                                    try:
                                                        client.order_market_sell(symbol=pair[0], quantity=q, newClientOrderId=ncoim)
                                                        trade_order = True
                                                        break
                                                    except Exception as e:
                                                        try:
                                                            logging.error(str(extract_tb(exc_info()[2])[0][1]) + ' ' + pair[0] + ' ' + coin['b'] + ' ' + coin['B'] + ' ' + q + '\n' + str(e))
                                                        except:
                                                            logging.error(str(e))
                                                        time.sleep(5)
                                                elif ((float(pair[1]['allQuantity']) - float(q))*float(pair[1]['averagePrice']) <= float(pair[1]['minNotional']) or float(coin['b']) <= float(pair[1]['trailingPrice']) or float(pair[1]['allQuantity']) - float(q) <= float(q)*(1 + multi_num_average)) and float(coin['b']) >= float(pair[1]['averagePrice']):
                                                    try:
                                                        client.order_market_sell(symbol=pair[0], quantity=pair[1]['allQuantity'], newClientOrderId=ncoi)
                                                        trade_order = True
                                                        break
                                                    except Exception as e:
                                                        try:
                                                            logging.error(str(extract_tb(exc_info()[2])[0][1]) + ' ' + pair[0] + ' ' + coin['b'] + ' ' + coin['B'] + ' ' + pair[1]['allQuantity'] + '\n' + str(e))
                                                        except:
                                                            logging.error(str(e))
                                                        time.sleep(5)
                                                elif float(usdt_balance) > float(('{:.' + str(tick_size) + 'f}').format(float(pair[1]['allQuantity'])*(2 + multi_num_average)*float(coin['a']))) and float(coin['a']) <= float(('{:.' + str(tick_size) + 'f}').format(float(pair[1]['buyPrice']) - float(pair[1]['buyPrice'])/100*(float(buy_down) - buy_down_delta))):
                                                    info_rewrite(pair[0], stepSize=pair[1]['stepSize'], tickSize=pair[1]['tickSize'], minNotional=pair[1]['minNotional'], priceChangePercent=coin['P'], askPrice=num_round(coin['a']), averagePrice=pair[1]['averagePrice'], buyPrice=pair[1]['buyPrice'], sellPrice=pair[1]['sellPrice'], trailingPrice=pair[1]['trailingPrice'], allQuantity=pair[1]['allQuantity'], free=pair[1]['allQuantity'], idOrder=pair[1]['idOrder'], profit=pair[1]['profit'], totalUSDT=pair[1]['totalUSDT'], numAverage=pair[1]['numAverage'], status='CANCELED_SELL_ORDER')
                                                    break
                                                else:
                                                    info_rewrite(pair[0], stepSize=pair[1]['stepSize'], tickSize=pair[1]['tickSize'], minNotional=pair[1]['minNotional'], priceChangePercent=coin['P'], askPrice=num_round(coin['a']), averagePrice=pair[1]['averagePrice'], buyPrice=pair[1]['buyPrice'], sellPrice=pair[1]['sellPrice'], trailingPrice=pair[1]['trailingPrice'], allQuantity=pair[1]['allQuantity'], free=pair[1]['free'], idOrder=pair[1]['idOrder'], profit=pair[1]['profit'], totalUSDT=pair[1]['totalUSDT'], numAverage=pair[1]['numAverage'], status=pair[1]['status'])
                                            else:
                                                info_rewrite(pair[0], stepSize=pair[1]['stepSize'], tickSize=pair[1]['tickSize'], minNotional=pair[1]['minNotional'], priceChangePercent=coin['P'], askPrice=num_round(coin['a']), averagePrice=pair[1]['averagePrice'], buyPrice=pair[1]['buyPrice'], sellPrice=pair[1]['sellPrice'], trailingPrice=pair[1]['trailingPrice'], allQuantity=pair[1]['allQuantity'], free=pair[1]['free'], idOrder=pair[1]['idOrder'], profit=pair[1]['profit'], totalUSDT=pair[1]['totalUSDT'], numAverage=pair[1]['numAverage'], status=pair[1]['status'])
                                            if float(usdt_balance) >= float(min_balance) and pair[1]['status'] == 'CANCELED_SELL_ORDER' and float(usdt_balance) > float(('{:.' + str(tick_size) + 'f}').format(float(pair[1]['allQuantity'])*(2 + multi_num_average)*float(coin['a']))):
                                                old_order_quantity = pair[1]['free']
                                                new_order_quantity = num_round(('{:.' + str(step_size) + 'f}').format(float(old_order_quantity)*(2 + multi_num_average)))
                                                usdt_balance = '{:.8f}'.format(float(usdt_balance) - float(new_order_quantity)*float(coin['a']))
                                                average_buy_price = ('{:.' + str(tick_size) + 'f}').format((float(pair[1]['averagePrice'])*float(old_order_quantity) + float(coin['a'])*float(new_order_quantity))/(float(old_order_quantity) + float(new_order_quantity)))
                                                average_sell_price = ('{:.' + str(tick_size) + 'f}').format(float(average_buy_price) + float(average_buy_price)/100*(float(sell_up) + delta_perc))
                                                info_rewrite(pair[0], stepSize=pair[1]['stepSize'], tickSize=pair[1]['tickSize'], minNotional=pair[1]['minNotional'], priceChangePercent=coin['P'], askPrice=num_round(coin['a']), averagePrice=average_buy_price, buyPrice=num_round(coin['a']), sellPrice=num_round(average_sell_price), trailingPrice=average_buy_price, allQuantity=new_order_quantity, free=pair[1]['free'], idOrder=pair[1]['idOrder'], profit=pair[1]['profit'], totalUSDT=pair[1]['totalUSDT'], numAverage=pair[1]['numAverage'], status='AVERAGE_BUY_ORDER')
                                                client.order_limit_buy(symbol=coin['s'], quantity=new_order_quantity, price=num_round(coin['a']), newClientOrderId=ncoi)
                                                trade_order = True
                                                break
                                            elif pair[1]['status'] == 'CANCELED_SELL_ORDER' and float(usdt_balance) < float(('{:.' + str(tick_size) + 'f}').format(float(pair[1]['allQuantity'])*(2 + multi_num_average)*float(coin['a']))):
                                                q = ('{:.' + str(step_size) + 'f}').format(float(pair[1]['free']))
                                                client.order_limit_sell(symbol=pair[0], quantity=q, price=pair[1]['sellPrice'], newClientOrderId=ncoi)
                                                info_rewrite(pair[0], stepSize=pair[1]['stepSize'], tickSize=pair[1]['tickSize'], minNotional=pair[1]['minNotional'], priceChangePercent=coin['P'], askPrice=num_round(coin['a']), averagePrice=pair[1]['averagePrice'], buyPrice=pair[1]['buyPrice'], sellPrice=pair[1]['sellPrice'], trailingPrice=pair[1]['trailingPrice'], allQuantity=pair[1]['free'], free=0, idOrder=pair[1]['idOrder'], profit=pair[1]['profit'], totalUSDT=pair[1]['totalUSDT'], numAverage=pair[1]['numAverage'], status='SELL_ORDER')
                                                trade_order = True
                                                break
                                            elif pair[1]['status'] == 'AVERAGE_BUY_ORDER' and float(coin['a']) >= float(('{:.' + str(tick_size) + 'f}').format(float(pair[1]['buyPrice'])*(1 + (float(sell_up) + delta_perc)/100))):
                                                info_rewrite(pair[0], stepSize=pair[1]['stepSize'], tickSize=pair[1]['tickSize'], minNotional=pair[1]['minNotional'], priceChangePercent=coin['P'], askPrice=num_round(coin['a']), averagePrice=pair[1]['averagePrice'], buyPrice=pair[1]['buyPrice'], sellPrice=pair[1]['sellPrice'], trailingPrice=pair[1]['trailingPrice'], allQuantity=pair[1]['allQuantity'], free=pair[1]['free'], idOrder=pair[1]['idOrder'], profit=pair[1]['profit'], totalUSDT=pair[1]['totalUSDT'], numAverage=pair[1]['numAverage'], status=pair[1]['status'])
                                                canceled_order(pair[0], pair[1]['idOrder'], ncoi, 'BUY')
                                                trade_order = True
                                                break
                                                if float(bnb_balance) < 0.1:
                                                    for pair in tickers:
                                                        if pair['symbol'] == 'BNBUSDT':
                                                            for step in exchange:
                                                                if step['symbol'] == 'BNBUSDT' and float(bnb_balance) < 0.1:
                                                                    try:
                                                                        q = ('{:.' + str(get_count(num_round(step['filters'][2]['stepSize']))) + 'f}').format(float(num_round(step['filters'][3]['minNotional']))/float(pair['askPrice']))
                                                                        while float(q)*float(pair['askPrice']) <= float(step['filters'][3]['minNotional']):
                                                                            q = ('{:.' + str(get_count(num_round(step['filters'][2]['stepSize']))) + 'f}').format(float(q) + float(step['filters'][2]['stepSize']))
                                                                        client.order_market_buy(symbol='BNBUSDT', quantity=q)
                                                                        bnb_balance = '{:.8f}'.format(float(bnb_balance) + float(q))
                                                                        trade_order = True
                                                                        break
                                                                    except Exception as e:
                                                                        try:
                                                                            logging.error(str(extract_tb(exc_info()[2])[0][1]) + ' ' + 'Ошибка при покупке BNB: ' + q + '\n' + str(e))
                                                                            cprint('|' + str(datetime.datetime.now().strftime('%H:%M:%S')) + '| ' + str(extract_tb(exc_info()[2])[0][1]) + ' ' + colored('Ошибка при покупке BNB: ', 'cyan') + q + colored('\x1b[K\n' + str(e), 'red'), end='\r', flush=True)
                                                                        except:
                                                                            logging.error(str(e))
                                    elif float(usdt_balance) >= float(min_balance) and pair[1]['status'] == 'CANCELED_SELL_ORDER' and float(usdt_balance) > float(('{:.' + str(tick_size) + 'f}').format(float(pair[1]['allQuantity'])*(2 + multi_num_average)*float(coin['a']))):
                                        old_order_quantity = pair[1]['free']
                                        new_order_quantity = num_round(('{:.' + str(step_size) + 'f}').format(float(old_order_quantity)*(2 + multi_num_average)))
                                        usdt_balance = '{:.8f}'.format(float(usdt_balance) - float(new_order_quantity)*float(coin['a']))
                                        average_buy_price = ('{:.' + str(tick_size) + 'f}').format((float(pair[1]['averagePrice'])*float(old_order_quantity) + float(coin['a'])*float(new_order_quantity))/(float(old_order_quantity) + float(new_order_quantity)))
                                        average_sell_price = ('{:.' + str(tick_size) + 'f}').format(float(average_buy_price) + float(average_buy_price)/100*(float(sell_up) + delta_perc))
                                        info_rewrite(pair[0], stepSize=pair[1]['stepSize'], tickSize=pair[1]['tickSize'], minNotional=pair[1]['minNotional'], priceChangePercent=coin['P'], askPrice=num_round(coin['a']), averagePrice=average_buy_price, buyPrice=num_round(coin['a']), sellPrice=num_round(average_sell_price), trailingPrice=average_buy_price, allQuantity=new_order_quantity, free=pair[1]['free'], idOrder=pair[1]['idOrder'], profit=pair[1]['profit'], totalUSDT=pair[1]['totalUSDT'], numAverage=pair[1]['numAverage'], status='AVERAGE_BUY_ORDER')
                                        client.order_limit_buy(symbol=coin['s'], quantity=new_order_quantity, price=num_round(coin['a']), newClientOrderId=ncoi)
                                        trade_order = True
                                        break
                                    elif pair[1]['status'] == 'CANCELED_SELL_ORDER' and float(usdt_balance) < float(('{:.' + str(tick_size) + 'f}').format(float(pair[1]['allQuantity'])*(2 + multi_num_average)*float(coin['a']))):
                                        q = ('{:.' + str(step_size) + 'f}').format(float(pair[1]['free']))
                                        client.order_limit_sell(symbol=pair[0], quantity=q, price=pair[1]['sellPrice'], newClientOrderId=ncoi)
                                        info_rewrite(pair[0], stepSize=pair[1]['stepSize'], tickSize=pair[1]['tickSize'], minNotional=pair[1]['minNotional'], priceChangePercent=coin['P'], askPrice=num_round(coin['a']), averagePrice=pair[1]['averagePrice'], buyPrice=pair[1]['buyPrice'], sellPrice=pair[1]['sellPrice'], trailingPrice=pair[1]['trailingPrice'], allQuantity=pair[1]['free'], free=0, idOrder=pair[1]['idOrder'], profit=pair[1]['profit'], totalUSDT=pair[1]['totalUSDT'], numAverage=pair[1]['numAverage'], status='SELL_ORDER')
                                        trade_order = True
                                        break
                                    elif pair[1]['status'] == 'AVERAGE_BUY_ORDER' and float(coin['a']) >= float(('{:.' + str(tick_size) + 'f}').format(float(pair[1]['buyPrice'])*(1 + (float(sell_up) + delta_perc)/100))):
                                        info_rewrite(pair[0], stepSize=pair[1]['stepSize'], tickSize=pair[1]['tickSize'], minNotional=pair[1]['minNotional'], priceChangePercent=coin['P'], askPrice=num_round(coin['a']), averagePrice=pair[1]['averagePrice'], buyPrice=pair[1]['buyPrice'], sellPrice=pair[1]['sellPrice'], trailingPrice=pair[1]['trailingPrice'], allQuantity=pair[1]['allQuantity'], free=pair[1]['free'], idOrder=pair[1]['idOrder'], profit=pair[1]['profit'], totalUSDT=pair[1]['totalUSDT'], numAverage=pair[1]['numAverage'], status=pair[1]['status'])
                                        canceled_order(pair[0], pair[1]['idOrder'], ncoi, 'BUY')
                                        trade_order = True
                                        break
                                        if float(bnb_balance) < 0.1:
                                            for pair in tickers:
                                                if pair['symbol'] == 'BNBUSDT':
                                                    for step in exchange:
                                                        if step['symbol'] == 'BNBUSDT' and float(bnb_balance) < 0.1:
                                                            try:
                                                                q = ('{:.' + str(get_count(num_round(step['filters'][2]['stepSize']))) + 'f}').format(float(num_round(step['filters'][3]['minNotional']))/float(pair['askPrice']))
                                                                while float(q)*float(pair['askPrice']) <= float(step['filters'][3]['minNotional']):
                                                                    q = ('{:.' + str(get_count(num_round(step['filters'][2]['stepSize']))) + 'f}').format(float(q) + float(step['filters'][2]['stepSize']))
                                                                client.order_market_buy(symbol='BNBUSDT', quantity=q)
                                                                bnb_balance = '{:.8f}'.format(float(bnb_balance) + float(q))
                                                                trade_order = True
                                                                break
                                                            except Exception as e:
                                                                try:
                                                                    logging.error(str(extract_tb(exc_info()[2])[0][1]) + ' ' + 'Ошибка при покупке BNB: ' + q + '\n' + str(e))
                                                                    cprint('|' + str(datetime.datetime.now().strftime('%H:%M:%S')) + '| ' + str(extract_tb(exc_info()[2])[0][1]) + ' ' + colored('Ошибка при покупке BNB: ', 'cyan') + q + colored('\x1b[K\n' + str(e), 'red'), end='\r', flush=True)
                                                                except:
                                                                    logging.error(str(e))
                        elif pair[1]['status'] == 'BUY_ORDER' and float(coin['a']) >= float(('{:.' + str(tick_size) + 'f}').format(float(pair[1]['averagePrice'])*(1 + (float(sell_up) + delta_perc)/100))):
                            info_rewrite(pair[0], stepSize=pair[1]['stepSize'], tickSize=pair[1]['tickSize'], minNotional=pair[1]['minNotional'], priceChangePercent=coin['P'], askPrice=num_round(coin['a']), averagePrice=pair[1]['averagePrice'], buyPrice=pair[1]['buyPrice'], sellPrice=pair[1]['sellPrice'], trailingPrice=pair[1]['trailingPrice'], allQuantity=pair[1]['allQuantity'], free=pair[1]['free'], idOrder=pair[1]['idOrder'], profit=pair[1]['profit'], totalUSDT=pair[1]['totalUSDT'], numAverage=pair[1]['numAverage'], status=pair[1]['status'])
                            canceled_order(pair[0], pair[1]['idOrder'], ncoi, 'BUY')
                            trade_order = True
                            break
                        elif pair[1]['status'] == 'SELL_ORDER':
                            if float(usdt_balance) >= float(min_balance) and float(usdt_balance) > float(('{:.' + str(tick_size) + 'f}').format(float(pair[1]['allQuantity'])*(2 + multi_num_average)*float(coin['a']))) and float(coin['a']) <= float(('{:.' + str(tick_size) + 'f}').format(float(pair[1]['buyPrice']) - float(pair[1]['buyPrice'])/100*(float(pair[1]['numAverage']) + float(buy_down) - buy_down_delta))):
                                usdt_balance = '{:.8f}'.format(float(usdt_balance) - float(('{:.' + str(tick_size) + 'f}').format(float(pair[1]['allQuantity'])*(2 + multi_num_average)*float(coin['a']))))
                                canceled_order(pair[0], pair[1]['idOrder'], ncoi, 'SELL')
                                trade_order = True
                                break
                            else:
                                if trailing_sell == 'y' and float(coin['a']) >= float(pair[1]['sellPrice'])*(1 - float(trailing_percent)/100) and float(coin['b']) >= float(trailing_price):
                                    new_sell_price = pair[1]['sellPrice']
                                    while float(coin['a']) > float(new_sell_price) or float(new_sell_price) == float(pair[1]['sellPrice']):
                                        new_sell_price = ('{:.' + str(tick_size) + 'f}').format(float(new_sell_price) + float(_tick_size))
                                    info_rewrite(pair[0], stepSize=pair[1]['stepSize'], tickSize=pair[1]['tickSize'], minNotional=pair[1]['minNotional'], priceChangePercent=coin['P'], askPrice=num_round(coin['a']), averagePrice=pair[1]['averagePrice'], buyPrice=pair[1]['buyPrice'], sellPrice=new_sell_price, trailingPrice=pair[1]['trailingPrice'], allQuantity=pair[1]['allQuantity'], free=pair[1]['free'], idOrder=pair[1]['idOrder'], profit=pair[1]['profit'], totalUSDT=pair[1]['totalUSDT'], numAverage=pair[1]['numAverage'], status='TRAILING_SELL_ORDER')
                                    canceled_order(pair[0], pair[1]['idOrder'], ncoi, 'SELL')
                                    trade_order = True
                                    break
                                else:
                                    info_rewrite(pair[0], stepSize=pair[1]['stepSize'], tickSize=pair[1]['tickSize'], minNotional=pair[1]['minNotional'], priceChangePercent=coin['P'], askPrice=num_round(coin['a']), averagePrice=pair[1]['averagePrice'], buyPrice=pair[1]['buyPrice'], sellPrice=pair[1]['sellPrice'], trailingPrice=pair[1]['trailingPrice'], allQuantity=pair[1]['allQuantity'], free=pair[1]['free'], idOrder=pair[1]['idOrder'], profit=pair[1]['profit'], totalUSDT=pair[1]['totalUSDT'], numAverage=pair[1]['numAverage'], status=pair[1]['status'])
                                if pair[1]['status'] == 'TRAILING_SELL_ORDER':
                                    if float(coin['a']) >= float(pair[1]['sellPrice']):
                                        new_sell_price = pair[1]['sellPrice']
                                        while float(coin['a']) > float(new_sell_price) or float(new_sell_price) == float(pair[1]['sellPrice']):
                                            new_sell_price = num_round(('{:.' + str(tick_size) + 'f}').format(float(new_sell_price) + float(_tick_size)))
                                        new_trailing_price = pair[1]['trailingPrice'] if float(pair[1]['trailingPrice']) + float(pair[1]['trailingPrice'])/100*float(sell_up)/2 > float(new_sell_price) else num_round(('{:.' + str(tick_size) + 'f}').format(float(new_sell_price) - float(pair[1]['trailingPrice'])/100*float(sell_up)/2 + float(_tick_size)))
                                        if float(new_trailing_price) == pair[1]['trailingPrice']:
                                            new_trailing_price = num_round(('{:.' + str(tick_size) + 'f}').format(float(new_trailing_price) + float(_tick_size)))
                                        info_rewrite(pair[0], stepSize=pair[1]['stepSize'], tickSize=pair[1]['tickSize'], minNotional=pair[1]['minNotional'], priceChangePercent=coin['P'], askPrice=num_round(coin['a']), averagePrice=pair[1]['averagePrice'], buyPrice=pair[1]['buyPrice'], sellPrice=new_sell_price, trailingPrice=new_trailing_price, allQuantity=pair[1]['allQuantity'], free=pair[1]['free'], idOrder=pair[1]['idOrder'], profit=pair[1]['profit'], totalUSDT=pair[1]['totalUSDT'], numAverage=pair[1]['numAverage'], status=pair[1]['status'])
                                    else:
                                        if float(coin['a']) < float(pair[1]['sellPrice'])*(1 - float(trailing_percent)/100):
                                            new_sell_price = num_round(('{:.' + str(tick_size) + 'f}').format(float(pair[1]['sellPrice']) - float(_tick_size)))
                                            q = num_round(('{:.' + str(step_size) + 'f}').format(float(pair[1]['minNotional'])/float(coin['b'])))
                                            while float(pair[1]['minNotional']) > float(q)*float(coin['b']):
                                                q = num_round(('{:.' + str(step_size) + 'f}').format(float(q) + float(_step_size)))
                                            if ((float(pair[1]['allQuantity']) - float(q))*float(pair[1]['trailingPrice']) > float(pair[1]['minNotional']) or float(pair[1]['allQuantity']) - float(q) > float(q)*(1 + multi_num_average)) and float(coin['b']) > float(pair[1]['trailingPrice']):
                                                try:
                                                    client.order_market_sell(symbol=pair[0], quantity=q, newClientOrderId=ncoim)
                                                    trade_order = True
                                                    break
                                                except Exception as e:
                                                    try:
                                                        logging.error(str(extract_tb(exc_info()[2])[0][1]) + ' ' + pair[0] + ' ' + coin['b'] + ' ' + coin['B'] + ' ' + q + '\n' + str(e))
                                                    except:
                                                        logging.error(str(e))
                                                    time.sleep(5)
                                            elif ((float(pair[1]['allQuantity']) - float(q))*float(pair[1]['averagePrice']) <= float(pair[1]['minNotional']) or float(coin['b']) <= float(pair[1]['trailingPrice']) or float(pair[1]['allQuantity']) - float(q) <= float(q)*(1 + multi_num_average)) and float(coin['b']) >= float(pair[1]['averagePrice']):
                                                try:
                                                    client.order_market_sell(symbol=pair[0], quantity=pair[1]['allQuantity'], newClientOrderId=ncoi)
                                                    trade_order = True
                                                    break
                                                except Exception as e:
                                                    try:
                                                        logging.error(str(extract_tb(exc_info()[2])[0][1]) + ' ' + pair[0] + ' ' + coin['b'] + ' ' + coin['B'] + ' ' + pair[1]['allQuantity'] + '\n' + str(e))
                                                    except:
                                                        logging.error(str(e))
                                                    time.sleep(5)
                                            elif float(usdt_balance) > float(('{:.' + str(tick_size) + 'f}').format(float(pair[1]['allQuantity'])*(2 + multi_num_average)*float(coin['a']))) and float(coin['a']) <= float(('{:.' + str(tick_size) + 'f}').format(float(pair[1]['buyPrice']) - float(pair[1]['buyPrice'])/100*(float(buy_down) - buy_down_delta))):
                                                info_rewrite(pair[0], stepSize=pair[1]['stepSize'], tickSize=pair[1]['tickSize'], minNotional=pair[1]['minNotional'], priceChangePercent=coin['P'], askPrice=num_round(coin['a']), averagePrice=pair[1]['averagePrice'], buyPrice=pair[1]['buyPrice'], sellPrice=pair[1]['sellPrice'], trailingPrice=pair[1]['trailingPrice'], allQuantity=pair[1]['allQuantity'], free=pair[1]['allQuantity'], idOrder=pair[1]['idOrder'], profit=pair[1]['profit'], totalUSDT=pair[1]['totalUSDT'], numAverage=pair[1]['numAverage'], status='CANCELED_SELL_ORDER')
                                                break
                                            else:
                                                info_rewrite(pair[0], stepSize=pair[1]['stepSize'], tickSize=pair[1]['tickSize'], minNotional=pair[1]['minNotional'], priceChangePercent=coin['P'], askPrice=num_round(coin['a']), averagePrice=pair[1]['averagePrice'], buyPrice=pair[1]['buyPrice'], sellPrice=pair[1]['sellPrice'], trailingPrice=pair[1]['trailingPrice'], allQuantity=pair[1]['allQuantity'], free=pair[1]['free'], idOrder=pair[1]['idOrder'], profit=pair[1]['profit'], totalUSDT=pair[1]['totalUSDT'], numAverage=pair[1]['numAverage'], status=pair[1]['status'])
                                        else:
                                            info_rewrite(pair[0], stepSize=pair[1]['stepSize'], tickSize=pair[1]['tickSize'], minNotional=pair[1]['minNotional'], priceChangePercent=coin['P'], askPrice=num_round(coin['a']), averagePrice=pair[1]['averagePrice'], buyPrice=pair[1]['buyPrice'], sellPrice=pair[1]['sellPrice'], trailingPrice=pair[1]['trailingPrice'], allQuantity=pair[1]['allQuantity'], free=pair[1]['free'], idOrder=pair[1]['idOrder'], profit=pair[1]['profit'], totalUSDT=pair[1]['totalUSDT'], numAverage=pair[1]['numAverage'], status=pair[1]['status'])
                                        if float(usdt_balance) >= float(min_balance) and pair[1]['status'] == 'CANCELED_SELL_ORDER' and float(usdt_balance) > float(('{:.' + str(tick_size) + 'f}').format(float(pair[1]['allQuantity'])*(2 + multi_num_average)*float(coin['a']))):
                                            old_order_quantity = pair[1]['free']
                                            new_order_quantity = num_round(('{:.' + str(step_size) + 'f}').format(float(old_order_quantity)*(2 + multi_num_average)))
                                            usdt_balance = '{:.8f}'.format(float(usdt_balance) - float(new_order_quantity)*float(coin['a']))
                                            average_buy_price = ('{:.' + str(tick_size) + 'f}').format((float(pair[1]['averagePrice'])*float(old_order_quantity) + float(coin['a'])*float(new_order_quantity))/(float(old_order_quantity) + float(new_order_quantity)))
                                            average_sell_price = ('{:.' + str(tick_size) + 'f}').format(float(average_buy_price) + float(average_buy_price)/100*(float(sell_up) + delta_perc))
                                            info_rewrite(pair[0], stepSize=pair[1]['stepSize'], tickSize=pair[1]['tickSize'], minNotional=pair[1]['minNotional'], priceChangePercent=coin['P'], askPrice=num_round(coin['a']), averagePrice=average_buy_price, buyPrice=num_round(coin['a']), sellPrice=num_round(average_sell_price), trailingPrice=average_buy_price, allQuantity=new_order_quantity, free=pair[1]['free'], idOrder=pair[1]['idOrder'], profit=pair[1]['profit'], totalUSDT=pair[1]['totalUSDT'], numAverage=pair[1]['numAverage'], status='AVERAGE_BUY_ORDER')
                                            client.order_limit_buy(symbol=coin['s'], quantity=new_order_quantity, price=num_round(coin['a']), newClientOrderId=ncoi)
                                            trade_order = True
                                            break
                                        elif pair[1]['status'] == 'CANCELED_SELL_ORDER' and float(usdt_balance) < float(('{:.' + str(tick_size) + 'f}').format(float(pair[1]['allQuantity'])*(2 + multi_num_average)*float(coin['a']))):
                                            q = ('{:.' + str(step_size) + 'f}').format(float(pair[1]['free']))
                                            client.order_limit_sell(symbol=pair[0], quantity=q, price=pair[1]['sellPrice'], newClientOrderId=ncoi)
                                            info_rewrite(pair[0], stepSize=pair[1]['stepSize'], tickSize=pair[1]['tickSize'], minNotional=pair[1]['minNotional'], priceChangePercent=coin['P'], askPrice=num_round(coin['a']), averagePrice=pair[1]['averagePrice'], buyPrice=pair[1]['buyPrice'], sellPrice=pair[1]['sellPrice'], trailingPrice=pair[1]['trailingPrice'], allQuantity=pair[1]['free'], free=0, idOrder=pair[1]['idOrder'], profit=pair[1]['profit'], totalUSDT=pair[1]['totalUSDT'], numAverage=pair[1]['numAverage'], status='SELL_ORDER')
                                            trade_order = True
                                            break
                                        elif pair[1]['status'] == 'AVERAGE_BUY_ORDER' and float(coin['a']) >= float(('{:.' + str(tick_size) + 'f}').format(float(pair[1]['buyPrice'])*(1 + (float(sell_up) + delta_perc)/100))):
                                            info_rewrite(pair[0], stepSize=pair[1]['stepSize'], tickSize=pair[1]['tickSize'], minNotional=pair[1]['minNotional'], priceChangePercent=coin['P'], askPrice=num_round(coin['a']), averagePrice=pair[1]['averagePrice'], buyPrice=pair[1]['buyPrice'], sellPrice=pair[1]['sellPrice'], trailingPrice=pair[1]['trailingPrice'], allQuantity=pair[1]['allQuantity'], free=pair[1]['free'], idOrder=pair[1]['idOrder'], profit=pair[1]['profit'], totalUSDT=pair[1]['totalUSDT'], numAverage=pair[1]['numAverage'], status=pair[1]['status'])
                                            canceled_order(pair[0], pair[1]['idOrder'], ncoi, 'BUY')
                                            trade_order = True
                                            break
                                            if float(bnb_balance) < 0.1:
                                                for pair in tickers:
                                                    if pair['symbol'] == 'BNBUSDT':
                                                        for step in exchange:
                                                            if step['symbol'] == 'BNBUSDT' and float(bnb_balance) < 0.1:
                                                                try:
                                                                    q = ('{:.' + str(get_count(num_round(step['filters'][2]['stepSize']))) + 'f}').format(float(num_round(step['filters'][3]['minNotional']))/float(pair['askPrice']))
                                                                    while float(q)*float(pair['askPrice']) <= float(step['filters'][3]['minNotional']):
                                                                        q = ('{:.' + str(get_count(num_round(step['filters'][2]['stepSize']))) + 'f}').format(float(q) + float(step['filters'][2]['stepSize']))
                                                                    client.order_market_buy(symbol='BNBUSDT', quantity=q)
                                                                    bnb_balance = '{:.8f}'.format(float(bnb_balance) + float(q))
                                                                    trade_order = True
                                                                    break
                                                                except Exception as e:
                                                                    try:
                                                                        logging.error(str(extract_tb(exc_info()[2])[0][1]) + ' ' + 'Ошибка при покупке BNB: ' + q + '\n' + str(e))
                                                                        cprint('|' + str(datetime.datetime.now().strftime('%H:%M:%S')) + '| ' + str(extract_tb(exc_info()[2])[0][1]) + ' ' + colored('Ошибка при покупке BNB: ', 'cyan') + q + colored('\x1b[K\n' + str(e), 'red'), end='\r', flush=True)
                                                                    except:
                                                                        logging.error(str(e))
                                elif float(usdt_balance) >= float(min_balance) and pair[1]['status'] == 'CANCELED_SELL_ORDER' and float(usdt_balance) > float(('{:.' + str(tick_size) + 'f}').format(float(pair[1]['allQuantity'])*(2 + multi_num_average)*float(coin['a']))):
                                    old_order_quantity = pair[1]['free']
                                    new_order_quantity = num_round(('{:.' + str(step_size) + 'f}').format(float(old_order_quantity)*(2 + multi_num_average)))
                                    usdt_balance = '{:.8f}'.format(float(usdt_balance) - float(new_order_quantity)*float(coin['a']))
                                    average_buy_price = ('{:.' + str(tick_size) + 'f}').format((float(pair[1]['averagePrice'])*float(old_order_quantity) + float(coin['a'])*float(new_order_quantity))/(float(old_order_quantity) + float(new_order_quantity)))
                                    average_sell_price = ('{:.' + str(tick_size) + 'f}').format(float(average_buy_price) + float(average_buy_price)/100*(float(sell_up) + delta_perc))
                                    info_rewrite(pair[0], stepSize=pair[1]['stepSize'], tickSize=pair[1]['tickSize'], minNotional=pair[1]['minNotional'], priceChangePercent=coin['P'], askPrice=num_round(coin['a']), averagePrice=average_buy_price, buyPrice=num_round(coin['a']), sellPrice=num_round(average_sell_price), trailingPrice=average_buy_price, allQuantity=new_order_quantity, free=pair[1]['free'], idOrder=pair[1]['idOrder'], profit=pair[1]['profit'], totalUSDT=pair[1]['totalUSDT'], numAverage=pair[1]['numAverage'], status='AVERAGE_BUY_ORDER')
                                    client.order_limit_buy(symbol=coin['s'], quantity=new_order_quantity, price=num_round(coin['a']), newClientOrderId=ncoi)
                                    trade_order = True
                                    break
                                elif pair[1]['status'] == 'CANCELED_SELL_ORDER' and float(usdt_balance) < float(('{:.' + str(tick_size) + 'f}').format(float(pair[1]['allQuantity'])*(2 + multi_num_average)*float(coin['a']))):
                                    q = ('{:.' + str(step_size) + 'f}').format(float(pair[1]['free']))
                                    client.order_limit_sell(symbol=pair[0], quantity=q, price=pair[1]['sellPrice'], newClientOrderId=ncoi)
                                    info_rewrite(pair[0], stepSize=pair[1]['stepSize'], tickSize=pair[1]['tickSize'], minNotional=pair[1]['minNotional'], priceChangePercent=coin['P'], askPrice=num_round(coin['a']), averagePrice=pair[1]['averagePrice'], buyPrice=pair[1]['buyPrice'], sellPrice=pair[1]['sellPrice'], trailingPrice=pair[1]['trailingPrice'], allQuantity=pair[1]['free'], free=0, idOrder=pair[1]['idOrder'], profit=pair[1]['profit'], totalUSDT=pair[1]['totalUSDT'], numAverage=pair[1]['numAverage'], status='SELL_ORDER')
                                    trade_order = True
                                    break
                                elif pair[1]['status'] == 'AVERAGE_BUY_ORDER' and float(coin['a']) >= float(('{:.' + str(tick_size) + 'f}').format(float(pair[1]['buyPrice'])*(1 + (float(sell_up) + delta_perc)/100))):
                                    info_rewrite(pair[0], stepSize=pair[1]['stepSize'], tickSize=pair[1]['tickSize'], minNotional=pair[1]['minNotional'], priceChangePercent=coin['P'], askPrice=num_round(coin['a']), averagePrice=pair[1]['averagePrice'], buyPrice=pair[1]['buyPrice'], sellPrice=pair[1]['sellPrice'], trailingPrice=pair[1]['trailingPrice'], allQuantity=pair[1]['allQuantity'], free=pair[1]['free'], idOrder=pair[1]['idOrder'], profit=pair[1]['profit'], totalUSDT=pair[1]['totalUSDT'], numAverage=pair[1]['numAverage'], status=pair[1]['status'])
                                    canceled_order(pair[0], pair[1]['idOrder'], ncoi, 'BUY')
                                    trade_order = True
                                    break
                                    if float(bnb_balance) < 0.1:
                                        for pair in tickers:
                                            if pair['symbol'] == 'BNBUSDT':
                                                for step in exchange:
                                                    if step['symbol'] == 'BNBUSDT' and float(bnb_balance) < 0.1:
                                                        try:
                                                            q = ('{:.' + str(get_count(num_round(step['filters'][2]['stepSize']))) + 'f}').format(float(num_round(step['filters'][3]['minNotional']))/float(pair['askPrice']))
                                                            while float(q)*float(pair['askPrice']) <= float(step['filters'][3]['minNotional']):
                                                                q = ('{:.' + str(get_count(num_round(step['filters'][2]['stepSize']))) + 'f}').format(float(q) + float(step['filters'][2]['stepSize']))
                                                            client.order_market_buy(symbol='BNBUSDT', quantity=q)
                                                            bnb_balance = '{:.8f}'.format(float(bnb_balance) + float(q))
                                                            trade_order = True
                                                            break
                                                        except Exception as e:
                                                            try:
                                                                logging.error(str(extract_tb(exc_info()[2])[0][1]) + ' ' + 'Ошибка при покупке BNB: ' + q + '\n' + str(e))
                                                                cprint('|' + str(datetime.datetime.now().strftime('%H:%M:%S')) + '| ' + str(extract_tb(exc_info()[2])[0][1]) + ' ' + colored('Ошибка при покупке BNB: ', 'cyan') + q + colored('\x1b[K\n' + str(e), 'red'), end='\r', flush=True)
                                                            except:
                                                                logging.error(str(e))
                        elif pair[1]['status'] == 'TRAILING_SELL_ORDER':
                            if float(coin['a']) >= float(pair[1]['sellPrice']):
                                new_sell_price = pair[1]['sellPrice']
                                while float(coin['a']) > float(new_sell_price) or float(new_sell_price) == float(pair[1]['sellPrice']):
                                    new_sell_price = num_round(('{:.' + str(tick_size) + 'f}').format(float(new_sell_price) + float(_tick_size)))
                                new_trailing_price = pair[1]['trailingPrice'] if float(pair[1]['trailingPrice']) + float(pair[1]['trailingPrice'])/100*float(sell_up)/2 > float(new_sell_price) else num_round(('{:.' + str(tick_size) + 'f}').format(float(new_sell_price) - float(pair[1]['trailingPrice'])/100*float(sell_up)/2 + float(_tick_size)))
                                if float(new_trailing_price) == pair[1]['trailingPrice']:
                                    new_trailing_price = num_round(('{:.' + str(tick_size) + 'f}').format(float(new_trailing_price) + float(_tick_size)))
                                info_rewrite(pair[0], stepSize=pair[1]['stepSize'], tickSize=pair[1]['tickSize'], minNotional=pair[1]['minNotional'], priceChangePercent=coin['P'], askPrice=num_round(coin['a']), averagePrice=pair[1]['averagePrice'], buyPrice=pair[1]['buyPrice'], sellPrice=new_sell_price, trailingPrice=new_trailing_price, allQuantity=pair[1]['allQuantity'], free=pair[1]['free'], idOrder=pair[1]['idOrder'], profit=pair[1]['profit'], totalUSDT=pair[1]['totalUSDT'], numAverage=pair[1]['numAverage'], status=pair[1]['status'])
                            else:
                                if float(coin['a']) < float(pair[1]['sellPrice'])*(1 - float(trailing_percent)/100):
                                    new_sell_price = num_round(('{:.' + str(tick_size) + 'f}').format(float(pair[1]['sellPrice']) - float(_tick_size)))
                                    q = num_round(('{:.' + str(step_size) + 'f}').format(float(pair[1]['minNotional'])/float(coin['b'])))
                                    while float(pair[1]['minNotional']) > float(q)*float(coin['b']):
                                        q = num_round(('{:.' + str(step_size) + 'f}').format(float(q) + float(_step_size)))
                                    if ((float(pair[1]['allQuantity']) - float(q))*float(pair[1]['trailingPrice']) > float(pair[1]['minNotional']) or float(pair[1]['allQuantity']) - float(q) > float(q)*(1 + multi_num_average)) and float(coin['b']) > float(pair[1]['trailingPrice']):
                                        try:
                                            client.order_market_sell(symbol=pair[0], quantity=q, newClientOrderId=ncoim)
                                            trade_order = True
                                            break
                                        except Exception as e:
                                            try:
                                                logging.error(str(extract_tb(exc_info()[2])[0][1]) + ' ' + pair[0] + ' ' + coin['b'] + ' ' + coin['B'] + ' ' + q + '\n' + str(e))
                                            except:
                                                logging.error(str(e))
                                            time.sleep(5)
                                    elif ((float(pair[1]['allQuantity']) - float(q))*float(pair[1]['averagePrice']) <= float(pair[1]['minNotional']) or float(coin['b']) <= float(pair[1]['trailingPrice']) or float(pair[1]['allQuantity']) - float(q) <= float(q)*(1 + multi_num_average)) and float(coin['b']) >= float(pair[1]['averagePrice']):
                                        try:
                                            client.order_market_sell(symbol=pair[0], quantity=pair[1]['allQuantity'], newClientOrderId=ncoi)
                                            trade_order = True
                                            break
                                        except Exception as e:
                                            try:
                                                logging.error(str(extract_tb(exc_info()[2])[0][1]) + ' ' + pair[0] + ' ' + coin['b'] + ' ' + coin['B'] + ' ' + pair[1]['allQuantity'] + '\n' + str(e))
                                            except:
                                                logging.error(str(e))
                                            time.sleep(5)
                                    elif float(usdt_balance) > float(('{:.' + str(tick_size) + 'f}').format(float(pair[1]['allQuantity'])*(2 + multi_num_average)*float(coin['a']))) and float(coin['a']) <= float(('{:.' + str(tick_size) + 'f}').format(float(pair[1]['buyPrice']) - float(pair[1]['buyPrice'])/100*(float(buy_down) - buy_down_delta))):
                                        info_rewrite(pair[0], stepSize=pair[1]['stepSize'], tickSize=pair[1]['tickSize'], minNotional=pair[1]['minNotional'], priceChangePercent=coin['P'], askPrice=num_round(coin['a']), averagePrice=pair[1]['averagePrice'], buyPrice=pair[1]['buyPrice'], sellPrice=pair[1]['sellPrice'], trailingPrice=pair[1]['trailingPrice'], allQuantity=pair[1]['allQuantity'], free=pair[1]['allQuantity'], idOrder=pair[1]['idOrder'], profit=pair[1]['profit'], totalUSDT=pair[1]['totalUSDT'], numAverage=pair[1]['numAverage'], status='CANCELED_SELL_ORDER')
                                        break
                                    else:
                                        info_rewrite(pair[0], stepSize=pair[1]['stepSize'], tickSize=pair[1]['tickSize'], minNotional=pair[1]['minNotional'], priceChangePercent=coin['P'], askPrice=num_round(coin['a']), averagePrice=pair[1]['averagePrice'], buyPrice=pair[1]['buyPrice'], sellPrice=pair[1]['sellPrice'], trailingPrice=pair[1]['trailingPrice'], allQuantity=pair[1]['allQuantity'], free=pair[1]['free'], idOrder=pair[1]['idOrder'], profit=pair[1]['profit'], totalUSDT=pair[1]['totalUSDT'], numAverage=pair[1]['numAverage'], status=pair[1]['status'])
                                else:
                                    info_rewrite(pair[0], stepSize=pair[1]['stepSize'], tickSize=pair[1]['tickSize'], minNotional=pair[1]['minNotional'], priceChangePercent=coin['P'], askPrice=num_round(coin['a']), averagePrice=pair[1]['averagePrice'], buyPrice=pair[1]['buyPrice'], sellPrice=pair[1]['sellPrice'], trailingPrice=pair[1]['trailingPrice'], allQuantity=pair[1]['allQuantity'], free=pair[1]['free'], idOrder=pair[1]['idOrder'], profit=pair[1]['profit'], totalUSDT=pair[1]['totalUSDT'], numAverage=pair[1]['numAverage'], status=pair[1]['status'])
                                if float(usdt_balance) >= float(min_balance) and pair[1]['status'] == 'CANCELED_SELL_ORDER' and float(usdt_balance) > float(('{:.' + str(tick_size) + 'f}').format(float(pair[1]['allQuantity'])*(2 + multi_num_average)*float(coin['a']))):
                                    old_order_quantity = pair[1]['free']
                                    new_order_quantity = num_round(('{:.' + str(step_size) + 'f}').format(float(old_order_quantity)*(2 + multi_num_average)))
                                    usdt_balance = '{:.8f}'.format(float(usdt_balance) - float(new_order_quantity)*float(coin['a']))
                                    average_buy_price = ('{:.' + str(tick_size) + 'f}').format((float(pair[1]['averagePrice'])*float(old_order_quantity) + float(coin['a'])*float(new_order_quantity))/(float(old_order_quantity) + float(new_order_quantity)))
                                    average_sell_price = ('{:.' + str(tick_size) + 'f}').format(float(average_buy_price) + float(average_buy_price)/100*(float(sell_up) + delta_perc))
                                    info_rewrite(pair[0], stepSize=pair[1]['stepSize'], tickSize=pair[1]['tickSize'], minNotional=pair[1]['minNotional'], priceChangePercent=coin['P'], askPrice=num_round(coin['a']), averagePrice=average_buy_price, buyPrice=num_round(coin['a']), sellPrice=num_round(average_sell_price), trailingPrice=average_buy_price, allQuantity=new_order_quantity, free=pair[1]['free'], idOrder=pair[1]['idOrder'], profit=pair[1]['profit'], totalUSDT=pair[1]['totalUSDT'], numAverage=pair[1]['numAverage'], status='AVERAGE_BUY_ORDER')
                                    client.order_limit_buy(symbol=coin['s'], quantity=new_order_quantity, price=num_round(coin['a']), newClientOrderId=ncoi)
                                    trade_order = True
                                    break
                                elif pair[1]['status'] == 'CANCELED_SELL_ORDER' and float(usdt_balance) < float(('{:.' + str(tick_size) + 'f}').format(float(pair[1]['allQuantity'])*(2 + multi_num_average)*float(coin['a']))):
                                    q = ('{:.' + str(step_size) + 'f}').format(float(pair[1]['free']))
                                    client.order_limit_sell(symbol=pair[0], quantity=q, price=pair[1]['sellPrice'], newClientOrderId=ncoi)
                                    info_rewrite(pair[0], stepSize=pair[1]['stepSize'], tickSize=pair[1]['tickSize'], minNotional=pair[1]['minNotional'], priceChangePercent=coin['P'], askPrice=num_round(coin['a']), averagePrice=pair[1]['averagePrice'], buyPrice=pair[1]['buyPrice'], sellPrice=pair[1]['sellPrice'], trailingPrice=pair[1]['trailingPrice'], allQuantity=pair[1]['free'], free=0, idOrder=pair[1]['idOrder'], profit=pair[1]['profit'], totalUSDT=pair[1]['totalUSDT'], numAverage=pair[1]['numAverage'], status='SELL_ORDER')
                                    trade_order = True
                                    break
                                elif pair[1]['status'] == 'AVERAGE_BUY_ORDER' and float(coin['a']) >= float(('{:.' + str(tick_size) + 'f}').format(float(pair[1]['buyPrice'])*(1 + (float(sell_up) + delta_perc)/100))):
                                    info_rewrite(pair[0], stepSize=pair[1]['stepSize'], tickSize=pair[1]['tickSize'], minNotional=pair[1]['minNotional'], priceChangePercent=coin['P'], askPrice=num_round(coin['a']), averagePrice=pair[1]['averagePrice'], buyPrice=pair[1]['buyPrice'], sellPrice=pair[1]['sellPrice'], trailingPrice=pair[1]['trailingPrice'], allQuantity=pair[1]['allQuantity'], free=pair[1]['free'], idOrder=pair[1]['idOrder'], profit=pair[1]['profit'], totalUSDT=pair[1]['totalUSDT'], numAverage=pair[1]['numAverage'], status=pair[1]['status'])
                                    canceled_order(pair[0], pair[1]['idOrder'], ncoi, 'BUY')
                                    trade_order = True
                                    break
                                    if float(bnb_balance) < 0.1:
                                        for pair in tickers:
                                            if pair['symbol'] == 'BNBUSDT':
                                                for step in exchange:
                                                    if step['symbol'] == 'BNBUSDT' and float(bnb_balance) < 0.1:
                                                        try:
                                                            q = ('{:.' + str(get_count(num_round(step['filters'][2]['stepSize']))) + 'f}').format(float(num_round(step['filters'][3]['minNotional']))/float(pair['askPrice']))
                                                            while float(q)*float(pair['askPrice']) <= float(step['filters'][3]['minNotional']):
                                                                q = ('{:.' + str(get_count(num_round(step['filters'][2]['stepSize']))) + 'f}').format(float(q) + float(step['filters'][2]['stepSize']))
                                                            client.order_market_buy(symbol='BNBUSDT', quantity=q)
                                                            bnb_balance = '{:.8f}'.format(float(bnb_balance) + float(q))
                                                            trade_order = True
                                                            break
                                                        except Exception as e:
                                                            try:
                                                                logging.error(str(extract_tb(exc_info()[2])[0][1]) + ' ' + 'Ошибка при покупке BNB: ' + q + '\n' + str(e))
                                                                cprint('|' + str(datetime.datetime.now().strftime('%H:%M:%S')) + '| ' + str(extract_tb(exc_info()[2])[0][1]) + ' ' + colored('Ошибка при покупке BNB: ', 'cyan') + q + colored('\x1b[K\n' + str(e), 'red'), end='\r', flush=True)
                                                            except:
                                                                logging.error(str(e))
                        elif float(usdt_balance) >= float(min_balance) and pair[1]['status'] == 'CANCELED_SELL_ORDER' and float(usdt_balance) > float(('{:.' + str(tick_size) + 'f}').format(float(pair[1]['allQuantity'])*(2 + multi_num_average)*float(coin['a']))):
                            old_order_quantity = pair[1]['free']
                            new_order_quantity = num_round(('{:.' + str(step_size) + 'f}').format(float(old_order_quantity)*(2 + multi_num_average)))
                            usdt_balance = '{:.8f}'.format(float(usdt_balance) - float(new_order_quantity)*float(coin['a']))
                            average_buy_price = ('{:.' + str(tick_size) + 'f}').format((float(pair[1]['averagePrice'])*float(old_order_quantity) + float(coin['a'])*float(new_order_quantity))/(float(old_order_quantity) + float(new_order_quantity)))
                            average_sell_price = ('{:.' + str(tick_size) + 'f}').format(float(average_buy_price) + float(average_buy_price)/100*(float(sell_up) + delta_perc))
                            info_rewrite(pair[0], stepSize=pair[1]['stepSize'], tickSize=pair[1]['tickSize'], minNotional=pair[1]['minNotional'], priceChangePercent=coin['P'], askPrice=num_round(coin['a']), averagePrice=average_buy_price, buyPrice=num_round(coin['a']), sellPrice=num_round(average_sell_price), trailingPrice=average_buy_price, allQuantity=new_order_quantity, free=pair[1]['free'], idOrder=pair[1]['idOrder'], profit=pair[1]['profit'], totalUSDT=pair[1]['totalUSDT'], numAverage=pair[1]['numAverage'], status='AVERAGE_BUY_ORDER')
                            client.order_limit_buy(symbol=coin['s'], quantity=new_order_quantity, price=num_round(coin['a']), newClientOrderId=ncoi)
                            trade_order = True
                            break
                        elif pair[1]['status'] == 'CANCELED_SELL_ORDER' and float(usdt_balance) < float(('{:.' + str(tick_size) + 'f}').format(float(pair[1]['allQuantity'])*(2 + multi_num_average)*float(coin['a']))):
                            q = ('{:.' + str(step_size) + 'f}').format(float(pair[1]['free']))
                            client.order_limit_sell(symbol=pair[0], quantity=q, price=pair[1]['sellPrice'], newClientOrderId=ncoi)
                            info_rewrite(pair[0], stepSize=pair[1]['stepSize'], tickSize=pair[1]['tickSize'], minNotional=pair[1]['minNotional'], priceChangePercent=coin['P'], askPrice=num_round(coin['a']), averagePrice=pair[1]['averagePrice'], buyPrice=pair[1]['buyPrice'], sellPrice=pair[1]['sellPrice'], trailingPrice=pair[1]['trailingPrice'], allQuantity=pair[1]['free'], free=0, idOrder=pair[1]['idOrder'], profit=pair[1]['profit'], totalUSDT=pair[1]['totalUSDT'], numAverage=pair[1]['numAverage'], status='SELL_ORDER')
                            trade_order = True
                            break
                        elif pair[1]['status'] == 'AVERAGE_BUY_ORDER' and float(coin['a']) >= float(('{:.' + str(tick_size) + 'f}').format(float(pair[1]['buyPrice'])*(1 + (float(sell_up) + delta_perc)/100))):
                            info_rewrite(pair[0], stepSize=pair[1]['stepSize'], tickSize=pair[1]['tickSize'], minNotional=pair[1]['minNotional'], priceChangePercent=coin['P'], askPrice=num_round(coin['a']), averagePrice=pair[1]['averagePrice'], buyPrice=pair[1]['buyPrice'], sellPrice=pair[1]['sellPrice'], trailingPrice=pair[1]['trailingPrice'], allQuantity=pair[1]['allQuantity'], free=pair[1]['free'], idOrder=pair[1]['idOrder'], profit=pair[1]['profit'], totalUSDT=pair[1]['totalUSDT'], numAverage=pair[1]['numAverage'], status=pair[1]['status'])
                            canceled_order(pair[0], pair[1]['idOrder'], ncoi, 'BUY')
                            trade_order = True
                            break
                            if float(bnb_balance) < 0.1:
                                for pair in tickers:
                                    if pair['symbol'] == 'BNBUSDT':
                                        for step in exchange:
                                            if step['symbol'] == 'BNBUSDT' and float(bnb_balance) < 0.1:
                                                try:
                                                    q = ('{:.' + str(get_count(num_round(step['filters'][2]['stepSize']))) + 'f}').format(float(num_round(step['filters'][3]['minNotional']))/float(pair['askPrice']))
                                                    while float(q)*float(pair['askPrice']) <= float(step['filters'][3]['minNotional']):
                                                        q = ('{:.' + str(get_count(num_round(step['filters'][2]['stepSize']))) + 'f}').format(float(q) + float(step['filters'][2]['stepSize']))
                                                    client.order_market_buy(symbol='BNBUSDT', quantity=q)
                                                    bnb_balance = '{:.8f}'.format(float(bnb_balance) + float(q))
                                                    trade_order = True
                                                    break
                                                except Exception as e:
                                                    try:
                                                        logging.error(str(extract_tb(exc_info()[2])[0][1]) + ' ' + 'Ошибка при покупке BNB: ' + q + '\n' + str(e))
                                                        cprint('|' + str(datetime.datetime.now().strftime('%H:%M:%S')) + '| ' + str(extract_tb(exc_info()[2])[0][1]) + ' ' + colored('Ошибка при покупке BNB: ', 'cyan') + q + colored('\x1b[K\n' + str(e), 'red'), end='\r', flush=True)
                                                    except:
                                                        logging.error(str(e))
                    elif float(bnb_balance) < 0.1:
                        for pair in tickers:
                            if pair['symbol'] == 'BNBUSDT':
                                for step in exchange:
                                    if step['symbol'] == 'BNBUSDT' and float(bnb_balance) < 0.1:
                                        try:
                                            q = ('{:.' + str(get_count(num_round(step['filters'][2]['stepSize']))) + 'f}').format(float(num_round(step['filters'][3]['minNotional']))/float(pair['askPrice']))
                                            while float(q)*float(pair['askPrice']) <= float(step['filters'][3]['minNotional']):
                                                q = ('{:.' + str(get_count(num_round(step['filters'][2]['stepSize']))) + 'f}').format(float(q) + float(step['filters'][2]['stepSize']))
                                            client.order_market_buy(symbol='BNBUSDT', quantity=q)
                                            bnb_balance = '{:.8f}'.format(float(bnb_balance) + float(q))
                                            trade_order = True
                                            break
                                        except Exception as e:
                                            try:
                                                logging.error(str(extract_tb(exc_info()[2])[0][1]) + ' ' + 'Ошибка при покупке BNB: ' + q + '\n' + str(e))
                                                cprint('|' + str(datetime.datetime.now().strftime('%H:%M:%S')) + '| ' + str(extract_tb(exc_info()[2])[0][1]) + ' ' + colored('Ошибка при покупке BNB: ', 'cyan') + q + colored('\x1b[K\n' + str(e), 'red'), end='\r', flush=True)
                                            except:
                                                logging.error(str(e))
                if trade_order == True:
                    break
        except Exception as e:
            try:
                logging.error(str(extract_tb(exc_info()[2])[0][1]) + ' ' + coin['s'] + '\n' + str(e))
                if str(e.__dict__['code']) == '-1003':
                    time.sleep(60)
            except:
                logging.error(str(e))
        try:
            if float(bnb_balance) >= 0.1:
                spinner_delta_color = 'red' if spinner_delta > info_delta else 'green'
                upd_spinner_delta_color = 'yellow' if spinner_delta == info_delta else spinner_delta_color
                row_delta = '↓' if spinner_delta > info_delta else '↑'
                upd_row_delta = '' if spinner_delta == info_delta else row_delta
                spinner_delta = info_delta
                sync_time = [time.time() - float(times['E'])/1000 for times in msg_sp if times['s'] in data_base.keys()]
                sync_time = sum(sync_time)/len(sync_time)
                sync_times_color = 'green' if sync_time <= 3 else 'yellow'
                sync_times_color = 'red' if sync_time >= 10 else sync_times_color
                sync_times = colored('•', sync_times_color) + ' '
                best_coin = sorted([pair for pair in data_base.items() if pair[0] not in system_key and float(pair[1]['sellPrice']) != 0 and float(pair[1]['askPrice']) != 0], key=lambda pair: float(pair[1]['sellPrice'])/float(pair[1]['askPrice']), reverse=False)
                best_coin_name = '' if len(best_coin) == 0 else ' | ' + colored('Л: ', 'cyan') + colored(best_coin[0][0].replace('USDT', ''), 'yellow') + ' ' + colored(num_round('{:.2f}'.format((float(best_coin[0][1]['sellPrice'])/float(best_coin[0][1]['askPrice']) - 1)*100)) + '%', 'yellow') + colored(' (' + best_coin[0][1]['sellPrice'] + ' USDT)', 'yellow')
                auto_trade = colored('М: ', 'cyan') + colored(num_round(max_trade_pairs), 'yellow') + ' | ' if auto_trade_pairs == 'y' and float(max_trade_pairs) >= 0 else ''
                cprint('|' + str(datetime.datetime.now().strftime('%H:%M:%S')) + '| ' + sync_times + auto_trade + colored('П: ' + colored(num_round('{:.8f}'.format(float(data_base['trade_info']['profit']))) + ' USDT', 'yellow'), 'cyan') + ' | ' + colored('Б: ' + colored(num_round(usdt_balance) + ' USDT', 'yellow') + best_coin_name + ' | ' + colored('Д: ' + colored(num_round(info_delta) + '% ', upd_spinner_delta_color), 'cyan') + colored(upd_row_delta, upd_spinner_delta_color) + '\x1b[K', 'cyan'), 'white', end='\r', flush=True)
        except Exception as e:
            try:
                logging.error(str(extract_tb(exc_info()[2])[0][1]) + ' ' + coin['s'] + ' Output to console\n' + str(e))
            except:
                logging.error(str(e))
        time_ = time.time()
    mutex.release()

def new_order(_symbol, _side, _price, _LBTC, _quantity, _id, _status, _clientId='xbot_'):
    try:
        for pair in data_base.items():
            if pair[0] == _symbol:
                logging.warning(str(pair[0]) + '\n' + str(pair[1]))
                q = num_round(_quantity)
                price = num_round(_price) if float(_LBTC) == 0 else num_round(_LBTC)
                status = 'BUY_ORDER' if 'xbot_' in str(_clientId) else 'USER_BUY_ORDER'
                if (pair[1]['status'] == 'NO_ORDER' or pair[1]['status'] == 'TRAILING_SELL_ORDER') and _side == 'BUY':
                    info_rewrite(pair[0], stepSize=pair[1]['stepSize'], tickSize=pair[1]['tickSize'], minNotional=pair[1]['minNotional'], priceChangePercent=pair[1]['priceChangePercent'], askPrice=pair[1]['askPrice'], averagePrice=price, buyPrice=price, sellPrice=pair[1]['sellPrice'], trailingPrice=price, allQuantity=pair[1]['allQuantity'], free=pair[1]['free'], idOrder=_id, profit=pair[1]['profit'], totalUSDT=pair[1]['totalUSDT'], numAverage=pair[1]['numAverage'], status=status)
                    if float(price) != 0:
                        cprint('|' + str(datetime.datetime.now().strftime('%H:%M:%S')) + '| ' + colored('BUY  ', 'green') + '(PLACED): ' + colored('[' + q + ']', 'grey', 'on_white') + ' ' + colored(pair[0].replace('USDT', ''), 'magenta', attrs=['bold']) + ' for ' + colored(price + ' USDT\x1b[K', 'yellow'))
                if pair[1]['status'] == 'AVERAGE_BUY_ORDER' and _side == 'BUY':
                    info_rewrite(pair[0], stepSize=pair[1]['stepSize'], tickSize=pair[1]['tickSize'], minNotional=pair[1]['minNotional'], priceChangePercent=pair[1]['priceChangePercent'], askPrice=price, averagePrice=pair[1]['averagePrice'], buyPrice=price, sellPrice=pair[1]['sellPrice'], trailingPrice=pair[1]['trailingPrice'], allQuantity=pair[1]['allQuantity'], free=pair[1]['free'], idOrder=_id, profit=pair[1]['profit'], totalUSDT=pair[1]['totalUSDT'], numAverage=pair[1]['numAverage'], status=pair[1]['status'])
                    cprint('|' + str(datetime.datetime.now().strftime('%H:%M:%S')) + '| ' + colored('BUY  ', 'green') + '(PLACED): ' + colored('[' + q + ']', 'grey', 'on_white') + ' ' + colored(pair[0].replace('USDT', ''), 'magenta', attrs=['bold']) + ' for ' + colored(price + ' USDT\x1b[K', 'yellow'))
                free_ = 0 if pair[1]['status'] == 'SELL_ORDER' else pair[1]['free']
                quantity_ = num_round(_quantity) if pair[1]['status'] == 'SELL_ORDER' else pair[1]['allQuantity']
                info_rewrite(pair[0], stepSize=pair[1]['stepSize'], tickSize=pair[1]['tickSize'], minNotional=pair[1]['minNotional'], priceChangePercent=pair[1]['priceChangePercent'], askPrice=price, averagePrice=pair[1]['averagePrice'], buyPrice=pair[1]['buyPrice'], sellPrice=price, trailingPrice=pair[1]['trailingPrice'], allQuantity=quantity_, free=free_, idOrder=_id, profit=pair[1]['profit'], totalUSDT=pair[1]['totalUSDT'], numAverage=pair[1]['numAverage'], status=pair[1]['status'])
                true_meaasge = False if pair[1]['status'] == 'TRAILING_SELL_ORDER' else cprint('|' + str(datetime.datetime.now().strftime('%H:%M:%S')) + '| ' + colored('SELL ', 'red') + '(PLACED): ' + colored('[' + q + ']', 'grey', 'on_white') + ' ' + colored(pair[0].replace('USDT', ''), 'magenta', attrs=['bold']) + ' for ' + colored(price + ' USDT\x1b[K', 'yellow'))
                if true_meaasge != False:
                    true_meaasge
                info_rewrite('trade_info', sell_filled_orders=data_base['trade_info']['sell_filled_orders'], sell_open_orders=float(data_base['trade_info']['sell_open_orders']) + 1, profit=data_base['trade_info']['profit'], daily_volume=data_base['trade_info']['daily_volume'])
                break
    except Exception as e:
        try:
            logging.error(str(extract_tb(exc_info()[2])[0][1]) + '\n' + str(e))
            cprint('|' + str(datetime.datetime.now().strftime('%H:%M:%S')) + '| ' + str(extract_tb(exc_info()[2])[0][1]) + colored('\x1b[K\n' + str(e), 'red'))
        except:
            logging.error(str(e))

def partially_filled_order(_symbol, _side, _allQuantity, _lQuantity, _zQuantity, _id):
    try:
        for pair in data_base.items():
            if pair[0] == _symbol and _side == 'BUY' and pair[1]['idOrder'] == str(_id):
                logging.warning(str(pair[0]) + '\n' + str(pair[1]))
                step_size = get_count(pair[1]['stepSize'])
                all_quantity = num_round(('{:.' + str(step_size) + 'f}').format(float(pair[1]['allQuantity']) - float(_lQuantity)))
                free_quantity = num_round(('{:.' + str(step_size) + 'f}').format(float(pair[1]['free']) + float(_lQuantity)))
                info_rewrite(pair[0], stepSize=pair[1]['stepSize'], tickSize=pair[1]['tickSize'], minNotional=pair[1]['minNotional'], priceChangePercent=pair[1]['priceChangePercent'], askPrice=pair[1]['askPrice'], averagePrice=pair[1]['averagePrice'], buyPrice=pair[1]['buyPrice'], sellPrice=pair[1]['sellPrice'], trailingPrice=pair[1]['trailingPrice'], allQuantity=all_quantity, free=free_quantity, idOrder=pair[1]['idOrder'], profit=pair[1]['profit'], totalUSDT=pair[1]['totalUSDT'], numAverage=pair[1]['numAverage'], status=pair[1]['status'])
                break
            if pair[0] == _symbol and _side == 'SELL' and pair[1]['idOrder'] == str(_id):
                step_size = get_count(pair[1]['stepSize'])
                all_quantity = num_round(('{:.' + str(step_size) + 'f}').format(float(_allQuantity) - float(_zQuantity)))
                info_rewrite(pair[0], stepSize=pair[1]['stepSize'], tickSize=pair[1]['tickSize'], minNotional=pair[1]['minNotional'], priceChangePercent=pair[1]['priceChangePercent'], askPrice=pair[1]['askPrice'], averagePrice=pair[1]['averagePrice'], buyPrice=pair[1]['buyPrice'], sellPrice=pair[1]['sellPrice'], trailingPrice=pair[1]['trailingPrice'], allQuantity=all_quantity, free=pair[1]['free'], idOrder=pair[1]['idOrder'], profit=pair[1]['profit'], totalUSDT=pair[1]['totalUSDT'], numAverage=pair[1]['numAverage'], status=pair[1]['status'])
                break
    except Exception as e:
        try:
            logging.error(str(extract_tb(exc_info()[2])[0][1]) + '\n' + str(e))
            cprint('|' + str(datetime.datetime.now().strftime('%H:%M:%S')) + '| ' + str(extract_tb(exc_info()[2])[0][1]) + colored('\x1b[K\n' + str(e), 'red'))
        except:
            logging.error(str(e))

def filled_order(_symbol, _side, _price, _allQuantity, _LBTC, _lQuantity, _zQuantity, _ZBTC, _id, _clientId='xbot_'):
    try:
        for pair in data_base.items():
            if pair[0] == _symbol and pair[1]['status'] != 'ERROR_ORDER':
                logging.warning(str(pair[0]) + '\n' + str(pair[1]))
                ncoi = 'xbot_' + _symbol
                _step_size = pair[1]['stepSize']
                step_size = get_count(_step_size)
                quantity = ('{:.' + str(step_size) + 'f}').format(float(_lQuantity) + float(pair[1]['free']))
                price = num_round(_price) if float(_LBTC) == 0 else num_round(_LBTC)
                ZBTC = _ZBTC if float(_ZBTC) != 0 else num_round('{:.8f}'.format(float(price)*float(quantity)))
                if _side == 'BUY':
                    sell_price = num_round('{:.' + str(get_count(pair[1]['tickSize'])) + 'f}').format(float(price) + float(price)/100*(float(sell_up) + delta_perc))
                    sell_price = num_round('{:.' + str(get_count(pair[1]['tickSize'])) + 'f}').format(float(price) + float(pair[1]['tickSize'])) if float(sell_price) == float(price) else sell_price
                    sell_true = pair[1]['sellPrice'] if pair[1]['status'] == 'AVERAGE_BUY_ORDER' else sell_price
                    status_print = '(FILLED): ' if pair[1]['status'] == 'AVERAGE_BUY_ORDER' else '(FILLED): '
                    cprint('|' + str(datetime.datetime.now().strftime('%H:%M:%S')) + '| ' + colored('BUY  ', 'green') + status_print + colored('[' + num_round(_zQuantity) + ']', 'grey', 'on_white') + ' ' + colored(pair[0].replace('USDT', ''), 'magenta', attrs=['bold']) + ' for ' + colored(price + ' USDT\x1b[K', 'yellow'))
                    client.order_limit_sell(symbol=_symbol, quantity=quantity, price=sell_true, newClientOrderId=ncoi)
                    total_usdt = '{:.8f}'.format(float(pair[1]['totalUSDT']) + float(ZBTC))
                    num_average = float(pair[1]['numAverage']) + float(data_base['trade_params']['step_aver']) if data_base['trade_params']['num_aver'] == 'y' else float(pair[1]['numAverage'])
                    averagePrice_ = price if 'xbot_' not in str(_clientId) or float(pair[1]['averagePrice']) == 0 else pair[1]['averagePrice']
                    buyPrice_ = price if 'xbot_' not in str(_clientId) or float(pair[1]['buyPrice']) == 0 else pair[1]['buyPrice']
                    info_rewrite(pair[0], stepSize=pair[1]['stepSize'], tickSize=pair[1]['tickSize'], minNotional=pair[1]['minNotional'], priceChangePercent=pair[1]['priceChangePercent'], askPrice=pair[1]['askPrice'], averagePrice=averagePrice_, buyPrice=buyPrice_, sellPrice=sell_true, trailingPrice=averagePrice_, allQuantity=quantity, free=0, idOrder=pair[1]['idOrder'], profit=pair[1]['profit'], totalUSDT=total_usdt, numAverage=num_average, status='SELL_ORDER')
                    info_rewrite('trade_info', sell_filled_orders=data_base['trade_info']['sell_filled_orders'], sell_open_orders=data_base['trade_info']['sell_open_orders'], profit=data_base['trade_info']['profit'], daily_volume='{:.8f}'.format(float(data_base['trade_info']['daily_volume']) + float(ZBTC)))
                print_color = 'magenta' if pair[1]['status'] == 'TRAILING_SELL_ORDER' else 'red'
                profit = '{:.8f}'.format(float(pair[1]['profit']) + float(ZBTC) - float(pair[1]['totalUSDT']))
                perc_profit = '{:.2f}'.format(100 - float(pair[1]['totalUSDT'])/float(ZBTC)*100)
                if (pair[1]['status'] == 'TRAILING_SELL_ORDER' or pair[1]['status'] == 'SELL_ORDER') and _symbol in data_base['trailing_orders'].keys():
                    trailing_orders = data_base['trailing_orders']
                    trailing_orders[_symbol].append([{'p': price, 'q': num_round(_allQuantity)}][0])
                else:
                    trailing_orders = dict()
                if tg_notification == 'y':
                    logging.warning('Filled order, push to Telegram ' + _symbol + ': ' + str(_allQuantity) + ' ' + str(pair[1]['averagePrice']) + ' ' + str(price) + ' ' + str(perc_profit) + ' ' + str('{:.8f}'.format(float(ZBTC) - float(pair[1]['totalUSDT']))) + '\n' + str(trailing_orders))
                    send_telegram(_symbol, _allQuantity, pair[1]['averagePrice'], price, perc_profit, '{:.8f}'.format(float(ZBTC) - float(pair[1]['totalUSDT'])), trailing_message=trailing_orders)
                if _symbol in trailing_orders:
                    trailing_orders.pop(_symbol)
                    data_base['trailing_orders'] = trailing_orders
                cprint('|' + str(datetime.datetime.now().strftime('%H:%M:%S')) + '| ' + colored('SELL ', print_color) + '(FILLED): ' + colored('[' + num_round(_zQuantity) + ']', 'grey', 'on_white') + ' ' + colored(pair[0].replace('USDT', ''), 'magenta', attrs=['bold']) + ' for ' + colored(price + ' USDT\x1b[K', 'yellow'))
                daily_profit(str(datetime.date.today()), '{:.8f}'.format(float(ZBTC) - float(pair[1]['totalUSDT'])))
                info_rewrite(pair[0], stepSize=pair[1]['stepSize'], tickSize=pair[1]['tickSize'], minNotional=pair[1]['minNotional'], priceChangePercent=pair[1]['priceChangePercent'], askPrice=price, averagePrice=0, buyPrice=0, sellPrice=0, trailingPrice=0, allQuantity=0, free=0, idOrder=0, profit=profit, totalUSDT=0, numAverage=0, status='NO_ORDER')
                info_rewrite('trade_info', sell_filled_orders=float(data_base['trade_info']['sell_filled_orders']) + 1, sell_open_orders=float(data_base['trade_info']['sell_open_orders']) - 1, profit='{:.8f}'.format(float(data_base['trade_info']['profit']) + float(ZBTC) - float(pair[1]['totalUSDT'])), daily_volume='{:.8f}'.format(float(data_base['trade_info']['daily_volume']) + float(ZBTC)))
                break
    except Exception as e:
        try:
            logging.error(str(extract_tb(exc_info()[2])[0][1]) + '\n' + str(e))
            cprint('|' + str(datetime.datetime.now().strftime('%H:%M:%S')) + '| ' + str(extract_tb(exc_info()[2])[0][1]) + colored('\x1b[K\n' + str(e), 'red'))
        except:
            logging.error(str(e))

def trailing_price_merket(_symbol, _allQuantity, _lQuantity, _LBTC, _zQuantity, _ZBTC):
    try:
        for pair in data_base.items():
            if pair[0] == _symbol:
                logging.warning(str(pair[0]) + '\n' + str(pair[1]))
                price = num_round(_LBTC)
                cprint('|' + str(datetime.datetime.now().strftime('%H:%M:%S')) + '| ' + colored('SELL ', 'magenta') + '(MARKET): ' + colored('[' + num_round(_allQuantity) + ']', 'grey', 'on_white') + ' ' + colored(pair[0].replace('USDT', ''), 'magenta', attrs=['bold']) + ' for ' + colored(price + ' USDT\x1b[K', 'yellow'))
                all_quantity = num_round(('{:.' + str(get_count(pair[1]['stepSize'])) + 'f}').format(float(pair[1]['allQuantity']) - float(_allQuantity)))
                total_usdt = '{:.8f}'.format(float(pair[1]['totalUSDT']) - float(_ZBTC))
                trailing_orders = data_base['trailing_orders']
                if _symbol not in data_base['trailing_orders'].keys():
                    trailing_orders[_symbol] = [{'p': price, 'q': num_round(_allQuantity)}]
                else:
                    trailing_orders[_symbol].append([{'p': price, 'q': num_round(_allQuantity)}][0])
                data_base['trailing_orders'] = trailing_orders
                info_rewrite(pair[0], stepSize=pair[1]['stepSize'], tickSize=pair[1]['tickSize'], minNotional=pair[1]['minNotional'], priceChangePercent=pair[1]['priceChangePercent'], askPrice=pair[1]['askPrice'], averagePrice=pair[1]['averagePrice'], buyPrice=pair[1]['buyPrice'], sellPrice=num_round(float(price) - float(pair[1]['tickSize'])), trailingPrice=pair[1]['trailingPrice'], allQuantity=all_quantity, free=pair[1]['free'], idOrder=pair[1]['idOrder'], profit=pair[1]['profit'], totalUSDT=total_usdt, numAverage=0, status=pair[1]['status'])
                break
    except Exception as e:
        try:
            logging.error(str(extract_tb(exc_info()[2])[0][1]) + '\n' + str(e))
            cprint('|' + str(datetime.datetime.now().strftime('%H:%M:%S')) + '| ' + str(extract_tb(exc_info()[2])[0][1]) + colored('\x1b[K\n' + str(e), 'red'))
        except:
            logging.error(str(e))

def cancel_order(_symbol, _side, _price, _quantity, _zQuantity, _id, _status):
    try:
        for pair in data_base.items():
            if pair[0] == _symbol:
                logging.warning(str(pair[0]) + '\n' + str(pair[1]))
                ncoi = 'xbot_' + _symbol
                q = num_round(_quantity)
                if _side == 'BUY' and pair[1]['status'] != 'AVERAGE_BUY_ORDER':
                    cprint('|' + str(datetime.datetime.now().strftime('%H:%M:%S')) + '| ' + colored('BUY  ', 'yellow') + '(CANCELED): ' + colored('[' + q + ']', 'grey', 'on_white') + ' ' + colored(pair[0].replace('USDT', ''), 'magenta', attrs=['bold']) + ' for ' + colored(num_round(_price) + ' USDT ', 'yellow') + colored('ID ' + str(_id) + '\x1b[K', 'grey', attrs=['bold']))
                    info_rewrite(pair[0], stepSize=pair[1]['stepSize'], tickSize=pair[1]['tickSize'], minNotional=pair[1]['minNotional'], priceChangePercent=pair[1]['priceChangePercent'], askPrice=pair[1]['askPrice'], averagePrice=0, buyPrice=0, sellPrice=0, trailingPrice=0, allQuantity=0, free=num_round(_zQuantity), idOrder=0, profit=pair[1]['profit'], totalUSDT=pair[1]['totalUSDT'], numAverage=0, status='NO_ORDER')
                if _side == 'SELL' and pair[1]['status'] == 'SELL_ORDER':
                    cprint('|' + str(datetime.datetime.now().strftime('%H:%M:%S')) + '| ' + colored('SELL ', 'yellow') + '(CANCELED): ' + colored('[' + q + ']', 'grey', 'on_white') + ' ' + colored(pair[0].replace('USDT', ''), 'magenta', attrs=['bold']) + ' for ' + colored(num_round(_price) + ' USDT ', 'yellow') + colored('ID ' + str(_id) + '\x1b[K', 'grey', attrs=['bold']))
                    info_rewrite(pair[0], stepSize=pair[1]['stepSize'], tickSize=pair[1]['tickSize'], minNotional=pair[1]['minNotional'], priceChangePercent=pair[1]['priceChangePercent'], askPrice=pair[1]['askPrice'], averagePrice=pair[1]['averagePrice'], buyPrice=pair[1]['buyPrice'], sellPrice=pair[1]['sellPrice'], trailingPrice=pair[1]['trailingPrice'], allQuantity=pair[1]['allQuantity'], free=q, idOrder=0, profit=pair[1]['profit'], totalUSDT=pair[1]['totalUSDT'], numAverage=pair[1]['numAverage'], status='CANCELED_SELL_ORDER')
                    info_rewrite('trade_info', sell_filled_orders=data_base['trade_info']['sell_filled_orders'], sell_open_orders=float(data_base['trade_info']['sell_open_orders']) - 1, profit=data_base['trade_info']['profit'], daily_volume=data_base['trade_info']['daily_volume'])
                if _side == 'SELL' and pair[1]['status'] == 'TRAILING_SELL_ORDER':
                    cprint('|' + str(datetime.datetime.now().strftime('%H:%M:%S')) + '| ' + colored('SELL ', 'magenta') + '(CANCELED): ' + colored('[' + q + ']', 'grey', 'on_white') + ' ' + colored(pair[0].replace('USDT', ''), 'magenta', attrs=['bold']) + ' for ' + colored(num_round(_price) + ' USDT ', 'yellow') + colored('ID ' + str(_id) + '\x1b[K', 'grey', attrs=['bold']))
                    info_rewrite(pair[0], stepSize=pair[1]['stepSize'], tickSize=pair[1]['tickSize'], minNotional=pair[1]['minNotional'], priceChangePercent=pair[1]['priceChangePercent'], askPrice=pair[1]['askPrice'], averagePrice=pair[1]['averagePrice'], buyPrice=pair[1]['buyPrice'], sellPrice=pair[1]['sellPrice'], trailingPrice=pair[1]['trailingPrice'], allQuantity=pair[1]['allQuantity'], free=pair[1]['free'], idOrder=0, profit=pair[1]['profit'], totalUSDT=pair[1]['totalUSDT'], numAverage=pair[1]['numAverage'], status=pair[1]['status'])
                    info_rewrite('trade_info', sell_filled_orders=data_base['trade_info']['sell_filled_orders'], sell_open_orders=float(data_base['trade_info']['sell_open_orders']) - 1, profit=data_base['trade_info']['profit'], daily_volume=data_base['trade_info']['daily_volume'])
                if _side == 'BUY' and pair[1]['status'] == 'AVERAGE_BUY_ORDER':
                    cprint('|' + str(datetime.datetime.now().strftime('%H:%M:%S')) + '| ' + colored('BUY  ', 'yellow') + '(CANCELED): ' + colored('[' + q + ']', 'grey', 'on_white') + ' ' + colored(pair[0].replace('USDT', ''), 'magenta', attrs=['bold']) + ' for ' + colored(num_round(_price) + ' USDT ', 'yellow') + colored('ID ' + str(_id) + '\x1b[K', 'grey', attrs=['bold']))
                    quantity = num_round(float(pair[1]['free']))
                    client.order_limit_sell(symbol=_symbol, quantity=quantity, price=pair[1]['sellPrice'], newClientOrderId=ncoi)
                    info_rewrite(pair[0], stepSize=pair[1]['stepSize'], tickSize=pair[1]['tickSize'], minNotional=pair[1]['minNotional'], priceChangePercent=pair[1]['priceChangePercent'], askPrice=pair[1]['askPrice'], averagePrice=pair[1]['averagePrice'], buyPrice=pair[1]['buyPrice'], sellPrice=pair[1]['sellPrice'], trailingPrice=pair[1]['trailingPrice'], allQuantity=quantity, free=0, idOrder=0, profit=pair[1]['profit'], totalUSDT=pair[1]['totalUSDT'], numAverage=pair[1]['numAverage'], status='SELL_ORDER')
                break
    except Exception as e:
        try:
            logging.error(str(extract_tb(exc_info()[2])[0][1]) + '\n' + str(e))
            cprint('|' + str(datetime.datetime.now().strftime('%H:%M:%S')) + '| ' + str(extract_tb(exc_info()[2])[0][1]) + colored('\x1b[K\n' + str(e), 'red'))
        except:
            logging.error(str(e))

def start_user_socket(msg_sus):
    global usdt_balance, bnb_balance, tickers, exchange, trade_order, check_tg
    mutex.acquire()
    logging.warning("""start_user_socket(msg_sus):
""" + str(msg_sus))
    try:
        if msg_sus['e'] == 'outboundAccountPosition':
            for coin in msg_sus.get('B'):
                if coin['a'] == 'USDT':
                    usdt_balance = coin['f']
                if coin['a'] == 'BNB':
                    bnb_balance = coin['f']
                    if float(coin['f']) < 0.1:
                        tickers = client.get_ticker()
                        exchange = client.get_exchange_info()['symbols']
                        for pair in tickers:
                            if pair['symbol'] == 'BNBUSDT' and float(bnb_balance) < 0.1:
                                for step in exchange:
                                    if step['symbol'] == pair['symbol']:
                                        try:
                                            q = ('{:.' + str(get_count(num_round(step['filters'][2]['stepSize']))) + 'f}').format(float(num_round(step['filters'][3]['minNotional']))/float(pair['askPrice']))
                                            while float(q)*float(pair['askPrice']) <= float(step['filters'][3]['minNotional']):
                                                q = ('{:.' + str(get_count(num_round(step['filters'][2]['stepSize']))) + 'f}').format(float(q) + float(step['filters'][2]['stepSize']))
                                            client.order_market_buy(symbol='BNBUSDT', quantity=q)
                                            bnb_balance = '{:.8f}'.format(float(bnb_balance) + float(q))
                                            break
                                        except Exception as e:
                                            try:
                                                logging.error(str(extract_tb(exc_info()[2])[0][1]) + ' ' + q + '\n' + str(e))
                                                cprint('|' + str(datetime.datetime.now().strftime('%H:%M:%S')) + '| ' + str(extract_tb(exc_info()[2])[0][1]) + ' ' + q + colored('\x1b[K\n' + str(e), 'red'))
                                                cprint('|' + str(datetime.datetime.now().strftime('%H:%M:%S')) + '| ' + colored('Ошибка при покупке BNB: ', 'cyan') + colored(str(e), 'red'))
                                            except:
                                                logging.error(str(e))
                                            break
    except Exception as e:
        try:
            logging.error(str(extract_tb(exc_info()[2])[0][1]) + """ start_user_socket(outboundAccountPosition)
""" + str(e))
        except:
            logging.error(str(e))
    try:
        if msg_sus['e'] == 'executionReport':
            s = msg_sus.get('s')
            S = msg_sus.get('S')
            p = msg_sus.get('p')
            q = msg_sus.get('q')
            l = msg_sus.get('l')
            L = msg_sus.get('L')
            z = msg_sus.get('z')
            Z = msg_sus.get('Z')
            i = msg_sus.get('i')
            X = msg_sus.get('X')
            c = msg_sus.get('c')
            C = msg_sus.get('C')
            n = msg_sus.get('n')
            N = msg_sus.get('N')
            if X == 'PARTIALLY_FILLED' or X == 'FILLED':
                try:
                    bnb_burn = data_base['bnb_burn']
                    if N not in data_base['bnb_burn'].keys():
                        bnb_burn[N] = [n]
                    else:
                        bnb_burn[N].append(n)
                    data_base['bnb_burn'] = bnb_burn
                except:
                    pass
            if 'trailingabt_' in c and X == 'FILLED':
                trailing_price_merket(s, q, l, L, z, Z)
                data_base_update()
            if 'xbot_' in c or 'xbot_' in C:
                if X == 'NEW':
                    new_order(s, S, p, L, q, i, X)
                elif X == 'PARTIALLY_FILLED':
                    partially_filled_order(s, S, q, l, z, i)
                elif X == 'FILLED':
                    filled_order(s, S, p, q, L, l, z, Z, i)
                elif X == 'CANCELED' and 'xbot_' not in c:
                    client.order_limit_sell(symbol=s, quantity=num_round(q), price=num_round(p), newClientOrderId=C)
                elif X == 'CANCELED':
                    cancel_order(s, S, p, q, z, i, X)
                data_base_update()
            elif 'xbot_' not in c and user_order == 'y' and s in data_base['white_list']:
                if X == 'NEW' and data_base[s]['status'] == 'NO_ORDER':
                    new_order(s, S, p, L, q, i, X, c)
                elif X == 'PARTIALLY_FILLED' and data_base[s]['status'] == 'USER_BUY_ORDER':
                    partially_filled_order(s, S, q, l, z, i)
                elif X == 'FILLED' and data_base[s]['status'] == 'USER_BUY_ORDER':
                    filled_order(s, S, p, q, L, l, z, Z, i, c)
                elif X == 'CANCELED' and data_base[s]['status'] == 'USER_BUY_ORDER':
                    cancel_order(s, S, p, q, z, i, X)
            trade_order = False
    except Exception as e:
        try:
            if tg_notification == 'y':
                while check_tg <= 3:
                    try:
                        text = """<code>❗ Стрим веб-сокета остановлен из-за ошибки:
📄 {}
🔌 Перезапустите бота!</code>""".format(str(e))
                        bot.send_message(chat_id=tg_name, text=text, parse_mode='HTML')
                        check_tg = 0
                        break
                    except Exception as e:
                        check_tg += 1
                        logging.error(str(e))
            cprint('Socket Error: STOP TRADE', 'red')
            logging.error(str(extract_tb(exc_info()[2])[0][1]) + """ Socket Error: STOP TRADE - start_user_socket(executionReport)
""" + str(e) + ' ' + str(msg_sus))
        except:
            logging.error(str(e))
    mutex.release()

def check_license():
    deposit_address_bnb = client.get_deposit_address(asset='BNB')
    deposit_address_btc = client.get_deposit_address(asset='BTC')
    priv = """-----BEGIN RSA PRIVATE KEY-----
            MIIJKQIBAAKCAgEAq/7hyQLMziGXwZBCV3vgyR5hiwIm0z2Fyay2x46XTuqOoVw8
            tt6Kpz/7qA1qqLw5MvKOT47KGsJWV8v5RtWWVbrjzJS7PgA3JVS/xuOpOI65Tqun
            h47+Mkqzv+tj1s4H9f7diWZNsBzINrpuPGwxEPqP/7TJX5zxVelvE1CKGo0Fkx5Y
            jyxKBIdg8Z08rieLIOi5w0hU0QIAGUdC7iLLGHp2xkKoFAjo5i8PGy5J5/dQ9VlV
            H+6KJ6Cr8agLXoyEj8BBb1aVTwmgSlN0MAnAN6OzB6cOWA98RicuhqFAZNYq3mK7
            HvdbQQ9lT2WhQZpLOIS92QYITJk2iFHKbhXiozB8SXZS9ytMRiFhN4YNx/yzlltM
            cLYRAAYikdDPfcaqspnMk6xqLn5Qyof12loJ8epXg7tct/lYAu8DyFjoU6t6kyKw
            X0sIUEhxNcnBQ+bZ5kPj3UHYmrDqSeCS+xi89RkAVi/P19HXtA4Yac/jiBKRVS9e
            PvFqMeEVn1Swq1OuCme8enOP2QnETm8uKH2G8kdD1DyGUhN01PuSuWoQQ1XreTsZ
            dQPa6Ebta1gbffg6sUp9JTkTOA1uhAcCd+Z/nNcI9zu8VYb/N5KVxNry9Z00z/YO
            XqUarFJ4lqCdCAm5iE4Zm/wQCszCtlWnSCOrUwwWSUtWTr+Ihz8CFcKeDVsCAwEA
            AQKCAgA+4Mx8ZximlyNasTl/sBsKi5/PaPb2rPw3MXwU0m1AfYGtPgI4PH1mDX8b
            /eOrUjx7Aq/CKAp84+Ua7cfw/G6cYtma1hjp3rxKWoRN2rbnpU3bk+eIKF+H1UWH
            eS+jvOiuJwGolIz8QFl1oIxibI83jNKOAfLIkKCt7swbvIrwj/OkyChKFz/sDe4E
            Bp7DcFNtsYcP/GZ9joSouSOf2Xp0NXksm/vEb0lttXCJWE/OjNy9BW6YYOWC/Ts+
            +ldFtotT3k5NvNKS9YrzATVtxnLOJHtz5b/Zs7eUEgjxUQwwkRdU+7U66eUjkNRR
            xW7Bg/3R6L1bFNh94FlOVtBxlHCo7DVw6a/dMC/v1I2j2tajmuYnDSR082ndBezX
            1VEMDW9Pd1mQ3y5GLrcmtvAMAjWVwowkdI0N3YDJH/H5jh0VXTfMoiVxyX2cuXBj
            IGy8R6Lxo6VCoiTUtqUViU1KstnH/uXKoSfnJFq9FA6le6UNVRFQUdhgyr41MrQB
            Rz77rlBEj9aL9SCR2+p2gciA7MrRdsa0HHEnedEa0DupjbA9D6+fH2l05b7wnGtj
            3r63d+Gf3ntcOy1yuc9gPNtvIAaNOiQEwcfoZ2iMcaPs7ITIs3+nSyvov1asWOI9
            ahLJih0VRpSuDYOqh1WaPMDr53YU45BfdKrdNQC26w9WQTKBGQKCAQEA5NLWeGZs
            o26PXW+0cdZb0ACVOd0aHzsR7rH4TqFj5DuLZkpj02T+seoGWdlYJ0xExfc9IpSU
            o4yXmU/3Pe0jQU+aH6AvD1N8LKInuN5RZKGpturYu1+Y3Bf8i92ZD7pcdZgdQClZ
            5y4l4Mu8W3TEoSUqUCRFZBSBELBp1kmmwKJOA7HfZkSPNFt98MgoVH04qSmkihQU
            w9XdEUoUYwzpNgo56PJ9yUdNzeyF5uJjexJgNqtnKv+ZLa0UbKGqvlMayCzrlk30
            SpV3/eYdiNX0DV2rvAFVFqCaBOJYwxrrUSpQSeu5cHAj5/VumvZvZuszNmCjuuS2
            3ERJuKFu/nqZvQKCAQEAwGw+omj35qlN4IKF/afFDoRVTaIMQW7ejBlnEDSPwWHB
            Wy5qLe6H4pGu3N2jm3JhSdakrkj7p/RmYT22B2OQo8+urXRvXwFMWHHNNePOJNd+
            CEGj3XxXpcRroRNTI46aNmFmWPy/f3j0qzwkaCvdi4eR9Vj0SzdpBeR/pPjg5O+E
            syl/ekZPM/T0DO9msIwA6WWqcaDxtHALULyDoh4cGXC0g0O8puQvbWOUPwIjUaXC
            pXPK/9ZKShn992eQrOULan2lM4tQB6bFgkhjdMHGoatz/dbYItqUv9Li1ks03rKt
            ixkjhLFvd+kThNkJSRYc47myND15Pq1I3TCWWTIY9wKCAQEAik1wuabWhNVfK49H
            lgKEzax8hVPA5R1z0jyZIxVi5eCjebj+qxeA5ZHYMtgt8tqjOrAbsFnzmQJx4oU1
            n6VDyMbPFcxghTfldqivr4oX0eXwSRGa222FW4nX58WRLLNsDNta2pvjrdnzpPIf
            L3vdGLT45SV3F21ZMPgfkBhGBGpVEuCgcRSBJZki/rRLw/1HkN8NhzNp9Y++pSOM
            PO3hyvrVU5m1M0G4of0SVaGBlTJfGsvweEmykKvrC1mPdKeQKWsVHWySeb3rn3dF
            ZJ5Eewuhr+lyP1HkpY0VLx+HGTClBHjIRVBSM3HhXyIR5TfFZVl1vJFegLV5hXF1
            P7RkVQKCAQAWixfzcxTIA0HKccA87XDauIo95CRHbjPIehlm/qFw6ID8q71o0C8/
            Tg4MdjL6vTXErs7wVECXdryf29j9mJ6TcntmeuOpX7+QBRUjoSK/kjeDxBzsj+q8
            0vxBDMCKw+QxRsv01PeieYtAnHUvdyQneqSQ9/D29vDo7dI+g6HlcGI9kzkKHD6f
            Oa117n47ZMuejHihg1eN6iqJNOy/C4QDPv8G+eKaMtWTnTz6/Mcig6cAN0arHnHp
            qI3mdE2w08y4lyvJlCK2IsW088IjJaidvDaEoK0FuFIA/zXwITN6e7h1OWa93wPO
            KpJM2BiMZXjQ/SpxkFoqC6cjstOKc6IVAoIBAQDDsufGLb+WLe6/fUB+9kzNojk8
            ZSnZZznDm0tiGBinfcbOKCguloHIz2gdku5yr5NZAPGm6rVoSQ/qd/Nu0n4nLY9/
            U2W7LMBnOeTwFFjeuHaA3ITQAxMfS+kkgP2VB40ZDUd7CnfY10GcTmriftfh/O8R
            j1fWDaY0dlHvJtiIfCOfVwG5XpeGxH/UvGGpCAYb3PzdWQs2c2X8IjTgpt8OcyYT
            fgGgU4S7hUl0EN0U4Culj8yn7syxSp3gitF/bHizeEtc+TTL+SCN+tiyJrIdwSzr
            zsisgAaJ7OtsRMwsP3NRbt9xqttQys/ExautQevqGTUjKk30DBXKx1DZOJq7
            -----END RSA PRIVATE KEY-----"""
    pub = """-----BEGIN PUBLIC KEY-----
            MIICIjANBgkqhkiG9w0BAQEFAAOCAg8AMIICCgKCAgEArPgR22icHYT9Tf0+k5Ah
            /hwB/vtGveRPFBOsY1Z2zzJMZcj5nAY/Gj15Fez7XqYLLc3iluqOar47YQZC5f+g
            qg1o7/wr1gDS1tw453oFYccL2xxk3/Qlylj6SjArLDRug4UzdEJrVGQIpn5JIIJh
            lUaM5xYkMYNCTuvnWXfI085jArPSfWhDF0/C1ofsREM4/Szn2gl//ejRq5RQQlw1
            vUkJMhuPev59FltAd1/z42W7RHG4N7Cic1dPXFIRkLyy7BPiErsTArEqeSdhLNxr
            S1qbs5AhRuL5WTYLEylrKbpq77CXRxq0BU6SGldVKeWk+dAIWLqdRim+Zg8k+5DF
            UIc3VcbgXtNPq5/v54/Fy1bEr29FkQOfCzYm03TWkDw9UUKxV3tgx9NVu9FA58w2
            ywUkl7t0JL/JdPD+AdKlwDzLEw5TxnBgV8Ymp7QV37XDFVOQ9oNJ/ff+rFMH0qIF
            OHi2OJGrrvmk1b3F/Qd+FGbxdkXMMpg5QhpVdLUGcftku/gS2O/Fngm7+8Qwn1Yo
            YimzgE/4OtGuLGCqbSr2aUZfMhiegU8DHBtNLLeA0Nu1GaRxYiiC4yBat69IhufN
            PIDG3p1oGaRz53LULxisLfQpykYOTSLisQIuZXXDwmMsSoKqHJUaqGfh3Qtww7KI
            RB4Tn/KJFPQWyFeobQeyC0UCAwEAAQ==
            -----END PUBLIC KEY-----"""
    priv = rsa.PrivateKey.load_pkcs1(priv)
    try:
        deposit_address_bnb_addressTag = deposit_address_bnb['addressTag']
    except:
        deposit_address_bnb_addressTag = 0
    json_crypto = {'bot': 'xbot', 'referal': referal, 'memo': deposit_address_bnb_addressTag, 'address_btc': deposit_address_btc['address'], 'time': str(time.time())}
    json_object = json.dumps(json_crypto)
    pub = rsa.PublicKey.load_pkcs1_openssl_pem(pub)
    message = json_object.encode('utf-8')
    message = rsa.encrypt(message, pub)
    message = message.hex()
    url = 'https://zilliqagbot.mitagmio.ru/aver/'
    data = {'time': time.time(), 'message': message}
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    try:
        r = requests.post(url, data=json.dumps(data), headers=headers, verify=False)
        message = r.json()['message']
        message = json.loads(rsa.decrypt(bytes.fromhex(message), priv).decode())
        return message
    except Exception as e:
        try:
            cprint('|' + str(datetime.datetime.now().strftime('%H:%M:%S')) + '| ' + str(extract_tb(exc_info()[2])[0][1]) + colored('\x1b[K\n' + str(e), 'red'))
            cprint('Повторная попытка соединения с сервером')
            time.sleep(40)
            check_license()
        except:
            logging.error(str(e))

