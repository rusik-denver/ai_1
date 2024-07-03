from telegram import Update, constants, ReplyKeyboardMarkup
from telegram.ext import ContextTypes
from _funcs import *
from _main import *
from _processing import *
from _contacts import *

async def question_1(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    global MESSAGES, QUESTIONS, BUTTONS

    if 'показать опции' in update.message.text.lower() or 'все' in update.message.text.lower():
        _ = await get_options(0, 'все', update, context)
        await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['all_options'], 
                                        parse_mode=constants.ParseMode.HTML, 
                                        reply_markup=ReplyKeyboardMarkup(context.user_data['buttons'], 
                                                                         one_time_keyboard=True))
        
        return QUESTION_1
    elif 'скрыть опции' in update.message.text.lower():
        _ = await get_options(0, 'скрыть', update, context)
        await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['options_cleared'], 
                                        parse_mode=constants.ParseMode.HTML, 
                                        reply_markup=ReplyKeyboardMarkup(BUTTONS['question_buttons_1'], 
                                                                         one_time_keyboard=True))
        
        return QUESTION_1
    elif 'далее' in update.message.text.lower() and ('entry' not in context.user_data.keys() or not context.user_data['entry']):
        await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['prev_question'], 
                                                parse_mode=constants.ParseMode.HTML, 
                                            reply_markup=ReplyKeyboardMarkup(BUTTONS['question_buttons_1'], 
                                                                            one_time_keyboard=True))
        await get_question(0, 'question_buttons_1', update, context)

        return QUESTION_1
    else:
        if ('buttons_raw' in context.user_data.keys() and update.message.text not in context.user_data['buttons_raw']) and ('options_raw' in context.user_data.keys() and update.message.text not in context.user_data['options_raw']):
            _ = await get_options(0, update.message.text, update, context)
            
            if 'options_qty' in context.user_data.keys() and context.user_data['options_qty']:
                button = context.user_data['buttons']
                msg = 'all_options'
            else:
                button = BUTTONS['question_buttons_1']
                msg = 'option_not_found'

            await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions'][msg], 
                                            parse_mode=constants.ParseMode.HTML, 
                                            reply_markup=ReplyKeyboardMarkup(button, 
                                                                            one_time_keyboard=True))
            
            return QUESTION_1
        elif 'options_raw' in context.user_data.keys() and update.message.text in context.user_data['options_raw']:
            context.user_data['entry'] = update.message.text
            await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['question_confirm'], 
                                            parse_mode=constants.ParseMode.HTML, 
                                            reply_markup=ReplyKeyboardMarkup(BUTTONS['question_buttons_1'], 
                                                                            one_time_keyboard=True))
            
            return QUESTION_1_CHECK
        else:
            await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['intro'], 
                                parse_mode=constants.ParseMode.HTML)
            await get_question(0, 'question_buttons_1', update, context)
            _ = await get_options(0, update.message.text, update, context)
            await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['next_btn_alt'], 
                                                    parse_mode=constants.ParseMode.HTML, 
                                                reply_markup=ReplyKeyboardMarkup(BUTTONS['question_buttons_1'], 
                                                                                one_time_keyboard=True))
            
async def question_1_check(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    global MESSAGES

    if 'search_data' not in context.user_data.keys():
        context.user_data['search_data'] = {}

    if 'entry' in context.user_data.keys() and context.user_data['entry']:
        context.user_data['search_data'][0] = context.user_data['entry']
        await clean_temp(update, context)

    await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['next_question'], 
                                            parse_mode=constants.ParseMode.HTML)

    await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['intro'], 
                                parse_mode=constants.ParseMode.HTML)
    await get_question(1, 'question_buttons_1', update, context)
    _ = await get_options(1, update.message.text, update, context)
    await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['next_btn_alt'], 
                                            parse_mode=constants.ParseMode.HTML, 
                                        reply_markup=ReplyKeyboardMarkup(BUTTONS['question_buttons_1'], 
                                                                        one_time_keyboard=True))
    
    return QUESTION_2

async def question_2(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    global MESSAGES, QUESTIONS, BUTTONS

    if 'показать опции' in update.message.text.lower() or update.message.text in QUESTIONS[1]['options']:
        query = 'все'
    else:
        query = update.message.text

    await get_options(1, query, update, context)

    if 'question' not in context.user_data.keys():
        context.user_data['question'] = dict(zip(context.user_data['options_raw'], [False] * len(context.user_data['options_raw'])))
    
    if ('suggestions' not in context.user_data.keys()) or (update.message.text not in context.user_data['options_raw']) or ('показать опции' in update.message.text.lower()):
        context.user_data['suggestions'] = context.user_data['buttons'].copy()
        questions = [x for x,y in context.user_data['question'].items() if y]
        context.user_data['questions_qty'] = len(questions)
        context.user_data['suggestions'] = [x for x in context.user_data['suggestions'] if x[0] not in questions]

    if 'показать опции' in update.message.text.lower() or 'все' in update.message.text.lower():
        suggestions = await get_options(1, 'все', update, context)
        await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['all_options'], 
                                        parse_mode=constants.ParseMode.HTML, 
                                        reply_markup=ReplyKeyboardMarkup(context.user_data['suggestions'], 
                                                                        one_time_keyboard=True))
        
        return QUESTION_2
    elif 'скрыть опции' in update.message.text.lower():
        suggestions = await get_options(1, 'скрыть', update, context)
        await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['options_cleared'], 
                                        parse_mode=constants.ParseMode.HTML, 
                                        reply_markup=ReplyKeyboardMarkup(BUTTONS['question_buttons_1'], 
                                                                        one_time_keyboard=True))
        
        return QUESTION_2_CHECK
    elif 'далее' in update.message.text.lower() and 'questions_qty' in context.user_data.keys() and context.user_data['questions_qty']:
        await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['next_btn_alt'], 
                                                parse_mode=constants.ParseMode.HTML, 
                                            reply_markup=ReplyKeyboardMarkup(BUTTONS['question_buttons_1'], 
                                                                            one_time_keyboard=True))

        return QUESTION_2_CHECK
    elif 'далее' in update.message.text.lower() and ('questions_qty' in context.user_data.keys() and not context.user_data['questions_qty']):
        await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['prev_question'], 
                                                parse_mode=constants.ParseMode.HTML, 
                                                reply_markup=ReplyKeyboardMarkup(BUTTONS['question_buttons_1'], 
                                                                            one_time_keyboard=True))
        await get_question(1, 'question_buttons_1', update, context)

        return QUESTION_2
    else:
        if ('buttons_raw' in context.user_data.keys() and update.message.text not in context.user_data['buttons_raw']) and ('options_raw' in context.user_data.keys() and update.message.text not in context.user_data['options_raw']):
            _ = await get_options(1, update.message.text, update, context)
            
            if 'options_qty' in context.user_data.keys() and context.user_data['options_qty']:
                button = context.user_data['buttons']
                msg = 'all_options'
            else:
                button = BUTTONS['question_buttons_1']
                msg = 'option_not_found'

            await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions'][msg], 
                                            parse_mode=constants.ParseMode.HTML, 
                                            reply_markup=ReplyKeyboardMarkup(button, 
                                                                            one_time_keyboard=True))
            
            return QUESTION_2
        elif 'options_raw' in context.user_data.keys() and update.message.text in context.user_data['options_raw']:
            context.user_data['question'][update.message.text] = True
            context.user_data['suggestions'] = context.user_data['buttons'].copy()
            questions = [x for x,y in context.user_data['question'].items() if y]
            context.user_data['questions_qty'] = len(questions)
            context.user_data['suggestions'] = [x for x in context.user_data['suggestions'] if x[0] not in questions]
            context.user_data['suggestions'] = map(lambda x: x.remove(update.message.text) if (update.message.text in x) and (update.message.text not in context.user_data['buttons_raw']) else x, context.user_data['suggestions'])
            context.user_data['suggestions'] = [i for i in context.user_data['suggestions'] if i]

            await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['question_confirm'], 
                                        parse_mode=constants.ParseMode.HTML, 
                                        reply_markup=ReplyKeyboardMarkup(context.user_data['suggestions'], 
                                                                        one_time_keyboard=True))
                
async def question_2_check(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    global MESSAGES

    if 'search_data' in context.user_data.keys() and '1' not in str(context.user_data['search_data'].keys()):
        context.user_data['search_data'][1] = [x for x,y in context.user_data['question'].items() if y]
        await clean_temp(update, context)

    await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['next_question'], 
                                            parse_mode=constants.ParseMode.HTML)

    await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['intro'], 
                                parse_mode=constants.ParseMode.HTML)
    await get_question(2, 'question_buttons', update, context)
    _ = await get_options(2, update.message.text, update, context)
    await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['next_btn'], 
                                            parse_mode=constants.ParseMode.HTML, 
                                        reply_markup=ReplyKeyboardMarkup(BUTTONS['question_buttons'], 
                                                                        one_time_keyboard=True))
    
    return QUESTION_3

async def question_3(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    global MESSAGES, QUESTIONS, BUTTONS

    if 'показать опции' in update.message.text.lower() or update.message.text in QUESTIONS[2]['options']:
        query = 'все'
    else:
        query = update.message.text

    await get_options(2, query, update, context)

    if 'question' not in context.user_data.keys():
        context.user_data['question'] = dict(zip(context.user_data['options_raw'], [False] * len(context.user_data['options_raw'])))
    
    if ('suggestions' not in context.user_data.keys()) or (update.message.text not in context.user_data['options_raw']) or ('показать опции' in update.message.text.lower()):
        context.user_data['suggestions'] = context.user_data['buttons'].copy()
        questions = [x for x,y in context.user_data['question'].items() if y]
        context.user_data['questions_qty'] = len(questions)
        context.user_data['suggestions'] = [x for x in context.user_data['suggestions'] if x[0] not in questions]

    if 'показать опции' in update.message.text.lower() or 'все' in update.message.text.lower():
        suggestions = await get_options(2, 'все', update, context)
        await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['all_options'], 
                                        parse_mode=constants.ParseMode.HTML, 
                                        reply_markup=ReplyKeyboardMarkup(context.user_data['suggestions'], 
                                                                        one_time_keyboard=True))
        
        return QUESTION_3
    elif 'скрыть опции' in update.message.text.lower():
        suggestions = await get_options(2, 'скрыть', update, context)
        await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['options_cleared'], 
                                        parse_mode=constants.ParseMode.HTML, 
                                        reply_markup=ReplyKeyboardMarkup(BUTTONS['question_buttons'], 
                                                                        one_time_keyboard=True))
        
        return QUESTION_3_CHECK
    elif 'пропустить вс' in update.message.text.lower():
        print('skip all',update.message.text.lower())
        await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['skip_all_confirm'], 
                                        parse_mode=constants.ParseMode.HTML, 
                                        reply_markup=ReplyKeyboardMarkup(BUTTONS['skip_all_yes'], 
                                                                        one_time_keyboard=True))
        return QUESTION_3_CHECK
    elif 'пропустить' in update.message.text.lower():
        print('skip',update.message.text.lower())
        await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['skip_confirm'], 
                                        parse_mode=constants.ParseMode.HTML, 
                                        reply_markup=ReplyKeyboardMarkup(BUTTONS['skip_yes'], 
                                                                        one_time_keyboard=True))
        return QUESTION_3_CHECK
    elif 'далее' in update.message.text.lower() and 'questions_qty' in context.user_data.keys() and context.user_data['questions_qty']:
        await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['next_btn'], 
                                                parse_mode=constants.ParseMode.HTML, 
                                            reply_markup=ReplyKeyboardMarkup(BUTTONS['question_buttons'], 
                                                                            one_time_keyboard=True))

        return QUESTION_3_CHECK
    elif 'далее' in update.message.text.lower() and ('questions_qty' in context.user_data.keys() and not context.user_data['questions_qty']):
        await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['prev_question'], 
                                                parse_mode=constants.ParseMode.HTML, 
                                                reply_markup=ReplyKeyboardMarkup(BUTTONS['question_buttons'], 
                                                                            one_time_keyboard=True))
        await get_question(2, 'question_buttons', update, context)

        return QUESTION_3
    else:
        if ('buttons_raw' in context.user_data.keys() and update.message.text not in context.user_data['buttons_raw']) and ('options_raw' in context.user_data.keys() and update.message.text not in context.user_data['options_raw']):
            _ = await get_options(2, update.message.text, update, context)
            
            if 'options_qty' in context.user_data.keys() and context.user_data['options_qty']:
                button = context.user_data['buttons']
                msg = 'all_options'
            else:
                button = BUTTONS['question_buttons']
                msg = 'option_not_found'

            await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions'][msg], 
                                            parse_mode=constants.ParseMode.HTML, 
                                            reply_markup=ReplyKeyboardMarkup(button, 
                                                                            one_time_keyboard=True))
            
            return QUESTION_3
        elif 'options_raw' in context.user_data.keys() and update.message.text in context.user_data['options_raw']:
            context.user_data['question'][update.message.text] = True
            context.user_data['suggestions'] = context.user_data['buttons'].copy()
            questions = [x for x,y in context.user_data['question'].items() if y]
            context.user_data['questions_qty'] = len(questions)
            context.user_data['suggestions'] = [x for x in context.user_data['suggestions'] if x[0] not in questions]
            context.user_data['suggestions'] = map(lambda x: x.remove(update.message.text) if (update.message.text in x) and (update.message.text not in context.user_data['buttons_raw']) else x, context.user_data['suggestions'])
            context.user_data['suggestions'] = [i for i in context.user_data['suggestions'] if i]

            await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['question_confirm'], 
                                        parse_mode=constants.ParseMode.HTML, 
                                        reply_markup=ReplyKeyboardMarkup(context.user_data['suggestions'], 
                                                                        one_time_keyboard=True))

async def question_3_check(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if 'передумал' in update.message.text.lower():
        await get_question(2, 'question_buttons', update, context)
        _ = await get_options(2, update.message.text, update, context)
        await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['next_btn'], 
                                                parse_mode=constants.ParseMode.HTML, 
                                            reply_markup=ReplyKeyboardMarkup(BUTTONS['question_buttons'], 
                                                                            one_time_keyboard=True))
        return QUESTION_3
    elif 'да, пропустить вс' in update.message.text.lower():
        await update.message.reply_text(MESSAGES['processing']['intro'], 
                                                parse_mode=constants.ParseMode.HTML)
        await update.message.reply_text(MESSAGES['processing']['contacts']['intro'], 
                                                parse_mode=constants.ParseMode.HTML, 
                                            reply_markup=ReplyKeyboardMarkup(BUTTONS['next_cancel'], 
                                                                            one_time_keyboard=True))
        return PROCESSING
    else:
        if 'search_data' in context.user_data.keys() and '2' not in str(context.user_data['search_data'].keys()):
            context.user_data['search_data'][2] = [x for x,y in context.user_data['question'].items() if y]
            await clean_temp(update, context)

        await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['next_question'], 
                                                parse_mode=constants.ParseMode.HTML)

        await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['intro'], 
                                    parse_mode=constants.ParseMode.HTML)
        await get_question(3, 'question_buttons', update, context)
        _ = await get_options(3, update.message.text, update, context)
        await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['next_btn'], 
                                                parse_mode=constants.ParseMode.HTML, 
                                            reply_markup=ReplyKeyboardMarkup(BUTTONS['question_buttons'], 
                                                                            one_time_keyboard=True))
        return QUESTION_4

async def question_4(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    global MESSAGES, QUESTIONS, BUTTONS

    if 'показать опции' in update.message.text.lower() or 'все' in update.message.text.lower():
        _ = await get_options(3, 'все', update, context)
        await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['all_options'], 
                                        parse_mode=constants.ParseMode.HTML, 
                                        reply_markup=ReplyKeyboardMarkup(context.user_data['buttons'], 
                                                                         one_time_keyboard=True))
        
        return QUESTION_4
    elif 'скрыть опции' in update.message.text.lower():
        _ = await get_options(3, 'скрыть', update, context)
        await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['options_cleared'], 
                                        parse_mode=constants.ParseMode.HTML, 
                                        reply_markup=ReplyKeyboardMarkup(BUTTONS['question_buttons'], 
                                                                         one_time_keyboard=True))
        
        return QUESTION_4
    elif 'пропустить вс' in update.message.text.lower():
        await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['skip_confirm'], 
                                        parse_mode=constants.ParseMode.HTML, 
                                        reply_markup=ReplyKeyboardMarkup(BUTTONS['skip_all_yes'], 
                                                                        one_time_keyboard=True))
        return QUESTION_4_CHECK
    elif 'пропустить' in update.message.text.lower():
        await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['skip_confirm'], 
                                        parse_mode=constants.ParseMode.HTML, 
                                        reply_markup=ReplyKeyboardMarkup(BUTTONS['skip_yes'], 
                                                                        one_time_keyboard=True))
        return QUESTION_4_CHECK
    elif 'далее' in update.message.text.lower() and ('entry' not in context.user_data.keys() or not context.user_data['entry']):
        await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['prev_question'], 
                                                parse_mode=constants.ParseMode.HTML, 
                                            reply_markup=ReplyKeyboardMarkup(BUTTONS['question_buttons'], 
                                                                            one_time_keyboard=True))
        await get_question(3, 'question_buttons', update, context)

        return QUESTION_4
    else:
        if ('buttons_raw' in context.user_data.keys() and update.message.text not in context.user_data['buttons_raw']) and ('options_raw' in context.user_data.keys() and update.message.text not in context.user_data['options_raw']):
            _ = await get_options(3, update.message.text, update, context)
            
            if 'options_qty' in context.user_data.keys() and context.user_data['options_qty']:
                button = context.user_data['buttons']
                msg = 'all_options'
            else:
                button = BUTTONS['question_buttons']
                msg = 'option_not_found'

            await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions'][msg], 
                                            parse_mode=constants.ParseMode.HTML, 
                                            reply_markup=ReplyKeyboardMarkup(button, 
                                                                            one_time_keyboard=True))
            
            return QUESTION_4
        elif 'options_raw' in context.user_data.keys() and update.message.text in context.user_data['options_raw']:
            context.user_data['entry'] = update.message.text
            await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['question_confirm'], 
                                            parse_mode=constants.ParseMode.HTML, 
                                            reply_markup=ReplyKeyboardMarkup(BUTTONS['question_buttons'], 
                                                                            one_time_keyboard=True))
            
            return QUESTION_4_CHECK
        else:
            await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['intro'], 
                                parse_mode=constants.ParseMode.HTML)
            await get_question(3, 'question_buttons', update, context)
            _ = await get_options(3, update.message.text, update, context)
            await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['next_btn_alt'], 
                                                    parse_mode=constants.ParseMode.HTML, 
                                                reply_markup=ReplyKeyboardMarkup(BUTTONS['question_buttons'], 
                                                                                one_time_keyboard=True))

