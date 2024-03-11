import sqlite3
from pprint import pprint
import requests


class WbAd:
    def __init__(self, adApi):
        self.errorCount = 0
        self.headers = {'Authorization': adApi}

    def startAd(self, numAd):
        payload = {'id': numAd}
        response = requests.get('https://advert-api.wb.ru/adv/v0/start', headers=self.headers, params=payload)
        print(response.text)  #

    def pauseAd(self, numAd):
        payload = {'id': numAd}
        response = requests.get('https://advert-api.wb.ru/adv/v0/pause', headers=self.headers, params=payload)
        print(response.text)

    def stopAd(self, numAd):
        payload = {'id': numAd}
        response = requests.get('https://advert-api.wb.ru/adv/v0/stop', headers=self.headers, params=payload)
        print(response.text)

    def getListPriceAd(self, zapros):
        # берем инфу с сылки по запросу
        try:
            response = requests.get(f'https://catalog-ads.wildberries.ru/api/v5/search?keyword={zapros}')
            topList = []
            topPlace = [i['positions'] for i in response.json()['pages']]
            topId = [i['id'] for i in response.json()['adverts']]
            topCpm = [i['cpm'] for i in response.json()['adverts']]
            for i in zip(topPlace[0], topId, topCpm):
                topList.append(i)

            return topList

        except:
            self.errorCount += 1

            if self.errorCount > 3:
                print('Попробуйте через 10 секунд, некорректный запрос.')
            else:
                self.getListPriceAd(zapros)

    def getParam(self, idAd):
        params = {'id': idAd}
        response = requests.get('https://advert-api.wb.ru/adv/v0/advert', headers=self.headers, params=params).json()
        return int(response['params'][0]['subjectId'])

    def getMyAds(self):
        try:
            response = requests.get('https://advert-api.wb.ru/adv/v0/adverts', headers=self.headers).json()
            id_list = []
            for i in response:
                if i['type'] == 6 and (i['status'] == 9 or i['status'] == 11):
                    id_list.append(i['advertId'])

            str_response = ''
            for i in id_list:
                ifincontrol = self.checkIfControl(i)
                params = {'id': i}
                res = requests.get('https://advert-api.wb.ru/adv/v0/advert', headers=self.headers, params=params).json()
                str_response += f"Название рекламы: <b>{res['name']}</b>" + '\n'
                str_response += f"Номер рекламы: {res['advertId']}" + '\n'
                # str_response += f"Текущая цена рекламы: {res['params'][0]['price']}" + '\n'
                if res['status'] == 9:
                    str_response += f"Статус: <b>АКТИВНА</b>" + '\n'
                if res['status'] == 11:
                    str_response += f"Статус: <b>ПРИОСТАНОВЛЕНА</b>" + '\n'
                if len(ifincontrol) == 0:
                    str_response += f"Контроль позиции: <b>НЕТ</b>" + '\n'
                if len(ifincontrol) != 0:
                    poz, price, zap, curpoz,pozpage = ifincontrol[0][1], ifincontrol[0][2], ifincontrol[0][3],ifincontrol[0][4],ifincontrol[0][5]
                    str_response += f"Контроль позиции: <b>ДА</b>" + '\n'
                    str_response += f'Предпочтительная позиция: {poz}' + '\n'
                    str_response += f'Текущая позиция среди реклам: <b>{curpoz}</b>' + '\n'
                    str_response += f'Текущая позиция на странице поиска: <b>{pozpage}</b>' + '\n'

                    str_response += f'Максимальная ставка: {price}' + '\n'
                    str_response += f'Запрос: {zap}' + '\n'
                #     print(ifincontrol,12321313)

                str_response += '*' * 10 + '\n'
            if str_response == '':
                return 0
            else:
                return str_response
        except Exception as ex:
            print(ex)

    def checkIfControl(self, adId):
        conn = sqlite3.connect('chatAndAd.db')
        return conn.execute(f'SELECT * FROM ad WHERE adId = {adId}').fetchall()

    def getPositionPriceAd(self, zapros, position):
        # берем инфу с сылки по запросу
        try:
            response = requests.get(f'https://catalog-ads.wildberries.ru/api/v5/search?keyword={zapros}')
            topCpm = [i['cpm'] for i in response.json()['adverts']]
            if len(topCpm) >= position:
                print(topCpm[position - 1])
            else:
                print(f'Колличество рекламы меньше чем ваша позиция, всего позиций {len(topCpm)}')
                print('Хотели бы занять последнюю позицию?')

        except Exception as ex:
            print(ex)
            self.errorCount += 1

            if self.errorCount > 3:
                print('Попробуйте через 10 секунд, некорректный запрос.')

            else:
                self.getPositionPriceAd(zapros, position)

        # pprint(response.json())

    def changeAdBit(self, advertId, newPrice):
        params = {
            "advertId": advertId,
            "type": 6,
            "cpm": int(newPrice),
            "param": self.getParam(advertId)
        }

        response = requests.post('https://advert-api.wb.ru/adv/v0/cpm', headers=self.headers, json=params)
        # print(response.text)
        #######################################################
    def getLitsNameMyAds(self):
        response = requests.get('https://advert-api.wb.ru/adv/v0/adverts', headers=self.headers).json()
        # pprint(response)
        rez_list = []
        for i in response:
            if i['type'] == 6:
                if i['status'] == 9:
                    rez_list.append(f"{i['name']} : {i['advertId']}")

                if i['status'] == 11:
                    rez_list.append(f"{i['name']} : {i['advertId']}")
        return rez_list
