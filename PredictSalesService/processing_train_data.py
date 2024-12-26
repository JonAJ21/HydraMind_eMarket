import pandas as pd
import numpy as np
import pyarrow


sales_train_data = pd.read_csv('data/sales_train.csv', parse_dates=['date'], dayfirst=True)
item_categories = pd.read_csv('data/item_categories.csv')
items = pd.read_csv('data/items.csv')
shops = pd.read_csv('data/shops.csv')

sales_train_data.drop_duplicates()

monthly_sales = sales_train_data.groupby(['date_block_num', 'shop_id', 'item_id']).agg({'item_cnt_day': 'sum', 'item_price': 'mean'}).reset_index()
monthly_sales.rename(columns={'item_cnt_day': 'item_cnt_month', 'item_price': 'avg_item_price'}, inplace=True)


max_date_block_num = monthly_sales['date_block_num'].max()

# Получим список всех магазинов и товаров
shops_list = monthly_sales['shop_id'].unique()
items_list = monthly_sales['item_id'].unique()
date_block_num = monthly_sales['date_block_num'].unique()

# Создадим полный набор данных
full_matrix = pd.DataFrame([(i, j, k) for k in date_block_num for i in shops_list for j in items_list],
                           columns=['shop_id', 'item_id', 'date_block_num'])

full_data = pd.merge(full_matrix, monthly_sales, on=['shop_id', 'item_id', 'date_block_num'], how='left')
full_data['item_cnt_month'].fillna(0, inplace=True)
full_data['avg_item_price'].fillna(0, inplace=True)

# Объединение с информацией о товарах
full_data = pd.merge(full_data, items, on='item_id', how='left')

# Объединение с категориями товаров
full_data = pd.merge(full_data, item_categories, on='item_category_id', how='left')

# Объединение с информацией о магазинах
full_data = pd.merge(full_data, shops, on='shop_id', how='left')

# Обработка категориальных признаков (если необходимо)
# Например, кодирование названий магазинов и категорий
full_data['shop_name'] = full_data['shop_name'].astype('category').cat.codes
full_data['item_category_name'] = full_data['item_category_name'].astype('category').cat.codes

full_data['year'] = 2013 + (full_data['date_block_num'] // 12)
full_data['month'] = (full_data['date_block_num'] % 12) + 1

for lag in [1,2,3]:
    tmp = monthly_sales[['date_block_num', 'shop_id', 'item_id', 'item_cnt_month']].copy()
    tmp['date_block_num'] += lag
    tmp = tmp.rename(columns={'item_cnt_month': f'item_cnt_lag_{lag}'})
    full_data = pd.merge(full_data, tmp, on=['shop_id', 'item_id', 'date_block_num'], how='left')
    full_data[f'item_cnt_lag_{lag}'].fillna(0, inplace=True)
    
train_data = full_data[full_data['date_block_num'] < max_date_block_num]
train_data.to_feather('train_data.feather', chunksize=10000)