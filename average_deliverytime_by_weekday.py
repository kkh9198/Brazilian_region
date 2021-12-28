#%%

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pandas.core.tools.datetimes import to_datetime
import seaborn as sns
import csv
import os
from datetime import datetime

#주문 날짜 요일별 분류

#주문 데이터셋
orders_dataset=pd.read_csv("archive/olist_orders_dataset.csv", delimiter=',')

orders_dataset.head(5)
orders_dataset.describe()

pd.options.display.max_columns = 999

# orders_dataset['order_approved_at'] = pd.to_datetime(orders_dataset['order_approved_at'], format='%Y-%m-%d HH:MM')

# 배송 소요 기간 (주문확인부터 배송완료까지)
# order_approved_at 대신 order_delivered_carrier_date 사용도 고려
orders_dataset['order_approved_at'] = pd.to_datetime(orders_dataset.order_approved_at)
orders_dataset['order_delivered_customer_date'] = pd.to_datetime(orders_dataset.order_delivered_customer_date)
orders_dataset['order_delivered_carrier_date'] = pd.to_datetime(orders_dataset.order_delivered_carrier_date)

orders_dataset['actual_delivery_time'] = orders_dataset.order_delivered_customer_date - orders_dataset.order_approved_at
orders_dataset['actual_delivery_time'] = orders_dataset['actual_delivery_time'].dt.days

orders_dataset['actual_delivery_time']

orders_dataset['order_approved_at_date'] = pd.to_datetime(orders_dataset['order_approved_at'], format='%Y-%m-%d HH:MM')
orders_dataset['order_approved_at_weekday'] = orders_dataset['order_approved_at_date'].dt.day_name()
orders_dataset['order_approved_at_weekday']

weeksum = orders_dataset.groupby('order_approved_at_weekday')['actual_delivery_time'].mean()

weeks = ['Monday','Tuesday','Wednesday','Thursday',"Friday","Saturday","Sunday"]

weeksum = weeksum.agg(weeks)

weeksum

#%%

# 요일별 평균 배송시간
plt.figure(figsize=(10,5))
plt.plot(weeksum.index,weeksum)
plt.title('average delivery time by weekday')
plt.xlabel('weekday')
plt.ylabel('delivery time(day)')
plt.yticks(np.arange(5,15))
plt.xticks(np.arange(7))
plt.show()

# %%
