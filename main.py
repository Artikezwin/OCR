import telebot

from telebot import types
from auth_data import token
from OCR import text_recognition_tesseract


def telegram_bot(token):
    bot = telebot.TeleBot(token)

    @bot.message_handler(commands=["start"])
    def start_message(message):
        bot.send_message(
            message.chat.id,
            f"Приветствую, {message.from_user.first_name}. Пришлите любую картинку, а я попробую ее распознать. "
            'Для удобства отправьте мне команду /buttons'
        )

    @bot.message_handler(commands=['buttons'])
    def add_buttons(message):
        markup = types.ReplyKeyboardMarkup()  # Объявление объекта для создания кнопок
        start = types.KeyboardButton('/start')  # Создание кнопки
        dollar = types.KeyboardButton('Recognize')  # Создание кнопки
        markup.add(dollar, start)  # Добавление кнопок
        bot.send_message(message.chat.id, 'Выберите нужную вам команду', reply_markup=markup)  # прикрепление кнопок

    @bot.message_handler(content_types=["text"])
    def send_text(message):
        if message.text.lower() == "recognize":
            bot.send_message(message.chat.id, "Пожалуйста пришлите картинку, которую необходимо проанализировать")

            @bot.message_handler(content_types=["photo"])
            def send_result(message_photo):
                file_info = bot.get_file(message_photo.photo[-1].file_id)
                downloaded_file = bot.download_file(file_info.file_path)

                src = 'images-for-test/' + file_info.file_path
                with open(src, 'wb') as new_file:
                    new_file.write(downloaded_file)

                bot.reply_to(message, "Пожалуй, я это проанализирую...")

                text_recognition_tesseract(file_path=src, text_file_name="request-for-user.txt")
                bot.send_document(message_photo.chat.id, open(r"request-for-user.txt"))

        else:
            bot.send_message(message.chat.id, "Я тебя не понимаю... Попробуй пересформулировать вышесказанное")

    bot.polling()


if __name__ == '__main__':
    telegram_bot(token)
