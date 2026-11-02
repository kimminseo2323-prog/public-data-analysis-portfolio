##############################################################################################

##   데이터  전처리      ####

##############################################################################################

##############################################################################################
## 분석 패키지 설정    ####
##############################################################################################

import gc
import numpy as np
import datetime as dt
from datetime import datetime, timedelta
import pandasql as pandasql
import openpyxl as openpyxl
import datatable as dtable
import glob
import itertools
import os

from pandasql import sqldf

# boxplot 그리기
import seaborn as sns
import matplotlib.pyplot as plt

from pandas import DataFrame
from datetime import datetime, date
from pandasql import *

## GIS 정보 불러오기
import geopandas as gpd
import matplotlib.pyplot as plt

## 정규분포 PSI 분석을 위한 패키지 : Scipy 패키지 설치
from scipy.stats import norm

## 두 분포가 겹치는 분석 Mixture 모델
from sklearn.mixture import GaussianMixture

## 상관관계 분석
from scipy.stats import pearsonr

## 군집분석 표준화
from sklearn.preprocessing import StandardScaler      # 패키지 sklearn_pandas

## 계층적 군집분석
from scipy.cluster.hierarchy import linkage, dendrogram
import matplotlib.pyplot as plt

## 군집분석
from sklearn.cluster import KMeans

## decision tree
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.tree._export import export_text

## 회귀분석
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import MinMaxScaler, StandardScaler, RobustScaler
import statsmodels.api as sm

## 로지스틱
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

## 예측값 , 타겟 검증
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error, r2_score

# 다중공선성
from statsmodels.stats.outliers_influence import variance_inflation_factor


##############################################################################################
## 원천데이터 로딩 후 분석데이터 생성    ####
##############################################################################################

## 분석데이터 불러오기

living_comdb = pd.read_pickle('living_comdb2.pkl')    # 생활업종 데이터 중 아산시만 추출

## 업종분류코드
industry_lv2 = pd.read_excel('D:\\data\\기타\\아산시_업종카테고리.xlsx', dtype=str, sheet_name=1)
industry_lv1 = pd.read_excel('D:\\data\\기타\\아산시_업종카테고리.xlsx', dtype=str, sheet_name=2)

############################################################################################

#############   충청남도 인허가데이터 다운로드. 엑셀데이터 오류 발생하여 csv 파일로 로드

folder_path = 'D:\\data\\생활업종_csv'

# 폴더 내의 Excel 파일 목록 가져오기
csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]

# 데이터프레임을 담을 딕셔너리 초기화
dataframes = {}

varlist = ['번호', '개방서비스명', '개방서비스아이디', '개방자치단체코드', '관리번호', '인허가일자', '인허가취소일자',
           '영업상태구분코드', '영업상태명', '상세영업상태코드', '상세영업상태명', '폐업일자', '휴업시작일자', '휴업종료일자',
           '재개업일자', '소재지전체주소', '도로명전체주소','사업장명', '최종수정시점', '데이터갱신일자','좌표정보(x)', '좌표정보(y)']

# Excel 파일을 읽어와서 데이터프레임 생성
for idx, csv_file in enumerate(csv_files, start=1):
    full_path = os.path.join(folder_path, csv_file)
    dataframe = pd.read_csv(full_path, encoding='CP949')
    dataframes[f'db{idx}'] = dataframe[varlist]
living_comdb_new = []
living_comdb_new = pd.concat(dataframes)

living_comdb_new.to_pickle('living_comdb_new.pkl')

print(living_comdb_new['인허가일자'].min())

##################################################################

## 상세 업종 필요하여 업종별 인파일
# 1. 일반음식점, 2. 휴게음식점, 3. 미용업, 4. 숙박업, 5. 병원, 6. 의원
job_0724_food_gnl = pd.read_csv('D:\\data\\생활업종_csv\\6440000_충청남도_07_24_04_P_일반음식점.csv', dtype=str, encoding='CP949' )
job_0724_food_semi = pd.read_csv('D:\\data\\생활업종_csv\\6440000_충청남도_07_24_05_P_휴게음식점.csv', dtype=str, encoding='CP949' )
job_0518_beauty = pd.read_csv('D:\\data\\생활업종_csv\\6440000_충청남도_05_18_01_P_미용업.csv', dtype=str, encoding='CP949' )
job_0311_hotel = pd.read_csv('D:\\data\\생활업종_csv\\6440000_충청남도_03_11_03_P_숙박업.csv', dtype=str, encoding='CP949' )
job_0101_hospi = pd.read_csv('D:\\data\\생활업종_csv\\6440000_충청남도_01_01_01_P_병원.csv', dtype=str, encoding='CP949' )
job_0101_clinic = pd.read_csv('D:\\data\\생활업종_csv\\6440000_충청남도_01_01_02_P_의원.csv', dtype=str, encoding='CP949' )

# 사업체 인허가 중복 체크 : 삼성전자(주) 고압가스업
job_0928_gas = pd.read_csv('D:\\data\\생활업종_csv\\6440000_충청남도_09_28_05_P_고압가스업.csv', dtype=str, encoding='CP949' )
job_0826_sales = pd.read_csv('D:\\data\\생활업종_csv\\6440000_충청남도_08_26_04_P_통신판매업.csv', dtype=str, encoding='CP949' )

##########################

## 전국 행정동 이름

