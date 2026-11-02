###########################################################
# 과 제 명: A28_수원시_주차장수요공급분석
# 파 일 명: 4.배후지역 세분화
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
#기초구역데이터
base_cd_5179 = gpd.read_file(PATH_RESULT3 + '//경계면데이터//기초구역경계//기초구역경계.gpkg',driver='GPKG')
sgg_hjd = gpd.read_file(PATH_RESULT3 + '//경계면데이터//행정동경계//시군구_행정동경계.gpkg',driver='GPKG')
#배후지역 세분화 데이터
seg_data = pd.read_pickle(path_pretreat + '//배후지역세분화//seg_info (2).pkl')
seg_data
seg_data.info()
seg_data.nunique()

seg_data.describe()
seg_data.fillna(0.0, inplace=True)
seg_data.columns

#교차표
pd.crosstab(seg_data["Cluster_4"], seg_data["Cluster_4"], margins=True)

'''
# Cluster_4컬럼의 값별로 나머지 변수의 평균값 계산
cluster_column4 = 'Cluster_4'
variables = ['V_SUM_h0', 'V_SUM_h14', 'H_SUM_h0', 'H_SUM_h14',
       'W_SUM_h0', 'W_SUM_h14', '거주인구_h0', '거주인구_h14', '기초구역면적', '연면적합계',
       '연면적주택', '건축물수', '건물평균연면적', '카드금액', '생활인구_h0', '생활인구_h14', '직장방문비율_h14',
       '건물면적비율', '주택비율', '생활인구비율_h14']

# 클러스터별 평균값 계산
cluster4_means = seg_data.groupby(cluster_column4)[variables].mean()
cluster4_means


seg_data_c4 = seg_data.groupby(['기초구역번호','Cluster_4'])[variables].mean().reset_index()
seg_data_c4_geo = pd.merge(base_cd_5179,seg_data_c4,on='기초구역번호',how='left')
seg_data_c4_geo = gpd.GeoDataFrame(seg_data_c4_geo, geometry='geometry')
seg_data_c4_geo.to_file(PATH_RESULT3 + '//배후지역클러스터링//cluster4.gpkg', driver='GPKG')
seg_data_c4_geo.columns
'''
# Cluster_5컬럼의 값별로 나머지 변수의 평균값 계산
cluster_column5 = 'Cluster_5'
variables = [ 'V_SUM_h0', 'V_SUM_h14', 'H_SUM_h0', 'H_SUM_h14',
       'W_SUM_h0', 'W_SUM_h14', '거주인구_h0', '거주인구_h14', '기초구역면적', '연면적합계',
       '연면적주택', '건축물수', '건물평균연면적', '카드금액', '생활인구_h0', '생활인구_h14', '직장방문비율_h14',
       '건물면적비율', '주택비율', '생활인구비율_h14']

# 클러스터별 평균값 계산
cluster5_means = seg_data.groupby(cluster_column5)[variables].mean()
cluster5_means

seg_data_c5 = seg_data.groupby(['기초구역번호','Cluster_5'])[variables].mean().reset_index()
seg_data_c5_geo = pd.merge(base_cd_5179,seg_data_c5,on='기초구역번호',how='left')
seg_data_c5_geo = gpd.GeoDataFrame(seg_data_c5_geo, geometry='geometry')
seg_data_c5_geo.to_file(PATH_RESULT3 + '//배후지역클러스터링//cluster5_new.gpkg', driver='GPKG')


# Cluster_5컬럼의 값별로 나머지 변수의 평균값 계산
cluster_column5 = 'Cluster_5'
variables = [ 'V_SUM_h0', 'V_SUM_h14', 'H_SUM_h0', 'H_SUM_h14',
       'W_SUM_h0', 'W_SUM_h14', '거주인구_h0', '거주인구_h14', '기초구역면적', '연면적합계',
       '연면적주택', '건축물수', '건물평균연면적', '카드금액', '생활인구_h0', '생활인구_h14', '직장방문비율_h14',
       '건물면적비율', '주택비율', '생활인구비율_h14']

