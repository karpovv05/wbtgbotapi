import sqlite3
from datetime import datetime, timedelta
from time import sleep


def del_user_without_podp():
    for i in sqlite3.connect('podpiska.db').execute('select tg,podp from data').fetchall():
        if datetime.strptime(i[1], '%Y-%m-%d') + timedelta(days=1) < datetime.today():
            user = sqlite3.connect('chatAndAd.db').execute(f'select * from tg where tgId = {i[0]}').fetchall()
            if user:
                sqlite3.connect('chatAndAd.db').execute(f'delete from tg where tgId = {i[0]}').connection.commit()
                for numAd in user:
                    sqlite3.connect('chatAndAd.db').execute(
                        f'delete from ad where adId = {numAd[0]}').connection.commit()


while True:
    del_user_without_podp()
    sleep(2000)