addr_nm = pd.read_csv('D:\\data\\생활업종_기타\\전국행정동코드.csv',  dtype=str,  encoding='CP949' )

##########################

## BC카드 데이터

folder_path = 'D:\\data\\생활업종_BC카드'

# 폴더 내의 Excel 파일 목록 가져오기
csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]

# 데이터프레임을 담을 딕셔너리 초기화
dataframes = {}

# 파일을 읽어와서 데이터프레임 생성
for idx, csv_file in enumerate(csv_files, start=1):
    full_path = os.path.join(folder_path, csv_file)
    dataframe = pd.read_csv(full_path)
    dataframes[f'db{idx}'] = dataframe
living_card = []
living_card = pd.concat(dataframes)
living_card.to_pickle('living_card.pkl')

#####################################################################################

## 유동인구 데이터 : 데이터사이즈가 커서 연도별 작업

folder_path = 'D:\\data\\생활업종_유동인구_2023'

# 폴더 내의 Excel 파일 목록 가져오기
csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]

# 데이터프레임을 담을 딕셔너리 초기화
dataframes = {}

# 파일을 읽어와서 데이터프레임 생성
for idx, csv_file in enumerate(csv_files, start=1):
    full_path = os.path.join(folder_path, csv_file)
    dataframe = pd.read_csv(full_path, encoding='CP949')
    dataframes[f'db{idx}'] = dataframe
living_skt = []
living_skt = pd.concat(dataframes)
living_skt.to_pickle('living_skt_2023.pkl')



######

folder_path = 'D:\\data\\생활업종_유동인구_2019'

# 폴더 내의 Excel 파일 목록 가져오기
csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]

# 데이터프레임을 담을 딕셔너리 초기화
dataframes = {}

# 파일을 읽어와서 데이터프레임 생성
for idx, csv_file in enumerate(csv_files, start=1):
    full_path = os.path.join(folder_path, csv_file)
    dataframe = pd.read_csv(full_path, encoding='CP949')
    dataframes[f'db{idx}'] = dataframe
living_skt = []
living_skt = pd.concat(dataframes)
living_skt.to_pickle('living_skt_2019.pkl')

##  2020

folder_path = 'D:\\data\\생활업종_유동인구_2020'

# 폴더 내의 Excel 파일 목록 가져오기
csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]

# 데이터프레임을 담을 딕셔너리 초기화
dataframes = {}

# 파일을 읽어와서 데이터프레임 생성
for idx, csv_file in enumerate(csv_files, start=1):
    full_path = os.path.join(folder_path, csv_file)
    dataframe = pd.read_csv(full_path, encoding='CP949')
    dataframes[f'db{idx}'] = dataframe
living_skt = []
living_skt = pd.concat(dataframes)
living_skt.to_pickle('living_skt_2020.pkl')

##  2021

folder_path = 'D:\\data\\생활업종_유동인구_2021'

# 폴더 내의 Excel 파일 목록 가져오기
csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]

# 데이터프레임을 담을 딕셔너리 초기화
dataframes = {}

# 파일을 읽어와서 데이터프레임 생성
for idx, csv_file in enumerate(csv_files, start=1):
    full_path = os.path.join(folder_path, csv_file)
    dataframe = pd.read_csv(full_path, encoding='CP949')
    dataframes[f'db{idx}'] = dataframe
living_skt = []
living_skt = pd.concat(dataframes)
living_skt.to_pickle('living_skt_2021.pkl')

##  2022

folder_path = 'D:\\data\\생활업종_유동인구_2022'

# 폴더 내의 Excel 파일 목록 가져오기
csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]

# 데이터프레임을 담을 딕셔너리 초기화
dataframes = {}

# 파일을 읽어와서 데이터프레임 생성
for idx, csv_file in enumerate(csv_files, start=1):
    full_path = os.path.join(folder_path, csv_file)
    dataframe = pd.read_csv(full_path, encoding='CP949')
    dataframes[f'db{idx}'] = dataframe
living_skt = []
living_skt = pd.concat(dataframes)
living_skt.to_pickle('living_skt_2022.pkl')


#####################################################

## KCB 데이터 : 법정동 맵핑을 위해 행안부 10자리 표준 법정동코드 데이터 적용

folder_path = 'D:\\data\\생활업종_kcb'

# 폴더 내의 Excel 파일 목록 가져오기
csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]

# 데이터프레임을 담을 딕셔너리 초기화
dataframes = {}

# 파일을 읽어와서 데이터프레임 생성
for idx, csv_file in enumerate(csv_files, start=1):
    full_path = os.path.join(folder_path, csv_file)
    dataframe = pd.read_csv(full_path, encoding='CP949')
    dataframes[f'db{idx}'] = dataframe
living_kcb = []
living_kcb = pd.concat(dataframes)
living_kcb.to_pickle('living_kcb.pkl')

col_list = pd.DataFrame(living_kcb.columns)
col_list.to_excel('d:\\out\\아산시_D1205_kcb데이터칼럼.xlsx')

