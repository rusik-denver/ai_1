import random
import datetime
import numpy as np
from faker import Faker
from faker.providers import DynamicProvider

# factories reandom data generation
def factories_gen(options, qty):
  fake = Faker('ru_RU')
  data = []

  for i in range(qty):
    name = fake.first_name() + ' ' + fake.last_name()
    verified = list(np.random.choice(['нет','да'], 1, p=[0.25, 0.75]))[0] # amount of verified accounts is about 75%

    if verified == 'да': # if verified, other required columns should be filled
      inn = random.randrange(10**(11), 10**12)
      minpromtorg = 'да'
      phone = random.randrange(10**(10), 10**11)
      email = fake.ascii_free_email()
      title = fake.company()
    else: # if not verified, we add ИНН in about 80% of cases etc.
      inn = list(np.random.choice([None, random.randrange(10**(11), 10**12)], 1, p=[0.2, 0.8]))[0]
      minpromtorg = list(np.random.choice(['нет','да'], 1, p=[0.3, 0.7]))[0]

      if inn != None or minpromtorg != 'нет':
        phone = list(np.random.choice([None, random.randrange(10**(10), 10**11)], 1, p=[0.2,0.8]))[0]

        if phone != None:
          email = list(np.random.choice([None, fake.ascii_company_email()], 1, p=[0.3,0.7]))[0]
        else:
          email = list(np.random.choice([None, fake.ascii_company_email()], 1, p=[0,1]))[0]

        title = list(np.random.choice([None, fake.company()], 1, p=[0.2, 0.8]))[0]
        name = list(np.random.choice([None, name], 1, p=[0.2,0.8]))[0]

      else:
        verified = list(np.random.choice(['нет','да'], 1, p=[0.3, 0.7]))[0]
        inn = list(np.random.choice([None, random.randrange(10**(11), 10**12)], 1, p=[0.2, 0.8]))[0]
        minpromtorg = list(np.random.choice(['нет','да'], 1, p=[0.3, 0.7]))[0]
        phone = list(np.random.choice([None, random.randrange(10**(10), 10**11)], 1, p=[0.3,0.7]))[0]

        if phone != None:
          email = list(np.random.choice([None, fake.ascii_company_email()], 1, p=[0.7,0.3]))[0]
        else:
          email = list(np.random.choice([None, fake.ascii_company_email()], 1, p=[0,1]))[0]

        title = list(np.random.choice([None, fake.company()], 1, p=[0.7, 0.3]))[0]
        name = list(np.random.choice([None, name], 1, p=[0.7,0.3]))[0]

    # generate data
    data.append({
      'Проверен': verified,
      'ИНН': inn,
      'Минпромторг': minpromtorg,
      'Телефон': phone,
      'Email': email,
      'Название': title,
      'Имя': name,
      'Логотип': list(np.random.choice([None, fake.image_url()], 1, p=[0.3, 0.7]))[0],
      'Роли': list(np.random.choice(['Магазин продавца', 'Магазин продавца, Клиент'], 1, p=[0.7, 0.3]))[0],
      'Регистрация': fake.date_time_between_dates(datetime_start=datetime.datetime(2022,1,1,0,0,0), datetime_end=datetime.datetime(2024,4,25,23,59,59)),

      'Тип одежды': ", ".join(list(np.random.choice(options['Тип одежды'], random.randint(0,len(options['Тип одежды'])-1)))),
      'Назначение': ", ".join(list(np.random.choice(options['Назначение'], random.randint(0,len(options['Назначение'])-1)))),
      'Минимальная партия': list(np.random.choice(options['Минимальная партия'], 1))[0],
      'Минимальный заказ': list(np.random.choice(options['Минимальный заказ'], 1))[0],
      'Другие виды изделий': ", ".join(list(np.random.choice(options['Другие виды изделий'], random.randint(0,len(options['Другие виды изделий'])-1)))),
      'Пол и возраст': ", ".join(list(np.random.choice(options['Пол и возраст'], random.randint(0,len(options['Пол и возраст'])-1)))),
      'Дополнительные услуги': ", ".join(list(np.random.choice(options['Дополнительные услуги'], random.randint(0,len(options['Дополнительные услуги'])-1)))),
      'Ценовой сегмент': list(np.random.choice(options['Ценовой сегмент'], 1))[0],
      'Ценовые сегменты': list(np.random.choice(options['Ценовые сегменты'], 1))[0],
      'По сезону': ", ".join(list(np.random.choice(options['По сезону'], random.randint(0,len(options['По сезону'])-1)))),

      'Регион производства': list(np.random.choice(options['Регионы'], 1))[0],
      'Регионы поставок': ", ".join(list(np.random.choice(options['Регионы'], random.randint(0,len(options['Регионы'])-1)))),

      'Загруженность': list(np.random.choice(options['Загруженность'], 1))[0],
      'Требования к заказчику': ", ".join(list(np.random.choice(options['Требования к заказчику'], random.randint(0,len(options['Требования к заказчику'])-1)))),
      'Конструирование': ", ".join(list(np.random.choice(options['Конструирование'], random.randint(0,len(options['Конструирование'])-1)))),
      'Техническая документация': ", ".join(list(np.random.choice(options['Техническая документация'], random.randint(0,len(options['Техническая документация'])-1)))),
      'Технология': ", ".join(list(np.random.choice(options['Технология'], random.randint(0,len(options['Технология'])-1)))),
      'Условия оплаты': ", ".join(list(np.random.choice(options['Условия оплаты'], random.randint(0,12)))),
      'Образцы': list(np.random.choice(options['Образцы'], 1))[0],
      'Дополнительная информация': list(np.random.choice([None, fake.paragraph(nb_sentences=5)], 1, p=[0.4, 0.6]))[0],
    })
  
  return data

