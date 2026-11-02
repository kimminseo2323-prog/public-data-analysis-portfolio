###########################################################
# 과 제 명: A28_수원시_주차장수요공급분석
# 파 일 명: 5. 추가분석 및 수정
# 작 성 자: 김민서
###########################################################

import os, importlib, warnings;
warnings.filterwarnings(action='ignore')
# DB 접속: 사내 모듈 사용 (비공개)  # 원본: from config import config_A28 as config;
# importlib.reload(config)
from utils import functions_utils as fu;
importlib.reload(fu)
from utils import functions_log as fl;
importlib.reload(fl)
# DB 접속: 사내 모듈 사용 (비공개)  # 원본: from utils import functions_lime as flime;
# importlib.reload(flime)
# DB 접속: 사내 모듈 사용 (비공개)  # 원본: from utils import functions_utils_db as fud;
# importlib.reload(fud)
# ==================================================================================================
# [0-1] log 기록 정의
log = fl.Logger(config.PATH_LOG, config.LOG_FILE_NM);
log.set_log_level("info")
log.info("0-1 log 기록 정의")

# ==================================================================================================
# [0-2] 실행 변수 정의
log.info("0.2.실행 변수 정의")
config_info = fu.f_get_config_info(config.config_run, config.ENV_DEV)

# ==================================================================================================
# [0-3] 실행 변수
log.info("0.3.실행 변수 추가");
fu.f_memory_check()
# 전역 변수 선언 부분
# config_info["TODAY"]           = "20230630"

# [분석 처리 시작]
fl.f_log_line("수요공급분석.py")

# 1.실행 변수 정의
log.info("1.실행 변수 정의")

#path_base = "2024-06-13"
path_data_out = os.path.join(config_info["PATH_DATA_COLLECT"], "01.외부")
path_data_in = os.path.join(config_info["PATH_DATA_COLLECT"], "02.내부")
path_data_analyze = os.path.join(config_info["PATH_DATA_ANALYZE"])
path_data_output = os.path.join(config_info["PATH_DATA_OUTPUT"])

path_database = os.path.join(config_info["PATH_DATA_OUTPUT_DATEBASE"])
path_pretreat = os.path.join(config_info["PATH_DATA_OUTPUT_PRETREAT"])
path_middle = os.path.join(config_info["PATH_DATA_OUTPUT_MIDDLE"])
path_result = os.path.join(config_info["PATH_DATA_OUTPUT_RESULT"])
PATH_RESULT3 = os.path.join(config_info["PATH_RESULT"],'QGIS_DATA')
###################################################################################################
import pandas as pd
import geopandas as gpd
import numpy as np
from scipy.stats import pearsonr
import re

# 경계면 데이터
base_cd_5179 = gpd.read_file(PATH_RESULT3 + '//경계면데이터//기초구역경계//기초구역경계.gpkg',driver='GPKG')
base_boundary = gpd.read_file(PATH_RESULT3 + '//경계면데이터//기초구역경계//기초구역경계(시군구,행정동매핑).gpkg')
sgg_hjd = gpd.read_file(PATH_RESULT3 + '//경계면데이터//행정동경계//시군구_행정동경계.gpkg',driver='GPKG')
sgg = gpd.read_file(PATH_RESULT3 + '//경계면데이터//시군구경계//시군구경계.gpkg',driver='GPKG')
car = pd.read_excel(path_data_in + '//2024-06-13//분석용 데이터//차량등록현황_202405//자동차 등록 현황.xlsx') #기존 등록차량데이터
minus_car = pd.read_excel(path_data_in + '//2024-09-30//자동차관리사업자(매매업) 주소지.xlsx') #제거대상

#차량등록대수 현황
pre_car = car.copy()
pre_car
pre_car['sgg_name'] = pre_car['등록주소'].str.extract(r' (\S+구)')
pre_car.to_excel(path_middle+'//수원시_수요_차량등록대수.xlsx',index=False)
pre_car = pre_car[['sgg_name','등록주소', '용도', '차종',]]


pre_car_pivot = pre_car.pivot_table(index=['sgg_name','등록주소', '용도'], columns='차종', aggfunc='size', fill_value=0).reset_index()
pre_car_pivot['합계'] = pre_car_pivot[['경형', '대형', '소형', '저상형', '중형']].sum(axis=1)
pre_car_pivot.groupby('sgg_name')['합계'].sum()#(568,327건 기타 8건)

#우편번호 프로그램 후
pre_car2 = pd.read_excel(path_middle+'//차량등록대수//차량등록대수(우편번호).xlsx')
pre_car2 = pre_car2[['우편번호','등록주소']]
pre_car2.drop_duplicates(inplace=True)
pre_car3 = pd.merge(pre_car_pivot,pre_car2[['등록주소','우편번호']],on='등록주소',how="left")
pre_car3 = pre_car3.rename(columns={'우편번호':'기초구역번호'})
pre_car3.groupby('sgg_name')['합계'].sum()#(568,327건 기타 8건)
pre_car3.isnull().sum()
pre_car4 = pre_car3.dropna()
pre_car4['기초구역번호'] = pre_car4['기초구역번호'].astype(int)
pre_car4['기초구역번호'] = pre_car4['기초구역번호'].astype(str)
#pre_car3.to_excel(path_middle + '//차량등록대수//차량등록대수_null존재.xlsx',index=False )

#제거대상 등록주소 제거
minus_car.rename(columns={'도로명주소':'등록주소'},inplace=True)
pre_car4[pre_car4['등록주소'] == '경기도 수원시 권선구 권선로 308-5']
removed_data = pre_car4[pre_car4['등록주소'].isin(minus_car['등록주소'])]
removed_sum = removed_data['합계'].sum()
removed_sum

pre_car4_1 = pre_car4[~pre_car4['등록주소'].isin(minus_car['등록주소'])]
pre_car4_1['합계'].sum()#(527,539건 )
remaining_sum = pre_car4_1['합계'].sum()
remaining_sum

pre_car4_1_geo = pd.merge(pre_car4_1,base_boundary,on='기초구역번호',how='left')
pre_car4_2 = pre_car4_1_geo[['SGG_NM','HJD_NM','기초구역번호', '용도', '경형', '대형', '소형', '저상형', '중형', '합계']]
pre_car5_1 = pre_car4_2.groupby(['SGG_NM','HJD_NM','기초구역번호', '용도'])[['경형', '대형', '소형', '저상형', '중형', '합계']].sum().reset_index()
pre_car5_1.to_excel(path_result + '//차량등록대수//차량등록대수_수정.xlsx',index=False )

#주차장 확보율 재산출
#기초구역별 차량등록대수 대비 주차장공급비율
base_car = pd.read_excel(path_result + "//차량등록대수//차량등록대수_수정.xlsx")
base_parkk = pd.read_excel(path_result + "//공급분석//수원시_기초구역별_주차장공급분석(구분).xlsx")

base_carr = base_car.groupby('기초구역번호')['합계'].sum().reset_index()
base_carr.columns = ['기초구역번호','총등록차량수']

base_result1 = pd.merge(base_parkk,base_carr,on='기초구역번호',how='left')
base_result1 = base_result1.fillna(0)

