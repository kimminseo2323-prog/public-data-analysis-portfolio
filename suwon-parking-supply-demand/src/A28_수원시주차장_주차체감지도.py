###########################################################
# 과 제 명: A28_수원시_주차장수요공급분석
# 파 일 명: A28_수원시주차장_주차체감지도
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
import geopandas as gpd
import pandas as pd
import os
import numpy as np
from scipy.stats import pearsonr

## 주차체감지도 작성 : 주차장 공급지수 + 시간대별
###################################################################################################
## 주차 체감지표 개발
###################################################################################################

##1. 유입/유출 좌표로 기초구역 ID 생성
move_id = pd.read_pickle(path_result + '//KT_인구//1.유동인구//최근한달유동인구_기초구역매핑.pkl')
move_id.columns
move_id_var = move_id[['기초구역번호', 'UTMK_X', 'UTMK_Y']]
move_id_dong = move_id[['기초구역번호', 'HJD_NM']]
move_id_dong = move_id_dong.drop_duplicates()

## 기초구역별 주차장 확보율
park_db = pd.read_pickle(path_middle + '//기초구역경계//기초구역경계_주차장확보율_수정.pkl')

# 생활인구 데이터
move_t3_202405 = pd.read_pickle(path_middle + '//주차체감지도//move_t3_202405.pkl')

# 차량 유입/유출 데이터 연계를 위한 연령대 정보 새로 생성
move_t3_202405['M_AGE_02'] =  ( move_t3_202405['H_M_10_CNT']+move_t3_202405['W_M_10_CNT']+move_t3_202405['V_M_10_CNT']
                             + move_t3_202405['H_M_15_CNT']+move_t3_202405['W_M_15_CNT']+move_t3_202405['V_M_15_CNT'])
move_t3_202405['M_AGE_03'] =  ( move_t3_202405['H_M_20_CNT']+move_t3_202405['W_M_20_CNT']+move_t3_202405['V_M_20_CNT']
                             + move_t3_202405['H_M_25_CNT']+move_t3_202405['W_M_25_CNT']+move_t3_202405['V_M_25_CNT'])
move_t3_202405['M_AGE_04'] =  ( move_t3_202405['H_M_30_CNT']+move_t3_202405['W_M_30_CNT']+move_t3_202405['V_M_30_CNT']
                             + move_t3_202405['H_M_35_CNT']+move_t3_202405['W_M_35_CNT']+move_t3_202405['V_M_35_CNT'])
move_t3_202405['M_AGE_05'] =  ( move_t3_202405['H_M_40_CNT']+move_t3_202405['W_M_40_CNT']+move_t3_202405['V_M_40_CNT']
                             + move_t3_202405['H_M_45_CNT']+move_t3_202405['W_M_45_CNT']+move_t3_202405['V_M_45_CNT'])
move_t3_202405['M_AGE_06'] =  ( move_t3_202405['H_M_50_CNT']+move_t3_202405['W_M_50_CNT']+move_t3_202405['V_M_50_CNT']
                             + move_t3_202405['H_M_55_CNT']+move_t3_202405['W_M_55_CNT']+move_t3_202405['V_M_55_CNT'])
move_t3_202405['M_AGE_07'] = (  move_t3_202405['H_M_60_CNT']+move_t3_202405['W_M_60_CNT']+move_t3_202405['V_M_60_CNT']
                             + move_t3_202405['H_M_65_CNT']+move_t3_202405['W_M_65_CNT']+move_t3_202405['V_M_65_CNT'])
move_t3_202405['M_AGE_08'] =   move_t3_202405['H_M_70_CNT']+move_t3_202405['W_M_70_CNT']+move_t3_202405['V_M_70_CNT']

move_t3_202405['F_AGE_02'] =  ( move_t3_202405['H_F_10_CNT']+move_t3_202405['W_F_10_CNT']+move_t3_202405['V_F_10_CNT']
                             + move_t3_202405['H_F_15_CNT']+move_t3_202405['W_F_15_CNT']+move_t3_202405['V_F_15_CNT'])
move_t3_202405['F_AGE_03'] =  ( move_t3_202405['H_F_20_CNT']+move_t3_202405['W_F_20_CNT']+move_t3_202405['V_F_20_CNT']
                             + move_t3_202405['H_F_25_CNT']+move_t3_202405['W_F_25_CNT']+move_t3_202405['V_F_25_CNT'])
move_t3_202405['F_AGE_04'] =  ( move_t3_202405['H_F_30_CNT']+move_t3_202405['W_F_30_CNT']+move_t3_202405['V_F_30_CNT']
                             + move_t3_202405['H_F_35_CNT']+move_t3_202405['W_F_35_CNT']+move_t3_202405['V_F_35_CNT'])
move_t3_202405['F_AGE_05'] = (  move_t3_202405['H_F_40_CNT']+move_t3_202405['W_F_40_CNT']+move_t3_202405['V_F_40_CNT']
                             + move_t3_202405['H_F_45_CNT']+move_t3_202405['W_F_45_CNT']+move_t3_202405['V_F_45_CNT'])
move_t3_202405['F_AGE_06'] = (  move_t3_202405['H_F_50_CNT']+move_t3_202405['W_F_50_CNT']+move_t3_202405['V_F_50_CNT']
                             + move_t3_202405['H_F_55_CNT']+move_t3_202405['W_F_55_CNT']+move_t3_202405['V_F_55_CNT'])
