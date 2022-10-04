#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb  8 17:22:20 2022
@author: brianszekely
buy and sell conditions
"""

def buy_signal_hft(trade_crypt, kraken, volume_inst, account_bal):
    traded = False
    try:
        # if trade_crypt == "YFIUSD":
            
        #     volume_inst = float(volume_inst) * 4
        #     new_vol = str(volume_inst)
        #     open_pos = True
        #     response = kraken.add_standard_order(pair=trade_crypt, type='buy', ordertype='limit',
        #                                      volume=new_vol, price=MATI_ask, validate=False)
        #     print(response)
        #     traded = True
        #     return open_pos, MATI_ask, traded
        # else:
            #percentage of total in account 
        curr = account_bal * 0.99
        vol_min = float(volume_inst)
        if trade_crypt == "YFIUSD":
            MATI_ask = int(float((kraken.get_ticker_information(trade_crypt))['a'][0][0]))
            price_per_v = MATI_ask * vol_min
            vol_ratio = curr / price_per_v
            new_vol = vol_ratio * vol_min
            new_vol = str(round(new_vol),5)
        else:
            
            MATI_ask = float((kraken.get_ticker_information(trade_crypt))['a'][0][0])
            price_per_v = MATI_ask * vol_min
            vol_ratio = curr / price_per_v
            new_vol = vol_ratio * vol_min
            new_vol = str(round(new_vol,5))
        response = kraken.add_standard_order(pair=trade_crypt, type='buy', ordertype='market',
                                         volume=new_vol, validate=False)
        # response = kraken.add_standard_order(pair=trade_crypt, type='buy', ordertype='limit',
        #                                  volume=new_vol, price=MATI_ask, validate=False)
        print(response)
        traded = True
        open_pos = False
        #trade min way
        # response = kraken.add_standard_order(pair=trade_crypt, type='buy', ordertype='limit',
        #                                  volume=float(volume_inst), price=MATI_ask, validate=False)
        # print(response)
        # open_pos = False
        return open_pos, MATI_ask, traded
    except Exception as e:
        print(f'Error placing buy order: {e}')
        open_pos = True
        MATI_ask = 0.0
        traded = False
        return open_pos, MATI_ask, traded

def basic_sell(trade_crypt, kraken, volume_inst, balance):
    trade_crypt_save = trade_crypt.replace('USD', '')
    trade_crypt_og = trade_crypt_save
    m = 1
    while m == 1:
        try:
            if trade_crypt_save == "BTC":
                trade_crypt_save = 'XXBT'
                volume_inst_save = balance.vol[trade_crypt_save]
            elif trade_crypt_save == "MLN":
                trade_crypt_save = 'XMLN'
                volume_inst_save = balance.vol[trade_crypt_save]
            elif trade_crypt_save == "LTC":
                trade_crypt_save = 'XLTC'
                volume_inst_save = balance.vol[trade_crypt_save]
            elif trade_crypt_save == "ETC":
                trade_crypt_save = 'XETC'
                volume_inst_save = balance.vol[trade_crypt_save]
            elif trade_crypt_save == "ETH":
                trade_crypt_save = 'XETH'
                volume_inst_save = balance.vol[trade_crypt_save]
            elif trade_crypt_save == "DOGE":
                trade_crypt_save = 'XXDG'
                volume_inst_save = balance.vol[trade_crypt_save]
            elif trade_crypt_save == "XLM":
                trade_crypt_save = 'XXLM'
                volume_inst_save = balance.vol[trade_crypt_save]
            elif trade_crypt_save == "XMR":
                trade_crypt_save = 'XXMR'
                volume_inst_save = balance.vol[trade_crypt_save]
            elif trade_crypt_save == "XTZ":
                trade_crypt_save = 'XXTZ'
                volume_inst_save = balance.vol[trade_crypt_save]
            elif trade_crypt_save == "ZEC":
                trade_crypt_save = 'XZEC'
                volume_inst_save = balance.vol[trade_crypt_save]
            elif trade_crypt_save == "REP":
                trade_crypt_save = 'XREP'
            else:
                volume_inst_save = balance.vol[trade_crypt_save]
            m = 0
            if m == 0:
                break
        except Exception as e:
            print(f'Error placing sell order: {e}')
    volume_final = str(volume_inst_save)
    trade_crypt_save = trade_crypt_save + 'USD'
    trade_crypt_og = trade_crypt_og + 'USD'
    print(f'asset pair: {trade_crypt_og}')
    print(f'asset pair volume: {volume_final}')
    print('sell: Gain')
    try:
        response = kraken.add_standard_order(pair=trade_crypt_og, type='sell', ordertype='market',
                                     volume=volume_final, validate=False)
        print(response)
        open_pos = True
        i = -10
        return open_pos, i
    except Exception as e:
        print(f'Error placing sell order: {e}')
        open_pos = False
        i = 1
        return open_pos, i
    else:
        open_pos = False
        i = 1
        return open_pos, i

def target_sell_hft(target_gain, trade_crypt, kraken, volume_inst, balance, target_loss):
    bid_in = float((kraken.get_ticker_information(trade_crypt))['b'][0][0])
    print('==============================================================================')
    print(f'bid price: {bid_in} | target sell: {target_gain} | target loss: {target_loss}')
    print('==============================================================================')
    trade_crypt_save = trade_crypt.replace('USD', '')
    trade_crypt_og = trade_crypt_save
    m = 1
    while m == 1:
        try:
            if trade_crypt_save == "BTC":
                trade_crypt_save = 'XXBT'
                volume_inst_save = balance.vol[trade_crypt_save]
            elif trade_crypt_save == "MLN":
                trade_crypt_save = 'XMLN'
                volume_inst_save = balance.vol[trade_crypt_save]
            elif trade_crypt_save == "LTC":
                trade_crypt_save = 'XLTC'
                volume_inst_save = balance.vol[trade_crypt_save]
            elif trade_crypt_save == "ETC":
                trade_crypt_save = 'XETC'
                volume_inst_save = balance.vol[trade_crypt_save]
            elif trade_crypt_save == "ETH":
                trade_crypt_save = 'XETH'
                volume_inst_save = balance.vol[trade_crypt_save]
            elif trade_crypt_save == "DOGE":
                trade_crypt_save = 'XXDG'
                volume_inst_save = balance.vol[trade_crypt_save]
            elif trade_crypt_save == "XLM":
                trade_crypt_save = 'XXLM'
                volume_inst_save = balance.vol[trade_crypt_save]
            elif trade_crypt_save == "XMR":
                trade_crypt_save = 'XXMR'
                volume_inst_save = balance.vol[trade_crypt_save]
            elif trade_crypt_save == "XTZ":
                trade_crypt_save = 'XXTZ'
                volume_inst_save = balance.vol[trade_crypt_save]
            elif trade_crypt_save == "ZEC":
                trade_crypt_save = 'XZEC'
                volume_inst_save = balance.vol[trade_crypt_save]
            elif trade_crypt_save == "REP":
                trade_crypt_save = 'XREP'
            else:
                volume_inst_save = balance.vol[trade_crypt_save]
            m = 0
            if m == 0:
                break
        except Exception as e:
            print(f'Error placing sell order: {e}')
    volume_final = str(volume_inst_save)
    trade_crypt_save = trade_crypt_save + 'USD'
    trade_crypt_og = trade_crypt_og + 'USD'
    print(f'asset pair: {trade_crypt_save}')
    print(f'asset pair volume: {volume_final}')

    if bid_in >= target_gain:
        print('sell: Gain')
        if trade_crypt == "YFIUSD":
            bid_in = int(float((kraken.get_ticker_information(trade_crypt))['b'][0][0]))
            print('change bid price from float to int ')
        try:
            response = kraken.add_standard_order(pair=trade_crypt_og, type='sell', ordertype='market',
                                         volume=volume_final, validate=False)
            # response = kraken.add_standard_order(pair=trade_crypt_save, type='sell', ordertype='limit',
            #                              volume=volume_final, price=bid_in, validate=False)
            print(response)
            open_pos = True
            i = -10
            return open_pos, i, bid_in
        except Exception as e:
            print(f'Error placing sell order: {e}')
            open_pos = False
            i = 1
            return open_pos, i, bid_in

    elif bid_in < target_loss:
        print('sell: Loss')
        try:
            response = kraken.add_standard_order(pair=trade_crypt_og, type='sell', ordertype='market',
                                         volume=volume_final, validate=False)
            print(response)
            open_pos = True
            i = -10
            return open_pos, i, bid_in
        except Exception as e:
            print(f'Error placing sell order: {e}')
            open_pos = False
            i = 1
            return open_pos, i, bid_in
    else:
        open_pos = False
        i = 1
        return open_pos, i, bid_in


def buy_signal(trade_crypt, kraken, volume_inst, account_bal):
    try:
        # if trade_crypt == "YFIUSD":
        #     MATI_ask = int(float((kraken.get_ticker_information(trade_crypt))['a'][0][0]))
        #     volume_inst = float(volume_inst) * 4
        #     new_vol = str(volume_inst)
        #     open_pos = True
        #     response = kraken.add_standard_order(pair=trade_crypt, type='buy', ordertype='limit',
        #                                      volume=new_vol, price=MATI_ask, validate=False)
        #     print(response)
        #     return open_pos, MATI_ask
        # else:
        curr = account_bal * 0.98
        vol_min = float(volume_inst)
        if trade_crypt == "YFIUSD":
            MATI_ask = int(float((kraken.get_ticker_information(trade_crypt))['a'][0][0]))
        else:
            
            MATI_ask = float((kraken.get_ticker_information(trade_crypt))['a'][0][0])
        price_per_v = MATI_ask * vol_min
        vol_ratio = curr / price_per_v
        new_vol = vol_ratio * vol_min
        new_vol = str(round(new_vol,5))
        response = kraken.add_standard_order(pair=trade_crypt, type='buy', ordertype='limit',
                                         volume=new_vol, price=MATI_ask, validate=False)
        print(response)
        open_pos = True
        return open_pos, MATI_ask
    except Exception as e:
        print(f'Error placing buy order: {e}')
        open_pos = False
        MATI_ask = 0.0
        return open_pos, MATI_ask

def target_sell(target_gain, trade_crypt, kraken, volume_inst, balance, target_loss):
    bid_in = float((kraken.get_ticker_information(trade_crypt))['b'][0][0])
    print('===================================================')
    print(f'bid price: {bid_in} | target sell: {target_gain} | target loss: {target_loss}')
    print('===================================================')
    trade_crypt_save = trade_crypt.replace('USD', '')
    volume_inst_save = balance.vol[trade_crypt_save]
    volume_final = str(round(volume_inst_save,5))
    trade_crypt_save = trade_crypt_save + 'USD'
    print(f'asset pair: {trade_crypt_save}')
    print(f'asset pair volume: {volume_final}')

    if bid_in >= target_gain:
        print('sell: Gain')
        if trade_crypt == "YFIUSD":
            bid_in = int(float((kraken.get_ticker_information(trade_crypt))['b'][0][0]))
            print('change bid price from float to int ')
        try:
            response = kraken.add_standard_order(pair=trade_crypt_save, type='sell', ordertype='limit',
                                         volume=volume_final, price=bid_in, validate=False)
            print(response)
            open_pos = False
            i = 0
            return open_pos, i, bid_in
        except Exception as e:
            print(f'Error placing sell order: {e}')
            open_pos = True
            i = 1
            return open_pos, i, bid_in

    elif bid_in < target_loss:
        print('sell: Loss')
        if trade_crypt == "YFIUSD":
            bid_in = int(float((kraken.get_ticker_information(trade_crypt))['b'][0][0]))
            print('change bid price from float to int ')
        try:
            response = kraken.add_standard_order(pair=trade_crypt_save, type='sell', ordertype='limit',
                                         volume=volume_final, price=bid_in, validate=False)
            print(response)
            open_pos = False
            i = 0
            return open_pos, i, bid_in
        except Exception as e:
            print(f'Error placing sell order: {e}')
            open_pos = True
            i = 1
            return open_pos, i, bid_in
    else:
        open_pos = True
        i = 1
        return open_pos, i, bid_in

def stop_time(now_time_2, stop_date, trade_crypt, kraken, volume_inst, balance):
# =============================================================================
#     stop time function call
# =============================================================================
    #Stop date
    if now_time_2 == stop_date or now_time_2 > stop_date: #or bid_in < target_loss
        print("sell: Loss, TIME IS UP")
        if trade_crypt == "YFIUSD":
            MATI_bid = int(float((kraken.get_ticker_information(trade_crypt))['b'][0][0]))
            print('change bid price from float to int ')
        else:
            MATI_bid = float((kraken.get_ticker_information(trade_crypt))['b'][0][0])
        try:
            trade_crypt_save = trade_crypt.replace('USD', '')
            volume_inst_save = balance.vol[trade_crypt_save]
            volume_final = str(round(volume_inst_save,5))
            trade_crypt_save = trade_crypt_save + 'USD'
            
            response = kraken.add_standard_order(pair=trade_crypt_save, type='sell', ordertype='limit',
                                         volume=volume_final, price=MATI_bid, validate=False)
            print(response)
            open_pos = False
            i = 0
            return open_pos, i, MATI_bid
        except Exception as e:
            print(f'Error placing sell time order: {e}')
            open_pos = True
            i = 1
            return open_pos, i, 0
    else:
        open_pos = True
        i = 1
        return open_pos, i, 0
    
    
def buy_signal_basic(trade_crypt, kraken, volume_inst, account_bal):
    try:
        if trade_crypt == "YFIUSD":
            MATI_ask = int(float((kraken.get_ticker_information(trade_crypt))['a'][0][0]))
            volume_inst = float(volume_inst) * 4
            new_vol = str(volume_inst)
            open_pos = True
            response = kraken.add_standard_order(pair=trade_crypt, type='buy', ordertype='limit',
                                             volume=new_vol, price=MATI_ask, validate=False)
            print(response)
            return open_pos, MATI_ask
        else:
            curr = account_bal * 0.99
            vol_min = float(volume_inst)
            MATI_ask = float((kraken.get_ticker_information(trade_crypt))['a'][0][0])
            price_per_v = MATI_ask * vol_min
            vol_ratio = curr / price_per_v
            new_vol = vol_ratio * vol_min
            new_vol = str(round(new_vol,5))
            response = kraken.add_standard_order(pair=trade_crypt, type='buy', ordertype='limit',
                                             volume=new_vol, price=MATI_ask, validate=False)
            print(response)
            open_pos = True
            return open_pos
    except Exception as e:
        print(f'Error placing buy order: {e}')
        open_pos = False
        MATI_ask = 0.0
        return open_pos