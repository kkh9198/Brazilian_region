#https://coderzcolumn.com/tutorials/data-science/how-to-create-connection-map-chart-in-python-jupyter-notebook-plotly-and-geopandas
#참고용 추가 데이터셋
#https://www.kaggle.com/ramirobentes/flights-in-brazil
#pip install plotly
import pandas as pd
import geopandas as gpd

import matplotlib.pyplot as plt
import plotly.graph_objects as go

#geolocation정보 평균값 출력
geolocation_dataset= pd.read_csv("archive/olist_geolocation_dataset.csv", delimiter=',')
geolocation_dataset.head()

#우편번호로 그룹바이
avg_group=geolocation_dataset.groupby(by=geolocation_dataset.geolocation_zip_code_prefix)
#출력
avg.to_csv('avg_zip_code.csv')
