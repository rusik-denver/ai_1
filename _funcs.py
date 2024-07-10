import time
import emoji
from pathlib import Path
import pandas as pd
from telegram import Update, constants, ReplyKeyboardMarkup
from telegram.ext import ContextTypes
import os
from dotenv import load_dotenv
from smtplib import SMTP
from email.mime.text import MIMEText

load_dotenv()
OPTIONS = {} #Options dict

# read refactored datasets into DBs dict
options_db = pd.read_csv('./db/db_refactored_options.csv')

# extract options from dataframe
for option in options_db.columns:
    OPTIONS.update({option: list(options_db[option].dropna().unique())})

QUESTIONS = [
        {
            'column':'Тип одежды',
            'question':'Какой тип одежды вы планируете заказать?',
            'clarification':'Возможно, вы имели ввиду один из следующих вариантов:',
            'options':OPTIONS['Тип одежды']
            },
        {
            'column':'Назначение или сфера применения.',
            'question':'Каково назначение или сфера применения для заказываемого товара.',
            'clarification':'Выберите один или более вариантов из следующего списка:',
            'options':OPTIONS['Назначение']
            },
        {
            'column':'Пол и возраст',
            'question':'Для какого пола и/или возрастной категории предназначены заказываемые товары?',
            'clarification':'Выберите один или более вариантов из следующего списка:',
            'options':OPTIONS['Пол и возраст']
            },
        {
            'column':'Количество изделий или минимальная партия',
            'question':'Каково количество изделий или минимальную партию для заказываемого товара.',
            'clarification':'Выберите один из следующих вариантов:',
            'options':OPTIONS['Минимальная партия']
            },
        {
            'column':'Плановый или минимальный бюджет',
            'question':'Какой плановый или минимальный бюджет предполагается для заказа?',
            'clarification':'Выберите один следующих вариантов:',
            'options':OPTIONS['Минимальный заказ']
            },
        {
            'column':'Регион производства',
            'question':'В каком регион или регионах производства будем искать фабрику.',
            'clarification':'Выберите один или более вариантов из следующего списка:',
            'options':OPTIONS['Регионы']
            },
        {
            'column':'Регион поставки',
            'question':'В какой регион необходимо доставить заказ?',
            'clarification':'Выберите один из следующих вариантов:',
            'options':OPTIONS['Регионы']
            },
        {
            'column':'Ценовой сегмент',
            'question':'В каком ценовом сегменте искать фабрику?',
            'clarification':'Выберите один из следующих вариантов:',
            'options':OPTIONS['Ценовой сегмент']
            },
        {
            'column':'Вид изделия',
            'question':'Уточните, какой вид изделия вы планируете заказать.',
            'clarification':'Выберите один из следующих вариантов:',
            'options':OPTIONS['Вид изделия']
            },
        {
            'column':'Дополнительные услуги',
            'question':'Требуются ли вам дополнительные услуги и если да, то укажите, какие?',
            'clarification':'Выберите один или более вариантов из следующего списка:',
            'options':OPTIONS['Дополнительные услуги']
            },
        {
            'column':'Техническая документация',
            'question':'Укажите требования для технической документации, если такие имеются.',
            'clarification':'Выберите один из следующих вариантов:',
            'options':OPTIONS['Техническая документация']
            },
        {
            'column':'Технология',
            'question':'Укажите требования для технологии, если такие имеются.',
            'clarification':'Выберите один или более вариантов из следующего списка:',
            'options':OPTIONS['Технология']
            },
        {
            'column':'Требования к исполнителю',
            'question':'Укажите требования к исполнителю, если такие имеются.',
            'clarification':'Выберите один или более вариантов из следующего списка:',
            'options':OPTIONS['Требования']
            },
        {
            'column':'Условия оплаты',
            'question':'Если имеются условия оплаты, укажите их.',
            'clarification':'Выберите один из следующих вариантов:',
            'options':OPTIONS['Условия оплаты']
            },
        {
            'column':'Конструирование',
            'question':'Укажите требования для конструирования, если такие имеются.',
            'clarification':'Выберите один или более вариантов из следующего списка:',
            'options':OPTIONS['Конструирование']
            },
        {
            'column':'Образцы',
            'question':'Необходимы ли вам бесплатные образцы перед тем, как сделать заказ? (Да/Нет)',
            'clarification':None,
            'options':None
            },
        {
            'column':'Дизайн и моделирование',
            'question':'Укажите требования для дизайна и моделирования, если такие имеются.',
            'clarification':None,
            'options':None
            },
        {
            'column':'Виды нанесения',
            'question':'Укажите требования для видов нанесения, если такие имеются.',
            'clarification':None,
            'options':None
            },
        {
            'column':'Нанесение принта',
            'question':'Укажите требования для нанесения принта, если такие имеются.',
            'clarification':None,
            'options':None
            },
        {
            'column':'Ткани и фурнитура',
            'question':'Укажите требования для ткани и фурнитуры, если такие имеются.',
            'clarification':None,
            'options':None
            },
        {
            'column':'Плотность материала',
            'question':'Укажите требования для плотности материала, если такие имеются.',
            'clarification':None,
            'options':None
            },
        {
            'column':'Обеспечение сырьём',
            'question':'Укажите требования для обеспечения сырьём, если такие имеются.',
            'clarification':None,
            'options':None
            },
        {
            'column':'Сертификация',
            'question':'Укажите требования для сертификации, если такие имеются.',
            'clarification':None,
            'options':None
            },
        {
            'column':'Сроки поставки',
            'question':'Укажите крайнюю дату поставки заказа.',
            'clarification':None,
            'options':None
            },
        {
            'column':'Упаковка',
            'question':'Укажите требования для упаковки, если такие имеются.',
            'clarification':None,
            'options':None},
        {
            'column':'Комментарий к заказу',
            'question':'Вы можете оставить комментарий к заказу.',
            'clarification':None,
            'options':None
            },
]

