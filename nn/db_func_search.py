from pathlib import Path
import pandas as pd
import random
from funcs import read_dataset, sfilter

BASE_DIR = Path(__file__).resolve().parent.parent
DB_DIR = BASE_DIR / 'db'
DB = {} # DBs dict
OPTIONS = {} #Options dict
CLUSTERS = {
    'search': {
        'sfilter': [('Тип одежды',['Тип одежды','Другие виды изделий']),('Назначение','Назначение'),('Количество изделий','Минимальная партия'),('Плановый бюджет','Минимальный заказ'),('Пол и возраст','Пол и возраст'),('Дополнительные услуги','Дополнительные услуги'),('Цена за единицу','Ценовой сегмент'),('Ценовой сегмент','Ценовые сегменты')],
        'location': [('Регион поставки','Регионы поставок'), ('Регионы производства','Регион производства')],
        'info': [('Техническая документация','Техническая документация'),('Технология','Технология'),(['Требования','Требования к заказчику'],'Требования к заказчику'),('Условия оплаты','Условия оплаты'),('Конструирование','Конструирование')],
    },
    'info': {
        'factories': ['Загруженность','Образцы','Дополнительная информация','По сезону'],
        'orders': ['Вид изделия', 'Изображение','Название','Дата','Плотность материала','Сертификация','Срок поставки','Упаковка','Комментарий к заказу','Нанесение принта','Обеспечение сырьем','Ткани и фурнитура','Виды нанесения','Дизайн и моделирование'],
        'profile': ['Проверен','ИНН','Минпромторг','Телефон','Email','Название','Имя','Логотип','Роли','Регистрация'],
    }
}

# read refactored datasets into DBs dict
DB.update({'options':pd.read_csv(DB_DIR / 'db_refactored_options.csv')})
DB.update({'factories':read_dataset(DB_DIR, 'db_refactored_factories.csv')})
DB.update({'orders':read_dataset(DB_DIR, 'db_refactored_orders.csv')})

# extract options from dataframe
for option in DB['options'].columns:
    OPTIONS.update({option: list(DB['options'][option].dropna().unique())})

# get random orders index
idx = random.randint(0, DB['orders'].shape[0])
row = DB['orders'].loc[idx].dropna()

# get search filter on refactored dataset with nans
results = pd.concat(sfilter(row, DB['factories'], CLUSTERS['search']))
print(row)
print(results['Тип одежды'])

# get search filter on refactored dataset with unknowns

# get search filter on refactored dataset with added generated data

# get search filter on fully generated data
