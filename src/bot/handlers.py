from datetime import datetime
from src.bot.keyboards import create_main_menu, create_data_format_menu, create_data_menu
from src.lme_parser.generate_file import generate_excel
from src.lme_parser.full_parser import AluminiumHistoricData, CopperHistoricData, NickelHistoricData, ZincHistoricData, \
    TinHistoricData, LeadHistoricData
import logging

current_data_type = None  # Может быть "actual" или "historical"
current_metal = None
user_state = {}

metal_data = {
    "Алюминий": AluminiumHistoricData(),
    "Медь": CopperHistoricData(),
    "Никель": NickelHistoricData(),
    "Цинк": ZincHistoricData(),
    "Олово": TinHistoricData(),
    "Свинец": LeadHistoricData()
}


def is_valid_date(date_str):
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def handle_start(message, bot):
    global current_metal
    current_metal = None
    markup = create_main_menu()
    bot.send_message(message.chat.id,
                     text="Здравствуйте, я бот для парсинга данных с сайта LME. Какой металл вас интересует?",
                     reply_markup=markup)


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def handle_text(message, bot):
    global current_data_type, current_metal, user_state

    logger.info(f"User {message.chat.id} sent: {message.text}")
    logger.info(f"Current state: {user_state.get(message.chat.id)}")

    if message.text in metal_data.keys():
        markup = create_data_format_menu()
        bot.send_message(message.chat.id, text="Выберите формат данных", reply_markup=markup)
        current_metal = message.text

    elif message.text == "Актуальные данные":
        current_data_type = "actual"
        markup = create_data_menu()
        bot.send_message(message.chat.id, text="Выберите название из списка", reply_markup=markup)


    elif message.text == "Исторические данные (выбрать период)":
        current_data_type = "historical"
        user_state[message.chat.id] = {"step": "waiting_start_date"}
        bot.send_message(
            message.chat.id,
            # text="Введите начальную дату в формате: YYYY-MM-DD\nИли введите /exit для возврата в главное меню."
            text = "Введите начальную дату в формате: YYYY-MM-DD"
        )

    # elif message.text == "/exit":
    #     current_data_type = None
    #     current_metal = None
    #     if message.chat.id in user_state:
    #         del user_state[message.chat.id]
    #         logger.info(f"State cleared for user {message.chat.id} on '/exit'")
    #
    #     markup = create_main_menu()
    #     bot.send_message(message.chat.id, text="Вы вернулись в главное меню", reply_markup=markup)

    elif message.text == "Назад":
        current_data_type = None
        current_metal = None
        if message.chat.id in user_state:
            user_state.clear()
            logger.info(f"State cleared for user {message.chat.id} on 'Назад'")
        markup = create_main_menu()
        bot.send_message(message.chat.id, text="Вы вернулись в главное меню", reply_markup=markup)

    elif message.chat.id in user_state:
        if user_state[message.chat.id]["step"] == "waiting_start_date":
            if is_valid_date(message.text):
                user_state[message.chat.id]["start_date"] = message.text
                user_state[message.chat.id]["step"] = "waiting_end_date"
                bot.send_message(message.chat.id, text="Введите конечную дату в формате: YYYY-MM-DD")
            else:
                bot.send_message(message.chat.id, text="Некорректный формат даты. Введите дату в формате: YYYY-MM-DD")

        elif user_state[message.chat.id]["step"] == "waiting_end_date":
            if is_valid_date(message.text):
                user_state[message.chat.id]["end_date"] = message.text
                start_date = user_state[message.chat.id]["start_date"]
                end_date = user_state[message.chat.id]["end_date"]

                if datetime.strptime(start_date, "%Y-%m-%d") > datetime.strptime(end_date, "%Y-%m-%d"):
                    bot.send_message(message.chat.id,
                                     text="Начальная дата не может быть позже конечной. Попробуйте снова.")
                    return

                if current_metal == "Алюминий":
                    metal_instance = AluminiumHistoricData(start_date=start_date, end_date=end_date)
                elif current_metal == "Медь":
                    metal_instance = CopperHistoricData(start_date=start_date, end_date=end_date)
                elif current_metal == "Никель":
                    metal_instance = NickelHistoricData(start_date=start_date, end_date=end_date)
                elif current_metal == "Цинк":
                    metal_instance = ZincHistoricData(start_date=start_date, end_date=end_date)
                elif current_metal == "Олово":
                    metal_instance = TinHistoricData(start_date=start_date, end_date=end_date)
                elif current_metal == "Свинец":
                    metal_instance = LeadHistoricData(start_date=start_date, end_date=end_date)
                else:
                    bot.send_message(message.chat.id, text="Ошибка: неизвестный металл")
                    return

                metal_data[current_metal] = metal_instance
                markup = create_data_menu()
                bot.send_message(message.chat.id,
                                 text="Период установлен. Теперь выберите тип данных", reply_markup=markup)

                del user_state[message.chat.id]
                logger.info(f"State cleared for user {message.chat.id}")
            else:
                bot.send_message(message.chat.id, text="Некорректный формат даты. Введите дату в формате: YYYY-MM-DD")

    elif message.text in ["Cash, Bid", "Cash, Offer", "3-month, Bid", "3-month, Offer"]:
        handle_data_selection(message, bot)

    elif message.text == "Скачать файл Excel":
        handle_excel_download(message, bot)

    else:
        bot.send_message(message.chat.id, text="На такую команду я не запрограммирован. Нажмите /start чтобы начать заново")