base_result1['주차장확보율'] = ((base_result1['총주차면수']/base_result1['총등록차량수'])*100).round(1)
base_result1['주차장확보율'].replace([np.inf, -np.inf], 0, inplace=True)
base_result1 = base_result1.fillna(0)
base_result1.columns


base_result1.to_pickle(path_middle + '//기초구역경계//기초구역경계_주차장확보율_수정.pkl')
base_result1.to_excel(path_result + '//주차장확보율//차량등록수_주차장공급비율_기초구역기준_수정.xlsx',index=False)
base_boundary['기초구역번호'] = base_boundary['기초구역번호'].astype(int)
base_result2 = pd.merge(base_boundary[['기초구역번호','geometry']],base_result1,on='기초구역번호',how='left')
base_result2 = base_result2[['기초구역번호',  'SGG_NM', 'HJD_CD', 'HJD_NM', '노상', '노외', '부설','총주차면수', '총등록차량수', '주차장확보율','geometry']]
base_result2 = gpd.GeoDataFrame(base_result2, geometry='geometry', crs='EPSG:5179')
base_result2.to_file(PATH_RESULT3 + '//주차장확보율//차량등록수_주차장공급비율_기초구역기준_수정.gpkg',driver='GPKG')



# PPT 수정작업 진행 부분
'''
-29p : 수원시 차량등록대수_자가용
-30p : 수원시 차량등록대수_영업용
-31p : 수원시 차량등록대수기준 주차장공급비율
-34p : 거주인구_주차장공급비율(총주차면수/거주인구)
-35p : 거주인구_주차장공급비율(등록차량대수/거주인구)
-36p : 거주인구_거주자주차장 공급비율
-87p : gis 기반 주차 체감지도 (시간대별 자동차 유입/유출 수량을 반영한 주차 체감지도 생성) // QGIS 
-89p : gis 기반 주차 체감지도 (시간대별 점수등 여유,양호,보통,부족,혼잡,심각 분류 진행)  // QGIS 
'''
#주차장 확보율 재산출
#기초구역별 차량등록대수 대비 주차장공급비율
base_car = pd.read_excel(path_result + "//차량등록대수//차량등록대수_수정.xlsx")
base_car['기초구역번호'] = base_car['기초구역번호'].astype(str)
# 자가용
pre_car4_geo_1 = base_car[base_car['용도'] == '자가용']
pre_car4_geo_1 = pre_car4_geo_1.groupby(['기초구역번호'])[['경형', '대형', '소형', '저상형', '중형', '합계']].sum().reset_index()
pre_car4_geo_1 = pd.merge(base_boundary,pre_car4_geo_1,on='기초구역번호',how='left')
pre_car4_geo_1 = pre_car4_geo_1.fillna(0)
pre_car4_geo_1 = gpd.GeoDataFrame(pre_car4_geo_1, geometry='geometry', crs='EPSG:5179')
pre_car4_geo_1.to_file(PATH_RESULT3 + '//차량등록대수//차량등록대수_자가용_수정.gpkg',driver='GPKG')

# 영업용
pre_car4_geo_2 = base_car[base_car['용도'] == '영업용']
pre_car4_geo_2 = pre_car4_geo_2.groupby(['기초구역번호'])[['경형', '대형', '소형', '저상형', '중형', '합계']].sum().reset_index()
pre_car4_geo_2 = pd.merge(base_boundary,pre_car4_geo_2,on='기초구역번호',how='left')
pre_car4_geo_2 = pre_car4_geo_2.fillna(0)
pre_car4_geo_2 = gpd.GeoDataFrame(pre_car4_geo_2, geometry='geometry', crs='EPSG:5179')
pre_car4_geo_2.to_file(PATH_RESULT3 + '//차량등록대수//차량등록대수_영업용_수정.gpkg',driver='GPKG')



#거주인구
base_cd_pop5179 = gpd.read_file(PATH_RESULT3 + '//거주인구//기초구역경계_거주인구.gpkg')
base_pop = base_cd_pop5179[['기초구역번호', '면적', 'area', 'population']]
base_pop['기초구역번호'] = base_pop['기초구역번호'].astype(str)
base_boundary['기초구역번호'] = base_boundary['기초구역번호'].astype(str)
base_pop_mer = pd.merge(base_boundary,base_pop,on='기초구역번호',how='left')
base_pop_mer2 = base_pop_mer[[ 'SGG_NM','HJD_CD', 'HJD_NM', '기초구역번호','population']]
base_pop_mer = base_pop_mer[[ 'SGG_NM','HJD_CD', 'HJD_NM', '기초구역번호','population','geometry']]
base_pop_mer['기초구역번호'] = base_pop_mer['기초구역번호'].astype(str)
base_pop_mer.columns = ['SGG_NM','HJD_CD','HJD_NM','기초구역번호','거주인구','geometry']

# 거주인구 대비 주차장 공급비율
base_result2['기초구역번호'] = base_result2['기초구역번호'].astype(str)
parking_r = pd.merge(base_result2,base_pop_mer,on=['SGG_NM','HJD_CD','HJD_NM','기초구역번호'],how='left')
parking_r['주차장공급비율(%)'] = ((parking_r['총주차면수'] / parking_r['거주인구'])*100).round(1)

parking_r

# 거주인구 대비 차량 대수 비율 계산
pre_car6 = base_car.groupby(['SGG_NM','HJD_NM','기초구역번호'])[['경형', '대형', '소형', '저상형', '중형', '합계']].sum().reset_index()
parking_r2 = pd.merge(parking_r,pre_car6,on=['SGG_NM','HJD_NM','기초구역번호'],how='left')
parking_r2 = parking_r2.fillna(0)
parking_r2['차량대수비율(%)'] = ((parking_r2['합계'] / parking_r2['거주인구'])*100).round(1)
parking_r2.replace([np.inf, -np.inf], np.nan, inplace=True)
parking_r2.fillna(0, inplace=True)

parking_r3 = parking_r2[['SGG_NM', 'HJD_CD', 'HJD_NM', '기초구역번호','거주인구','총등록차량수','총주차면수','주차장공급비율(%)', '차량대수비율(%)']]
parking_r3.to_excel(path_result + '//수요분석//거주인구대비분석_수정.xlsx',index=False )
parking_r2.rename(columns={'geometry_x':'geometry'},inplace=True)
parking_r2_geo = parking_r2[['SGG_NM', 'HJD_CD', 'HJD_NM', '기초구역번호','거주인구','총등록차량수','총주차면수','주차장공급비율(%)','차량대수비율(%)','geometry']]
parking_r2_geo = gpd.GeoDataFrame(parking_r2_geo, geometry='geometry', crs='EPSG:5179')
parking_r2_geo.to_file(PATH_RESULT3 + '//거주인구//거주인구대비분석_수정.gpkg',driver='GPKG')

correlation = parking_r2[['거주인구', '총등록차량수']].corr().iloc[0, 1]
print(f'거주인구와 등록차량 대수 간의 상관관계: {correlation:.2f}')



################################################# 행정동별 분석 ##########################################################