BUTTONS = {
    'start': [[emoji.emojize(':rocket: СТАРТ')]],
    'order_type': [
        [emoji.emojize(":package: СУЩЕСТВУЮЩИЙ ЗАКАЗ")],
        [emoji.emojize(":shopping_cart: НОВЫЙ ЗАКАЗ"),
            emoji.emojize(':cross_mark: ОТМЕНА')],
    ],
    'search_type': [
        [emoji.emojize(':spiral_notepad: АНКЕТИРОВАНИЕ')],
        [emoji.emojize(':magnifying_glass_tilted_right: ПОИСК ПО ШАБЛОНУ')],
        [emoji.emojize(':gear: ПРОИЗВОЛЬНЫЙ ПОИСК')],
        [emoji.emojize(':cross_mark: ОТМЕНА')],
    ],
    'back_cancel': [[
        emoji.emojize(':backhand_index_pointing_left: НАЗАД'),
        emoji.emojize(':cross_mark: ОТМЕНА'),
    ]],
    'next_back': [[
        emoji.emojize('ПРОДОЛЖИТЬ :backhand_index_pointing_right:'),
        emoji.emojize(':backhand_index_pointing_left: НАЗАД'),
    ]],
    'next_back_cancel': [
        [emoji.emojize('ПРОДОЛЖИТЬ :backhand_index_pointing_right:')],
        [emoji.emojize(':backhand_index_pointing_left: НАЗАД'),
            emoji.emojize(':cross_mark: ОТМЕНА')],
    ],
    'next_cancel': [[
        emoji.emojize('ПРОДОЛЖИТЬ :backhand_index_pointing_right:'),
        emoji.emojize(':cross_mark: ОТМЕНА'),
    ]],
    'question_buttons': [
        [emoji.emojize("ПОКАЗАТЬ ОПЦИИ :card_index_dividers:"),
            emoji.emojize('ДАЛЕЕ :backhand_index_pointing_right:')],
        [emoji.emojize('ПРОПУСТИТЬ :man_running:'),
            emoji.emojize('ПРОПУСТИТЬ ВСË :man_surfing:')],
    ],
    'question_buttons_1': [[
        emoji.emojize("ПОКАЗАТЬ ОПЦИИ :card_index_dividers:"),
        emoji.emojize('ДАЛЕЕ :backhand_index_pointing_right:'),
    ]],
    'question_buttons_2': [
        [emoji.emojize('ДАЛЕЕ :backhand_index_pointing_right:'),
            emoji.emojize('ПРОПУСТИТЬ :man_running:')],
        [emoji.emojize('ПРОПУСТИТЬ ВСË :man_surfing:')],
    ],
    'skip': [[
        emoji.emojize(':man_running: ПРОПУСТИТЬ'),
        emoji.emojize(':backhand_index_pointing_left: НАЗАД'),
    ]],
    'skip_yes': [[
        emoji.emojize(':man_running: ДА, ПРОПУСТИТЬ'),
        emoji.emojize(':backhand_index_pointing_left: ПЕРЕДУМАЛ'),
    ]],
    'skip_all_yes': [
        [emoji.emojize(':man_running: ДА, ПРОПУСТИТЬ ВСЕ')],
        [emoji.emojize(':backhand_index_pointing_left: ПЕРЕДУМАЛ')],
    ],
    'search': [[emoji.emojize(':magnifying_glass_tilted_right: ИСКАТЬ')]],
    'show_hide_options': [[
        emoji.emojize("ПОКАЗАТЬ ОПЦИИ :card_index_dividers:"),
        emoji.emojize("СКРЫТЬ ОПЦИИ :card_index_dividers:"),
    ]],
    'hide_options': [[emoji.emojize("СКРЫТЬ ОПЦИИ :card_index_dividers:")]],
    'show_options': [[emoji.emojize("ПОКАЗАТЬ ОПЦИИ :card_index_dividers:")]],
}