list_kcb = ['癤풠RTR_YM','STDG_CD','AGE_DVS','NOPE','ML_NOPE','FM_NOPE','SLR_NOPE','S_OWNR_NOPE','ETC_NOPE','FRGNR_NOPE',
           'MM_INCM','CARD_OWRN_NOPE','CARD_GRAMT_AVG','LON_OWNR_NOPE','CR_LON_OWNR_NOPE','HOUSE_LON_OWRN_NOPE',
            'PLC_LON_OWRN_NOPE','LON_AVG_BLC','CR_LON_AVG_BLC','HOUSE_LON_AVG_BLC']
living_kcb2 = living_kcb[list_kcb]
living_kcb2.columns =['CRTR_YM','STDG_CD','AGE_DVS','NOPE','ML_NOPE','FM_NOPE','SLR_NOPE','S_OWNR_NOPE','ETC_NOPE','FRGNR_NOPE',
           'MM_INCM','CARD_OWRN_NOPE','CARD_GRAMT_AVG','LON_OWNR_NOPE','CR_LON_OWNR_NOPE','HOUSE_LON_OWRN_NOPE',
            'PLC_LON_OWRN_NOPE','LON_AVG_BLC','CR_LON_AVG_BLC','HOUSE_LON_AVG_BLC']

living_kcb2['incm_nope'] = living_kcb2['SLR_NOPE'] + living_kcb2['S_OWNR_NOPE'] + living_kcb2['ETC_NOPE']
living_kcb2['incm_sum'] = living_kcb2['MM_INCM']*living_kcb2['incm_nope']
living_kcb2['card_usesum'] = living_kcb2['CARD_GRAMT_AVG']*living_kcb2['CARD_OWRN_NOPE']
living_kcb2['lon_sum'] = living_kcb2['LON_AVG_BLC']*living_kcb2['LON_OWNR_NOPE']
living_kcb2['crlon_sum'] = living_kcb2['CR_LON_AVG_BLC']*living_kcb2['CR_LON_OWNR_NOPE']
living_kcb2['houselon_sum'] = living_kcb2['HOUSE_LON_AVG_BLC']*living_kcb2['HOUSE_LON_OWRN_NOPE']
living_kcb2['dong'] = living_kcb2['STDG_CD'].astype('str').str[:8]

living_kcb3 = living_kcb2[['CRTR_YM','dong','AGE_DVS','NOPE','ML_NOPE','FM_NOPE','SLR_NOPE','S_OWNR_NOPE','ETC_NOPE','FRGNR_NOPE',
                'CARD_OWRN_NOPE', 'LON_OWNR_NOPE','CR_LON_OWNR_NOPE','HOUSE_LON_OWRN_NOPE', 'PLC_LON_OWRN_NOPE',
                'incm_nope', 'incm_sum', 'card_usesum', 'lon_sum', 'crlon_sum', 'houselon_sum' ]]

living_kcb4 = living_kcb3.groupby(['CRTR_YM','dong','AGE_DVS']).sum().reset_index()
living_kcb4.to_pickle('living_kcb4.pkl')

#####################################################

## Tmap 데이터 :

folder_path = 'D:\\data\\생활업종_TMAP'

# 폴더 내의 Excel 파일 목록 가져오기
csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]

# 데이터프레임을 담을 딕셔너리 초기화
dataframes = {}

# 파일을 읽어와서 데이터프레임 생성
for idx, csv_file in enumerate(csv_files, start=1):
    full_path = os.path.join(folder_path, csv_file)
    dataframe = pd.read_csv(full_path)
    dataframes[f'db{idx}'] = dataframe
living_tmap = []
living_tmap = pd.concat(dataframes)
living_tmap.columns
# 법정동 주소 생성 : 목적지 주소에서 법정동 추출 (행정동 정보는 데이터에 포함되어 있음)
living_tmap['STDG_NM'] = living_tmap['dstn_addr'].str.split(' ').str[2]
living_tmap.to_pickle('living_tmap.pkl')

#####################################################################

## 행정동 경계 GIS 데이터 불러오기 : 소스 - 국가공간정보포털 오픈마켓  http://data.nsdi.go.kr/dataset/20171206ds00001
##  파일명 : (센서스경계) 법정동경계 Z_SOP_BND_ADM_DONG_PG.zip   : 해당폴더에 압축파일 5개 모두 있어야 함
##  행정동과 법정동이 다르기 때문에 각각 받아야 함

import geopandas as gpd

sensus = gpd.read_file('D:\\data\\생활업종_기타\\법정동\\LSMD_ADM_SECT_UMD_44_202312.shp',encoding='cp949')

## 아산시만 추출 후 시흥시 경계면 저장
asan = sensus[sensus['COL_ADM_SE'].str.startswith('4420')]   # 아산시 지역코드, 전국 법정동 코드 파일 참조

## 아산시에 해당하는 경계면 맵핑

## SKT 유동인구 데이터에 법정동 정보 추가

skt_2022 = pd.read_pickle('living_skt_2022.pkl')

## 좌표계 정보만 추출
skt_point = skt_2022.groupby(['COORD_X', 'COORD_Y']).size().reset_index()
skt_point = skt_point[['COORD_X', 'COORD_Y']]

## GEOMETRY 정보 생성
geometry = [Point(xy) for xy in zip(skt_point['COORD_X'], skt_point['COORD_Y'])]

# 새로운 'geometry' 컬럼을 생성합니다.
skt_point['geometry'] = geometry

# 좌표계를 정의합니다. 여기서는 WGS84 좌표계를 사용하겠습니다. (임의의 좌표계 지정)
crs = {'init': 'epsg:4326'}