base_parkk = pd.read_excel(path_result + "//공급분석//수원시_기초구역별_주차장공급분석(구분).xlsx")
hjd_park = base_parkk.groupby('HJD_NM')['총주차면수'].sum().reset_index()
hjd_park.columns = ['행정동명','총주차면수']
sgg_hjd = gpd.read_file(PATH_RESULT3 + '//경계면데이터//행정동경계//시군구_행정동경계.gpkg',driver='GPKG')
sgg_hjd = pd.merge(sgg_hjd,hjd_park,on='행정동명',how='left')
sgg_hjd.columns
sgg_hjd = sgg_hjd[['시군구명', '행정동명', '행정동코드', '총주차면수', 'geometry']]

base_car = pd.read_excel(path_result + "//차량등록대수//차량등록대수_수정.xlsx")
base_carr = base_car.groupby('HJD_NM')['합계'].sum().reset_index()
base_carr.columns = ['행정동명','총등록차량수']

base_car_p = base_car[base_car['HJD_NM'] == '평동']
base_car_p.groupby('용도')['합계'].sum()
hjd_result1 = pd.merge(sgg_hjd,base_carr,on='행정동명',how='left')
hjd_result1 = hjd_result1.fillna(0)
total_registered_vehicles = hjd_result1['총등록차량수'].sum()
hjd_result1['등록차량비율'] = hjd_result1['총등록차량수'] / total_registered_vehicles
hjd_result = hjd_result1[['시군구명', '행정동명', '행정동코드', '총주차면수', '총등록차량수','등록차량비율']]
hjd_result.to_excel(path_result + '//차량등록대수//차량등록대수_행정동기준.xlsx',index=False )

hjd_result1['주차장확보율'] = ((hjd_result1['총주차면수']/hjd_result1['총등록차량수'])*100).round(1)
hjd_result1['주차장확보율'].replace([np.inf, -np.inf], 0, inplace=True)
hjd_result1 = hjd_result1.fillna(0)
hjd_result1.columns

hjd_result2 = hjd_result1[['시군구명', '행정동명', '행정동코드', '총주차면수', '총등록차량수', '주차장확보율','등록차량비율']]
hjd_result2.to_pickle(path_middle + '//행정동경계//행정동경계_주차장확보율.pkl')
hjd_result2.to_excel(path_result + '//주차장확보율//차량등록수_주차장공급비율_행정동기준.xlsx',index=False)

hjd_result3 = hjd_result1[['시군구명', '행정동명', '행정동코드', '총주차면수', '총등록차량수', '주차장확보율','등록차량비율', 'geometry']]
hjd_result3 = gpd.GeoDataFrame(hjd_result3, geometry='geometry', crs='EPSG:5179')

hjd_result3.to_file(PATH_RESULT3 + '//주차장확보율//차량등록수_주차장공급비율_행정동기준_수정.gpkg',driver='GPKG')


# 자가용
pre_car4_geo_1 = base_car[base_car['용도'] == '자가용']
pre_car4_geo_hjd = pre_car4_geo_1.groupby(['HJD_NM'])[['경형', '대형', '소형', '저상형', '중형', '합계']].sum().reset_index()
pre_car4_geo_hjd.rename(columns={'HJD_NM':'행정동명'},inplace=True)

pre_car4_geo_hjd.columns

pre_car4_geo_hjd = pd.merge(sgg_hjd,pre_car4_geo_hjd,on='행정동명',how='left')
pre_car4_geo_hjd = pre_car4_geo_hjd.fillna(0)
pre_car4_geo_hjd = gpd.GeoDataFrame(pre_car4_geo_hjd, geometry='geometry', crs='EPSG:5179')
pre_car4_geo_hjd_1 = pre_car4_geo_hjd[['시군구명', '행정동명', '행정동코드', '총주차면수', '경형', '대형', '소형', '저상형','중형', '합계']]
pre_car4_geo_hjd_1.to_excel(path_result + '//차량등록대수//차량등록대수_자가용_행정동기준.xlsx',index=False )
pre_car4_geo_hjd_2 = pre_car4_geo_hjd[['시군구명', '행정동명', '행정동코드', '총주차면수', '경형', '대형', '소형', '저상형','중형', '합계','geometry']]
pre_car4_geo_hjd_2.to_file(PATH_RESULT3 + '//차량등록대수//차량등록대수_자가용_행정동기준.gpkg',driver='GPKG')

# 영업용
pre_car4_geo_1 = base_car[base_car['용도'] == '영업용']
pre_car4_geo_hjd = pre_car4_geo_1.groupby(['HJD_NM'])[['경형', '대형', '소형', '저상형', '중형', '합계']].sum().reset_index()
pre_car4_geo_hjd.rename(columns={'HJD_NM':'행정동명'},inplace=True)

pre_car4_geo_hjd.columns

pre_car4_geo_hjd = pd.merge(sgg_hjd,pre_car4_geo_hjd,on='행정동명',how='left')
pre_car4_geo_hjd = pre_car4_geo_hjd.fillna(0)
pre_car4_geo_hjd = gpd.GeoDataFrame(pre_car4_geo_hjd, geometry='geometry', crs='EPSG:5179')
pre_car4_geo_hjd_1 = pre_car4_geo_hjd[['시군구명', '행정동명', '행정동코드', '총주차면수', '경형', '대형', '소형', '저상형','중형', '합계']]
pre_car4_geo_hjd_1.to_excel(path_result + '//차량등록대수//차량등록대수_영업용_행정동기준.xlsx',index=False )
pre_car4_geo_hjd_2 = pre_car4_geo_hjd[['시군구명', '행정동명', '행정동코드', '총주차면수', '경형', '대형', '소형', '저상형','중형', '합계','geometry']]
pre_car4_geo_hjd_2.to_file(PATH_RESULT3 + '//차량등록대수//차량등록대수_영업용_행정동기준.gpkg',driver='GPKG')


# 행정동별 거주인구 대비 주차장공급면수
#거주인구
hjd_base_pop = pd.merge(base_boundary,base_cd_pop5179,on='기초구역번호',how='left')
hjd_base_pop = hjd_base_pop[[ 'HJD_NM','population']]
hjd_pop = hjd_base_pop.groupby('HJD_NM')['population'].sum().reset_index()
hjd_pop.rename(columns={'HJD_NM':'행정동명','population':'거주인구'},inplace=True)
hjd_pop2 = pd.merge(sgg_hjd,hjd_pop,on='행정동명',how='left')
hjd_pop2['주차장공급비율(%)'] = ((hjd_pop2['총주차면수'] / hjd_pop2['거주인구'])*100).astype(int)
hjd_pop2 = hjd_pop2[['시군구명', '행정동명', '행정동코드', '총주차면수', '거주인구','주차장공급비율(%)', 'geometry']]
hjd_pop2

base_car_hjd = base_car.groupby('HJD_NM')['합계'].sum().reset_index()
base_car_hjd.rename(columns={'HJD_NM':'행정동명','합계':'총등록차량수'},inplace=True)
hjd_pop3 = pd.merge(hjd_pop2,base_car_hjd,on='행정동명',how='left')
hjd_pop3['차량대수비율(%)'] = ((hjd_pop3['총등록차량수'] / hjd_pop3['거주인구'])*100).astype(int)
hjd_pop3 = hjd_pop3[['시군구명', '행정동명', '행정동코드', '총주차면수', '거주인구','주차장공급비율(%)','총등록차량수','차량대수비율(%)', 'geometry']]