move_t3_202405['F_AGE_07'] = (  move_t3_202405['H_F_60_CNT']+move_t3_202405['W_F_60_CNT']+move_t3_202405['V_F_60_CNT']
                             + move_t3_202405['H_F_65_CNT']+move_t3_202405['W_F_65_CNT']+move_t3_202405['V_F_65_CNT'])
move_t3_202405['F_AGE_08'] =   move_t3_202405['H_F_70_CNT']+move_t3_202405['W_F_70_CNT']+move_t3_202405['V_F_70_CNT']

move_t3_202405 = pd.merge(move_t3_202405, move_id_var, how = 'left', on = [ 'UTMK_X', 'UTMK_Y'])
t3_202405 = move_t3_202405.groupby(['기초구역번호', 'ETL_YMD', 'TIME_CD' ])[['M_AGE_02', 'M_AGE_03', 'M_AGE_04',
       'M_AGE_05', 'M_AGE_06', 'M_AGE_07', 'M_AGE_08', 'F_AGE_02', 'F_AGE_03', 'F_AGE_04',
       'F_AGE_05', 'F_AGE_06', 'F_AGE_07', 'F_AGE_08']].sum().reset_index()

t3_202405.to_pickle(path_middle + '//주차체감지도//t3_202405_수정.pkl')

#######################################################################################################################

t3_202405 = pd.read_pickle(path_middle + '//주차체감지도//t3_202405_수정.pkl')

# 남성 정보 생성
t3_202405_male = t3_202405[['기초구역번호',  'ETL_YMD', 'TIME_CD','M_AGE_02', 'M_AGE_03', 'M_AGE_04','M_AGE_05', 'M_AGE_06', 'M_AGE_07', 'M_AGE_08']]
t3_202405_male['SEX_CD'] = 'M'
t3_202405_male['ETL_YMD'] = t3_202405_male['ETL_YMD'].astype(str)
t3_202405_male.columns = ['기초구역번호', 'ETL_YMD', 'TIME_CD', 'AGE_02', 'AGE_03', 'AGE_04',
                           'AGE_05', 'AGE_06', 'AGE_07', 'AGE_08', 'SEX_CD']
t3_male = t3_202405_male.melt(id_vars=['기초구역번호',  'ETL_YMD', 'TIME_CD', 'SEX_CD'],
                              value_vars=['AGE_02', 'AGE_03','AGE_04','AGE_05','AGE_06','AGE_07','AGE_08'],
                              var_name = 'AGE_GB',
                              value_name = 'CNT')
t3_male = pd.merge(t3_male, move_id_dong, how = 'left', on = '기초구역번호')

# 여성 정보 생성
t3_202405_female = t3_202405[['기초구역번호',  'ETL_YMD', 'TIME_CD',
                             'F_AGE_02', 'F_AGE_03', 'F_AGE_04','F_AGE_05', 'F_AGE_06', 'F_AGE_07', 'F_AGE_08']]
t3_202405_female['SEX_CD'] = 'F'
t3_202405_female['ETL_YMD'] = t3_202405_female['ETL_YMD'].astype(str)
t3_202405_female.columns = ['기초구역번호', 'ETL_YMD', 'TIME_CD', 'AGE_02', 'AGE_03', 'AGE_04',
                           'AGE_05', 'AGE_06', 'AGE_07', 'AGE_08', 'SEX_CD']
t3_female = t3_202405_female.melt(id_vars=['기초구역번호',  'ETL_YMD', 'TIME_CD', 'SEX_CD'],
                              value_vars=['AGE_02', 'AGE_03','AGE_04','AGE_05','AGE_06','AGE_07','AGE_08'],
                              var_name = 'AGE_GB',
                              value_name = 'CNT')
t3_female = pd.merge(t3_female, move_id_dong, how = 'left', on = '기초구역번호')

##########################################################

### 자동차 유입인구 : move_t7
move_t7 = pd.read_pickle(path_middle + '//주차체감지도//move_t7.pkl')

move_t7['ETL_YMD'] = move_t7['ETL_YMD'].astype(str)
move_t7s = move_t7[move_t7['ETL_YMD'].str[:6] == '202405']
move_t7s_car = move_t7s[move_t7s['TRANS_GB'] == 0]
move_t7s_car = move_t7s_car[move_t7s_car['D_CTY_NM'].isin(['수원시 권선구', '수원시 영통구', '수원시 장안구', '수원시 팔달구' ])]
t7s_car_sum = move_t7s_car.groupby(['ETL_YMD', 'D_TIME_CD', 'D_ADMI_NM', 'SEX_CD', 'AGE_GRP'])['CNT'].sum().reset_index()
t7s_car_sum.columns = ['ETL_YMD', 'TIME_CD', 'HJD_NM', 'SEX_CD', 'AGE_GRP', 'CNT']
t7s_car_sum['AGE_GB'] = np.where(t7s_car_sum['AGE_GRP'] == 1, 'AGE_02',
                            np.where(t7s_car_sum['AGE_GRP'] == 2, 'AGE_02',
                                np.where(t7s_car_sum['AGE_GRP'] == 3, 'AGE_03',
                                    np.where(t7s_car_sum['AGE_GRP'] == 4, 'AGE_04',
                                        np.where(t7s_car_sum['AGE_GRP'] == 5, 'AGE_05',
                                           np.where(t7s_car_sum['AGE_GRP'] == 6, 'AGE_06',
                                              np.where(t7s_car_sum['AGE_GRP'] == 7, 'AGE_07',  'AGE_08')))))))