MESSAGES = {
    'start_step': [
        emoji.emojize('<b>Привет! Я ИИ-помощник :robot: по подбору фабрик :factory: для выполнения заказов :package: по пошиву одежды :dress:.</b>'),
        emoji.emojize('<b><i>Я с радостью :nerd_face: помогу вам подобрать список :card_index_dividers: оптимальных фабрик :factory: для выполнения вашего заказа :hundred_points:.</i></b>'),
        emoji.emojize('<b>:fire: Для запуска программы нажмите :rocket: СТАРТ.</b>')
        ],
    'launch_step': {
        'intro': emoji.emojize('<u>Уточните, пожалуйста</u> :slightly_smiling_face:, <u>это поиск для нового</u> :shopping_cart: <u>заказа или существующего</u> :package:?'),
    },
    'existed_order': {
        'intro': emoji.emojize('<i>ОК. Раз заказ уже существует :package:, отправьте нам, пожалуйста, номер заказа :input_numbers: в формате #xxxx (знак решётки и номер заказа) или нажмите :backhand_index_pointing_left: НАЗАД, если вы не помните номер.</i>'),
        'wrong_order_format': emoji.emojize(':cross_mark: Неверный формат заказа. Номер заказа начинается со знака решётка, после которого следуют цифры (#12345). Если вы не помните :thinking_face: номер заказа и хотите начать новый поиск, нажмите :backhand_index_pointing_left: НАЗАД.'),
    },
    'new_order': {
        'intro': emoji.emojize(''':exclamation_question_mark: <b>Каким образом вы хотите осуществить поиск :magnifying_glass_tilted_left:? Выберите из списка :card_index_dividers:.</b>
            
    <i>:backhand_index_pointing_right: АНКЕТИРОВАНИЕ :spiral_notepad: - подробный аопросник</i>,
    <i>:backhand_index_pointing_right: ПОИСК ПО ФИЛЬТРАМ :magnifying_glass_tilted_left:  - поиск по отдельным характеристикам</i>,
    <i>:backhand_index_pointing_right: ПРОИЗВОЛЬНЫЙ ПОИСК :gear: - поиск по перечисленным через запятую характеристикам</i>.
        
:information: Для отмены, нажмите :cross_mark: ОТМЕНА'''),
        'questionnaire': {
            'intro': emoji.emojize('''Вы выбрали ПОИСК через АНКЕТИРОВАНИЕ :spiral_notepad:. Это самый длительный способ, но он даёт наиболее точный результат :hundred_points:.
Если вы готовы, нажмите :backhand_index_pointing_right: ПРОДОЛЖИТЬ.
Для возврата к предыдущему меню, нажмите :backhand_index_pointing_left: НАЗАД.'''),
            'info': emoji.emojize(''':exclamation_question_mark: <b>Для определения критериев поиска :magnifying_glass_tilted_left:, мы зададим вам несколько вопросов :speech_balloon:. Чем больше критериев :card_index_dividers: для поиска вы введёте, тем точнее результат получите :hundred_points:.</b>

Чтобы перейти к анкетированию нажмите :backhand_index_pointing_right: ПРОДОЛЖИТЬ.'''),
            'photo_intro': emoji.emojize(':index_pointing_up: Для начала, отправьте фото :framed_picture: образцов изделия или изделий, которые вы планируете заказать :shopping_cart:.'),
            'photo_uploaded': emoji.emojize('Спасибо :folded_hands:, мы получили ваше фото :framed_picture:.'),
            'photo_processing': emoji.emojize('🕐 Обработка фото :framed_picture:...'),
            'photo_error': emoji.emojize(':cross_mark: Не удалось загрузить фото :framed_picture:. Используйте фото в формате JPG или PNG. Попробуйте загрузить фото ещё раз.'),
            'questions': {
                'intro': emoji.emojize(''':speech_balloon: <i>Отправте ваш ответ или выберите из представленного списка :card_index_dividers:.
Для пропуска отдельных вопросов, нажмите :man_running: ПРОПУСТИТЬ, а чтобы пропустить все оставшиеся вопросы нажмите :man_surfing: ПРОПУСТИТЬ ВСЕ.</i>'''),
                'next_question': emoji.emojize(':man_running: Переходим к следующему вопросу.'),
                'prev_question': emoji.emojize('Вы не ответили на вопрос. Чтобы перейти к следующему вопросу, ответьте на вопрос и нажмите :backhand_index_pointing_right: ДАЛЕЕ. Если в меню есть кнопка ПРОПУСТИТЬ, нажмите её, чтобы пропустить вопрос.'),
                'next_btn': emoji.emojize(':sparkles: Выберите все желаемые опции :card_index_dividers: и/или нажмите :pinching_hand: любую для продолжения.'),
                'next_btn_alt': emoji.emojize(':sparkles: Выберите один ответ и/или нажмите :backhand_index_pointing_right: ДАЛЕЕ для продолжения.'),
                'all_options': emoji.emojize('Выберите ответ из представленных опций :card_index_dividers:'),
                'options_cleared': emoji.emojize('Список возможных опций убран :backhand_index_pointing_up:. Введите ваше значение :input_latin_letters:.'),
                'question_confirm': emoji.emojize(':thinking_face: Если вы закончили с ответом, нажмите :backhand_index_pointing_right: ДАЛЕЕ'),
                'option_not_found': emoji.emojize(':writing_hand: Введите другое слово или слова через запятую. Чтобы увидеть :eye: список всех возможных значений :card_index_dividers: введите слово ВСЕ или нажмине :pinching_hand: на :card_index_dividers: ПОКАЗАТЬ ОПЦИИ.'),
                'skip_confirm': emoji.emojize(':exclamation_question_mark: Вы уверены, что хотите пропустить вопрос :man_running: и перейти к следующему вопросу?'),
                'skip_all_confirm': emoji.emojize(':exclamation_question_mark: Вы уверены, что хотите пропустить все оставшиеся вопросы :man_running: и перейти к подбору исполнителей?'),
    
            },
        },
        'filters': {
            'intro': emoji.emojize('''Вы выбрали ПОИСК ПО ФИЛЬТРАМ :magnifying_glass_tilted_left:. Вам необходимо будет ввести критерии поиска вручную :keyboard:.
Если вы готовы, нажмите :backhand_index_pointing_right: ПРОДОЛЖИТЬ.
Для возврата к предыдущему меню, нажмите :backhand_index_pointing_left: НАЗАД.'''),
            'info': emoji.emojize(''':exclamation_question_mark: <b>Для ввода критериев поиска следуйте следующему шаблону :world_map::</b>
        :pushpin: [минимальная партия];
        :pushpin: [минимальная сумма заказа];
        :pushpin: [регион/ы производства];
        :pushpin: [регион/ы поставки];
        :pushpin: [ценовой сегмент];
        :pushpin: [вид изделия];
        :pushpin: [дополнительные услуги];
        :pushpin: [техническая документация];
        :pushpin: [технология];
        :pushpin: [требования к фабрике];
        :pushpin: [условия оплаты];
        :pushpin: [требования по дизайну и моделированию];
        :pushpin: [необходимы ли образцы];
        :pushpin: [требования по дизайну и моделированию];
        :pushpin: [виды нанесения];
        :pushpin: [нанесение логотипа/принта];
        :pushpin: [ткани и фурнитура];
        :pushpin: [плотность материала];
        :pushpin: [обеспечение сырьём];
        :pushpin: [сертификация];
        :pushpin: [сроки поставки];
        :pushpin: [упаковка];
        :pushpin: [комментарий к заказу]
:exclamation_question_mark: <i>Используйте только необходимые :double_exclamation_mark: критерии и не удаляйте :wastebasket: не использованные. Вместо наименования критерия добавить неограниченное :infinity: количество значений, разделяя их запятыми.</i>
Для этого скопируйте следующую строку и отправьте нам после редактирования: 

    [минимальная_партия];[минимальная_сумма_заказа];[регион/ы_производства];[регион/ы_поставки];[ценовой_сегмент];[вид_изделия];[дополнительные_услуги];[техническая_документация];[технология];[требования_к_фабрике];[условия_оплаты];[требования_по_дизайну_и_моделированию];[необходимы_ли_образцы];[требования_по_дизайну_и_моделированию];[виды_нанесения];[нанесение_логотипа/принта];[ткани_и_фурнитура];[плотность_материала];[обеспечение_сырьём];[сертификация];[сроки_поставки];[упаковка];[комментарий_к_заказу]'''),
        },
        'custom': {
            'intro': emoji.emojize('Вы выбрали ПРОИЗВОЛЬНЫЙ ПОИСК :gear:. Вам необходимо ввести критерии поиска вручную :input_latin_letters: через запятую и отправить нам. Для продоления нажмите :backhand_index_pointing_right: ДАЛЕЕ, для возврата к предыдущему меню, нажмите :backhand_index_pointing_left: НАЗАД.'),
            'info': emoji.emojize(':information: Введите необходимые :double_exclamation_mark: характеристики в произвольной форме :gear:, разделяя их запятыми и отпрвьте нам.'),
        }
    },
    'processing': {
        'intro': emoji.emojize(':flexed_biceps: Всё готово к поиску!'),
        'output_number': emoji.emojize('Пришлите количество результатов, которые вы хотите получить.'),
        'wrong_number': emoji.emojize('Неверный формат данных. Количество результатов должно быть числом от 1 до 100. Попробуйте еще раз.'),
        'contacts': {
            'intro': emoji.emojize('Для того, чтобы мы смогли отправить :e_mail: вам результаты поиска :card_index_dividers:, нам нужно знать, кому отправить :information: информацию о вашем заказе :shopping_cart:. Если вы согласны :check_mark_button: предоставить нам эту информацию :information: нажмите :backhand_index_pointing_right: ДАЛЕЕ, если нет нажмите :cross_mark: ОТМЕНА.'),
            'email': emoji.emojize('Введите :information: Вашу электронную почту :envelope:, на которую придут результаты поиска :magnifying_glass_tilted_left:.'),
            'thanks': emoji.emojize('Спасибо :folded_hands: за ваши :information: контактные данные.'),
        },
        'init': emoji.emojize('Чтобы приступить к обработке :fire_engine: запроса и предоставить вам список :card_index_dividers: подходящих фабрик :factory:, нажмите :backhand_index_pointing_right: ПРОДОЛЖИТЬ.'),
    },
    'finish': {
        'intro': emoji.emojize(':check_mark_button: Поиск завершён. Результаты :beer_mug: придут вам на email.'),
        'sent': emoji.emojize(':information: Ваши результаты поиска :card_index_dividers: отправлены на электронную почту :envelope:.')
    },
    'cancel': emoji.emojize(':double_exclamation_mark: Вы отменили поиск. Если хотите начать новый поиск :magnifying_glass_tilted_left:, введите /start'),
    'photo': {
        'results': emoji.emojize(':information: Результаты анализа полученного изображения :framed_picture::.'),
    },

    
    'order_id_entered': emoji.emojize(':information:Номер заказа: {}. Если верно, нажмите :magnifying_glass_tilted_right: ИСКАТЬ или измените :pencil: номер заказа.'),
    'skip_all': emoji.emojize(':exclamation_question_mark: Вы действительно хотите пропустить все :man_surfing: оставшиеся вопросы? Количество заданных критериев влияет на точность :hundred_points: поиска. Нажмите :backhand_index_pointing_right: ПРОДОЛЖИТЬ для начала поиска или :backhand_index_pointing_left: НАЗАД для возврата к вопросам.'),
    'skip_to_processing_confirm': emoji.emojize(':exclamation_question_mark: Вы уверены, что хотите пропустить вопрос :man_running: и перейти к обработке запроса?'),
    'process_intro': emoji.emojize('Спасибо :folded_hands: за ваши ответы. Теперь мы готовы :clapping_hands: перейти к обработке :fire_engine: вашего запроса.'),
    'contacts_confirm': emoji.emojize('Переходим к формированию :building_construction: списка подходящих фабрик :factory: для реализации вашего заказа :package:. Чтобы продолжить, нажмите :backhand_index_pointing_right: ДАЛЕЕ.'),
    'processing_contacts': emoji.emojize('Для того, чтобы мы смогли отправить :e_mail: вам результаты поиска :card_index_dividers:, нам нужно знать, кому отправить :information: информацию о вашем заказе :shopping_cart:. Если вы согласны :check_mark_button: предоставить нам эту информацию :information: нажмите :backhand_index_pointing_right: ДАЛЕЕ, если нет нажмите :cross_mark: ОТМЕНА.'),
    'comment_error': emoji.emojize(':cross_mark: Вы не ввели :pencil: комментарий. Если вы не хотите добавлять комментарий, нажмите :backhand_index_pointing_right: ПРОПУСТИТЬ.'),
}

