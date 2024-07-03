from pathlib import Path
import pandas as pd
import numpy as np
import random
from tensorflow.keras.preprocessing.text import Tokenizer
from funcs import read_dataset
from funcs_embedding import *

# load stopwords for Russian
nltk.download('stopwords')
nltk.download('punkt')

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
#search cluster columns have their pairs or more in both datasets
#in tuples, first is orders' columns, next - factories'
#ignore set is for both columns
CLUSTERS = {
    'sfilter': [('Тип одежды',['Тип одежды','Другие виды изделий']),('Назначение','Назначение'),
                ('Количество изделий','Минимальная партия'),('Плановый бюджет','Минимальный заказ'),
                ('Пол и возраст','Пол и возраст'),('Дополнительные услуги','Дополнительные услуги'),
                 ('Цена за единицу','Ценовой сегмент'),('Ценовой сегмент','Ценовые сегменты')],
    'location': [('Регион поставки','Регионы поставок'), ('Регионы производства','Регион производства')],
    'info': [('Техническая документация','Техническая документация'),('Технология','Технология'),
            (['Требования','Требования к заказчику'],'Требования к заказчику'),
             ('Условия оплаты','Условия оплаты'),('Конструирование','Конструирование')],
    'merged': [(['Вид изделия', 'Название','Плотность материала','Сертификация','Упаковка','Комментарий к заказу','Нанесение принта','Обеспечение сырьем','Ткани и фурнитура','Виды нанесения','Дизайн и моделирование'],['Загруженность','Образцы','Дополнительная информация','По сезону'])],
    'profile': ['Проверен','ИНН','Минпромторг','Телефон','Email','Название','Имя','Логотип','Роли','Регистрация'],
    'ignore': ['Изображение','Дата','Срок поставки'],
}

#merge all search columns
SEARCH_CLUSTERS = [*CLUSTERS['sfilter'], *CLUSTERS['location'], *CLUSTERS['info'], *CLUSTERS['merged']]

MAX_VOCAB_SIZE = 500
# mask = np.array([0.25, 0.25, 0.05, 0.05, 0.15, 0.05, 0.02, 0.05, 0.02, 0.01, 0.01, 0.01, 0.02, 0.02, 0.02, 0.02]) #mask for marking columns importance
mask = np.array([0.3, 0.2, 0.047, 0.048, 0.174, 0.049, 0.015, 0.05, 0.016, 0.008, 0.009, 0.01, 0.017, 0.018, 0.019, 0.02]) #mask for marking columns importance

# vars for aggregate Series
data_f = []
data_o = []

# merge columns if needed to create datasets for using in model training
for cluster in SEARCH_CLUSTERS:
  data_f.append(pd.concat([merge_columns(DB['factories'], cluster[1])], axis=1))
  data_o.append(pd.concat([merge_columns(DB['orders'], cluster[0])], axis=1))

DATA_F = pd.concat(data_f, axis=1)
DATA_O = pd.concat(data_o, axis=1)

# data cleaning
for cluster in SEARCH_CLUSTERS:
  if isinstance(cluster[1], list):
    if len(cluster[1]) <= 3: #if merged less than 4
      column = '_'.join(cluster[1]) # get merged column title
      DATA_F[column] = DATA_F[column].apply(
          lambda x: ', '.join(
              map(
                  str.strip,
                  x.split(',')
                  )
              )
          )

  if isinstance(cluster[0], list):
    if len(cluster[0]) <= 3: #if merged less than 4
      column = '_'.join(cluster[0]) # get merged column title
      DATA_O[column] = DATA_O[column].apply(
          lambda x: ', '.join(
              map(
                  str.strip,
                  x.split(',')
                  )
              )
          )

DATA_F.iloc[:,-1] = DATA_F.iloc[:,-1].apply(
  lambda x: ', '.join(
    filter(
      None,
      map(
        str.strip,
        x.split(',')
        )
      )
    )
  )