t7s_car_sum = t7s_car_sum.groupby(['ETL_YMD', 'TIME_CD', 'HJD_NM', 'SEX_CD', 'AGE_GB'])['CNT'].sum().reset_index()
t7s_car_sum.columns = ['ETL_YMD', 'TIME_CD', 'HJD_NM', 'SEX_CD', 'AGE_GB', 'CNT_CAR']
t7s_car_sum['ETL_YMD'] = t7s_car_sum['ETL_YMD'].astype(str)

weeklist = ['04','05','06', '11','12', '15', '18', '19', '25', '26']
t7s_car_sum['week_yn'] = np.where(t7s_car_sum['ETL_YMD'].str[6:8].isin(weeklist), '1', '0')

#### 전체 유입인구 : move_7
move_t7s_2 = move_t7s[move_t7s['D_CTY_NM'].isin(['수원시 권선구', '수원시 영통구', '수원시 장안구', '수원시 팔달구' ])]
t7s_sum = move_t7s_2.groupby(['ETL_YMD', 'D_TIME_CD', 'D_ADMI_NM', 'SEX_CD', 'AGE_GRP'])['CNT'].sum().reset_index()
t7s_sum.columns = ['ETL_YMD', 'TIME_CD', 'HJD_NM', 'SEX_CD', 'AGE_GRP', 'CNT']
t7s_sum['AGE_GB'] = np.where(t7s_sum['AGE_GRP'] == 1, 'AGE_02',
                            np.where(t7s_sum['AGE_GRP'] == 2, 'AGE_02',
                                np.where(t7s_sum['AGE_GRP'] == 3, 'AGE_03',
                                    np.where(t7s_sum['AGE_GRP'] == 4, 'AGE_04',
                                        np.where(t7s_sum['AGE_GRP'] == 5, 'AGE_05',
                                           np.where(t7s_sum['AGE_GRP'] == 6, 'AGE_06',
                                              np.where(t7s_sum['AGE_GRP'] == 7, 'AGE_07',  'AGE_08')))))))

t7s_sum = t7s_sum.groupby(['ETL_YMD', 'TIME_CD', 'HJD_NM', 'SEX_CD', 'AGE_GB'])['CNT'].sum().reset_index()
t7s_sum.columns = ['ETL_YMD', 'TIME_CD', 'HJD_NM', 'SEX_CD', 'AGE_GB', 'CNT_TOT']
t7s_sum['ETL_YMD'] = t7s_sum['ETL_YMD'].astype(str)

weeklist = ['04','05','06', '11','12', '15', '18', '19', '25', '26']
t7s_sum['week_yn'] = np.where(t7s_sum['ETL_YMD'].str[6:8].isin(weeklist), '1', '0')



### 자동차 유출인구 : move_t11
move_t11 = pd.read_pickle(path_middle + '//주차체감지도//move_t11.pkl')

move_t11['ETL_YMD'] = move_t11['ETL_YMD'].astype(str)
move_t11s = move_t11[move_t11['ETL_YMD'].str[:6] == '202405']
move_t11s_car = move_t11s[move_t11s['TRANS_GB'] == 0]
move_t11s_car = move_t11s_car[move_t11s_car['O_CTY_NM'].isin(['수원시 권선구', '수원시 영통구', '수원시 장안구', '수원시 팔달구' ])]
t11s_car_sum = move_t11s_car.groupby(['ETL_YMD', 'O_TIME_CD', 'O_ADMI_NM', 'SEX_CD', 'AGE_GRP'])['CNT'].sum().reset_index()
t11s_car_sum.columns = ['ETL_YMD', 'TIME_CD', 'HJD_NM', 'SEX_CD', 'AGE_GRP', 'CNT']
t11s_car_sum['AGE_GB'] = np.where(t11s_car_sum['AGE_GRP'] == 1, 'AGE_02',
                            np.where(t11s_car_sum['AGE_GRP'] == 2, 'AGE_02',
                                np.where(t11s_car_sum['AGE_GRP'] == 3, 'AGE_03',
                                    np.where(t11s_car_sum['AGE_GRP'] == 4, 'AGE_04',
                                        np.where(t11s_car_sum['AGE_GRP'] == 5, 'AGE_05',
                                           np.where(t11s_car_sum['AGE_GRP'] == 6, 'AGE_06',
                                              np.where(t11s_car_sum['AGE_GRP'] == 7, 'AGE_07',  'AGE_08')))))))

t11s_car_sum = t11s_car_sum.groupby(['ETL_YMD', 'TIME_CD', 'HJD_NM', 'SEX_CD', 'AGE_GB'])['CNT'].sum().reset_index()
t11s_car_sum.columns = ['ETL_YMD', 'TIME_CD', 'HJD_NM', 'SEX_CD', 'AGE_GB', 'CNT_CAR']
t11s_car_sum['ETL_YMD'] = t11s_car_sum['ETL_YMD'].astype(str)
t11s_car_sum['week_yn'] = np.where(t11s_car_sum['ETL_YMD'].str[6:8].isin(weeklist), '1', '0')

