import random

import psycopg2
import telebot
from telebot import types

bot = telebot.TeleBot('')

user_data = {}


@bot.message_handler(commands=['start'])
def start(message):
    sex = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    sex.add("Мужчина", "Женщина")
    bot.send_message(message.chat.id, "Привет, я - Бот,который поможет вам выбрать подарки на любой повод! Для начала выберите пол получателя подарка:", reply_markup=sex)

@bot.message_handler(func=lambda message: message.text in ["Мужчина", "Женщина"])
def handle_gender(message):
    user_data[message.chat.id] = {'gender': message.text}
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add("До 13", "14-18", "19-100")
    bot.send_message(message.chat.id, "Укажите возраст получателя:", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text in ["До 13", "14-18", "19-100"])
def handle_age(message):
    if message.chat.id not in user_data:
        user_data[message.chat.id] = {}
    user_data[message.chat.id]['age'] = message.text
    holidays = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    holidays.add("День рождения", "8 марта", "14 февраля")
    holidays.add("23 февраля", "Новый год", "День отца", "День матери")
    bot.send_message(message.chat.id, "Выберите праздник:", reply_markup=holidays)

# Праздник → Бюджет
@bot.message_handler(func=lambda message: message.text in [
    "День рождения", "8 марта", "14 февраля",
    "23 февраля", "Новый год", "День отца", "День матери"
])
def handle_holiday(message):
    if message.chat.id not in user_data:
        user_data[message.chat.id] = {}
    user_data[message.chat.id]['holiday'] = message.text
    budget = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    budget.add("До 50 BYN", "до 70 BYN", "до 100 BYN", "свыше 100 BYN")
    bot.send_message(message.chat.id, "Укажите бюджет:", reply_markup=budget)

# Бюджет → Отношения
@bot.message_handler(func=lambda message: message.text in ["До 50 BYN", "до 70 BYN", "до 100 BYN", "свыше 100 BYN"])
def handle_budget(message):
    if message.chat.id not in user_data:
        user_data[message.chat.id] = {}
    user_data[message.chat.id]['budget'] = message.text
    relation = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    relation.add("Друг", "Коллега", "Мама", "Папа", "Вторая половинка", "Ребенок")
    bot.send_message(message.chat.id, "Кто вам этот человек?", reply_markup=relation)

# Отношения → Получение подарка из базы
@bot.message_handler(func=lambda message: message.text in ["Друг", "Коллега", "Мама", "Папа", "Вторая половинка", "Ребенок"])
def handle_relation(message):
    relation_map = {
        "Мама": "родитель",
        "Папа": "родитель",
        "Друг": "друг",
        "Коллега": "коллега",
        "Вторая половинка": "вторая половинка",
        "Ребенок": "ребенок"
    }
    if message.chat.id not in user_data:
        user_data[message.chat.id] = {}
    user_data[message.chat.id]['relation'] = relation_map[message.text]

    data = user_data[message.chat.id]  # ← добавил эту строку

    gender = data.get('gender')
    age = data.get('age')
    holiday = data.get('holiday')
    budget = data.get('budget')
    relation = data.get('relation')

    gift_message = get_gift_from_db(gender, age, holiday, budget, relation)

    # Отправляем результат пользователю
    bot.send_message(message.chat.id, gift_message)

def get_gift_from_db(gender, age, holiday, budget, relation):
    # Сопоставление названия праздника и имени таблицы
    table_map = {
        "День рождения": "birthday_gifts",
        "Новый год": "new_year_gifts",
        "8 марта": "womens_day_gifts",
        "14 февраля": "lovers_day_gifts",
        "23 февраля": "mans_day_gifts",
        "День отца": "fathers_day_gifts",
        "День матери": "mothers_day_gifts"
    }

    age_map = {
        "До 13": "0-13",
        "14-18": "13-18",
        "19-100": "18-100"
    }

    budget_map = {
        "До 50 BYN": "до 50",
        "до 70 BYN": "до 70",
        "до 100 BYN": "до 100",
        "свыше 100 BYN": "свыше 100"
    }

    gender_map = {
        "Мужчина": "Мужской",
        "Женщина": "Женский"
    }

    table_name = table_map.get(holiday)
    if not table_name:
        return "Не удалось найти таблицу для праздника."

    # Преобразуем значения в те, что в БД
    gender = gender_map.get(gender, gender)
    age = age_map.get(age, age)
    budget = budget_map.get(budget, budget)

    try:
        conn = psycopg2.connect(
            dbname="postgres",
            user="postgres",
            password="password",
            host="localhost",  # или ваш хост
            port="5432"  # или ваш порт
        )
        cursor = conn.cursor()

        # Выполняем запрос с фильтрами
        query = f"""
        SELECT gift_name, gift_number, store 
        FROM {table_name}
        WHERE sex = %s
        AND age = %s
        AND budget = %s
        AND relation = %s
        """
        cursor.execute(query, (gender, age, budget, relation))
        results = cursor.fetchall()
        conn.close()

        if results:
            # Формируем строку с результатами
            gift_details = [f"🎁 Подарок: {gift[0]}, Артикул: {gift[1]}, Магазин: {gift[2]}" for gift in results]
            return "\n".join(gift_details)
        else:
            return "К сожалению, подходящих подарков не найдено."

        question_markup = types.InlineKeyboardMarkup()
        question_markup.add(types.InlineKeyboardButton('Подобрать подарок снова', callback_data='restart_gift'))
        question_markup.add(types.InlineKeyboardButton('Закончить', callback_data='end'))

        bot.send_message(call.message.chat.id, gifts_message, reply_markup=question_markup)

    except Exception as e:
        return f"Ошибка при обращении к базе данных: {e}"

bot.polling()