async def question_4_check(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if 'передумал' in update.message.text.lower():
        await get_question(3, 'question_buttons', update, context)
        _ = await get_options(3, update.message.text, update, context)
        await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['next_btn'], 
                                                parse_mode=constants.ParseMode.HTML, 
                                            reply_markup=ReplyKeyboardMarkup(BUTTONS['question_buttons'], 
                                                                            one_time_keyboard=True))
        return QUESTION_4
    elif 'да, пропустить вс' in update.message.text.lower():
        await update.message.reply_text(MESSAGES['processing']['intro'], 
                                                parse_mode=constants.ParseMode.HTML)
        await update.message.reply_text(MESSAGES['processing']['contacts']['intro'], 
                                                parse_mode=constants.ParseMode.HTML, 
                                            reply_markup=ReplyKeyboardMarkup(BUTTONS['next_cancel'], 
                                                                            one_time_keyboard=True))
        return PROCESSING   
    else:
        if 'search_data' in context.user_data.keys() and '3' not in str(context.user_data['search_data'].keys()):
            context.user_data['search_data'][3] = context.user_data['entry']
            await clean_temp(update, context)

        await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['next_question'], 
                                                parse_mode=constants.ParseMode.HTML)

        await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['intro'], 
                                    parse_mode=constants.ParseMode.HTML)
        await get_question(4, 'question_buttons', update, context)
        _ = await get_options(4, update.message.text, update, context)
        await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['next_btn'], 
                                                parse_mode=constants.ParseMode.HTML, 
                                            reply_markup=ReplyKeyboardMarkup(BUTTONS['question_buttons'], 
                                                                            one_time_keyboard=True))
        return QUESTION_5

async def question_5(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    global MESSAGES, QUESTIONS, BUTTONS

    if 'показать опции' in update.message.text.lower() or 'все' in update.message.text.lower():
        _ = await get_options(4, 'все', update, context)
        await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['all_options'], 
                                        parse_mode=constants.ParseMode.HTML, 
                                        reply_markup=ReplyKeyboardMarkup(context.user_data['buttons'], 
                                                                         one_time_keyboard=True))
        
        return QUESTION_5
    elif 'скрыть опции' in update.message.text.lower():
        _ = await get_options(4, 'скрыть', update, context)
        await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['options_cleared'], 
                                        parse_mode=constants.ParseMode.HTML, 
                                        reply_markup=ReplyKeyboardMarkup(BUTTONS['question_buttons'], 
                                                                         one_time_keyboard=True))
        
        return QUESTION_5
    elif 'пропустить вс' in update.message.text.lower():
        await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['skip_confirm'], 
                                        parse_mode=constants.ParseMode.HTML, 
                                        reply_markup=ReplyKeyboardMarkup(BUTTONS['skip_all_yes'], 
                                                                        one_time_keyboard=True))
        return QUESTION_5_CHECK
    elif 'пропустить' in update.message.text.lower():
        await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['skip_confirm'], 
                                        parse_mode=constants.ParseMode.HTML, 
                                        reply_markup=ReplyKeyboardMarkup(BUTTONS['skip_yes'], 
                                                                        one_time_keyboard=True))
        return QUESTION_5_CHECK
    elif 'далее' in update.message.text.lower() and ('entry' not in context.user_data.keys() or not context.user_data['entry']):
        await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['prev_question'], 
                                                parse_mode=constants.ParseMode.HTML, 
                                            reply_markup=ReplyKeyboardMarkup(BUTTONS['question_buttons'], 
                                                                            one_time_keyboard=True))
        await get_question(4, 'question_buttons', update, context)

        return QUESTION_5
    else:
        if ('buttons_raw' in context.user_data.keys() and update.message.text not in context.user_data['buttons_raw']) and ('options_raw' in context.user_data.keys() and update.message.text not in context.user_data['options_raw']):
            _ = await get_options(4, update.message.text, update, context)
            
            if 'options_qty' in context.user_data.keys() and context.user_data['options_qty']:
                button = context.user_data['buttons']
                msg = 'all_options'
            else:
                button = BUTTONS['question_buttons']
                msg = 'option_not_found'

            await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions'][msg], 
                                            parse_mode=constants.ParseMode.HTML, 
                                            reply_markup=ReplyKeyboardMarkup(button, 
                                                                            one_time_keyboard=True))
            
            return QUESTION_5
        elif 'options_raw' in context.user_data.keys() and update.message.text in context.user_data['options_raw']:
            context.user_data['entry'] = update.message.text
            await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['question_confirm'], 
                                            parse_mode=constants.ParseMode.HTML, 
                                            reply_markup=ReplyKeyboardMarkup(BUTTONS['question_buttons'], 
                                                                            one_time_keyboard=True))
            
            return QUESTION_5_CHECK
        else:
            await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['intro'], 
                                parse_mode=constants.ParseMode.HTML)
            await get_question(4, 'question_buttons', update, context)
            _ = await get_options(4, update.message.text, update, context)
            await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['next_btn_alt'], 
                                                    parse_mode=constants.ParseMode.HTML, 
                                                reply_markup=ReplyKeyboardMarkup(BUTTONS['question_buttons'], 
                                                                                one_time_keyboard=True))

async def question_5_check(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if 'передумал' in update.message.text.lower():
        await get_question(4, 'question_buttons', update, context)
        _ = await get_options(4, update.message.text, update, context)
        await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['next_btn'], 
                                                parse_mode=constants.ParseMode.HTML, 
                                            reply_markup=ReplyKeyboardMarkup(BUTTONS['question_buttons'], 
                                                                            one_time_keyboard=True))
        return QUESTION_5
    elif 'да, пропустить вс' in update.message.text.lower():
        await update.message.reply_text(MESSAGES['processing']['intro'], 
                                                parse_mode=constants.ParseMode.HTML)
        await update.message.reply_text(MESSAGES['processing']['contacts']['intro'], 
                                                parse_mode=constants.ParseMode.HTML, 
                                            reply_markup=ReplyKeyboardMarkup(BUTTONS['next_cancel'], 
                                                                            one_time_keyboard=True))
        return PROCESSING 
    else:
        if 'search_data' in context.user_data.keys() and '4' not in str(context.user_data['search_data'].keys()):
            context.user_data['search_data'][4] = context.user_data['entry']
            await clean_temp(update, context)

        await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['next_question'], 
                                                parse_mode=constants.ParseMode.HTML)

        await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['intro'], 
                                    parse_mode=constants.ParseMode.HTML)
        await get_question(5, 'question_buttons', update, context)
        _ = await get_options(5, update.message.text, update, context)
        await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['next_btn'], 
                                                parse_mode=constants.ParseMode.HTML, 
                                            reply_markup=ReplyKeyboardMarkup(BUTTONS['question_buttons'], 
                                                                            one_time_keyboard=True))
        return QUESTION_6

async def question_6(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    global MESSAGES, QUESTIONS, BUTTONS

    if 'показать опции' in update.message.text.lower() or update.message.text in QUESTIONS[5]['options']:
        query = 'все'
    else:
        query = update.message.text

    await get_options(5, query, update, context)

    if 'question' not in context.user_data.keys():
        context.user_data['question'] = dict(zip(context.user_data['options_raw'], [False] * len(context.user_data['options_raw'])))
    
    if ('suggestions' not in context.user_data.keys()) or (update.message.text not in context.user_data['options_raw']) or ('показать опции' in update.message.text.lower()):
        context.user_data['suggestions'] = context.user_data['buttons'].copy()
        questions = [x for x,y in context.user_data['question'].items() if y]
        context.user_data['questions_qty'] = len(questions)
        context.user_data['suggestions'] = [x for x in context.user_data['suggestions'] if x[0] not in questions]

    if 'показать опции' in update.message.text.lower() or 'все' in update.message.text.lower():
        suggestions = await get_options(5, 'все', update, context)
        await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['all_options'], 
                                        parse_mode=constants.ParseMode.HTML, 
                                        reply_markup=ReplyKeyboardMarkup(context.user_data['suggestions'], 
                                                                        one_time_keyboard=True))
        
        return QUESTION_6
    elif 'скрыть опции' in update.message.text.lower():
        suggestions = await get_options(5, 'скрыть', update, context)
        await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['options_cleared'], 
                                        parse_mode=constants.ParseMode.HTML, 
                                        reply_markup=ReplyKeyboardMarkup(BUTTONS['question_buttons'], 
                                                                        one_time_keyboard=True))
        
        return QUESTION_6_CHECK
    elif 'пропустить вс' in update.message.text.lower():
        await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['skip_confirm'], 
                                        parse_mode=constants.ParseMode.HTML, 
                                        reply_markup=ReplyKeyboardMarkup(BUTTONS['skip_all_yes'], 
                                                                        one_time_keyboard=True))
        return QUESTION_6_CHECK
    elif 'пропустить' in update.message.text.lower():
        await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['skip_confirm'], 
                                        parse_mode=constants.ParseMode.HTML, 
                                        reply_markup=ReplyKeyboardMarkup(BUTTONS['skip_yes'], 
                                                                        one_time_keyboard=True))
        return QUESTION_6_CHECK
    elif 'далее' in update.message.text.lower() and 'questions_qty' in context.user_data.keys() and context.user_data['questions_qty']:
        await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['next_btn'], 
                                                parse_mode=constants.ParseMode.HTML, 
                                            reply_markup=ReplyKeyboardMarkup(BUTTONS['question_buttons'], 
                                                                            one_time_keyboard=True))

        return QUESTION_6_CHECK
    elif 'далее' in update.message.text.lower() and ('questions_qty' in context.user_data.keys() and not context.user_data['questions_qty']):
        await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['prev_question'], 
                                                parse_mode=constants.ParseMode.HTML, 
                                                reply_markup=ReplyKeyboardMarkup(BUTTONS['question_buttons'], 
                                                                            one_time_keyboard=True))
        await get_question(5, 'question_buttons', update, context)

        return QUESTION_6
    else:
        if ('buttons_raw' in context.user_data.keys() and update.message.text not in context.user_data['buttons_raw']) and ('options_raw' in context.user_data.keys() and update.message.text not in context.user_data['options_raw']):
            _ = await get_options(5, update.message.text, update, context)
            
            if 'options_qty' in context.user_data.keys() and context.user_data['options_qty']:
                button = context.user_data['buttons']
                msg = 'all_options'
            else:
                button = BUTTONS['question_buttons']
                msg = 'option_not_found'

            await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions'][msg], 
                                            parse_mode=constants.ParseMode.HTML, 
                                            reply_markup=ReplyKeyboardMarkup(button, 
                                                                            one_time_keyboard=True))
            
            return QUESTION_6
        elif 'options_raw' in context.user_data.keys() and update.message.text in context.user_data['options_raw']:
            context.user_data['question'][update.message.text] = True
            context.user_data['suggestions'] = context.user_data['buttons'].copy()
            questions = [x for x,y in context.user_data['question'].items() if y]
            context.user_data['questions_qty'] = len(questions)
            context.user_data['suggestions'] = [x for x in context.user_data['suggestions'] if x[0] not in questions]
            context.user_data['suggestions'] = map(lambda x: x.remove(update.message.text) if (update.message.text in x) and (update.message.text not in context.user_data['buttons_raw']) else x, context.user_data['suggestions'])
            context.user_data['suggestions'] = [i for i in context.user_data['suggestions'] if i]

            await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['question_confirm'], 
                                        parse_mode=constants.ParseMode.HTML, 
                                        reply_markup=ReplyKeyboardMarkup(context.user_data['suggestions'], 
                                                                        one_time_keyboard=True))

async def question_6_check(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if 'передумал' in update.message.text.lower():
        await get_question(5, 'question_buttons', update, context)
        _ = await get_options(5, update.message.text, update, context)
        await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['next_btn'], 
                                                parse_mode=constants.ParseMode.HTML, 
                                            reply_markup=ReplyKeyboardMarkup(BUTTONS['question_buttons'], 
                                                                            one_time_keyboard=True))
        return QUESTION_6
    elif 'да, пропустить вс' in update.message.text.lower():
        await update.message.reply_text(MESSAGES['processing']['intro'], 
                                                parse_mode=constants.ParseMode.HTML)
        await update.message.reply_text(MESSAGES['processing']['contacts']['intro'], 
                                                parse_mode=constants.ParseMode.HTML, 
                                            reply_markup=ReplyKeyboardMarkup(BUTTONS['next_cancel'], 
                                                                            one_time_keyboard=True))
        return PROCESSING 
    else:
        if 'search_data' in context.user_data.keys() and '5' not in str(context.user_data['search_data'].keys()):
            context.user_data['search_data'][5] = [x for x,y in context.user_data['question'].items() if y]
            await clean_temp(update, context)

        await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['next_question'], 
                                                parse_mode=constants.ParseMode.HTML)

        await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['intro'], 
                                    parse_mode=constants.ParseMode.HTML)
        await get_question(6, 'question_buttons', update, context)
        _ = await get_options(6, update.message.text, update, context)
        await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['next_btn'], 
                                                parse_mode=constants.ParseMode.HTML, 
                                            reply_markup=ReplyKeyboardMarkup(BUTTONS['question_buttons'], 
                                                                            one_time_keyboard=True))
        return QUESTION_7

async def question_7(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    global MESSAGES, QUESTIONS, BUTTONS

    if 'показать опции' in update.message.text.lower() or 'все' in update.message.text.lower():
        _ = await get_options(6, 'все', update, context)
        await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['all_options'], 
                                        parse_mode=constants.ParseMode.HTML, 
                                        reply_markup=ReplyKeyboardMarkup(context.user_data['buttons'], 
                                                                         one_time_keyboard=True))
        
        return QUESTION_7
    elif 'скрыть опции' in update.message.text.lower():
        _ = await get_options(6, 'скрыть', update, context)
        await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['options_cleared'], 
                                        parse_mode=constants.ParseMode.HTML, 
                                        reply_markup=ReplyKeyboardMarkup(BUTTONS['question_buttons'], 
                                                                         one_time_keyboard=True))
        
        return QUESTION_7
    elif 'пропустить вс' in update.message.text.lower():
        await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['skip_confirm'], 
                                        parse_mode=constants.ParseMode.HTML, 
                                        reply_markup=ReplyKeyboardMarkup(BUTTONS['skip_all_yes'], 
                                                                        one_time_keyboard=True))
        return QUESTION_7_CHECK
    elif 'пропустить' in update.message.text.lower():
        await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['skip_confirm'], 
                                        parse_mode=constants.ParseMode.HTML, 
                                        reply_markup=ReplyKeyboardMarkup(BUTTONS['skip_yes'], 
                                                                        one_time_keyboard=True))
        return QUESTION_7_CHECK
    elif 'далее' in update.message.text.lower() and ('entry' not in context.user_data.keys() or not context.user_data['entry']):
        await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['prev_question'], 
                                                parse_mode=constants.ParseMode.HTML, 
                                            reply_markup=ReplyKeyboardMarkup(BUTTONS['question_buttons'], 
                                                                            one_time_keyboard=True))
        await get_question(6, 'question_buttons', update, context)

        return QUESTION_7
    else:
        if ('buttons_raw' in context.user_data.keys() and update.message.text not in context.user_data['buttons_raw']) and ('options_raw' in context.user_data.keys() and update.message.text not in context.user_data['options_raw']):
            _ = await get_options(6, update.message.text, update, context)
            
            if 'options_qty' in context.user_data.keys() and context.user_data['options_qty']:
                button = context.user_data['buttons']
                msg = 'all_options'
            else:
                button = BUTTONS['question_buttons']
                msg = 'option_not_found'

            await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions'][msg], 
                                            parse_mode=constants.ParseMode.HTML, 
                                            reply_markup=ReplyKeyboardMarkup(button, 
                                                                            one_time_keyboard=True))
            
            return QUESTION_7
        elif 'options_raw' in context.user_data.keys() and update.message.text in context.user_data['options_raw']:
            context.user_data['entry'] = update.message.text
            await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['question_confirm'], 
                                            parse_mode=constants.ParseMode.HTML, 
                                            reply_markup=ReplyKeyboardMarkup(BUTTONS['question_buttons'], 
                                                                            one_time_keyboard=True))
            
            return QUESTION_7_CHECK
        else:
            await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['intro'], 
                                parse_mode=constants.ParseMode.HTML)
            await get_question(6, 'question_buttons', update, context)
            _ = await get_options(6, update.message.text, update, context)
            await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['next_btn_alt'], 
                                                    parse_mode=constants.ParseMode.HTML, 
                                                reply_markup=ReplyKeyboardMarkup(BUTTONS['question_buttons'], 
                                                                                one_time_keyboard=True))