#### 전체 유출인구 : move_11
move_t11s_2 = move_t11s[move_t11s['O_CTY_NM'].isin(['수원시 권선구', '수원시 영통구', '수원시 장안구', '수원시 팔달구' ])]
t11s_sum = move_t11s_2.groupby(['ETL_YMD', 'O_TIME_CD', 'O_ADMI_NM', 'SEX_CD', 'AGE_GRP'])['CNT'].sum().reset_index()
t11s_sum.columns = ['ETL_YMD', 'TIME_CD', 'HJD_NM', 'SEX_CD', 'AGE_GRP', 'CNT']
t11s_sum['AGE_GB'] = np.where(t11s_sum['AGE_GRP'] == 1, 'AGE_02',
                            np.where(t11s_sum['AGE_GRP'] == 2, 'AGE_02',
                                np.where(t11s_sum['AGE_GRP'] == 3, 'AGE_03',
                                    np.where(t11s_sum['AGE_GRP'] == 4, 'AGE_04',
                                        np.where(t11s_sum['AGE_GRP'] == 5, 'AGE_05',
                                           np.where(t11s_sum['AGE_GRP'] == 6, 'AGE_06',
                                              np.where(t11s_sum['AGE_GRP'] == 7, 'AGE_07',  'AGE_08')))))))

t11s_sum = t11s_sum.groupby(['ETL_YMD', 'TIME_CD', 'HJD_NM', 'SEX_CD', 'AGE_GB'])['CNT'].sum().reset_index()
t11s_sum.columns = ['ETL_YMD', 'TIME_CD', 'HJD_NM', 'SEX_CD', 'AGE_GB', 'CNT_TOT']
t11s_sum['ETL_YMD'] = t11s_sum['ETL_YMD'].astype(str)

weeklist = ['04','05','06', '11','12', '15', '18', '19', '25', '26']
t11s_sum['week_yn'] = np.where(t11s_sum['ETL_YMD'].str[6:8].isin(weeklist), '1', '0')

## 행정동별 요일별 시간대별 차량 유입유출인구수

t11s_car_db = t11s_car_sum.groupby(['ETL_YMD', 'week_yn', 'TIME_CD', 'HJD_NM'])['CNT_CAR'].sum().reset_index()
t11s_car_db2 = t11s_car_db.groupby(['HJD_NM', 'week_yn', 'TIME_CD'])['CNT_CAR'].mean().reset_index()
t11s_car_db2.columns = ['HJD_NM', 'week_yn', 'TIME_CD', '차량유출인구']

t7s_car_db = t7s_car_sum.groupby(['ETL_YMD', 'week_yn', 'TIME_CD', 'HJD_NM'])['CNT_CAR'].sum().reset_index()
t7s_car_db2 = t7s_car_db.groupby(['HJD_NM', 'week_yn', 'TIME_CD'])['CNT_CAR'].mean().reset_index()
t7s_car_db2.columns = ['HJD_NM', 'week_yn', 'TIME_CD', '차량유입인구']

## 통합
inout_car_db = pd.merge(t7s_car_db2, t11s_car_db2, how = 'left', on = ['HJD_NM', 'week_yn', 'TIME_CD'])
inout_car_db.to_pickle(path_middle + '//유입유출//inout_car_db_수정.pkl')


########################################################################
## 생활인구와 자동차유입인구 합치기 : 동별/날짜별/시간대별 생활인구수 또는 시간대별 증감 & 동별 차량/전체 유입인구/유출인구수 검증
#### 1. 동별 시간대별 생활인구수 : 남자
t3_m_dong = t3_male.groupby(['HJD_NM', 'SEX_CD', 'AGE_GB', 'ETL_YMD', 'TIME_CD' ])['CNT'].sum().reset_index()

t3t11_m = pd.merge(t3_m_dong, t11s_sum, how='left', on=['HJD_NM', 'SEX_CD', 'AGE_GB', 'ETL_YMD', 'TIME_CD'])
t3t11_m = t3t11_m.drop('week_yn', axis=1)
t3t11_m.columns = ['HJD_NM', 'SEX_CD', 'AGE_GB', 'ETL_YMD', 'TIME_CD', 'CNT', '유출인구']
t3t11_m = pd.merge(t3t11_m, t7s_sum, how='left', on=['HJD_NM', 'SEX_CD', 'AGE_GB', 'ETL_YMD', 'TIME_CD'])
t3t11_m.columns = ['HJD_NM', 'SEX_CD', 'AGE_GB', 'ETL_YMD', 'TIME_CD', 'CNT', '유출인구', '유입인구', 'week_yn']
t3t11_m['증감인구'] = t3t11_m['유입인구'] - t3t11_m['유출인구']

# '이전 값' 항목 생성하여 앞 행의 값을 유지하도록 함  retain
t3t11_m['cnt_add'] = t3t11_m['CNT'] - t3t11_m['CNT'].shift()
t3t11_m = t3t11_m.fillna(0)
correlation_coefficient, p_value =  pearsonr(t3t11_m['cnt_add'], t3t11_m['증감인구'])
print(f"Pearson 상관계수: {correlation_coefficient, p_value}")  # Pearson 상관계수: (0.5835675512041657, 0.0)

