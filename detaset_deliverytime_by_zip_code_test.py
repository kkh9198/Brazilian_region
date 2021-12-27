#%%
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
import os
from sklearn.datasets import load_boston

#고객데이터셋
customers_dataset=pd.read_csv("archive/olist_customers_dataset.csv", dtype={'customer_zip_code_prefix': str}, delimiter=',')
#지역데이터셋
geolocation_dataset= pd.read_csv("archive/olist_geolocation_dataset.csv", dtype={'geolocation_zip_code_prefix': str}, delimiter=',')
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

#%%

#--------------테스트----------------

geolocation_dataset= pd.read_csv("archive/olist_geolocation_dataset.csv", dtype={'geolocation_zip_code_prefix': str}, delimiter=',')

# Gets the first three and four first digits of zip codes, we will explore this further to understand how zip codes works
geolocation_dataset['geolocation_zip_code_prefix_1_digits'] = geolocation_dataset['geolocation_zip_code_prefix'].str[0:1]
geolocation_dataset['geolocation_zip_code_prefix_2_digits'] = geolocation_dataset['geolocation_zip_code_prefix'].str[0:2]
geolocation_dataset['geolocation_zip_code_prefix_3_digits'] = geolocation_dataset['geolocation_zip_code_prefix'].str[0:3]
geolocation_dataset['geolocation_zip_code_prefix_4_digits'] = geolocation_dataset['geolocation_zip_code_prefix'].str[0:4]
geolocation_dataset.head(3)

geolocation_dataset['geolocation_zip_code_prefix'].value_counts().to_frame().describe()

# Removing some outliers
#Brazils most Northern spot is at 5 deg 16′ 27.8″ N latitude.;
geolocation_dataset = geolocation_dataset[geolocation_dataset.geolocation_lat <= 5.27438888]
#it’s most Western spot is at 73 deg, 58′ 58.19″W Long.
geolocation_dataset = geolocation_dataset[geolocation_dataset.geolocation_lng >= -73.98283055]
#It’s most southern spot is at 33 deg, 45′ 04.21″ S Latitude.
geolocation_dataset = geolocation_dataset[geolocation_dataset.geolocation_lat >= -33.75116944]
#It’s most Eastern spot is 34 deg, 47′ 35.33″ W Long.
geolocation_dataset = geolocation_dataset[geolocation_dataset.geolocation_lng <=  -34.79314722]

from datashader.utils import lnglat_to_meters as webm
x, y = webm(geolocation_dataset.geolocation_lng, geolocation_dataset.geolocation_lat)
geolocation_dataset['x'] = pd.Series(x)
geolocation_dataset['y'] = pd.Series(y)

# Zip Codes in Brazil
# transforming the prefixes to int for plotting purposes
geolocation_dataset['geolocation_zip_code_prefix'] = geolocation_dataset['geolocation_zip_code_prefix'].astype(int)
geolocation_dataset['geolocation_zip_code_prefix_1_digits'] = geolocation_dataset['geolocation_zip_code_prefix_1_digits'].astype(int)
geolocation_dataset['geolocation_zip_code_prefix_2_digits'] = geolocation_dataset['geolocation_zip_code_prefix_2_digits'].astype(int)
geolocation_dataset['geolocation_zip_code_prefix_3_digits'] = geolocation_dataset['geolocation_zip_code_prefix_3_digits'].astype(int)
geolocation_dataset['geolocation_zip_code_prefix_4_digits'] = geolocation_dataset['geolocation_zip_code_prefix_4_digits'].astype(int)

brazil = geolocation_dataset
agg_name = 'geolocation_zip_code_prefix'
brazil[agg_name].describe().to_frame()

import holoviews as hv
import geoviews as gv
import datashader as ds
from colorcet import fire, rainbow, bgy, bjy, bkr, kb, kr
from datashader.colors import colormap_select, Greys9
from holoviews.streams import RangeXY
from holoviews.operation.datashader import datashade, dynspread, rasterize
from bokeh.io import push_notebook, show, output_notebook

hv.extension('bokeh')