DATA_O.iloc[:,-1] = DATA_O.iloc[:,-1].apply(
  lambda x: ', '.join(
    filter(
      None,
      map(
        str.strip,
        x.split(',')
        )
      )
    )
  )

#preprocess the last merged columns
#texts from the last columns of the both datasets
merged_text_f = DATA_F.iloc[:,-1].to_list()
merged_text_o = DATA_O.iloc[:,-1].to_list()

#concatenate last columns from bothe datasets
merged_texts = np.concatenate(
    [
        merged_text_f,
        merged_text_o
    ]
)

#preprocess text
merged_texts = short_words_text_filter(merged_texts, 2)
merged_texts = texts_predrocess(merged_texts)

#tokenize vocabulary
tokenizer = Tokenizer(num_words=MAX_VOCAB_SIZE, filters='!"#$%&()*+,-–—./…:;<=>?@[\\]^_`{|}~«»\t\n\xa0\ufeff', lower=True, split=' ', oov_token='unknown', char_level=False)
tokenizer.fit_on_texts(merged_texts)

merged_items = list(tokenizer.word_index.items())

merged_seq_f = tokenizer.texts_to_sequences(merged_text_f)
merged_bow_f = tokenizer.sequences_to_matrix(merged_seq_f)

merged_seq_o = tokenizer.texts_to_sequences(merged_text_o)
merged_bow_o = tokenizer.sequences_to_matrix(merged_seq_o)

#preprocess the rest of the columns
ohe_f = []
ohe_o = []

for i in range(len(SEARCH_CLUSTERS)):
  column_f = DATA_F.columns[i]
  column_o = DATA_O.columns[i]

  rows_f = DATA_F[column_f].to_list()
  rows_o = DATA_O[column_o].to_list()

  bow_f = []
  bow_o = []

  if column_o in OPTIONS.keys():
    options = OPTIONS[column_o]

    # ohe encode options in both datasets
    for row in rows_o:
      bow_o.append(str_to_ohe(row, options))

    for row in rows_f:
      bow_f.append(str_to_ohe(row, options))

  else:
    #filter and merge data in columns
    all_columns = np.concatenate([rows_f, rows_o])
    all_columns = short_words_text_filter(all_columns, 2)
    all_columns = texts_predrocess(all_columns)

    # tokenize vocabulary
    tokenizer = Tokenizer(num_words=MAX_VOCAB_SIZE, filters='!"#$%&()*+,-–—./…:;<=>?@[\\]^_`{|}~«»\t\n\xa0\ufeff', lower=True, split=' ', oov_token='unknown', char_level=False)
    tokenizer.fit_on_texts(all_columns)

    columns_items = list(tokenizer.word_index.items())

    seq_o = tokenizer.texts_to_sequences(rows_o)
    bow_o = tokenizer.sequences_to_matrix(seq_o)

    seq_f = tokenizer.texts_to_sequences(rows_f)
    bow_f = tokenizer.sequences_to_matrix(seq_f)

  ohe_o.append(bow_o)
  ohe_f.append(bow_f)

# test to get a distance for an order (id) 162
min_dist_arg, min_dist = closest_factory([ohe_f, ohe_o], SEARCH_CLUSTERS, len(bow_f), 162, mask)
print('Min distance: ',min_dist)

#sort factories
sorted_f = sort_factories([ohe_f, ohe_o], SEARCH_CLUSTERS, len(bow_f), 166, mask)
print(sorted_f)

print(DATA_O.iloc[166])

result_db = []
counter = 0
for factory, vector in sorted_f:
  if counter < 25 and vector < 0.17: #best results
    result_db.append(DB['factories'].iloc[factory])

  if counter < 10 and vector > 0.17 and vector < 0.3:
    result_db.append(DB['factories'].iloc[factory]) #not good results

  counter += 1

result = pd.concat(result_db, axis=1)
result = pd.DataFrame(result.T)
print(result.shape)

print(result)