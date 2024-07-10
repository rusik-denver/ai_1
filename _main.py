from telegram import Update, constants, ReplyKeyboardRemove, ReplyKeyboardMarkup
from telegram.ext import ContextTypes
from _funcs import *
from _questionnaire import *
from _processing import *
from _contacts import *
from _photo_processing import from_picture

# launch step
async def launch(update: Update, context:ContextTypes) -> int:
    await update.message.reply_text(MESSAGES['launch_step']['intro'], 
                                    parse_mode=constants.ParseMode.HTML, 
                                    reply_markup=ReplyKeyboardMarkup(BUTTONS['order_type'], 
                                                                    one_time_keyboard=True))
    
    return ORDER_TYPE

#search type step
async def order_type(update: Update, context:ContextTypes) -> int:
    if 'новый заказ' in update.message.text.lower():
        context.user_data.clear()
        context.user_data['order_type'] = 'new_order'
        await update.message.reply_text(MESSAGES['new_order']['questionnaire']['photo_intro'], 
                                        parse_mode=constants.ParseMode.HTML)
        
        return QUESTIONS_PHOTO
    elif 'существующий заказ' in update.message.text.lower():
        context.user_data.clear()
        context.user_data['order_type'] = 'existed'
        await update.message.reply_text(MESSAGES['existed_order']['intro'], 
                                        parse_mode=constants.ParseMode.HTML, 
                                        reply_markup=ReplyKeyboardMarkup(BUTTONS['back_cancel'], 
                                                                         one_time_keyboard=True))
        
        return PROCESSING

# search variables step
async def search_type(update: Update, context:ContextTypes) -> int:
    if 'анкетирование' in update.message.text.lower():
        if 'search_data' in context.user_data.keys():
            search_data = context.user_data['search_data']
        context.user_data.clear()
        context.user_data['search_data'] = search_data
        context.user_data['order_type'] = 'new_order'
        context.user_data['search_type'] = 'questionnaire'
        await update.message.reply_text(MESSAGES['new_order']['questionnaire']['intro'], 
                                        parse_mode=constants.ParseMode.HTML, 
                                        reply_markup=ReplyKeyboardMarkup(BUTTONS['next_back_cancel'], 
                                                                        one_time_keyboard=True))
        
        return QUESTIONS_INTRO
    elif 'поиск по шаблону' in update.message.text.lower():
        if 'search_data' in context.user_data.keys():
            search_data = context.user_data['search_data']
        context.user_data.clear()
        context.user_data['search_data'] = search_data
        context.user_data['order_type'] = 'new_order'
        context.user_data['search_type'] = 'filters'
        await update.message.reply_text(MESSAGES['new_order']['filters']['intro'], 
                                        parse_mode=constants.ParseMode.HTML, 
                                        reply_markup=ReplyKeyboardMarkup(BUTTONS['next_back_cancel'], 
                                                                        one_time_keyboard=True))
        
        return FILTERS_SEARCH
    elif 'произвольный поиск' in update.message.text.lower():
        if 'search_data' in context.user_data.keys():
            search_data = context.user_data['search_data']
        context.user_data.clear()
        context.user_data['search_data'] = search_data
        context.user_data['order_type'] = 'new_order'
        context.user_data['search_type'] = 'custom'
        await update.message.reply_text(MESSAGES['new_order']['custom']['intro'], 
                                        parse_mode=constants.ParseMode.HTML,
                                        reply_markup=ReplyKeyboardMarkup(BUTTONS['next_back_cancel'], 
                                                                            one_time_keyboard=True))
        
        return CUSTOM_SEARCH
    else:
        await update.message.reply_text(MESSAGES['new_order']['intro'], 
                                        parse_mode=constants.ParseMode.HTML, 
                                        reply_markup=ReplyKeyboardMarkup(BUTTONS['search_type'], 
                                                                        one_time_keyboard=True))
            
# custom search step
async def custom_search(update:Update, context:ContextTypes) -> int:
    if 'назад' in update.message.text.lower():
        if 'search_data' in context.user_data.keys():
            search_data = context.user_data['search_data']
        context.user_data.clear()
        context.user_data['search_data'] = search_data
        await update.message.reply_text(MESSAGES['new_order']['intro'], 
                                        parse_mode=constants.ParseMode.HTML, 
                                        reply_markup=ReplyKeyboardMarkup(BUTTONS['search_type'], 
                                                                         one_time_keyboard=True))
        
        return SEARCH_TYPE
    elif 'назад' not in update.message.text.lower() and 'отмена' not in update.message.text.lower():
            await update.message.reply_text(MESSAGES['new_order']['custom']['info'], 
                                            parse_mode=constants.ParseMode.HTML, 
                                            reply_markup=ReplyKeyboardRemove())
            
            return PROCESSING
    else:
        await update.message.reply_text(MESSAGES['new_order']['custom']['info'], 
                                        parse_mode=constants.ParseMode.HTML, 
                                        reply_markup=ReplyKeyboardMarkup(BUTTONS['back_cancel'], 
                                                                            one_time_keyboard=True))

