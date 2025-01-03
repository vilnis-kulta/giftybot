import sqlite3
from unittest.mock import call

import telebot
from pyexpat.errors import messages
from telebot import types

bot = telebot.TeleBot('')

user_data = {}
gift_suggestions = {
    (range(0, 13), 'Мужской', 'Новый год'): [
        'машинка Lego - 261094316, \nнабор "Создай свой слайм" - 14130888, \nпижама - 263600517, \nаквариум для рыбок - 218649828'],
    (range(0, 13), 'Женский', 'Новый год'): [
        'цветочная оранжерея - 195905714,\nпижама - 181129796,\nпарфюм - 86957538,\nорганайзер - 228183998, \nмягкая игрушка - 225761747'],
    (range(13, 18), 'Мужской', 'Новый год'): [
        'спортивный костюм - 167953664, \nбутылка для спортивного питания - 174479122,\nклавиатура с подсветкой - 10554940,\nнаушники - 196598251'],
    (range(13, 18), 'Женский', 'Новый год'): [
        'косметичка - 187559583,\nкружка - 248358095,\nсумка - 140303471,\nмассажный набор - 109819627,\nкартина по номерам - 171788009,\nнабор the act - 18165016,\nтапочки - 247674900'],
    (range(18, 100), 'Мужской', 'Новый год'): [
        'кошелек - кошелек,\nсумка кожаная -153586243,\n электробритва - 236253622,\nчасы - 197625996,\nпылесос в машину - 269977708'],
    (range(18, 100), 'Женский', 'Новый год'): [
        'часы - 265669618,\nкошелек	- 234913969,\nсвечи - 216358665,\nфен	- 139263450,\nпарфюм - 208840395,\nпостельное белье - 177238479,\nбокалы - 264670867'],
    (range(0, 13), 'Мужской', 'День рождения'): [
        'Мольберт для рисования - 252614343,\nПазлы "Синий трактор" - 162692818,\nБизиборд - 9641631,\nБизикуб - 253612772,\nМагнитная рыбалка - 177846912,\nПижама - 183189542,'
        '\nИгрушка для ванной - 149915617,\nМяч - 230693283,\nВнедорожник на пульте управления - 262100773,\nДетский стол растущий - 146376820,\nНочник "Мягкий медведь" - 291174810,\nОчки виртуальной реальности - 256774896'],
    (range(0, 13), 'Женский', 'День рождения'): ['Набор для творчества', 'Мягкая игрушка'],
    (range(13, 18), 'Мужской', 'День рождения'): ['Игровая гарнитура', 'Книга приключений'],
    (range(13, 18), 'Женский', 'День рождения'): ['Блокнот с уникальным дизайном', 'Украшение для волос'],
    (range(18, 100), 'Мужской', 'День рождения'): ['Умные часы', 'Электронная книга'],
    (range(18, 100), 'Женский', 'День рождения'): ['Духи', 'Набор для ухода за кожей'],
    (range(18, 100), 'Мужской', 'День Отца'): ['Мужской парфюм', 'Кожаный кошелёк'],
    (range(18, 100), 'Женский', 'День Матери'): ['Букет цветов', 'Сертификат на SPA'],
    (range(13, 18), 'Мужской', '14 февраля'): ['Шоколадный набор', 'Футболка с романтическим принтом'],
    (range(13, 18), 'Женский', '14 февраля'): ['Шоколадный набор', 'Подвеска в форме сердца'],
    (range(18, 100), 'Мужской', '14 февраля'): ['Билет на совместный концерт', 'Романтический ужин'],
    (range(18, 100), 'Женский', '14 февраля'): ['Ювелирное украшение', 'Романтический ужин'],
    (range(0, 13), 'Мужской', '23 февраля'): [
        'Набор динозавров - 201771402,\n,Парковка для машин - 223252019,\nМагнитная рыбалка - 15854558,'
        '\nНабор машинок	- 88629446,\nНабор инструментов - 57178576,\nРобот Кузя - 201441025,'
        '\nНабор для опытов - 164446348,\nАвтотрек - 210772966,\nТанк - 178111210,\nГигантские пузыри - 171895790,'
        '\nПланшет для рисования светом - 16304709,\nМашинка для дрифта - 263274364,\nКоллекция опытов 12 в 1 - 46957132,'
        '\nПистолет с интерактивным пауком - 246239532,\nКонструктор - 276850443,\nИгра "Скажи,если сможешь"	- 84920974,'
        '\nИнтерактивный тренажер для бокса - 273090756,\nПулемет - 267377976,\nМеч световой - 244486657,'
        '\nМеталлическая головоломка - 96708248'],
    (range(13, 18), 'Мужской', '23 февраля'): [
        'Игра "Что за мем" - 79462698,\nПодарочный набор - 263909275,\nСпортивная футболка - 238801698,'
        '\nСпортивный лонгслив - 237715331,\nЧасы - 213852872,\nНоски - 205852364,\nНабор для душа - 243692215,'
        '\nПодарочный набор - 254859059'],
    (range(18, 100), 'Мужской', '23 февраля'): [''],
    (range(0, 13), 'Женский', '8 марта'): [
        'Детский супермаркет - 169855582,\nНочник - 255606546,\nПодарочный бокс единорог - 267375416,\nПодарочный набор масок - 251918531,'
        '\nНабор слаймов - 28872234,\nПогремушка подвеска - 65144411,\nМобиль в кроватку - 138981683,\nИгрушка для сна - 243900305,'
        '\nПижама 7 в 1	- 215337226,\n 3 д конструктор - 220735250,\nКонструктор "Карета Принцессы"	- 269290279,\nЗамок Хогвартс - 223339960,'
        '\nМеховая сумка - 189799266,\nСумка для маленькой принцессы - 211541929,\nСумка через плечо - 188892713'],
    (range(13, 18), 'Женский', '8 марта'): [
        'Книга "Этому не учат в школе" - 243462186,\nПалетка теней - 227871550,\nЖивая роза в колбе с украшением - 170739275,'
        '\nНабор косметики для макияжа - 248681119,\nКартина по номерам - 230801145,\n3 д стикеры на телефон - 223207794,\nКисти для макияжа - 180790342,'
        '\nФутболка с принтом - 247897839,\nСкраб для тела - 18165016,\nШёлковая пижама 7 в 1	- 150989309,'
        '\nСумка через плечо - 249399126,\nСумка белая - 251241569,\nКосметичка - 222877932,\nСпортивный костюм - 206483166'
        '\nМагнитная подсветка - 246477766,\nНабор для маникюра 70 в 1 - 116112872,\nНабор кремов для рук - 124737470,\n'
        'Beauty box	- 204506781,\nАдвент календарь с косметикой - 264347880,\nКонструктор на пульте управления - 248380682'],
    (range(18, 100), 'Женский', '8 марта'): [
        'Набор чашек - 277349587,\nНабор кухонных принадлежностей - 225906007,\nПодарочный набор для массажа лица - 119495900,'
        '\nПодарочный набор уходовой косметики - 203883139,\nТарелки в виде бутылок - 156660173,\nНабор кухонных полотенец - 237976737,'
        '\nХалат шелковый - 172744486, \nХалат махровый - 192850169,\nДиффузор - 17669172,\nПижама - 266191151']
}