# geometry 컬럼을 기반으로 GeoDataFrame을 생성합니다.
skt_point = gpd.GeoDataFrame(skt_point, crs=crs, geometry=geometry)

#### 두개 파일의 geometry 정보 통일

asan = asan.to_crs(skt_point.crs)

#### geometry 기준 조인
skt_point = gpd.sjoin(skt_point, asan,  how='left')

skt_point =  skt_point[['COORD_X', 'COORD_Y', 'EMD_NM']]
skt_point.to_pickle('skt_point_asan.pkl')

###############################################################################################################


living_comdb2 = living_comdb_new[(living_comdb_new['소재지전체주소'].str[:8] == '충청남도 아산시')|(living_comdb_new['도로명전체주소'].str[:8] == '충청남도 아산시')]
living_comdb2.to_pickle('living_comdb2.pkl')

## 업종, 영업상태 분포

comdb = living_comdb2

st_cate = comdb.groupby(['개방서비스명']).size().reset_index()
st_cate.to_excel('d:\\out\\아산시_D1101_업종.xlsx')

comdb.groupby(['영업상태명']).size().reset_index()



## 인파일 누락데이터 체크
living_comdb = pd.read_pickle('living_comdb.pkl')
st_cate = living_comdb.groupby(['개방서비스명']).size().reset_index()
st_cate.to_excel('d:\\out\\아산시_D1107_업종전체.xlsx')

comdb = living_comdb2

comdb.columns
comdb['인허가일자'].min()

## 업종 분류
comdb['cate_1'] = 'C_' + comdb['개방서비스아이디'].str[:2]
comdb['cate_2'] = 'C_' + comdb['개방서비스아이디'].str[:5]
comdb['yn'] = 1

comdb = pd.merge(comdb, industry_lv1, how = 'left', on = 'cate_1' )
comdb = pd.merge(comdb, industry_lv2, how = 'left', on = 'cate_2' )


st_cate1 = comdb.groupby(['catenm_1']).size().reset_index()
st_cate2 = comdb.groupby(['catenm_1', 'catenm_2']).size().reset_index()

industry_lv1.columns = ['cate_1', 'catenm_1']
industry_lv2.columns = ['cate_2', 'catenm_2']

st_cate1 = pd.merge(st_cate1, industry_lv1, how = 'left', on = 'cate_1' )
st_cate2 = pd.merge(st_cate2, industry_lv2, how = 'left', on = 'cate_2' )

st_stat2 =  comdb.groupby(['catenm_1', 'catenm_2', '개방서비스명', '개방서비스아이디'])['yn'].sum().reset_index()

st_cate1.to_excel('d:\\out\\아산시_D1107_업종카테고리_대분류.xlsx')
st_cate2.to_excel('d:\\out\\아산시_D1107_업종카테고리_중분류.xlsx')
st_stat2.to_excel('d:\\out\\아산시_D1121_업종카테고리_아이디.xlsx')


###################################################################################

####  데이터 전처리 : 분석데이터 생성  ####

###################################################################################

## 인허가 데이터 --> 생활업종 추출하여 분석정보 생성(업태 필요한 업종은 별도 인파일)

