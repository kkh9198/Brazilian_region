#!/usr/bin/env python
# coding: utf-8

# In[1]:
import pandas as pd
import numpy as np
import datetime
import joblib

#함수
def makeMyList(price,freight,weight,category,s_state,distance,volume):
    now = datetime.datetime.now()

    return  [price,freight,weight,category,0,'SP',s_state,distance,
     now.year,now.month,now.day,now.weekday(),now.hour,volume] 

def toList(x):
    a = []
    a.append(str(x))
    return a

def plusCustomer(x):
    return x+"_C"

def plusSeller(x):
    return x+"_S"

def ss(a,b,c,d,e,f,g):
    df = pd.read_csv('dataInputFormat.csv')

    new = pd.DataFrame([makeMyList(a,b,c,d,e,f,g)],
                columns = df.columns.tolist())

    #test 전처리
    test = pd.concat([df, new],ignore_index=True)
    test['product_category_name_english']= test['product_category_name_english'].apply(toList)
    test['customer_state']= test['customer_state'].apply(plusCustomer)
    test['seller_state']= test['seller_state'].apply(plusSeller)
    test['customer_state']= test['customer_state'].apply(toList)
    test['seller_state']= test['seller_state'].apply(toList)

    #원핫인코딩
    from sklearn.preprocessing import MultiLabelBinarizer
    mlb = MultiLabelBinarizer()
    test = pd.concat([test, pd.DataFrame(mlb.fit_transform(test['product_category_name_english']), columns = mlb.classes_, index = test.index)], axis = 1)
    test = pd.concat([test, pd.DataFrame(mlb.fit_transform(test['customer_state']), columns = mlb.classes_, index = test.index)], axis = 1)
    test = pd.concat([test, pd.DataFrame(mlb.fit_transform(test['seller_state']), columns = mlb.classes_, index = test.index)], axis = 1)

    #필요없는 컬럼 제거
    test.drop('product_category_name_english',axis=1,inplace=True)
    test.drop('customer_state',axis=1,inplace=True)
    test.drop('seller_state',axis=1,inplace=True)
    print("******************************************************1")
    #표준화 
    from sklearn.model_selection import train_test_split
    from sklearn.pipeline import Pipeline
    from sklearn.compose import ColumnTransformer
    from sklearn.preprocessing import StandardScaler

    test_no =test.drop(['order_delivered_customer_date_delay'], axis = 1)
    test_no['order_purchase_month_sin'] = np.sin(test_no['order_purchase_month'] / 12 * 2 * np.pi)
    test_no['order_purchase_month_cos'] = np.cos(test_no['order_purchase_month'] / 12 * 2 * np.pi)
    test_no['order_purchase_day_sin'] = np.sin(test_no['order_purchase_day'] / 31 * 2 * np.pi)
    test_no['order_purchase_day_cos'] = np.cos(test_no['order_purchase_day'] / 31 * 2 * np.pi)
    test_no['order_purchase_dayofweek_sin'] = np.sin(test_no['order_purchase_dayofweek'] / 7 * 2 * np.pi)
    test_no['order_purchase_dayofweek_cos'] = np.cos(test_no['order_purchase_dayofweek'] / 7 * 2 * np.pi)
    test_no['order_purchase_hour_sin'] = np.sin(test_no['order_purchase_hour'] / 24 * 2 * np.pi)
    test_no['order_purchase_hour_cos'] = np.cos(test_no['order_purchase_hour'] / 24 * 2 * np.pi)

    #컬럼 드롭
    columns3 = ['order_purchase_year', 'order_purchase_month', 'order_purchase_day',
        'order_purchase_dayofweek', 'order_purchase_hour']
    test_no.drop(columns3,axis=1,inplace=True)

    #데이터셋 split
    train_data, test_data, train_labels, test_labels = train_test_split(test_no.iloc[:-1], test['order_delivered_customer_date_delay'].iloc[:-1], test_size = 0.2, random_state = 42)

    #연속형 컬럼 정규화
    numerical_columns = [ 'price', 'freight_value', 'product_weight_g', 'distance_crawling',
                        'volume_cm']

    pipeline = ColumnTransformer([
        ("Numerical", StandardScaler(), numerical_columns),
        ], remainder = 'passthrough',)

    train_data = pipeline.fit_transform(train_data)
    test_data = pipeline.transform(test_data)

    #우리가 필요한 행 정규화
    last_row_list = test_no.iloc[-1,:].tolist()
    print(last_row_list)
    print(type(last_row_list))
    last_row_df = pd.DataFrame([last_row_list],columns = test_no.columns.tolist())
    last_row_data = pipeline.transform(last_row_df)
    print("******************************************************2")
    return last_row_data
def road():
    from xgboost.sklearn import XGBRegressor
    xgb = XGBRegressor()
    xgb.fit(train_data, train_labels)

    joblib.dump(xgb,'model.pkl')
def start():
    res =xgb.predict(last_row_data)
    res[0]