# 상관관계 분석
correlation = hjd_pop3[['거주인구', '총등록차량수']].corr().iloc[0, 1]
print(f'거주인구와 등록차량 대수 간의 상관관계: {correlation:.2f}')

#기초구역별 거주인구 및 거주자주차장 데이터 생성
parking_1 = pd.read_excel(path_result + '//공급분석//수원시_기초구역별_주차장공급분석(유형).xlsx')
parking_2 = pd.read_excel(path_result + '//주차장현황//최종_건축물대장주차장.xlsx')

parking_1_p = parking_1[['HJD_NM','거주자우선주차장_면수']]
parking_1_p = parking_1.groupby('HJD_NM')['거주자우선주차장_면수'].sum().reset_index()
parking_1_p.rename(columns={'HJD_NM':'행정동명'},inplace=True)


parking_2_p = parking_2[parking_2['주용도코드명'].isin(['공동주택', '단독주택'])]
parking_2_p = parking_2_p.groupby('행정동명')['총주차수'].sum().reset_index()
parking_2_p['총주차수'].sum()

parking_home = pd.merge(parking_1_p,parking_2_p,on='행정동명',how='left')
parking_home['총거주자주차장'] = parking_home['거주자우선주차장_면수'] + parking_home['총주차수']
parking_home2 = parking_home[['행정동명','총거주자주차장']]

hjd_pop4 = pd.merge(hjd_pop3,parking_home2,on='행정동명',how='left')
hjd_pop4['거주자주차장비율(%)'] = ((hjd_pop4['총거주자주차장']/hjd_pop4['거주인구'])*100).astype(int)

hjd_pop4_geo = hjd_pop4[['시군구명', '행정동명', '행정동코드', '거주인구', '총주차면수','총거주자주차장','총등록차량수','주차장공급비율(%)','차량대수비율(%)','거주자주차장비율(%)', 'geometry']]
hjd_pop5 = hjd_pop4[['시군구명', '행정동명', '행정동코드', '거주인구', '총주차면수','총거주자주차장','총등록차량수','주차장공급비율(%)','차량대수비율(%)','거주자주차장비율(%)']]
hjd_pop5.to_excel(path_result + '//수요분석//거주인구대비분석(행정동).xlsx',index=False)
hjd_pop4_geo.to_file(PATH_RESULT3+'//거주인구//거주인구대비분석(행정동).gpkg',driver='GPKG')



## 주차체감지도 작성 : 주차장 공급지수 + 시간대별
###################################################################################################
## 주차 체감지표 개발
###################################################################################################

##1. 유입/유출 좌표로 기초구역 ID 생성
move_id = pd.read_pickle(path_result + '//KT_인구//1.유동인구//최근한달유동인구_기초구역매핑.pkl')
move_id.columns
move_id_var = move_id[['HJD_NM', 'UTMK_X', 'UTMK_Y']]
move_id_dong = move_id[['HJD_NM']]
move_id_dong = move_id_dong.drop_duplicates()

## 행정동별 주차장 확보율
park_db = pd.read_pickle(path_middle + '//행정동경계//행정동경계_주차장확보율.pkl')
index_dong = pd.read_pickle(path_middle + '//주차체감지도//행정동분석//index_dong.pkl')

# 체감지표 분포도
aa31 = index_dong.groupby(['park_index_gr']).size().reset_index()
aa31.to_excel(path_middle + '//주차체감지도//행정동분석//D0923_체감지표현황.xlsx')

## 평일 아침 7시 혼잡도
aa32 = index_dong[(index_dong['TIME_CD'] == 7)&(index_dong['week_yn'] == '0')].groupby(['park_index_gr']).size().reset_index()
aa32.to_excel(path_middle + '//주차체감지도//행정동분석//D0923_체감지표현황_평일7시.xlsx')

## 평일 20시 혼잡도
aa34 = index_dong[(index_dong['TIME_CD'] == 20)&(index_dong['week_yn'] == '0')].groupby(['park_index_gr']).size().reset_index()
aa34.to_excel(path_middle + '//주차체감지도//행정동분석//D0923_체감지표현황_평일20시.xlsx')

## 평일 아침 12시 혼잡도
aa32 = index_dong[(index_dong['TIME_CD'] == 12)&(index_dong['week_yn'] == '0')].groupby(['park_index_gr']).size().reset_index()
aa32.to_excel(path_middle + '//주차체감지도//행정동분석//D0923_체감지표현황_평일12시.xlsx')

## index 7시, 12시

index_02_7h =  index_dong[(index_dong['TIME_CD'] == 7)&(index_dong['week_yn'] == '0')]
index_02_12h =  index_dong[(index_dong['TIME_CD'] == 12)&(index_dong['week_yn'] == '0')]
index_02_20h =  index_dong[(index_dong['TIME_CD'] == 20)&(index_dong['week_yn'] == '0')]

index_02_7h.to_pickle(path_middle + '//주차체감지도//행정동분석//행정동별주차체감지표_평일7시.pkl')
index_02_12h.to_pickle(path_middle + '//주차체감지도//행정동분석//행정동별주차체감지표_평일12시.pkl')
index_02_20h.to_pickle(path_middle + '//주차체감지도//행정동분석//행정동별주차체감지표_평일20시.pkl')


aa33 = index_02_20h.groupby(['index_group','index_name']).size().reset_index()
aa33.to_excel(path_middle + '//주차체감지도//행정동분석//D0923_체감지표등급_평일20시.xlsx')

aa34 = index_02_12h.groupby(['index_group','index_name']).size().reset_index()
aa34.to_excel(path_middle + '//주차체감지도//행정동분석//D0923_체감지표등급_평일12시.xlsx')





######################## 주차체감지도 ptt 시각화 자료 생성 ##########################
#기초구역데이터
base_cd_5179 = gpd.read_file(PATH_RESULT3 + '//경계면데이터//기초구역경계//기초구역경계.gpkg',driver='GPKG')
sgg_hjd = gpd.read_file(PATH_RESULT3 + '//경계면데이터//행정동경계//시군구_행정동경계.gpkg',driver='GPKG')

inandout_7 = pd.read_pickle(path_middle + '//주차체감지도//행정동분석//행정동별유입유출차이_7시.pkl')
inandout_12 = pd.read_pickle(path_middle + '//주차체감지도//행정동분석//행정동별유입유출차이_12시.pkl')

sgg_hjd_r = sgg_hjd.rename(columns={'행정동명':'HJD_NM'})
inandout_7r = pd.merge(inandout_7,sgg_hjd_r,on='HJD_NM',how='left')
inandout_12r = pd.merge(inandout_12,sgg_hjd_r,on='HJD_NM',how='left')

