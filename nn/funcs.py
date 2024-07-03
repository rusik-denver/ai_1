from pathlib import Path
import pandas as pd
import numpy as np

# function for reading datasets
def read_dataset(path, file_name):
    ext = Path(path / file_name).suffix

    if ext[1:] == 'xlsx':
        return pd.read_excel(path / file_name, sheet_name=None, index_col=0)
    
    return pd.read_csv(path / file_name)

# function for procession options from a column
def options_processing(db, options):

    # function for extracting unique values/options from a row
    def get_options(raw_lst):
        new_lst = []

        for lst in raw_lst:
            if 'str' in str(type(lst)):
                _lst = lst.split(',')

                for l in _lst:
                    if not pd.isna(l) and l: new_lst.append(l.lower().strip().split('|')[0])
            else:
                if not pd.isna(lst) and lst: new_lst.append(lst)

        return sorted(list(set(new_lst)))
    
    unique_options = {}

    # extract unique values from columns
    if 'pandas' in str(type(db)):
        for column in db:
            unique_options.update({column:get_options(db[column].unique())})
    # extract unique values from xls-file
    elif 'dict' in str(type(db)):
        for spr in db.items():
            unique_options.update({spr[0]:list(options[spr[1]]['name'].str.lower())})

    return unique_options

# function for merging options from datasets and options from xlsx-file
def merge_options(labels, options, lst, verbose=0):

    def print_output(option, options_lst, verbose):
        print(f'\nAmount of merged unique options in {option}:', len(options_lst))
        
        if verbose:
            print(*options_lst, sep='\n')
        
        print(('*'*100 + '\n')*2)

    for option in labels:
        _option_lst = []

        if option == 'Дополнительная информация':
            continue
        elif option == 'Минимальная партия':
            cur_val = ['1-99', '100-249', '250-499', '500-999', '1000-4999', '5000-9999', '10000+']
            _option_lst.extend(cur_val)
        elif option == 'Минимальный заказ':
            cur_val = ['1-9999', '10000-49999', '50000-99999', '100000-249999', '250000-499999', '500000-999999', '1000000-4999999', '5000000+']
            _option_lst.extend(cur_val)
        elif (option == 'Регионы поставок') or (option == 'Регион производства') or (option == 'Регионы производства') or (option == 'Регион поставки'):
            _option_lst.extend(lst['extra_options']['Регион производства'])
            
            #sort, get rid off all duplicates and check if not null
            if _option_lst:
                _option_lst = sorted(list(set(_option_lst)))
                _option_lst = [_option.title() for _option in _option_lst]
            
            options.update({'Регионы': _option_lst}) # for all regions columns we create only one with broad title Регионы
            print('***All regional options merged to one single option Регионы***')
            print_output(option, _option_lst, verbose)
            continue
        else:
            if option in lst['factories'].keys():
                _option_lst.extend(lst['factories'][option])

            if option in lst['orders'].keys():
                _option_lst.extend(lst['orders'][option])

            if option in lst['extra_options'].keys():
                _option_lst.extend(lst['extra_options'][option])

        #sort, get rid off all duplicates and check if not null
        if _option_lst:
            _option_lst = sorted(list(set(_option_lst)))
            _option_lst = [_option.capitalize() for _option in _option_lst]
            options.update({option: _option_lst})

        print_output(option, _option_lst, verbose)
        
    return options

# get search filter on refactored dataset with nans
# ****function filter looks like poor solution****
def sfilter(row, search_db, clusters):

    def search_options(row, clusters):
        options = {}
        for _,opts in clusters.items():
            for option in opts:
                if 'list' in str(type(option[0])):
                    for opt in option[0]:
                        if opt in row.keys():
                            options.update({opt:row[opt]})
                elif 'list' in str(type(option[1])):
                    if option[0] in row.keys():
                        for opt in option[1]:
                            if opt in row.keys():
                                options.update({opt:row[opt]})
                else:
                    if option[0] in row.keys():
                        options.update({option[1]:row[option[0]]})
        return options

    results = []
    filters = search_options(row, clusters)
    
    for key,option in filters.items():
        if key in search_db.keys():
            result = search_db[search_db[key] == option]
            if result.shape[0] > 0:
                results.append(result)

    # add filter for best results********************

    return results

# function for OneHotEncode
# def str_to_ohe(arg, class_dict):
#     classes_qty = class_dict[0] 
#     result = np.zeros(classes_qty)

#     if arg:
#         # put 1 on the index of the arg
#         for value,cls in class_dict[1].items():
#             if value in arg:
#                 result[cls] = 1.

#     return result

# function for extracting data from categorized clusters
# def extract_row_data(row, categories):
#     stack = {}
#     print(row)
#     for category in categories.keys():
#         if category in row.keys():
#             stack.update({category: str_to_ohe(str(row[category]), categories[category])})
#         else:
#             stack.update({category: str_to_ohe(None, categories[category])})

#     print(stack)
    # sex, age = extract_sex_age_years(row[COL_SEX_AGE])      # Пол, возраст
    # sex_vec = np.array([sex])                               # Пол в виде вектора
    # age_ohe = age_years_to_ohe(age)                         # Возраст в one hot encoding
    # city_ohe = extract_city_to_ohe(row[COL_CITY])           # Город
    # empl_multi = extract_employment_to_multi(row[COL_EMPL]) # Тип занятости
    # sсhed_multi = extract_schedule_to_multi(row[COL_SCHED]) # График работы
    # edu_multi = extract_education_to_multi(row[COL_EDU])    # Образование
    # exp_months = extract_experience_months(row[COL_EXP])    # Опыт работы в месяцах
    # exp_ohe = experience_months_to_ohe(exp_months)          # Опыт работы в one hot encoding
    # salary = extract_salary(row[COL_SALARY])                # Зарплата в тысячах рублей
    # salary_vec = np.array([salary])                         # Зарплата в виде вектора

    # # Объединение всех входных данных в один общий вектор
    # x_data = np.hstack([sex_vec,
    #                     age_ohe,
    #                     city_ohe,
    #                     empl_multi,
    #                     sсhed_multi,
    #                     edu_multi,
    #                     exp_ohe])

    # # Возврат входных данных и выходных (зарплаты)
    # return x_data, salary_vec


# Создание общей выборки
# def construct_train_data(row_list):
#     x_data = []
#     y_data = []

#     for row in row_list:
#         x, y = extract_row_data(row)
#         if y[0] > 0:                      # Данные добавляются, только если есть зарплата
#             x_data.append(x)
#             y_data.append(y)

#     return np.array(x_data), np.array(y_data)
