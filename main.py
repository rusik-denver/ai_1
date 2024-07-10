import os
from dotenv import load_dotenv
from warnings import filterwarnings
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, ConversationHandler, MessageHandler, filters
from telegram.warnings import PTBUserWarning
from _main import *
from _questionnaire import *
from _processing import *
from _contacts import *

filterwarnings(action="ignore", message=r".*CallbackQueryHandler", category=PTBUserWarning)
load_dotenv()
TOKEN = os.getenv('TG_TOKEN')

#get ready directory for images
os.makedirs('images', exist_ok=True)

# функция-обработчик команды /start
async def start(update: Update, context:ContextTypes) -> int:
    #start messages output, except of the last one
    for i in range(len(MESSAGES['start_step']) - 1):
        await update.message.reply_text(MESSAGES['start_step'][i], 
                                        parse_mode=constants.ParseMode.HTML)
        time.sleep(0.15)
    
    #last of start messages output
    await update.message.reply_text(MESSAGES['start_step'][-1], 
                                    parse_mode=constants.ParseMode.HTML, 
                                    reply_markup=ReplyKeyboardMarkup(BUTTONS['start'], 
                                                                     one_time_keyboard=True))
    return LAUNCH

# функция-обработчик команды /cancel
async def cancel(update: Update, context:ContextTypes) -> int:
    await update.message.reply_text(MESSAGES['cancel'])
    context.user_data.clear()
    return ConversationHandler.END