# orders random data generation
def orders_gen(options, qty):
  fake = Faker('ru_RU')
  data = []

  for i in range(qty):
    title = list(np.random.choice(options['Вид изделия'], 1))[0]
    data.append({
      'Изображение': list(np.random.choice([None, fake.image_url()], 1, p=[0.3, 0.7]))[0],
      'Вид изделия': title,
      'Название': title,
      'Тип одежды': list(np.random.choice(options['Тип одежды'], 1))[0],
      'Назначение': ", ".join(list(np.random.choice(options['Назначение'], random.randint(0,len(options['Назначение'])-1)))),
      'Пол и возраст': ", ".join(list(np.random.choice(options['Пол и возраст'], random.randint(0,len(options['Пол и возраст'])-1)))),
      'Регион поставки': ", ".join(list(np.random.choice(options['Регионы'], random.randint(0,len(options['Регионы'])-1)))),
      'Регионы производства': ", ".join(list(np.random.choice(options['Регионы'], random.randint(0,len(options['Регионы'])-1)))),
      'Виды нанесения': ", ".join(list(np.random.choice(options['Виды нанесения'], random.randint(0,len(options['Виды нанесения'])-1)))),
      'Дизайн и моделирование': ", ".join(list(np.random.choice(options['Дизайн и моделирование'], random.randint(0,len(options['Дизайн и моделирование'])-1)))),
      'Дополнительные услуги': ", ".join(list(np.random.choice(options['Дополнительные услуги'], random.randint(0,len(options['Дополнительные услуги'])-1)))),
      'Требования к заказчику': ", ".join(list(np.random.choice(options['Требования к заказчику'], random.randint(0,len(options['Требования к заказчику'])-1)))),
      'Количество изделий': list(np.random.choice(options['Минимальная партия'], 1))[0],
      'Комментарий к заказу': list(np.random.choice([None, fake.paragraph(nb_sentences=5)], 1, p=[0.4, 0.6]))[0],
      'Конструирование': ", ".join(list(np.random.choice(options['Конструирование'], random.randint(0,len(options['Конструирование'])-1)))),
      'Нанесение принта': ", ".join(list(np.random.choice(options['Нанесение принта'], random.randint(0,len(options['Нанесение принта'])-1)))),
      'Обеспечение сырьем': ", ".join(list(np.random.choice(options['Обеспечение сырьем'], random.randint(0,len(options['Обеспечение сырьем'])-1)))),
      'Ткани и фурнитура': ", ".join(list(np.random.choice(options['Ткани и фурнитура'], random.randint(0,len(options['Ткани и фурнитура'])-1)))),
      'Плановый бюджет': list(np.random.choice(options['Минимальный заказ'], 1))[0],
      'Плотность материала': ", ".join(list(np.random.choice(options['Плотность материала'], random.randint(0,len(options['Плотность материала'])-1)))),
      'Сертификация': ", ".join(list(np.random.choice(options['Сертификация'], random.randint(0,len(options['Сертификация'])-1)))),
      'Срок поставки': fake.date_time_between_dates(datetime_start=datetime.datetime(2022,1,1,0,0,0), datetime_end=datetime.datetime(2024,4,25,23,59,59)),
      'Техническая документация': list(np.random.choice(options['Техническая документация'], 1))[0],
      'Технология': ", ".join(list(np.random.choice(options['Технология'], random.randint(0,len(options['Технология'])-1)))),
      'Требования': ", ".join(list(np.random.choice(options['Требования'], random.randint(0,len(options['Требования'])-1)))),
      'Упаковка': list(np.random.choice(options['Упаковка'], 1))[0],
      'Условия оплаты': list(np.random.choice(options['Условия оплаты'], 1))[0],
      'Цена за единицу': random.randint(0,10000),
      'Ценовой сегмент': list(np.random.choice(options['Ценовой сегмент'], 1))[0],
      'Дата': fake.date_time_between_dates(datetime_start=datetime.datetime(2022,1,1,0,0,0), datetime_end=datetime.datetime(2024,4,25,23,59,59)),
    })
  
  return data