#### 2. 동별 시간대별 생활인구수 : 여자
t3_w_dong = t3_female.groupby(['HJD_NM', 'SEX_CD', 'AGE_GB', 'ETL_YMD', 'TIME_CD' ])['CNT'].sum().reset_index()
t3_w_dong['SEX_CD'] = 'W'
t3t11_w = pd.merge(t3_w_dong, t11s_sum, how='left', on=['HJD_NM', 'SEX_CD', 'AGE_GB', 'ETL_YMD', 'TIME_CD'])
t3t11_w = t3t11_w.drop('week_yn', axis=1)
t3t11_w.columns = ['HJD_NM', 'SEX_CD', 'AGE_GB', 'ETL_YMD', 'TIME_CD', 'CNT', '유출인구']
t3t11_w = pd.merge(t3t11_w, t7s_sum, how='left', on=['HJD_NM', 'SEX_CD', 'AGE_GB', 'ETL_YMD', 'TIME_CD'])
t3t11_w.columns = ['HJD_NM', 'SEX_CD', 'AGE_GB', 'ETL_YMD', 'TIME_CD', 'CNT', '유출인구', '유입인구', 'week_yn']
t3t11_w['증감인구'] = t3t11_w['유입인구'] - t3t11_w['유출인구']

# '이전 값' 항목 생성하여 앞 행의 값을 유지하도록 함  retain
t3t11_w['cnt_add'] = t3t11_w['CNT'] - t3t11_w['CNT'].shift()
t3t11_w = t3t11_w.fillna(0)
correlation_coefficient, p_value =  pearsonr(t3t11_w['cnt_add'], t3t11_w['증감인구'])
print(f"Pearson 상관계수: {correlation_coefficient, p_value}") # Pearson 상관계수: (0.4319856140984584, 0.0)


########################################################################

##  체감지표 생성
## 1. 행정동별 차량 유입/유출 데이터를 기초구역별 차량 유입/유출로 할당 :  생활인구와 자동차유입인구 상관관계 분석

#### 1.1 행정동별 성별/연령/날짜/시간대별 생활인구
#### t3_male : 기초구역별 성별 연령대별 시간대별 생활인구수, 생활인구수 증감 산출
t3_male['cnt_add'] = t3_male['CNT'] - t3_male['CNT'].shift()
t3_female['cnt_add'] = t3_female['CNT'] - t3_female['CNT'].shift()
t3_female['SEX_CD'] = 'W'

t3_all = pd.concat([t3_male, t3_female], axis = 0 )

## 행궁동 샘플 데이터 생성
# t3_males = t3_male[t3_male['HJD_NM'] == '행궁동']
inout = t3_all


# A 그룹, B 그룹의 순서 number 생성   : 그룹의 첫번째 행 값 생성 . 그룹별 순번
inout['no'] = inout.groupby(['HJD_NM','기초구역번호','SEX_CD', 'AGE_GB']).cumcount() + 1

inout['cnt_add'] = np.where(inout['no'] == 1, 0, inout['cnt_add'])
inout['cnt_incr'] = np.where(inout['cnt_add'] >0, inout['cnt_add'], 0)
inout['cnt_decr'] = np.where(inout['cnt_add'] <0, abs(inout['cnt_add']), 0)

## 행정동별 생활인구수, 유입유출 데이터 추가
inout_tot = inout.groupby(['HJD_NM','SEX_CD', 'AGE_GB','ETL_YMD', 'TIME_CD'])[['CNT','cnt_incr', 'cnt_decr']].sum().reset_index()
inout_tot.columns = ['HJD_NM', 'SEX_CD', 'AGE_GB', 'ETL_YMD', 'TIME_CD', 'cnt_dong', 'incr_dong', 'decr_dong']

## 기초구역 생활인구에 행정동별 생활인구 정보 추가
inout_2 = pd.merge(inout, inout_tot, how = 'left', on =  ['HJD_NM', 'SEX_CD', 'AGE_GB', 'ETL_YMD', 'TIME_CD'])
inout_2['incr_rt'] = np.where(inout_2['incr_dong'] == 0,inout_2['CNT']/inout_2['cnt_dong'], inout_2['cnt_incr']/inout_2['incr_dong'])
inout_2['decr_rt'] = np.where(inout_2['decr_dong'] == 0,inout_2['CNT']/inout_2['cnt_dong'], inout_2['cnt_decr']/inout_2['decr_dong'])

## 행정동별 차량 유입/유출량 정보 추가
join_t7s_car = t7s_car_sum[['ETL_YMD', 'TIME_CD', 'HJD_NM', 'SEX_CD', 'AGE_GB', 'CNT_CAR']]
join_t7s_car.columns = ['ETL_YMD', 'TIME_CD', 'HJD_NM', 'SEX_CD', 'AGE_GB', 'in_car']

join_t11s_car = t11s_car_sum[['ETL_YMD', 'TIME_CD', 'HJD_NM', 'SEX_CD', 'AGE_GB', 'CNT_CAR']]
join_t11s_car.columns = ['ETL_YMD', 'TIME_CD', 'HJD_NM', 'SEX_CD', 'AGE_GB', 'out_car']

inout_3 = pd.merge(inout_2, join_t7s_car, how = 'left', on = ['ETL_YMD', 'TIME_CD', 'HJD_NM', 'SEX_CD', 'AGE_GB'])
inout_3 = pd.merge(inout_3, join_t11s_car, how = 'left', on = ['ETL_YMD', 'TIME_CD', 'HJD_NM', 'SEX_CD', 'AGE_GB'])
inout_3 = inout_3.fillna(0)

