from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackQueryHandler
from telegram import InlineKeyboardMarkup, Update, InlineKeyboardButton, ReplyKeyboardMarkup
from dotenv import load_dotenv
import os

# подгружаем переменные окружения
load_dotenv()

# токен бота
TOKEN = os.getenv('TG_TOKEN')

# форма inline клавиатуры
inline_frame = [[InlineKeyboardButton("English", callback_data="english")],
                [InlineKeyboardButton("Русский", callback_data="russia")]]
# создаем inline клавиатуру
inline_keyboard = InlineKeyboardMarkup(inline_frame)

# функция-обработчик команды /start
async def start(update, context):
    await update.message.reply_text('Выбери язык интерфейса', reply_markup=inline_keyboard)

# функция-обработчик текстовых сообщений
async def text(update: Update, context):
    if context.user_data['lang'] == 'english':
        text = 'We’ve received a message from you!'
    else:
        text = 'Текстовое сообщение получено!'

    await update.message.reply_text(text)

# функция-обработчик текстовых сообщений
async def voice(update: Update, context):
    if context.user_data['lang'] == 'english':
        text = 'We’ve received a voice message from you!'
    else:
        text = 'Голосовое сообщение получено'

    await update.message.reply_photo('images/bot_image.jpg', caption=text)

# функция-обработчик текстовых сообщений
async def image(update: Update, context):
    if context.user_data['lang'] == 'english':
        text = 'Photo saved!'
    else:
        text = 'Фотография сохранена'

    photo = await update.message.photo[-1].get_file()
    os.makedirs('photos', exist_ok=True)

    photo_path = f'photos/{photo.file_path.split("/")[-1]}'

    if not os.path.exists(photo_path):
        await photo.download_to_drive(photo_path)

    await update.message.reply_text(text)

# функция-обработчик нажатий на кнопки
async def button(update: Update, context):
    # получаем callback query из update
    query = update.callback_query
    context.user_data['lang'] = query.data
    
    # редактируем сообщение после нажатия
    if context.user_data['lang'] == 'english':
        text = 'You\'ve chosen English!'
    else:
        text = 'Ваш язык - русский'

    await query.edit_message_text(text=text)

def main():

    # создаем приложение и передаем в него токен
    application = Application.builder().token(TOKEN).build()
    print('Бот запущен...')

    # добавляем обработчик команды /start
    application.add_handler(CommandHandler("start", start))
    # application.add_handler(CommandHandler("help", help))

    # добавляем обработчик текстовых сообщений
    application.add_handler(MessageHandler(filters.TEXT, text))

    # добавляем обработчик голосовых сообщений
    application.add_handler(MessageHandler(filters.VOICE, voice))

    # добавляем обработчик изображений
    application.add_handler(MessageHandler(filters.PHOTO, image))

    # добавляем CallbackQueryHandler (только для inline кнопок)
    application.add_handler(CallbackQueryHandler(button))

    # запускаем бота (нажать Ctrl-C для остановки бота)
    application.run_polling()
    print('Бот остановлен')


if __name__ == "__main__":
    main()