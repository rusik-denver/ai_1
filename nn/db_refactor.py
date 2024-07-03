from pathlib import Path
import pandas as pd
from funcs import read_dataset, options_processing, merge_options

BASE_DIR = Path(__file__).resolve().parent.parent
DB_DIR = BASE_DIR / 'db'
DB = {} # DBs dict
OPTIONS = {} #Options dict
OPTIONS_ORIGIN = {} #Options dict of original data

# original datasets (factories, orders, and options)
orig_datasets = list(Path(DB_DIR).glob('orig_*'))

# read datasets into DBs dict
for file in orig_datasets:
    title = file.name.split('.')[0].split('_')[1]
    DB.update({title: read_dataset(DB_DIR, file.name)})


# drop duplicate column - Регион производства.1 - from factories dataset
DB['factories'].drop(columns='Регион производства.1', inplace=True)

# rename & shorten column titles
DB['factories'].rename(columns={'Имя контактного лица':'Имя', 'Сфера применения':'Назначение', 'Минимальная партия, шт.':'Минимальная партия', 'Минимальная сумма заказа, руб':'Минимальный заказ', 'Наличии в реестре Минпромторга':'Минпромторг', 'Другие услуги':'Дополнительные услуги', 'Заказчик должен предоставить':'Требования к заказчику', 'Подготовка изделия к производству':'Техническая документация', 'По полу/возрасту':'Пол и возраст', 'Возможность бесплатного предоставления образцов':'Образцы'}, inplace=True)
DB['orders'].rename(columns={'По полу и возрасту':'Пол и возраст', 'Заказчик предоставит:':'Требования к заказчику', 'Нанесение логотипа/принта':'Нанесение принта', 'Описание тканей и состав фурнитуры':'Ткани и фурнитура', 'Требуется:':'Требования'}, inplace=True)

# unique options from columns
OPTIONS_ORIGIN.update({'factories': options_processing(DB['factories'][['Тип одежды', 'Назначение', 'Регион производства', 'Минимальная партия', 'Минимальный заказ', 'Другие виды изделий', 'Дополнительные услуги', 'Требования к заказчику', 'Конструирование', 'Техническая документация', 'Пол и возраст', 'Регионы поставок', 'Технология', 'Дополнительная информация', 'Загруженность', 'По сезону', 'Условия оплаты', 'Ценовой сегмент', 'Ценовые сегменты', 'Образцы']], DB['options'])})
OPTIONS_ORIGIN.update({'orders': options_processing(DB['orders'][['Вид изделия', 'Тип одежды', 'Назначение', 'Пол и возраст', 'Регион поставки', 'Регионы производства', 'Дополнительные услуги', 'Требования к заказчику', 'Количество изделий', 'Конструирование', 'Плановый бюджет', 'Сертификация', 'Техническая документация', 'Технология', 'Требования', 'Изображение', 'Название', 'Виды нанесения', 'Дизайн и моделирование', 'Комментарий к заказу', 'Нанесение принта', 'Обеспечение сырьем', 'Ткани и фурнитура', 'Плотность материала', 'Срок поставки', 'Упаковка', 'Условия оплаты', 'Цена за единицу', 'Ценовой сегмент']], DB['options'])})

# unique options from xls-file
new_options = {
    'Тип одежды':'spr_tip_odejdy',
    'Назначение':'spr_sfera_prim',
    'Регион производства':'spr_regions',
    'Регионы поставок':'spr_regions',
    'Дополнительные услуги':'spr_dop_uslugi',
    'Конструирование':'spr_tz_lekala',
    'Техническая документация':'spr_tz_tehnolog',
    'Пол и возраст':'spr_pol',
    'По сезону':'spr_sezons',
    'Вид изделия':'spr_vid_odejdy',
}
OPTIONS_ORIGIN.update({'extra_options': options_processing(new_options, DB['options'])})

# all labels/columns from all datasets
labels = list(OPTIONS_ORIGIN['factories'].keys())
labels.extend(list(OPTIONS_ORIGIN['orders'].keys()))
labels = set(list(labels))

# get rid off trash in options sets and save them in OPTIONS_ORIGIN['*_sanitized'] dict
OPTIONS_ORIGIN.update({
    'factories_sanitized': {},
    'orders_sanitized': {}
})

for l in labels:   
    if l in OPTIONS_ORIGIN['factories'].keys() and OPTIONS_ORIGIN['factories'][l] and (l == 'Дополнительная информация' or l == 'Минимальная партия' or l == 'Минимальный заказ' or l == 'Регионы поставок' or l == 'Регион производства'):
        del OPTIONS_ORIGIN['factories'][l]

    if l in OPTIONS_ORIGIN['orders'].keys() and OPTIONS_ORIGIN['orders'][l] and (l == 'Количество изделий' or l == 'Плановый бюджет' or l == 'Регион поставки' or l == 'Регионы производства' or l == 'Цена за единицу' or l == 'Срок поставки'  or l == 'Название' or l == 'Комментарий к заказу' or l == 'Изображение' or l == 'Техническая документация' or l == 'Ценовой сегмент'):
        del OPTIONS_ORIGIN['orders'][l]

# merge options from columns and xls-file
OPTIONS = merge_options(labels, OPTIONS, OPTIONS_ORIGIN)

# output all options from all columns
for key,options in OPTIONS.items():
    print(f'***** {key}: *****\n')
    print(*options, sep='\n')
    print(('*'*100 + '\n')*2)

# change options for Проверен, Минпромторг и Образцы [да, нет]
DB['factories'].fillna({'Проверен':'Нет'}, inplace=True)
DB['factories'].replace({'Проверен': 1}, value='Да', inplace=True)
DB['factories'].fillna({'Минпромторг':'Нет'}, inplace=True)
DB['factories'].fillna({'Образцы':'Нет'}, inplace=True)

# capitalize data in datasets
DB['factories'] = DB['factories'].map(lambda x: ", ".join(map(lambda y: y.capitalize(), x.split(', '))) if 'str' in str(type(x)) else x)

# save refactored DB (factories & orders)
DB['factories'].to_csv(DB_DIR / 'db_refactored_factories.csv', index=False)
print('Refactored factories dataset saved!')

DB['orders'].to_csv(DB_DIR / 'db_refactored_orders.csv', index=False)
print('Refactored orders dataset saved!')

# save options to a single DataFrame
options_db = pd.DataFrame(dict([(key, pd.Series(value)) for key, value in OPTIONS.items()]))
options_db.to_csv(DB_DIR / 'db_refactored_options.csv', index=False)
print('Refactored options dataset saved!')

# change types of columns in DBs
DB['factories'] = DB['factories'].astype({'По сезону': object, 'ИНН': object})
DB['orders'] = DB['orders'].astype({'Вид изделия': object, 'Пол и возраст': object, 'Регионы производства': object, 'Техническая документация': object, 'Условия оплаты': object, 'Ценовой сегмент': object})

# refactor DBs (factories & orders) by replacing nan's with unknown
DB['factories'].fillna('unknown', inplace=True)
DB['orders'].fillna('unknown', inplace=True)

# save refactored (without nan) DBs
DB['factories'].to_csv(DB_DIR / 'db_refactored_factories_unknown.csv', index=False)
print('Refactored factories dataset with unknown\'s saved!')

DB['orders'].to_csv(DB_DIR / 'db_refactored_orders_unknown.csv', index=False)
print('Refactored orders dataset with unknown\'s saved!')