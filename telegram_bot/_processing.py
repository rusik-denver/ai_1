from telegram import Update, constants, ReplyKeyboardRemove
from telegram.ext import ContextTypes
import re
from _funcs import *
from _questionnaire import *
from _processing import *
from _contacts import *

# processing step
async def processing(update:Update, context:ContextTypes) -> int:
    if 'назад' in update.message.text.lower():
        context.user_data.clear()
        await update.message.reply_text(MESSAGES['new_order']['intro'], 
                                        parse_mode=constants.ParseMode.HTML, 
                                        reply_markup=ReplyKeyboardMarkup(BUTTONS['search_type'], 
                                                                         one_time_keyboard=True))
        return SEARCH_TYPE
    else:
        if re.match(r"(^#)", update.message.text) and not re.match(r"(^#\d{3,}$)", update.message.text):
            await update.message.reply_text(MESSAGES['existed_order']['wrong_order_format'], 
                                            parse_mode=constants.ParseMode.HTML)
        else:
            if 'order_type' in context.user_data.keys() and context.user_data['order_type'] == 'new_order' and 'search_type' in context.user_data.keys() and context.user_data['search_type'] == 'custom':
                entry = update.message.text.split(',')
                context.user_data['order_query'] = list(map(lambda x: x.strip(), entry))
            elif 'order_type' in context.user_data.keys() and context.user_data['order_type'] == 'new_order' and 'search_type' in context.user_data.keys() and context.user_data['search_type'] == 'filters':
                entry = update.message.text.split(';')
                order_query_lst = list(map(lambda x: x.strip(), entry))
                context.user_data['order_query'] = {}

                for i,x in enumerate(order_query_lst):
                    elem = x.replace('[', '').replace(']', '')
                    if elem not in FILTERS:
                        elem = elem.split(',')
                        elem = list(map(lambda x: x.strip(), elem))
                        context.user_data['order_query'].update({FILTERS[i]: elem})
                    else:
                        context.user_data['order_query'].update({FILTERS[i]: []})
            
            context.user_data['entry'] = update.message.text
            await update.message.reply_text(MESSAGES['processing']['init'],
                                        parse_mode=constants.ParseMode.HTML, 
                                        reply_markup=ReplyKeyboardMarkup(BUTTONS['next_cancel'], 
                                                                         one_time_keyboard=True))
            
            return SEARCH_INIT

async def search_init(update: Update, context:ContextTypes) -> int:
    if 'order_type' in context.user_data.keys() and context.user_data['order_type'] == 'existed':
        if re.match(r'(^#\d{3,}$)', update.message.text):
            context.user_data['order_id'] = update.message.text[1:]
        elif 'entry' in context.user_data.keys() and re.match(r'(^#\d{3,}$)', context.user_data['entry']):
            context.user_data['order_id'] = context.user_data['entry'][1:]
        else:
            await update.message.reply_text(MESSAGES['existed_order']['wrong_order_format'],
                                            parse_mode=constants.ParseMode.HTML)
            return SEARCH_INIT

    await update.message.reply_text(MESSAGES['processing']['intro'], 
                                    parse_mode=constants.ParseMode.HTML, 
                                    reply_markup=ReplyKeyboardRemove())
    time.sleep(0.15)
    await update.message.reply_text(MESSAGES['processing']['output_number'], 
                                            parse_mode=constants.ParseMode.HTML)

    return SEARCH

async def search(update: Update, context:ContextTypes) -> int:
    if re.match(r'\d+', update.message.text):
        context.user_data['output_number'] = update.message.text

        await update.message.reply_text(MESSAGES['processing']['contacts']['intro'],
                                        parse_mode=constants.ParseMode.HTML, 
                                        reply_markup=ReplyKeyboardMarkup(BUTTONS['next_cancel'], 
                                                                         one_time_keyboard=True))
        
        return CONTACTS_INTRO
    else:
        await update.message.reply_text(MESSAGES['processing']['wrong_number'],
                                        parse_mode=constants.ParseMode.HTML)
        
        return SEARCH

# # processing step
# async def processing(update: Update, context:ContextTypes) -> int:
#     print('processing stage')
#     # if go back selected go back to choose search type
#     if 'НАЗАД' in update.message.text:
#         await update.message.reply_text(MESSAGES['new_order_intro'], parse_mode=constants.ParseMode.HTML, reply_markup=ReplyKeyboardMarkup(BUTTONS['search_type'], one_time_keyboard=True))
#         return SEARCH_TYPE
#     # if start search selected go to search step
#     elif 'ИСКАТЬ' in update.message.text:
#         await update.message.reply_text(MESSAGES['processing_intro'], parse_mode=constants.ParseMode.HTML, reply_markup=ReplyKeyboardMarkup(BUTTONS['search'], one_time_keyboard=True))
#         return SEARCH
#     elif 'ПЕРЕЙТИ К ОБРАБОТКЕ' in update.message.text:
#         # if 'skip_all' in context.user_data.keys(): del context.user_data['skip_all']
#         # if 'entry' in context.user_data.keys(): del context.user_data['entry']
#         # if 'show_options' in context.user_data.keys(): del context.user_data['show_options']
#         # if 'next_btn' in context.user_data.keys(): del context.user_data['next_btn']
#         await update.message.reply_text(MESSAGES['processing_contacts'], parse_mode=constants.ParseMode.HTML, reply_markup=ReplyKeyboardMarkup(BUTTONS['next_cancel'], one_time_keyboard=True))
#         return NAME
#     # if wrong order format sent, start over
#     else:
#         await update.message.reply_text(MESSAGES['wrong_order_format'], parse_mode=constants.ParseMode.HTML, reply_markup=ReplyKeyboardMarkup(BUTTONS['back'], one_time_keyboard=True))