async def question_7_check(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if 'передумал' in update.message.text.lower():
        await get_question(6, 'question_buttons', update, context)
        _ = await get_options(6, update.message.text, update, context)
        await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['next_btn'], 
                                                parse_mode=constants.ParseMode.HTML, 
                                            reply_markup=ReplyKeyboardMarkup(BUTTONS['question_buttons'], 
                                                                            one_time_keyboard=True))
        return QUESTION_5
    elif 'да, пропустить вс' in update.message.text.lower():
        await update.message.reply_text(MESSAGES['processing']['intro'], 
                                                parse_mode=constants.ParseMode.HTML)
        await update.message.reply_text(MESSAGES['processing']['contacts']['intro'], 
                                                parse_mode=constants.ParseMode.HTML, 
                                            reply_markup=ReplyKeyboardMarkup(BUTTONS['next_cancel'], 
                                                                            one_time_keyboard=True))
        return PROCESSING 
    else:
        if 'search_data' in context.user_data.keys() and '6' not in str(context.user_data['search_data'].keys()):
            context.user_data['search_data'][6] = context.user_data['entry']
            await clean_temp(update, context)

        await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['next_question'], 
                                                parse_mode=constants.ParseMode.HTML)

        await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['intro'], 
                                    parse_mode=constants.ParseMode.HTML)
        await get_question(7, 'question_buttons', update, context)
        _ = await get_options(7, update.message.text, update, context)
        await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['next_btn'], 
                                                parse_mode=constants.ParseMode.HTML, 
                                            reply_markup=ReplyKeyboardMarkup(BUTTONS['question_buttons'], 
                                                                            one_time_keyboard=True))
        return QUESTION_8

async def question_8(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    global MESSAGES, QUESTIONS, BUTTONS

    if 'показать опции' in update.message.text.lower() or 'все' in update.message.text.lower():
        _ = await get_options(7, 'все', update, context)
        await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['all_options'], 
                                        parse_mode=constants.ParseMode.HTML, 
                                        reply_markup=ReplyKeyboardMarkup(context.user_data['buttons'], 
                                                                         one_time_keyboard=True))
        
        return QUESTION_8
    elif 'скрыть опции' in update.message.text.lower():
        _ = await get_options(7, 'скрыть', update, context)
        await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['options_cleared'], 
                                        parse_mode=constants.ParseMode.HTML, 
                                        reply_markup=ReplyKeyboardMarkup(BUTTONS['question_buttons'], 
                                                                         one_time_keyboard=True))
        
        return QUESTION_8
    elif 'пропустить вс' in update.message.text.lower():
        await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['skip_confirm'], 
                                        parse_mode=constants.ParseMode.HTML, 
                                        reply_markup=ReplyKeyboardMarkup(BUTTONS['skip_all_yes'], 
                                                                        one_time_keyboard=True))
        return QUESTION_8_CHECK
    elif 'пропустить' in update.message.text.lower():
        await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['skip_confirm'], 
                                        parse_mode=constants.ParseMode.HTML, 
                                        reply_markup=ReplyKeyboardMarkup(BUTTONS['skip_yes'], 
                                                                        one_time_keyboard=True))
        return QUESTION_8_CHECK
    elif 'далее' in update.message.text.lower() and ('entry' not in context.user_data.keys() or not context.user_data['entry']):
        await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['prev_question'], 
                                                parse_mode=constants.ParseMode.HTML, 
                                            reply_markup=ReplyKeyboardMarkup(BUTTONS['question_buttons'], 
                                                                            one_time_keyboard=True))
        await get_question(7, 'question_buttons', update, context)

        return QUESTION_8
    else:
        if ('buttons_raw' in context.user_data.keys() and update.message.text not in context.user_data['buttons_raw']) and ('options_raw' in context.user_data.keys() and update.message.text not in context.user_data['options_raw']):
            _ = await get_options(7, update.message.text, update, context)
            
            if 'options_qty' in context.user_data.keys() and context.user_data['options_qty']:
                button = context.user_data['buttons']
                msg = 'all_options'
            else:
                button = BUTTONS['question_buttons']
                msg = 'option_not_found'

            await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions'][msg], 
                                            parse_mode=constants.ParseMode.HTML, 
                                            reply_markup=ReplyKeyboardMarkup(button, 
                                                                            one_time_keyboard=True))
            
            return QUESTION_8
        elif 'options_raw' in context.user_data.keys() and update.message.text in context.user_data['options_raw']:
            context.user_data['entry'] = update.message.text
            await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['question_confirm'], 
                                            parse_mode=constants.ParseMode.HTML, 
                                            reply_markup=ReplyKeyboardMarkup(BUTTONS['question_buttons'], 
                                                                            one_time_keyboard=True))
            
            return QUESTION_8_CHECK
        else:
            await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['intro'], 
                                parse_mode=constants.ParseMode.HTML)
            await get_question(7, 'question_buttons', update, context)
            _ = await get_options(7, update.message.text, update, context)
            await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['next_btn_alt'], 
                                                    parse_mode=constants.ParseMode.HTML, 
                                                reply_markup=ReplyKeyboardMarkup(BUTTONS['question_buttons'], 
                                                                                one_time_keyboard=True))

async def question_8_check(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if 'передумал' in update.message.text.lower():
        await get_question(7, 'question_buttons', update, context)
        _ = await get_options(7, update.message.text, update, context)
        await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['next_btn'], 
                                                parse_mode=constants.ParseMode.HTML, 
                                            reply_markup=ReplyKeyboardMarkup(BUTTONS['question_buttons'], 
                                                                            one_time_keyboard=True))
        return QUESTION_8
    elif 'да, пропустить вс' in update.message.text.lower():
        await update.message.reply_text(MESSAGES['processing']['intro'], 
                                                parse_mode=constants.ParseMode.HTML)
        await update.message.reply_text(MESSAGES['processing']['contacts']['intro'], 
                                                parse_mode=constants.ParseMode.HTML, 
                                            reply_markup=ReplyKeyboardMarkup(BUTTONS['next_cancel'], 
                                                                            one_time_keyboard=True))
        return PROCESSING 
    else:
        if 'search_data' in context.user_data.keys() and '7' not in str(context.user_data['search_data'].keys()):
            context.user_data['search_data'][7] = context.user_data['entry']
            await clean_temp(update, context)

        await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['next_question'], 
                                                parse_mode=constants.ParseMode.HTML)

        await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['intro'], 
                                    parse_mode=constants.ParseMode.HTML)
        await get_question(8, 'question_buttons', update, context)
        _ = await get_options(8, update.message.text, update, context)
        await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['next_btn'], 
                                                parse_mode=constants.ParseMode.HTML, 
                                            reply_markup=ReplyKeyboardMarkup(BUTTONS['question_buttons'], 
                                                                            one_time_keyboard=True))

        return QUESTION_9

async def question_9(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    global MESSAGES, QUESTIONS, BUTTONS

    if 'показать опции' in update.message.text.lower() or 'все' in update.message.text.lower():
        _ = await get_options(8, 'все', update, context)
        await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['all_options'], 
                                        parse_mode=constants.ParseMode.HTML, 
                                        reply_markup=ReplyKeyboardMarkup(context.user_data['buttons'], 
                                                                         one_time_keyboard=True))
        
        return QUESTION_9
    elif 'скрыть опции' in update.message.text.lower():
        _ = await get_options(8, 'скрыть', update, context)
        await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['options_cleared'], 
                                        parse_mode=constants.ParseMode.HTML, 
                                        reply_markup=ReplyKeyboardMarkup(BUTTONS['question_buttons'], 
                                                                         one_time_keyboard=True))
        
        return QUESTION_9
    elif 'пропустить вс' in update.message.text.lower():
        await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['skip_confirm'], 
                                        parse_mode=constants.ParseMode.HTML, 
                                        reply_markup=ReplyKeyboardMarkup(BUTTONS['skip_all_yes'], 
                                                                        one_time_keyboard=True))
        return QUESTION_9_CHECK
    elif 'пропустить' in update.message.text.lower():
        await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['skip_confirm'], 
                                        parse_mode=constants.ParseMode.HTML, 
                                        reply_markup=ReplyKeyboardMarkup(BUTTONS['skip_yes'], 
                                                                        one_time_keyboard=True))
        return QUESTION_9_CHECK
    elif 'далее' in update.message.text.lower() and ('entry' not in context.user_data.keys() or not context.user_data['entry']):
        await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['prev_question'], 
                                                parse_mode=constants.ParseMode.HTML, 
                                            reply_markup=ReplyKeyboardMarkup(BUTTONS['question_buttons'], 
                                                                            one_time_keyboard=True))
        await get_question(8, 'question_buttons', update, context)

        return QUESTION_9
    else:
        if ('buttons_raw' in context.user_data.keys() and update.message.text not in context.user_data['buttons_raw']) and ('options_raw' in context.user_data.keys() and update.message.text not in context.user_data['options_raw']):
            _ = await get_options(8, update.message.text, update, context)
            
            if 'options_qty' in context.user_data.keys() and context.user_data['options_qty']:
                button = context.user_data['buttons']
                msg = 'all_options'
            else:
                button = BUTTONS['question_buttons']
                msg = 'option_not_found'

            await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions'][msg], 
                                            parse_mode=constants.ParseMode.HTML, 
                                            reply_markup=ReplyKeyboardMarkup(button, 
                                                                            one_time_keyboard=True))
            
            return QUESTION_9
        elif 'options_raw' in context.user_data.keys() and update.message.text in context.user_data['options_raw']:
            context.user_data['entry'] = update.message.text
            await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['question_confirm'], 
                                            parse_mode=constants.ParseMode.HTML, 
                                            reply_markup=ReplyKeyboardMarkup(BUTTONS['question_buttons'], 
                                                                            one_time_keyboard=True))
            
            return QUESTION_9_CHECK
        else:
            await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['intro'], 
                                parse_mode=constants.ParseMode.HTML)
            await get_question(8, 'question_buttons', update, context)
            _ = await get_options(8, update.message.text, update, context)
            await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['next_btn_alt'], 
                                                    parse_mode=constants.ParseMode.HTML, 
                                                reply_markup=ReplyKeyboardMarkup(BUTTONS['question_buttons'], 
                                                                                one_time_keyboard=True))

async def question_9_check(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if 'передумал' in update.message.text.lower():
        await get_question(8, 'question_buttons', update, context)
        _ = await get_options(8, update.message.text, update, context)
        await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['next_btn'], 
                                                parse_mode=constants.ParseMode.HTML, 
                                            reply_markup=ReplyKeyboardMarkup(BUTTONS['question_buttons'], 
                                                                            one_time_keyboard=True))
        return QUESTION_9
    elif 'да, пропустить вс' in update.message.text.lower():
        await update.message.reply_text(MESSAGES['processing']['intro'], 
                                                parse_mode=constants.ParseMode.HTML)
        await update.message.reply_text(MESSAGES['processing']['contacts']['intro'], 
                                                parse_mode=constants.ParseMode.HTML, 
                                            reply_markup=ReplyKeyboardMarkup(BUTTONS['next_cancel'], 
                                                                            one_time_keyboard=True))
        return PROCESSING 
    else:
        if 'search_data' in context.user_data.keys() and '8' not in str(context.user_data['search_data'].keys()):
            context.user_data['search_data'][8] = context.user_data['entry']
            await clean_temp(update, context)

        await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['next_question'], 
                                                parse_mode=constants.ParseMode.HTML)

        await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['intro'], 
                                    parse_mode=constants.ParseMode.HTML)
        await get_question(9, 'question_buttons', update, context)
        _ = await get_options(9, update.message.text, update, context)
        await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['next_btn'], 
                                                parse_mode=constants.ParseMode.HTML, 
                                            reply_markup=ReplyKeyboardMarkup(BUTTONS['question_buttons'], 
                                                                            one_time_keyboard=True))
        return QUESTION_10

async def question_10(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    global MESSAGES, QUESTIONS, BUTTONS

    if 'показать опции' in update.message.text.lower() or update.message.text in QUESTIONS[9]['options']:
        query = 'все'
    else:
        query = update.message.text

    await get_options(9, query, update, context)

    if 'question' not in context.user_data.keys():
        context.user_data['question'] = dict(zip(context.user_data['options_raw'], [False] * len(context.user_data['options_raw'])))
    
    if ('suggestions' not in context.user_data.keys()) or (update.message.text not in context.user_data['options_raw']) or ('показать опции' in update.message.text.lower()):
        context.user_data['suggestions'] = context.user_data['buttons'].copy()
        questions = [x for x,y in context.user_data['question'].items() if y]
        context.user_data['questions_qty'] = len(questions)
        context.user_data['suggestions'] = [x for x in context.user_data['suggestions'] if x[0] not in questions]

    if 'показать опции' in update.message.text.lower() or 'все' in update.message.text.lower():
        suggestions = await get_options(9, 'все', update, context)
        await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['all_options'], 
                                        parse_mode=constants.ParseMode.HTML, 
                                        reply_markup=ReplyKeyboardMarkup(context.user_data['suggestions'], 
                                                                        one_time_keyboard=True))
        
        return QUESTION_10
    elif 'скрыть опции' in update.message.text.lower():
        suggestions = await get_options(9, 'скрыть', update, context)
        await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['options_cleared'], 
                                        parse_mode=constants.ParseMode.HTML, 
                                        reply_markup=ReplyKeyboardMarkup(BUTTONS['question_buttons'], 
                                                                        one_time_keyboard=True))
        
        return QUESTION_10_CHECK
    elif 'пропустить вс' in update.message.text.lower():
        await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['skip_confirm'], 
                                        parse_mode=constants.ParseMode.HTML, 
                                        reply_markup=ReplyKeyboardMarkup(BUTTONS['skip_all_yes'], 
                                                                        one_time_keyboard=True))
        return QUESTION_10_CHECK
    elif 'пропустить' in update.message.text.lower():
        await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['skip_confirm'], 
                                        parse_mode=constants.ParseMode.HTML, 
                                        reply_markup=ReplyKeyboardMarkup(BUTTONS['skip_yes'], 
                                                                        one_time_keyboard=True))
        return QUESTION_10_CHECK
    elif 'далее' in update.message.text.lower() and 'questions_qty' in context.user_data.keys() and context.user_data['questions_qty']:
        await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['next_btn'], 
                                                parse_mode=constants.ParseMode.HTML, 
                                            reply_markup=ReplyKeyboardMarkup(BUTTONS['question_buttons'], 
                                                                            one_time_keyboard=True))

        return QUESTION_10_CHECK
    elif 'далее' in update.message.text.lower() and ('questions_qty' in context.user_data.keys() and not context.user_data['questions_qty']):
        await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['prev_question'], 
                                                parse_mode=constants.ParseMode.HTML, 
                                                reply_markup=ReplyKeyboardMarkup(BUTTONS['question_buttons'], 
                                                                            one_time_keyboard=True))
        await get_question(9, 'question_buttons', update, context)

        return QUESTION_10
    else:
        if ('buttons_raw' in context.user_data.keys() and update.message.text not in context.user_data['buttons_raw']) and ('options_raw' in context.user_data.keys() and update.message.text not in context.user_data['options_raw']):
            _ = await get_options(9, update.message.text, update, context)
            
            if 'options_qty' in context.user_data.keys() and context.user_data['options_qty']:
                button = context.user_data['buttons']
                msg = 'all_options'
            else:
                button = BUTTONS['question_buttons']
                msg = 'option_not_found'

            await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions'][msg], 
                                            parse_mode=constants.ParseMode.HTML, 
                                            reply_markup=ReplyKeyboardMarkup(button, 
                                                                            one_time_keyboard=True))
            
            return QUESTION_10
        elif 'options_raw' in context.user_data.keys() and update.message.text in context.user_data['options_raw']:
            context.user_data['question'][update.message.text] = True
            context.user_data['suggestions'] = context.user_data['buttons'].copy()
            questions = [x for x,y in context.user_data['question'].items() if y]
            context.user_data['questions_qty'] = len(questions)
            context.user_data['suggestions'] = [x for x in context.user_data['suggestions'] if x[0] not in questions]
            context.user_data['suggestions'] = map(lambda x: x.remove(update.message.text) if (update.message.text in x) and (update.message.text not in context.user_data['buttons_raw']) else x, context.user_data['suggestions'])
            context.user_data['suggestions'] = [i for i in context.user_data['suggestions'] if i]

            await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['question_confirm'], 
                                        parse_mode=constants.ParseMode.HTML, 
                                        reply_markup=ReplyKeyboardMarkup(context.user_data['suggestions'], 
                                                                        one_time_keyboard=True))