inandout_7r_geo = gpd.GeoDataFrame(inandout_7r, geometry='geometry', crs='EPSG:5179')
inandout_12r_geo = gpd.GeoDataFrame(inandout_12r, geometry='geometry', crs='EPSG:5179')
inandout_7r_geo.to_file(PATH_RESULT3 + '//주차체감지도//행정동분석//행정동별유입유출차이_7시_수정.gpkg',driver='GPKG')
inandout_12r_geo.to_file(PATH_RESULT3 + '//주차체감지도//행정동분석//행정동별유입유출차이_12시_수정.gpkg',driver='GPKG')


base_inandout_12 = pd.read_pickle(path_middle + '//주차체감지도//행정동분석//행정동별주차체감지표_평일12시.pkl')
base_inandout_20 = pd.read_pickle(path_middle + '//주차체감지도//행정동분석//행정동별주차체감지표_평일7시.pkl')
base_inandout_12.reset_index(drop=True, inplace=True)
base_inandout_20.reset_index(drop=True, inplace=True)
base_boundary.columns
base_inandout_12r = pd.merge(base_boundary,base_inandout_12,on='HJD_NM',how='left')
base_inandout_20r = pd.merge(base_boundary,base_inandout_20,on='HJD_NM',how='left')

base_inandout_12r.fillna(0,inplace=True)
base_inandout_20r.fillna(0,inplace=True)
base_inandout_12r_geo = gpd.GeoDataFrame(base_inandout_12r, geometry='geometry', crs='EPSG:5179')
base_inandout_20r_geo = gpd.GeoDataFrame(base_inandout_20r, geometry='geometry', crs='EPSG:5179')
base_inandout_12r_geo.to_file(PATH_RESULT3 + '//주차체감지도//행정동분석//행정동별유입유출차이_12시_수정.gpkg',driver='GPKG')
base_inandout_20r_geo.to_file(PATH_RESULT3 + '//주차체감지도//행정동분석//행정동별유입유출차이_20시_수정.gpkg',driver='GPKG')


######################## 전체데이터 ##########################
#주차제감등급
#주차제감지표
index_dong = pd.read_pickle(path_middle + '//주차체감지도//행정동분석//index_dong.pkl')
index_dong['week_yn'] = index_dong['week_yn'].astype('int')


weekday_data = index_dong[index_dong['week_yn'] == 0] #평일
weekend_data = index_dong[index_dong['week_yn'] == 1] #주말


#주차체감지표 구간설정
weekday_data['park_index_gr'] = weekday_data['park_index_gr'].astype('int')
weekend_data['park_index_gr'] = weekend_data['park_index_gr'].astype('int')

def add_park_index_gr2(df, col_name='park_index_gr'):
    # 조건에 맞는 구간 설정
    conditions = [
        (df[col_name] >= 0) & (df[col_name] < 50),
        (df[col_name] >= 50) & (df[col_name] < 60),
        (df[col_name] >= 60) & (df[col_name] < 70),
        (df[col_name] >= 70) & (df[col_name] < 80),
        (df[col_name] >= 80) & (df[col_name] < 90),
        (df[col_name] >= 90) & (df[col_name] < 100),
        (df[col_name] >= 100) & (df[col_name] < 110),
        (df[col_name] >= 110) & (df[col_name] < 120),
        (df[col_name] >= 120) & (df[col_name] < 130),
        (df[col_name] >= 130) & (df[col_name] < 140),
        (df[col_name] >= 140) & (df[col_name] < 150),
        (df[col_name] >= 150)
    ]

    # 각 조건에 대한 구간값 (문자열)
    choices = ['0-50', '50-60', '60-70', '70-80', '80-90', '90-100', '100-110', '110-120', '120-130', '130-140',
               '140-150', '150 이상']

    # np.select로 새로운 컬럼 생성
    df['park_index_gr2'] = np.select(conditions, choices, default='미분류')
    return df


# 함수 호출 예시
weekday_data = add_park_index_gr2(weekday_data)
weekend_data = add_park_index_gr2(weekend_data)

weekday_data.rename(columns = {'HJD_NM':'행정동명'}, inplace=True)
weekend_data.rename(columns = {'HJD_NM':'행정동명'}, inplace=True)

# 기초구역별 평일,주말 시간대별로 파일 저장
def save_time_based_files(data, filename_prefix):
    for hour in range(24):
        hour_data = data[data['TIME_CD'] == hour]
        hour_data  = pd.merge(sgg_hjd,hour_data,on='행정동명',how='left')
        hour_data_geo = gpd.GeoDataFrame(hour_data, geometry='geometry', crs='EPSG:5179')
        hour_data_geo.fillna(0, inplace=True)
        if not hour_data.empty:
            hour_data.to_file(PATH_RESULT3 + f'//주차체감지도//행정동분석//주차체감지표//{filename_prefix}//{filename_prefix}_{hour}시.gpkg',driver='GPKG')


save_time_based_files(weekday_data, '평일')
save_time_based_files(weekend_data, '주말')




#특정 시간대(7시, 12시, 20시)별, 주차체감 지수가 심각한 지역(행정동, 기초구역) TOP 10 도출
#기초구역
index_02_base = pd.read_pickle(path_middle + '//주차체감지도//index_02.pkl')
weekday_data_base = index_02_base[index_02_base['week_yn'] == 0] #평일
# 평일 7시
weekday_data_base_7 = weekday_data_base[weekday_data_base['TIME_CD'] == 7]
weekday_data_base_7.to_excel(path_result + '//주차체감지수//기초구역_주차체감지수_평일7시.xlsx',index=False)
# 평일 12시
weekday_data_base_12 = weekday_data_base[weekday_data_base['TIME_CD'] == 12]
weekday_data_base_12.to_excel(path_result + '//주차체감지수//기초구역_주차체감지수_평일12시.xlsx',index=False)
# 평일 20시
weekday_data_base_20 = weekday_data_base[weekday_data_base['TIME_CD'] == 20]
weekday_data_base_20.to_excel(path_result + '//주차체감지수//기초구역_주차체감지수_평일20시.xlsx',index=False)
index_02_base.to_excel(path_result + '//주차체감지수//기초구역별_평일주말_시간대별_주차체감지수.xlsx',index=False)

#행정동
index_02_hjd = pd.read_pickle(path_middle + '//주차체감지도//행정동분석//index_dong.pkl')
index_02_hjd['week_yn'] = index_02_hjd['week_yn'].astype('int')
weekday_data_hjd = index_02_hjd[index_02_hjd['week_yn'] == 0] #평일

# 평일 7시
weekday_data_hjd_7 = weekday_data_hjd[weekday_data_hjd['TIME_CD'] == 7]
weekday_data_hjd_7.to_excel(path_result + '//주차체감지수//행정동분석//행정동_주차체감지수_평일7시.xlsx',index=False)
# 평일 12시
weekday_data_hjd_12 = weekday_data_hjd[weekday_data_hjd['TIME_CD'] == 12]
weekday_data_hjd_12.to_excel(path_result + '//주차체감지수//행정동분석//행정동_주차체감지수_평일12시.xlsx',index=False)
# 평일 20시
weekday_data_hjd_20 = weekday_data_hjd[weekday_data_hjd['TIME_CD'] == 20]
weekday_data_hjd_20.to_excel(path_result + '//주차체감지수//행정동분석//행정동_주차체감지수_평일20시.xlsx',index=False)
index_02_hjd.to_excel(path_result + '//주차체감지수//행정동분석//행정동별_평일주말_시간대별_주차체감지수.xlsx',index=False)

