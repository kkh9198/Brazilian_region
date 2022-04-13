#홈페이지 연동할때 보면 좋을 블로그
#https://ichi.pro/ko/leaflet-d3-js-mich-python-eul-sayonghayeo-daesi-bodeu-peuloto-taib-eul-bildeuhaneun-bangbeob-31875696360373
#이동 관련으로 보면 좋은 블로그
#https://coderzcolumn.com/tutorials/data-science/how-to-create-connection-map-chart-in-python-jupyter-notebook-plotly-and-geopandas
#추가로 보면 좋을것 같은 브라질 통게데이터 모음
#https://www.kaggle.com/andresionek/geospatial-analysis-of-brazilian-e-commerce
#참고222
#https://python.plainenglish.io/how-to-create-a-interative-map-using-plotly-express-geojson-to-brazil-in-python-fb5527ae38fc

#-----------------아래 필요내용-------------------------------------
#참고블로그
#https://rodrigodutcosky.medium.com/mapas-coropl%C3%A9ticos-com-os-estados-do-brasil-em-python-b9b48c6db585
#geopandas import error
#https://blog.daum.net/geoscience/1659
#추가 설치패키지
# conda install descartes

import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
#from dataprep.eda import plot, plot_correlation, plot_missing 

#--------------------브라질 지도정보------------------------------------------------------
INFOS_UFS = gpd.read_file('bcim_2016_21_11_2018.gpkg', layer='lim_unidade_federacao_a')
#-------------------------테스트출력------------------------------------
#INFOS_UFS.columns
#print("Esado:"+INFOS_UFS.nome[2])
#INFOS_UFS.geometry[2]

#-----------------지도 표시대상임포드-------------------------------------------------------------
cases= pd.read_csv("count_geo_customer.csv", delimiter=',')
#cases= pd.read_csv("count_geo_seller.csv", delimiter=',')
#cases.head()
INFOS_UFS.rename({'sigla':'state'},axis=1,inplace=True)
#----------------지도정보+표시정보----------------------------------------------
BRASIL= INFOS_UFS.merge(cases, on='state',how='right')
BRASIL[{'state', 'confirmed_cases','geometry'}].head()

#--------------------출력------------------------------------------------------
#%matplotlib inline
BRASIL.plot(column='confirmed_cases',cmap='Reds',figsize=(16,10),legend=True, edgecolor='black')