async def question_10_check(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if 'передумал' in update.message.text.lower():
        await get_question(9, 'question_buttons', update, context)
        _ = await get_options(9, update.message.text, update, context)
        await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['next_btn'], 
                                                parse_mode=constants.ParseMode.HTML, 
                                            reply_markup=ReplyKeyboardMarkup(BUTTONS['question_buttons'], 
                                                                            one_time_keyboard=True))
        return QUESTION_10
    elif 'да, пропустить вс' in update.message.text.lower():
        await update.message.reply_text(MESSAGES['processing']['intro'], 
                                                parse_mode=constants.ParseMode.HTML)
        await update.message.reply_text(MESSAGES['processing']['contacts']['intro'], 
                                                parse_mode=constants.ParseMode.HTML, 
                                            reply_markup=ReplyKeyboardMarkup(BUTTONS['next_cancel'], 
                                                                            one_time_keyboard=True))
        return PROCESSING 
    else:
        if 'search_data' in context.user_data.keys() and '9' not in str(context.user_data['search_data'].keys()):
            context.user_data['search_data'][9] = [x for x,y in context.user_data['question'].items() if y]
            await clean_temp(update, context)

        await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['next_question'], 
                                                parse_mode=constants.ParseMode.HTML)

        await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['intro'], 
                                    parse_mode=constants.ParseMode.HTML)
        await get_question(10, 'question_buttons', update, context)
        _ = await get_options(10, update.message.text, update, context)
        await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['next_btn'], 
                                                parse_mode=constants.ParseMode.HTML, 
                                            reply_markup=ReplyKeyboardMarkup(BUTTONS['question_buttons'], 
                                                                            one_time_keyboard=True))
        return QUESTION_11

async def question_11(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    global MESSAGES, QUESTIONS, BUTTONS

    if 'показать опции' in update.message.text.lower() or 'все' in update.message.text.lower():
        _ = await get_options(10, 'все', update, context)
        await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['all_options'], 
                                        parse_mode=constants.ParseMode.HTML, 
                                        reply_markup=ReplyKeyboardMarkup(context.user_data['buttons'], 
                                                                         one_time_keyboard=True))
        
        return QUESTION_11
    elif 'скрыть опции' in update.message.text.lower():
        _ = await get_options(10, 'скрыть', update, context)
        await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['options_cleared'], 
                                        parse_mode=constants.ParseMode.HTML, 
                                        reply_markup=ReplyKeyboardMarkup(BUTTONS['question_buttons'], 
                                                                         one_time_keyboard=True))
        
        return QUESTION_11
    elif 'пропустить вс' in update.message.text.lower():
        await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['skip_confirm'], 
                                        parse_mode=constants.ParseMode.HTML, 
                                        reply_markup=ReplyKeyboardMarkup(BUTTONS['skip_all_yes'], 
                                                                        one_time_keyboard=True))
        return QUESTION_11_CHECK
    elif 'пропустить' in update.message.text.lower():
        await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['skip_confirm'], 
                                        parse_mode=constants.ParseMode.HTML, 
                                        reply_markup=ReplyKeyboardMarkup(BUTTONS['skip_yes'], 
                                                                        one_time_keyboard=True))
        return QUESTION_11_CHECK
    elif 'далее' in update.message.text.lower() and ('entry' not in context.user_data.keys() or not context.user_data['entry']):
        await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['prev_question'], 
                                                parse_mode=constants.ParseMode.HTML, 
                                            reply_markup=ReplyKeyboardMarkup(BUTTONS['question_buttons'], 
                                                                            one_time_keyboard=True))
        await get_question(10, 'question_buttons', update, context)

        return QUESTION_11
    else:
        if ('buttons_raw' in context.user_data.keys() and update.message.text not in context.user_data['buttons_raw']) and ('options_raw' in context.user_data.keys() and update.message.text not in context.user_data['options_raw']):
            _ = await get_options(10, update.message.text, update, context)
            
            if 'options_qty' in context.user_data.keys() and context.user_data['options_qty']:
                button = context.user_data['buttons']
                msg = 'all_options'
            else:
                button = BUTTONS['question_buttons']
                msg = 'option_not_found'

            await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions'][msg], 
                                            parse_mode=constants.ParseMode.HTML, 
                                            reply_markup=ReplyKeyboardMarkup(button, 
                                                                            one_time_keyboard=True))
            
            return QUESTION_11
        elif 'options_raw' in context.user_data.keys() and update.message.text in context.user_data['options_raw']:
            context.user_data['entry'] = update.message.text
            await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['question_confirm'], 
                                            parse_mode=constants.ParseMode.HTML, 
                                            reply_markup=ReplyKeyboardMarkup(BUTTONS['question_buttons'], 
                                                                            one_time_keyboard=True))
            
            return QUESTION_11_CHECK
        else:
            await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['intro'], 
                                parse_mode=constants.ParseMode.HTML)
            await get_question(10, 'question_buttons', update, context)
            _ = await get_options(10, update.message.text, update, context)
            await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['next_btn_alt'], 
                                                    parse_mode=constants.ParseMode.HTML, 
                                                reply_markup=ReplyKeyboardMarkup(BUTTONS['question_buttons'], 
                                                                                one_time_keyboard=True))

async def question_11_check(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if 'передумал' in update.message.text.lower():
        await get_question(10, 'question_buttons', update, context)
        _ = await get_options(10, update.message.text, update, context)
        await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['next_btn'], 
                                                parse_mode=constants.ParseMode.HTML, 
                                            reply_markup=ReplyKeyboardMarkup(BUTTONS['question_buttons'], 
                                                                            one_time_keyboard=True))
        return QUESTION_11
    elif 'да, пропустить вс' in update.message.text.lower():
        await update.message.reply_text(MESSAGES['processing']['intro'], 
                                                parse_mode=constants.ParseMode.HTML)
        await update.message.reply_text(MESSAGES['processing']['contacts']['intro'], 
                                                parse_mode=constants.ParseMode.HTML, 
                                            reply_markup=ReplyKeyboardMarkup(BUTTONS['next_cancel'], 
                                                                            one_time_keyboard=True))
        return PROCESSING 
    else:
        if 'search_data' in context.user_data.keys() and '10' not in str(context.user_data['search_data'].keys()):
            context.user_data['search_data'][10] = context.user_data['entry']
            await clean_temp(update, context)

        await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['next_question'], 
                                                parse_mode=constants.ParseMode.HTML)

        await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['intro'], 
                                    parse_mode=constants.ParseMode.HTML)
        await get_question(11, 'question_buttons', update, context)
        _ = await get_options(11, update.message.text, update, context)
        await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['next_btn'], 
                                                parse_mode=constants.ParseMode.HTML, 
                                            reply_markup=ReplyKeyboardMarkup(BUTTONS['question_buttons'], 
                                                                            one_time_keyboard=True))
        return QUESTION_12

async def question_12(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    global MESSAGES, QUESTIONS, BUTTONS

    if 'показать опции' in update.message.text.lower() or update.message.text in QUESTIONS[11]['options']:
        query = 'все'
    else:
        query = update.message.text

    await get_options(11, query, update, context)

    if 'question' not in context.user_data.keys():
        context.user_data['question'] = dict(zip(context.user_data['options_raw'], [False] * len(context.user_data['options_raw'])))
    
    if ('suggestions' not in context.user_data.keys()) or (update.message.text not in context.user_data['options_raw']) or ('показать опции' in update.message.text.lower()):
        context.user_data['suggestions'] = context.user_data['buttons'].copy()
        questions = [x for x,y in context.user_data['question'].items() if y]
        context.user_data['questions_qty'] = len(questions)
        context.user_data['suggestions'] = [x for x in context.user_data['suggestions'] if x[0] not in questions]

    if 'показать опции' in update.message.text.lower() or 'все' in update.message.text.lower():
        suggestions = await get_options(11, 'все', update, context)
        await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['all_options'], 
                                        parse_mode=constants.ParseMode.HTML, 
                                        reply_markup=ReplyKeyboardMarkup(context.user_data['suggestions'], 
                                                                        one_time_keyboard=True))
        
        return QUESTION_12
    elif 'скрыть опции' in update.message.text.lower():
        suggestions = await get_options(11, 'скрыть', update, context)
        await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['options_cleared'], 
                                        parse_mode=constants.ParseMode.HTML, 
                                        reply_markup=ReplyKeyboardMarkup(BUTTONS['question_buttons'], 
                                                                        one_time_keyboard=True))
        
        return QUESTION_12_CHECK
    elif 'пропустить вс' in update.message.text.lower():
        await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['skip_confirm'], 
                                        parse_mode=constants.ParseMode.HTML, 
                                        reply_markup=ReplyKeyboardMarkup(BUTTONS['skip_all_yes'], 
                                                                        one_time_keyboard=True))
        return QUESTION_12_CHECK
    elif 'пропустить' in update.message.text.lower():
        await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['skip_confirm'], 
                                        parse_mode=constants.ParseMode.HTML, 
                                        reply_markup=ReplyKeyboardMarkup(BUTTONS['skip_yes'], 
                                                                        one_time_keyboard=True))
        return QUESTION_12_CHECK
    elif 'далее' in update.message.text.lower() and 'questions_qty' in context.user_data.keys() and context.user_data['questions_qty']:
        await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['next_btn'], 
                                                parse_mode=constants.ParseMode.HTML, 
                                            reply_markup=ReplyKeyboardMarkup(BUTTONS['question_buttons'], 
                                                                            one_time_keyboard=True))

        return QUESTION_12_CHECK
    elif 'далее' in update.message.text.lower() and ('questions_qty' in context.user_data.keys() and not context.user_data['questions_qty']):
        await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['prev_question'], 
                                                parse_mode=constants.ParseMode.HTML, 
                                                reply_markup=ReplyKeyboardMarkup(BUTTONS['question_buttons'], 
                                                                            one_time_keyboard=True))
        await get_question(11, 'question_buttons', update, context)

        return QUESTION_12
    else:
        if ('buttons_raw' in context.user_data.keys() and update.message.text not in context.user_data['buttons_raw']) and ('options_raw' in context.user_data.keys() and update.message.text not in context.user_data['options_raw']):
            _ = await get_options(11, update.message.text, update, context)
            
            if 'options_qty' in context.user_data.keys() and context.user_data['options_qty']:
                button = context.user_data['buttons']
                msg = 'all_options'
            else:
                button = BUTTONS['question_buttons']
                msg = 'option_not_found'

            await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions'][msg], 
                                            parse_mode=constants.ParseMode.HTML, 
                                            reply_markup=ReplyKeyboardMarkup(button, 
                                                                            one_time_keyboard=True))
            
            return QUESTION_12
        elif 'options_raw' in context.user_data.keys() and update.message.text in context.user_data['options_raw']:
            context.user_data['question'][update.message.text] = True
            context.user_data['suggestions'] = context.user_data['buttons'].copy()
            questions = [x for x,y in context.user_data['question'].items() if y]
            context.user_data['questions_qty'] = len(questions)
            context.user_data['suggestions'] = [x for x in context.user_data['suggestions'] if x[0] not in questions]
            context.user_data['suggestions'] = map(lambda x: x.remove(update.message.text) if (update.message.text in x) and (update.message.text not in context.user_data['buttons_raw']) else x, context.user_data['suggestions'])
            context.user_data['suggestions'] = [i for i in context.user_data['suggestions'] if i]

            await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['question_confirm'], 
                                        parse_mode=constants.ParseMode.HTML, 
                                        reply_markup=ReplyKeyboardMarkup(context.user_data['suggestions'], 
                                                                        one_time_keyboard=True))

async def question_12_check(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if 'передумал' in update.message.text.lower():
        await get_question(11, 'question_buttons', update, context)
        _ = await get_options(11, update.message.text, update, context)
        await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['next_btn'], 
                                                parse_mode=constants.ParseMode.HTML, 
                                            reply_markup=ReplyKeyboardMarkup(BUTTONS['question_buttons'], 
                                                                            one_time_keyboard=True))
        return QUESTION_12
    elif 'да, пропустить вс' in update.message.text.lower():
        await update.message.reply_text(MESSAGES['processing']['intro'], 
                                                parse_mode=constants.ParseMode.HTML)
        await update.message.reply_text(MESSAGES['processing']['contacts']['intro'], 
                                                parse_mode=constants.ParseMode.HTML, 
                                            reply_markup=ReplyKeyboardMarkup(BUTTONS['next_cancel'], 
                                                                            one_time_keyboard=True))
        return PROCESSING 
    else:
        if 'search_data' in context.user_data.keys() and '11' not in str(context.user_data['search_data'].keys()):
            context.user_data['search_data'][11] = [x for x,y in context.user_data['question'].items() if y]
            await clean_temp(update, context)

        await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['next_question'], 
                                                parse_mode=constants.ParseMode.HTML)

        await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['intro'], 
                                    parse_mode=constants.ParseMode.HTML)
        await get_question(12, 'question_buttons', update, context)
        _ = await get_options(12, update.message.text, update, context)
        await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['next_btn'], 
                                                parse_mode=constants.ParseMode.HTML, 
                                            reply_markup=ReplyKeyboardMarkup(BUTTONS['question_buttons'], 
                                                                            one_time_keyboard=True))
        return QUESTION_13

async def question_13(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    global MESSAGES, QUESTIONS, BUTTONS

    if 'показать опции' in update.message.text.lower() or update.message.text in QUESTIONS[12]['options']:
        query = 'все'
    else:
        query = update.message.text

    await get_options(12, query, update, context)

    if 'question' not in context.user_data.keys():
        context.user_data['question'] = dict(zip(context.user_data['options_raw'], [False] * len(context.user_data['options_raw'])))
    
    if ('suggestions' not in context.user_data.keys()) or (update.message.text not in context.user_data['options_raw']) or ('показать опции' in update.message.text.lower()):
        context.user_data['suggestions'] = context.user_data['buttons'].copy()
        questions = [x for x,y in context.user_data['question'].items() if y]
        context.user_data['questions_qty'] = len(questions)
        context.user_data['suggestions'] = [x for x in context.user_data['suggestions'] if x[0] not in questions]

    if 'показать опции' in update.message.text.lower() or 'все' in update.message.text.lower():
        suggestions = await get_options(12, 'все', update, context)
        await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['all_options'], 
                                        parse_mode=constants.ParseMode.HTML, 
                                        reply_markup=ReplyKeyboardMarkup(context.user_data['suggestions'], 
                                                                        one_time_keyboard=True))
        
        return QUESTION_13
    elif 'скрыть опции' in update.message.text.lower():
        suggestions = await get_options(12, 'скрыть', update, context)
        await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['options_cleared'], 
                                        parse_mode=constants.ParseMode.HTML, 
                                        reply_markup=ReplyKeyboardMarkup(BUTTONS['question_buttons'], 
                                                                        one_time_keyboard=True))
        
        return QUESTION_13_CHECK
    elif 'пропустить вс' in update.message.text.lower():
        await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['skip_confirm'], 
                                        parse_mode=constants.ParseMode.HTML, 
                                        reply_markup=ReplyKeyboardMarkup(BUTTONS['skip_all_yes'], 
                                                                        one_time_keyboard=True))
        return QUESTION_13_CHECK
    elif 'пропустить' in update.message.text.lower():
        await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['skip_confirm'], 
                                        parse_mode=constants.ParseMode.HTML, 
                                        reply_markup=ReplyKeyboardMarkup(BUTTONS['skip_yes'], 
                                                                        one_time_keyboard=True))
        return QUESTION_13_CHECK
    elif 'далее' in update.message.text.lower() and 'questions_qty' in context.user_data.keys() and context.user_data['questions_qty']:
        await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['next_btn'], 
                                                parse_mode=constants.ParseMode.HTML, 
                                            reply_markup=ReplyKeyboardMarkup(BUTTONS['question_buttons'], 
                                                                            one_time_keyboard=True))

        return QUESTION_13_CHECK
    elif 'далее' in update.message.text.lower() and ('questions_qty' in context.user_data.keys() and not context.user_data['questions_qty']):
        await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['prev_question'], 
                                                parse_mode=constants.ParseMode.HTML, 
                                                reply_markup=ReplyKeyboardMarkup(BUTTONS['question_buttons'], 
                                                                            one_time_keyboard=True))
        await get_question(12, 'question_buttons', update, context)

        return QUESTION_13
    else:
        if ('buttons_raw' in context.user_data.keys() and update.message.text not in context.user_data['buttons_raw']) and ('options_raw' in context.user_data.keys() and update.message.text not in context.user_data['options_raw']):
            _ = await get_options(12, update.message.text, update, context)
            
            if 'options_qty' in context.user_data.keys() and context.user_data['options_qty']:
                button = context.user_data['buttons']
                msg = 'all_options'
            else:
                button = BUTTONS['question_buttons']
                msg = 'option_not_found'

            await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions'][msg], 
                                            parse_mode=constants.ParseMode.HTML, 
                                            reply_markup=ReplyKeyboardMarkup(button, 
                                                                            one_time_keyboard=True))
            
            return QUESTION_13
        elif 'options_raw' in context.user_data.keys() and update.message.text in context.user_data['options_raw']:
            context.user_data['question'][update.message.text] = True
            context.user_data['suggestions'] = context.user_data['buttons'].copy()
            questions = [x for x,y in context.user_data['question'].items() if y]
            context.user_data['questions_qty'] = len(questions)
            context.user_data['suggestions'] = [x for x in context.user_data['suggestions'] if x[0] not in questions]
            context.user_data['suggestions'] = map(lambda x: x.remove(update.message.text) if (update.message.text in x) and (update.message.text not in context.user_data['buttons_raw']) else x, context.user_data['suggestions'])
            context.user_data['suggestions'] = [i for i in context.user_data['suggestions'] if i]

            await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['question_confirm'], 
                                        parse_mode=constants.ParseMode.HTML, 
                                        reply_markup=ReplyKeyboardMarkup(context.user_data['suggestions'], 
                                                                        one_time_keyboard=True))

