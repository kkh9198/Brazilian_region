#  브라질 E-commerce Olist 배송기간 예측 프로젝트

팀원 :  김강현, 김주성, 이힘찬, 윤민우, 임윤정

## 프로젝트 요약

### 1.  프로젝트 주제 

   브라질 E-commerce회사인 Olist의 거래 정보 데이터(https://www.kaggle.com/olistbr/brazilian-ecommerce) 를 활용한 배송기간예측
   

### 2.  주제 선정 배경

* 브라질의 배송환경은 국내와 다르게 굉장히 오랜시간이 걸리고, 도심과 비도심의 배송기간의 격차가 큽니다. 따라서 본 프로젝트를 통해 브라질의 Olist를 이용하는 고객에게 예상 배송기간을 예측하고, 더 나아가 이 서비스를 Olist측에 제안하는 형태로 진행했습니다.

### 3.  프로젝트 개요
* Kaggle출처(https://www.kaggle.com/olistbr/brazilian-ecommerce) 를 활용해 배송기간을 예측 하는 모형을 만들고, 이를 서비스화 하여 제공함으로 Olist사에는 고정 고객 유치와 고객에게는 예상 배송기간 제공이라는 서비스를 제공합니다. 

![아키텍처](./이미지/Olist/아키텍처.png)


* 분석된 데이터는 자바와 파이썬 flask를 통해 웹으로 구현 됩니다.  DB는 sqlite를 사용했습니다. 

### 4.  분석에 사용된 툴



|언어|분석 라이브러리|웹|데이터 분석|
|---|---|---|---|
|Python,Java,SQL|Pandas, Numpy, Sikit-Learn,XGBRegressor,BeautifulSoup|HTML5,JS,ajax,CSS|pandas,numpy,datetime,train_test_split,StandardScaler,</br> XGBRegressor,MultiLabelBinarizer,seabBeautifulSoup

|개발 도구|데이터베이스|협업 툴|
|---|---|---|
|Vscode 1.63.2,Python 3.9.7,Jupyter notebook 6.4.5,ANACONDA 2.1.1|Sqlite 3.12.2|Google Drive & Github|




## 프로젝트 정보

### 1.  프로젝트 주제 

   브라질 E-commerce회사인 Olist의 거래 정보 데이터(https://www.kaggle.com/olistbr/brazilian-ecommerce) 를 활용한 배송기간예측

   

### 2.  주제 선정 배경 및 개요

   * 브라질의 배송환경은 국내와 다르게 굉장히 오랜시간이 걸리고, 도심과 비도심의 배송기간의 격차가 큽니다. 따라서 본 프로젝트를 통해 브라질의 Olist를 이용하는 고객에게 예상 배송기간을 예측하고, 더 나아가 이 서비스를 Olist측에 제안하는 형태로 진행했습니다.


   * 브라질 E-commerce의 유니콘 기업인 Olist에 배송기간예측서비스 제공이라는 제안을 하여 고정고객 확보와 더 나아가 이용고객에게 만족을 도모한다.  
     ![개요](./이미지/Olist/개요.png)

   

### 3. 프로젝트 환경

   ![프로젝트환경](./이미지/Olist/프로젝트환경.png)


### 4. 데이터 수집 및 전처리 

데이터는 캐글 Olist의 거래 정보 데이터(https://www.kaggle.com/olistbr/brazilian-ecommerce) 를 활용함.
데이터셋의 ERD는 다음과 같다.

![ERD](./이미지/Olist/ERD.png)

이중에서 분석에 필요한 컬러만 팀 회의를 통해 선정

  ![변수제외](./이미지/Olist/변수제외.png)

다음과 같은 변수들을 선정함

* 이후 포르투갈어로 된 product_category_name을 product_category_name_english로 1:1 매칭 시켜줌

* 데이터는 배송이 완료된 데이터만을 가지고 분석을 진행

* 제품의 높이, 폭, 길이의 컬럼을 부피라는 컬럼으로 전처리 함 

* 결측치는 제품의 크기에 관련한 것은 해당 제품의 카테고리 평균치로 처리 

* 제품의 카테고리가 결측치인 경우 other로 처리


### 5. EDA 

![EDA1](./이미지/Olist/EDA1.png)
![EDA2](./이미지/Olist/EDA2.png)
![EDA3](./이미지/Olist/EDA3.png)
![EDA4](./이미지/Olist/EDA4.png)
![EDA5](./이미지/Olist/EDA5.png)
![EDA6](./이미지/Olist/EDA6.png)

### 6. 파생변수

* 선행된 연구에서는 판매자와 구매자의 위도와 경도를 활용해 geopy 라이브러리를 활용해 지구의 구를 반영한 직선거리를 채택해 분석에 활용했다. 
  하지만, 배송기간예측이라는 목적에는 실제 차량이동거리가 더 주요할 것이라고 판단하여, 실제 차량이 이동한 거리를 크롤링을 진행했다. 시간은 PC 5대로 총 25시간이 걸렸다.  
  ![파생변수](./이미지/Olist/파생변수.png)

### 7. 모델링

* 모델링에는 총 10개의 회귀모형을 사용했으며, 각 각 파생변수 추가 전, 후 geopy가 아닌 실제 이동거리를 적용한 데이터셋 총 3번의 모델링을 진행했다. 

* 이때는 각각 모델의 디폴트 값으로 모델링을 진행했다.

* 데이터셋이 배송기간예측을 위한 셋이 아니다 보니 결과는 좋지 않게 나왔다. 

![모델링](./이미지/Olist/모델링.png)
![모델링1](./이미지/Olist/모델링1.png)
![모델링2](./이미지/Olist/모델링2.png)
![모델링3](./이미지/Olist/모델링3.png)
![모델링4](./이미지/Olist/모델링4.png)


### 8. 프로젝트 시연

   ![실행화면](./이미지/Olist/실행화면.gif)

### 9. 결론

![결론](./이미지/Olist/결론.png)


### 10. 프로젝트 한계점 및 개선점

* 배송기간예측에 최적화 된 데이터셋이 아니라 EDA로 주로 활용되는 데이터셋을 가지고 예측프로젝트를 진행하다 보니 배송기간예측에 주요하게 활용될만한 컬럼이 부족했다고 생각함.

* 다양한 모델의 하이퍼파라미터 조정을 통해 조금더 개선된 모델의 성능을 이끌어 낼 수 있을 것 같다. 

