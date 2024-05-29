from pathlib import Path
import pandas as pd
from funcs import read_dataset
from fakers import factories_gen, orders_gen, factories_single_value, orders_single_value

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

# create fully generated datasets
f_db = pd.DataFrame(factories_gen(OPTIONS, 10_000))
o_db = pd.DataFrame(orders_gen(OPTIONS, 30_000))

# #save refactored factories dataset with randomly generated data for nan's
f_db.to_csv(DB_DIR / 'db_generated_factories.csv', index=False)
print('Factories dataset with randomly generated data saved!')

# #save refactored orders dataset with randomly generated data for nan's
o_db.to_csv(DB_DIR / 'db_generated_orders.csv', index=False)
print('Orders dataset with randomly generated data saved!')

# create datasets with fully generated data for nan's only
f_refactored = pd.DataFrame(DB['factories'])
o_refactored = pd.DataFrame(DB['orders'])

# loop columns and find NaN and change it with randomly generated data
for col in f_refactored.columns:
    if f_refactored[col].isnull().values.any():
        print(f'We\'re updating values in {col}...')
        f_refactored[col] = f_refactored[col].map(lambda x: factories_single_value(col, OPTIONS))
        print(f'Values in {col} updated!')

#save refactored factories dataset with randomly generated data for nan's
f_refactored.to_csv(DB_DIR / 'db_refactored_factories_generated.csv', index=False)
print('Refactored factories dataset with randomly generated data saved!')

for col in o_refactored.columns:
    if o_refactored[col].isnull().values.any():
        print(f'We\'re updating values in {col}...')
        o_refactored[col] = o_refactored[col].map(lambda x: orders_single_value(col, OPTIONS))
        print(f'Values in {col} updated!')

#save refactored orders dataset with randomly generated data for nan's
o_refactored.to_csv(DB_DIR / 'db_refactored_orders_generated.csv', index=False)
print('Refactored orders dataset with randomly generated data saved!')