# 클러스터별 평균값 계산
cluster5_means = seg_data.groupby(cluster_column5)[variables].mean()
cluster5_means

seg_data_c5 = seg_data.groupby(['기초구역번호','Cluster_5'])[variables].mean().reset_index()
seg_data_c5_geo = pd.merge(base_cd_5179,seg_data_c5,on='기초구역번호',how='left')
seg_data_c5_geo = gpd.GeoDataFrame(seg_data_c5_geo, geometry='geometry')
seg_data_c5_geo.to_file(PATH_RESULT3 + '//배후지역클러스터링//cluster5_new2.gpkg', driver='GPKG')

seg_data_c5_geo = gpd.read_file(PATH_RESULT3 + '//배후지역클러스터링//cluster5_new2.gpkg', driver='GPKG')
seg_data_c5_geo['Cluster_5'].value_counts()
mapping = {
    4: '1',
    1: '2',
    3: '3',
    0: '4',
    2: '5',
    9: '6'
}
seg_data_c5_geo['그룹'] = seg_data_c5_geo['Cluster_5'].map(mapping)
seg_data_c5_geo.to_file(PATH_RESULT3 + '//배후지역클러스터링//cluster5_new2.gpkg', driver='GPKG')
'''
seg_data_c6.columns
# Cluster_6 컬럼의 값별로 나머지 변수의 평균값 계산
cluster_column6 = 'Cluster_6'
variables = ['V_SUM_h0', 'V_SUM_h14', 'H_SUM_h0', 'H_SUM_h14',
       'W_SUM_h0', 'W_SUM_h14', '거주인구_h0', '거주인구_h14', '기초구역면적', '연면적합계',
       '연면적주택', '건축물수', '건물평균연면적', '카드금액', '생활인구_h0', '생활인구_h14', '직장방문비율_h14',
       '건물면적비율', '주택비율', '생활인구비율_h14']
# 클러스터별 평균값 계산
cluster6_means = seg_data.groupby(cluster_column6)[variables].mean()
cluster6_means

seg_data_c6 = seg_data.groupby(['기초구역번호','Cluster_6'])[variables].mean().reset_index()


seg_data_c6_geo = pd.merge(base_cd_5179,seg_data_c6,on='기초구역번호',how='left')
seg_data_c6_geo = gpd.GeoDataFrame(seg_data_c6_geo, geometry='geometry')
seg_data_c6_geo.to_file(PATH_RESULT3 + '//배후지역클러스터링//cluster6.gpkg', driver='GPKG')

'''
######################## 주차체감지도 ptt 시각화 자료 생성 ##########################

inandout_7 = pd.read_pickle(path_result + '//KT_인구//3.유입유출인구//행정동별유입유출차이_7시.pkl')
inandout_12 = pd.read_pickle(path_result + '//KT_인구//3.유입유출인구//행정동별유입유출차이_12시.pkl')

sgg_hjd_r = sgg_hjd.rename(columns={'행정동명':'HJD_NM'})
inandout_7r = pd.merge(inandout_7,sgg_hjd_r,on='HJD_NM',how='left')
inandout_12r = pd.merge(inandout_12,sgg_hjd_r,on='HJD_NM',how='left')

inandout_7r_geo = gpd.GeoDataFrame(inandout_7r, geometry='geometry', crs='EPSG:5179')
inandout_12r_geo = gpd.GeoDataFrame(inandout_12r, geometry='geometry', crs='EPSG:5179')
inandout_7r_geo.to_file(PATH_RESULT3 + '//주차체감지도//행정동별유입유출차이_7시.gpkg',driver='GPKG')
inandout_12r_geo.to_file(PATH_RESULT3 + '//주차체감지도//행정동별유입유출차이_12시.gpkg',driver='GPKG')