# 일반음식점
job_0724_food_gnl['job_cate'] = ''
job_0724_food_gnl['job_cate'] = np.where(job_0724_food_gnl['업태구분명'] == '냉면집', '한식', job_0724_food_gnl['job_cate'])
job_0724_food_gnl['job_cate'] = np.where(job_0724_food_gnl['업태구분명'] == '복어취급', '한식', job_0724_food_gnl['job_cate'])
job_0724_food_gnl['job_cate'] = np.where(job_0724_food_gnl['업태구분명'] == '뷔페식', '한식', job_0724_food_gnl['job_cate'])
job_0724_food_gnl['job_cate'] = np.where(job_0724_food_gnl['업태구분명'] == '식육(숯불구이)', '한식', job_0724_food_gnl['job_cate'])
job_0724_food_gnl['job_cate'] = np.where(job_0724_food_gnl['업태구분명'] == '출장조리', '한식', job_0724_food_gnl['job_cate'])
job_0724_food_gnl['job_cate'] = np.where(job_0724_food_gnl['업태구분명'] == '탕류(보신용)', '한식', job_0724_food_gnl['job_cate'])
job_0724_food_gnl['job_cate'] = np.where(job_0724_food_gnl['업태구분명'] == '한식', '한식', job_0724_food_gnl['job_cate'])
job_0724_food_gnl['job_cate'] = np.where(job_0724_food_gnl['업태구분명'] == '중국식', '중식', job_0724_food_gnl['job_cate'])
job_0724_food_gnl['job_cate'] = np.where(job_0724_food_gnl['업태구분명'] == '일식', '일식', job_0724_food_gnl['job_cate'])
job_0724_food_gnl['job_cate'] = np.where(job_0724_food_gnl['업태구분명'] == '횟집', '일식', job_0724_food_gnl['job_cate'])
job_0724_food_gnl['job_cate'] = np.where(job_0724_food_gnl['업태구분명'] == '김밥(도시락)', '분식', job_0724_food_gnl['job_cate'])
job_0724_food_gnl['job_cate'] = np.where(job_0724_food_gnl['업태구분명'] == '분식', '분식', job_0724_food_gnl['job_cate'])
job_0724_food_gnl['job_cate'] = np.where(job_0724_food_gnl['업태구분명'] == '경양식', '서양식', job_0724_food_gnl['job_cate'])
job_0724_food_gnl['job_cate'] = np.where(job_0724_food_gnl['업태구분명'] == '패밀리레스트랑', '서양식', job_0724_food_gnl['job_cate'])
job_0724_food_gnl['job_cate'] = np.where(job_0724_food_gnl['업태구분명'] == '패스트푸드', '패스트푸드', job_0724_food_gnl['job_cate'])
job_0724_food_gnl['job_cate'] = np.where(job_0724_food_gnl['업태구분명'] == '이동조리', '패스트푸드', job_0724_food_gnl['job_cate'])
job_0724_food_gnl['job_cate'] = np.where(job_0724_food_gnl['업태구분명'] == '기타', '패스트푸드', job_0724_food_gnl['job_cate'])
job_0724_food_gnl['job_cate'] = np.where(job_0724_food_gnl['업태구분명'] == '통닭(치킨)', '치킨', job_0724_food_gnl['job_cate'])
job_0724_food_gnl['job_cate'] = np.where(job_0724_food_gnl['업태구분명'] == '감성주점', '호프및간이주점', job_0724_food_gnl['job_cate'])
job_0724_food_gnl['job_cate'] = np.where(job_0724_food_gnl['업태구분명'] == '정종/대포집/소주방', '호프및간이주점', job_0724_food_gnl['job_cate'])
job_0724_food_gnl['job_cate'] = np.where(job_0724_food_gnl['업태구분명'] == '호프/통닭', '호프및간이주점', job_0724_food_gnl['job_cate'])
job_0724_food_gnl['job_cate'] = np.where(job_0724_food_gnl['업태구분명'] == '까페', '카페', job_0724_food_gnl['job_cate'])
job_0724_food_gnl['job_cate'] = np.where(job_0724_food_gnl['업태구분명'] == '라이브카페', '카페', job_0724_food_gnl['job_cate'])
job_0724_food_gnl['job_cate'] = np.where(job_0724_food_gnl['업태구분명'] == '전통찻집', '카페', job_0724_food_gnl['job_cate'])
job_0724_food_gnl['job_cate'] = np.where(job_0724_food_gnl['업태구분명'] == '커피숍', '카페', job_0724_food_gnl['job_cate'])
job_0724_food_gnl['job_cate'] = np.where(job_0724_food_gnl['업태구분명'] == '키즈카페', '카페', job_0724_food_gnl['job_cate'])
job_0724_food_gnl['job_cate'] = np.where(job_0724_food_gnl['업태구분명'] == '외국음식전문점(인도,태국등)', '기타외국식', job_0724_food_gnl['job_cate'])

# 간이음식점

job_0724_food_semi['job_cate'] = ''
job_0724_food_semi['job_cate'] = np.where(job_0724_food_semi['업태구분명'] == '과자점', '제과점', job_0724_food_semi['job_cate'])
job_0724_food_semi['job_cate'] = np.where(job_0724_food_semi['업태구분명'] == '고속도로', '패스트푸드', job_0724_food_semi['job_cate'])
job_0724_food_semi['job_cate'] = np.where(job_0724_food_semi['업태구분명'] == '관광호텔', '패스트푸드', job_0724_food_semi['job_cate'])
job_0724_food_semi['job_cate'] = np.where(job_0724_food_semi['업태구분명'] == '극장', '패스트푸드', job_0724_food_semi['job_cate'])
job_0724_food_semi['job_cate'] = np.where(job_0724_food_semi['업태구분명'] == '기타 휴게음식점', '패스트푸드', job_0724_food_semi['job_cate'])
job_0724_food_semi['job_cate'] = np.where(job_0724_food_semi['업태구분명'] == '백화점', '패스트푸드', job_0724_food_semi['job_cate'])
job_0724_food_semi['job_cate'] = np.where(job_0724_food_semi['업태구분명'] == '아이스크림', '패스트푸드', job_0724_food_semi['job_cate'])
job_0724_food_semi['job_cate'] = np.where(job_0724_food_semi['업태구분명'] == '유원지', '패스트푸드', job_0724_food_semi['job_cate'])
job_0724_food_semi['job_cate'] = np.where(job_0724_food_semi['업태구분명'] == '일반조리판매', '패스트푸드', job_0724_food_semi['job_cate'])
job_0724_food_semi['job_cate'] = np.where(job_0724_food_semi['업태구분명'] == '철도역구내', '패스트푸드', job_0724_food_semi['job_cate'])
job_0724_food_semi['job_cate'] = np.where(job_0724_food_semi['업태구분명'] == '패스트푸드', '패스트푸드', job_0724_food_semi['job_cate'])
job_0724_food_semi['job_cate'] = np.where(job_0724_food_semi['업태구분명'] == '푸드트럭', '패스트푸드', job_0724_food_semi['job_cate'])
job_0724_food_semi['job_cate'] = np.where(job_0724_food_semi['업태구분명'] == '한식', '패스트푸드', job_0724_food_semi['job_cate'])
job_0724_food_semi['job_cate'] = np.where(job_0724_food_semi['업태구분명'] == '다방', '카페', job_0724_food_semi['job_cate'])
job_0724_food_semi['job_cate'] = np.where(job_0724_food_semi['업태구분명'] == '떡카페', '카페', job_0724_food_semi['job_cate'])
job_0724_food_semi['job_cate'] = np.where(job_0724_food_semi['업태구분명'] == '전통찻집', '카페', job_0724_food_semi['job_cate'])
job_0724_food_semi['job_cate'] = np.where(job_0724_food_semi['업태구분명'] == '커피숍', '카페', job_0724_food_semi['job_cate'])
job_0724_food_semi['job_cate'] = np.where(job_0724_food_semi['업태구분명'] == '키즈카페', '카페', job_0724_food_semi['job_cate'])
job_0724_food_semi['job_cate'] = np.where(job_0724_food_semi['업태구분명'] == '편의점', '편의점', job_0724_food_semi['job_cate'])