# filters search step
async def filters_search(update:Update, context:ContextTypes) -> int:
    if 'назад' in update.message.text.lower():
        if 'search_data' in context.user_data.keys():
            search_data = context.user_data['search_data']
        context.user_data.clear()
        context.user_data['search_data'] = search_data
        await update.message.reply_text(MESSAGES['new_order']['intro'], 
                                        parse_mode=constants.ParseMode.HTML, 
                                        reply_markup=ReplyKeyboardMarkup(BUTTONS['search_type'], 
                                                                         one_time_keyboard=True))
        
        return SEARCH_TYPE
    elif 'назад' not in update.message.text.lower() and 'отмена' not in update.message.text.lower():
            await update.message.reply_text(MESSAGES['new_order']['filters']['info'], 
                                            parse_mode=constants.ParseMode.HTML)
            
            return PROCESSING
    else:
        await update.message.reply_text(MESSAGES['new_order']['filters']['info'], 
                                        parse_mode=constants.ParseMode.HTML, 
                                        reply_markup=ReplyKeyboardMarkup(BUTTONS['back_cancel'], 
                                                                            one_time_keyboard=True))
    
# questionnair intro step
async def questions_intro(update:Update, context:ContextTypes) -> int:
    if 'назад' in update.message.text.lower():
        if 'search_data' in context.user_data.keys():
            search_data = context.user_data['search_data']
        context.user_data.clear()
        context.user_data['search_data'] = search_data
        await update.message.reply_text(MESSAGES['new_order']['intro'], 
                                        parse_mode=constants.ParseMode.HTML, 
                                        reply_markup=ReplyKeyboardMarkup(BUTTONS['search_type'], 
                                                                         one_time_keyboard=True))
        
        return SEARCH_TYPE
    elif 'продолжить' in update.message.text.lower():
        await update.message.reply_text(MESSAGES['new_order']['questionnaire']['info'], 
                                        parse_mode=constants.ParseMode.HTML, 
                                            reply_markup=ReplyKeyboardMarkup(BUTTONS['next_cancel'], 
                                                                            one_time_keyboard=True))
        
        return QUESTION_4

# questions photo step
async def questions_photo(update: Update, context:ContextTypes) -> int:
    if update.message.photo:
        photo_file = await update.message.photo[-1].get_file()
    elif update.message.document:
        photo_file = await update.message.document.get_file()

    await photo_file.download_to_drive("images/image." + photo_file.file_path.split('.')[-1])


    await update.message.reply_text(MESSAGES['new_order']['questionnaire']['photo_uploaded'], 
                                    parse_mode=constants.ParseMode.HTML)

    res = await questions_photo_processing(update, context)

    if res:
        if res["Тип одежды"][1] < 0.7:
            await update.message.reply_text(MESSAGES['photo']['error'], 
                                            parse_mode=constants.ParseMode.HTML)
        else:
            await update.message.reply_text(MESSAGES['photo']['results'], 
                                            parse_mode=constants.ParseMode.HTML)
            time.sleep(0.15)
            result_string = f'<b>Тип одежды:</b> {res["Тип одежды"][0]}\n' \
                            f'<b>Назначение:</b> {res["Назначение"]}\n' \
                            f'<b>Пол и возраст:</b> {res["Пол и возраст"]}\n' \
                            f'<b>Сезон:</b> {res["Сезон"]}'
            await update.message.reply_text(result_string, 
                                            parse_mode=constants.ParseMode.HTML)
            time.sleep(0.15)
            await update.message.reply_text(MESSAGES['new_order']['intro'], 
                                            parse_mode=constants.ParseMode.HTML, 
                                            reply_markup=ReplyKeyboardMarkup(BUTTONS['search_type'], 
                                                                            one_time_keyboard=True))

            return SEARCH_TYPE
    else:
        return QUESTIONS_PHOTO

#photo processing
async def questions_photo_processing(update: Update, context:ContextTypes) -> int:
    if 'search_data' not in context.user_data.keys():
        context.user_data['search_data'] = {}

    await update.message.reply_text(MESSAGES['new_order']['questionnaire']['photo_processing'],
                                    parse_mode=constants.ParseMode.HTML)
    
    res = from_picture("images/image.jpg")

    if res:
        context.user_data['search_data'][0] = res['Тип одежды']
        context.user_data['search_data'][1] = res['Назначение']
        context.user_data['search_data'][2] = res['Пол и возраст']
        context.user_data['search_data'][26] = res['Сезон']

        return res
    else: 
        return photo_error(update, context)

#photo error
async def photo_error(update: Update, context:ContextTypes) -> int:
    await update.message.reply_text(MESSAGES['new_order']['questionnaire']['photo_error'], 
                                    parse_mode=constants.ParseMode.HTML)
    
    return QUESTIONS_PHOTO

#questions step
async def questionnaire(update: Update, context: ContextTypes) -> int:
    await update.message.reply_text(MESSAGES['new_order']['questionnaire']['info'], 
                                    parse_mode=constants.ParseMode.HTML, 
                                        reply_markup=ReplyKeyboardMarkup(BUTTONS['next_cancel'], 
                                                                         one_time_keyboard=True)) 

    return QUESTION_4