async def question_13_check(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if 'передумал' in update.message.text.lower():
        await get_question(12, 'question_buttons', update, context)
        _ = await get_options(12, update.message.text, update, context)
        await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['next_btn'], 
                                                parse_mode=constants.ParseMode.HTML, 
                                            reply_markup=ReplyKeyboardMarkup(BUTTONS['question_buttons'], 
                                                                            one_time_keyboard=True))
        return QUESTION_13
    elif 'да, пропустить вс' in update.message.text.lower():
        await update.message.reply_text(MESSAGES['processing']['intro'], 
                                                parse_mode=constants.ParseMode.HTML)
        await update.message.reply_text(MESSAGES['processing']['contacts']['intro'], 
                                                parse_mode=constants.ParseMode.HTML, 
                                            reply_markup=ReplyKeyboardMarkup(BUTTONS['next_cancel'], 
                                                                            one_time_keyboard=True))
        return PROCESSING 
    else:
        if 'search_data' in context.user_data.keys() and '12' not in str(context.user_data['search_data'].keys()):
            context.user_data['search_data'][12] = [x for x,y in context.user_data['question'].items() if y]
            await clean_temp(update, context)

        await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['next_question'], 
                                                parse_mode=constants.ParseMode.HTML)

        await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['intro'], 
                                    parse_mode=constants.ParseMode.HTML)
        await get_question(13, 'question_buttons', update, context)
        _ = await get_options(13, update.message.text, update, context)
        await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['next_btn'], 
                                                parse_mode=constants.ParseMode.HTML, 
                                            reply_markup=ReplyKeyboardMarkup(BUTTONS['question_buttons'], 
                                                                            one_time_keyboard=True))
        return QUESTION_14

async def question_14(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    global MESSAGES, QUESTIONS, BUTTONS

    if 'показать опции' in update.message.text.lower() or 'все' in update.message.text.lower():
        _ = await get_options(13, 'все', update, context)
        await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['all_options'], 
                                        parse_mode=constants.ParseMode.HTML, 
                                        reply_markup=ReplyKeyboardMarkup(context.user_data['buttons'], 
                                                                         one_time_keyboard=True))
        
        return QUESTION_14
    elif 'скрыть опции' in update.message.text.lower():
        _ = await get_options(13, 'скрыть', update, context)
        await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['options_cleared'], 
                                        parse_mode=constants.ParseMode.HTML, 
                                        reply_markup=ReplyKeyboardMarkup(BUTTONS['question_buttons'], 
                                                                         one_time_keyboard=True))
        
        return QUESTION_14
    elif 'пропустить вс' in update.message.text.lower():
        await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['skip_confirm'], 
                                        parse_mode=constants.ParseMode.HTML, 
                                        reply_markup=ReplyKeyboardMarkup(BUTTONS['skip_all_yes'], 
                                                                        one_time_keyboard=True))
        return QUESTION_14_CHECK
    elif 'пропустить' in update.message.text.lower():
        await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['skip_confirm'], 
                                        parse_mode=constants.ParseMode.HTML, 
                                        reply_markup=ReplyKeyboardMarkup(BUTTONS['skip_yes'], 
                                                                        one_time_keyboard=True))
        return QUESTION_14_CHECK
    elif 'далее' in update.message.text.lower() and ('entry' not in context.user_data.keys() or not context.user_data['entry']):
        await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['prev_question'], 
                                                parse_mode=constants.ParseMode.HTML, 
                                            reply_markup=ReplyKeyboardMarkup(BUTTONS['question_buttons'], 
                                                                            one_time_keyboard=True))
        await get_question(13, 'question_buttons', update, context)

        return QUESTION_14
    else:
        if ('buttons_raw' in context.user_data.keys() and update.message.text not in context.user_data['buttons_raw']) and ('options_raw' in context.user_data.keys() and update.message.text not in context.user_data['options_raw']):
            _ = await get_options(13, update.message.text, update, context)
            
            if 'options_qty' in context.user_data.keys() and context.user_data['options_qty']:
                button = context.user_data['buttons']
                msg = 'all_options'
            else:
                button = BUTTONS['question_buttons']
                msg = 'option_not_found'

            await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions'][msg], 
                                            parse_mode=constants.ParseMode.HTML, 
                                            reply_markup=ReplyKeyboardMarkup(button, 
                                                                            one_time_keyboard=True))
            
            return QUESTION_14
        elif 'options_raw' in context.user_data.keys() and update.message.text in context.user_data['options_raw']:
            context.user_data['entry'] = update.message.text
            await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['question_confirm'], 
                                            parse_mode=constants.ParseMode.HTML, 
                                            reply_markup=ReplyKeyboardMarkup(BUTTONS['question_buttons'], 
                                                                            one_time_keyboard=True))
            
            return QUESTION_14_CHECK
        else:
            await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['intro'], 
                                parse_mode=constants.ParseMode.HTML)
            await get_question(13, 'question_buttons', update, context)
            _ = await get_options(13, update.message.text, update, context)
            await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['next_btn_alt'], 
                                                    parse_mode=constants.ParseMode.HTML, 
                                                reply_markup=ReplyKeyboardMarkup(BUTTONS['question_buttons'], 
                                                                                one_time_keyboard=True))

async def question_14_check(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if 'передумал' in update.message.text.lower():
        await get_question(13, 'question_buttons', update, context)
        _ = await get_options(13, update.message.text, update, context)
        await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['next_btn'], 
                                                parse_mode=constants.ParseMode.HTML, 
                                            reply_markup=ReplyKeyboardMarkup(BUTTONS['question_buttons'], 
                                                                            one_time_keyboard=True))
        return QUESTION_14
    elif 'да, пропустить вс' in update.message.text.lower():
        await update.message.reply_text(MESSAGES['processing']['intro'], 
                                                parse_mode=constants.ParseMode.HTML)
        await update.message.reply_text(MESSAGES['processing']['contacts']['intro'], 
                                                parse_mode=constants.ParseMode.HTML, 
                                            reply_markup=ReplyKeyboardMarkup(BUTTONS['next_cancel'], 
                                                                            one_time_keyboard=True))
        return PROCESSING 
    else:
        if 'search_data' in context.user_data.keys() and '13' not in str(context.user_data['search_data'].keys()):
            context.user_data['search_data'][13] = context.user_data['entry']
            await clean_temp(update, context)

        await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['next_question'], 
                                                parse_mode=constants.ParseMode.HTML)

        await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['intro'], 
                                    parse_mode=constants.ParseMode.HTML)
        await get_question(14, 'question_buttons', update, context)
        _ = await get_options(14, update.message.text, update, context)
        await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['next_btn'], 
                                                parse_mode=constants.ParseMode.HTML, 
                                            reply_markup=ReplyKeyboardMarkup(BUTTONS['question_buttons'], 
                                                                            one_time_keyboard=True))
        return QUESTION_15

async def question_15(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    global MESSAGES, QUESTIONS, BUTTONS

    if 'показать опции' in update.message.text.lower() or update.message.text in QUESTIONS[14]['options']:
        query = 'все'
    else:
        query = update.message.text

    await get_options(14, query, update, context)

    if 'question' not in context.user_data.keys():
        context.user_data['question'] = dict(zip(context.user_data['options_raw'], [False] * len(context.user_data['options_raw'])))
    
    if ('suggestions' not in context.user_data.keys()) or (update.message.text not in context.user_data['options_raw']) or ('показать опции' in update.message.text.lower()):
        context.user_data['suggestions'] = context.user_data['buttons'].copy()
        questions = [x for x,y in context.user_data['question'].items() if y]
        context.user_data['questions_qty'] = len(questions)
        context.user_data['suggestions'] = [x for x in context.user_data['suggestions'] if x[0] not in questions]

    if 'показать опции' in update.message.text.lower() or 'все' in update.message.text.lower():
        suggestions = await get_options(14, 'все', update, context)
        await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['all_options'], 
                                        parse_mode=constants.ParseMode.HTML, 
                                        reply_markup=ReplyKeyboardMarkup(context.user_data['suggestions'], 
                                                                        one_time_keyboard=True))
        
        return QUESTION_15
    elif 'скрыть опции' in update.message.text.lower():
        suggestions = await get_options(14, 'скрыть', update, context)
        await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['options_cleared'], 
                                        parse_mode=constants.ParseMode.HTML, 
                                        reply_markup=ReplyKeyboardMarkup(BUTTONS['question_buttons'], 
                                                                        one_time_keyboard=True))
        
        return QUESTION_15_CHECK
    elif 'пропустить вс' in update.message.text.lower():
        await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['skip_confirm'], 
                                        parse_mode=constants.ParseMode.HTML, 
                                        reply_markup=ReplyKeyboardMarkup(BUTTONS['skip_all_yes'], 
                                                                        one_time_keyboard=True))
        return QUESTION_15_CHECK
    elif 'пропустить' in update.message.text.lower():
        await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['skip_confirm'], 
                                        parse_mode=constants.ParseMode.HTML, 
                                        reply_markup=ReplyKeyboardMarkup(BUTTONS['skip_yes'], 
                                                                        one_time_keyboard=True))
        return QUESTION_15_CHECK
    elif 'далее' in update.message.text.lower() and 'questions_qty' in context.user_data.keys() and context.user_data['questions_qty']:
        await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['next_btn'], 
                                                parse_mode=constants.ParseMode.HTML, 
                                            reply_markup=ReplyKeyboardMarkup(BUTTONS['question_buttons'], 
                                                                            one_time_keyboard=True))

        return QUESTION_15_CHECK
    elif 'далее' in update.message.text.lower() and ('questions_qty' in context.user_data.keys() and not context.user_data['questions_qty']):
        await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['prev_question'], 
                                                parse_mode=constants.ParseMode.HTML, 
                                                reply_markup=ReplyKeyboardMarkup(BUTTONS['question_buttons'], 
                                                                            one_time_keyboard=True))
        await get_question(9, 'question_buttons', update, context)

        return QUESTION_15
    else:
        if ('buttons_raw' in context.user_data.keys() and update.message.text not in context.user_data['buttons_raw']) and ('options_raw' in context.user_data.keys() and update.message.text not in context.user_data['options_raw']):
            _ = await get_options(14, update.message.text, update, context)
            
            if 'options_qty' in context.user_data.keys() and context.user_data['options_qty']:
                button = context.user_data['buttons']
                msg = 'all_options'
            else:
                button = BUTTONS['question_buttons']
                msg = 'option_not_found'

            await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions'][msg], 
                                            parse_mode=constants.ParseMode.HTML, 
                                            reply_markup=ReplyKeyboardMarkup(button, 
                                                                            one_time_keyboard=True))
            
            return QUESTION_15
        elif 'options_raw' in context.user_data.keys() and update.message.text in context.user_data['options_raw']:
            context.user_data['question'][update.message.text] = True
            context.user_data['suggestions'] = context.user_data['buttons'].copy()
            questions = [x for x,y in context.user_data['question'].items() if y]
            context.user_data['questions_qty'] = len(questions)
            context.user_data['suggestions'] = [x for x in context.user_data['suggestions'] if x[0] not in questions]
            context.user_data['suggestions'] = map(lambda x: x.remove(update.message.text) if (update.message.text in x) and (update.message.text not in context.user_data['buttons_raw']) else x, context.user_data['suggestions'])
            context.user_data['suggestions'] = [i for i in context.user_data['suggestions'] if i]

            await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['question_confirm'], 
                                        parse_mode=constants.ParseMode.HTML, 
                                        reply_markup=ReplyKeyboardMarkup(context.user_data['suggestions'], 
                                                                        one_time_keyboard=True))

async def question_15_check(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if 'передумал' in update.message.text.lower():
        await get_question(14, 'question_buttons', update, context)
        _ = await get_options(14, update.message.text, update, context)
        await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['next_btn'], 
                                                parse_mode=constants.ParseMode.HTML, 
                                            reply_markup=ReplyKeyboardMarkup(BUTTONS['question_buttons'], 
                                                                            one_time_keyboard=True))
        return QUESTION_15
    elif 'да, пропустить вс' in update.message.text.lower():
        await update.message.reply_text(MESSAGES['processing']['intro'], 
                                                parse_mode=constants.ParseMode.HTML)
        await update.message.reply_text(MESSAGES['processing']['contacts']['intro'], 
                                                parse_mode=constants.ParseMode.HTML, 
                                            reply_markup=ReplyKeyboardMarkup(BUTTONS['next_cancel'], 
                                                                            one_time_keyboard=True))
        return PROCESSING 
    else:
        if 'search_data' in context.user_data.keys() and '14' not in str(context.user_data['search_data'].keys()):
            context.user_data['search_data'][14] = [x for x,y in context.user_data['question'].items() if y]
            await clean_temp(update, context)

        await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['next_question'], 
                                                parse_mode=constants.ParseMode.HTML)

        await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['intro'], 
                                    parse_mode=constants.ParseMode.HTML)
        await get_question(15, 'question_buttons', update, context)
        _ = await get_options(15, update.message.text, update, context)
        await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['next_btn'], 
                                                parse_mode=constants.ParseMode.HTML, 
                                            reply_markup=ReplyKeyboardMarkup(BUTTONS['question_buttons'], 
                                                                            one_time_keyboard=True))
        return QUESTION_16

async def question_16(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    global MESSAGES, QUESTIONS, BUTTONS

    if 'показать опции' in update.message.text.lower() or 'все' in update.message.text.lower():
        _ = await get_options(15, 'все', update, context)
        await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['all_options'], 
                                        parse_mode=constants.ParseMode.HTML, 
                                        reply_markup=ReplyKeyboardMarkup(context.user_data['buttons'], 
                                                                         one_time_keyboard=True))
        
        return QUESTION_16
    elif 'скрыть опции' in update.message.text.lower():
        _ = await get_options(15, 'скрыть', update, context)
        await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['options_cleared'], 
                                        parse_mode=constants.ParseMode.HTML, 
                                        reply_markup=ReplyKeyboardMarkup(BUTTONS['question_buttons_2'], 
                                                                         one_time_keyboard=True))
        
        return QUESTION_16
    elif 'пропустить вс' in update.message.text.lower():
        await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['skip_confirm'], 
                                        parse_mode=constants.ParseMode.HTML, 
                                        reply_markup=ReplyKeyboardMarkup(BUTTONS['skip_all_yes'], 
                                                                        one_time_keyboard=True))
        return QUESTION_16_CHECK
    elif 'пропустить' in update.message.text.lower():
        await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['skip_confirm'], 
                                        parse_mode=constants.ParseMode.HTML, 
                                        reply_markup=ReplyKeyboardMarkup(BUTTONS['skip_yes'], 
                                                                        one_time_keyboard=True))
        return QUESTION_16_CHECK
    elif 'далее' in update.message.text.lower() and ('entry' not in context.user_data.keys() or not context.user_data['entry']):
        await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['prev_question'], 
                                                parse_mode=constants.ParseMode.HTML, 
                                            reply_markup=ReplyKeyboardMarkup(BUTTONS['question_buttons_2'], 
                                                                            one_time_keyboard=True))
        await get_question(15, 'question_buttons_2', update, context)

        return QUESTION_16
    else:
        if ('buttons_raw' in context.user_data.keys() and update.message.text not in context.user_data['buttons_raw']) and ('options_raw' in context.user_data.keys() and update.message.text not in context.user_data['options_raw']):
            _ = await get_options(15, update.message.text, update, context)
            
            if 'options_qty' in context.user_data.keys() and context.user_data['options_qty']:
                button = context.user_data['buttons']
                msg = 'all_options'
            else:
                button = BUTTONS['question_buttons_2']
                msg = 'option_not_found'

            await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions'][msg], 
                                            parse_mode=constants.ParseMode.HTML, 
                                            reply_markup=ReplyKeyboardMarkup(button, 
                                                                            one_time_keyboard=True))
            
            return QUESTION_16
        elif 'options_raw' in context.user_data.keys() and update.message.text in context.user_data['options_raw']:
            context.user_data['entry'] = update.message.text
            await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['question_confirm'], 
                                            parse_mode=constants.ParseMode.HTML, 
                                            reply_markup=ReplyKeyboardMarkup(BUTTONS['question_buttons_2'], 
                                                                            one_time_keyboard=True))
            
            return QUESTION_16_CHECK
        else:
            await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['intro'], 
                                parse_mode=constants.ParseMode.HTML)
            await get_question(15, 'question_buttons_2', update, context)
            _ = await get_options(15, update.message.text, update, context)
            await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['next_btn_alt'], 
                                                    parse_mode=constants.ParseMode.HTML, 
                                                reply_markup=ReplyKeyboardMarkup(BUTTONS['question_buttons_2'], 
                                                                                one_time_keyboard=True))