HELP = '''
Добро пожаловать в ИИ-помощник по подбору фабрик для заказа одежды!

В меню вы можете выбрать один из следующих вариантов:
    \U0001F449 <b>Поиск фабрик по общему фильтру</b> - вам будут заданы вопросы по каждой из характеристик, две из которых обязательные, а из остальных можно :man_surfing: пропустить все или только некоторые из них. <i>Точность результатов поиска зависят от того, насколько полно вы заполните все поля.</i>
      
    \U0001F449 <b>Поиск фабрик по отдельным характиристикам</b>. Для этого используется следующий шаблон:

      \U00002705 <b><i>тип одежды</i></b>: [тип одежды], 
      \U00002705 <b><i>назначение</i></b>: [назначение], 
      \U00002705 <b><i>пол и возраст</i></b>: [пол и возраст], 
      \U00002705 <b><i>минимальная партия</i></b>: [минимальная партия], 
      \U00002705 <b><i>минимальный заказ</i></b>: [минимальная сумма заказа],
      \U00002705 <b><i>регион производства</i></b>: [регион/ы производства], 
      \U00002705 <b><i>регион поставки</i></b>: [регион/ы поставки],
      \U00002705 <b><i>ценовой сегмент</i></b>: [ценовой сегмент], 
      \U00002705 <b><i>вид изделия</i></b>: [вид изделия], 
      \U00002705 <b><i>дополнительные услуги</i></b>: [дополнительные услуги],
      \U00002705 <b><i>техническая документация</i></b>: [техническая документация], 
      \U00002705 <b><i>технология</i></b>: [технология],
      \U00002705 <b><i>требования</i></b>: [требования к фабрике], 
      \U00002705 <b><i>условия оплаты</i></b>: [условия оплаты], 
      \U00002705 <b><i>конструирование</i></b>: [требования по дизайну и моделированию],
      \U00002705 <b><i>образцы</i></b>: [необходимы ли образцы], 
      \U00002705 <b><i>дизайн и моделирование</i></b>: [требования по дизайну и моделированию], 
      \U00002705 <b><i>виды нанесения</i></b>: [виды нанесения],
      \U00002705 <b><i>нанесение принта</i></b>: [нанесение логотипа/принта], 
      \U00002705 <b><i>ткани и фурнитура</i></b>: [ткани и фурнитура], 
      \U00002705 <b><i>плотность материала</i></b>: [плотность материала],
      \U00002705 <b><i>обеспечение сырьём</i></b>: [обеспечение сырьём], 
      \U00002705 <b><i>сертификация</i></b>: [сертификация], 
      \U00002705 <b><i>сроки поставки</i></b>: [сроки поставки], 
      \U00002705 <b><i>упаковка</i></b>: [упаковка],
      \U00002705 <b><i>комментарий к заказу</i></b>: [комментарий к заказу]

      Используйте только необходимые критерии. Вы можете добавить неограниченное количество значений в каждый пункт, разделяя их запятыми.
'''

