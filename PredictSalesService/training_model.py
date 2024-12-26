import pandas as pd
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.utils.class_weight import compute_class_weight
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.metrics import classification_report, mean_squared_error
import joblib
import numpy as np


train_data = pd.read_feather('train_data.feather')

classes = np.array([0, 1])  # 0 - нулевые продажи, 1 - ненулевые продажи
y_binary = (train_data['item_cnt_month'] > 0).astype(int)
class_weights = compute_class_weight(class_weight='balanced', classes=classes, y=y_binary)
weights = {0: class_weights[0], 1: class_weights[1]}

# Добавление весов в обучающие данные
train_data['weight'] = train_data['item_cnt_month'].apply(lambda x: weights[0] if x == 0 else weights[1])

train_data['is_sale'] = (train_data['item_cnt_month'] > 0).astype(int)


X = train_data.drop(['item_cnt_month', 'is_sale', 'item_name', 'item_category_id'], axis=1)
y_class = train_data['is_sale']
y_reg = train_data['item_cnt_month']


X_train, X_val, y_train_class, y_val_class, y_train_reg, y_val_reg = train_test_split(
    X, y_class, y_reg, test_size=0.2, random_state=42, stratify=y_class
)


# Обучение классификатора
clf = RandomForestClassifier(n_estimators=100, class_weight='balanced', random_state=42)
clf.fit(X_train, y_train_class)

joblib.dump(clf, "model3_clf1.pkl") # Сохранение модели классификатора


y_pred_class = clf.predict(X_val)
print(classification_report(y_val_class, y_pred_class))


X_train_reg = X_train[y_train_class == 1]
y_train_reg_subset = y_train_reg[y_train_class == 1]

# Обучение регрессора только на данных с продажами в валидационной выборке
X_val_reg = X_val[y_val_class == 1]
y_val_reg_subset = y_val_reg[y_val_class == 1]

reg = RandomForestRegressor(n_estimators=100, random_state=42)
reg.fit(X_train_reg, y_train_reg)

joblib.dump(reg, "model3_reg.pkl") # Сохранение модели регрессора


y_pred_reg = reg.predict(X_val_reg)
rmse = np.sqrt(mean_squared_error(y_val_reg, y_pred_reg))
print(f'RMSE для регрессии: {rmse}')

# Итоговое предсказание
final_predictions = clf.predict(X_val) * reg.predict(X_val)