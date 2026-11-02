###########################################################
# 과 제 명: A28_수원시_주차장수요공급분석
# 파 일 명: 3. 인구데이터
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
fl.f_log_line("3. 인구데이터.py")

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
import matplotlib.pyplot as plt
from datetime import datetime
from shapely.geometry import Point

flowpop_test = pd.read_csv('D://24project//T1_GG_50CELL_FLOWPOP_202405_4111.csv')
livepop_test = pd.read_csv('D://24project//T3_GG_50CELL_LIVEPOP_202405_4111.csv')

population_columns = [col for col in flowpop_test.columns if col.endswith('_CNT')]
flowpop_test['total_cnt'] = flowpop_test[population_columns].sum(axis=1)
flowpop_test2 = flowpop_test.drop(columns=population_columns)

population_columns2 = [col for col in livepop_test.columns if col.endswith('_CNT')]
livepop_test['total_cnt_live'] = livepop_test[population_columns2].sum(axis=1)
livepop_test2 = livepop_test.drop(columns=population_columns2)

merge_columns = ['ADMI_CD', 'CTY_NM', 'ADMI_NM', 'UTMK_X', 'UTMK_Y', 'TIME_CD', 'ETL_YMD']
df_merged = pd.merge(flowpop_test2, livepop_test2, on=merge_columns, how='inner')
df_merged

base_cd_5179 = gpd.read_file(PATH_RESULT3 + '//경계면데이터//기초구역경계//기초구역경계(시군구,행정동매핑).gpkg',driver='GPKG')
sgg_hjd = gpd.read_file(PATH_RESULT3 + '//경계면데이터//행정동경계//시군구_행정동경계.gpkg',driver='GPKG') #행정동경계
org_pop_hjd = pd.read_excel(path_pretreat + '//거주인구_거주자주차장.xlsx')
org_pop_base = pd.read_excel(path_pretreat + '//거주인구_거주자주차장(기초구역).xlsx')


# 행정동별 유동인구
flow_pop_SXAGE = pd.read_excel(path_result + '//KT_인구//1.유동인구//유동인구.xlsx',sheet_name='SX_AGE')
flow_pop_DOW = pd.read_excel(path_result + '//KT_인구//1.유동인구//유동인구.xlsx',sheet_name='DOW')
flow_pop_TIME = pd.read_excel(path_result + '//KT_인구//1.유동인구//유동인구.xlsx',sheet_name='TIME')

#행정동별 서비스인구
live_pop_SXAGE = pd.read_excel(path_result + '//KT_인구//2.생활인구//2.생활인구.xlsx',sheet_name='SX_AGE_PTYPE')
live_pop_DOW = pd.read_excel(path_result + '//KT_인구//2.생활인구//2.생활인구.xlsx',sheet_name='DOW_PTYPE')
live_pop_TIME = pd.read_excel(path_result + '//KT_인구//2.생활인구//2.생활인구.xlsx',sheet_name='TIME_PTYPE')

flow_pop_SXAGE['시군구명'] = flow_pop_SXAGE['시군구명'].str.split().str[1]
flow_pop_DOW['시군구명'] = flow_pop_DOW['시군구명'].str.split().str[1]
flow_pop_TIME['시군구명'] = flow_pop_TIME['시군구명'].str.split().str[1]
live_pop_SXAGE['시군구명'] = live_pop_SXAGE['시군구명'].str.split().str[1]
live_pop_DOW['시군구명'] = live_pop_DOW['시군구명'].str.split().str[1]
live_pop_TIME['시군구명'] = live_pop_TIME['시군구명'].str.split().str[1]

flow_pop_SXAGE[(flow_pop_SXAGE['년월'] == 202302) & (flow_pop_SXAGE['시군구명'] == '권선구')]['CNT'].sum()
flow_pop_DOW[(flow_pop_DOW['년월'] == 202302) & (flow_pop_DOW['시군구명'] == '권선구')]['CNT'].sum()
flow_pop_TIME[(flow_pop_TIME['년월'] == 202302) & (flow_pop_TIME['시군구명'] == '권선구')]['CNT'].sum()


# 거주인구를 기준으로 그룹화하여 4.5개씩 나누기
# 거주인구를 기준으로 내림차순 정렬
org_pop_hjd['거주자주차장'] = org_pop_hjd['거주자주차장'].astype(int)
df_sorted = org_pop_hjd.sort_values(by='거주인구', ascending=False).reset_index(drop=True)