# 기초구역기준 특정시간대별 체감지수 심각지역 top10 특성도출
weekday_data_base_7 = pd.read_excel(path_result + '//주차체감지수//기초구역_주차체감지수_평일7시.xlsx') # 7시,12시,20시 모두 동일

plus_suyo = pd.read_excel(path_result + '//수요분석//거주인구대비분석_수정.xlsx')
flowpop = gpd.read_file(PATH_RESULT3 + '//유동인구//기초구역경계_유동인구(최근한달).gpkg', driver='GPKG')
base_cd_5179['기초구역번호'] = base_cd_5179['기초구역번호'].astype(int)
flowpop['기초구역번호'] = flowpop['기초구역번호'].astype(int)

weekday_data_base_7.head()
top_10_base = weekday_data_base_7.sort_values(by='park_index').head(10)
top_10_base = top_10_base[['HJD_NM', '기초구역번호','park_index', 'index_name']]
top_10_base = pd.merge(top_10_base,plus_suyo[[ 'HJD_NM', '기초구역번호', '거주인구', '총등록차량수', '총주차면수','주차장공급비율(%)', '차량대수비율(%)']],on=['HJD_NM','기초구역번호'],how='left')
top_10_base = top_10_base.sort_values(by='기초구역번호')
top_10_base = pd.merge(top_10_base,flowpop[['기초구역번호','flowpop_sum']],on='기초구역번호',how='left')
top_10_base.rename(columns={'flowpop_sum':'최근한달_유동인구'},inplace=True)
top_10_base['최근한달_유동인구'] =top_10_base['최근한달_유동인구'].round(1)
top_10_base.to_excel(path_result + '//주차체감지수//기초구역기준_심각TOP10.xlsx',index=False)

top_10_base = pd.merge(top_10_base,base_cd_5179[['기초구역번호','geometry']],on='기초구역번호',how='left')
top_10_base = gpd.GeoDataFrame(top_10_base, geometry='geometry')
top_10_base.to_file(PATH_RESULT3 + '//주차체감지도//기초구역기준_심각TOP10.gpkg',driver='GPKG')

# 행정동기준 특정시간대별 체감지수 심각지역 top10 특성도출
weekday_data_hjd_7 = pd.read_excel(path_result + '//주차체감지수//행정동분석//행정동_주차체감지수_평일7시.xlsx')
weekday_data_hjd_12 = pd.read_excel(path_result + '//주차체감지수//행정동분석//행정동_주차체감지수_평일12시.xlsx')
weekday_data_hjd_20 = pd.read_excel(path_result + '//주차체감지수//행정동분석//행정동_주차체감지수_평일20시.xlsx')
sgg_hjd = gpd.read_file(PATH_RESULT3 + '//경계면데이터//행정동경계//시군구_행정동경계.gpkg',driver='GPKG')
plus_suyo_hjd = pd.read_excel(path_result + '//수요분석//거주인구대비분석(행정동).xlsx')

in_out_car_0_7 = gpd.read_file(PATH_RESULT3 + '//유입유출차량//평일//평일_7시.gpkg',driver='GPKG')
in_out_car_0_12 = gpd.read_file(PATH_RESULT3 + '//유입유출차량//평일//평일_12시.gpkg',driver='GPKG')
in_out_car_0_20 = gpd.read_file(PATH_RESULT3 + '//유입유출차량//평일//평일_20시.gpkg',driver='GPKG')

flowpop = gpd.read_file(PATH_RESULT3 + '//유동인구//기초구역경계_유동인구(최근한달).gpkg', driver='GPKG')
flowpop['기초구역번호'] = flowpop['기초구역번호'].astype(int)
flowpop_hjd = flowpop.groupby('HJD_NM')[['flowpop_sum']].sum().round(1).reset_index()
flowpop_hjd.rename(columns={'flowpop_sum':'최근한달_유동인구'},inplace=True)

top10_7_hjd = weekday_data_hjd_7.sort_values(by='park_index').head(10)
top10_12_hjd = weekday_data_hjd_12.sort_values(by='park_index').head(10)
top10_20_hjd = weekday_data_hjd_20.sort_values(by='park_index').head(10)

top10_7_hjd = top10_7_hjd[['HJD_NM','park_index', 'index_name']]
top10_12_hjd = top10_12_hjd[['HJD_NM','park_index', 'index_name']]
top10_20_hjd = top10_20_hjd[['HJD_NM','park_index', 'index_name']]

plus_suyo_hjd.rename(columns={'행정동명':'HJD_NM'},inplace=True)
top10_7_hjd = pd.merge(top10_7_hjd,plus_suyo_hjd[['HJD_NM', '거주인구', '총등록차량수', '총주차면수']],on='HJD_NM',how='left')
top10_12_hjd = pd.merge(top10_12_hjd,plus_suyo_hjd[['HJD_NM', '거주인구', '총등록차량수', '총주차면수']],on='HJD_NM',how='left')
top10_20_hjd = pd.merge(top10_20_hjd,plus_suyo_hjd[['HJD_NM', '거주인구', '총등록차량수', '총주차면수']],on='HJD_NM',how='left')

top10_7_hjd = pd.merge(top10_7_hjd,flowpop_hjd[['HJD_NM', '최근한달_유동인구']],on='HJD_NM',how='left')
top10_12_hjd = pd.merge(top10_12_hjd,flowpop_hjd[['HJD_NM', '최근한달_유동인구']],on='HJD_NM',how='left')
top10_20_hjd = pd.merge(top10_20_hjd,flowpop_hjd[['HJD_NM', '최근한달_유동인구']],on='HJD_NM',how='left')

top10_7_hjd.rename(columns={'HJD_NM':'행정동명'},inplace=True)
top10_12_hjd.rename(columns={'HJD_NM':'행정동명'},inplace=True)
top10_20_hjd.rename(columns={'HJD_NM':'행정동명'},inplace=True)

top10_7_hjd = pd.merge(top10_7_hjd,in_out_car_0_7[['행정동명', '차량유입인구','차량유출인구']],on='행정동명',how='left')
top10_12_hjd = pd.merge(top10_12_hjd,in_out_car_0_12[['행정동명', '차량유입인구','차량유출인구']],on='행정동명',how='left')
top10_20_hjd = pd.merge(top10_20_hjd,in_out_car_0_20[['행정동명', '차량유입인구','차량유출인구']],on='행정동명',how='left')

hjd_result3 = gpd.read_file(PATH_RESULT3 + '//주차장확보율//차량등록수_주차장공급비율_행정동기준_수정.gpkg',driver='GPKG')
top10_7_hjd = pd.merge(top10_7_hjd,hjd_result3[['행정동명', '주차장확보율']],on='행정동명',how='left')
top10_12_hjd = pd.merge(top10_12_hjd,hjd_result3[['행정동명', '주차장확보율']],on='행정동명',how='left')
top10_20_hjd = pd.merge(top10_20_hjd,hjd_result3[['행정동명', '주차장확보율']],on='행정동명',how='left')