base_inandout_12 = pd.read_pickle(path_result + '//KT_인구//3.유입유출인구//기초구역별주차체감지표_평일12시.pkl')
base_inandout_20 = pd.read_pickle(path_result + '//KT_인구//3.유입유출인구//기초구역별주차체감지표_평일7시.pkl')
base_inandout_12.reset_index(drop=True, inplace=True)
base_inandout_20.reset_index(drop=True, inplace=True)

base_inandout_12r = pd.merge(base_cd_5179,base_inandout_12,on='기초구역번호',how='left')
base_inandout_20r = pd.merge(base_cd_5179,base_inandout_20,on='기초구역번호',how='left')

base_inandout_12r.fillna(0,inplace=True)
base_inandout_20r.fillna(0,inplace=True)
base_inandout_12r_geo = gpd.GeoDataFrame(base_inandout_12r, geometry='geometry', crs='EPSG:5179')
base_inandout_20r_geo = gpd.GeoDataFrame(base_inandout_20r, geometry='geometry', crs='EPSG:5179')
base_inandout_12r_geo.to_file(PATH_RESULT3 + '//주차체감지도//기초구역별유입유출차이_12시.gpkg',driver='GPKG')
base_inandout_20r_geo.to_file(PATH_RESULT3 + '//주차체감지도//기초구역별유입유출차이_20시.gpkg',driver='GPKG')


######################## 전체데이터 ##########################
#주차제감등급
#주차제감지표
# 기초구역별 유입유출차이 (평일,주말 따로 시간대별로 시각화하기) 총 48개 시각화결과 나와야함 평일 0~23시, 주말 0~23시
index_02 = pd.read_pickle(path_result + '//KT_인구//3.유입유출인구//index_02.pkl')
index_02.columns
index_02['week_yn'] = index_02['week_yn'].astype('int')


weekday_data = index_02[index_02['week_yn'] == 0] #평일
weekend_data = index_02[index_02['week_yn'] == 1] #주말


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


# 기초구역별 평일,주말 시간대별로 파일 저장
def save_time_based_files(data, filename_prefix):
    for hour in range(24):
        hour_data = data[data['TIME_CD'] == hour]
        hour_data  = pd.merge(base_cd_5179,hour_data,on='기초구역번호',how='left')
        hour_data_geo = gpd.GeoDataFrame(hour_data, geometry='geometry', crs='EPSG:5179')
        hour_data_geo.fillna(0, inplace=True)
        if not hour_data.empty:
            hour_data.to_file(PATH_RESULT3 + f'//주차체감지도//주차체감지표//{filename_prefix}//{filename_prefix}_{hour}시.gpkg',driver='GPKG')

save_time_based_files(weekday_data, '평일')
save_time_based_files(weekend_data, '주말')

#########################################################################################################
inout_car_db = pd.read_pickle(path_result + '//KT_인구//3.유입유출인구//inout_car_db.pkl')
inout_car_db['week_yn'] = inout_car_db['week_yn'].astype('int')
inout_car_db_O = inout_car_db[inout_car_db['week_yn'] == 0] #평일
inout_car_db_1 = inout_car_db[inout_car_db['week_yn'] == 1] #주말

inout_car_db_O.rename(columns = {'HJD_NM':'행정동명'}, inplace=True)
inout_car_db_1.rename(columns = {'HJD_NM':'행정동명'}, inplace=True)

def save_time_based_files(data, filename_prefix):
    for hour in range(24):
        hour_data = data[data['TIME_CD'] == hour]
        hour_data  = pd.merge(sgg_hjd,hour_data,on='행정동명',how='left')
        hour_data_geo = gpd.GeoDataFrame(hour_data, geometry='geometry', crs='EPSG:5179')
        hour_data_geo.fillna(0, inplace=True)
        if not hour_data.empty:
            hour_data.to_file(PATH_RESULT3 + f'//유입유출차량//{filename_prefix}//{filename_prefix}_{hour}시.gpkg',driver='GPKG')

save_time_based_files(inout_car_db_O, '평일')
save_time_based_files(inout_car_db_1, '주말')