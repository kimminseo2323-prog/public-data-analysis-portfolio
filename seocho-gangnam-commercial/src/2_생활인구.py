###########################################################
# 과 제 명: A39_서초구_인구이동 및 도시계획
# 파 일 명: 생활인구 분석
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
from datetime import datetime, timedelta


#격자
grid_250_5181_s = gpd.read_file(PATH_RESULT3 + '//격자//250M격자거주인구//grid250_seocho_5181.gpkg', driver='GPKG')
grid_250_5181_g = gpd.read_file(PATH_RESULT3 + '//격자//250M격자거주인구//grid250_gangnam_5181.gpkg', driver='GPKG')
grid_250_sg = pd.concat([grid_250_5181_s, grid_250_5181_g])

#행정경계
boundary_hjd_sc = gpd.read_file(PATH_RESULT3 + '//경계면//행정동//boundary_hjd_seocho_5181.gpkg', driver='GPKG')
boundary_hjd_gn = gpd.read_file(PATH_RESULT3 + '//경계면//행정동//boundary_hjd_gangnam_5181.gpkg', driver='GPKG')

#집계구
boundary_oa_sc = gpd.read_file(PATH_RESULT3 + '//경계면//집계구//boundary_oa_seocho_5181.gpkg', driver='GPKG')
boundary_oa_gn = gpd.read_file(PATH_RESULT3 + '//경계면//집계구//boundary_oa_gangnam_5181.gpkg', driver='GPKG')

# 250M 격자 매핑키
id_key = pd.read_excel(path_data_analyze + '//서초구 ID key.xlsx')
id_key1 = id_key[['gid','생활인구_cell_id']].drop_duplicates()
id_key2 = id_key[['gid','생활이동인구_cell_id']].drop_duplicates()


# 250M 생활이동 unique 격자 id
move_point_gdf = gpd.read_file(path_data_analyze+'//move_point_id_2024.gpkg',driver='GPKG')
move_point_gdf = move_point_gdf.rename(columns={'id' : 'CELL_ID'})
move_point_gdf
# 서초구 제공 생활인구 데이터 전처리
live_pop =pd.read_csv(path_data_in + '//생활인구//생활인구_서초구_202301-202406.csv',encoding='utf-8')
live_pop_g = pd.merge(live_pop, move_point_gdf[['CELL_ID', 'hjd_cd', 'geometry']], on='CELL_ID', how='left')
live_pop_g.to_pickle('D://24project//A39_서초구 인구이동 및 도시계획 분석//2.analyze//생활인구//spop_232406.pkl')
## 전체 생활인구  7842817969.490008 명 중 197732458.77999985 가 널값에 해당되는 생활인구 ( 약 2%로 제외함)

# 250M 격자 매핑키
id_key = pd.read_excel(path_data_analyze + '//서초구 ID key.xlsx')
id_key = id_key[['gid','생활인구_cell_id']].drop_duplicates()

live_pop_g = pd.read_pickle('D://24project//A39_서초구 인구이동 및 도시계획 분석//2.analyze//생활인구//spop_232406.pkl')
#live_pop_g = gpd.GeoDataFrame(live_pop_g, geometry='geometry',crs='EPSG:5179')
#live_pop_g = live_pop_g.to_crs('EPSG:5181')
live_pop_g.rename(columns={'CELL_ID':'생활인구_cell_id'},inplace=True)
live_pop_gid = live_pop_g[['YMD', 'TT', 'H_DNG_CD', '생활인구_cell_id', 'SPOP', 'M00', 'M20', 'M40','M60', 'F00', 'F20', 'F40', 'F60', 'hjd_cd']]
live_pop_gid = pd.merge(live_pop_gid,id_key,on='생활인구_cell_id',how='left')

