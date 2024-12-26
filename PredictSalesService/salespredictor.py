import os
import pandas as pd
import numpy as np
import joblib
from sklearn.utils.class_weight import compute_class_weight
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor

class SalesPredictor:
    def __init__(self, data_path='data/', models_path='models/', processed_data_path='processed_data/'):
        """
        Инициализация класса SalesPredictor.

        :param data_path: Путь к директории с исходными данными.
        :param models_path: Путь к директории с моделями.
        :param processed_data_path: Путь к директории для сохранения обработанных данных.
        """
        self.data_path = data_path
        self.models_path = models_path
        self.processed_data_path = processed_data_path

        os.makedirs(self.processed_data_path, exist_ok=True)

        self.full_data_file = os.path.join(self.processed_data_path, 'full_data.pkl')

        # Загрузка данных
        self.sales_train_data = pd.read_csv(f'{self.data_path}sales_train.csv', parse_dates=['date'], dayfirst=True)
        self.item_categories = pd.read_csv(f'{self.data_path}item_categories.csv')
        self.items = pd.read_csv(f'{self.data_path}items.csv')
        self.shops = pd.read_csv(f'{self.data_path}shops.csv')

        # Предварительная обработка данных 
        self._preprocess_data()

        # Загрузка моделей, если они уже обучены
        try:
            self.classifier = joblib.load(f'{self.models_path}model3_clf1.pkl')
            self.regressor = joblib.load(f'{self.models_path}model3_reg.pkl')
            print("Модели успешно загружены.")
        except FileNotFoundError:
            print("Модели не найдены. Требуется обучение моделей.")
            self.classifier = None
            self.regressor = None

    def _preprocess_data(self):
        """
        Внутренний метод для предварительной обработки данных.
        Загружает обработанные данные, если они существуют, иначе выполняет обработку и сохраняет результат.
        """
        if os.path.exists(self.full_data_file):
            print("Загружаем обработанные данные из файла.")
            self.full_data = pd.read_pickle(self.full_data_file)
            self.max_date_block_num = self.full_data['date_block_num'].max()
        else:
            print("Обрабатываем исходные данные.")
            
            self.sales_train_data.drop_duplicates(inplace=True)

            # Агрегация данных по месяцам, магазинам и товарам
            monthly_sales = self.sales_train_data.groupby(['date_block_num', 'shop_id', 'item_id']).agg({
                'item_cnt_day': 'sum',
                'item_price': 'mean'
            }).reset_index()
            monthly_sales.rename(columns={'item_cnt_day': 'item_cnt_month', 'item_price': 'avg_item_price'}, inplace=True)

            self.max_date_block_num = monthly_sales['date_block_num'].max()

            shops_list = self.shops['shop_id'].unique()
            items_list = self.items['item_id'].unique()
            date_block_num = monthly_sales['date_block_num'].unique()

            # Создание полной матрицы комбинаций магазинов, товаров и месяцев
            full_matrix = pd.DataFrame([
                (i, j, k) for k in date_block_num for i in shops_list for j in items_list
            ], columns=['shop_id', 'item_id', 'date_block_num'])

            full_data = pd.merge(full_matrix, monthly_sales, on=['shop_id', 'item_id', 'date_block_num'], how='left')
            full_data['item_cnt_month'].fillna(0, inplace=True)
            full_data['avg_item_price'].fillna(0, inplace=True)

            # Объединение с информацией о товарах, категориях и магазинах
            full_data = pd.merge(full_data, self.items, on='item_id', how='left')
            full_data = pd.merge(full_data, self.item_categories, on='item_category_id', how='left')
            full_data = pd.merge(full_data, self.shops, on='shop_id', how='left')

            # Кодирование категориальных признаков
            full_data['shop_name'] = full_data['shop_name'].astype('category').cat.codes
            full_data['item_category_name'] = full_data['item_category_name'].astype('category').cat.codes

            # Создание признаков года и месяца
            full_data['year'] = 2013 + (full_data['date_block_num'] // 12)
            full_data['month'] = (full_data['date_block_num'] % 12) + 1

            # Создание лаговых признаков
            for lag in [1, 2, 3]:
                tmp = monthly_sales[['date_block_num', 'shop_id', 'item_id', 'item_cnt_month']].copy()
                tmp['date_block_num'] += lag
                tmp = tmp.rename(columns={'item_cnt_month': f'item_cnt_lag_{lag}'})
                full_data = pd.merge(full_data, tmp, on=['shop_id', 'item_id', 'date_block_num'], how='left')
                full_data[f'item_cnt_lag_{lag}'].fillna(0, inplace=True)

            full_data.fillna(0, inplace=True)

            # Сохранение обработанных данных
            self.full_data = full_data
            self.save_processed_data()
            print("Обработанные данные сохранены.")

    def save_processed_data(self):
        """
        Сохраняет обработанные данные в файл.
        """
        self.full_data.to_pickle(self.full_data_file)
        print(f"Обработанные данные сохранены в {self.full_data_file}")

    def load_processed_data(self):
        """
        Загружает обработанные данные из файла.
        """
        if os.path.exists(self.full_data_file):
            self.full_data = pd.read_pickle(self.full_data_file)
            self.max_date_block_num = self.full_data['date_block_num'].max()
            print("Обработанные данные успешно загружены.")
        else:
            print("Файл с обработанными данными не найден. Необходимо выполнить предварительную обработку.")
            self._preprocess_data()

    def train_models(self):
        """
        Обучение классификатора и регрессора на подготовленных данных.
        """
        train_data = self.full_data[self.full_data['date_block_num'] < self.max_date_block_num]

        # Создание бинарной цели для классификации
        y_binary = (train_data['item_cnt_month'] > 0).astype(int)

        # Вычисление весов классов
        classes = np.array([0, 1])  # 0 - нулевые продажи, 1 - ненулевые продажи
        class_weights = compute_class_weight(class_weight='balanced', classes=classes, y=y_binary)
        weights = {0: class_weights[0], 1: class_weights[1]}

        # Обучение классификатора
        clf = RandomForestClassifier(n_estimators=100, class_weight=weights, random_state=42, n_jobs=-1)
        X = train_data.drop(['item_cnt_month', 'item_name', 'item_category_id'], axis=1)
        y_class = y_binary
        clf.fit(X, y_class)

        # Сохранение классификатора
        joblib.dump(clf, os.path.join(self.models_path, 'model3_clf1.pkl'))
        self.classifier = clf
        print("Классификатор обучен и сохранён.")

        # Обучение регрессора на подмножестве данных с ненулевыми продажами
        train_data_reg = train_data[train_data['item_cnt_month'] > 0]
        X_reg = train_data_reg.drop(['item_cnt_month', 'item_name', 'item_category_id'], axis=1)
        y_reg = train_data_reg['item_cnt_month']

        reg = RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1)
        reg.fit(X_reg, y_reg)

        # Сохранение регрессора
        joblib.dump(reg, os.path.join(self.models_path, 'model3_reg.pkl'))
        self.regressor = reg
        print("Регрессор обучен и сохранён.")

    def prepare_features(self, current_date_block_num):
        """
        Подготовка признаков для предсказания следующего месяца.

        :param current_date_block_num: Текущий номер блока дат (месяц).
        :return: DataFrame с признаками для предсказания.
        """
        # Создание полного набора комбинаций для следующего месяца
        next_date_block_num = current_date_block_num + 1
        shops_list = self.shops['shop_id'].unique()
        items_list = self.items['item_id'].unique()

        full_matrix_next = pd.DataFrame([
            (i, j, next_date_block_num) for i in shops_list for j in items_list
        ], columns=['shop_id', 'item_id', 'date_block_num'])

        # Объединение с историческими данными
        next_data = pd.merge(full_matrix_next, self.full_data, on=['shop_id', 'item_id', 'date_block_num'], how='left')
        next_data['item_cnt_month'].fillna(0, inplace=True)
        next_data['avg_item_price'].fillna(0, inplace=True)

        # Объединение с информацией о товарах, категориях и магазинах
        next_data = pd.merge(next_data, self.items, on='item_id', how='left')
        next_data = pd.merge(next_data, self.item_categories, on='item_category_id', how='left')
        next_data = pd.merge(next_data, self.shops, on='shop_id', how='left')

        # Кодирование категориальных признаков
        next_data['shop_name'] = next_data['shop_name'].astype('category').cat.codes
        next_data['item_category_name'] = next_data['item_category_name'].astype('category').cat.codes

        # Создание признаков года и месяца
        next_data['year'] = 2013 + (next_data['date_block_num'] // 12)
        next_data['month'] = (next_data['date_block_num'] % 12) + 1

        # Создание лаговых признаков
        for lag in [1, 2, 3]:
            lag_date_block_num = next_date_block_num - lag
            lag_data = self.full_data[self.full_data['date_block_num'] == lag_date_block_num][['shop_id', 'item_id', 'item_cnt_month']]
            lag_data = lag_data.rename(columns={'item_cnt_month': f'item_cnt_lag_{lag}'})
            next_data = pd.merge(next_data, lag_data, on=['shop_id', 'item_id'], how='left')
            next_data[f'item_cnt_lag_{lag}'].fillna(0, inplace=True)

        
        next_data.fillna(0, inplace=True)

        # Выбор необходимых признаков 
        features = [
            'shop_id', 'item_id', 'date_block_num', 'avg_item_price',
            'shop_name', 'item_category_name', 'year', 'month',
            'item_cnt_lag_1', 'item_cnt_lag_2', 'item_cnt_lag_3'
        ]
        X_next = next_data[features]

        return X_next

    def predict_next_month(self, current_date_block_num):
        """
        Предсказание продаж на следующий месяц.

        :param current_date_block_num: Текущий номер блока дат (месяц).
        :return: DataFrame с предсказанными продажами.
        """
        if self.classifier is None or self.regressor is None:
            raise ValueError("Модели не загружены.")

        
        X_next = self.prepare_features(current_date_block_num)

        # Предсказание наличия продаж
        y_pred_class = self.classifier.predict(X_next)

        # Предсказание количества продаж 
        X_reg = X_next[y_pred_class == 1]
        y_pred_reg = self.regressor.predict(X_reg)

        # Создание финального предсказания
        y_pred = np.zeros(len(X_next))
        y_pred[y_pred_class == 1] = y_pred_reg

        # Создание результирующего DataFrame
        predictions = X_next.copy()
        predictions['item_cnt_month_pred'] = y_pred
        predictions['is_sale_pred'] = y_pred_class

        return predictions[['shop_id', 'item_id', 'item_cnt_month_pred', 'is_sale_pred']]


    def update_data(self, new_sales_data):
        """
        Обновление исторических данных новыми продажами.

        :param new_sales_data: DataFrame с новыми продажами.
        """
        print("Обновляем исторические данные новыми продажами.")
        # Агрегация новых продаж
        new_monthly_sales = new_sales_data.groupby(['date_block_num', 'shop_id', 'item_id']).agg({
            'item_cnt_day': 'sum',
            'item_price': 'mean'
        }).reset_index()
        new_monthly_sales.rename(columns={'item_cnt_day': 'item_cnt_month', 'item_price': 'avg_item_price'}, inplace=True)

        # Обновление full_data
        self.full_data = pd.concat([self.full_data, new_monthly_sales], ignore_index=True)

        # Объединение с информацией о товарах, категориях и магазинах
        self.full_data = pd.merge(self.full_data, self.items, on='item_id', how='left', suffixes=('', '_y'))
        self.full_data = pd.merge(self.full_data, self.item_categories, on='item_category_id', how='left', suffixes=('', '_y'))
        self.full_data = pd.merge(self.full_data, self.shops, on='shop_id', how='left', suffixes=('', '_y'))

        # Удаление дублирующихся колонок
        self.full_data = self.full_data.loc[:, ~self.full_data.columns.duplicated()]

        self.full_data['shop_name'] = self.full_data['shop_name'].astype('category').cat.codes
        self.full_data['item_category_name'] = self.full_data['item_category_name'].astype('category').cat.codes

        self.full_data['year'] = 2013 + (self.full_data['date_block_num'] // 12)
        self.full_data['month'] = (self.full_data['date_block_num'] % 12) + 1

        for lag in [1, 2, 3]:
            tmp = new_monthly_sales[['date_block_num', 'shop_id', 'item_id', 'item_cnt_month']].copy()
            tmp['date_block_num'] += lag
            tmp = tmp.rename(columns={'item_cnt_month': f'item_cnt_lag_{lag}'})
            self.full_data = pd.merge(self.full_data, tmp, on=['shop_id', 'item_id', 'date_block_num'], how='left')
            self.full_data[f'item_cnt_lag_{lag}'].fillna(0, inplace=True)

        self.full_data.fillna(0, inplace=True)

        self.max_date_block_num = self.full_data['date_block_num'].max()

        # Сохранение обновлённых обработанных данных
        self.save_processed_data()
        print("Исторические данные обновлены и сохранены.")