top10_7_hjd.to_excel(path_result + '//주차체감지수//행정동분석//행정동기준_평일7시_심각TOP10.xlsx',index=False)
top10_12_hjd.to_excel(path_result + '//주차체감지수//행정동분석//행정동기준_평일12시_심각TOP10.xlsx',index=False)
top10_20_hjd.to_excel(path_result + '//주차체감지수//행정동분석//행정동기준_평일20시_심각TOP10.xlsx',index=False)

top10_7_hjd = pd.merge(top10_7_hjd,sgg_hjd[['행정동명','geometry']],on='행정동명',how='left')
top10_7_hjd = gpd.GeoDataFrame(top10_7_hjd, geometry='geometry')
top10_12_hjd = pd.merge(top10_12_hjd,sgg_hjd[['행정동명','geometry']],on='행정동명',how='left')
top10_12_hjd = gpd.GeoDataFrame(top10_12_hjd, geometry='geometry')
top10_20_hjd = pd.merge(top10_20_hjd,sgg_hjd[['행정동명','geometry']],on='행정동명',how='left')
top10_20_hjd = gpd.GeoDataFrame(top10_20_hjd, geometry='geometry')

top10_7_hjd.to_file(PATH_RESULT3 + '//주차체감지도//행정동기준_평일7시_심각TOP10.gpkg',driver='GPKG')
top10_12_hjd.to_file(PATH_RESULT3 + '//주차체감지도//행정동기준_평일12시_심각TOP10.gpkg',driver='GPKG')
top10_20_hjd.to_file(PATH_RESULT3 + '//주차체감지도//행정동기준_평일20시_심각TOP10.gpkg',driver='GPKG')


# 불법주정차 민원분석
## 원천데이터 자체를 지오코딩한 결과
bulbub_car_1geo = gpd.read_file(path_data_analyze + '//지오코딩//불법주정차//org//불법주정차 민원리스트(20230501~20240430)_WGS.shp',encoding='cp949')
bulbub_car_1geo = gpd.GeoDataFrame(bulbub_car_1geo, geometry='geometry', crs='EPSG:4326')
bulbub_car_1geo.to_crs(epsg=5179, inplace=True)
bulbub_car_1geo.to_file(path_data_analyze + '//지오코딩//불법주정차//org//org_5179.gpkg', driver='GPKG')
bulbub_car_1geo.to_excel(path_result +'//불법주정차//원천_지오코딩.xlsx',index=False)
#수원시 시군구 내의 매핑되는 불법민원주차장 정보
bul_org_map =  gpd.sjoin(bulbub_car_1geo, base_boundary, how="inner", op="within")
#bul_org_map #5714개중 1270개

bulbub_car = pd.read_excel(path_data_in + '//2024-06-11//불법주정차 민원리스트(20230501~20240430).xlsx')
# 정규 표현식을 사용하여 괄호 포함 뒤의 내용 삭제
bulbub_car['address_cleaned'] = bulbub_car['위치'].apply(lambda x: re.sub(r'\(.*\)', '', x).strip())
bulbub_car['address_cleaned2'] = bulbub_car['address_cleaned'].apply(lambda x: re.sub(r'^[^가-힣0-9]+|^\d+\.\s*', '', x).strip())
bulbub_car['address_cleaned3'] = bulbub_car['address_cleaned2'].apply(lambda x: re.sub(r'^\[위치\]\s*', '', x).strip())
bulbub_car.to_excel(path_data_analyze + '//지오코딩//불법주정차//pre//1차_pre.xlsx',index=False)

bulbub_car_2geo = gpd.read_file(path_data_analyze + '//지오코딩//불법주정차//pre//1차_pre_WGS.shp',encoding='cp949')
bulbub_car_2geo = gpd.GeoDataFrame(bulbub_car_2geo, geometry='geometry', crs='EPSG:4326')
bulbub_car_2geo.to_crs(epsg=5179, inplace=True)
bulbub_car_2geo.to_file(path_data_analyze + '//지오코딩//불법주정차//pre//1차_pre_5179.gpkg', driver='GPKG')
#수원시 시군구 내의 매핑되는 불법민원주차장 정보의 1차 전처리 후 지오코딩 결과
bul_org_map2 =  gpd.sjoin(bulbub_car_2geo, base_boundary, how="inner", op="within")
#bul_org_map2 #5714개중 1,208개

#원천데이터와 전처리 데이터 매핑
bul_org_map_1 = bul_org_map[['번호', '접수일시', '제목', 'SGG_NM', 'HJD_NM','기초구역번호', 'geometry']]
bul_org_map2_1 = bul_org_map2[['번호', '접수일시', '제목', 'SGG_NM', 'HJD_NM','기초구역번호', 'geometry']]

only_in_A = bul_org_map_1.merge(bul_org_map2_1, how='outer', indicator=True).loc[lambda x: x['_merge'] == 'left_only']
only_in_B = bul_org_map_1.merge(bul_org_map2_1, how='outer', indicator=True).loc[lambda x: x['_merge'] == 'right_only']

only_in_A['번호'] = only_in_A['번호'].astype(int)
only_in_B['번호'] = only_in_B['번호'].astype(int)

only_in_A_1 = pd.merge(only_in_A,bulbub_car[['번호','위치','address_cleaned3']],on='번호',how='left')
only_in_B_1 = pd.merge(only_in_B,bulbub_car[['번호','위치','address_cleaned3']],on='번호',how='left')

combined_data = pd.concat([bul_org_map_1, bul_org_map2_1])
combined_data_unique = combined_data.drop_duplicates()
combined_data_unique.to_file(path_data_analyze + '//지오코딩//불법주정차//최종_불법민원주정차.gpkg', driver='GPKG')
combined_data_unique.to_file(PATH_RESULT3 + '//불법주정차//최종_불법민원주정차.gpkg', driver='GPKG')
########################################################################################################################
result_bulbub = gpd.read_file(path_data_analyze + '//지오코딩//불법주정차//최종_불법민원주정차.gpkg', driver='GPKG')
bulbub_car_hu = pd.read_excel(path_data_in + '//2024-06-11//불법주정차 민원리스트(20230501~20240430)_지오코딩결과.xlsx')
result_bulbub['번호'] = result_bulbub['번호'].astype(int)
result_bulbub_x = result_bulbub[['번호', '접수일시', '제목', 'SGG_NM', 'HJD_NM', '기초구역번호']]
result_bulbub_x['번호'] = result_bulbub_x['번호'].astype(int)
result_bulbub_x = pd.merge(result_bulbub_x,bulbub_car_hu[['번호','위치','CLSS']],on='번호',how='left')
result_bulbub_x.to_excel(path_result + '//불법주정차//불법민원주정차_위치.xlsx')
result_bulbub_x['CLSS'].value_counts()
result_bulbub_o = result_bulbub_x[result_bulbub_x['CLSS'] == '정좌표']
result_bulbub_o = result_bulbub_o[['번호', '접수일시']]
result_bulbub_o = pd.merge(result_bulbub_o,result_bulbub,on=['번호', '접수일시'],how='left')
result_bulbub_o = result_bulbub_o.drop_duplicates()
result_bulbub_o = gpd.GeoDataFrame(result_bulbub_o, geometry='geometry', crs='EPSG:5179')
result_bulbub_o.to_file(PATH_RESULT3 + '//불법주정차//최종_불법민원주정차_정좌표.gpkg', driver='GPKG')
########################################################################################################################
base_boundary = gpd.read_file(PATH_RESULT3 + '//경계면데이터//기초구역경계//기초구역경계(시군구,행정동매핑).gpkg')
sgg_hjd = gpd.read_file(PATH_RESULT3 + '//경계면데이터//행정동경계//시군구_행정동경계.gpkg',driver='GPKG')
result_bulbub_o.rename(columns={'HJD_NM':'행정동명'},inplace=True)