FILTERS = ['тип_одежды','назначение','пол_и_возраст','минимальная_партия','минимальная_сумма_заказа','регион/ы_производства','регион/ы_поставки','ценовой_сегмент','вид_изделия','дополнительные_услуги','техническая_документация','технология','требования_к_фабрике','условия_оплаты','требования_по_дизайну_и_моделированию','необходимы_ли_образцы','требования_по_дизайну_и_моделированию','виды_нанесения','нанесение_логотипа/принта','ткани_и_фурнитура','плотность_материала','обеспечение_сырьём','сертификация','сроки_поставки','упаковка','комментарий_к_заказу']

#questions options
options_range = [x for x in range(15)]
multichoice_options = [1,2,5,9,11,12,14]

# Email configuration (replace with your own email details)
EMAIL_HOST = os.getenv('SMTP_HOST')
EMAIL_PORT = os.getenv('SMTP_PORT')
EMAIL_ADDRESS = os.getenv('SMTP_EMAIL')
EMAIL_PASSWORD = os.getenv('SMTP_PASSWORD')

#conversation steps
LAUNCH, ORDER_TYPE, SEARCH_TYPE, CUSTOM_SEARCH, FILTERS_SEARCH, QUESTIONS_INTRO, QUESTIONS_PHOTO, QUESTIONNAIRE, PROCESSING, SEARCH_INIT, CONTACTS_EMAIL, CONTACTS_FINISH = range(12)
QUESTION_1, QUESTION_2, QUESTION_3, QUESTION_4, QUESTION_5, QUESTION_6, QUESTION_7, QUESTION_8, QUESTION_9, QUESTION_10, QUESTION_11, QUESTION_12, QUESTION_13, QUESTION_14, QUESTION_15, QUESTION_16, QUESTION_17, QUESTION_18, QUESTION_19, QUESTION_20, QUESTION_21, QUESTION_22, QUESTION_23, QUESTION_24, QUESTION_25, QUESTION_26 = range(12,38)
QUESTION_1_CHECK, QUESTION_2_CHECK, QUESTION_3_CHECK, QUESTION_4_CHECK, QUESTION_5_CHECK, QUESTION_6_CHECK, QUESTION_7_CHECK, QUESTION_8_CHECK, QUESTION_9_CHECK, QUESTION_10_CHECK, QUESTION_11_CHECK, QUESTION_12_CHECK, QUESTION_13_CHECK, QUESTION_14_CHECK, QUESTION_15_CHECK, QUESTION_16_CHECK, QUESTION_17_CHECK, QUESTION_18_CHECK, QUESTION_19_CHECK, QUESTION_20_CHECK, QUESTION_21_CHECK, QUESTION_22_CHECK, QUESTION_23_CHECK, QUESTION_24_CHECK, QUESTION_25_CHECK, QUESTION_26_CHECK = range(38,64)
#functions
#function for getting help
def get_help():
    global HELP
    return HELP

