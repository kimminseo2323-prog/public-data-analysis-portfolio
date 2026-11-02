###########################################################
# 과 제 명: A39_서초구_인구이동 및 도시계획
# 파 일 명: 0.수집 및 전처리
# 작 성 자: 김민서
###########################################################
''''''
import os, importlib, warnings;

import pandas

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
import glob
import pickle
import matplotlib.pyplot as plt
from datetime import datetime
from shapely.geometry import Point

# 격자
grid_100_s = gpd.read_file(PATH_RESULT3  + '//격자//100M격자거주인구//서초구//nlsp_021001001.shp',encoding='utf-8') #서초구 격자
grid_100_g = gpd.read_file(PATH_RESULT3  + '//격자//100M격자거주인구//강남구//nlsp_021001001.shp',encoding='utf-8') #강남구 격자

grid_100_5181_s = gpd.GeoDataFrame(grid_100_s, geometry='geometry',crs='EPSG:5179')
grid_100_5181_s = grid_100_5181_s.to_crs("EPSG:5181")
grid_100_5181_s.to_file(PATH_RESULT3 + '//격자//100M격자거주인구//grid100_seocho_5181.gpkg', driver='GPKG')

grid_100_5181_g = gpd.GeoDataFrame(grid_100_g, geometry='geometry',crs='EPSG:5179')
grid_100_5181_g = grid_100_5181_g.to_crs("EPSG:5181")
grid_100_5181_g.to_file(PATH_RESULT3 + '//격자//100M격자거주인구//grid100_gangnam_5181.gpkg', driver='GPKG')

grid_250_s = gpd.read_file(PATH_RESULT3  + '//격자//250M격자거주인구//서초구//nlsp_031001001.shp',encoding='utf-8') #서초구 격자
grid_250_5181_s = gpd.GeoDataFrame(grid_250_s, geometry='geometry',crs='EPSG:5179')
grid_250_5181_s = grid_250_5181_s.to_crs("EPSG:5181")
grid_250_5181_s.to_file(PATH_RESULT3 + '//격자//250M격자거주인구//grid250_seocho_5181.gpkg', driver='GPKG')

grid_250_g = gpd.read_file(PATH_RESULT3  + '//격자//250M격자거주인구//강남구//nlsp_031001001.shp',encoding='utf-8') #서초구 격자
grid_250_5181_g = gpd.GeoDataFrame(grid_250_g, geometry='geometry',crs='EPSG:5179')
grid_250_5181_g = grid_250_5181_g.to_crs("EPSG:5181")
grid_250_5181_g.to_file(PATH_RESULT3 + '//격자//250M격자거주인구//grid250_gangnam_5181.gpkg', driver='GPKG')

#행정경계
boundary_hjd = gpd.read_file(PATH_RESULT3 + '//경계면//행정동//BND_ADM_DONG_PG.shp',encoding='cp949')
boundary_hjd_sc = boundary_hjd[boundary_hjd['ADM_CD'].str.startswith('11220')]
boundary_hjd_sc = gpd.GeoDataFrame(boundary_hjd_sc, geometry='geometry',crs='EPSG:5186')
boundary_hjd_sc = boundary_hjd_sc.to_crs("EPSG:5181")
boundary_hjd_sc.to_file(PATH_RESULT3 + '//경계면//행정동//boundary_hjd_seocho_5181.gpkg', driver='GPKG')

boundary_hjd_gn = boundary_hjd[boundary_hjd['ADM_CD'].str.startswith('11230')]
boundary_hjd_gn = gpd.GeoDataFrame(boundary_hjd_gn, geometry='geometry',crs='EPSG:5186')
boundary_hjd_gn = boundary_hjd_gn.to_crs("EPSG:5181")
boundary_hjd_gn.to_file(PATH_RESULT3 + '//경계면//행정동//boundary_hjd_gangnam_5181.gpkg', driver='GPKG')

#집계구
boundary_oa = gpd.read_file(PATH_RESULT3 + '//경계면//집계구//BND_TOTAL_OA_PG.shp',encoding='cp949')
boundary_oa_sc = boundary_oa[boundary_oa['ADM_CD'].str.startswith('11220') ]
boundary_oa_sc = gpd.GeoDataFrame(boundary_oa_sc, geometry='geometry',crs='EPSG:5186')
boundary_oa_sc = boundary_oa_sc.to_crs("EPSG:5181")
boundary_oa_sc.to_file(PATH_RESULT3 + '//경계면//집계구//boundary_oa_seocho_5181.gpkg', driver='GPKG')

boundary_oa_gn = boundary_oa[boundary_oa['ADM_CD'].str.startswith('11230') ]
boundary_oa_gn = gpd.GeoDataFrame(boundary_oa_gn, geometry='geometry',crs='EPSG:5179')
boundary_oa_gn = boundary_oa_gn.to_crs("EPSG:5181")
boundary_oa_gn.to_file(PATH_RESULT3 + '//경계면//집계구//boundary_oa_gangnam_5181.gpkg', driver='GPKG')















