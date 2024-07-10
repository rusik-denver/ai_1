# Import libraries
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk
from nltk.corpus import stopwords
from keras.models import load_model

# load stopwords for Russian
nltk.download('stopwords')
nltk.download('punkt')
stop_words = list(stopwords.words('russian'))

#@title Datasets and variables
manufactures_url = {
    'refactored':'https://drive.google.com/file/d/1Ikfs67ftCVtVdAdoT7aQb9IyAY8XI1Rt/view',
    'original': 'https://drive.google.com/file/d/1iNt2nIDAf4v_Y4dtPDcfGnzETuSkCl7K/view'
}
orders_url = {
    'refactored':'https://drive.google.com/file/d/1XQJBUUvTJxyQrpwXY5FAYzJur4O0Ftrd/view',
    'original': 'https://drive.google.com/file/d/1Ob5wslkMzX1V71gv4JDQ-bqJOKgjRBJL/view'
}
options_url = 'https://drive.google.com/file/d/1FyxQNqTeYD8LZBTbJ4lTl14PuF5yAR9U/view'

drive_path = '/content/drive/My Drive/УИИ/стажировки/ai_1/practice/'

#@title Functions
#function for getting rid off redundant columns
def clean_db(db_lst, original):
  if isinstance(db_lst, list):
    if original:
      db_1 = db_lst[0].drop(columns=['Проверен','ИНН','Наличии в реестре Минпромторга','Телефон','Email','Название','Имя контактного лица','Логотип','Роли','Регистрация','Регион производства.1'], axis=1)
    else:
      db_1 = db_lst[0].drop(columns=['Проверен','ИНН','Минпромторг','Телефон','Email','Название','Имя','Логотип','Роли','Регистрация'], axis=1)

    db_2 = db_lst[1].drop(columns=['Изображение','Дата','Срок поставки'])

    return db_1, db_2
  else:
    return db_lst.drop(columns=['Изображение','Дата','Срок поставки'])

def combine_columns(db):
  db['combined'] = db.apply(lambda x: ' '.join(x.dropna().astype(str)), axis=1)
  #drop rows with all NaNs
  db.drop(db.loc[db['combined'] == 'Нет'].index, inplace=True)
  return db

def recommended_manufacturers(order_request, n=25, original=False, db_type='original'):
  manufacturers_db = pd.read_csv('https://drive.google.com/uc?id=' + manufactures_url[db_type].split('/')[-2])
  orders_db = pd.read_csv('https://drive.google.com/uc?id=' + orders_url[db_type].split('/')[-2])
  db_lst = [manufacturers_db,orders_db]
  dbs = []

  db_lst = clean_db(db_lst, original)

  for i,db in enumerate(db_lst):
    cur_db = combine_columns(db)
    dbs.append(cur_db)

  if isinstance(order_request, int):
    order = dbs[1].iloc[order_request,:].dropna().astype(str).to_list()
    order_combined = ' '.join(order)
  elif isinstance(order_request, list):
    order_combined = ' '.join(order_request)
  elif isinstance(order_request, str):
    _ord = order_request.split(',')
    _ord_lst = [''] * 26
    for i in range(len(_ord)):
      _ord_lst[i] = _ord[i]
    order_combined = _ord_lst
  else:
    print('Order request has wrong format. It might be either Order ID, list of features, or a string')
    return IOError
  
  model = './db/model_learned_by_auto_keras_with_all_tfidf_data_3_posttrained.keras'
  model = load_model(model)

  vectorizer = TfidfVectorizer(analyzer = 'word',stop_words=stop_words) # Initialize the TF-IDF vectorizer
  tfidf_matrix = vectorizer.fit_transform(dbs[0]['combined'])# Fit and transform the manufacturers' data
  order_tfidf = vectorizer.transform(order_combined) # Transform the order request text
  cosine_similarities = cosine_similarity(order_tfidf, tfidf_matrix).flatten() # Calculate cosine similarity between the order request and all manufacturers
  dbs[0]['similarity'] = cosine_similarities # Add the similarity scores to the manufacturers DataFrame
  recommended = dbs[0].sort_values(by='similarity', ascending=False) # Sort manufacturers by similarity scores in descending order
  
  #move similarity column to the first position
  first_column = recommended.pop('similarity')
  recommended.insert(0, 'similarity', first_column)
  
  predictions = model.predict(order_tfidf)

  return recommended.head(int(n)), manufacturers_db, predictions # Select top N manufacturers (e.g., top n)

order_request = 'Верхняя одежда, Торжественная одежда, Женская одежда, Всесезон / помещения'
num = 10
top_n_manufacturers, db, predictions = recommended_manufacturers(order_request, num, True, 'original')

print("Top recommended manufacturers for the order:")
print(top_n_manufacturers[['similarity']])
print(predictions)

# highlighted_text = []

# for key, val in clean_db(orders_db).iloc[order_id,:].dropna().items():
#   if isinstance(val, str) and len(val):
#     highlighted_text.extend(val.lower().split(', '))

# for i in range(top_n_manufacturers.shape[0]):
#   result = manufacturers_db.iloc[top_n_manufacturers.index[i],:].dropna()
#   print(f'#{i+1}\n')

#   for key, val in result.items():
#     text = []

#     if isinstance(val, str) and len(val):
#       for x in val.split(', '):
#         if x.lower() in highlighted_text:
#           text.append(f'\x1b[31m{x}\x1b[0m')
#         else:
#           text.append(f'{x}')

#     text = ", ".join(text)
#     print(f'{key}: {text}')
#   print()
#   print('*'*100)
#   print()









# # model.summary()

# # Initialize the TF-IDF vectorizer
# vectorizer = TfidfVectorizer(analyzer = 'word',stop_words=stop_words)

# query = 'Верхняя одежда Торжественная одежда Женская одежда Всесезон / помещения'

# # Transform the order request text
# order_tfidf = vectorizer.transform([query])

# predictions = model.predict(query)
# # Получаем номер цифры с наибольшей вероятностью
# digit = np.argmax(predictions)
# print(predictions, digit)