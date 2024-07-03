from pathlib import Path
import pandas as pd
import numpy as np
import random
from funcs import read_dataset, extract_row_data

BASE_DIR = Path(__file__).resolve().parent.parent
DB_DIR = BASE_DIR / 'db'
DB = {} # DBs dict
OPTIONS = {} #Options dict

# read refactored datasets into DBs dict
DB.update({'options':pd.read_csv(DB_DIR / 'db_refactored_options.csv')})
DB.update({'factories':read_dataset(DB_DIR, 'db_refactored_factories.csv')})
DB.update({'orders':read_dataset(DB_DIR, 'db_refactored_orders.csv')})

# extract options from dataframe
for option in DB['options'].columns:
    OPTIONS.update({option: list(DB['options'][option].dropna().unique())})

# columns clasterization
# sfilter and location clusters - categorize/ohe
# columns from info clusters - embedding BoW
# profile - for information in results and for weights
CLUSTERS = {
    'factories': {
        'profile': ['Проверен','ИНН','Минпромторг','Телефон','Email','Название','Имя','Логотип','Роли','Регистрация'],
        'location': ['Регион производства','Регионы поставок'],
        'sfilter': ['Тип одежды','Другие виды изделий','Назначение','Минимальная партия','Минимальный заказ','Пол и возраст','Дополнительные услуги','Ценовой сегмент'],
        'info': ['Загруженность','Требования к заказчику','Конструирование','Техническая документация','Технология','Условия оплаты','Образцы','Дополнительная информация','По сезону','Ценовые сегменты'],
    },
    'orders': {
        'location': ['Регион поставки','Регионы производства'],
        'sfilter': ['Вид изделия','Тип одежды','Назначение','Количество изделий','Плановый бюджет','Пол и возраст','Дополнительные услуги','Ценовой сегмент'],
        'info': ['Изображение','Название','Дата','Плотность материала','Сертификация','Срок поставки','Техническая документация','Технология','Требования','Упаковка','Условия оплаты','Цена за единицу','Комментарий к заказу','Конструирование','Нанесение принта','Обеспечение сырьем','Ткани и фурнитура','Виды нанесения','Дизайн и моделирование','Требования к заказчику'],
    }    
}

# categorize all options from sfilter and location clusters
# for factories and orders seperately
# other clusters - embedding/BoW
_f_categorical_columns = []
_f_categorical_columns.extend(CLUSTERS['factories']['sfilter'])
_f_categorical_columns.extend(CLUSTERS['factories']['location'])


_o_categorical_columns = []
_o_categorical_columns.extend(CLUSTERS['orders']['sfilter'])
_o_categorical_columns.extend(CLUSTERS['orders']['location'])

f_categorical_columns = np.array(_f_categorical_columns)
o_categorical_columns = np.array(_o_categorical_columns)

f_categories = {} # all factories categories dict for ohe
o_categories = {} # all orders categories dict for ohe

# get ready data for ohe
for column in categorical_columns:
    options = {}

    if column in OPTIONS.keys():
        counter = 0

        for option in OPTIONS[column]:
            options.update({option: counter})
            counter += 1

        categories.update({column: [len(OPTIONS[column]),options]})
        print(f'Options for category {column} processed successfully!')
    else:
        _column = None

        if (column == 'Регион производства') or (column == 'Регионы поставок') or (column == 'Регион поставки') or (column == 'Регионы производства'):
            _column = 'Регионы'
        elif column == 'Количество изделий':
            _column = 'Минимальная партия'
        elif column == 'Плановый бюджет':
            _column = 'Минимальный заказ'
        
        if _column in OPTIONS.keys():
            counter = 0

            for option in OPTIONS[_column]:
                options.update({option: counter})
                counter += 1
            
            categories.update({_column: [len(OPTIONS[_column]),options]})

# get random orders index
idx = random.randint(0, DB['orders'].shape[0])
row = DB['orders'].loc[idx].dropna()
print(idx)
extract_row_data(row, categories)

#save categorized data to file
        
# print(np.setdiff1d(list(OPTIONS.keys()), columns))
# print(_ - .extend(list(CLUSTERS['orders']['sfilter'])).extend(list(CLUSTERS['orders']['location'])))

# create BoW for info and profile clusters

# save BoW to file