inout_3['incar_area'] = inout_3['incr_rt']*inout_3['in_car']
inout_3['outcar_area'] = inout_3['decr_rt']*inout_3['out_car']

inout_4 = inout_3.groupby(['HJD_NM','기초구역번호','ETL_YMD', 'TIME_CD'])[['incar_area', 'outcar_area']].sum().reset_index()
week_yn = t11s_sum.groupby(['ETL_YMD'])['week_yn'].max().reset_index()
inout_4 = pd.merge(inout_4, week_yn, how = 'left', on = 'ETL_YMD')

## 평일/주말별 기초구역별 시간대별 현황
inout_5 = inout_4.groupby(['HJD_NM','기초구역번호','week_yn', 'TIME_CD'])[['incar_area', 'outcar_area']].mean().reset_index()


## Index 생성.  남자, 기초구역별 생활인구수와 차량 유출입 합치기
#### 행정동별 차량, 유입 유출

join_park = park_db[['HJD_NM', '기초구역번호', '총주차면수', '총등록차량수', '주차장확보율']]
join_park['기초구역번호'] = join_park['기초구역번호'].astype('str')
index_02 = pd.merge(join_park, inout_5,   how = 'left', on = ['HJD_NM', '기초구역번호'])
index_02 = index_02.fillna(0)

## 기초구역별 시간대별 증가/감소 생활인구 생성
index_02 = index_02.sort_values(by = ['HJD_NM','기초구역번호', 'week_yn','TIME_CD' ], ascending = True)
index_02['car_add'] = (index_02['incar_area'] -  index_02['outcar_area'])/1.8
index_02['add_cum'] = index_02.groupby(['HJD_NM','기초구역번호', 'week_yn'])['car_add'].cumsum()
index_02 = index_02.fillna(0)

index_02['park_addrt'] = np.where((index_02['총등록차량수'] + index_02['add_cum'])==0, 0, index_02['총주차면수'] / (index_02['총등록차량수'] + index_02['add_cum']))
index_02['park_addrt'] =  round(index_02['park_addrt']*100, 1)

index_02['park_index'] = np.where(index_02['총주차면수'] == 0, 0,
                            np.where(index_02['park_addrt'] < 0, 200,
                               np.where(index_02['park_addrt'] >= 200, 200, index_02['park_addrt'])))

index_02['park_index_gr'] = np.where((index_02['park_index'] > 0 ) & (index_02['park_index'] < 10 ), 1, (index_02['park_index']*0.1).astype(int)*10)
index_02['index_group'] = np.where(index_02['park_index'] < 50, 0,
                                np.where(index_02['park_index'] < 80, 1,
                                   np.where(index_02['park_index'] < 100, 2,
                                      np.where(index_02['park_index'] < 120, 3,
                                           np.where(index_02['park_index'] < 150, 4, 5)))))
index_02['index_name'] = np.where(index_02['park_index'] < 50, '심각',
                                np.where(index_02['park_index'] < 80, '혼잡',
                                   np.where(index_02['park_index'] < 100, '부족',
                                      np.where(index_02['park_index'] < 120, '보통',
                                           np.where(index_02['park_index'] < 150, '양호', '여유')))))


index_02.to_pickle(path_middle + '//주차체감지도//index_02.pkl')
index_02 = pd.read_pickle(path_middle + '//주차체감지도//index_02.pkl')

## 보고서 현황분석 자료 생성
# 시간대별 차량유출 인구수

aa01 = t11s_car_sum.groupby(['ETL_YMD','week_yn', 'TIME_CD'])['CNT_CAR'].sum().reset_index()
aa011 = aa01.groupby(['week_yn', 'TIME_CD'])['CNT_CAR'].mean().reset_index()
aa011.to_excel(path_result + '//주차체감지도//D0922_시간대별차량유출현황.xlsx')

aa02 = t7s_car_sum.groupby(['ETL_YMD','week_yn', 'TIME_CD'])['CNT_CAR'].sum().reset_index()
aa021 = aa02.groupby(['week_yn', 'TIME_CD'])['CNT_CAR'].mean().reset_index()
aa021.to_excel(path_result + '//주차체감지도//D0922_시간대별차량유입현황.xlsx')

# 7시 행정구역별 유입/유출 (행굼동)  : 기초구역별로 안됨
aa03 = t11s_car_sum[(t11s_car_sum['TIME_CD'] == 7) & (t11s_car_sum['week_yn'] == '0')]
aa03_out = aa03.groupby(['HJD_NM'])['CNT_CAR'].sum().reset_index()
aa03_out.columns = ['HJD_NM', '차량인구_유출']

aa031 = t7s_car_sum[(t7s_car_sum['TIME_CD'] == 7) & (t7s_car_sum['week_yn'] == '0')]
aa03_in = aa031.groupby(['HJD_NM'])['CNT_CAR'].sum().reset_index()
aa03_in.columns = ['HJD_NM', '차량인구_유입']

