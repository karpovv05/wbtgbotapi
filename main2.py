from classWbad import WbAd
import telebot
from classSqlite import sqliteCommand
from telebot import types
from sqlAd import useChat
import requests
from telebot.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
import sqlite3
from datetime import datetime, date, timedelta, datetime
import os
import subprocess



def control(m,req): #обработчик ставки и ставка на контроль
    if len(m.text.split())>=3 and len(m.text.split())<=10: # проверка кол-ва слов в запросе
         pass
    else:
        bot.send_message(m.chat.id,'Проверьте правильность запроса.\nЕсли все верно, напишите @karpov_coach')
        exit()
    
    poz,price,zapros = m.text.split()[0],m.text.split()[1],' '.join(m.text.split()[2:])#проверка ценника
    firstPrice,secPrice = poz.split('-')[0].isdigit(),poz.split('-')[-1].isdigit()
    if firstPrice and secPrice: #проверка ценника
          pass
    else:
        bot.send_message(m.chat.id,'Проверьте правильность запроса.\nЕсли все верно, напишите @karpov_coach')
        exit()
    numAd = req.split()[1]
    bot.send_message(m.chat.id,useChat().addDataInChats(m.chat.id, numAd, poz, price, zapros))
def getPriceList(m):#получение цены по запросу
    try:
        per = sqlite3.connect('chatAndAd.db').execute(
            f'select adid from tg where tgid={m.chat.id};').fetchall()
        rez = [per[i][0] for i in range(len(per))]

        url = f'https://catalog-ads.wildberries.ru/api/v5/search?keyword={m.text}'  # URL сайта, который вы хотите скачать
        response = requests.get(url)  # Отправляем запрос на получение содержимого страницы
        if response.status_code == 200:  # Если запрос успешен
            content = requests.get(url).json()
            positions_list = []
            id_list = []
            cpm_list = []
            advertId_list = []
            info = ''
            page_cou = 0
            pos_cou = 0
            for i in content['pages']:
                for j in i['positions']:
                    positions_list.append(j)
            for i in content['adverts']:
                id_list.append(i['id'])
                cpm_list.append(i['cpm'])
                advertId_list.append(i['advertId'])

            for pos, id, cpm, ad in zip(positions_list, id_list, cpm_list, advertId_list):
                pos_cou += 1

                if pos_cou % 30 == 1 or len(advertId_list)==pos_cou:
                    page_cou += 1
                    if page_cou == 2:
                        bot.send_message(m.chat.id, info, parse_mode='HTML')
                        continue
                if ad in rez:
                    info += f'<b>{pos_cou}) Позиция на сайте: {pos}, Артикул: {id}, Цена места: {cpm}</b>\n'
                else:
                    info += f'{pos_cou}) Позиция на сайте: {pos}, Артикул: {id}, Цена места: {cpm}\n'

        markup = InlineKeyboardMarkup(row_width=1)
        markup.add(DMenu['workWithAds'],
                DMenu['checkPrice'],
                DMenu['options'],
                DMenu['buySub'],
                DMenu['help'])
        bot.send_message(m.from_user.id, "Главное меню", reply_markup = markup)
        pass
    except Exception as ex:
        bot.send_message(m.chat.id,
                            'По данному запросу ничего не нашел, попробуйте это запрос через 5 минут.')
def addApi(m):
    if len(m.text) > 100:
        sql.addPerson(m.chat.id, m.text)
        bot.send_message(m.chat.id, f"Ваш токен добавлен.")
    else:
        bot.send_message(m.chat.id, f"Что то с токеном неладное.")
def changeApi(m):
    if len(m.text) > 100:
        sql.changeApi(m.chat.id, m.text)
        bot.send_message(m.chat.id, f"Ваш токен изменен.")
    else:
        bot.send_message(m.chat.id, f"Что то с токеном неладное.")
def chek_podp(m):
            proverkaUser = sqlite3.connect('podpiska.db').execute(
                f'SELECT * FROM data where tg={m.chat.id};').fetchall()
            if datetime.strptime(proverkaUser[0][1], '%Y-%m-%d').date() < date.today():
                bot.send_message(m.chat.id, "Ваша подписка закончилась, для продления напишите @karpov_coach")
                return False
            else:
                return True


