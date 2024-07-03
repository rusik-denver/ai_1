from pathlib import Path
import pandas as pd
import numpy as np
import math
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

#function for merging columns
def merge_columns(db, columns):
  result = []

  if isinstance(columns, list):
    for column in columns:
      result.append(db[column].astype(str).replace('nan',''))

    result = pd.concat(result, axis=1).apply(lambda x: ', '.join(x) if not x.all() == '' else x, axis=1)

    if len(columns) > 3:
      result.name = 'Merged Columns'
    else:
      result.name = '_'.join(columns)

  else:
    result = db[columns].astype(str).replace('nan','')

  return result

# function for text preprocessing
def texts_predrocess(text_lst):

  def text_preprocess(text):
    stop_words = set(stopwords.words('russian'))

    text = text.lower()
    words = word_tokenize(text, language='russian')
    filtered_words = [word for word in words if word not in stop_words and word.isalpha()] #filter text

    return ' '.join(filtered_words)

  return [text_preprocess(text) for text in text_lst]

# function for filtering short words
def short_words_text_filter(text_lst, min_length = 2):

  def short_words_filter(text, min_length = 2):
    words = re.findall(r'\b\w+\b', text)
    filtered_text = ' '.join([word for word in words if len(word) > min_length]) #filter out short words

    return filtered_text

  return [short_words_filter(text, min_length) for text in text_lst]

# function for OneHotEncode
def str_to_ohe(arg, class_dict):
    classes_qty = len(class_dict )
    result = np.zeros(classes_qty)

    if arg:
        # put 1 on the index of the arg
        for i,value in enumerate(class_dict):
            if value in arg:
                result[i] = 1.

    return result

#function for getting distance between BoW
def dist_between_BoW(a, b):
  a = np.array(a)
  b = np.array(b)
  dim = sum(a)

  if dim == 0:
    return 0

  return math.dist(a, b * a) / np.sqrt(dim)

#function for getting distance between order and factories
def dist_between_order_and_factory(ohe, clusters, order_id, factory_id, mask = 1):
  manuf_region = 10
  ohe_f, ohe_o = ohe

  dist = [dist_between_BoW(ohe_o[column][order_id], ohe_f[column][factory_id]) for column in np.arange(len(clusters))]

  if sum(np.multiply(ohe_o[manuf_region][order_id], ohe_f[manuf_region][factory_id])) > 0:
    dist[manuf_region] = 0
  else:
    dist[manuf_region] = 1

  zero_point = [0 for _ in np.arange(len(clusters))]

  return math.dist(dist * mask, zero_point)

#function to find a closest factory for an order
def closest_factory(ohe, clusters, max_len, idx, mask):
  min_dist = np.float64('inf')
  min_dist_arg = 0

  for i in np.arange(max_len):
    cur_dist = dist_between_order_and_factory(ohe, clusters, idx, i, mask)

    if min_dist > cur_dist:
      min_dist = cur_dist
      min_dist_arg = i

  return min_dist_arg, min_dist

#function for sorting factories
def sort_factories(ohe, clusters, max_len, idx, mask):
  factories = []

  for i in np.arange(max_len):
    now_dist = dist_between_order_and_factory(ohe, clusters, idx, i, mask)
    factories.append([i, now_dist])

  return sorted(factories, key  = lambda k: k[1])