livepop_250_grid = pd.merge(grid_250_sg,live_pop_gid,on='gid',how='left')
livepop_250_grid = livepop_250_grid[['gid','생활인구_cell_id', 'lbl', 'val', 'YMD', 'TT', 'H_DNG_CD','SPOP', 'M00', 'M20', 'M40', 'M60', 'F00', 'F20', 'F40','F60', 'geometry']]
livepop_250_grid = gpd.GeoDataFrame(livepop_250_grid, geometry='geometry',crs='EPSG:5181')
livepop_250_grid.to_file(path_pretreat + '//생활인구//livepop_250_grid.gpkg', driver='GPKG')

def categorize_time(hour):
    if hour == 0:
        adjusted_hour = 24
    else:
        adjusted_hour = hour
    if 11 <= adjusted_hour < 14:
        return '점심'
    elif 14 <= adjusted_hour < 17:
        return '오후'
    elif 18 <= adjusted_hour <= 21:
        return '저녁'
    else:
        return None

livepop_250_grid = gpd.read_file(path_pretreat + '//생활인구//livepop_250_grid.gpkg', driver='GPKG')
livepop_250_grid

# 생활인구 커널밀도함수
gdf = livepop_250_grid.copy()
gdf.isnull().sum()
gdf = gdf[gdf['YMD'].notnull()]

gdf['YMD'] = gdf['YMD'].astype(str).str.split('.').str[0]
gdf['YMD'] = pd.to_datetime(gdf['YMD'], format='%Y%m%d', errors='coerce')
gdf['year'] = gdf['YMD'].dt.year
gdf['month'] = gdf['YMD'].dt.month
gdf['year_month'] = gdf['YMD'].dt.to_period('M').astype(str)

recent_year_month = '2024-04' # 최근한달 기준 - 거주인구와 비교 이유
recent_data = gdf[gdf['year_month'] == recent_year_month]

#population_columns = ['SPOP', 'M00', 'M20', 'M40', 'M60', 'F00', 'F20', 'F40', 'F60'] # 생활인구 관련 컬럼
aggregated_data = recent_data.groupby('생활인구_cell_id')['SPOP'].sum().reset_index()
aggregated_gdf = recent_data.drop_duplicates('생활인구_cell_id')[['생활인구_cell_id', 'geometry']].merge(aggregated_data,on='생활인구_cell_id')
aggregated_gdf.to_file(PATH_RESULT3 + '//격자//생활인구//생활인구_250M_202404.gpkg', driver='GPKG')


# 거주인구 밀집 VS 생활이동 평균이동거리 (유입기준)
data_244 = pd.read_pickle('D://24project//A39_서초구 인구이동 및 도시계획 분석//2.analyze//생활이동//3.행정동정보//도착기준//mv_2024_4_d.pkl')
data_244['평일구분'] = data_244['요일'].apply(lambda x: 0 if x in ['Saturday', 'Sunday'] else 1)
data_244 = data_244[['연도', '월', 'date', '요일','평일구분', 'd_time', 'd_cell_id','d_cell_tp',
             'o_admi_cd', 'd_admi_cd', 'o_sgg', 'o_admi', 'o_full', 'd_sgg','d_admi', 'd_full',
             'move_purpose', 'move_dist', 'move_time', 'total_cnt',
             'male_00_cnt', 'male_20_cnt','male_40_cnt', 'male_60_cnt',
             'feml_00_cnt', 'feml_20_cnt','feml_40_cnt', 'feml_60_cnt']]
data_244_sort = data_244.sort_values(by=['연도', '월', 'date', '요일','평일구분','d_admi', 'd_time','d_cell_id'], ascending=True)
data_244_sort_seocho = data_244_sort[data_244_sort['d_sgg'] == '서초구']
data_244_sort_seocho['time_category'] = data_244_sort_seocho['d_time'].apply(categorize_time)