sql = sqliteCommand()
bot = telebot.TeleBot('6303791556:AAEqfNunwnk8kBRQZo34yFWvjt_SV5g5_1A')

commands = ['/menu']
bot.set_my_commands([types.BotCommand(command, 'Вызвать меню') for command in commands])
DMenu = {
                            #Главная
        'workWithAds':InlineKeyboardButton(text='🧑‍🏭 Работа с рекламой', callback_data='workWithAds'),
        'checkPrice':InlineKeyboardButton(text='🔭 Проверка цен по запросу', callback_data='checkPrice'),
        'buySub':InlineKeyboardButton(text='🛒 Купить подписку', callback_data='buySub'),
        'options':InlineKeyboardButton(text='🛠 Настройки', callback_data='options'),
        'refProgram':InlineKeyboardButton(text='🤝 Приведи друга', callback_data='refProgram'), 
        'help':InlineKeyboardButton(text='🆘 Помощь и вопросы', callback_data='help'),

                            #Работа с рекламой
        'myAds':InlineKeyboardButton(text='Моя реклама', callback_data='myAds'),
        'controlAds':InlineKeyboardButton(text='Управление рекламой', callback_data='controlAds'),
                             
                            #Настройки
        'addApi':InlineKeyboardButton(text='Добавить рекламный API', callback_data='addApi'),
        'changeApi':InlineKeyboardButton(text='Изменить рекламный API', callback_data='changeApi'),


                            #Помощь и вопросы
        'video':InlineKeyboardButton(text='Видеоурок', callback_data='video',url='https://cloud.mail.ru/public/jTLu/wUmvAygka'),
        'howWorkBot':InlineKeyboardButton(text='Как работает бот', callback_data='howWorkBot'),
        'howAddToken':InlineKeyboardButton(text='Где взять и как добавить токен', callback_data='howAddToken',url='https://cloud.mail.ru/public/ycFj/UuKxkWpKn'),
        'helpComl':InlineKeyboardButton(text='Вопрос/Жалоба/Предложение', callback_data='helpComl'), 




                            #Главное меню
        'main':InlineKeyboardButton(text='Главное меню', callback_data='main'),}