# factories - random data generation for a single value
def factories_single_value(column, options):
  fake = Faker('ru_RU')

  if column == 'Проверен': return list(np.random.choice(['нет','да'], 1, p=[0.25, 0.75]))[0]
  elif column == 'ИНН': return list(np.random.choice([None, random.randrange(10**(11), 10**12)], 1, p=[0.2, 0.8]))[0]
  elif column == 'Минпромторг': return list(np.random.choice(['нет','да'], 1, p=[0.3, 0.7]))[0]
  elif column == 'Телефон': return list(np.random.choice([None, random.randrange(10**(10), 10**11)], 1, p=[0.2,0.8]))[0]
  elif column == 'Email': return list(np.random.choice([None, fake.ascii_company_email()], 1, p=[0.3,0.7]))[0]
  elif column == 'Название': return list(np.random.choice([None, fake.company()], 1, p=[0.2, 0.8]))[0]
  elif column == 'Имя': return list(np.random.choice([None, fake.first_name() + ' ' + fake.last_name()], 1, p=[0.7,0.3]))[0]
  elif column == 'Логотип': return list(np.random.choice([None, fake.image_url()], 1, p=[0.3, 0.7]))[0]
  elif column == 'Роли': return list(np.random.choice(['Магазин продавца', 'Магазин продавца, Клиент'], 1, p=[0.7, 0.3]))[0]
  elif column == 'Регистрация': return fake.date_time_between_dates(datetime_start=datetime.datetime(2022,1,1,0,0,0), datetime_end=datetime.datetime(2024,4,25,23,59,59))

  elif column == 'Тип одежды': return ", ".join(list(np.random.choice(options['Тип одежды'], random.randint(0,len(options['Тип одежды'])-1))))
  elif column == 'Назначение': return ", ".join(list(np.random.choice(options['Назначение'], random.randint(0,len(options['Назначение'])-1))))
  elif column == 'Минимальная партия': return list(np.random.choice(options['Минимальная партия'], 1))[0]
  elif column == 'Минимальный заказ': return list(np.random.choice(options['Минимальный заказ'], 1))[0]
  elif column == 'Другие виды изделий': return ", ".join(list(np.random.choice(options['Другие виды изделий'], random.randint(0,len(options['Другие виды изделий'])-1))))
  elif column == 'Пол и возраст': return ", ".join(list(np.random.choice(options['Пол и возраст'], random.randint(0,len(options['Пол и возраст'])-1))))
  elif column == 'Дополнительные услуги': return ", ".join(list(np.random.choice(options['Дополнительные услуги'], random.randint(0,len(options['Дополнительные услуги'])-1))))
  elif column == 'Ценовой сегмент': return list(np.random.choice(options['Ценовой сегмент'], 1))[0]
  elif column == 'Ценовые сегменты': return list(np.random.choice(options['Ценовые сегменты'], 1))[0]
  elif column == 'По сезону': return ", ".join(list(np.random.choice(options['По сезону'], random.randint(0,len(options['По сезону'])-1))))

  elif column == 'Регион производства': return list(np.random.choice(options['Регионы'], 1))[0]
  elif column == 'Регионы поставок': return ", ".join(list(np.random.choice(options['Регионы'], random.randint(0,len(options['Регионы'])-1))))

  elif column == 'Загруженность': return list(np.random.choice(options['Загруженность'], 1))[0]
  elif column == 'Требования к заказчику': return ", ".join(list(np.random.choice(options['Требования к заказчику'], random.randint(0,len(options['Требования к заказчику'])-1))))
  elif column == 'Конструирование': return ", ".join(list(np.random.choice(options['Конструирование'], random.randint(0,len(options['Конструирование'])-1))))
  elif column == 'Техническая документация': return ", ".join(list(np.random.choice(options['Техническая документация'], random.randint(0,len(options['Техническая документация'])-1))))
  elif column == 'Технология': return ", ".join(list(np.random.choice(options['Технология'], random.randint(0,len(options['Технология'])-1))))
  elif column == 'Условия оплаты': return ", ".join(list(np.random.choice(options['Условия оплаты'], random.randint(0,12))))
  elif column == 'Образцы': return list(np.random.choice(options['Образцы'], 1))[0]
  elif column == 'Дополнительная информация': return list(np.random.choice([None, fake.paragraph(nb_sentences=5)], 1, p=[0.4, 0.6]))[0]

