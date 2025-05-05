from telebot import types


def create_main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Алюминий")
    btn2 = types.KeyboardButton("Медь")
    btn3 = types.KeyboardButton("Никель")
    btn4 = types.KeyboardButton("Цинк")
    btn5 = types.KeyboardButton("Олово")
    btn6 = types.KeyboardButton("Свинец")
    markup.add(btn1, btn2, btn3, btn4, btn5, btn6)
    return markup


def create_data_format_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn2 = types.KeyboardButton("Исторические данные (выбрать период)")
    btn3 = types.KeyboardButton("Актуальные данные")
    btn4 = types.KeyboardButton("Назад")
    markup.add(btn2, btn3, btn4)
    return markup


def create_data_menu(include_back_button=True):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton("Cash, Bid")
    button2 = types.KeyboardButton("Cash, Offer")
    button3 = types.KeyboardButton("3-month, Bid")
    button4 = types.KeyboardButton("3-month, Offer")
    button5 = types.KeyboardButton("Скачать файл Excel")

    # Добавляем кнопки в меню
    markup.add(button1, button2, button3, button4, button5)

    # Добавляем кнопку "Назад", если нужно
    if include_back_button:
        back_button = types.KeyboardButton("Назад")
        markup.add(back_button)

    return markup