MAX_MESSAGE_LENGTH = 4096

def send_long_message(bot, chat_id, text):
    lines = text.split("\n")
    message = ""
    for line in lines:
        if len(message) + len(line) + 1 < MAX_MESSAGE_LENGTH:
            message += line + "\n"
        else:
            bot.send_message(chat_id, message.strip())
            message = line + "\n"
    if message:
        bot.send_message(chat_id, message.strip())

def handle_data_selection(message, bot):
    if current_data_type == "actual":
        key_map = {
            "Cash, Bid": 0,
            "Cash, Offer": 1,
            "3-month, Bid": 2,
            "3-month, Offer": 3
        }
        key = key_map.get(message.text)
        if key is not None:
            value = next(reversed(metal_data[current_metal].historical_data.get(key).values()))
            actual_date = next(reversed(metal_data[current_metal].historical_data.get(key).keys()))
            formatted_actual_date = datetime.strptime(actual_date, "%d/%m/%Y").strftime("%d-%m-%Y")
            bot.send_message(message.chat.id,
                             text=f'Дата: {formatted_actual_date}\n{current_metal} LME ({message.text}),$/т: {value}')

    elif current_data_type == "historical":
        key_map = {
            "Cash, Bid": 0,
            "Cash, Offer": 1,
            "3-month, Bid": 2,
            "3-month, Offer": 3
        }
        key = key_map.get(message.text)
        if key is not None:
            data = metal_data[current_metal].historical_data.get(key)
            formatted_data = "\n".join([f"{date:<15} {value}" for date, value in data.items()])

            # Отправляем сообщение безопасно
            send_long_message(bot, message.chat.id, f"{current_metal} LME ({message.text}), $/т:\n{formatted_data}")


def handle_excel_download(message, bot):
    global excel_file
    try:
        excel_file = generate_excel(historical_data=metal_data[current_metal].historical_data,
                                    filename=f"{current_metal}_output.xlsx")
        bot.send_document(
            chat_id=message.chat.id,
            document=excel_file,
            visible_file_name=f"{current_metal}_output.xlsx",
            caption="Вот ваш Excel-файл!"
        )
    except Exception as e:
        bot.send_message(message.chat.id, text=f"Произошла ошибка при генерации файла: {e}")
    finally:
        excel_file.close()