async def question_16_check(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if 'передумал' in update.message.text.lower():
        await get_question(15, 'question_buttons', update, context)
        _ = await get_options(15, update.message.text, update, context)
        await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['next_btn'], 
                                                parse_mode=constants.ParseMode.HTML, 
                                            reply_markup=ReplyKeyboardMarkup(BUTTONS['question_buttons'], 
                                                                            one_time_keyboard=True))
        return QUESTION_16
    elif 'да, пропустить вс' in update.message.text.lower():
        await update.message.reply_text(MESSAGES['processing']['intro'], 
                                                parse_mode=constants.ParseMode.HTML)
        await update.message.reply_text(MESSAGES['processing']['contacts']['intro'], 
                                                parse_mode=constants.ParseMode.HTML, 
                                            reply_markup=ReplyKeyboardMarkup(BUTTONS['next_cancel'], 
                                                                            one_time_keyboard=True))
        return PROCESSING 
    else:
        if 'search_data' in context.user_data.keys() and '15' not in str(context.user_data['search_data'].keys()):
            context.user_data['search_data'][15] = context.user_data['entry']
            await clean_temp(update, context)

        await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['next_question'], 
                                                parse_mode=constants.ParseMode.HTML)

        await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['intro'], 
                                    parse_mode=constants.ParseMode.HTML)
        await get_question(16, 'question_buttons', update, context)
        _ = await get_options(16, update.message.text, update, context)
        await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['next_btn'], 
                                                parse_mode=constants.ParseMode.HTML, 
                                            reply_markup=ReplyKeyboardMarkup(BUTTONS['question_buttons'], 
                                                                            one_time_keyboard=True))
        return QUESTION_17

async def question_17(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    global MESSAGES, QUESTIONS, BUTTONS

    if 'показать опции' in update.message.text.lower() or 'все' in update.message.text.lower():
        _ = await get_options(16, 'все', update, context)
        await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['all_options'], 
                                        parse_mode=constants.ParseMode.HTML, 
                                        reply_markup=ReplyKeyboardMarkup(context.user_data['buttons'], 
                                                                         one_time_keyboard=True))
        
        return QUESTION_17
    elif 'скрыть опции' in update.message.text.lower():
        _ = await get_options(16, 'скрыть', update, context)
        await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['options_cleared'], 
                                        parse_mode=constants.ParseMode.HTML, 
                                        reply_markup=ReplyKeyboardMarkup(BUTTONS['question_buttons_2'], 
                                                                         one_time_keyboard=True))
        
        return QUESTION_17
    elif 'пропустить вс' in update.message.text.lower():
        await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['skip_confirm'], 
                                        parse_mode=constants.ParseMode.HTML, 
                                        reply_markup=ReplyKeyboardMarkup(BUTTONS['skip_all_yes'], 
                                                                        one_time_keyboard=True))
        return QUESTION_17_CHECK
    elif 'пропустить' in update.message.text.lower():
        await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['skip_confirm'], 
                                        parse_mode=constants.ParseMode.HTML, 
                                        reply_markup=ReplyKeyboardMarkup(BUTTONS['skip_yes'], 
                                                                        one_time_keyboard=True))
        return QUESTION_17_CHECK
    elif 'далее' in update.message.text.lower() and ('entry' not in context.user_data.keys() or not context.user_data['entry']):
        await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['prev_question'], 
                                                parse_mode=constants.ParseMode.HTML, 
                                            reply_markup=ReplyKeyboardMarkup(BUTTONS['question_buttons_2'], 
                                                                            one_time_keyboard=True))
        await get_question(16, 'question_buttons_2', update, context)

        return QUESTION_17
    else:
        if ('buttons_raw' in context.user_data.keys() and update.message.text not in context.user_data['buttons_raw']) and ('options_raw' in context.user_data.keys() and update.message.text not in context.user_data['options_raw']):
            _ = await get_options(16, update.message.text, update, context)
            
            if 'options_qty' in context.user_data.keys() and context.user_data['options_qty']:
                button = context.user_data['buttons']
                msg = 'all_options'
            else:
                button = BUTTONS['question_buttons_2']
                msg = 'option_not_found'

            await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions'][msg], 
                                            parse_mode=constants.ParseMode.HTML, 
                                            reply_markup=ReplyKeyboardMarkup(button, 
                                                                            one_time_keyboard=True))
            
            return QUESTION_17
        elif 'options_raw' in context.user_data.keys() and update.message.text in context.user_data['options_raw']:
            context.user_data['entry'] = update.message.text
            await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['question_confirm'], 
                                            parse_mode=constants.ParseMode.HTML, 
                                            reply_markup=ReplyKeyboardMarkup(BUTTONS['question_buttons_2'], 
                                                                            one_time_keyboard=True))
            
            return QUESTION_17_CHECK
        else:
            await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['intro'], 
                                parse_mode=constants.ParseMode.HTML)
            await get_question(16, 'question_buttons_2', update, context)
            _ = await get_options(16, update.message.text, update, context)
            await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['next_btn_alt'], 
                                                    parse_mode=constants.ParseMode.HTML, 
                                                reply_markup=ReplyKeyboardMarkup(BUTTONS['question_buttons_2'], 
                                                                                one_time_keyboard=True))

async def question_17_check(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if 'передумал' in update.message.text.lower():
        await get_question(16, 'question_buttons', update, context)
        _ = await get_options(16, update.message.text, update, context)
        await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['next_btn'], 
                                                parse_mode=constants.ParseMode.HTML, 
                                            reply_markup=ReplyKeyboardMarkup(BUTTONS['question_buttons'], 
                                                                            one_time_keyboard=True))
        return QUESTION_17
    elif 'да, пропустить вс' in update.message.text.lower():
        await update.message.reply_text(MESSAGES['processing']['intro'], 
                                                parse_mode=constants.ParseMode.HTML)
        await update.message.reply_text(MESSAGES['processing']['contacts']['intro'], 
                                                parse_mode=constants.ParseMode.HTML, 
                                            reply_markup=ReplyKeyboardMarkup(BUTTONS['next_cancel'], 
                                                                            one_time_keyboard=True))
        return PROCESSING 
    else:
        if 'search_data' in context.user_data.keys() and '16' not in str(context.user_data['search_data'].keys()):
            context.user_data['search_data'][16] = context.user_data['entry']
            await clean_temp(update, context)

        await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['next_question'], 
                                                parse_mode=constants.ParseMode.HTML)

        await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['intro'], 
                                    parse_mode=constants.ParseMode.HTML)
        await get_question(17, 'question_buttons', update, context)
        _ = await get_options(17, update.message.text, update, context)
        await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['next_btn'], 
                                                parse_mode=constants.ParseMode.HTML, 
                                            reply_markup=ReplyKeyboardMarkup(BUTTONS['question_buttons'], 
                                                                            one_time_keyboard=True))
        return QUESTION_18

async def question_18(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    global MESSAGES, QUESTIONS, BUTTONS

    if 'показать опции' in update.message.text.lower() or 'все' in update.message.text.lower():
        _ = await get_options(17, 'все', update, context)
        await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['all_options'], 
                                        parse_mode=constants.ParseMode.HTML, 
                                        reply_markup=ReplyKeyboardMarkup(context.user_data['buttons'], 
                                                                         one_time_keyboard=True))
        
        return QUESTION_18
    elif 'скрыть опции' in update.message.text.lower():
        _ = await get_options(17, 'скрыть', update, context)
        await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['options_cleared'], 
                                        parse_mode=constants.ParseMode.HTML, 
                                        reply_markup=ReplyKeyboardMarkup(BUTTONS['question_buttons_2'], 
                                                                         one_time_keyboard=True))
        
        return QUESTION_18
    elif 'пропустить вс' in update.message.text.lower():
        await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['skip_confirm'], 
                                        parse_mode=constants.ParseMode.HTML, 
                                        reply_markup=ReplyKeyboardMarkup(BUTTONS['skip_all_yes'], 
                                                                        one_time_keyboard=True))
        return QUESTION_18_CHECK
    elif 'пропустить' in update.message.text.lower():
        await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['skip_confirm'], 
                                        parse_mode=constants.ParseMode.HTML, 
                                        reply_markup=ReplyKeyboardMarkup(BUTTONS['skip_yes'], 
                                                                        one_time_keyboard=True))
        return QUESTION_18_CHECK
    elif 'далее' in update.message.text.lower() and ('entry' not in context.user_data.keys() or not context.user_data['entry']):
        await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['prev_question'], 
                                                parse_mode=constants.ParseMode.HTML, 
                                            reply_markup=ReplyKeyboardMarkup(BUTTONS['question_buttons_2'], 
                                                                            one_time_keyboard=True))
        await get_question(17, 'question_buttons_2', update, context)

        return QUESTION_18
    else:
        if ('buttons_raw' in context.user_data.keys() and update.message.text not in context.user_data['buttons_raw']) and ('options_raw' in context.user_data.keys() and update.message.text not in context.user_data['options_raw']):
            _ = await get_options(17, update.message.text, update, context)
            
            if 'options_qty' in context.user_data.keys() and context.user_data['options_qty']:
                button = context.user_data['buttons']
                msg = 'all_options'
            else:
                button = BUTTONS['question_buttons_2']
                msg = 'option_not_found'

            await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions'][msg], 
                                            parse_mode=constants.ParseMode.HTML, 
                                            reply_markup=ReplyKeyboardMarkup(button, 
                                                                            one_time_keyboard=True))
            
            return QUESTION_18
        elif 'options_raw' in context.user_data.keys() and update.message.text in context.user_data['options_raw']:
            context.user_data['entry'] = update.message.text
            await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['question_confirm'], 
                                            parse_mode=constants.ParseMode.HTML, 
                                            reply_markup=ReplyKeyboardMarkup(BUTTONS['question_buttons_2'], 
                                                                            one_time_keyboard=True))
            
            return QUESTION_18_CHECK
        else:
            await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['intro'], 
                                parse_mode=constants.ParseMode.HTML)
            await get_question(17, 'question_buttons_2', update, context)
            _ = await get_options(17, update.message.text, update, context)
            await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['next_btn_alt'], 
                                                    parse_mode=constants.ParseMode.HTML, 
                                                reply_markup=ReplyKeyboardMarkup(BUTTONS['question_buttons_2'], 
                                                                                one_time_keyboard=True))

async def question_18_check(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if 'передумал' in update.message.text.lower():
        await get_question(17, 'question_buttons', update, context)
        _ = await get_options(17, update.message.text, update, context)
        await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['next_btn'], 
                                                parse_mode=constants.ParseMode.HTML, 
                                            reply_markup=ReplyKeyboardMarkup(BUTTONS['question_buttons'], 
                                                                            one_time_keyboard=True))
        return QUESTION_18
    elif 'да, пропустить вс' in update.message.text.lower():
        await update.message.reply_text(MESSAGES['processing']['intro'], 
                                                parse_mode=constants.ParseMode.HTML)
        await update.message.reply_text(MESSAGES['processing']['contacts']['intro'], 
                                                parse_mode=constants.ParseMode.HTML, 
                                            reply_markup=ReplyKeyboardMarkup(BUTTONS['next_cancel'], 
                                                                            one_time_keyboard=True))
        return PROCESSING 
    else:
        if 'search_data' in context.user_data.keys() and '17' not in str(context.user_data['search_data'].keys()):
            context.user_data['search_data'][17] = context.user_data['entry']
            await clean_temp(update, context)

        await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['next_question'], 
                                                parse_mode=constants.ParseMode.HTML)

        await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['intro'], 
                                    parse_mode=constants.ParseMode.HTML)
        await get_question(18, 'question_buttons', update, context)
        _ = await get_options(18, update.message.text, update, context)
        await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['next_btn'], 
                                                parse_mode=constants.ParseMode.HTML, 
                                            reply_markup=ReplyKeyboardMarkup(BUTTONS['question_buttons'], 
                                                                            one_time_keyboard=True))
        return QUESTION_19

async def question_19(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    global MESSAGES, QUESTIONS, BUTTONS

    if 'показать опции' in update.message.text.lower() or 'все' in update.message.text.lower():
        _ = await get_options(18, 'все', update, context)
        await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['all_options'], 
                                        parse_mode=constants.ParseMode.HTML, 
                                        reply_markup=ReplyKeyboardMarkup(context.user_data['buttons'], 
                                                                         one_time_keyboard=True))
        
        return QUESTION_19
    elif 'скрыть опции' in update.message.text.lower():
        _ = await get_options(18, 'скрыть', update, context)
        await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['options_cleared'], 
                                        parse_mode=constants.ParseMode.HTML, 
                                        reply_markup=ReplyKeyboardMarkup(BUTTONS['question_buttons_2'], 
                                                                         one_time_keyboard=True))
        
        return QUESTION_19
    elif 'пропустить вс' in update.message.text.lower():
        await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['skip_confirm'], 
                                        parse_mode=constants.ParseMode.HTML, 
                                        reply_markup=ReplyKeyboardMarkup(BUTTONS['skip_all_yes'], 
                                                                        one_time_keyboard=True))
        return QUESTION_19_CHECK
    elif 'пропустить' in update.message.text.lower():
        await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['skip_confirm'], 
                                        parse_mode=constants.ParseMode.HTML, 
                                        reply_markup=ReplyKeyboardMarkup(BUTTONS['skip_yes'], 
                                                                        one_time_keyboard=True))
        return QUESTION_19_CHECK
    elif 'далее' in update.message.text.lower() and ('entry' not in context.user_data.keys() or not context.user_data['entry']):
        await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['prev_question'], 
                                                parse_mode=constants.ParseMode.HTML, 
                                            reply_markup=ReplyKeyboardMarkup(BUTTONS['question_buttons_2'], 
                                                                            one_time_keyboard=True))
        await get_question(18, 'question_buttons_2', update, context)

        return QUESTION_19
    else:
        if ('buttons_raw' in context.user_data.keys() and update.message.text not in context.user_data['buttons_raw']) and ('options_raw' in context.user_data.keys() and update.message.text not in context.user_data['options_raw']):
            _ = await get_options(18, update.message.text, update, context)
            
            if 'options_qty' in context.user_data.keys() and context.user_data['options_qty']:
                button = context.user_data['buttons']
                msg = 'all_options'
            else:
                button = BUTTONS['question_buttons_2']
                msg = 'option_not_found'

            await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions'][msg], 
                                            parse_mode=constants.ParseMode.HTML, 
                                            reply_markup=ReplyKeyboardMarkup(button, 
                                                                            one_time_keyboard=True))
            
            return QUESTION_19
        elif 'options_raw' in context.user_data.keys() and update.message.text in context.user_data['options_raw']:
            context.user_data['entry'] = update.message.text
            await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['question_confirm'], 
                                            parse_mode=constants.ParseMode.HTML, 
                                            reply_markup=ReplyKeyboardMarkup(BUTTONS['question_buttons_2'], 
                                                                            one_time_keyboard=True))
            
            return QUESTION_19_CHECK
        else:
            await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['intro'], 
                                parse_mode=constants.ParseMode.HTML)
            await get_question(18, 'question_buttons_2', update, context)
            _ = await get_options(18, update.message.text, update, context)
            await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['next_btn_alt'], 
                                                    parse_mode=constants.ParseMode.HTML, 
                                                reply_markup=ReplyKeyboardMarkup(BUTTONS['question_buttons_2'], 
                                                                                one_time_keyboard=True))

async def question_19_check(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if 'передумал' in update.message.text.lower():
        await get_question(18, 'question_buttons', update, context)
        _ = await get_options(18, update.message.text, update, context)
        await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['next_btn'], 
                                                parse_mode=constants.ParseMode.HTML, 
                                            reply_markup=ReplyKeyboardMarkup(BUTTONS['question_buttons'], 
                                                                            one_time_keyboard=True))
        return QUESTION_19
    elif 'да, пропустить вс' in update.message.text.lower():
        await update.message.reply_text(MESSAGES['processing']['intro'], 
                                                parse_mode=constants.ParseMode.HTML)
        await update.message.reply_text(MESSAGES['processing']['contacts']['intro'], 
                                                parse_mode=constants.ParseMode.HTML, 
                                            reply_markup=ReplyKeyboardMarkup(BUTTONS['next_cancel'], 
                                                                            one_time_keyboard=True))
        return PROCESSING 
    else:
        if 'search_data' in context.user_data.keys() and '18' not in str(context.user_data['search_data'].keys()):
            context.user_data['search_data'][18] = context.user_data['entry']
            await clean_temp(update, context)

        await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['next_question'], 
                                                parse_mode=constants.ParseMode.HTML)

        await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['intro'], 
                                    parse_mode=constants.ParseMode.HTML)
        await get_question(19, 'question_buttons', update, context)
        _ = await get_options(19, update.message.text, update, context)
        await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['next_btn'], 
                                                parse_mode=constants.ParseMode.HTML, 
                                            reply_markup=ReplyKeyboardMarkup(BUTTONS['question_buttons'], 
                                                                            one_time_keyboard=True))
        return QUESTION_20