#get questions output
async def get_question(id, btn, update: Update, context:ContextTypes) -> None:
    global options_range, QUESTIONS, BUTTONS

    question = QUESTIONS[id]
    await update.message.reply_text('Критерий: ' + question['column'])
    time.sleep(0.15)
    await update.message.reply_text(question['question'], 
                                    parse_mode=constants.ParseMode.HTML, 
                                    reply_markup=ReplyKeyboardMarkup(BUTTONS[btn], 
                                                                    one_time_keyboard=True))

#function returns a list of options available
async def get_options(id: int, text: str, update: Update, context: ContextTypes) -> list:
    global options_range, BUTTONS, QUESTIONS

    if id in range(len(QUESTIONS)):
        question = QUESTIONS[id]
        suggestions = {
            'buttons': [],
            'suggestions': []
        }

        #you can skip questions now
        if id in options_range:
            if text != 'скрыть':
                suggestions['buttons'].append(BUTTONS['hide_options'][0])
            else:
                suggestions['buttons'].append(BUTTONS['show_options'][0])
        
        if text != 'скрыть':
            for opt in question['options']:        
                if text.lower() == 'все': #all options
                    suggestions['suggestions'].append([opt])
                elif ',' in text: #list of options
                    for e in text.lower().split(','):
                        if e.strip() in opt.lower():
                            suggestions['suggestions'].append([opt])
                elif text.lower() in opt.lower(): #single option
                    suggestions['suggestions'].append([opt])
        
        await get_suggestions(id, suggestions, update, context)
        return suggestions
    else:
        return []