# 미용업

job_0518_beauty['job_cate'] = ''
job_0518_beauty['job_cate'] = np.where(job_0518_beauty['업태구분명'] == '일반미용업', '미용실', job_0518_beauty['job_cate'])
job_0518_beauty['job_cate'] = np.where(job_0518_beauty['업태구분명'] == '일반이용업', '미용실', job_0518_beauty['job_cate'])
job_0518_beauty['job_cate'] = np.where(job_0518_beauty['업태구분명'] == '미용업기타', '미용실', job_0518_beauty['job_cate'])
job_0518_beauty['job_cate'] = np.where(job_0518_beauty['업태구분명'] == '기타', '미용실', job_0518_beauty['job_cate'])
job_0518_beauty['job_cate'] = np.where(job_0518_beauty['업태구분명'] == '피부미용업', '피부/미용', job_0518_beauty['job_cate'])
job_0518_beauty['job_cate'] = np.where(job_0518_beauty['업태구분명'] == '메이크업업', '피부/미용', job_0518_beauty['job_cate'])
job_0518_beauty['job_cate'] = np.where(job_0518_beauty['업태구분명'] == '네일아트업', '피부/미용', job_0518_beauty['job_cate'])

# 숙박업

job_0311_hotel['job_cate'] = ''
job_0311_hotel['job_cate'] = np.where(job_0311_hotel['업태구분명'] == '일반호텔', '호텔', job_0311_hotel['job_cate'])
job_0311_hotel['job_cate'] = np.where(job_0311_hotel['업태구분명'] == '관광호텔', '호텔', job_0311_hotel['job_cate'])
job_0311_hotel['job_cate'] = np.where(job_0311_hotel['업태구분명'] == '휴양콘도미니엄업', '호텔', job_0311_hotel['job_cate'])
job_0311_hotel['job_cate'] = np.where(job_0311_hotel['업태구분명'] == '여관업', '여관', job_0311_hotel['job_cate'])
job_0311_hotel['job_cate'] = np.where(job_0311_hotel['업태구분명'] == '여인숙업', '여관', job_0311_hotel['job_cate'])
job_0311_hotel['job_cate'] = np.where(job_0311_hotel['업태구분명'] == '숙박업(생활)', '여관', job_0311_hotel['job_cate'])
job_0311_hotel['job_cate'] = np.where(job_0311_hotel['업태구분명'] == '숙박업 기타', '여관', job_0311_hotel['job_cate'])

# 병원
job_0101_hospi['job_cate'] = np.where(job_0101_hospi['업태구분명'] == '한방병원', '한방병원', '병원')

# 의원
job_0101_clinic['job_cate'] = np.where(job_0101_clinic['업태구분명'] == '한의원', '한방병원', '병원')

## 분석항목 추출
varlist2 = ['번호', '개방서비스명', '개방서비스아이디', '개방자치단체코드', '관리번호', '인허가일자', '인허가취소일자',
           '영업상태구분코드', '영업상태명', '상세영업상태코드', '상세영업상태명', '폐업일자', '휴업시작일자', '휴업종료일자',
           '재개업일자', '소재지전체주소', '도로명전체주소','사업장명', '최종수정시점', '데이터갱신일자','좌표정보(x)', '좌표정보(y)', 'job_cate' ]

job_0724_food_gnl = job_0724_food_gnl[varlist2]
job_0724_food_semi = job_0724_food_semi[varlist2]
job_0518_beauty = job_0518_beauty[varlist2]
job_0311_hotel = job_0311_hotel[varlist2]
job_0101_hospi = job_0101_hospi[varlist2]
job_0101_clinic = job_0101_clinic[varlist2]

living_add =  pd.concat([job_0724_food_gnl,job_0724_food_semi,job_0518_beauty,job_0311_hotel,job_0101_hospi,job_0101_clinic ] , axis=0)