# 4개씩 그룹화하여 평균값 계산
num_groups = len(df_sorted) // 4 + int(len(df_sorted) % 4 > 0)  # 그룹의 수
grouped_df = df_sorted.groupby(np.arange(len(df_sorted)) // 4).agg({'거주인구': 'mean', '거주자주차장': 'sum'}).reset_index(drop=True)


df_sorted['그룹'] = np.arange(len(df_sorted)) // 4 + 1
group_info = df_sorted.groupby('그룹')['행정동명'].apply(list).reset_index() # 각 그룹별 행정동 확인
group_info.columns = ['그룹', '행정동명 목록']
grouped_df['행정동명 목록'] = group_info['행정동명 목록']

# 최종 데이터프레임
final_df = pd.concat([group_info, grouped_df], axis=1)

# 그래프 그리기
fig, ax1 = plt.subplots(figsize=(8, 4))
ax1.bar(range(num_groups), grouped_df['거주인구'], color='b', alpha=0.6, label='거주인구 그룹평균')
ax2 = ax1.twinx()
ax2.plot(range(num_groups), grouped_df['거주자주차장'], 'ro-', label='거주자주차장 합계')

ax1.set_xlabel('행정동 그룹', fontsize=14)
ax1.set_ylabel('거주인구 평균 (막대 그래프)', color='b', fontsize=14)
ax2.set_ylabel('거주자주차장 합계 (포인트 그래프)', color='r', fontsize=14)
ax1.set_xticks(range(num_groups))
ax1.set_xticklabels([f'그룹 {i+1}' for i in range(num_groups)])
plt.grid(True)

plt.show()

# 비율 계산: 거주인구 대비 거주자주차장
org_pop_hjd2 = org_pop_hjd.copy()
org_pop_hjd2['주차공급대비_거주인구_비율'] = org_pop_hjd2['거주자주차장'] / org_pop_hjd2['거주인구']

df_sorted = org_pop_hjd2.sort_values(by='주차공급대비_거주인구_비율', ascending=False)
top10_df = df_sorted.head(10)

# 그래프 그리기
plt.figure(figsize=(12, 10))
plt.barh(top10_df['행정동명'], top10_df['주차공급대비_거주인구_비율'], color='teal')
plt.xlabel('주차공급 대비 거주인구 비율', fontsize=14)
plt.ylabel('행정동명', fontsize=14)
plt.gca().invert_yaxis()  # 상위 값을 위에 표시
plt.grid(axis='x')
plt.show()

with pd.ExcelWriter(path_result + "//주차장현황//거주인구_거주자주차장.xlsx") as writer:
    org_pop_hjd2.to_excel(writer, sheet_name='Sheet1', index=False)  # 원본 데이터프레임 저장
    grouped_df.to_excel(writer, sheet_name='Sheet2')  # 그룹 평균 데이터프레임 저장




#생활인구
live_PRE = pd.read_pickle(path_data_analyze + "//생활인구//서비스인구_livepop.pkl")
live_PRE['ETL_Y'] = live_PRE['ETL_YMD'].str[:4]
live_PRE['ETL_YM'] = live_PRE['ETL_YMD'].str[:6]
live_PRE['V_SUM'] = live_PRE.filter(like='V_').sum(axis=1)
live_PRE['H_SUM'] = live_PRE.filter(like='H_').sum(axis=1)
live_PRE['W_SUM'] = live_PRE.filter(like='W_').sum(axis=1)

live_PRE_sum = live_PRE.groupby(['ETL_Y','ETL_YM','ETL_YMD','TIME_CD'])[['V_SUM','H_SUM','W_SUM']].sum().reset_index()
live_PRE_sum['total'] = live_PRE_sum[['V_SUM','H_SUM','W_SUM']].sum(axis=1)

live_PRE_sum['ETL_YMD'] = pd.to_datetime(live_PRE_sum['ETL_YMD'], format='%Y%m%d')
live_PRE_sum['ETL_DAY'] = live_PRE_sum['ETL_YMD'].dt.day_name()
live_PRE_sum['ETL_DAY2'] = live_PRE_sum['ETL_DAY'].apply(lambda x: '주말' if x in ['Saturday', 'Sunday'] else '평일')
live_PRE_sum['ETL_DAYS'] = live_PRE_sum['ETL_YM'].apply(
    lambda ym: (datetime.strptime(ym, '%Y%m') + pd.offsets.MonthEnd(0)).day
)
#live_PRE_sum['V_day'] = (live_PRE_sum['V_SUM']/live_PRE_sum['ETL_DAYS']).round(1)
#live_PRE_sum['W_day'] = (live_PRE_sum['W_SUM']/live_PRE_sum['ETL_DAYS']).round(1)
#live_PRE_sum['H_day'] = (live_PRE_sum['H_SUM']/live_PRE_sum['ETL_DAYS']).round(1)
live_PRE_sum['V_day'] = (live_PRE_sum['V_SUM']/24)
live_PRE_sum['W_day'] = (live_PRE_sum['W_SUM']/24)
live_PRE_sum['H_day'] = (live_PRE_sum['H_SUM']/24)

live_PRE_sum.to_excel(path_result + '//KT_인구//2.생활인구//3.생활인구.xlsx',index=False)



#2024.05기준 추가 현황분석(생활인구)
test_service = pd.read_csv('F:\\24Project\\A28_수원시\\202405\\T3_GG_50CELL_LIVEPOP_202405_4111.csv')
test_service['ETL_YMD'] =test_service['ETL_YMD'].astype(str)
test_service['ETL_YM'] = test_service['ETL_YMD'].str[:6]
test_service['V_SUM'] = test_service.filter(like='V_').sum(axis=1)
test_service['H_SUM'] = test_service.filter(like='H_').sum(axis=1)
test_service['W_SUM'] = test_service.filter(like='W_').sum(axis=1)

live2405 = test_service[['ETL_YM', 'ETL_YMD','ADMI_CD', 'CTY_NM', 'ADMI_NM', 'UTMK_X', 'UTMK_Y', 'TIME_CD','V_SUM', 'H_SUM', 'W_SUM']]
live2405['ETL_YMD'] = pd.to_datetime(live2405['ETL_YMD'], format='%Y%m%d')
live2405['ETL_DAY'] = live2405['ETL_YMD'].dt.day_name()
live2405['ETL_DAY2'] = live2405['ETL_DAY'].apply(lambda x: '주말' if x in ['Saturday', 'Sunday'] else '평일')
live2405['ETL_DAYS'] = live2405['ETL_YM'].apply(
    lambda ym: (datetime.strptime(ym, '%Y%m') + pd.offsets.MonthEnd(0)).day
)

live2405['total'] = live2405[['V_SUM', 'H_SUM', 'W_SUM']].sum(axis=1)
live2405_daysum = live2405.groupby(['ETL_YMD','ADMI_NM','ETL_DAY','ETL_DAY2','TIME_CD'])[['V_SUM','H_SUM','W_SUM','total']].sum().reset_index()

#live2405_daysum.to_csv(path_result + '//KT_인구//2.생활인구//4.생활인구_202405.csv',encoding='cp949', index=False)
live2405_daysum.to_excel(path_result + '//KT_인구//2.생활인구//4.생활인구_202405.xlsx', index=False)

#(동료) 요청데이터
#2024.05기준 추가 현황분석(생활인구)
base_cd_5179 = gpd.read_file(PATH_RESULT3 + '//경계면데이터//기초구역경계//기초구역경계.gpkg',driver='GPKG')
base_cd_pop5179 = gpd.read_file(PATH_RESULT3 + '//거주인구//기초구역경계_거주인구.gpkg',driver='GPKG')
test_service = pd.read_csv('F:\\24Project\\A28_수원시\\202405\\T3_GG_50CELL_LIVEPOP_202405_4111.csv')
test_service['ETL_YMD'] =test_service['ETL_YMD'].astype(str)
test_service['ETL_YM'] = test_service['ETL_YMD'].str[:6]
test_service['V_SUM'] = test_service.filter(like='V_').sum(axis=1)
test_service['H_SUM'] = test_service.filter(like='H_').sum(axis=1)
test_service['W_SUM'] = test_service.filter(like='W_').sum(axis=1)

live2405 = test_service[['ETL_YM', 'ETL_YMD','ADMI_CD', 'CTY_NM', 'ADMI_NM', 'UTMK_X', 'UTMK_Y', 'TIME_CD','V_SUM', 'H_SUM', 'W_SUM']]
live2405['ETL_YMD'] = pd.to_datetime(live2405['ETL_YMD'], format='%Y%m%d')
live2405['ETL_DAY'] = live2405['ETL_YMD'].dt.day_name()
live2405['ETL_DAY2'] = live2405['ETL_DAY'].apply(lambda x: '주말' if x in ['Saturday', 'Sunday'] else '평일')
live2405['ETL_DAYS'] = live2405['ETL_YM'].apply(
    lambda ym: (datetime.strptime(ym, '%Y%m') + pd.offsets.MonthEnd(0)).day
)
live2405['total'] = live2405[['V_SUM', 'H_SUM', 'W_SUM']].sum(axis=1)
live2405['geometry'] = live2405.apply(lambda row: Point(row['UTMK_X'], row['UTMK_Y']), axis=1)
live2405_5179 = gpd.GeoDataFrame(live2405, geometry='geometry', crs = 'EPSG:5179')
live2405_5179 = live2405_5179.to_crs(epsg=5179)

live2405_5179_gdf = gpd.sjoin(live2405_5179, base_cd_5179, how='left', op='within')
live2405_5179_gdf = live2405_5179_gdf[['ETL_YM', 'ETL_YMD',  'ADMI_NM','기초구역번호','면적','TIME_CD', 'V_SUM','H_SUM', 'W_SUM', 'ETL_DAY', 'ETL_DAY2','geometry']]
live2405_5179_gdf2 = live2405_5179_gdf[live2405_5179_gdf['TIME_CD'].isin([0, 14])]
live2405_5179_gdf3 = live2405_5179_gdf2[live2405_5179_gdf2['ETL_DAY2'] == '평일']

columns_to_sort = ['ETL_YM', 'ETL_YMD', 'ADMI_NM', '기초구역번호']
live2405_5179_gdf4 = live2405_5179_gdf3.sort_values(by=columns_to_sort)
live2405_5179_gdf4.columns
live2405_5179_gdf5 = live2405_5179_gdf4.groupby(['ETL_YM', 'ETL_Y[MD', 'ADMI_NM', '기초구역번호', '면적','TIME_CD'])[[ 'V_SUM','H_SUM', 'W_SUM']].sum().reset_index()
live2405_5179_gdf6 = pd.merge(live2405_5179_gdf5,base_cd_pop5179[['기초구역번호','population']],on='기초구역번호',how='left')
live2405_5179_gdf6.rename(columns={'population':'거주인구'},inplace=True)

live2405_5179_gdf6.to_pickle(path_result + '//KT_인구//2.생활인구//5.생활인구(평일,0,14,기초구역).pkl')
live2405_5179_gdf6 = pd.read_pickle(path_result + '//KT_인구//2.생활인구//5.생활인구(평일,0,14,기초구역).pkl')

#생활인구 최근 한달치 행정동 및 기초구역 매핑
base_cd_5179 = gpd.read_file(PATH_RESULT3 + '//경계면데이터//기초구역경계//기초구역경계(시군구,행정동매핑).gpkg',driver='GPKG')
livepop_202405 = pd.read_csv('F://24Project//A28_수원시//202405//T3_GG_50CELL_LIVEPOP_202405_4111.csv',encoding='utf-8')
livepop_202405.columns
df_selected2 = livepop_202405[['ADMI_CD', 'CTY_NM', 'ADMI_NM', 'UTMK_X', 'UTMK_Y']]
df_unique2 = df_selected2.drop_duplicates(subset=['UTMK_X', 'UTMK_Y'])
df_unique2['geometry'] = df_unique2.apply(lambda row: Point(row['UTMK_X'], row['UTMK_Y']), axis=1)

df_unique2 = df_unique2.drop_duplicates(subset=['geometry'])
points_gdf2 = gpd.GeoDataFrame(df_unique2, geometry='geometry',crs='EPSG:5179')

#pkl생성
livepop_202405_2 = gpd.sjoin(points_gdf2, base_cd_5179, how='left', op='within')
livepop_202405_2.to_file(PATH_RESULT3 + '//생활인구//생활인구_기초구역매핑.gpkg', driver='GPKG')
livepop_202405_2 = livepop_202405_2[['HJD_CD', 'HJD_NM','기초구역번호', 'UTMK_X', 'UTMK_Y']]
livepop_202405_2 = livepop_202405_2.drop_duplicates(subset=['UTMK_X', 'UTMK_Y'])
livepop_202405_2.to_pickle(path_result + '//KT_인구//2.생활인구//최근한달생활인구_기초구역매핑.pkl')
livepop_202405_2.nunique()


#유동인구 최근 한달치 행정동 및 기초구역 매핑
base_cd_5179 = gpd.read_file(PATH_RESULT3 + '//경계면데이터//기초구역경계//기초구역경계(시군구,행정동매핑).gpkg',driver='GPKG')
flowpop_202405 = pd.read_csv('G://24Project//A28_수원시//202405//T1_GG_50CELL_FLOWPOP_202405_4111.csv',encoding='utf-8')
flowpop_202405.columns

df_selected = flowpop_202405[['ADMI_CD', 'CTY_NM', 'ADMI_NM', 'UTMK_X', 'UTMK_Y']]

df_unique = df_selected.drop_duplicates(subset=['UTMK_X', 'UTMK_Y'])
df_unique['geometry'] = df_unique.apply(lambda row: Point(row['UTMK_X'], row['UTMK_Y']), axis=1)

df_unique = df_unique.drop_duplicates(subset=['geometry'])
points_gdf = gpd.GeoDataFrame(df_unique, geometry='geometry',crs='EPSG:5179')
#pkl생성
flowpop_202405_2 = gpd.sjoin(points_gdf, base_cd_5179, how='left', op='within')
flowpop_202405_2.to_file(PATH_RESULT3 + '//유동인구//유동인구_기초구역매핑.gpkg', driver='GPKG')
flowpop_202405_2.columns

flowpop_202405_2 = flowpop_202405_2[['HJD_CD', 'HJD_NM','기초구역번호', 'UTMK_X', 'UTMK_Y']]
flowpop_202405_2 = flowpop_202405_2.drop_duplicates(subset=['UTMK_X', 'UTMK_Y'])
flowpop_202405_2.to_pickle(path_result + '//KT_인구//1.유동인구//최근한달유동인구_기초구역매핑.pkl')



#유동인구 최근 한달치 행정동 및 기초구역 매핑
base_cd_5179 = gpd.read_file(PATH_RESULT3 + '//경계면데이터//기초구역경계//기초구역경계(시군구,행정동매핑).gpkg',driver='GPKG')
flowpop_202405 = pd.read_csv('G://24Project//A28_수원시//202405//T1_GG_50CELL_FLOWPOP_202405_4111.csv',encoding='utf-8')
flowpop_202405_2 = pd.read_pickle(path_result + '//KT_인구//1.유동인구//최근한달유동인구_기초구역매핑.pkl')
parking11_geo = gpd.read_file(PATH_RESULT3 + '//공급분석//기초구역별_주차장공급.gpkg',driver='GPKG')

flowpop_202405.columns
flowpop_202405['flowpop_M_SUM'] = flowpop_202405.filter(like='M_').sum(axis=1)
flowpop_202405['flowpop_F_SUM'] = flowpop_202405.filter(like='F_').sum(axis=1)
flowpop_202405['flowpop_sum'] = flowpop_202405['flowpop_M_SUM'] + flowpop_202405['flowpop_F_SUM']
flowpop_202405.columns
f2405 = flowpop_202405[['ADMI_CD', 'CTY_NM', 'ADMI_NM', 'UTMK_X', 'UTMK_Y', 'TIME_CD','flowpop_M_SUM','flowpop_F_SUM', 'flowpop_sum']]
f2405['geometry'] = f2405.apply(lambda row: Point(row['UTMK_X'], row['UTMK_Y']), axis=1)
f2405_g2 = gpd.GeoDataFrame(f2405, geometry='geometry',crs='EPSG:5179')
f2405_g3 = gpd.sjoin(f2405_g2, base_cd_5179, how='left', op='within')

f2405_g = f2405_g3.groupby(['기초구역번호','TIME_CD'])[['flowpop_M_SUM','flowpop_F_SUM', 'flowpop_sum']].mean().reset_index()


f2405_RE = pd.merge(base_cd_5179,f2405_g,on='기초구역번호',how='left')
f2405_RE.columns
f2405_RE = f2405_RE[['HJD_CD', 'HJD_NM','기초구역번호','TIME_CD', 'flowpop_M_SUM', 'flowpop_F_SUM', 'flowpop_sum', 'geometry']]
f2405_RE.to_file(PATH_RESULT3 + '//유동인구//최근한달유동인구(시간평균)_기초구역매핑.gpkg', driver='GPKG')


f2405_RE_g = f2405_RE.groupby(['기초구역번호'])[['flowpop_M_SUM','flowpop_F_SUM', 'flowpop_sum']].sum().reset_index()
f2405_RE_g = pd.merge(base_cd_5179,f2405_RE_g,on='기초구역번호',how='left')
f2405_RE_g = gpd.GeoDataFrame(f2405_RE_g, geometry='geometry',crs='EPSG:5179')
f2405_RE_g.to_file(PATH_RESULT3 + '//유동인구//기초구역경계_유동인구(최근한달).gpkg', driver='GPKG')
#1. 기초구역별 유동인구 대비 주차장공급비율
## -7시 12시 20시
f2405_RE = gpd.read_file(PATH_RESULT3 + '//유동인구//최근한달유동인구(시간평균)_기초구역매핑.gpkg', driver='GPKG')
f2405_RE_07 = f2405_RE[f2405_RE['TIME_CD']==7]
f2405_RE_12 = f2405_RE[f2405_RE['TIME_CD']==12]
f2405_RE_20 = f2405_RE[f2405_RE['TIME_CD']==20]
f2405_RE_07.columns
f2405_RE_07 = pd.merge(base_cd_5179,f2405_RE_07[[ '기초구역번호', 'TIME_CD', 'flowpop_M_SUM','flowpop_F_SUM', 'flowpop_sum']],on='기초구역번호',how='left')
f2405_RE_12 = pd.merge(base_cd_5179,f2405_RE_12[[ '기초구역번호', 'TIME_CD', 'flowpop_M_SUM','flowpop_F_SUM', 'flowpop_sum']],on='기초구역번호',how='left')
f2405_RE_20 = pd.merge(base_cd_5179,f2405_RE_20[[ '기초구역번호', 'TIME_CD', 'flowpop_M_SUM','flowpop_F_SUM', 'flowpop_sum']],on='기초구역번호',how='left')

f2405_RE_07.fillna(0.0, inplace=True)
f2405_RE_12.fillna(0.0, inplace=True)
f2405_RE_20.fillna(0.0, inplace=True)

f2405_RE_07.to_file(PATH_RESULT3 + '//유동인구//최근한달유동인구(시간평균)_7시_기초구역매핑.gpkg', driver='GPKG')
f2405_RE_12.to_file(PATH_RESULT3 + '//유동인구//최근한달유동인구(시간평균)_12시_기초구역매핑.gpkg', driver='GPKG')
f2405_RE_20.to_file(PATH_RESULT3 + '//유동인구//최근한달유동인구(시간평균)_20시_기초구역매핑.gpkg', driver='GPKG')

# 최근한달 유동인구 대비 주차장공급비율
parking11_geo
parking11_geo.columns
parking_r = pd.merge(parking11_geo,f2405_RE_g,on=['HJD_CD','HJD_NM','기초구역번호','geometry'],how='left')
parking_r['주차장공급비율(%)'] = ((parking_r['총주차면수'] / parking_r['flowpop_sum'])*100).round(1)
parking_r
parking_r2 = parking_r[['HJD_CD', 'HJD_NM', '기초구역번호','flowpop_sum','총주차면수','주차장공급비율(%)','geometry']]
parking_r2 = gpd.GeoDataFrame(parking_r2, geometry='geometry', crs='EPSG:5179')
parking_r2.to_file(PATH_RESULT3 + '//유동인구//유동인구대비분석.gpkg',driver='GPKG')


'''
#카드데이터 기초구역 매핑
base_geo = gpd.read_file(PATH_RESULT3 + '//경계면데이터//기초구역경계//기초구역경계.gpkg')
card_data = pd.read_pickle(path_result + '//카드분석//card_blkamt.pkl')
base_geo = base_geo[['기초구역번호','geometry']]
card_map = pd.merge(base_geo,card_data,on='기초구역번호',how='left')
card_map.fillna(0,inplace=True)
card_map = card_map[['SGG_NM', 'HJD_NM','기초구역번호','공공', '공연', '미디', '생활', '소매',
       '여가', '음식', '의료', '학문', '카드총액', '노상', '노외', '부설', '주차장',
       '소매비율', '음식비율', '의료비율', '학문비율', 'geometry']]
card_map = gpd.GeoDataFrame(card_map, geometry='geometry', crs='EPSG:5179')
card_map.to_file(PATH_RESULT3 + '//카드분석//카드분석결과.gpkg',driver='GPKG')

card_data2 = card_data[['SGG_NM', 'HJD_NM', '기초구역번호', '공공', '공연', '미디', '생활', '소매', '여가', '음식','의료', '학문', '카드총액']]
'''