#Обработчик запросов call
@bot.callback_query_handler(func=lambda call:True)
def callback_query(call):
    #проверка на наличие токена в бд
    if sql.check_id(call.message.chat.id) == False:
        bot.send_message(call.message.chat.id,
                        'Вам НЕОБХОДИМО добавить свой РЕКЛАМНЫЙ токен в меню "Работа с токенами (API)".')
    try:
        req = call.data.split('_')
        if req[0] == 'unseen':
            bot.delete_message(call.message.chat.id, call.message.message_id)

        if req[0] == 'workWithAds':
            bot.delete_message(call.message.chat.id, call.message.message_id)
            markup = InlineKeyboardMarkup(row_width=1)
            markup.add(
                DMenu['myAds'],
                DMenu['controlAds'],
                DMenu['main'],)
            bot.send_message(call.message.chat.id,'Работа с рекламой',reply_markup = markup)

        if req[0] == 'main':
            bot.delete_message(call.message.chat.id, call.message.message_id)
            markup = InlineKeyboardMarkup(row_width=1)
            markup.add(DMenu['workWithAds'],
                DMenu['checkPrice'],
                DMenu['options'],
                DMenu['buySub'],
                DMenu['refProgram'],
                DMenu['help'])
            bot.send_message(call.message.chat.id,'Главное меню',reply_markup = markup)

        if req[0] == 'options':
            bot.delete_message(call.message.chat.id, call.message.message_id)
            markup = InlineKeyboardMarkup(row_width=1)
            markup.add(DMenu['addApi'],
                DMenu['changeApi'],
                DMenu['main'],)
            bot.send_message(call.message.chat.id,'Настройки',reply_markup = markup)

        if req[0] == 'help':
                bot.delete_message(call.message.chat.id, call.message.message_id)
                markup = InlineKeyboardMarkup(row_width=1)
                markup.add(DMenu['video'],
                    DMenu['howWorkBot'],
                    DMenu['howAddToken'],
                    DMenu['helpComl'],
                    DMenu['main'],)
                bot.send_message(call.message.chat.id,'Помощь и вопросы',reply_markup = markup)

        if req[0] == 'howWorkBot':
                bot.send_message(call.message.chat.id,'Как работает бот?'
                                                        '\n1) Бот работает по принципу автоматизированному выставления актуальной ставки по запросу, что бы вы могли гаратированно'
                                                        ' находиться в топе и не переплачивать, тем самым экономив свой бюджет!'
                                                        '\n2) Если ваша максимальная ставка МЕНЬШЕ чем стоимость промежутка позиций, что вы задали,'
                                                        ' бот ставит цену 50рублей на 1000 показов и ждет, когда цена позиций, что вы задали, '
                                                        ' будет удовлетворять вашей максимальной ставке на 1000 показов.'
                                                        '\n<b>Примечания:</b>'
                                                        '\n    1) Бот работает только с рекламными компаниями в <b>ПОИСКЕ</b>'
                                                        '\n    2) Бот отвечает за нахождение в топе ваилдбериз по запросу',
                                        parse_mode='HTML')
        if req[0] == 'myAds':
            bot.delete_message(call.message.chat.id, call.message.message_id)
            try:
                            bot.send_message(call.message.chat.id, '<b>----------Загружаю!----------</b>', parse_mode='HTML')
                            wb = WbAd(sql.getApi(call.message.chat.id)).getMyAds()
                            bot.send_message(call.message.chat.id, wb, parse_mode='HTML')
            except:
                            bot.send_message(call.message.chat.id, 'Проверьте рекламный токен! Не получается получить информацию.\За помощью напишите @karpov_coach')
            finally:
                markup = InlineKeyboardMarkup(row_width=1)
                markup.add(
                    DMenu['myAds'],
                    DMenu['controlAds'],
                    DMenu['main'],)
                bot.send_message(call.message.chat.id,'Работа с рекламой',reply_markup = markup)

        if req[0] == 'controlAds' and chek_podp(call.message):
            bot.delete_message(call.message.chat.id, call.message.message_id)
            markup = InlineKeyboardMarkup(row_width=1)
            for i in WbAd(sql.getApi(call.message.chat.id)).getLitsNameMyAds():
                                markup.add(InlineKeyboardButton(text = f'{i}',callback_data = f'Ad {i}' ))
            markup.add(DMenu['main'])
            bot.send_message(call.message.chat.id, 'Список вашей рекламы', reply_markup=markup)

        if req[0].split()[0] == 'Ad':
            i,num = ' '.join(req[0].split()[1:]),req[0].split()[-1]
            bot.delete_message(call.message.chat.id, call.message.message_id)
            markup = InlineKeyboardMarkup(row_width=1)
            markup.add(InlineKeyboardButton(text = f'Запустить рекламу',callback_data = f'Start {num}' ))
            markup.add(InlineKeyboardButton(text = f'Отсановить рекламу',callback_data = f'Stop {num}' ))
            markup.add(InlineKeyboardButton(text = f'Поставить на контроль',callback_data = f'GetConrol {num}' ))
            markup.add(InlineKeyboardButton(text = f'Снять с контроля',callback_data = f'StopControl {num}' ))
            
            markup.add(DMenu['controlAds'],DMenu['main'])
            bot.send_message(call.message.chat.id, f'Какое действие вы хотите совершить с рекламой <b>{i}</b>', reply_markup=markup,parse_mode='HTML')
        
        if req[0].split()[0] == 'Start':
            WbAd(sql.getApi(call.message.chat.id)).startAd(req[0].split()[1])
            bot.send_message(call.message.chat.id, "Запущена!")

        if req[0].split()[0] == 'Stop':
            WbAd(sql.getApi(call.message.chat.id)).pauseAd(req[0].split()[1])
            bot.send_message(call.message.chat.id, "Остановлена!")

        if req[0].split()[0] == 'GetConrol':
            msg = bot.send_message(call.message.chat.id, 'Напишите свой запрос по формату ниже через пробел!\n\
                            1) Желаемая позиция\n\
                            2) Максимальная Ставка за 1000 показов\n\
                            3) Мастер фраза пр которой будет браться ценник\n\n<b>Перед вами 3 примера:</b>\n(Боту нужно написать только <b>один</b> запрос одной строчкой)\n   -----\n4 120 пижама в горошек летняя\n7-14 200 брюки клеш\n1-20 325 тазик',
                            parse_mode='HTML')
            bot.register_next_step_handler(msg, control,req[0])
            
        if req[0].split()[0] == 'StopControl':
            useChat().delAd(req[0].split()[-1].strip())
            bot.send_message(call.message.chat.id, 'Реклама снята с контроля.')

        if req[0] == 'checkPrice':
            msg = bot.send_message(call.message.chat.id, 'Напишите запрос: \nПример: <b>майка розовая</b>',
                                        parse_mode='HTML')
            bot.register_next_step_handler(msg, getPriceList)

        if req[0] == 'addApi':
            msg = bot.send_message(call.message.chat.id,'Пришлите ваш <b>рекламный</b> Api', parse_mode='HTML')
            bot.register_next_step_handler(msg,addApi)

        if req[0] == 'changeApi':
            msg = bot.send_message(call.message.chat.id,'Пришлите ваш <b>новый рекламный</b> Api', parse_mode='HTML')
            bot.register_next_step_handler(msg,changeApi)

        if req[0] == 'buySub':
            markup = InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton(text='Оплата отправлена', callback_data='checkCash'))
            bot.send_photo(call.message.chat.id,open('sber.jpeg', 'rb'))
            bot.send_message(call.message.chat.id, f"Стоимость подписки составляет 1000р <b>при наличии реферального кода</b> и 1500р БЕЗ реферального кода\nОплата принимается на СБЕРБАНК переводом по номеру <b>+79773262093 \
                                (Карпов А.А.)</b>\n<b>ВНИМАНИЕ!</b>\nВ комметарии к переводу укажите данный код  <b>{call.message.chat.id}</b> и через (<b>:</b>) реферальный код, если он у вас есть.\
                            \nКомментарий отправьте в формате <b>{call.message.chat.id}:Реферальный код</b>\
                            \nПосле отправки <b>ОБЯЗАТЕЛЬНО</b> нажмите кнопку <b>Оплата отправлена</b>",parse_mode='HTML', reply_markup = markup)
        if req[0] == 'checkCash':
            markup = InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton(text='Да', callback_data='Yes'))
            markup.add(InlineKeyboardButton(text= 'Нет', callback_data='No'))

            bot.send_message(5645821676, f"Хотят купить подписку {call.message.chat.id}",reply_markup = markup)

            bot.edit_message_text('Администратор проверит в ближайшее время ваш платеж.\nПоддержка @karpov_coach',chat_id=call.message.chat.id, message_id=call.message.message_id, parse_mode='HTML')
            bot.send_message(call.message.chat.id, f"")
        
        if req[0] == 'Yes':
            id = call.message.text.split(' ')[-1]
            current_podpiska = datetime.strptime(sqlite3.connect('podpiska.db').execute(f'SELECT podp from data where tg = {id}').fetchone()[0],'%Y-%m-%d').date()
            if current_podpiska>= date.today():
                newdata = str(current_podpiska   + timedelta(days=int(31)))
                conn = sqlite3.connect('podpiska.db')
                cour = conn.cursor()
                cour.execute('UPDATE data SET podp = ? where tg = ?', (newdata, id))
                conn.commit()
                conn.close()
                bot.send_message(call.message.chat.id, str(
                    sqlite3.connect('podpiska.db').execute(f'select podp from data where tg = {id}').fetchone()[
                        0]))
                bot.send_message(id,f'Ваша подписка продлена до {newdata}')
                bot.edit_message_text(call.message.text,chat_id=call.message.chat.id, message_id=call.message.message_id)

                
            else:
                newdata = str(date.today() + timedelta(days=int(31)))
                conn = sqlite3.connect('podpiska.db')
                cour = conn.cursor()
                cour.execute('UPDATE data SET podp = ? where tg = ?', (newdata, id))
                conn.commit()
                conn.close()
                bot.send_message(call.message.chat.id, str(
                    sqlite3.connect('podpiska.db').execute(f'select podp from data where tg = {id}').fetchone()[
                        0]))
                bot.send_message(id,f'Ваша подписка продлена до {newdata}')
                bot.edit_message_text(call.message.text,chat_id=call.message.chat.id, message_id=call.message.message_id)

        if req[0] == 'No':
            id = call.message.text.split(' ')[-1]
            bot.send_message(id,'Оплата не поступила на карту!\nЕсли вы отправили денежные средства, обратитесь @karpov_coach')
            bot.edit_message_text(call.message.text,chat_id=call.message.chat.id, message_id=call.message.message_id)

        if req[0] == 'helpComl':
            bot.send_message(call.message.chat.id, 'Напишите @karpov_coach')
        
        if req[0] == 'refProgram':
            bot.send_message(call.message.chat.id,f'Скажи другу свой пригласительный код <b>{call.message.chat.id}</b>.\nПодарите другу постоянную скидку на 500р.\nТак же вы будете получать кэшбек на карту в размере 20% от суммы которую потратил товарищ на продление подписки.', parse_mode='HTML')
    except:
        markup = InlineKeyboardMarkup(row_width=1)
        markup.add(DMenu['workWithAds'],
            DMenu['checkPrice'],
            DMenu['options'],
            DMenu['buySub'],
            DMenu['refProgram'],
            DMenu['help'])
        bot.send_message(call.message.chat.id,'Главное меню',reply_markup = markup)