external_inflow_data = data_244_sort_seocho[data_244_sort_seocho['o_sgg'] != '서초구']  # 서초구 외부에서 유입된 데이터 필터링
grid_avg_move_dist = external_inflow_data.groupby('d_cell_id')['move_dist'].mean().reset_index()
grid_avg_move_dist = pd.merge(grid_avg_move_dist,id_key2,left_on='d_cell_id',right_on='생활이동인구_cell_id',how='left')
grid_avg_move_dist2 = pd.merge(grid_250_5181_s,grid_avg_move_dist,on='gid',how='left')
grid_avg_move_dist2 = grid_avg_move_dist2[grid_avg_move_dist2['생활이동인구_cell_id'].notnull()]
grid_avg_move_dist2.to_file(PATH_RESULT3 + '//격자//생활이동//유입기준_평균이동거리_202404.gpkg', driver='GPKG')


# 시간대별 생활인구 vs 시간대별 유입인구
# 생활인구 필터링
recent_data['time_category'] = recent_data['TT'].apply(categorize_time)
living_data_filtered2 = recent_data[['gid', 'year', 'month', 'year_month','SPOP', 'time_category', 'geometry']]
living_data_filtered_1 = living_data_filtered2[living_data_filtered2['time_category'] == '점심']
living_data_filtered_2 = living_data_filtered2[living_data_filtered2['time_category'] == '오후']
living_data_filtered_3 = living_data_filtered2[living_data_filtered2['time_category'] == '저녁']

living_data_filtered_1 = living_data_filtered_1.groupby(['gid','geometry'])['SPOP'].mean().reset_index()
living_data_filtered_2 = living_data_filtered_2.groupby(['gid','geometry'])['SPOP'].mean().reset_index()
living_data_filtered_3 = living_data_filtered_3.groupby(['gid','geometry'])['SPOP'].mean().reset_index()

living_data_filtered_1 = gpd.GeoDataFrame(living_data_filtered_1, geometry='geometry')
living_data_filtered_2 = gpd.GeoDataFrame(living_data_filtered_2, geometry='geometry')
living_data_filtered_3 = gpd.GeoDataFrame(living_data_filtered_3, geometry='geometry')

living_data_filtered_1.to_file(PATH_RESULT3 + '//격자//생활인구//점심기준_평균생활인구_202404.gpkg', driver='GPKG')
living_data_filtered_2.to_file(PATH_RESULT3 + '//격자//생활인구//오후기준_평균생활인구_202404.gpkg', driver='GPKG')
living_data_filtered_3.to_file(PATH_RESULT3 + '//격자//생활인구//저녁기준_평균생활인구_202404.gpkg', driver='GPKG')


#유입기준

#행정동별 산출
## 시간대별 평균이동거리
#data_244 = pd.read_pickle('D://24project//A39_서초구 인구이동 및 도시계획 분석//2.analyze//생활이동//3.행정동정보//도착기준//mv_2024_4_d.pkl')
data_244['평일구분'] = data_244['요일'].apply(lambda x: 0 if x in ['Saturday', 'Sunday'] else 1)
data_244 = data_244[['연도', '월', 'date', '요일','평일구분', 'd_time', 'd_cell_id','d_cell_tp',
             'o_admi_cd', 'd_admi_cd', 'o_sgg', 'o_admi', 'o_full', 'd_sgg','d_admi', 'd_full',
             'move_purpose', 'move_dist', 'move_time', 'total_cnt',
             'male_00_cnt', 'male_20_cnt','male_40_cnt', 'male_60_cnt',
             'feml_00_cnt', 'feml_20_cnt','feml_40_cnt', 'feml_60_cnt']]
data_244_sort = data_244.sort_values(by=['연도', '월', 'date', '요일','평일구분', 'd_time','d_cell_id'], ascending=True)
data_244_sort_seocho = data_244_sort[data_244_sort['d_sgg'] == '서초구']
external_inflow_data4 = data_244_sort_seocho[data_244_sort_seocho['o_sgg'] != '서초구']  # 서초구 외부에서 유입된 데이터 필터링
external_inflow_data4['time_category'] = external_inflow_data4['d_time'].apply(categorize_time)