aa032_7h = pd.merge(aa03_out, aa03_in, how = 'left', on = 'HJD_NM')
aa032_7h['유입유출차이'] =  aa032_7h['차량인구_유입'] - aa032_7h['차량인구_유출']
aa032_7h.to_pickle(path_middle + '//주차체감지도//행정동별유입유출차이_7시.pkl')
aa032_7h.to_excel(path_middle + '//주차체감지도//행정동별유입유출차이_7시.xlsx')

aa03 = t11s_car_sum[(t11s_car_sum['TIME_CD'] == 12) & (t11s_car_sum['week_yn'] == '0')]
aa03_out = aa03.groupby(['HJD_NM'])['CNT_CAR'].sum().reset_index()
aa03_out.columns = ['HJD_NM', '차량인구_유출']

aa031 = t7s_car_sum[(t7s_car_sum['TIME_CD'] == 12) & (t7s_car_sum['week_yn'] == '0')]
aa03_in = aa031.groupby(['HJD_NM'])['CNT_CAR'].sum().reset_index()
aa03_in.columns = ['HJD_NM', '차량인구_유입']

aa032_12h = pd.merge(aa03_out, aa03_in, how = 'left', on = 'HJD_NM')
aa032_12h['유입유출차이'] =  aa032_12h['차량인구_유입'] - aa032_12h['차량인구_유출']
aa032_12h.to_pickle(path_middle + '//주차체감지도//행정동별유입유출차이_12시.pkl')
aa032_12h.to_excel(path_middle + '//주차체감지도//행정동별유입유출차이_12시.xlsx')

# 체감지표 분포도
aa31 = index_02.groupby(['park_index_gr']).size().reset_index()
aa31.to_excel(path_middle + '//주차체감지도//D0923_체감지표현황.xlsx')

index_02['TIME_CD'] = index_02['TIME_CD'].astype('int')
index_02['week_yn'] = index_02['week_yn'].astype('str')
## 평일 아침 7시 혼잡도
aa32 = index_02[(index_02['TIME_CD'] == 7)&(index_02['week_yn'] == '0')].groupby(['park_index_gr']).size().reset_index()
aa32.to_excel(path_middle + '//주차체감지도//D0923_체감지표현황_평일7시.xlsx')

## 평일 20시 혼잡도
aa34 = index_02[(index_02['TIME_CD'] == 20)&(index_02['week_yn'] == '0')].groupby(['park_index_gr']).size().reset_index()
aa34.to_excel(path_middle + '//주차체감지도//D0923_체감지표현황_평일20시.xlsx')

## 평일 12시 혼잡도
aa32 = index_02[(index_02['TIME_CD'] == 12)&(index_02['week_yn'] == '0')].groupby(['park_index_gr']).size().reset_index()
aa32.to_excel(path_middle + '//주차체감지도//D0923_체감지표현황_평일12시.xlsx')

## index 7시, 12시
index_02_7h =  index_02[(index_02['TIME_CD'] == 7)&(index_02['week_yn'] == '0')]
index_02_12h =  index_02[(index_02['TIME_CD'] == 12)&(index_02['week_yn'] == '0')]
index_02_20h =  index_02[(index_02['TIME_CD'] == 20)&(index_02['week_yn'] == '0')]

index_02_7h.to_pickle(path_middle + '//주차체감지도//기초구역별주차체감지표_평일7시.pkl')
index_02_12h.to_pickle(path_middle + '//주차체감지도//기초구역별주차체감지표_평일12시.pkl')
index_02_20h.to_pickle(path_middle + '//주차체감지도//기초구역별주차체감지표_평일20시.pkl')


aa33 = index_02_20h.groupby(['index_group','index_name']).size().reset_index()
aa33.to_excel(path_middle + '//주차체감지도//D0923_체감지표등급_평일20시.xlsx')

aa34 = index_02_12h.groupby(['index_group','index_name']).size().reset_index()
aa34.to_excel(path_middle + '//주차체감지도//D0923_체감지표등급_평일12시.xlsx')


######################## 주차체감지도 ptt 시각화 자료 생성 ##########################
base_cd_5179 = gpd.read_file(PATH_RESULT3 + '//경계면데이터//기초구역경계//기초구역경계.gpkg',driver='GPKG')
sgg_hjd = gpd.read_file(PATH_RESULT3 + '//경계면데이터//행정동경계//시군구_행정동경계.gpkg',driver='GPKG')
inandout_7 = pd.read_pickle(path_middle + '//주차체감지도//행정동별유입유출차이_7시.pkl')
inandout_12 = pd.read_pickle(path_middle + '//주차체감지도//행정동별유입유출차이_12시.pkl')

sgg_hjd_r = sgg_hjd.rename(columns={'행정동명':'HJD_NM'})
inandout_7r = pd.merge(inandout_7,sgg_hjd_r,on='HJD_NM',how='left')
inandout_12r = pd.merge(inandout_12,sgg_hjd_r,on='HJD_NM',how='left')

inandout_7r_geo = gpd.GeoDataFrame(inandout_7r, geometry='geometry', crs='EPSG:5179')
inandout_12r_geo = gpd.GeoDataFrame(inandout_12r, geometry='geometry', crs='EPSG:5179')
inandout_7r_geo.to_file(PATH_RESULT3 + '//주차체감지도//행정동별유입유출차이_7시_수정.gpkg',driver='GPKG')
inandout_12r_geo.to_file(PATH_RESULT3 + '//주차체감지도//행정동별유입유출차이_12시_수정.gpkg',driver='GPKG')


