from telegram import Update, constants
from telegram.ext import ContextTypes, ConversationHandler
from _funcs import *
from _nn import recommended_manufacturers
import os
import dotenv

load_dotenv()

# contacts step
async def contacts_intro(update:Update, context:ContextTypes) -> int:
    if ('далее' in update.message.text.lower() or 'продолжить' in update.message.text.lower()) and 'contacts' not in context.user_data.keys():
        context.user_data['contacts'] = {}
        context.user_data['contacts_finished'] = False
        await update.message.reply_text(MESSAGES['processing']['contacts']['name'], 
                                        parse_mode=constants.ParseMode.HTML)
        return CONTACTS_COMPANY
            
async def contacts_company(update: Update, context:ContextTypes) -> int:
    if 'name' not in context.user_data['contacts'].keys() and update.message.text:
        context.user_data['contacts']['name'] = update.message.text
        await update.message.reply_text(MESSAGES['processing']['contacts']['company'], 
                                        parse_mode=constants.ParseMode.HTML)
        
        return CONTACTS_EMAIL
    
async def contacts_email(update: Update, context:ContextTypes) -> int:
    if 'company' not in context.user_data['contacts'].keys() and update.message.text:
        context.user_data['contacts']['company'] = update.message.text
        await update.message.reply_text(MESSAGES['processing']['contacts']['email'], 
                                        parse_mode=constants.ParseMode.HTML)
        
        return CONTACTS_PHONE
    
async def contacts_phone(update: Update, context:ContextTypes) -> int:
    if 'email' not in context.user_data['contacts'].keys() and update.message.text:
        context.user_data['contacts']['email'] = update.message.text
        await update.message.reply_text(MESSAGES['processing']['contacts']['phone'], 
                                        parse_mode=constants.ParseMode.HTML)
        
        return CONTACTS_FINISH

async def contacts_finish(update: Update, context:ContextTypes) -> int:
    if 'phone' not in context.user_data['contacts'].keys() and update.message.text:
        context.user_data['contacts']['phone'] = update.message.text
        
        await update.message.reply_text(MESSAGES['processing']['contacts']['thanks'], 
                                        parse_mode=constants.ParseMode.HTML)
        await update.message.reply_text(MESSAGES['finish']['intro'], 
                                        parse_mode=constants.ParseMode.HTML)

        order_request = await create_order_request(context.user_data, update, context)
        results, db = recommended_manufacturers(order_request, n=int(context.user_data['output_number']), original=True, db_type='original')
        sent = await send_recommendations_email(results, db, f'{context.user_data["contacts"]["name"]} <{context.user_data["contacts"]["email"]}>')
        
        res=''
        for i in range(results.shape[0]):
            result = db.iloc[results.index[i],:].dropna()
            res+=f'#{i+1}\n'

            for key, val in result.items():
                text = []

                if isinstance(val, str) and len(val):
                    for x in val.split(', '):
                        text.append(x)

                text = ", ".join(text)
                res+=f'{key}: {text}'
                res+='\n'
            res+='*'*100
            res+='\n'

        body = f'Часть результатов поиска: \n\n{res[:4000]}...'
        await update.message.reply_text(body,
                                        parse_mode=constants.ParseMode.HTML)

        if sent:
            await update.message.reply_text(MESSAGES['finish']['sent'], 
                                        parse_mode=constants.ParseMode.HTML)
            context.user_data.clear()
        

        return ConversationHandler.END
