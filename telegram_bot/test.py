from _funcs import *
from _nn import recommended_manufacturers

my_dict = {
    "key1": "value1",
    "key2": "value2",
    "key3": "value3"
}
print(list(my_dict.values()))

# results, db = recommended_manufacturers(162, n=25, original=True, db_type='original')
# res=''
# for i in range(results.shape[0]):
#     result = db.iloc[results.index[i],:].dropna()
#     res+=f'#{i+1}\n'

#     for key, val in result.items():
#         text = []

#         if isinstance(val, str) and len(val):
#             for x in val.split(', '):
#                 text.append(x)

#         text = ", ".join(text)
#         res+=f'{key}: {text}'
#         res+='\n'
#     res+='*'*100
#     res+='\n'

# body = f'Recommended manufacturers for your order: \n\n{res}'
# print(body)