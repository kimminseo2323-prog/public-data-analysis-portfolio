###########################################################
# 과 제 명: A39_서초구_인구이동 및 도시계획
# 파 일 명: 생활이동 분석
# 작 성 자: 김민서
###########################################################

import os, importlib, warnings;
warnings.filterwarnings(action='ignore')
# DB 접속: 사내 모듈 사용 (비공개)  # 원본: from config import config_A39 as config;
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
from shapely.geometry import Point, LineString
import glob
from tqdm import tqdm
import matplotlib.pyplot as plt
import seaborn as sns
def categorize_time(hour):
    if hour == 0:
        adjusted_hour = 24
    else:
        adjusted_hour = hour
    if 11 <= adjusted_hour < 14:
        return '점심'
    elif 14 <= adjusted_hour < 17:
        return '오후'
    elif 17 <= adjusted_hour <= 21:
        return '저녁'
    else:
        return None

# 최근한달
data_d = pd.read_pickle(path_data_analyze + '//추가분석//202405_유입.pkl')
data_o = pd.read_pickle(path_data_analyze + '//추가분석//202405_유출.pkl')

# data_d : 서초구 제외
data_d2 = data_d[data_d['o_sgg'] != '서초구']
data_o2 = data_o[data_o['d_sgg'] != '서초구']
data_d1 = data_d2.groupby(['월','o_sgg','d_sgg']).agg({'total_cnt':'sum','move_dist' : 'mean'}).reset_index()
data_o1 = data_o2.groupby(['월','d_sgg','o_sgg']).agg({'total_cnt':'sum','move_dist' : 'mean'}).reset_index()
data_d1.to_excel(path_result + '//생활이동//추가분석//전체_유입시군구1.xlsx', index=False)
data_o1.to_excel(path_result + '//생활이동//추가분석//전체_유출시군구1.xlsx', index=False)

## 유입 ##
#전체유입 시군구
data_d3 = data_d2.groupby(['월','o_sgg','d_sgg','d_admi']).agg({'total_cnt':'sum','move_dist' : 'mean'}).reset_index()
data_d3.to_excel(path_result + '//생활이동//추가분석//전체_유입시군구.xlsx', index=False)
#평일 휴일별 유입
data_d4 = data_d2.groupby(['월','평일구분','o_sgg','d_sgg','d_admi']).agg({'total_cnt':'sum','move_dist' : 'mean'}).reset_index()
data_d4.to_excel(path_result + '//생활이동//추가분석//평일휴일_유입시군구.xlsx', index=False)
#평일 시간대별
data_d5 = data_d2[data_d2['평일구분'] == 1]
data_d5['time_category'] = data_d5['d_time'].apply(categorize_time)
data_d5 = data_d5.groupby(['월','평일구분','time_category','o_sgg']).agg({'total_cnt':'sum','move_dist' : 'mean'}).reset_index()
data_d5.to_excel(path_result + '//생활이동//추가분석//평일시간대_유입시군구.xlsx', index=False)
#연령대별
data_d6 = data_d2.copy()
data_d6['age_00_cnt'] = data_d6['male_00_cnt'] + data_d6['feml_00_cnt']
data_d6['age_20_cnt'] = data_d6['male_20_cnt'] + data_d6['feml_20_cnt']
data_d6['age_40_cnt'] = data_d6['male_40_cnt'] + data_d6['feml_40_cnt']
data_d6['age_60_cnt'] = data_d6['male_60_cnt'] + data_d6['feml_60_cnt']

data_d6 = data_d6.groupby(['월','o_sgg']).agg({'age_00_cnt':'sum',
                                                               'age_20_cnt':'sum',
                                                               'age_40_cnt':'sum',
                                                               'age_60_cnt':'sum',
                                                               'move_dist' : 'mean'}).reset_index()
data_d6.to_excel(path_result + '//생활이동//추가분석//연령대별_유입시군구.xlsx', index=False)


## 유출 ##
#전체유출 시군구
data_o3 = data_o2.groupby(['월','o_sgg','o_admi','d_sgg']).agg({'total_cnt':'sum','move_dist' : 'mean'}).reset_index()
data_o3.to_excel(path_result + '//생활이동//추가분석//전체_유출시군구.xlsx', index=False)
#평일 휴일별 유입
data_o4 = data_o2.groupby(['월','평일구분','o_sgg','o_admi','d_sgg']).agg({'total_cnt':'sum','move_dist' : 'mean'}).reset_index()
data_o4.to_excel(path_result + '//생활이동//추가분석//평일휴일_유출시군구.xlsx', index=False)
#평일 시간대별
data_o5 = data_o2[data_o2['평일구분'] == 1]
data_o5['time_category'] = data_o5['s_time'].apply(categorize_time)
data_o5 = data_o5.groupby(['월','평일구분','time_category','d_sgg']).agg({'total_cnt':'sum','move_dist' : 'mean'}).reset_index()
data_o5.to_excel(path_result + '//생활이동//추가분석//평일시간대_유출시군구.xlsx', index=False)
#연령대별
data_o6 = data_o2.copy()
data_o6['age_00_cnt'] = data_o6['male_00_cnt'] + data_o6['feml_00_cnt']
data_o6['age_20_cnt'] = data_o6['male_20_cnt'] + data_o6['feml_20_cnt']
data_o6['age_40_cnt'] = data_o6['male_40_cnt'] + data_o6['feml_40_cnt']
data_o6['age_60_cnt'] = data_o6['male_60_cnt'] + data_o6['feml_60_cnt']

data_o6 = data_o6.groupby(['월','d_sgg']).agg({'age_00_cnt':'sum',
                                                               'age_20_cnt':'sum',
                                                               'age_40_cnt':'sum',
                                                               'age_60_cnt':'sum',
                                                               'move_dist' : 'mean'}).reset_index()
data_o6.to_excel(path_result + '//생활이동//추가분석//연령대별_유출시군구.xlsx', index=False)
















