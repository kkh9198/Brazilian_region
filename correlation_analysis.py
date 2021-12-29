#%%

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import csv

df = pd.read_csv('finaldf2.csv', parse_dates = ['order_purchase_timestamp', 'order_approved_at', 'order_delivered_carrier_date', 'order_delivered_customer_date'])

pd.options.display.max_columns = 999
# %%

df.corr()
plt.figure(figsize=(10,8))
sns.heatmap(df.corr(), vmin=-1, vmax=1, annot=True, cmap="cubehelix_r")
plt.show()

#%%
# 피어슨 상관계수
df.corr(method='pearson')
plt.figure(figsize=(10,8))
sns.heatmap(df.corr(method='pearson'), vmin=-1, vmax=1, annot=True, cmap="cubehelix_r")
plt.show()


# %%
# 스피어만 상관계수
df.corr(method='spearman')
plt.figure(figsize=(10,8))
sns.heatmap(df.corr(method='spearman'), vmin=-1, vmax=1, annot=True, cmap="cubehelix_r")
plt.show()
# %%