# orders - random data generation for a single value
def orders_single_value(column, options):
  fake = Faker('ru_RU')

  if column == 'Изображение': return list(np.random.choice([None, fake.image_url()], 1, p=[0.3, 0.7]))[0]
  elif column == 'Вид изделия': return list(np.random.choice(options['Вид изделия'], 1))[0]
  elif column == 'Название': return list(np.random.choice(options['Вид изделия'], 1))[0]
  elif column == 'Тип одежды': return list(np.random.choice(options['Тип одежды'], 1))[0]
  elif column == 'Назначение': return ", ".join(list(np.random.choice(options['Назначение'], random.randint(0,len(options['Назначение'])-1))))
  elif column == 'Пол и возраст': return ", ".join(list(np.random.choice(options['Пол и возраст'], random.randint(0,len(options['Пол и возраст'])-1))))
  elif column == 'Регион поставки': return ", ".join(list(np.random.choice(options['Регионы'], random.randint(0,len(options['Регионы'])-1))))
  elif column == 'Регионы производства': return ", ".join(list(np.random.choice(options['Регионы'], random.randint(0,len(options['Регионы'])-1))))
  elif column == 'Виды нанесения': return ", ".join(list(np.random.choice(options['Виды нанесения'], random.randint(0,len(options['Виды нанесения'])-1))))
  elif column == 'Дизайн и моделирование': return ", ".join(list(np.random.choice(options['Дизайн и моделирование'], random.randint(0,len(options['Дизайн и моделирование'])-1))))
  elif column == 'Дополнительные услуги': return ", ".join(list(np.random.choice(options['Дополнительные услуги'], random.randint(0,len(options['Дополнительные услуги'])-1))))
  elif column == 'Требования к заказчику': return ", ".join(list(np.random.choice(options['Требования к заказчику'], random.randint(0,len(options['Требования к заказчику'])-1))))
  elif column == 'Количество изделий': return list(np.random.choice(options['Минимальная партия'], 1))[0]
  elif column == 'Комментарий к заказу': return list(np.random.choice([None, fake.paragraph(nb_sentences=5)], 1, p=[0.4, 0.6]))[0]
  elif column == 'Конструирование': return ", ".join(list(np.random.choice(options['Конструирование'], random.randint(0,len(options['Конструирование'])-1))))
  elif column == 'Нанесение принта': return ", ".join(list(np.random.choice(options['Нанесение принта'], random.randint(0,len(options['Нанесение принта'])-1))))
  elif column == 'Обеспечение сырьем': return ", ".join(list(np.random.choice(options['Обеспечение сырьем'], random.randint(0,len(options['Обеспечение сырьем'])-1))))
  elif column == 'Ткани и фурнитура': return ", ".join(list(np.random.choice(options['Ткани и фурнитура'], random.randint(0,len(options['Ткани и фурнитура'])-1))))
  elif column == 'Плановый бюджет': return list(np.random.choice(options['Минимальный заказ'], 1))[0]
  elif column == 'Плотность материала': return ", ".join(list(np.random.choice(options['Плотность материала'], random.randint(0,len(options['Плотность материала'])-1))))
  elif column == 'Сертификация': return ", ".join(list(np.random.choice(options['Сертификация'], random.randint(0,len(options['Сертификация'])-1))))
  elif column == 'Срок поставки': return fake.date_time_between_dates(datetime_start=datetime.datetime(2022,1,1,0,0,0), datetime_end=datetime.datetime(2024,4,25,23,59,59))
  elif column == 'Техническая документация': return list(np.random.choice(options['Техническая документация'], 1))[0]
  elif column == 'Технология': return ", ".join(list(np.random.choice(options['Технология'], random.randint(0,len(options['Технология'])-1))))
  elif column == 'Требования': return ", ".join(list(np.random.choice(options['Требования'], random.randint(0,len(options['Требования'])-1))))
  elif column == 'Упаковка': return list(np.random.choice(options['Упаковка'], 1))[0]
  elif column == 'Условия оплаты': return list(np.random.choice(options['Условия оплаты'], 1))[0]
  elif column == 'Цена за единицу': return random.randint(0,10000)
  elif column == 'Ценовой сегмент': return list(np.random.choice(options['Ценовой сегмент'], 1))[0]
  elif column == 'Дата': return fake.date_time_between_dates(datetime_start=datetime.datetime(2022,1,1,0,0,0), datetime_end=datetime.datetime(2024,4,25,23,59,59))