async def question_20(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    global MESSAGES, QUESTIONS, BUTTONS

    if 'показать опции' in update.message.text.lower() or 'все' in update.message.text.lower():
        _ = await get_options(19, 'все', update, context)
        await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['all_options'], 
                                        parse_mode=constants.ParseMode.HTML, 
                                        reply_markup=ReplyKeyboardMarkup(context.user_data['buttons'], 
                                                                         one_time_keyboard=True))
        
        return QUESTION_20
    elif 'скрыть опции' in update.message.text.lower():
        _ = await get_options(19, 'скрыть', update, context)
        await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['options_cleared'], 
                                        parse_mode=constants.ParseMode.HTML, 
                                        reply_markup=ReplyKeyboardMarkup(BUTTONS['question_buttons_2'], 
                                                                         one_time_keyboard=True))
        
        return QUESTION_20
    elif 'пропустить вс' in update.message.text.lower():
        await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['skip_confirm'], 
                                        parse_mode=constants.ParseMode.HTML, 
                                        reply_markup=ReplyKeyboardMarkup(BUTTONS['skip_all_yes'], 
                                                                        one_time_keyboard=True))
        return QUESTION_20_CHECK
    elif 'пропустить' in update.message.text.lower():
        await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['skip_confirm'], 
                                        parse_mode=constants.ParseMode.HTML, 
                                        reply_markup=ReplyKeyboardMarkup(BUTTONS['skip_yes'], 
                                                                        one_time_keyboard=True))
        return QUESTION_20_CHECK
    elif 'далее' in update.message.text.lower() and ('entry' not in context.user_data.keys() or not context.user_data['entry']):
        await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['prev_question'], 
                                                parse_mode=constants.ParseMode.HTML, 
                                            reply_markup=ReplyKeyboardMarkup(BUTTONS['question_buttons_2'], 
                                                                            one_time_keyboard=True))
        await get_question(19, 'question_buttons_2', update, context)

        return QUESTION_20
    else:
        if ('buttons_raw' in context.user_data.keys() and update.message.text not in context.user_data['buttons_raw']) and ('options_raw' in context.user_data.keys() and update.message.text not in context.user_data['options_raw']):
            _ = await get_options(19, update.message.text, update, context)
            
            if 'options_qty' in context.user_data.keys() and context.user_data['options_qty']:
                button = context.user_data['buttons']
                msg = 'all_options'
            else:
                button = BUTTONS['question_buttons_2']
                msg = 'option_not_found'

            await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions'][msg], 
                                            parse_mode=constants.ParseMode.HTML, 
                                            reply_markup=ReplyKeyboardMarkup(button, 
                                                                            one_time_keyboard=True))
            
            return QUESTION_20
        elif 'options_raw' in context.user_data.keys() and update.message.text in context.user_data['options_raw']:
            context.user_data['entry'] = update.message.text
            await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['question_confirm'], 
                                            parse_mode=constants.ParseMode.HTML, 
                                            reply_markup=ReplyKeyboardMarkup(BUTTONS['question_buttons_2'], 
                                                                            one_time_keyboard=True))
            
            return QUESTION_20_CHECK
        else:
            await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['intro'], 
                                parse_mode=constants.ParseMode.HTML)
            await get_question(19, 'question_buttons_2', update, context)
            _ = await get_options(19, update.message.text, update, context)
            await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['next_btn_alt'], 
                                                    parse_mode=constants.ParseMode.HTML, 
                                                reply_markup=ReplyKeyboardMarkup(BUTTONS['question_buttons_2'], 
                                                                                one_time_keyboard=True))

async def question_20_check(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if 'передумал' in update.message.text.lower():
        await get_question(19, 'question_buttons', update, context)
        _ = await get_options(19, update.message.text, update, context)
        await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['next_btn'], 
                                                parse_mode=constants.ParseMode.HTML, 
                                            reply_markup=ReplyKeyboardMarkup(BUTTONS['question_buttons'], 
                                                                            one_time_keyboard=True))
        return QUESTION_20
    elif 'да, пропустить вс' in update.message.text.lower():
        await update.message.reply_text(MESSAGES['processing']['intro'], 
                                                parse_mode=constants.ParseMode.HTML)
        await update.message.reply_text(MESSAGES['processing']['contacts']['intro'], 
                                                parse_mode=constants.ParseMode.HTML, 
                                            reply_markup=ReplyKeyboardMarkup(BUTTONS['next_cancel'], 
                                                                            one_time_keyboard=True))
        return PROCESSING 
    else:
        if 'search_data' in context.user_data.keys() and '19' not in str(context.user_data['search_data'].keys()):
            context.user_data['search_data'][19] = context.user_data['entry']
            await clean_temp(update, context)

        await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['next_question'], 
                                                parse_mode=constants.ParseMode.HTML)

        await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['intro'], 
                                    parse_mode=constants.ParseMode.HTML)
        await get_question(20, 'question_buttons', update, context)
        _ = await get_options(20, update.message.text, update, context)
        await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['next_btn'], 
                                                parse_mode=constants.ParseMode.HTML, 
                                            reply_markup=ReplyKeyboardMarkup(BUTTONS['question_buttons'], 
                                                                            one_time_keyboard=True))
        return QUESTION_21

async def question_21(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    global MESSAGES, QUESTIONS, BUTTONS

    if 'показать опции' in update.message.text.lower() or 'все' in update.message.text.lower():
        _ = await get_options(20, 'все', update, context)
        await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['all_options'], 
                                        parse_mode=constants.ParseMode.HTML, 
                                        reply_markup=ReplyKeyboardMarkup(context.user_data['buttons'], 
                                                                         one_time_keyboard=True))
        
        return QUESTION_21
    elif 'скрыть опции' in update.message.text.lower():
        _ = await get_options(20, 'скрыть', update, context)
        await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['options_cleared'], 
                                        parse_mode=constants.ParseMode.HTML, 
                                        reply_markup=ReplyKeyboardMarkup(BUTTONS['question_buttons_2'], 
                                                                         one_time_keyboard=True))
        
        return QUESTION_21
    elif 'пропустить вс' in update.message.text.lower():
        await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['skip_confirm'], 
                                        parse_mode=constants.ParseMode.HTML, 
                                        reply_markup=ReplyKeyboardMarkup(BUTTONS['skip_all_yes'], 
                                                                        one_time_keyboard=True))
        return QUESTION_21_CHECK
    elif 'пропустить' in update.message.text.lower():
        await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['skip_confirm'], 
                                        parse_mode=constants.ParseMode.HTML, 
                                        reply_markup=ReplyKeyboardMarkup(BUTTONS['skip_yes'], 
                                                                        one_time_keyboard=True))
        return QUESTION_21_CHECK
    elif 'далее' in update.message.text.lower() and ('entry' not in context.user_data.keys() or not context.user_data['entry']):
        await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['prev_question'], 
                                                parse_mode=constants.ParseMode.HTML, 
                                            reply_markup=ReplyKeyboardMarkup(BUTTONS['question_buttons_2'], 
                                                                            one_time_keyboard=True))
        await get_question(20, 'question_buttons_2', update, context)

        return QUESTION_21
    else:
        if ('buttons_raw' in context.user_data.keys() and update.message.text not in context.user_data['buttons_raw']) and ('options_raw' in context.user_data.keys() and update.message.text not in context.user_data['options_raw']):
            _ = await get_options(20, update.message.text, update, context)
            
            if 'options_qty' in context.user_data.keys() and context.user_data['options_qty']:
                button = context.user_data['buttons']
                msg = 'all_options'
            else:
                button = BUTTONS['question_buttons_2']
                msg = 'option_not_found'

            await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions'][msg], 
                                            parse_mode=constants.ParseMode.HTML, 
                                            reply_markup=ReplyKeyboardMarkup(button, 
                                                                            one_time_keyboard=True))
            
            return QUESTION_21
        elif 'options_raw' in context.user_data.keys() and update.message.text in context.user_data['options_raw']:
            context.user_data['entry'] = update.message.text
            await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['question_confirm'], 
                                            parse_mode=constants.ParseMode.HTML, 
                                            reply_markup=ReplyKeyboardMarkup(BUTTONS['question_buttons_2'], 
                                                                            one_time_keyboard=True))
            
            return QUESTION_21_CHECK
        else:
            await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['intro'], 
                                parse_mode=constants.ParseMode.HTML)
            await get_question(20, 'question_buttons_2', update, context)
            _ = await get_options(20, update.message.text, update, context)
            await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['next_btn_alt'], 
                                                    parse_mode=constants.ParseMode.HTML, 
                                                reply_markup=ReplyKeyboardMarkup(BUTTONS['question_buttons_2'], 
                                                                                one_time_keyboard=True))

async def question_21_check(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if 'передумал' in update.message.text.lower():
        await get_question(20, 'question_buttons', update, context)
        _ = await get_options(20, update.message.text, update, context)
        await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['next_btn'], 
                                                parse_mode=constants.ParseMode.HTML, 
                                            reply_markup=ReplyKeyboardMarkup(BUTTONS['question_buttons'], 
                                                                            one_time_keyboard=True))
        return QUESTION_21
    elif 'да, пропустить вс' in update.message.text.lower():
        await update.message.reply_text(MESSAGES['processing']['intro'], 
                                                parse_mode=constants.ParseMode.HTML)
        await update.message.reply_text(MESSAGES['processing']['contacts']['intro'], 
                                                parse_mode=constants.ParseMode.HTML, 
                                            reply_markup=ReplyKeyboardMarkup(BUTTONS['next_cancel'], 
                                                                            one_time_keyboard=True))
        return PROCESSING 
    else:
        if 'search_data' in context.user_data.keys() and '20' not in str(context.user_data['search_data'].keys()):
            context.user_data['search_data'][20] = context.user_data['entry']
            await clean_temp(update, context)

        await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['next_question'], 
                                                parse_mode=constants.ParseMode.HTML)

        await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['intro'], 
                                    parse_mode=constants.ParseMode.HTML)
        await get_question(21, 'question_buttons', update, context)
        _ = await get_options(21, update.message.text, update, context)
        await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['next_btn'], 
                                                parse_mode=constants.ParseMode.HTML, 
                                            reply_markup=ReplyKeyboardMarkup(BUTTONS['question_buttons'], 
                                                                            one_time_keyboard=True))
        return QUESTION_22

async def question_22(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    global MESSAGES, QUESTIONS, BUTTONS

    if 'показать опции' in update.message.text.lower() or 'все' in update.message.text.lower():
        _ = await get_options(21, 'все', update, context)
        await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['all_options'], 
                                        parse_mode=constants.ParseMode.HTML, 
                                        reply_markup=ReplyKeyboardMarkup(context.user_data['buttons'], 
                                                                         one_time_keyboard=True))
        
        return QUESTION_22
    elif 'скрыть опции' in update.message.text.lower():
        _ = await get_options(21, 'скрыть', update, context)
        await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['options_cleared'], 
                                        parse_mode=constants.ParseMode.HTML, 
                                        reply_markup=ReplyKeyboardMarkup(BUTTONS['question_buttons_2'], 
                                                                         one_time_keyboard=True))
        
        return QUESTION_22
    elif 'пропустить вс' in update.message.text.lower():
        await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['skip_confirm'], 
                                        parse_mode=constants.ParseMode.HTML, 
                                        reply_markup=ReplyKeyboardMarkup(BUTTONS['skip_all_yes'], 
                                                                        one_time_keyboard=True))
        return QUESTION_22_CHECK
    elif 'пропустить' in update.message.text.lower():
        await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['skip_confirm'], 
                                        parse_mode=constants.ParseMode.HTML, 
                                        reply_markup=ReplyKeyboardMarkup(BUTTONS['skip_yes'], 
                                                                        one_time_keyboard=True))
        return QUESTION_22_CHECK
    elif 'далее' in update.message.text.lower() and ('entry' not in context.user_data.keys() or not context.user_data['entry']):
        await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['prev_question'], 
                                                parse_mode=constants.ParseMode.HTML, 
                                            reply_markup=ReplyKeyboardMarkup(BUTTONS['question_buttons_2'], 
                                                                            one_time_keyboard=True))
        await get_question(21, 'question_buttons_2', update, context)

        return QUESTION_22
    else:
        if ('buttons_raw' in context.user_data.keys() and update.message.text not in context.user_data['buttons_raw']) and ('options_raw' in context.user_data.keys() and update.message.text not in context.user_data['options_raw']):
            _ = await get_options(21, update.message.text, update, context)
            
            if 'options_qty' in context.user_data.keys() and context.user_data['options_qty']:
                button = context.user_data['buttons']
                msg = 'all_options'
            else:
                button = BUTTONS['question_buttons_2']
                msg = 'option_not_found'

            await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions'][msg], 
                                            parse_mode=constants.ParseMode.HTML, 
                                            reply_markup=ReplyKeyboardMarkup(button, 
                                                                            one_time_keyboard=True))
            
            return QUESTION_22
        elif 'options_raw' in context.user_data.keys() and update.message.text in context.user_data['options_raw']:
            context.user_data['entry'] = update.message.text
            await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['question_confirm'], 
                                            parse_mode=constants.ParseMode.HTML, 
                                            reply_markup=ReplyKeyboardMarkup(BUTTONS['question_buttons_2'], 
                                                                            one_time_keyboard=True))
            
            return QUESTION_22_CHECK
        else:
            await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['intro'], 
                                parse_mode=constants.ParseMode.HTML)
            await get_question(21, 'question_buttons_2', update, context)
            _ = await get_options(21, update.message.text, update, context)
            await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['next_btn_alt'], 
                                                    parse_mode=constants.ParseMode.HTML, 
                                                reply_markup=ReplyKeyboardMarkup(BUTTONS['question_buttons_2'], 
                                                                                one_time_keyboard=True))

async def question_22_check(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if 'передумал' in update.message.text.lower():
        await get_question(21, 'question_buttons', update, context)
        _ = await get_options(21, update.message.text, update, context)
        await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['next_btn'], 
                                                parse_mode=constants.ParseMode.HTML, 
                                            reply_markup=ReplyKeyboardMarkup(BUTTONS['question_buttons'], 
                                                                            one_time_keyboard=True))
        return QUESTION_22
    elif 'да, пропустить вс' in update.message.text.lower():
        await update.message.reply_text(MESSAGES['processing']['intro'], 
                                                parse_mode=constants.ParseMode.HTML)
        await update.message.reply_text(MESSAGES['processing']['contacts']['intro'], 
                                                parse_mode=constants.ParseMode.HTML, 
                                            reply_markup=ReplyKeyboardMarkup(BUTTONS['next_cancel'], 
                                                                            one_time_keyboard=True))
        return PROCESSING 
    else:
        if 'search_data' in context.user_data.keys() and '21' not in str(context.user_data['search_data'].keys()):
            context.user_data['search_data'][21] = context.user_data['entry']
            await clean_temp(update, context)

        await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['next_question'], 
                                                parse_mode=constants.ParseMode.HTML)

        await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['intro'], 
                                    parse_mode=constants.ParseMode.HTML)
        await get_question(22, 'question_buttons', update, context)
        _ = await get_options(22, update.message.text, update, context)
        await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['next_btn'], 
                                                parse_mode=constants.ParseMode.HTML, 
                                            reply_markup=ReplyKeyboardMarkup(BUTTONS['question_buttons'], 
                                                                            one_time_keyboard=True))
        return QUESTION_23

async def question_23(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    global MESSAGES, QUESTIONS, BUTTONS

    if 'показать опции' in update.message.text.lower() or 'все' in update.message.text.lower():
        _ = await get_options(22, 'все', update, context)
        await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['all_options'], 
                                        parse_mode=constants.ParseMode.HTML, 
                                        reply_markup=ReplyKeyboardMarkup(context.user_data['buttons'], 
                                                                         one_time_keyboard=True))
        
        return QUESTION_23
    elif 'скрыть опции' in update.message.text.lower():
        _ = await get_options(22, 'скрыть', update, context)
        await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['options_cleared'], 
                                        parse_mode=constants.ParseMode.HTML, 
                                        reply_markup=ReplyKeyboardMarkup(BUTTONS['question_buttons_2'], 
                                                                         one_time_keyboard=True))
        
        return QUESTION_23
    elif 'пропустить вс' in update.message.text.lower():
        await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['skip_confirm'], 
                                        parse_mode=constants.ParseMode.HTML, 
                                        reply_markup=ReplyKeyboardMarkup(BUTTONS['skip_all_yes'], 
                                                                        one_time_keyboard=True))
        return QUESTION_23_CHECK
    elif 'пропустить' in update.message.text.lower():
        await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['skip_confirm'], 
                                        parse_mode=constants.ParseMode.HTML, 
                                        reply_markup=ReplyKeyboardMarkup(BUTTONS['skip_yes'], 
                                                                        one_time_keyboard=True))
        return QUESTION_23_CHECK
    elif 'далее' in update.message.text.lower() and ('entry' not in context.user_data.keys() or not context.user_data['entry']):
        await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['prev_question'], 
                                                parse_mode=constants.ParseMode.HTML, 
                                            reply_markup=ReplyKeyboardMarkup(BUTTONS['question_buttons_2'], 
                                                                            one_time_keyboard=True))
        await get_question(22, 'question_buttons_2', update, context)

        return QUESTION_23
    else:
        if ('buttons_raw' in context.user_data.keys() and update.message.text not in context.user_data['buttons_raw']) and ('options_raw' in context.user_data.keys() and update.message.text not in context.user_data['options_raw']):
            _ = await get_options(22, update.message.text, update, context)
            
            if 'options_qty' in context.user_data.keys() and context.user_data['options_qty']:
                button = context.user_data['buttons']
                msg = 'all_options'
            else:
                button = BUTTONS['question_buttons_2']
                msg = 'option_not_found'

            await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions'][msg], 
                                            parse_mode=constants.ParseMode.HTML, 
                                            reply_markup=ReplyKeyboardMarkup(button, 
                                                                            one_time_keyboard=True))
            
            return QUESTION_23
        elif 'options_raw' in context.user_data.keys() and update.message.text in context.user_data['options_raw']:
            context.user_data['entry'] = update.message.text
            await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['question_confirm'], 
                                            parse_mode=constants.ParseMode.HTML, 
                                            reply_markup=ReplyKeyboardMarkup(BUTTONS['question_buttons_2'], 
                                                                            one_time_keyboard=True))
            
            return QUESTION_23_CHECK
        else:
            await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['intro'], 
                                parse_mode=constants.ParseMode.HTML)
            await get_question(22, 'question_buttons_2', update, context)
            _ = await get_options(22, update.message.text, update, context)
            await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['next_btn_alt'], 
                                                    parse_mode=constants.ParseMode.HTML, 
                                                reply_markup=ReplyKeyboardMarkup(BUTTONS['question_buttons_2'], 
                                                                                one_time_keyboard=True))