hjd_avg_move_dist_4 = external_inflow_data4[[  'd_admi', 'time_category', 'move_dist']]
hjd_avg_move_dist2 = hjd_avg_move_dist_4[hjd_avg_move_dist_4['d_admi'].notnull()]
hjd_avg_move_dist_1 = hjd_avg_move_dist2[hjd_avg_move_dist2['time_category'] == '점심']
hjd_avg_move_dist_2 = hjd_avg_move_dist2[hjd_avg_move_dist2['time_category'] == '오후']
hjd_avg_move_dist_3 = hjd_avg_move_dist2[hjd_avg_move_dist2['time_category'] == '저녁']
hjd_avg_move_dist_1 = hjd_avg_move_dist_1.groupby('d_admi')['move_dist'].mean().reset_index()
hjd_avg_move_dist_2 = hjd_avg_move_dist_2.groupby('d_admi')['move_dist'].mean().reset_index()
hjd_avg_move_dist_3 = hjd_avg_move_dist_3.groupby('d_admi')['move_dist'].mean().reset_index()
hjd_avg_move_dist_1.to_excel(path_result + '//생활이동//행정동별_점심기준_유입인구_평균이동거리_202404.xlsx', index='false')
hjd_avg_move_dist_2.to_excel(path_result + '//생활이동//행정동별_오후기준_유입인구_평균이동거리_202404.xlsx', index='false')
hjd_avg_move_dist_3.to_excel(path_result + '//생활이동//행정동별_저녁기준_유입인구_평균이동거리_202404.xlsx', index='false')
#####################################################################################################################

external_inflow_data4 = external_inflow_data4[[ 'd_cell_id','연도', '월', 'time_category', 'move_dist']]
grid_avg_move_dist = external_inflow_data4.copy()
grid_avg_move_dist2 = grid_avg_move_dist[grid_avg_move_dist['d_cell_id'].notnull()]
grid_avg_move_dist_1 = grid_avg_move_dist2[grid_avg_move_dist2['time_category'] == '점심']
grid_avg_move_dist_2 = grid_avg_move_dist2[grid_avg_move_dist2['time_category'] == '오후']
grid_avg_move_dist_3 = grid_avg_move_dist2[grid_avg_move_dist2['time_category'] == '저녁']

grid_avg_move_dist_1 = grid_avg_move_dist_1.groupby('d_cell_id')['move_dist'].mean().reset_index()
grid_avg_move_dist_2 = grid_avg_move_dist_2.groupby('d_cell_id')['move_dist'].mean().reset_index()
grid_avg_move_dist_3 = grid_avg_move_dist_3.groupby('d_cell_id')['move_dist'].mean().reset_index()

grid_avg_move_dist_1 = pd.merge(grid_avg_move_dist_1,id_key2,left_on='d_cell_id',right_on='생활이동인구_cell_id',how='left')
grid_avg_move_dist_1 = pd.merge(grid_250_5181_s,grid_avg_move_dist_1,on='gid',how='left')
grid_avg_move_dist_1 = grid_avg_move_dist_1[['gid','move_dist','geometry']]
grid_avg_move_dist_2 = pd.merge(grid_avg_move_dist_2,id_key2,left_on='d_cell_id',right_on='생활이동인구_cell_id',how='left')
grid_avg_move_dist_2 = pd.merge(grid_250_5181_s,grid_avg_move_dist_2,on='gid',how='left')
grid_avg_move_dist_2 = grid_avg_move_dist_2[['gid','move_dist','geometry']]
grid_avg_move_dist_3 = pd.merge(grid_avg_move_dist_3,id_key2,left_on='d_cell_id',right_on='생활이동인구_cell_id',how='left')
grid_avg_move_dist_3 = pd.merge(grid_250_5181_s,grid_avg_move_dist_3,on='gid',how='left')
grid_avg_move_dist_3 = grid_avg_move_dist_3[['gid','move_dist','geometry']]

grid_avg_move_dist_1 = gpd.GeoDataFrame(grid_avg_move_dist_1, geometry='geometry')
grid_avg_move_dist_2 = gpd.GeoDataFrame(grid_avg_move_dist_2, geometry='geometry')
grid_avg_move_dist_3 = gpd.GeoDataFrame(grid_avg_move_dist_3, geometry='geometry')

