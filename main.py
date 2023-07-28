import telebot
import random
from telebot import types

# Список фраз та їх перекладів
phrases = [
    ("напевно, що ні", "probably not", "audio/Probably_not"),
    ("я так не вважаю", "I don`t think so", "audio/I don`t think so.mp3"),
    ("це малоймовірно", "It`s not very likely", "audio/It`s not very likely.mp3"),
    ("швидше за все, що...", "odds are that...", "audio/Odds are that....mp3"),
    ("я переконаний, що...", "I`m convinced that...", "audio/I`m convinced that....mp3"),
    ("я не сумніваюся, що...", "I have no doubt that…", "audio/I have no doubt that….mp3"),
    ("я абсолютно впевнений", "I`m absolutely sure", "audio/I`m absolutely sure.mp3"),
    ("я дуже сумніваюся в цьому", "I seriously doubt it", "audio/I seriously doubt it.mp3"),
    ("існує ймовірність того, що...", "chances are that...", "audio/Chances are that....mp3"),
    ("імовірність цього невелика", "there`s not much chance of that", "audio/There's not much chance of that.mp3"),
    ("я на сто відсотків впевнений", "I`m a hundred percent certain", "audio/I`m a hundred percent certain.mp3"),
    ("я був би дуже здивований, якби це сталося", "I`d be very surprised if that happened", "audio/I`d be very surprised if that happened.mp3")
]

# Словник, що містить об'єкти користувачів
users = {}

# Створення об'єкту бота з токеном
bot = telebot.TeleBot("591620628:AAHtfHRbK4v5z56is4WBHpRc8IZ6S_2qxqU")


# Клас користувача!
class User:
    def __init__(self):
        self.phrase = ""
        self.translation = ""
        self.used_phrases = []
        self.audio_path = []

@bot.message_handler(commands=['help'])
def help(message):
    try:
        user_id = message.from_user.id
        user = choose_phrase(users[user_id])
        phrase = user.translation
        audio_path = user.audio_path
        bot.send_audio(message.chat.id, audio=open(audio_path, 'rb'))
        bot.send_message(message.chat.id, f'<b>{phrase}</b>', parse_mode='html')
    except:
        bot.send_message(message.chat.id, "start with command /start")
# # Функція-обробник команди /start
@bot.message_handler(commands=['start'])
def handle_start(message):
    # Отримання ID користувача
    user_id = message.from_user.id
    # Створення об'єкту користувача, якщо він не існує
    if not user_id in users:
        users[user_id] = User()


    murkup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    button_1 = types.KeyboardButton('probably not')
    button_2 = types.KeyboardButton('I don`t think so')
    button_3 = types.KeyboardButton('It`s not very likely')
    button_4 = types.KeyboardButton('odds are that...')
    button_5 = types.KeyboardButton('I`m convinced that...')
    button_6 = types.KeyboardButton('I have no doubt that…')
    button_7 = types.KeyboardButton('I`m absolutely sure')
    button_8 = types.KeyboardButton('I seriously doubt it')
    button_9 = types.KeyboardButton('chances are that...')
    button_10 = types.KeyboardButton('there`s not much chance of that')
    button_11 = types.KeyboardButton('I`m a hundred percent certain')
    button_12 = types.KeyboardButton('I`d be very surprised if that happened')
    murkup.add(button_1, button_2, button_3, button_4, button_5, button_6, button_7, button_8, button_9, button_10,
               button_11, button_12)
    # Вибір випадкової фрази та перекладу
    user = choose_phrase(users[user_id])
    phrase = user.phrase
    audio_path = user.audio_path
    bot.send_message(message.chat.id, f"Hello {message.chat.first_name}, let's learn useful phrases")
    bot.send_message(message.chat.id, f"Переклади на англійську: {phrase}", reply_markup=murkup)
# Функція-обробник повідомлень
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    # Отримання ID користувача
    user_id = message.from_user.id
    # Створення об'єкту користувача, якщо він не існує
    if not user_id in users:
        users[user_id] = User()
    check_translation(message)

# Функція, яка перевіряє відповідь користувача
def check_translation(message):
    # Отримання ID користувача
    user_id = message.from_user.id

    # Отримання введеної користувачем відповіді та об'єкту користувача
    user_answer = message.text.lower().strip()
    user = users.get(user_id)
    audio_path = user.audio_path

    murkup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    button_1 = types.KeyboardButton('probably not')
    button_2 = types.KeyboardButton('I don`t think so')
    button_3 = types.KeyboardButton('It`s not very likely')
    button_4 = types.KeyboardButton('odds are that...')
    button_5 = types.KeyboardButton('I`m convinced that...')
    button_6 = types.KeyboardButton('I have no doubt that…')
    button_7 = types.KeyboardButton('I`m absolutely sure')
    button_8 = types.KeyboardButton('I seriously doubt it')
    button_9 = types.KeyboardButton('chances are that...')
    button_10 = types.KeyboardButton('there`s not much chance of that')
    button_11 = types.KeyboardButton('I`m a hundred percent certain')
    button_12 = types.KeyboardButton('I`d be very surprised if that happened')
    murkup.add(button_1, button_2, button_3, button_4, button_5, button_6, button_7, button_8, button_9, button_10,
               button_11, button_12)
    if not user:
        user = User()
        users[user_id] = user
        choose_phrase(user)

    # Отримання правильної відповіді
    correct_answer = user.translation.lower()

    # Перевірка відповіді користувача
    if user_answer == correct_answer:
        bot.send_message(message.chat.id, f"Congratulations🎉🎉🎉, {message.chat.first_name}! \"{message.text}\" is the correct answer!\npress any key to continue..")
        bot.send_audio(message.chat.id, audio=open(audio_path, 'rb'))
        choose_phrase(user)
        phrase = user.phrase
        bot.send_message(message.chat.id, f"Переклади на англійську: <b> {phrase}</b>", reply_markup=murkup, parse_mode='html')
    else:
        bot.send_message(message.chat.id, f"Wrong. Try again \n/help")

# Функція, яка вибирає нову фразу для користувача
def choose_phrase(user):
    # Вибір випадкової фрази та перекладу
    phrase, translation, audio = random.choice(phrases)

    # # Перевірка, чи фраза вже була використана
    # while phrase in user.used_phrases:
    #     phrase, translation, audio = random.choice(phrases)
    # # Додавлення фрази до списку використаних
    # user.used_phrases.append(phrase)
    # # Перевірка, чи всі фрази вже були використані
    # if len(user.used_phrases) == len(phrases):
    #     user.used_phrases = []

    # Збереження фрази та її перекладу до об'єкту користувача
    user.phrase = phrase
    user.translation = translation
    user.audio_path = audio
    return user

# Запуск бота
bot.polling()