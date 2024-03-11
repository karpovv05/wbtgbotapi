import sqlite3

# class exId:

class useChat:
    # chat(adId int(50), tgId int(50))
    # ad(adId int(50), position int(22),price int(5),request text(200))

    def addDataInChats(self, chatId, adId, position, maxprice, request):
        try:
            conn = sqlite3.connect('chatAndAd.db')
            conn.execute('INSERT INTO tg values (?,?)', (adId,chatId))
            conn.execute('INSERT INTO ad values (?,?,?,?,?,?)', (adId, position, maxprice, request,0,0))
            conn.commit()
            conn.close()
            return 'Ваша реклама поставлена на контроль позиции.'
        except:
            return 'Эта реклама уже стоит на контроле. Сперва остановите Контроль позиции и запустите снова. '


    def delAd(self,adId):
        adId = int(adId)
        conn = sqlite3.connect('chatAndAd.db')
        conn.execute(f'DELETE FROM tg where adId = {adId};')
        conn.execute(f'DELETE FROM ad where adId = {adId};')
        conn.commit()
        conn.close()



#################
# conn = sqlite3.connect('chatAndAd.db')


# z = conn.execute(f'select tg.tgId,tg.adId,ad.position,ad.price,ad.request from tg join ad on tg.adId=ad.adId;').fetchall()

# z = conn.execute(f'select * from ad;').fetchall()

# print(z)
# print(len(z))
####################################

