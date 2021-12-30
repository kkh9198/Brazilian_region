#참고 블로그
#https://niceman.tistory.com/193?category=1009824
#https://aidenlim.dev/19
import time
import json
import os
import ssl
import urllib.request
from flask import Flask, render_template, request, redirect, url_for, jsonify
import sqlite3 as sql
import numpy as np
from sklearn.compose import ColumnTransformer
#from ml.model import export_model
#from flask_restful import Resource, Api

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('main.html')

@app.route('/home/')
def sample():
    con = sql.connect("database.db")
    con.row_factory = sql.Row

    cur = con.cursor()
    
    cur.execute("select distinct CATEGORY from olist_products")

    rows = cur.fetchall()
    return render_template('home.html', rows = rows)    

@app.route('/products/', methods=['POST'])
def searchProducts():
    data = request.form['categoryName']

    con = sql.connect("database.db")
    con.row_factory=sql.Row
    cur= con.cursor()
    cur.execute("select product_id from olist_products where category = '" + data + "'")
  
    datas = cur.fetchall()
    print(type(datas))

    datass = []
    for row in datas:
        datass.append([x for x in row])
    datass= np.squeeze(datass,axis=1).tolist()

    con.close()

    return jsonify(datass)

# @app.route('/sellers/', methods=['POST'])
# def searchSellers():
#     data = request.form['productId']
#     print("########################"+data)
#     con = sql.connect("database.db")
#     # con.row_factory=sql.Row
#     cur= con.cursor()
#     datas = cur.execute("select seller_id from olist_products where product_id = '" + data + "'").fetchone()
  
#     print(type(datas))
#     print(datas)

#     con.close()

#     return jsonify(datas)

@app.route('/addrec/', methods=['POST', 'GET'])
def addrec():
    if request.method == 'POST':
        #화면에서 입력받은값
        customer_lat = request.form['lat']
        customer_lng = request.form['lng']
        product_id = request.form['product_id']

        #product_id로 검색
        con = sql.connect("database.db")
        # con.row_factory = sql.Row
        cur = con.cursor()
        cur.execute("select * from OLIST_PRODUCTS a LEFT JOIN OLIST_SELLERS b on a.SELLER_ID = b.SELLER_ID where PRODUCT_ID = '" + product_id + "'")
        rows = cur.fetchone()
        product_id= rows[0]
        seller_id= rows[1]
        product_weight_g= rows[2]
        product_volume= rows[3]
        category= rows[4]
        price= rows[5]
        freight_value= rows[6]
        state= rows[8]
        lat= rows[9]
        lng= rows[10]
        
        #걸리는 시간을 구글에 검색
        origin          = customer_lat+","+customer_lng
        destination     = lat + "," + lng
        mode            = "driving"
        departure_time  = "now"
        key='AIzaSyCoqfsNFyisaIOFPk_kTPTt4wUyMiaK3Rs'

        url = "https://maps.googleapis.com/maps/api/directions/json?origin="+ origin \
            + "&destination=" + destination \
            + "&mode=" + mode \
            + "&departure_time=" + departure_time\
            + "&language=ko" \
            + "&key=" + key
        print(url)
        
        request1         = urllib.request.Request(url)
        context         = ssl._create_unverified_context()
        response        = urllib.request.urlopen(request1, context=context)
        responseText    = response.read().decode('utf-8')
        responseJson    = json.loads(responseText)

        with open("./Agent_Transit_Directions.json","w") as rltStream :
            json.dump(responseJson,rltStream)
        
        #검색 받은 값을 정리
        wholeDict = None
        with open("./Agent_Transit_Directions.json","r") as transitJson :
            wholeDict = dict(json.load(transitJson))
        print(wholeDict)
        path            = wholeDict["routes"][0]["legs"][0]
        duration_km    = path["distance"]["text"]
        #km삭제
        duration_km=duration_km[0:len(duration_km)-2]
        print("*******************"+duration_km)
        #--------------------모델에서 값 추출---------------------
        #입력값 정리
        #연속형 컬럼 정규화
        numerical_columns = [ price, freight_value, product_weight_g, duration_km, product_volume]

        pipeline = ColumnTransformer([
            ("Numerical", StandardScaler(), numerical_columns),
            ], remainder = 'passthrough',)

        train_data = pipeline.fit_transform(train_data)
        test_data = pipeline.transform(test_data)

        #우리가 필요한 행 정규화
        last_row_list = test_no.iloc[-1,:].tolist()
        last_row_df = pd.DataFrame([last_row_list],columns = test_no.columns.tolist())
        last_row_data = pipeline.transform(last_row_df)

        #모델 실행
        prediction= model.predict(last_row_data)
        label= prediction[0]
        #결과출력
        result=label
        print("***************************"+result)
        return render_template('result.html', msg=result)

if __name__ == '__main__':
    #모델부르기
    mode= joblib.load('mode.pkl')
    app.run(debug=True)