result_bulbub_base = result_bulbub_o.groupby(['행정동명','기초구역번호']).size().reset_index(name='민원발생수')
result_bulbub_base = pd.merge(result_bulbub_base,base_boundary[['기초구역번호','geometry']],on='기초구역번호',how='left')
result_bulbub_base = gpd.GeoDataFrame(result_bulbub_base, geometry='geometry')
result_bulbub_base.to_file(PATH_RESULT3 + '//불법주정차//기초구역기준_민원발생수.gpkg', driver='GPKG')
result_bulbub_base.to_excel(path_result + '//불법주정차//기초구역기준_민원발생수.xlsx',index=False)

result_bulbub_hjd = result_bulbub_o.groupby('행정동명').size().reset_index(name='민원발생수')
result_bulbub_hjd = pd.merge(result_bulbub_hjd,sgg_hjd[['행정동명','geometry']],on='행정동명',how='left')
result_bulbub_hjd = gpd.GeoDataFrame(result_bulbub_hjd, geometry='geometry')
result_bulbub_hjd.to_file(PATH_RESULT3 + '//불법주정차//행정동기준_민원발생수.gpkg', driver='GPKG')
result_bulbub_hjd.to_excel(path_result + '//불법주정차//행정동기준_민원발생수.xlsx',index=False)
########################################################################################################################

flowpop = gpd.read_file(PATH_RESULT3 + '//유동인구//기초구역경계_유동인구(최근한달).gpkg', driver='GPKG')
flowpop['기초구역번호'] = flowpop['기초구역번호'].astype(int)
flowpop_hjd = flowpop.groupby('HJD_NM')[['flowpop_sum']].sum().round(1).reset_index() #행정동
flowpop_hjd.rename(columns={'flowpop_sum':'최근한달_유동인구'},inplace=True)
flowpop_1 = flowpop[['기초구역번호','flowpop_sum']] #기초구역
flowpop_1.rename(columns={'flowpop_sum':'최근한달_유동인구'},inplace=True)
#----------------------------------------------------------------------------------------------------- 기초구역
result_bulbub_base = pd.read_excel(path_result + '//불법주정차//기초구역기준_민원발생수.xlsx')
plus_suyo = pd.read_excel(path_result + '//수요분석//거주인구대비분석_수정.xlsx')
plus_suyo_1 = plus_suyo[['기초구역번호','총주차면수','총등록차량수','거주인구']]
result_bulbub_base = pd.merge(result_bulbub_base,plus_suyo_1,on='기초구역번호',how = 'left')
result_bulbub_base = pd.merge(result_bulbub_base,flowpop_1,on='기초구역번호',how = 'left')

result_bulbub_10_base = result_bulbub_base.sort_values(by='민원발생수', ascending=False).head(10).reset_index(drop =True)
result_bulbub_10_base.to_excel(path_result + '//불법주정차//기초구역기준top10.xlsx',index=False)
result_bulbub_base = result_bulbub_base[['행정동명', '기초구역번호', '민원발생수', '총주차면수', '총등록차량수', '거주인구','최근한달_유동인구']]
df = pd.DataFrame(result_bulbub_base) # 기초구역기준
# 기초구역번호를 제외하고 상관관계 분석
correlation_matrix_excluding_id = df.drop(columns=['행정동명','기초구역번호']).corr()
# 민원발생수와 다른 컬럼들의 상관계수 추출
correlation_with_complaints_excluding_id = correlation_matrix_excluding_id['민원발생수'].drop('민원발생수')

# 결과를 txt 파일로 저장
file_path = path_result + '//불법주정차//기초구역기준_상관분석결과.txt'
with open(file_path, 'w') as file:
    file.write(correlation_with_complaints_excluding_id.to_string())
print(f"결과가 {file_path}로 저장되었습니다.")
#-----------------------------------------------------------------------------------------------------
result_bulbub_hjd = pd.read_excel(path_result + '//불법주정차//행정동기준_민원발생수.xlsx')
plus_suyo_hjd = pd.read_excel(path_result + '//수요분석//거주인구대비분석(행정동).xlsx')

plus_suyo_hjd = plus_suyo_hjd[[ '행정동명','총주차면수','총등록차량수','거주인구']]
result_bulbub_hjd = pd.merge(result_bulbub_hjd,plus_suyo_hjd ,on='행정동명',how = 'left')
flowpop_hjd.rename(columns={'HJD_NM':'행정동명'},inplace=True)
result_bulbub_hjd = pd.merge(result_bulbub_hjd,flowpop_hjd,on='행정동명',how = 'left')

result_bulbub_hjd_10 = result_bulbub_hjd.sort_values(by='민원발생수', ascending=False).head(10).reset_index(drop =True)

result_bulbub_hjd_10.to_excel(path_result + '//불법주정차//행정동기준top10.xlsx',index=False)
result_bulbub_hjd = result_bulbub_hjd[['행정동명', '민원발생수', '총주차면수', '총등록차량수', '거주인구', '최근한달_유동인구']]
df = pd.DataFrame(result_bulbub_hjd) # 행정동기준
# 행정동명을 제외하고 상관관계 분석
correlation_matrix_excluding_id = df.drop(columns=['행정동명']).corr()
# 민원발생수와 다른 컬럼들의 상관계수 추출
correlation_with_complaints_excluding_id = correlation_matrix_excluding_id['민원발생수'].drop('민원발생수')

# 결과를 txt 파일로 저장
file_path = path_result + '//불법주정차//행정동기준_상관분석결과.txt'
with open(file_path, 'w') as file:
    file.write(correlation_with_complaints_excluding_id.to_string())
print(f"결과가 {file_path}로 저장되었습니다.")


########################################################################################################################
base_park = pd.read_excel(path_result + '//주차장확보율//차량등록수_주차장공급비율_기초구역기준_수정.xlsx')
clu = gpd.read_file(PATH_RESULT3 + '//배후지역클러스터링//cluster5_new2.gpkg')

clu.columns
clu = clu[['기초구역번호','그룹']]
base_park = base_park[['기초구역번호','총주차면수','총등록차량수']]
clu['기초구역번호'] = clu['기초구역번호'].astype(int)
clu2 = pd.merge(clu,base_park,on='기초구역번호',how='left')
clu2 = clu2.groupby(['그룹'])[['총주차면수','총등록차량수']].sum().reset_index()
clu2['주차장확보율'] = ((clu2['총주차면수']/clu2['총등록차량수'])*100).round(1)
clu2.to_excel(path_result + '//주차장확보율//클러스터링별_주차장확보율.xlsx',index=False)