grid_avg_move_dist_1.to_file(PATH_RESULT3 + '//격자//생활이동//점심기준_유입인구_평균이동거리_202404.gpkg', driver='GPKG')
grid_avg_move_dist_2.to_file(PATH_RESULT3 + '//격자//생활이동//오후기준_유입인구_평균이동거리_202404.gpkg', driver='GPKG')
grid_avg_move_dist_3.to_file(PATH_RESULT3 + '//격자//생활이동//저녁기준_유입인구_평균이동거리_202404.gpkg', driver='GPKG')




# 추가분석
gdf = livepop_250_grid.copy()
gdf.isnull().sum()
gdf = gdf[gdf['YMD'].notnull()]

gdf['YMD'] = gdf['YMD'].astype(str).str.split('.').str[0]
gdf['YMD'] = pd.to_datetime(gdf['YMD'], format='%Y%m%d', errors='coerce')
gdf['year'] = gdf['YMD'].dt.year
gdf['month'] = gdf['YMD'].dt.month
gdf['year_month'] = gdf['YMD'].dt.to_period('M').astype(str)
gdf['요일'] = gdf['YMD'].dt.day_name()

recent_year_month = '2024-05' # 최근한달 기준
recent_data = gdf[gdf['year_month'] == recent_year_month]

recent_data['평일구분'] = recent_data['요일'].apply(lambda x: 0 if x in ['Saturday', 'Sunday'] else 1)
recent_data.to_pickle(path_data_analyze + '//생활인구//생활인구_202405.pkl')

recent_data_weekday = recent_data[recent_data['평일구분'] == 1]
recent_data_weekend = recent_data[recent_data['평일구분'] == 0]

#평일주말 시간대별 생활인구 분포
#recent_data_weekday_g = recent_data_weekday.groupby(['YMD','TT'])['SPOP'].mean().reset_index()
recent_data_weekday_g = recent_data_weekday.groupby(['YMD','TT'])['SPOP'].sum().reset_index()
recent_data_weekday_g = recent_data_weekday_g.groupby('TT')['SPOP'].mean().reset_index()
recent_data_weekday_g.to_excel(path_result + '//생활인구//평일시간대별_생활인구_202405.xlsx', index=False)

recent_data_weekend_g = recent_data_weekend.groupby(['YMD','TT'])['SPOP'].sum().reset_index()
recent_data_weekend_g = recent_data_weekend_g.groupby('TT')['SPOP'].mean().reset_index()
recent_data_weekend_g.to_excel(path_result + '//생활인구//주말시간대별_생활인구_202405.xlsx', index=False)



#추가분석 - 행정동별 밀집도 수치값 계산 (엑셀)
code = pd.read_excel(path_data_out + '//전국_행정동_코드정보//통계청_행안부코드.xlsx')
#행정동별 면적계산
boundary_hjd_sc_area = boundary_hjd_sc.copy()
boundary_hjd_sc_area['area_m2'] = boundary_hjd_sc_area.geometry.area
# 면적을 제곱킬로미터로 변환 (옵션)
boundary_hjd_sc_area['area_km2'] = (boundary_hjd_sc_area['area_m2'] / 1e6).round(2)
boundary_hjd_sc_area['area_km2'].sum() # 47km2
boundary_hjd_sc_area = boundary_hjd_sc_area[['ADM_NM', 'ADM_CD', 'geometry', 'area_m2', 'area_km2']]
boundary_hjd_sc_area['ADM_CD'] = boundary_hjd_sc_area['ADM_CD'].astype(int)
boundary_hjd_sc_area_code = pd.merge(boundary_hjd_sc_area,code,left_on='ADM_CD',right_on='통계청코드',how='left')
boundary_hjd_sc_area_code = boundary_hjd_sc_area_code[['행정동명','통계청코드', '행안부코드','area_m2', 'area_km2', 'geometry']]
boundary_hjd_sc_area_code
#거주인구_202404
lpop_202404 = pd.read_excel(path_data_out + '//행정동별_주민등록인구_202404.xlsx') #거주인구
#거주인구 밀집도
result1 = pd.merge(boundary_hjd_sc_area_code,lpop_202404[['행정동명','총인구수']],on='행정동명',how='left')
result1['val_per_km2'] = (result1['총인구수'] / result1['area_km2']).round(1) # 면적 대비 거주인구 계산