#get options, suggestions and buttons
async def get_suggestions(id, options, update:Update, context:ContextTypes) -> None:
    global QUESTIONS

    buttons = options['buttons'].copy()
    buttons.extend(options['suggestions'])
    context.user_data['buttons'] = buttons.copy()
    context.user_data['options_raw'] = QUESTIONS[id]['options']
    context.user_data['buttons_raw'] = [x[0] for x in buttons]
    context.user_data['options_qty'] = len(buttons) - len(options['buttons'])

async def clean_temp(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if 'entry' in context.user_data.keys(): del context.user_data['entry']
    if 'buttons' in context.user_data.keys(): del context.user_data['buttons']
    if 'suggestions' in context.user_data.keys(): del context.user_data['suggestions']
    if 'question' in context.user_data.keys(): del context.user_data['question']
    if 'options_raw' in context.user_data.keys(): del context.user_data['options_raw']
    if 'options_qty' in context.user_data.keys(): del context.user_data['options_qty']
    if 'buttons_raw' in context.user_data.keys(): del context.user_data['buttons_raw']
    if 'questions_qty' in context.user_data.keys(): del context.user_data['questions_qty']

async def send_recommendations_email(recommendations: list, db, email: str) -> None:
    res=''
    for i in range(recommendations.shape[0]):
        result = db.iloc[recommendations.index[i],:].dropna()
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

    body = f'Recommended manufacturers for your order: \n\n{res}'

    msg = MIMEText(body, 'plain')
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = email  # Replace with recipient's email
    msg['Subject'] = 'Recommended Manufacturers'

    with SMTP(EMAIL_HOST, EMAIL_PORT) as server:
        # server.set_debuglevel(1)
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.sendmail(f'Ruslan <{EMAIL_ADDRESS}>', email, msg.as_string())
    
    return 'sent'

async def create_order_request(data, update: Update, context: ContextTypes) -> list|int|str:
    if 'order_id' in context.user_data.keys() and context.user_data['order_id']:
        return int(context.user_data['order_id'])
    elif 'order_query' in context.user_data.keys() and context.user_data['order_query']:
        if isinstance(context.user_data['order_query'], dict):
            return list(filter(lambda x: x is not None, map(lambda x: x[1], context.user_data['order_query'].items())))
        elif isinstance(context.user_data['order_query'], list):
            return context.user_data['order_query']
    elif 'search_data' in context.user_data.keys() and context.user_data['search_data']:
        return list(filter(lambda x: x is not None, map(lambda x: x[1], context.user_data['search_data'].items())))