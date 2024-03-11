import sqlite3
import requests
from time import sleep
import telebot

bot = telebot.TeleBot("5888057605:AAF15FvP1BlH3W_lrmHrfsmWSHzmYWahFlo")


def changeAdBit(tgId, advertId, newPrice):
    api = getApi(tgId)
    headers = {'Authorization': api}
    params = {
        "advertId": advertId,
        "type": 6,
        "cpm": int(newPrice),
        "param": getParam(advertId, api)
    }
    try:
        requests.post('https://advert-api.wb.ru/adv/v0/cpm', headers=headers, json=params)
    except Exception as ex:
        print(ex)


def getParam(idAd, api):
    headers = {'Authorization': api}
    params = {'id': idAd}
    response = requests.get('https://advert-api.wb.ru/adv/v0/advert', headers=headers, params=params).json()
    return int(response['params'][0]['subjectId'])


def getApi(tgId):
    return sqlite3.connect('database.db').execute(f'SELECT adToken FROM Users where id ={tgId}').fetchall()[0][0]


def getPositionPriceAd(position: str, zapros, maxprice, myAdvertId):
    if len(position.split('-')) == 2:
        pmin, pmax = sorted(map(int, position.split('-')))
        poz_list = [i for i in range(pmin, pmax + 1)]

    else:
        poz_list = list()
        poz_list.append(int(position))

    try:
        response = requests.get(f'https://catalog-ads.wildberries.ru/api/v5/search?keyword={zapros}').json()
        topCpm = [i['cpm'] for i in response['adverts']]
        topAdvertId = [i['advertId'] for i in response['adverts']]
        for poz in poz_list:
            if len(topCpm) >= poz and int(topCpm[poz - 1]) <= int(maxprice):

                if myAdvertId == topAdvertId[poz - 1]:
                    pozPage = [i['positions'] for i in response['pages']][0][poz-1]
                    return int(topCpm[poz]) + 1, poz,pozPage
                else:
                    pozPage = [i['positions'] for i in response['pages']][0][poz-1]
                    return int(topCpm[poz - 1]) + 1, poz,pozPage
        return 50, 0,0
    except:
        return 50, 0,0


cou = 0
while True:
    try:
        conn = sqlite3.connect('chatAndAd.db')
        data = conn.execute(
            f'select tg.tgId,tg.adId,ad.position,ad.price,ad.request from tg join ad on tg.adId=ad.adId;').fetchall()
        conn.close()
        string = ''
        count = 0
        for i in data:
            count += 1
            price, poz,pozPage = getPositionPriceAd(i[2], i[4], i[3], i[1])
            # -------------------------------
            connad = sqlite3.connect('chatAndAd.db')
            connad.execute(f'update ad set pozad = {poz},pozpage={pozPage} where adid = {i[1]}')
            connad.commit()
            connad.close()

            # -------------------------------

            string += f"<b>{count}</b>) {str(price)} {str(i[4])} <b>{poz}</b>\n"
            changeAdBit(i[0], i[1], price)
        bot.send_message(5645821676, string, parse_mode='HTML')
        cou += 1
        sleep(180)


    except Exception as ex:
        sleep(5)

        bot.send_message(5645821676, str(ex))
        pass