@bot.message_handler()
def mainFun(m):
    if m.chat.id == 5645821676:
        if m.text.split()[0] == 'Send':
            mes = ' '.join(m.text.split()[1:])
            for i in sqlite3.connect('podpiska.db').execute('SELECT tg FROM data').fetchall():
                try:
                    bot.send_message(int(i[0]), mes)
                except:
                    continue        
        if m.text == '  ':
            for i in sqlite3.connect('podpiska.db').execute('SELECT tg FROM data').fetchall():
                try:
                    podp_data = sqlite3.connect('podpiska.db').execute(
                        f'SELECT podp FROM data where tg ={int(i[0])};').fetchall()[0][0]
                    bot.send_message(int(i[0]), f"Ваша подписка активна до {podp_data}")
                except:
                    continue
        if m.text == 'Reboot':
            os.system("reboot now")

    if m.text.split(' ')[0] == 'Add':
        none, id, days = m.text.split(' ')
        newdata = str(date.today() + timedelta(days=int(days)))

        conn = sqlite3.connect('podpiska.db')
        cour = conn.cursor()
        cour.execute('UPDATE data SET podp = ? where tg = ?', (newdata, id))
        conn.commit()
        conn.close()
        bot.send_message(m.chat.id, str(
            sqlite3.connect('podpiska.db').execute(f'select podp from data where tg = {id}').fetchone()[
                0]))
        
    if m.text == 'Reload':
        subprocess.call("../reload.sh")

    #проверка на наличие в базе данных
    proverkaUser = sqlite3.connect('podpiska.db').execute(
                f'SELECT * FROM data where tg={m.chat.id};').fetchall()
    if not proverkaUser:
                newdata = date.today() + timedelta(days=10)
                sqlite3.connect('podpiska.db').execute(
                    f'INSERT INTO data VALUES (?,?,?,?);', (m.chat.id, newdata, 1, None)).connection.commit()
                sqlite3.connect('podpiska.db').execute('UPDATE data SET podp=?, trial=1 where tg=?', (
                    date.today() + timedelta(days=10), m.chat.id)).connection.commit()
                bot.send_message(m.chat.id, f'Ваша подписка активна до {date.today() + timedelta(days=10)}')

    #ответ на любое сообщение
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(DMenu['workWithAds'],
            DMenu['checkPrice'],
            DMenu['options'],
            DMenu['buySub'],
            DMenu['refProgram'],
            DMenu['help'])
    bot.send_message(m.from_user.id, "Главное меню", reply_markup = markup)


if __name__ == '__main__':
    bot.polling(none_stop=True)
    