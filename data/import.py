import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from sklearn.datasets import load_boston
from dataprep.eda import plot, plot_correlation, plot_missing 

#데이터로드
#고객데이터셋
customers_dataset=pd.read_csv("archive/olist_customers_dataset.csv", delimiter=',')
#지역데이터셋
geolocation_dataset= pd.read_csv("archive/olist_geolocation_dataset.csv", delimiter=',')
#주문상품데이터셋
order_items_dataset=pd.read_csv("archive/olist_order_items_dataset.csv", delimiter=',')
#결제방식
order_payments_dataset=pd.read_csv("archive/olist_order_payments_dataset.csv", delimiter=',')
#리뷰방식
order_reviews_dataset=pd.read_csv("archive/olist_order_reviews_dataset.csv", delimiter=',')
#주문
orders_dataset=pd.read_csv("archive/olist_orders_dataset.csv", delimiter=',')
#상품
products_dataset=pd.read_csv("archive/olist_products_dataset2.csv", delimiter=',')
#판매자데이터셋
sellers_dataset=pd.read_csv("archive/olist_sellers_dataset.csv", delimiter=',')
#지역명
product_category_name_translation=pd.read_csv("archive/product_category_name_translation.csv", delimiter=',')