@bot.message_handler(commands=['start'])
def start(message):
    user_data[message.chat.id] = {}
    bot.send_message(message.chat.id,
                     'Привет, я - Бот,который поможет вам выбрать подарки на любой повод! Для начала укажите возраст человека, которому будем подбирать подарок')
    bot.register_next_step_handler(message, get_age)


def get_age(message):
    if not message.text.isdigit():
        if message.text.startswith('/'):
            bot.send_message(message.chat.id, 'Вы ввели команду вместо возраста. Давайте начнём заново.')
            start(message)
            return
        bot.send_message(message.chat.id, 'Пожалуйста, введите возраст числом.')
        bot.register_next_step_handler(message, get_age)
        return
    if message.chat.id not in user_data:
        user_data[message.chat.id] = {}
    user_data[message.chat.id]['age'] = int(message.text)
    sex = types.InlineKeyboardMarkup()
    btn_male = types.InlineKeyboardButton('Мужской', callback_data='male')
    btn_female = types.InlineKeyboardButton('Женский', callback_data='female')
    sex.row(btn_male, btn_female)
    bot.send_message(message.chat.id, 'Теперь выберите пол человека:', reply_markup=sex)


@bot.callback_query_handler(func=lambda call: call.data in ['male', 'female'])
def get_gender(call):
    gender = 'Мужской' if call.data == 'male' else 'Женский'
    user_data[call.message.chat.id]['gender'] = gender
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('Подарки ко Дню Рождения', callback_data='birthday_gifts'))
    markup.add(types.InlineKeyboardButton('Подарки к Новому Году', callback_data='new_year_gifts'))
    markup.add(types.InlineKeyboardButton('Подарки на 14 февраля', callback_data='14_february_gifts'))
    markup.add(types.InlineKeyboardButton('Подарки к 23 февраля', callback_data='23_february_gifts'))
    markup.add(types.InlineKeyboardButton('Подарки к 8 марта', callback_data='8_march_gifts'))
    markup.add(types.InlineKeyboardButton('Подарки ко Дню Матери', callback_data='mothers_day_gifts'))
    markup.add(types.InlineKeyboardButton('Подарки ко Дню Отца', callback_data='fathers_day_gifts'))
    bot.send_message(call.message.chat.id, 'Выберите нужную категорию из предложенных', reply_markup=markup)