#생활인구_202404
spop = pd.read_csv(path_data_out + '//서울열린데이터광장//LOCAL_PEOPLE_DONG_202404.csv', index_col=False)
filtered_df = spop[spop['행정동코드'].astype(str).str.startswith('11650')]
spop_sc = filtered_df[['기준일ID', '시간대구분', '행정동코드', '총생활인구수']]
spop_time = spop_sc.groupby('시간대구분')['총생활인구수'].sum().reset_index()
spop_time.to_excel(path_result + '//생활인구//시간대별_합계_202404기준.xlsx', index=False) # 오후 2시가 최댓값임으로 오후 2시로 밀집도 산출
spop_sc_14 = spop_sc[spop_sc['시간대구분'] == 14]
spop_sc_14 = spop_sc_14.groupby('행정동코드')['총생활인구수'].mean().reset_index()
spop_sc_14.rename(columns={'행정동코드':'행안부코드'}, inplace=True)
#거주인구 밀집도
result1 = pd.merge(result1,spop_sc_14[['행안부코드','총생활인구수']],on='행안부코드',how='left')
result1['spop_per_km2'] = (result1['총생활인구수'] / result1['area_km2']).round(1) # 면적 대비 거주인구 계산
result1.to_excel(path_result + '//생활인구//거주인구_생활인구_밀집도_202404.xlsx', index=False)


# 생활인구 시간대별 수치값 계산
spop = pd.read_csv(path_data_out + '//서울열린데이터광장//LOCAL_PEOPLE_DONG_202404.csv', index_col=False)
filtered_df = spop[spop['행정동코드'].astype(str).str.startswith('11650')]
spop_sc = filtered_df[['기준일ID', '시간대구분', '행정동코드', '총생활인구수']]
spop_sc['time_category'] = spop_sc['시간대구분'].apply(categorize_time)
spop_sc.rename(columns={'행정동코드':'행안부코드'}, inplace=True)
living_data_filtered_1 = spop_sc[spop_sc['time_category'] == '점심']
living_data_filtered_2 = spop_sc[spop_sc['time_category'] == '오후']
living_data_filtered_3 = spop_sc[spop_sc['time_category'] == '저녁']

hjd_avg_spop_1 = living_data_filtered_1.groupby('행안부코드')['총생활인구수'].mean().reset_index()
hjd_avg_spop_2 = living_data_filtered_2.groupby('행안부코드')['총생활인구수'].mean().reset_index()
hjd_avg_spop_3 = living_data_filtered_3.groupby('행안부코드')['총생활인구수'].mean().reset_index()


df2 = boundary_hjd_sc_area_code[['행정동명','통계청코드', '행안부코드','area_m2', 'area_km2']]
df2_1 = pd.merge(df2,hjd_avg_spop_1,on='행안부코드',how='left')
df2_2 = pd.merge(df2,hjd_avg_spop_2,on='행안부코드',how='left')
df2_3 = pd.merge(df2,hjd_avg_spop_3,on='행안부코드',how='left')
# 면적 대비 생활인구 계산
df2_1['밀집도'] = (df2_1['총생활인구수'] / df2_1['area_km2']).round()
df2_2['밀집도'] = (df2_2['총생활인구수'] / df2_2['area_km2']).round()
df2_3['밀집도'] = (df2_3['총생활인구수'] / df2_3['area_km2']).round()
df2_1.to_excel(path_result + '//생활인구//밀집도_점심_202404.xlsx', index=False)
df2_2.to_excel(path_result + '//생활인구//밀집도_오후_202404.xlsx', index=False)
df2_3.to_excel(path_result + '//생활인구//밀집도_저녁_202404.xlsx', index=False)