living_add['job_area'] = ''
living_add['job_area'] = np.where(living_add['job_cate'] == '호텔', '숙박', living_add['job_area'])
living_add['job_area'] = np.where(living_add['job_cate'] == '기타외국식', '음식', living_add['job_area'])
living_add['job_area'] = np.where(living_add['job_cate'] == '미용실', '생활서비스', living_add['job_area'])
living_add['job_area'] = np.where(living_add['job_cate'] == '병원', '의료', living_add['job_area'])
living_add['job_area'] = np.where(living_add['job_cate'] == '분식', '음식', living_add['job_area'])
living_add['job_area'] = np.where(living_add['job_cate'] == '서양식', '음식', living_add['job_area'])
living_add['job_area'] = np.where(living_add['job_cate'] == '여관', '숙박', living_add['job_area'])
living_add['job_area'] = np.where(living_add['job_cate'] == '일식', '음식', living_add['job_area'])
living_add['job_area'] = np.where(living_add['job_cate'] == '제과점', '음식', living_add['job_area'])
living_add['job_area'] = np.where(living_add['job_cate'] == '중식', '음식', living_add['job_area'])
living_add['job_area'] = np.where(living_add['job_cate'] == '치킨', '음식', living_add['job_area'])
living_add['job_area'] = np.where(living_add['job_cate'] == '카페', '음식', living_add['job_area'])
living_add['job_area'] = np.where(living_add['job_cate'] == '패스트푸드', '음식', living_add['job_area'])
living_add['job_area'] = np.where(living_add['job_cate'] == '편의점', '소매업', living_add['job_area'])
living_add['job_area'] = np.where(living_add['job_cate'] == '피부/미용', '생활서비스', living_add['job_area'])
living_add['job_area'] = np.where(living_add['job_cate'] == '한방병원', '의료', living_add['job_area'])
living_add['job_area'] = np.where(living_add['job_cate'] == '한식', '음식', living_add['job_area'])
living_add['job_area'] = np.where(living_add['job_cate'] == '호텔', '숙박', living_add['job_area'])
living_add['job_area'] = np.where(living_add['job_cate'] == '호프및간이주점', '음식', living_add['job_area'])

living_add = living_add[living_add['job_cate'] != '']

living_add.groupby(['job_area', 'job_cate']).size().reset_index()


##############################################

## 지자체인허가 업종으로 생활업종 생성

living_comdb['job_cate'] = ''

# 주유소 : 석유판매업, 석유및석유대체연료판매업체 로 수정
living_comdb['job_cate'] = np.where(living_comdb['개방서비스명'] == '석유판매업', '주유소', living_comdb['job_cate'])
living_comdb['job_cate'] = np.where(living_comdb['개방서비스명'] == '석유및석유대체연료판매업체', '주유소', living_comdb['job_cate'])

# 통신판매
living_comdb['job_cate'] = np.where(living_comdb['개방서비스명'] == '통신판매업', '통신판매', living_comdb['job_cate'])

# 목욕탕
living_comdb['job_cate'] = np.where(living_comdb['개방서비스명'] == '목욕장업', '목욕탕', living_comdb['job_cate'])

# 이발소
living_comdb['job_cate'] = np.where(living_comdb['개방서비스명'] == '이용업', '이발소', living_comdb['job_cate'])

# 세탁소
living_comdb['job_cate'] = np.where(living_comdb['개방서비스명'] == '세탁업', '세탁소', living_comdb['job_cate'])

# 호텔  - 관광숙박업
living_comdb['job_cate'] = np.where(living_comdb['개방서비스명'] == '관광숙박업', '호텔', living_comdb['job_cate'])

# 펜션/민박  - 관광숙박업
living_comdb['job_cate'] = np.where(living_comdb['개방서비스명'] == '농어촌민박업', '펜션/민박', living_comdb['job_cate'])
living_comdb['job_cate'] = np.where(living_comdb['개방서비스명'] == '한옥체험업', '펜션/민박', living_comdb['job_cate'])
living_comdb['job_cate'] = np.where(living_comdb['개방서비스명'] == '외국인관광도시민박업', '펜션/민박', living_comdb['job_cate'])
living_comdb['job_cate'] = np.where(living_comdb['개방서비스명'] == '일반야영장업', '펜션/민박', living_comdb['job_cate'])

# PC방
living_comdb['job_cate'] = np.where(living_comdb['개방서비스명'] == '인터넷컴퓨터게임시설제공업', 'PC방', living_comdb['job_cate'])

# 노래방
living_comdb['job_cate'] = np.where(living_comdb['개방서비스명'] == '노래연습장업', '노래방', living_comdb['job_cate'])

# 극장/영화관
living_comdb['job_cate'] = np.where(living_comdb['개방서비스명'] == '영화상영관', '극장/영화관', living_comdb['job_cate'])
living_comdb['job_cate'] = np.where(living_comdb['개방서비스명'] == '영화상영업', '극장/영화관', living_comdb['job_cate'])

# 도서관/박물관
living_comdb['job_cate'] = np.where(living_comdb['개방서비스명'] == '박물관, 미술관', '도서관/박물관', living_comdb['job_cate'])