async def question_23_check(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if 'передумал' in update.message.text.lower():
        await get_question(22, 'question_buttons', update, context)
        _ = await get_options(22, update.message.text, update, context)
        await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['next_btn'], 
                                                parse_mode=constants.ParseMode.HTML, 
                                            reply_markup=ReplyKeyboardMarkup(BUTTONS['question_buttons'], 
                                                                            one_time_keyboard=True))
        return QUESTION_23
    elif 'да, пропустить вс' in update.message.text.lower():
        await update.message.reply_text(MESSAGES['processing']['intro'], 
                                                parse_mode=constants.ParseMode.HTML)
        await update.message.reply_text(MESSAGES['processing']['contacts']['intro'], 
                                                parse_mode=constants.ParseMode.HTML, 
                                            reply_markup=ReplyKeyboardMarkup(BUTTONS['next_cancel'], 
                                                                            one_time_keyboard=True))
        return PROCESSING 
    else:
        if 'search_data' in context.user_data.keys() and '22' not in str(context.user_data['search_data'].keys()):
            context.user_data['search_data'][22] = context.user_data['entry']
            await clean_temp(update, context)

        await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['next_question'], 
                                                parse_mode=constants.ParseMode.HTML)

        await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['intro'], 
                                    parse_mode=constants.ParseMode.HTML)
        await get_question(23, 'question_buttons', update, context)
        _ = await get_options(23, update.message.text, update, context)
        await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['next_btn'], 
                                                parse_mode=constants.ParseMode.HTML, 
                                            reply_markup=ReplyKeyboardMarkup(BUTTONS['question_buttons'], 
                                                                            one_time_keyboard=True))
        return QUESTION_24

async def question_24(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    global MESSAGES, QUESTIONS, BUTTONS

    if 'показать опции' in update.message.text.lower() or 'все' in update.message.text.lower():
        _ = await get_options(23, 'все', update, context)
        await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['all_options'], 
                                        parse_mode=constants.ParseMode.HTML, 
                                        reply_markup=ReplyKeyboardMarkup(context.user_data['buttons'], 
                                                                         one_time_keyboard=True))
        
        return QUESTION_24
    elif 'скрыть опции' in update.message.text.lower():
        _ = await get_options(23, 'скрыть', update, context)
        await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['options_cleared'], 
                                        parse_mode=constants.ParseMode.HTML, 
                                        reply_markup=ReplyKeyboardMarkup(BUTTONS['question_buttons_2'], 
                                                                         one_time_keyboard=True))
        
        return QUESTION_24
    elif 'пропустить вс' in update.message.text.lower():
        await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['skip_confirm'], 
                                        parse_mode=constants.ParseMode.HTML, 
                                        reply_markup=ReplyKeyboardMarkup(BUTTONS['skip_all_yes'], 
                                                                        one_time_keyboard=True))
        return QUESTION_24_CHECK
    elif 'пропустить' in update.message.text.lower():
        await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['skip_confirm'], 
                                        parse_mode=constants.ParseMode.HTML, 
                                        reply_markup=ReplyKeyboardMarkup(BUTTONS['skip_yes'], 
                                                                        one_time_keyboard=True))
        return QUESTION_24_CHECK
    elif 'далее' in update.message.text.lower() and ('entry' not in context.user_data.keys() or not context.user_data['entry']):
        await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['prev_question'], 
                                                parse_mode=constants.ParseMode.HTML, 
                                            reply_markup=ReplyKeyboardMarkup(BUTTONS['question_buttons_2'], 
                                                                            one_time_keyboard=True))
        await get_question(23, 'question_buttons_2', update, context)

        return QUESTION_24
    else:
        if ('buttons_raw' in context.user_data.keys() and update.message.text not in context.user_data['buttons_raw']) and ('options_raw' in context.user_data.keys() and update.message.text not in context.user_data['options_raw']):
            _ = await get_options(23, update.message.text, update, context)
            
            if 'options_qty' in context.user_data.keys() and context.user_data['options_qty']:
                button = context.user_data['buttons']
                msg = 'all_options'
            else:
                button = BUTTONS['question_buttons_2']
                msg = 'option_not_found'

            await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions'][msg], 
                                            parse_mode=constants.ParseMode.HTML, 
                                            reply_markup=ReplyKeyboardMarkup(button, 
                                                                            one_time_keyboard=True))
            
            return QUESTION_24
        elif 'options_raw' in context.user_data.keys() and update.message.text in context.user_data['options_raw']:
            context.user_data['entry'] = update.message.text
            await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['question_confirm'], 
                                            parse_mode=constants.ParseMode.HTML, 
                                            reply_markup=ReplyKeyboardMarkup(BUTTONS['question_buttons_2'], 
                                                                            one_time_keyboard=True))
            
            return QUESTION_24_CHECK
        else:
            await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['intro'], 
                                parse_mode=constants.ParseMode.HTML)
            await get_question(23, 'question_buttons_2', update, context)
            _ = await get_options(23, update.message.text, update, context)
            await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['next_btn_alt'], 
                                                    parse_mode=constants.ParseMode.HTML, 
                                                reply_markup=ReplyKeyboardMarkup(BUTTONS['question_buttons_2'], 
                                                                                one_time_keyboard=True))

async def question_24_check(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if 'передумал' in update.message.text.lower():
        await get_question(23, 'question_buttons', update, context)
        _ = await get_options(23, update.message.text, update, context)
        await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['next_btn'], 
                                                parse_mode=constants.ParseMode.HTML, 
                                            reply_markup=ReplyKeyboardMarkup(BUTTONS['question_buttons'], 
                                                                            one_time_keyboard=True))
        return QUESTION_24
    elif 'да, пропустить вс' in update.message.text.lower():
        await update.message.reply_text(MESSAGES['processing']['intro'], 
                                                parse_mode=constants.ParseMode.HTML)
        await update.message.reply_text(MESSAGES['processing']['contacts']['intro'], 
                                                parse_mode=constants.ParseMode.HTML, 
                                            reply_markup=ReplyKeyboardMarkup(BUTTONS['next_cancel'], 
                                                                            one_time_keyboard=True))
        return PROCESSING 
    else:
        if 'search_data' in context.user_data.keys() and '23' not in str(context.user_data['search_data'].keys()):
            context.user_data['search_data'][23] = context.user_data['entry']
            await clean_temp(update, context)

        await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['next_question'], 
                                                parse_mode=constants.ParseMode.HTML)

        await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['intro'], 
                                    parse_mode=constants.ParseMode.HTML)
        await get_question(24, 'question_buttons', update, context)
        _ = await get_options(24, update.message.text, update, context)
        await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['next_btn'], 
                                                parse_mode=constants.ParseMode.HTML, 
                                            reply_markup=ReplyKeyboardMarkup(BUTTONS['question_buttons'], 
                                                                            one_time_keyboard=True))
        return QUESTION_25

async def question_25(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    global MESSAGES, QUESTIONS, BUTTONS

    if 'показать опции' in update.message.text.lower() or 'все' in update.message.text.lower():
        _ = await get_options(24, 'все', update, context)
        await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['all_options'], 
                                        parse_mode=constants.ParseMode.HTML, 
                                        reply_markup=ReplyKeyboardMarkup(context.user_data['buttons'], 
                                                                         one_time_keyboard=True))
        
        return QUESTION_25
    elif 'скрыть опции' in update.message.text.lower():
        _ = await get_options(24, 'скрыть', update, context)
        await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['options_cleared'], 
                                        parse_mode=constants.ParseMode.HTML, 
                                        reply_markup=ReplyKeyboardMarkup(BUTTONS['question_buttons_2'], 
                                                                         one_time_keyboard=True))
        
        return QUESTION_25
    elif 'пропустить вс' in update.message.text.lower():
        await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['skip_confirm'], 
                                        parse_mode=constants.ParseMode.HTML, 
                                        reply_markup=ReplyKeyboardMarkup(BUTTONS['skip_all_yes'], 
                                                                        one_time_keyboard=True))
        return QUESTION_25_CHECK
    elif 'пропустить' in update.message.text.lower():
        await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['skip_confirm'], 
                                        parse_mode=constants.ParseMode.HTML, 
                                        reply_markup=ReplyKeyboardMarkup(BUTTONS['skip_yes'], 
                                                                        one_time_keyboard=True))
        return QUESTION_25_CHECK
    elif 'далее' in update.message.text.lower() and ('entry' not in context.user_data.keys() or not context.user_data['entry']):
        await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['prev_question'], 
                                                parse_mode=constants.ParseMode.HTML, 
                                            reply_markup=ReplyKeyboardMarkup(BUTTONS['question_buttons_2'], 
                                                                            one_time_keyboard=True))
        await get_question(24, 'question_buttons_2', update, context)

        return QUESTION_25
    else:
        if ('buttons_raw' in context.user_data.keys() and update.message.text not in context.user_data['buttons_raw']) and ('options_raw' in context.user_data.keys() and update.message.text not in context.user_data['options_raw']):
            _ = await get_options(24, update.message.text, update, context)
            
            if 'options_qty' in context.user_data.keys() and context.user_data['options_qty']:
                button = context.user_data['buttons']
                msg = 'all_options'
            else:
                button = BUTTONS['question_buttons_2']
                msg = 'option_not_found'

            await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions'][msg], 
                                            parse_mode=constants.ParseMode.HTML, 
                                            reply_markup=ReplyKeyboardMarkup(button, 
                                                                            one_time_keyboard=True))
            
            return QUESTION_25
        elif 'options_raw' in context.user_data.keys() and update.message.text in context.user_data['options_raw']:
            context.user_data['entry'] = update.message.text
            await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['question_confirm'], 
                                            parse_mode=constants.ParseMode.HTML, 
                                            reply_markup=ReplyKeyboardMarkup(BUTTONS['question_buttons_2'], 
                                                                            one_time_keyboard=True))
            
            return QUESTION_25_CHECK
        else:
            await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['intro'], 
                                parse_mode=constants.ParseMode.HTML)
            await get_question(24, 'question_buttons_2', update, context)
            _ = await get_options(24, update.message.text, update, context)
            await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['next_btn_alt'], 
                                                    parse_mode=constants.ParseMode.HTML, 
                                                reply_markup=ReplyKeyboardMarkup(BUTTONS['question_buttons_2'], 
                                                                                one_time_keyboard=True))

async def question_25_check(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if 'передумал' in update.message.text.lower():
        await get_question(24, 'question_buttons', update, context)
        _ = await get_options(24, update.message.text, update, context)
        await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['next_btn'], 
                                                parse_mode=constants.ParseMode.HTML, 
                                            reply_markup=ReplyKeyboardMarkup(BUTTONS['question_buttons'], 
                                                                            one_time_keyboard=True))
        return QUESTION_25
    elif 'да, пропустить вс' in update.message.text.lower():
        await update.message.reply_text(MESSAGES['processing']['intro'], 
                                                parse_mode=constants.ParseMode.HTML)
        await update.message.reply_text(MESSAGES['processing']['contacts']['intro'], 
                                                parse_mode=constants.ParseMode.HTML, 
                                            reply_markup=ReplyKeyboardMarkup(BUTTONS['next_cancel'], 
                                                                            one_time_keyboard=True))
        return PROCESSING 
    else:
        if 'search_data' in context.user_data.keys() and '24' not in str(context.user_data['search_data'].keys()):
            context.user_data['search_data'][24] = context.user_data['entry']
            await clean_temp(update, context)

        await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['next_question'], 
                                                parse_mode=constants.ParseMode.HTML)

        await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['intro'], 
                                    parse_mode=constants.ParseMode.HTML)
        await get_question(25, 'question_buttons', update, context)
        _ = await get_options(25, update.message.text, update, context)
        await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['next_btn'], 
                                                parse_mode=constants.ParseMode.HTML, 
                                            reply_markup=ReplyKeyboardMarkup(BUTTONS['question_buttons'], 
                                                                            one_time_keyboard=True))
        return QUESTION_26

async def question_26(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    global MESSAGES, QUESTIONS, BUTTONS

    if 'показать опции' in update.message.text.lower() or 'все' in update.message.text.lower():
        _ = await get_options(25, 'все', update, context)
        await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['all_options'], 
                                        parse_mode=constants.ParseMode.HTML, 
                                        reply_markup=ReplyKeyboardMarkup(context.user_data['buttons'], 
                                                                         one_time_keyboard=True))
        
        return QUESTION_26
    elif 'скрыть опции' in update.message.text.lower():
        _ = await get_options(25, 'скрыть', update, context)
        await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['options_cleared'], 
                                        parse_mode=constants.ParseMode.HTML, 
                                        reply_markup=ReplyKeyboardMarkup(BUTTONS['question_buttons_2'], 
                                                                         one_time_keyboard=True))
        
        return QUESTION_26
    elif 'пропустить вс' in update.message.text.lower():
        await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['skip_confirm'], 
                                        parse_mode=constants.ParseMode.HTML, 
                                        reply_markup=ReplyKeyboardMarkup(BUTTONS['skip_all_yes'], 
                                                                        one_time_keyboard=True))
        return QUESTION_26_CHECK
    elif 'пропустить' in update.message.text.lower():
        await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['skip_confirm'], 
                                        parse_mode=constants.ParseMode.HTML, 
                                        reply_markup=ReplyKeyboardMarkup(BUTTONS['skip_yes'], 
                                                                        one_time_keyboard=True))
        return QUESTION_26_CHECK
    elif 'далее' in update.message.text.lower() and ('entry' not in context.user_data.keys() or not context.user_data['entry']):
        await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['prev_question'], 
                                                parse_mode=constants.ParseMode.HTML, 
                                            reply_markup=ReplyKeyboardMarkup(BUTTONS['question_buttons_2'], 
                                                                            one_time_keyboard=True))
        await get_question(25, 'question_buttons_2', update, context)

        return QUESTION_26
    else:
        if ('buttons_raw' in context.user_data.keys() and update.message.text not in context.user_data['buttons_raw']) and ('options_raw' in context.user_data.keys() and update.message.text not in context.user_data['options_raw']):
            _ = await get_options(25, update.message.text, update, context)
            
            if 'options_qty' in context.user_data.keys() and context.user_data['options_qty']:
                button = context.user_data['buttons']
                msg = 'all_options'
            else:
                button = BUTTONS['question_buttons_2']
                msg = 'option_not_found'

            await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions'][msg], 
                                            parse_mode=constants.ParseMode.HTML, 
                                            reply_markup=ReplyKeyboardMarkup(button, 
                                                                            one_time_keyboard=True))
            
            return QUESTION_26
        elif 'options_raw' in context.user_data.keys() and update.message.text in context.user_data['options_raw']:
            context.user_data['entry'] = update.message.text
            await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['question_confirm'], 
                                            parse_mode=constants.ParseMode.HTML, 
                                            reply_markup=ReplyKeyboardMarkup(BUTTONS['question_buttons_2'], 
                                                                            one_time_keyboard=True))
            
            return QUESTION_26_CHECK
        else:
            await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['intro'], 
                                parse_mode=constants.ParseMode.HTML)
            await get_question(25, 'question_buttons_2', update, context)
            _ = await get_options(25, update.message.text, update, context)
            await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['next_btn_alt'], 
                                                    parse_mode=constants.ParseMode.HTML, 
                                                reply_markup=ReplyKeyboardMarkup(BUTTONS['question_buttons_2'], 
                                                                                one_time_keyboard=True))

async def question_26_check(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if 'передумал' in update.message.text.lower():
        await get_question(25, 'question_buttons', update, context)
        _ = await get_options(25, update.message.text, update, context)
        await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['next_btn'], 
                                                parse_mode=constants.ParseMode.HTML, 
                                            reply_markup=ReplyKeyboardMarkup(BUTTONS['question_buttons'], 
                                                                            one_time_keyboard=True))
        return QUESTION_26
    elif 'да, пропустить вс' in update.message.text.lower():
        await update.message.reply_text(MESSAGES['processing']['intro'], 
                                                parse_mode=constants.ParseMode.HTML)
        await update.message.reply_text(MESSAGES['processing']['contacts']['intro'], 
                                                parse_mode=constants.ParseMode.HTML, 
                                            reply_markup=ReplyKeyboardMarkup(BUTTONS['next_cancel'], 
                                                                            one_time_keyboard=True))
        return PROCESSING 
    else:
        if 'search_data' in context.user_data.keys() and '25' not in str(context.user_data['search_data'].keys()):
            context.user_data['search_data'][25] = context.user_data['entry']
            await clean_temp(update, context)

        # await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['next_question'], 
        #                                         parse_mode=constants.ParseMode.HTML)

        # await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['intro'], 
        #                             parse_mode=constants.ParseMode.HTML)
        # await get_question(5, 'question_buttons', update, context)
        # _ = await get_options(5, update.message.text, update, context)
        # await update.message.reply_text(MESSAGES['new_order']['questionnaire']['questions']['next_btn'], 
        #                                         parse_mode=constants.ParseMode.HTML, 
        #                                     reply_markup=ReplyKeyboardMarkup(BUTTONS['question_buttons'], 
        #                                                                     one_time_keyboard=True))
        return PROCESSING