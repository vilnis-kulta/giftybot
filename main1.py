import sqlite3
from unittest.mock import call

import telebot
from pyexpat.errors import messages
from telebot import types

#bot = telebot.TeleBot('8183618236:AAHbYsy-KL0Am1l3qfc6tI_rsGzNFavY3rw') #мой бот
bot = telebot.TeleBot('7717112661:AAFx6LP6q89l_8ful01HrH50gT0mOB28Nps') #бот для колледжа

user_data = {}
gift_suggestions = {
    (range(0, 13), 'Мужской', 'Новый год'): ['Машинка', 'Пистолетик'],
    (range(0, 13), 'Женский', 'Новый год'): ['Кукла', 'Игрушечная кухня'],
    (range(13, 18), 'Мужской', 'Новый год'): ['Настольная игра', 'Наушники'],
    (range(13, 18), 'Женский', 'Новый год'): ['Дневник', 'Скрапбукинг набор'],
    (range(18, 100), 'Мужской', 'Новый год'): ['Часы', 'Книга'],
    (range(18, 100), 'Женский', 'Новый год'): ['Украшение', 'Шарф'],
    (range(0, 13), 'Мужской', 'День рождения'): ['Конструктор LEGO', 'Машинка на пульте управления'],
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
    (range(13, 18), 'Мужской', '23 февраля'): ['Армейский браслет', 'Футболка с военной символикой'],
    (range(18, 100), 'Мужской', '23 февраля'): ['Набор для бритья', 'Фляга с гравировкой'],
    (range(13, 18), 'Женский', '8 марта'): ['Мягкий плед', 'Украшение для интерьера'],
    (range(18, 100), 'Женский', '8 марта'): ['Духи', 'Букет цветов']
}

@bot.message_handler(commands=['start'])
def start(message):
    user_data[message.chat.id] = {}
    bot.send_message(message.chat.id, 'Привет, я - Бот,который поможет вам выбрать подарки на любой повод! Для начала укажите возраст человека, которому будем подбирать подарок')
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


@bot.callback_query_handler(func=lambda call: call.data in ['birthday_gifts','new_year_gifts','14_february_gifts','23_february_gifts','8_march_gifts','mothers_day_gifts', 'fathers_day_gifts'])
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
    bot.send_message(call.message.chat.id, f"Ваши данные сохранены! Возраст: {user_data[call.message.chat.id]['age']}, Пол: {user_data[call.message.chat.id]['gender']}, Праздник: {user_data[call.message.chat.id]['occasion']}. Нажмите, чтобы подобрать подарок", reply_markup=start_button)

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
    restart_markup.add(types.InlineKeyboardButton('Начать заново', callback_data = 'restart'))
    restart_markup.add(types.InlineKeyboardButton('Закончить', callback_data = 'end'))
    bot.send_message(call.message.chat.id,"Выберите действие:",reply_markup=restart_markup)

@bot.callback_query_handler(func=lambda call: call.data == 'restart')
def restart(call):
    bot.send_message(call.message.chat.id, 'Хорошо, начнём сначала!')
    start(call.message)  # Вызываем обработчик команды /start

@bot.callback_query_handler(func=lambda call: call.data == 'end')
def end(call):
    bot.send_message(call.message.chat.id, 'Спасибо, что воспользовались нашим ботом! 😊')

# Запуск бота
bot.polling()