# 그림 크게 만들어주는 코드
%opts Overlay [width=800 height=600 toolbar='above' xaxis=None yaxis=None]
%opts QuadMesh [tools=['hover'] colorbar=True] (alpha=0 hover_alpha=0.2)

T = 0.05
PX = 1

def plot_map(data, label, agg_data, agg_name, cmap):
    url="http://server.arcgisonline.com/ArcGIS/rest/services/Canvas/World_Dark_Gray_Base/MapServer/tile/{Z}/{Y}/{X}.png"
    geomap = gv.WMTS(url)
    points = hv.Points(gv.Dataset(data, kdims=['x', 'y'], vdims=[agg_name]))
    agg = datashade(points, element_type=gv.Image, aggregator=agg_data, cmap=cmap)
    zip_codes = dynspread(agg, threshold=T, max_px=PX)
    hover = hv.util.Dynamic(rasterize(points, aggregator=agg_data, width=50, height=25, streams=[RangeXY]), operation=hv.QuadMesh)
    hover = hover.options(cmap=cmap)
    img = geomap * zip_codes * hover
    img = img.relabel(label)
    return img

# plot_map(brazil, 'Zip Codes in Brazil', ds.min(agg_name), agg_name, cmap=rainbow)


# # Zip Codes in States
# def filter_data(level, name):
#     df = geolocation_dataset[geolocation_dataset[level] == name]
#     #remove outliers
#     df = df[(df.x <= df.x.quantile(0.999)) & (df.x >= df.x.quantile(0.001))]
#     df = df[(df.y <= df.y.quantile(0.999)) & (df.y >= df.y.quantile(0.001))]
#     return df

# sp = filter_data('geolocation_state', 'SP')
# agg_name = 'geolocation_zip_code_prefix'
# sp[agg_name].describe().to_frame()

# plot_map(sp, 'Zip Codes in Sao Paulo State', ds.min(agg_name), agg_name, cmap=rainbow)


# # Zip Codes in Large Cities
# saopaulo = filter_data('geolocation_city', 'sao paulo')
# agg_name = 'geolocation_zip_code_prefix'
# saopaulo[agg_name].describe().to_frame()

# plot_map(saopaulo, 'Zip Codes in Sao Paulo City', ds.min(agg_name), agg_name, cmap=rainbow)


# # Zip Codes in Small Cities
# atibaia = geolocation_dataset[geolocation_dataset['geolocation_city'] == 'atibaia']
# agg_name = 'geolocation_zip_code_prefix'
# atibaia[agg_name].describe().to_frame()

# plot_map(atibaia, 'Zip Codes in Atibaia', ds.min(agg_name), agg_name, cmap=rainbow)

# Average Delivery Time

# getting the first 3 digits of customer zipcode
customers_dataset['customer_zip_code_prefix_3_digits'] = customers_dataset['customer_zip_code_prefix'].str[0:3]
customers_dataset['customer_zip_code_prefix_3_digits'] = customers_dataset['customer_zip_code_prefix_3_digits'].astype(int)

orders = orders_dataset.merge(order_items_dataset, on='order_id')
orders = orders.merge(customers_dataset, on='customer_id')
orders = orders.merge(order_reviews_dataset, on='order_id')

brazil_geo = geolocation_dataset.set_index('geolocation_zip_code_prefix_3_digits').copy()

orders['order_delivered_customer_date'] = pd.to_datetime(orders.order_delivered_customer_date)
orders['order_estimated_delivery_date'] = pd.to_datetime(orders.order_estimated_delivery_date)
orders['order_delivered_carrier_date'] = pd.to_datetime(orders.order_delivered_carrier_date)
orders['actual_delivery_time'] = orders.order_delivered_customer_date - orders.order_delivered_carrier_date
orders['actual_delivery_time'] = orders['actual_delivery_time'].dt.days


gp = orders.groupby('customer_zip_code_prefix_3_digits')['actual_delivery_time'].mean().to_frame()
delivery_time = brazil_geo.join(gp)
agg_name = 'avg_delivery_time'
delivery_time[agg_name] = delivery_time['actual_delivery_time']

plot_map(delivery_time, 'Orders Average Delivery Time (days)', ds.mean(agg_name), agg_name, cmap=bjy)



# %%
