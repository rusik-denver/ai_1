# Import libraries
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk
from nltk.corpus import stopwords

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
def clean_db(db_lst, original=False):
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

def recommended_manufacturers(db_lst, order_request, n=25, original=False):
  dbs = []
  db_lst = clean_db(db_lst, original)

  for i,db in enumerate(db_lst):
    title = ''

    if i == 0:
      title = 'Manufacturers'
    else:
      title = 'Orders'

    print(f'{title}\' dataframe shape:', db.shape)

    cur_db = combine_columns(db)
    dbs.append(cur_db)

    print(f'{title}\' dataframe shape after cleaning:', cur_db.shape)

  if isinstance(order_request, int):
    order = dbs[1].iloc[order_request,:].dropna().astype(str).to_list()
    order_combined = ' '.join(order)
  elif isinstance(order_request, list):
    order_combined = ' '.join(order_request)
  elif isinstance(order_request, str):
    order_combined = order_request
  else:
    print('Order request has wrong format. It might be either Order ID, list of features, or a string')
    # return IOError

  # Initialize the TF-IDF vectorizer
  vectorizer = TfidfVectorizer(analyzer = 'word',stop_words=stop_words)

  # # Fit and transform the manufacturers' data
  tfidf_matrix = vectorizer.fit_transform(dbs[0]['combined'])

  # # Transform the order request text
  order_tfidf = vectorizer.transform([order_combined])

  # # Calculate cosine similarity between the order request and all manufacturers
  cosine_similarities = cosine_similarity(order_tfidf, tfidf_matrix).flatten()

  # # Add the similarity scores to the manufacturers DataFrame
  dbs[0]['similarity'] = cosine_similarities

  # # Sort manufacturers by similarity scores in descending order
  recommended = dbs[0].sort_values(by='similarity', ascending=False)

  # # Select top N manufacturers (e.g., top n)
  return recommended.head(n)

# Dataset
#factories dataset
manufacturers_db = pd.read_csv('https://drive.google.com/uc?id=' + manufactures_url['original'].split('/')[-2])
#orders dataset
orders_db = pd.read_csv('https://drive.google.com/uc?id=' + orders_url['original'].split('/')[-2])

order_id = 162
num = 10
top_n_manufacturers = recommended_manufacturers([manufacturers_db, orders_db], order_id, num, True)

#move similarity column to the first position
first_column = top_n_manufacturers.pop('similarity')
top_n_manufacturers.insert(0, 'similarity', first_column)

print("Top recommended manufacturers for the order:")
print(top_n_manufacturers[['similarity']])

highlighted_text = []

for key, val in clean_db(orders_db).iloc[order_id,:].dropna().items():
  if isinstance(val, str) and len(val):
    highlighted_text.extend(val.lower().split(', '))

for i in range(top_n_manufacturers.shape[0]):
  result = manufacturers_db.iloc[top_n_manufacturers.index[i],:].dropna()
  print(f'#{i+1}\n')

  for key, val in result.items():
    text = []

    if isinstance(val, str) and len(val):
      for x in val.split(', '):
        if x.lower() in highlighted_text:
          text.append(f'\x1b[31m{x}\x1b[0m')
        else:
          text.append(f'{x}')

    text = ", ".join(text)
    print(f'{key}: {text}')
  print()
  print('*'*100)
  print()