@bot.callback_query_handler(
    func=lambda call: call.data in ['birthday_gifts', 'new_year_gifts', '14_february_gifts', '23_february_gifts',
                                    '8_march_gifts', 'mothers_day_gifts', 'fathers_day_gifts'])
def get_occasion(call):
    occasion_list = {
        'birthday_gifts': 'День рождения',
        'new_year_gifts': 'Новый год',
        'mothers_day_gifts': 'День Матери',
        'fathers_day_gifts': 'День Отца',
        '14_february_gifts': '14 февраля',
        '23_february_gifts': '23 февраля',
        '8_march_gifts': '8 марта'
    }
    occasion = occasion_list.get(call.data, 'Неизвестный')
    if call.message.chat.id in user_data:
        user_data[call.message.chat.id]['occasion'] = occasion
    else:
        user_data[call.message.chat.id] = {'occasion': occasion}
    user = user_data.get(call.message.chat.id)
    if not user or 'age' not in user or 'gender' not in user or 'occasion' not in user:
        bot.send_message(call.message.chat.id, 'Ваши данные не найдены или неполные. Пожалуйста, начните заново.')
        start(call.message)
        return
    start_button = types.InlineKeyboardMarkup()
    start_button.add(types.InlineKeyboardButton('Подобрать подарок', callback_data='choose_gift'))
    bot.send_message(call.message.chat.id,
                     f"Ваши данные сохранены! Возраст: {user_data[call.message.chat.id]['age']}, Пол: {user_data[call.message.chat.id]['gender']}, Праздник: {user_data[call.message.chat.id]['occasion']}. Нажмите, чтобы подобрать подарок",
                     reply_markup=start_button)


@bot.callback_query_handler(func=lambda call: call.data == 'choose_gift')
def choose_gift(call):
    user = user_data.get(call.message.chat.id)
    if 'occasion' not in user:
        bot.send_message(call.message.chat.id, 'Не хватает ')
    elif 'age' not in user:
        bot.send_message(call.message.chat.id, 'Возраст не введен или введен некорректно')
    elif 'gender' not in user:
        bot.send_message(call.message.chat.id, 'Пол не найден или введен некорректно')
        start(call.message)
        return
    matching_gifts = []
    for (age_range, gift_gender, gift_holiday), gifts in gift_suggestions.items():
        if int(user['age']) in age_range and user['gender'] == gift_gender and user['occasion'] == gift_holiday:
            matching_gifts.extend(gifts)

    if matching_gifts:
        bot.send_message(call.message.chat.id, f"Рекомендуемые подарки: {', '.join(matching_gifts)}")
    else:
        bot.send_message(call.message.chat.id, "К сожалению, подходящих подарков не найдено")
    restart_markup = types.InlineKeyboardMarkup()
    restart_markup.add(types.InlineKeyboardButton('Начать заново', callback_data='restart'))
    restart_markup.add(types.InlineKeyboardButton('Закончить', callback_data='end'))
    bot.send_message(call.message.chat.id, "Выберите действие:", reply_markup=restart_markup)


@bot.callback_query_handler(func=lambda call: call.data == 'restart')
def restart(call):
    bot.send_message(call.message.chat.id, 'Хорошо, начнём сначала!')
    start(call.message)  # Вызываем обработчик команды /start


@bot.callback_query_handler(func=lambda call: call.data == 'end')
def end(call):
    bot.send_message(call.message.chat.id, 'Спасибо, что воспользовались нашим ботом! 😊')


# Запуск бота
bot.polling()