# 생활체육시설
living_comdb['job_cate'] = np.where(living_comdb['개방서비스명'] == '골프연습장업', '생활체육시설', living_comdb['job_cate'])
living_comdb['job_cate'] = np.where(living_comdb['개방서비스명'] == '골프장', '생활체육시설', living_comdb['job_cate'])
living_comdb['job_cate'] = np.where(living_comdb['개방서비스명'] == '등록체육시설업', '생활체육시설', living_comdb['job_cate'])
living_comdb['job_cate'] = np.where(living_comdb['개방서비스명'] == '당구장업', '생활체육시설', living_comdb['job_cate'])
living_comdb['job_cate'] = np.where(living_comdb['개방서비스명'] == '무도학원업', '생활체육시설', living_comdb['job_cate'])
living_comdb['job_cate'] = np.where(living_comdb['개방서비스명'] == '무도장업', '생활체육시설', living_comdb['job_cate'])
living_comdb['job_cate'] = np.where(living_comdb['개방서비스명'] == '빙상장업', '생활체육시설', living_comdb['job_cate'])
living_comdb['job_cate'] = np.where(living_comdb['개방서비스명'] == '수영장업', '생활체육시설', living_comdb['job_cate'])
living_comdb['job_cate'] = np.where(living_comdb['개방서비스명'] == '승마장업', '생활체육시설', living_comdb['job_cate'])
living_comdb['job_cate'] = np.where(living_comdb['개방서비스명'] == '썰매장업', '생활체육시설', living_comdb['job_cate'])
living_comdb['job_cate'] = np.where(living_comdb['개방서비스명'] == '체력단련장업', '생활체육시설', living_comdb['job_cate'])
living_comdb['job_cate'] = np.where(living_comdb['개방서비스명'] == '체육도장업', '생활체육시설', living_comdb['job_cate'])
living_comdb['job_cate'] = np.where(living_comdb['개방서비스명'] == '종합체육시설업', '생활체육시설', living_comdb['job_cate'])

# 여행사
living_comdb['job_cate'] = np.where(living_comdb['개방서비스명'] == '국내여행업', '여행사', living_comdb['job_cate'])
living_comdb['job_cate'] = np.where(living_comdb['개방서비스명'] == '국내외여행업', '여행사', living_comdb['job_cate'])
living_comdb['job_cate'] = np.where(living_comdb['개방서비스명'] == '종합여행업', '여행사', living_comdb['job_cate'])

# 약국
living_comdb['job_cate'] = np.where(living_comdb['개방서비스명'] == '약국', '약국', living_comdb['job_cate'])

# 기타의료업
living_comdb['job_cate'] = np.where(living_comdb['개방서비스명'] == '의료법인', '기타의료업', living_comdb['job_cate'])
living_comdb['job_cate'] = np.where(living_comdb['개방서비스명'] == '의료유사업', '기타의료업', living_comdb['job_cate'])
living_comdb['job_cate'] = np.where(living_comdb['개방서비스명'] == '부속의료기관', '기타의료업', living_comdb['job_cate'])
living_comdb['job_cate'] = np.where(living_comdb['개방서비스명'] == '산후조리업', '기타의료업', living_comdb['job_cate'])
living_comdb['job_cate'] = np.where(living_comdb['개방서비스명'] == '응급환자이송업', '기타의료업', living_comdb['job_cate'])

# 동물병원
living_comdb['job_cate'] = np.where(living_comdb['개방서비스명'] == '동물병원', '동물병원', living_comdb['job_cate'])

## 업종 대분류 생성
living_comdb['job_area'] = ''
living_comdb['job_area'] = np.where(living_comdb['job_cate'] == 'PC방', '여가생활', living_comdb['job_area'])
living_comdb['job_area'] = np.where(living_comdb['job_cate'] == '극장/영화관', '여가생활', living_comdb['job_area'])
living_comdb['job_area'] = np.where(living_comdb['job_cate'] == '기타의료업', '의료', living_comdb['job_area'])
living_comdb['job_area'] = np.where(living_comdb['job_cate'] == '노래방', '여가생활', living_comdb['job_area'])
living_comdb['job_area'] = np.where(living_comdb['job_cate'] == '도서관/박물관', '여가생활', living_comdb['job_area'])
living_comdb['job_area'] = np.where(living_comdb['job_cate'] == '동물병원', '의료', living_comdb['job_area'])
living_comdb['job_area'] = np.where(living_comdb['job_cate'] == '목욕탕', '생활서비스', living_comdb['job_area'])
living_comdb['job_area'] = np.where(living_comdb['job_cate'] == '생활체육시설', '여가생활', living_comdb['job_area'])
living_comdb['job_area'] = np.where(living_comdb['job_cate'] == '세탁소', '생활서비스', living_comdb['job_area'])
living_comdb['job_area'] = np.where(living_comdb['job_cate'] == '약국', '의료', living_comdb['job_area'])
living_comdb['job_area'] = np.where(living_comdb['job_cate'] == '여행사', '여가생활', living_comdb['job_area'])
living_comdb['job_area'] = np.where(living_comdb['job_cate'] == '이발소', '생활서비스', living_comdb['job_area'])
living_comdb['job_area'] = np.where(living_comdb['job_cate'] == '주유소', '소매업', living_comdb['job_area'])
living_comdb['job_area'] = np.where(living_comdb['job_cate'] == '통신판매', '소매업', living_comdb['job_area'])
living_comdb['job_area'] = np.where(living_comdb['job_cate'] == '펜션/민박', '숙박', living_comdb['job_area'])
living_comdb['job_area'] = np.where(living_comdb['job_cate'] == '호텔', '숙박', living_comdb['job_area'])

#### 업종데이터 전체 합치기
living_comdb2 = living_comdb[living_comdb['job_cate'] != '']

living_com = pd.concat([living_comdb2, living_add] , axis=0)

living_com.groupby(['job_area', 'job_cate']).size().reset_index()

living_com = living_com[(living_com['소재지전체주소'].str[:8] == '충청남도 아산시')|(living_com['도로명전체주소'].str[:8] == '충청남도 아산시')]

## 업종 맵핑결과 최종 테이블 생성

living_com.to_pickle('living_com.pkl')