def main() -> None:
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(TOKEN).build()
    print('Бот запущен...')

    # Set up conversation handlers
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            LAUNCH: [CommandHandler('cancel', cancel), MessageHandler(filters.Regex(r'(СТАРТ)$'), launch), MessageHandler(filters.Regex(r'(ОТМЕНА)$'), cancel)],
            ORDER_TYPE: [CommandHandler('cancel', cancel), MessageHandler(filters.Regex(r'(ОТМЕНА)$'), cancel), MessageHandler(filters.TEXT, order_type)],
            SEARCH_TYPE: [CommandHandler('cancel', cancel), MessageHandler(filters.Regex(r'(ОТМЕНА)$'), cancel), MessageHandler(filters.TEXT, search_type)],
            CUSTOM_SEARCH: [CommandHandler('cancel', cancel), MessageHandler(filters.Regex(r'(ОТМЕНА)$'), cancel), MessageHandler(filters.TEXT, custom_search)],
            FILTERS_SEARCH: [CommandHandler('cancel', cancel), MessageHandler(filters.Regex(r'(ОТМЕНА)$'), cancel), MessageHandler(filters.TEXT, filters_search)],
            QUESTIONS_INTRO: [CommandHandler('cancel', cancel), MessageHandler(filters.Regex(r'(ОТМЕНА)$'), cancel), MessageHandler(filters.TEXT, questions_intro)],
            QUESTIONS_PHOTO: [CommandHandler('cancel', cancel), MessageHandler(filters.Regex(r'(ОТМЕНА)$'), cancel), MessageHandler(filters.PHOTO, questions_photo), MessageHandler(filters.Document.IMAGE, questions_photo), MessageHandler(filters.ALL, photo_error)],
            QUESTIONNAIRE: [CommandHandler('cancel', cancel), MessageHandler(filters.Regex(r'(ОТМЕНА)$'), cancel), MessageHandler(filters.TEXT, questionnaire)],
            PROCESSING: [CommandHandler('cancel', cancel), MessageHandler(filters.Regex(r'(ОТМЕНА)$'), cancel), MessageHandler(filters.Regex(r"(ПЕРЕЙТИ К ОБРАБОТКЕ)"), processing), MessageHandler(filters.TEXT, processing)],
            SEARCH_INIT: [CommandHandler('cancel', cancel), MessageHandler(filters.Regex(r'(ОТМЕНА)$'), cancel), MessageHandler(filters.Regex(r"(^#\d{3,}$)"), search_init), MessageHandler(filters.TEXT, search_init)],
            CONTACTS_EMAIL: [CommandHandler('cancel', cancel), MessageHandler(filters.Regex(r'(ОТМЕНА)$'), cancel), MessageHandler(filters.TEXT, contacts_email)],
            CONTACTS_FINISH: [CommandHandler('cancel', cancel), MessageHandler(filters.Regex(r'(ОТМЕНА)$'), cancel), MessageHandler(filters.TEXT, contacts_finish)],
            QUESTION_1: [CommandHandler('cancel', cancel), MessageHandler(filters.Regex(r'(ОТМЕНА)$'), cancel), MessageHandler(filters.TEXT, question_1)], 
            QUESTION_2: [CommandHandler('cancel', cancel), MessageHandler(filters.Regex(r'(ОТМЕНА)$'), cancel), MessageHandler(filters.TEXT, question_2)], 
            QUESTION_3: [CommandHandler('cancel', cancel), MessageHandler(filters.Regex(r'(ОТМЕНА)$'), cancel), MessageHandler(filters.TEXT, question_3)], 
            QUESTION_4: [CommandHandler('cancel', cancel), MessageHandler(filters.Regex(r'(ОТМЕНА)$'), cancel), MessageHandler(filters.TEXT, question_4)], 
            QUESTION_5: [CommandHandler('cancel', cancel), MessageHandler(filters.Regex(r'(ОТМЕНА)$'), cancel), MessageHandler(filters.TEXT, question_5)], 
            QUESTION_6: [CommandHandler('cancel', cancel), MessageHandler(filters.Regex(r'(ОТМЕНА)$'), cancel), MessageHandler(filters.TEXT, question_6)], 
            QUESTION_7: [CommandHandler('cancel', cancel), MessageHandler(filters.Regex(r'(ОТМЕНА)$'), cancel), MessageHandler(filters.TEXT, question_7)], 
            QUESTION_8: [CommandHandler('cancel', cancel), MessageHandler(filters.Regex(r'(ОТМЕНА)$'), cancel), MessageHandler(filters.TEXT, question_8)], 
            QUESTION_9: [CommandHandler('cancel', cancel), MessageHandler(filters.Regex(r'(ОТМЕНА)$'), cancel), MessageHandler(filters.TEXT, question_9)], 
            QUESTION_10: [CommandHandler('cancel', cancel), MessageHandler(filters.Regex(r'(ОТМЕНА)$'), cancel), MessageHandler(filters.TEXT, question_10)], 
            QUESTION_11: [CommandHandler('cancel', cancel), MessageHandler(filters.Regex(r'(ОТМЕНА)$'), cancel), MessageHandler(filters.TEXT, question_11)], 
            QUESTION_12: [CommandHandler('cancel', cancel), MessageHandler(filters.Regex(r'(ОТМЕНА)$'), cancel), MessageHandler(filters.TEXT, question_12)], 
            QUESTION_13: [CommandHandler('cancel', cancel), MessageHandler(filters.Regex(r'(ОТМЕНА)$'), cancel), MessageHandler(filters.TEXT, question_13)], 
            QUESTION_14: [CommandHandler('cancel', cancel), MessageHandler(filters.Regex(r'(ОТМЕНА)$'), cancel), MessageHandler(filters.TEXT, question_14)], 
            QUESTION_15: [CommandHandler('cancel', cancel), MessageHandler(filters.Regex(r'(ОТМЕНА)$'), cancel), MessageHandler(filters.TEXT, question_15)], 
            QUESTION_16: [CommandHandler('cancel', cancel), MessageHandler(filters.Regex(r'(ОТМЕНА)$'), cancel), MessageHandler(filters.TEXT, question_16)], 
            QUESTION_17: [CommandHandler('cancel', cancel), MessageHandler(filters.Regex(r'(ОТМЕНА)$'), cancel), MessageHandler(filters.TEXT, question_17)], 
            QUESTION_18: [CommandHandler('cancel', cancel), MessageHandler(filters.Regex(r'(ОТМЕНА)$'), cancel), MessageHandler(filters.TEXT, question_18)], 
            QUESTION_19: [CommandHandler('cancel', cancel), MessageHandler(filters.Regex(r'(ОТМЕНА)$'), cancel), MessageHandler(filters.TEXT, question_19)], 
            QUESTION_20: [CommandHandler('cancel', cancel), MessageHandler(filters.Regex(r'(ОТМЕНА)$'), cancel), MessageHandler(filters.TEXT, question_20)], 
            QUESTION_21: [CommandHandler('cancel', cancel), MessageHandler(filters.Regex(r'(ОТМЕНА)$'), cancel), MessageHandler(filters.TEXT, question_21)], 
            QUESTION_22: [CommandHandler('cancel', cancel), MessageHandler(filters.Regex(r'(ОТМЕНА)$'), cancel), MessageHandler(filters.TEXT, question_22)], 
            QUESTION_23: [CommandHandler('cancel', cancel), MessageHandler(filters.Regex(r'(ОТМЕНА)$'), cancel), MessageHandler(filters.TEXT, question_23)], 
            QUESTION_24: [CommandHandler('cancel', cancel), MessageHandler(filters.Regex(r'(ОТМЕНА)$'), cancel), MessageHandler(filters.TEXT, question_24)], 
            QUESTION_25: [CommandHandler('cancel', cancel), MessageHandler(filters.Regex(r'(ОТМЕНА)$'), cancel), MessageHandler(filters.TEXT, question_25)],
            QUESTION_26: [CommandHandler('cancel', cancel), MessageHandler(filters.Regex(r'(ОТМЕНА)$'), cancel), MessageHandler(filters.TEXT, question_26)],
            QUESTION_1_CHECK: [CommandHandler('cancel', cancel), MessageHandler(filters.Regex(r'(ОТМЕНА)$'), cancel), MessageHandler(filters.TEXT, question_1_check)],  
            QUESTION_2_CHECK: [CommandHandler('cancel', cancel), MessageHandler(filters.Regex(r'(ОТМЕНА)$'), cancel), MessageHandler(filters.TEXT, question_2_check)], 
            QUESTION_3_CHECK: [CommandHandler('cancel', cancel), MessageHandler(filters.Regex(r'(ОТМЕНА)$'), cancel), MessageHandler(filters.TEXT, question_3_check)], 
            QUESTION_4_CHECK: [CommandHandler('cancel', cancel), MessageHandler(filters.Regex(r'(ОТМЕНА)$'), cancel), MessageHandler(filters.TEXT, question_4_check)], 
            QUESTION_5_CHECK: [CommandHandler('cancel', cancel), MessageHandler(filters.Regex(r'(ОТМЕНА)$'), cancel), MessageHandler(filters.TEXT, question_5_check)], 
            QUESTION_6_CHECK: [CommandHandler('cancel', cancel), MessageHandler(filters.Regex(r'(ОТМЕНА)$'), cancel), MessageHandler(filters.TEXT, question_6_check)], 
            QUESTION_7_CHECK: [CommandHandler('cancel', cancel), MessageHandler(filters.Regex(r'(ОТМЕНА)$'), cancel), MessageHandler(filters.TEXT, question_7_check)], 
            QUESTION_8_CHECK: [CommandHandler('cancel', cancel), MessageHandler(filters.Regex(r'(ОТМЕНА)$'), cancel), MessageHandler(filters.TEXT, question_8_check)], 
            QUESTION_9_CHECK: [CommandHandler('cancel', cancel), MessageHandler(filters.Regex(r'(ОТМЕНА)$'), cancel), MessageHandler(filters.TEXT, question_9_check)], 
            QUESTION_10_CHECK: [CommandHandler('cancel', cancel), MessageHandler(filters.Regex(r'(ОТМЕНА)$'), cancel), MessageHandler(filters.TEXT, question_10_check)], 
            QUESTION_11_CHECK: [CommandHandler('cancel', cancel), MessageHandler(filters.Regex(r'(ОТМЕНА)$'), cancel), MessageHandler(filters.TEXT, question_11_check)], 
            QUESTION_12_CHECK: [CommandHandler('cancel', cancel), MessageHandler(filters.Regex(r'(ОТМЕНА)$'), cancel), MessageHandler(filters.TEXT, question_12_check)], 
            QUESTION_13_CHECK: [CommandHandler('cancel', cancel), MessageHandler(filters.Regex(r'(ОТМЕНА)$'), cancel), MessageHandler(filters.TEXT, question_13_check)], 
            QUESTION_14_CHECK: [CommandHandler('cancel', cancel), MessageHandler(filters.Regex(r'(ОТМЕНА)$'), cancel), MessageHandler(filters.TEXT, question_14_check)], 
            QUESTION_15_CHECK: [CommandHandler('cancel', cancel), MessageHandler(filters.Regex(r'(ОТМЕНА)$'), cancel), MessageHandler(filters.TEXT, question_15_check)], 
            QUESTION_16_CHECK: [CommandHandler('cancel', cancel), MessageHandler(filters.Regex(r'(ОТМЕНА)$'), cancel), MessageHandler(filters.TEXT, question_16_check)], 
            QUESTION_17_CHECK: [CommandHandler('cancel', cancel), MessageHandler(filters.Regex(r'(ОТМЕНА)$'), cancel), MessageHandler(filters.TEXT, question_17_check)], 
            QUESTION_18_CHECK: [CommandHandler('cancel', cancel), MessageHandler(filters.Regex(r'(ОТМЕНА)$'), cancel), MessageHandler(filters.TEXT, question_18_check)], 
            QUESTION_19_CHECK: [CommandHandler('cancel', cancel), MessageHandler(filters.Regex(r'(ОТМЕНА)$'), cancel), MessageHandler(filters.TEXT, question_19_check)], 
            QUESTION_20_CHECK: [CommandHandler('cancel', cancel), MessageHandler(filters.Regex(r'(ОТМЕНА)$'), cancel), MessageHandler(filters.TEXT, question_20_check)], 
            QUESTION_21_CHECK: [CommandHandler('cancel', cancel), MessageHandler(filters.Regex(r'(ОТМЕНА)$'), cancel), MessageHandler(filters.TEXT, question_21_check)], 
            QUESTION_22_CHECK: [CommandHandler('cancel', cancel), MessageHandler(filters.Regex(r'(ОТМЕНА)$'), cancel), MessageHandler(filters.TEXT, question_22_check)], 
            QUESTION_23_CHECK: [CommandHandler('cancel', cancel), MessageHandler(filters.Regex(r'(ОТМЕНА)$'), cancel), MessageHandler(filters.TEXT, question_23_check)], 
            QUESTION_24_CHECK: [CommandHandler('cancel', cancel), MessageHandler(filters.Regex(r'(ОТМЕНА)$'), cancel), MessageHandler(filters.TEXT, question_24_check)], 
            QUESTION_25_CHECK: [CommandHandler('cancel', cancel), MessageHandler(filters.Regex(r'(ОТМЕНА)$'), cancel), MessageHandler(filters.TEXT, question_25_check)], 
            QUESTION_26_CHECK: [CommandHandler('cancel', cancel), MessageHandler(filters.Regex(r'(ОТМЕНА)$'), cancel), MessageHandler(filters.TEXT, question_26_check)], 
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    application.add_handler(conv_handler)

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()