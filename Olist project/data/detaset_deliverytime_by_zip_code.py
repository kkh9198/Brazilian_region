# 생성파일명 geo.csv
# olist_products_dataset2.csv 파일 정보 수정 있음
# 아래 항목이 표시되는 파일 생성(상품당 배송시간,구매자위치, 판매자 위치)
# order_id,
# customer_id,
# order_purchase_timestamp,
# order_approved_at,
# order_delivered_carrier_date,
# order_delivered_customer_date,
# product_id,
# seller_id,
# product_category_name_english,
# customer_zip_code_prefix,
# seller_zip_code_prefix

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import csv
from sklearn.datasets import load_boston

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
geolocation_dataset=pd.read_csv("archive/olist_geolocation_dataset.csv", delimiter=',')
#---------필요없는 내용 삭제-----------
#고객 테이블
delete_customers_dataset = customers_dataset.loc[:,['customer_id','customer_unique_id','customer_zip_code_prefix','customer_city','customer_state']]
delete_customers_dataset1=delete_customers_dataset.drop(['customer_unique_id','customer_city','customer_state'],axis='columns')
delete_customers_dataset1.to_csv('delete_customers_dataset1.csv',index=None)
#주문
delete_orders_dataset = orders_dataset.loc[:,['order_id','customer_id','order_status','order_purchase_timestamp','order_approved_at','order_delivered_carrier_date','order_delivered_customer_date','order_estimated_delivery_date']]
delete_orders_dataset1=delete_orders_dataset.drop(['order_status','order_estimated_delivery_date'],axis='columns')
delete_orders_dataset1.to_csv('delete_orders_dataset1.csv',index=None)
#주문상품
delete_order_items_dataset = order_items_dataset.loc[:,['order_id','order_item_id','product_id','seller_id','shipping_limit_date','price','freight_value']]
delete_order_items_dataset1=delete_order_items_dataset.drop(['order_item_id','shipping_limit_date','price','freight_value'],axis='columns')
delete_order_items_dataset1.to_csv('delete_order_items_dataset1.csv',index=None)
#상품
delete_products_dataset2 = products_dataset.loc[:,['no','product_id','product_name_lenght','product_description_lenght','product_photos_qty','product_weight_g','product_length_cm','product_height_cm','product_width_cm','product_category_name_english']]
delete_products_dataset21=delete_products_dataset2.drop(['no','product_name_lenght','product_description_lenght','product_photos_qty','product_weight_g','product_length_cm','product_height_cm','product_width_cm'],axis='columns')
delete_products_dataset21.to_csv('delete_products_dataset21.csv',index=None)
#판매자
delete_sellers_dataset = sellers_dataset.loc[:,['seller_id','seller_zip_code_prefix','seller_city','seller_state']]
delete_sellers_dataset1=delete_sellers_dataset.drop(['seller_city','seller_state'],axis='columns')
delete_sellers_dataset1.to_csv('delete_sellers_dataset1.csv',index=None)

#--------------내용 병합----------------
orders_dataset1=pd.read_csv("delete_orders_dataset1.csv", delimiter=',')
order_items_dataset1=pd.read_csv("delete_order_items_dataset1.csv", delimiter=',')
products_dataset21=pd.read_csv("delete_products_dataset21.csv", delimiter=',')
geo_sellers_dataset1=pd.read_csv("delete_sellers_dataset1.csv", delimiter=',')
geo_customers_dataset1=pd.read_csv("delete_customers_dataset1.csv", delimiter=',')

# 주문, 주문상품
testa =pd.merge(orders_dataset1,order_items_dataset1,on='order_id')
# 프로덕트
testb =pd.merge(testa,products_dataset21,how="left",on='product_id')
# 고객
testc=pd.merge(testb,geo_customers_dataset1,how="left",on='customer_id')
# 판매자
testd=pd.merge(testc,geo_sellers_dataset1,how="left",on='seller_id')
testd.to_csv('deliverytime_by_zip_code.csv',index=None)