base_inandout_12 = pd.read_pickle(path_middle + '//주차체감지도//기초구역별주차체감지표_평일12시.pkl')
base_inandout_20 = pd.read_pickle(path_middle + '//주차체감지도//기초구역별주차체감지표_평일7시.pkl')
base_inandout_12.reset_index(drop=True, inplace=True)
base_inandout_20.reset_index(drop=True, inplace=True)

base_inandout_12r = pd.merge(base_cd_5179,base_inandout_12,on='기초구역번호',how='left')
base_inandout_20r = pd.merge(base_cd_5179,base_inandout_20,on='기초구역번호',how='left')

base_inandout_12r.fillna(0,inplace=True)
base_inandout_20r.fillna(0,inplace=True)
base_inandout_12r_geo = gpd.GeoDataFrame(base_inandout_12r, geometry='geometry', crs='EPSG:5179')
base_inandout_20r_geo = gpd.GeoDataFrame(base_inandout_20r, geometry='geometry', crs='EPSG:5179')
base_inandout_12r_geo.to_file(PATH_RESULT3 + '//주차체감지도//기초구역별유입유출차이_12시_수정.gpkg',driver='GPKG')
base_inandout_20r_geo.to_file(PATH_RESULT3 + '//주차체감지도//기초구역별유입유출차이_20시_수정.gpkg',driver='GPKG')


######################## 전체데이터 ##########################
#주차제감등급
#주차제감지표
# 행정동별 유입유출차이 (평일,주말 따로 시간대별로 시각화하기) 총 48개 시각화결과 나와야함 평일 0~23시, 주말 0~23시
index_02 = pd.read_pickle(path_middle + '//주차체감지도//index_02.pkl')
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
inout_car_db = pd.read_pickle(path_middle + '//유입유출//inout_car_db_수정.pkl')
inout_car_db
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

######################## 행정동 주차체감지도 생성 ##########################

## 행정동별 차량유입, 유출인구 : inout_car_db
inout_car_db = pd.read_pickle(path_middle + '//유입유출//inout_car_db_수정.pkl')
#### 행정동별 주차면수, 등록차량
park_db = pd.read_pickle(path_middle + '//기초구역경계//기초구역경계_주차장확보율_수정.pkl')
park_db = park_db.groupby('HJD_NM')[['총주차면수', '총등록차량수']].sum().reset_index()
inout_car_db = pd.merge(inout_car_db, park_db, on = 'HJD_NM',how = 'left')
#join_park_dong = inout_car_db[['HJD_NM', 'ETL_YMD', 'TIME_CD', '총주차면수', '총등록차량수']]
#join_park_dong['week_yn'] = np.where(join_park_dong['ETL_YMD'].str[6:8].isin(weeklist), '1', '0')
join_park_dong = inout_car_db.groupby(['HJD_NM', 'week_yn', 'TIME_CD'])[['총주차면수', '총등록차량수']].mean().reset_index()
index_dong = pd.merge(join_park_dong, inout_car_db[['HJD_NM', 'week_yn', 'TIME_CD','차량유입인구','차량유출인구']],   how = 'left', on = ['HJD_NM', 'week_yn', 'TIME_CD'])
index_dong = index_dong.fillna(0)

index_dong = index_dong.sort_values(by = ['HJD_NM', 'week_yn', 'TIME_CD' ], ascending = True)
index_dong['car_add'] = (index_dong['차량유입인구'] -  index_dong['차량유출인구'])/1.8
index_dong['add_cum'] = index_dong.groupby(['HJD_NM', 'week_yn'])['car_add'].cumsum()
index_dong = index_dong.fillna(0)

index_dong['park_addrt'] = np.where((index_dong['총등록차량수'] + index_dong['add_cum'])==0, 0, index_dong['총주차면수'] / (index_dong['총등록차량수'] + index_dong['add_cum']))
index_dong['park_addrt'] =  round(index_dong['park_addrt']*100, 1)

index_dong['park_index'] = np.where(index_dong['총주차면수'] == 0, 0,
                            np.where(index_dong['park_addrt'] < 0, 200,
                               np.where(index_dong['park_addrt'] >= 200, 200, index_dong['park_addrt'])))

index_dong['park_index_gr'] = np.where((index_dong['park_index'] > 0 ) & (index_dong['park_index'] < 10 ), 1, (index_dong['park_index']*0.1).astype(int)*10)
index_dong['index_group'] = np.where(index_dong['park_index'] < 50, 0,
                                np.where(index_dong['park_index'] < 80, 1,
                                   np.where(index_dong['park_index'] < 100, 2,
                                      np.where(index_dong['park_index'] < 120, 3,
                                           np.where(index_dong['park_index'] < 150, 4, 5)))))
index_dong['index_name'] = np.where(index_dong['park_index'] < 50, '심각',
                                np.where(index_dong['park_index'] < 80, '혼잡',
                                   np.where(index_dong['park_index'] < 100, '부족',
                                      np.where(index_dong['park_index'] < 120, '보통',
                                           np.where(index_dong['park_index'] < 150, '양호', '여유')))))


index_dong.to_pickle(path_middle + '//주차체감지도//행정동분석//index_dong.pkl')
index_dong = pd.read_pickle(path_middle + '//주차체감지도//행정동분석//index_dong.pkl')