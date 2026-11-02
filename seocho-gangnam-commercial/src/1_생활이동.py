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
id_key = id_key[['gid','생활이동인구_cell_id']].drop_duplicates()

# 행정동 코드
hjd_cd = pd.read_csv(path_data_out + '//전국_행정동_코드정보//ADMI_202408.csv')
hjd_cd_o = hjd_cd[['SGG_NM', 'ADMI_NM', 'FULL_NM', 'ADMI_CD']]
hjd_cd_o.columns = ['o_sgg','o_admi','o_full','o_admi_cd']
hjd_cd_d = hjd_cd[['SGG_NM', 'ADMI_NM', 'FULL_NM', 'ADMI_CD']]
hjd_cd_d.columns = ['d_sgg','d_admi','d_full','d_admi_cd']
# 1. 좌표생성
'''
# 생활이동 데이터
# move_point = pd.read_pickle(path_data_out + '//빅데이터캠퍼스//생활이동_좌표ID//u_result.pkl') ### 생활이동 위치 유니크항 포인트 좌표 id
# move_point['geometry'] = move_point.apply(lambda row: Point(row['x'], row['y']), axis=1)
# move_point_gdf = gpd.GeoDataFrame(move_point, geometry='geometry',crs='EPSG:5179')
# move_point_gdf = move_point_gdf.drop_duplicates(subset=['id'])
# move_point_gdf.to_file(path_data_analyze + '//생활이동//move_point_id_2024.gpkg',driver='GPKG')
move_point_gdf = gpd.read_file('D://24project//A39_서초구 인구이동 및 도시계획 분석//2.analyze//move_point_id_2024.gpkg',driver='GPKG')
move_point_o = move_point_gdf.rename(columns = {'id':'o_cell_id','x':'o_x','y':'o_y','hjd_cd':'o_hjd_cd','geometry':'o_geometry'})
move_point_d = move_point_gdf.rename(columns = {'id':'d_cell_id','x':'d_x','y':'d_y','hjd_cd':'d_hjd_cd','geometry':'d_geometry'})
move_point_o.reset_index(inplace=True,drop=True)
move_point_d.reset_index(inplace=True,drop=True)
move_point_o = move_point_o[['o_cell_id','o_geometry']]
move_point_d = move_point_d[['d_cell_id','d_geometry']]
move_point_o = move_point_o.drop_duplicates(subset=['o_cell_id'])
move_point_d = move_point_d.drop_duplicates(subset=['d_cell_id'])


#생활이동 데이터 좌표 생성
move2023_path = 'D://24project//A39_서초구 인구이동 및 도시계획 분석//생활이동//2023//' # CSV 파일들이 있는 폴더 경로
move2024_path = 'D://24project//A39_서초구 인구이동 및 도시계획 분석//생활이동//2024//' # CSV 파일들이 있는 폴더 경로
output_path = ('D://24project//A39_서초구 인구이동 및 도시계획 분석//2.analyze//생활이동//1.좌표생성//')  # 저장할 폴더 경로
csv_files = glob.glob(os.path.join(move2023_path, '생활이동_서초구_*.csv'))

for i, file_path in enumerate(tqdm(csv_files, desc="Processing CSV Files"), start=1):
    # CSV 파일 불러오기
    mv_df = pd.read_csv(file_path, encoding='utf-8')

    # 데이터 병합
    mv_df_g = pd.merge(mv_df, move_point_o[['o_cell_id', 'o_geometry']], on='o_cell_id', how='left')
    mv_df_g = pd.merge(mv_df_g, move_point_d[['d_cell_id', 'd_geometry']], on='d_cell_id', how='left')

    # o_geometry와 d_geometry를 문자열로 변환
    mv_df_g['o_geometry'] = mv_df_g['o_geometry'].apply(lambda point: f"POINT ({point.x} {point.y})" if pd.notna(point) else 'NaN')
    mv_df_g['d_geometry'] = mv_df_g['d_geometry'].apply(lambda point: f"POINT ({point.x} {point.y})" if pd.notna(point) else 'NaN')

    # 파일명 생성 및 저장
    output_filename = f"mv_2023_{i}.pkl"
    output_filepath = os.path.join(output_path, output_filename)
    mv_df_g.to_pickle(output_filepath)

    print(f"{output_filename} 저장 완료")

'''

# 2. 20분단위 → 1시간단위
'''
# 서초구및 강남구 출발 기준 1시간단위 데이터 생성 : 출퇴근시간 20분단위 처리
def process_commute_data_str(data):
    data = data.drop_duplicates() # 중복 제거
    start_data = data[
        data['o_admi_cd'].astype(str).str.startswith('11650') |data['o_admi_cd'].astype(str).str.startswith('11680')]# 서초구 출발 데이터 필터링
    start_data['s_time'] = start_data['st_time_cd'].apply(lambda x: int(str(x)[:2]) if x >= 1000 else (int(str(x)[0]) if x >= 100 else x))
    start_data = start_data[[
        'date', 'o_cell_id', 'o_cell_tp', 'o_admi_cd', 'd_admi_cd',
        's_time', 'st_time_cd', 'in_forn_div_nm', 'move_purpose',
        'move_dist', 'move_time', 'total_cnt', 'male_00_cnt',
        'male_20_cnt', 'male_40_cnt', 'male_60_cnt', 'feml_00_cnt',
        'feml_20_cnt', 'feml_40_cnt', 'feml_60_cnt', 'o_geometry']]

    # 출퇴근 시간대 필터링
    commute_times = start_data[
        (start_data['s_time'].isin([7, 8, 9])) |(start_data['s_time'].isin([17, 18, 19]))]
    commute_times['weighted_move_dist'] = commute_times['move_dist'] * commute_times['total_cnt']
    commute_times['weighted_move_time'] = commute_times['move_time'] * commute_times['total_cnt']
    # 출퇴근 시간대 데이터 그룹화 및 처리
    grouped_commute = commute_times.groupby(
        ['date', 'o_cell_id', 'o_cell_tp', 'o_admi_cd', 'd_admi_cd', 's_time', 'in_forn_div_nm', 'move_purpose']
    ).agg({
        'total_cnt': 'sum',
        'weighted_move_dist': 'sum',
        'weighted_move_time': 'sum',
        'male_00_cnt': 'sum',
        'male_20_cnt': 'sum',
        'male_40_cnt': 'sum',
        'male_60_cnt': 'sum',
        'feml_00_cnt': 'sum',
        'feml_20_cnt': 'sum',
        'feml_40_cnt': 'sum',
        'feml_60_cnt': 'sum'
    }).reset_index()

    grouped_commute['move_dist'] = grouped_commute['weighted_move_dist'] / grouped_commute['total_cnt']
    grouped_commute['move_time'] = grouped_commute['weighted_move_time'] / grouped_commute['total_cnt']
    grouped_commute = grouped_commute.drop(columns=['weighted_move_dist', 'weighted_move_time'])

    # 기존 데이터에서 출퇴근 시간대 데이터 제거
    non_commute_times = start_data[~((start_data['s_time'].isin([7, 8, 9])) | (start_data['s_time'].isin([17, 18, 19])))]
    non_commute_times = non_commute_times[[
        'date', 'o_cell_id', 'o_cell_tp', 'o_admi_cd', 'd_admi_cd', 's_time',
        'in_forn_div_nm', 'move_purpose', 'total_cnt', 'male_00_cnt',
        'male_20_cnt', 'male_40_cnt', 'male_60_cnt', 'feml_00_cnt',
        'feml_20_cnt', 'feml_40_cnt', 'feml_60_cnt', 'move_dist', 'move_time']]

    # 출퇴근 시간대 데이터와 나머지 데이터 합치기
    pre_start_data = pd.concat([non_commute_times, grouped_commute], ignore_index=True).reset_index(drop=True)

    # 데이터 정렬
    pre_start_data['date'] = pd.to_datetime(pre_start_data['date'])
    pre_start_data['연도'] = pre_start_data['date'].dt.year
    pre_start_data['월'] = pre_start_data['date'].dt.month
    pre_start_data['요일'] = pre_start_data['date'].dt.day_name()

    start_final = pre_start_data.sort_values(by=['date', '연도', '월', '요일', 'o_cell_id', 'o_cell_tp', 'o_admi_cd', 'd_admi_cd', 's_time', 'in_forn_div_nm','move_purpose']).reset_index(drop=True)
'''
'''
# 서초구및 강남구 도착 기준 1시간단위 데이터 생성 : 출퇴근시간 20분단위 처리
def process_commute_data_arr(data):
    data = data.drop_duplicates() # 중복 제거
    start_data = data[
        data['d_admi_cd'].astype(str).str.startswith('11650') |data['d_admi_cd'].astype(str).str.startswith('11680')]# 서초구 및 강남구 도착 데이터 필터링
    start_data['d_time'] = start_data['fns_time_cd'].apply(lambda x: int(str(x)[:2]) if x >= 1000 else (int(str(x)[0]) if x >= 100 else x))
    start_data = start_data[[
        'date', 'd_cell_id', 'd_cell_tp', 'o_admi_cd', 'd_admi_cd',
        'd_time', 'fns_time_cd', 'in_forn_div_nm', 'move_purpose',
        'move_dist', 'move_time', 'total_cnt', 'male_00_cnt',
        'male_20_cnt', 'male_40_cnt', 'male_60_cnt', 'feml_00_cnt',
        'feml_20_cnt', 'feml_40_cnt', 'feml_60_cnt', 'o_geometry']]

    # 출퇴근 시간대 필터링
    commute_times = start_data[
        (start_data['d_time'].isin([7, 8, 9])) |(start_data['d_time'].isin([17, 18, 19]))]
    commute_times['weighted_move_dist'] = commute_times['move_dist'] * commute_times['total_cnt']
    commute_times['weighted_move_time'] = commute_times['move_time'] * commute_times['total_cnt']
    # 출퇴근 시간대 데이터 그룹화 및 처리
    grouped_commute = commute_times.groupby(
        ['date', 'd_cell_id', 'd_cell_tp', 'o_admi_cd', 'd_admi_cd', 'd_time', 'in_forn_div_nm', 'move_purpose']
    ).agg({
        'total_cnt': 'sum',
        'weighted_move_dist': 'sum',
        'weighted_move_time': 'sum',
        'male_00_cnt': 'sum',
        'male_20_cnt': 'sum',
        'male_40_cnt': 'sum',
        'male_60_cnt': 'sum',
        'feml_00_cnt': 'sum',
        'feml_20_cnt': 'sum',
        'feml_40_cnt': 'sum',
        'feml_60_cnt': 'sum'
    }).reset_index()

    grouped_commute['move_dist'] = grouped_commute['weighted_move_dist'] / grouped_commute['total_cnt']
    grouped_commute['move_time'] = grouped_commute['weighted_move_time'] / grouped_commute['total_cnt']
    grouped_commute = grouped_commute.drop(columns=['weighted_move_dist', 'weighted_move_time'])

    # 기존 데이터에서 출퇴근 시간대 데이터 제거
    non_commute_times = start_data[~((start_data['d_time'].isin([7, 8, 9])) | (start_data['d_time'].isin([17, 18, 19])))]
    non_commute_times = non_commute_times[[
        'date', 'd_cell_id', 'd_cell_tp', 'o_admi_cd', 'd_admi_cd', 'd_time',
        'in_forn_div_nm', 'move_purpose', 'total_cnt', 'male_00_cnt',
        'male_20_cnt', 'male_40_cnt', 'male_60_cnt', 'feml_00_cnt',
        'feml_20_cnt', 'feml_40_cnt', 'feml_60_cnt', 'move_dist', 'move_time']]

    # 출퇴근 시간대 데이터와 나머지 데이터 합치기
    pre_start_data = pd.concat([non_commute_times, grouped_commute], ignore_index=True).reset_index(drop=True)

    # 데이터 정렬
    pre_start_data['date'] = pd.to_datetime(pre_start_data['date'])
    pre_start_data['연도'] = pre_start_data['date'].dt.year
    pre_start_data['월'] = pre_start_data['date'].dt.month
    pre_start_data['요일'] = pre_start_data['date'].dt.day_name()

    arrive_final = pre_start_data.sort_values(by=['date', '연도', '월', '요일', 'd_cell_id', 'd_cell_tp', 'o_admi_cd', 'd_admi_cd', 'd_time', 'in_forn_div_nm','move_purpose']).reset_index(drop=True)
    return arrive_final
'''
'''
data_path =  ('D://24project//A39_서초구 인구이동 및 도시계획 분석//2.analyze//생활이동//좌표생성//')
output_path_o = ('D://24project//A39_서초구 인구이동 및 도시계획 분석//2.analyze//생활이동//2.출발기준_1시간//')
output_path_d = ('D://24project//A39_서초구 인구이동 및 도시계획 분석//2.analyze//생활이동//2.도착기준_1시간//')
# 폴더 내 모든 파일 처리
file_list = [file_name for file_name in os.listdir(data_path) if file_name.endswith('.pkl')]

for file_name in tqdm(file_list, desc="Processing files"):
    file_path = os.path.join(data_path, file_name)

    data = pd.read_pickle(file_path)
    start_data = process_commute_data_str(data)
    arrival_data = process_commute_data_arr(data)

    base_name, ext = os.path.splitext(file_name)
    start_output_file = f"{base_name}_o{ext}"
    arrival_output_file = f"{base_name}_d{ext}"

    # 결과 저장
    start_data.to_pickle(os.path.join(output_path_o, start_output_file))
    arrival_data.to_pickle(os.path.join(output_path_d, arrival_output_file))
'''

# 3. 행정동정보
'''
output = ('D://24project//A39_서초구 인구이동 및 도시계획 분석//2.analyze//생활이동//3.행정동정보//')
#출발기준 1시간 단위 데이터
data_path_o = ('D://24project//A39_서초구 인구이동 및 도시계획 분석//2.analyze//생활이동//2.출발기준_1시간//')
file_list = [file_name for file_name in os.listdir(data_path_o) if file_name.endswith('.pkl')]
for file_name in tqdm(file_list, desc="Processing files"):
    file_path = os.path.join(data_path_o, file_name)

    data = pd.read_pickle(file_path)
    data = data[['연도', '월', '요일', 'date', 'move_dist', 'move_time',
                 'o_cell_id', 'o_cell_tp', 'o_admi_cd', 'd_admi_cd', 's_time',
                 'in_forn_div_nm', 'move_purpose', 'total_cnt', 'male_00_cnt',
                 'male_20_cnt', 'male_40_cnt', 'male_60_cnt', 'feml_00_cnt',
                 'feml_20_cnt', 'feml_40_cnt', 'feml_60_cnt']]


    pre_data = pd.merge(data, hjd_cd_o, on='o_admi_cd', how='left')    # 행정동 정보 병합
    pre_data = pd.merge(pre_data, hjd_cd_d, on='d_admi_cd', how='left')
    output_file_path = os.path.join(output, file_name)    # 저장 파일 경로
    # 결과 저장
    pre_data.to_pickle(output_file_path)


#도착기준 1시간 단위 데이터
data_path_d = ('D://24project//A39_서초구 인구이동 및 도시계획 분석//2.analyze//생활이동//2.도착기준_1시간//')
file_list = [file_name for file_name in os.listdir(data_path_d) if file_name.endswith('.pkl')]

for file_name in tqdm(file_list, desc="Processing files"):
    file_path = os.path.join(data_path_d, file_name)

    data = pd.read_pickle(file_path)
    data = data[['연도', '월', '요일', 'date', 'move_dist', 'move_time',
                 'd_cell_id', 'd_cell_tp', 'o_admi_cd', 'd_admi_cd', 'd_time',
                 'in_forn_div_nm', 'move_purpose', 'total_cnt', 'male_00_cnt',
                 'male_20_cnt', 'male_40_cnt', 'male_60_cnt', 'feml_00_cnt',
                 'feml_20_cnt', 'feml_40_cnt', 'feml_60_cnt']]


    pre_data = pd.merge(data, hjd_cd_o, on='o_admi_cd', how='left')    # 행정동 정보 병합
    pre_data = pd.merge(pre_data, hjd_cd_d, on='d_admi_cd', how='left')
    output_file_path = os.path.join(output, file_name)    # 저장 파일 경로
    # 결과 저장
    pre_data.to_pickle(output_file_path)
'''

#유입기준
data_241 = pd.read_pickle('D://24project//A39_서초구 인구이동 및 도시계획 분석//2.analyze//생활이동//3.행정동정보//도착기준//mv_2024_1_d.pkl')
data_242 = pd.read_pickle('D://24project//A39_서초구 인구이동 및 도시계획 분석//2.analyze//생활이동//3.행정동정보//도착기준//mv_2024_2_d.pkl')
data_243 = pd.read_pickle('D://24project//A39_서초구 인구이동 및 도시계획 분석//2.analyze//생활이동//3.행정동정보//도착기준//mv_2024_3_d.pkl')
data_244 = pd.read_pickle('D://24project//A39_서초구 인구이동 및 도시계획 분석//2.analyze//생활이동//3.행정동정보//도착기준//mv_2024_4_d.pkl')
data_245 = pd.read_pickle('D://24project//A39_서초구 인구이동 및 도시계획 분석//2.analyze//생활이동//3.행정동정보//도착기준//mv_2024_5_d.pkl')

data_241['평일구분'] = data_241['요일'].apply(lambda x: 0 if x in ['Saturday', 'Sunday'] else 1)
data_242['평일구분'] = data_242['요일'].apply(lambda x: 0 if x in ['Saturday', 'Sunday'] else 1)
data_243['평일구분'] = data_243['요일'].apply(lambda x: 0 if x in ['Saturday', 'Sunday'] else 1)
data_244['평일구분'] = data_244['요일'].apply(lambda x: 0 if x in ['Saturday', 'Sunday'] else 1)
data_245['평일구분'] = data_245['요일'].apply(lambda x: 0 if x in ['Saturday', 'Sunday'] else 1)

data_241 = data_241[['연도', '월', 'date', '요일','평일구분', 'd_time', 'd_cell_id','d_cell_tp',
             'o_admi_cd', 'd_admi_cd', 'o_sgg', 'o_admi', 'o_full', 'd_sgg','d_admi', 'd_full',
             'move_purpose', 'move_dist', 'move_time', 'total_cnt',
             'male_00_cnt', 'male_20_cnt','male_40_cnt', 'male_60_cnt',
             'feml_00_cnt', 'feml_20_cnt','feml_40_cnt', 'feml_60_cnt']]
data_242 = data_242[['연도', '월', 'date', '요일','평일구분', 'd_time', 'd_cell_id','d_cell_tp',
             'o_admi_cd', 'd_admi_cd', 'o_sgg', 'o_admi', 'o_full', 'd_sgg','d_admi', 'd_full',
             'move_purpose', 'move_dist', 'move_time', 'total_cnt',
             'male_00_cnt', 'male_20_cnt','male_40_cnt', 'male_60_cnt',
             'feml_00_cnt', 'feml_20_cnt','feml_40_cnt', 'feml_60_cnt']]
data_243 = data_243[['연도', '월', 'date', '요일','평일구분', 'd_time', 'd_cell_id','d_cell_tp',
             'o_admi_cd', 'd_admi_cd', 'o_sgg', 'o_admi', 'o_full', 'd_sgg','d_admi', 'd_full',
             'move_purpose', 'move_dist', 'move_time', 'total_cnt',
             'male_00_cnt', 'male_20_cnt','male_40_cnt', 'male_60_cnt',
             'feml_00_cnt', 'feml_20_cnt','feml_40_cnt', 'feml_60_cnt']]
data_244 = data_244[['연도', '월', 'date', '요일','평일구분', 'd_time', 'd_cell_id','d_cell_tp',
             'o_admi_cd', 'd_admi_cd', 'o_sgg', 'o_admi', 'o_full', 'd_sgg','d_admi', 'd_full',
             'move_purpose', 'move_dist', 'move_time', 'total_cnt',
             'male_00_cnt', 'male_20_cnt','male_40_cnt', 'male_60_cnt',
             'feml_00_cnt', 'feml_20_cnt','feml_40_cnt', 'feml_60_cnt']]
data_245 = data_245[['연도', '월', 'date', '요일','평일구분', 'd_time', 'd_cell_id','d_cell_tp',
             'o_admi_cd', 'd_admi_cd', 'o_sgg', 'o_admi', 'o_full', 'd_sgg','d_admi', 'd_full',
             'move_purpose', 'move_dist', 'move_time', 'total_cnt',
             'male_00_cnt', 'male_20_cnt','male_40_cnt', 'male_60_cnt',
             'feml_00_cnt', 'feml_20_cnt','feml_40_cnt', 'feml_60_cnt']]

data_241_sort = data_241.sort_values(by=['연도', '월', 'date', '요일','평일구분', 'd_time','d_cell_id'], ascending=True)
data_242_sort = data_242.sort_values(by=['연도', '월', 'date', '요일','평일구분', 'd_time','d_cell_id'], ascending=True)
data_243_sort = data_243.sort_values(by=['연도', '월', 'date', '요일','평일구분', 'd_time','d_cell_id'], ascending=True)
data_244_sort = data_244.sort_values(by=['연도', '월', 'date', '요일','평일구분', 'd_time','d_cell_id'], ascending=True)
data_245_sort = data_245.sort_values(by=['연도', '월', 'date', '요일','평일구분', 'd_time','d_cell_id'], ascending=True)

data_241_sort_seocho = data_241_sort[data_241_sort['d_sgg'] == '서초구']
data_242_sort_seocho = data_242_sort[data_242_sort['d_sgg'] == '서초구']
data_243_sort_seocho = data_243_sort[data_243_sort['d_sgg'] == '서초구']
data_244_sort_seocho = data_244_sort[data_244_sort['d_sgg'] == '서초구']
data_245_sort_seocho = data_245_sort[data_245_sort['d_sgg'] == '서초구']

data_241_sort_seocho.to_pickle(path_data_analyze + '//유입인구//data_241_sort_seocho.pkl')
data_242_sort_seocho.to_pickle(path_data_analyze + '//유입인구//data_242_sort_seocho.pkl')
data_243_sort_seocho.to_pickle(path_data_analyze + '//유입인구//data_243_sort_seocho.pkl')
data_244_sort_seocho.to_pickle(path_data_analyze + '//유입인구//data_244_sort_seocho.pkl')
data_245_sort_seocho.to_pickle(path_data_analyze + '//유입인구//data_245_sort_seocho.pkl')


#서초구 격자 유형 (2024기준)
data_245_grid = data_245_sort_seocho[[ 'd_cell_id', 'd_cell_tp','d_admi']]
data_245_grid.drop_duplicates(subset=['d_cell_id', 'd_cell_tp', 'd_admi'], inplace=True)
data_244_grid = data_244_sort_seocho[[ 'd_cell_id', 'd_cell_tp','d_admi']]
data_244_grid.drop_duplicates(subset=['d_cell_id', 'd_cell_tp', 'd_admi'], inplace=True)
data_243_grid = data_243_sort_seocho[[ 'd_cell_id', 'd_cell_tp','d_admi']]
data_243_grid.drop_duplicates(subset=['d_cell_id', 'd_cell_tp', 'd_admi'], inplace=True)
data_242_grid = data_242_sort_seocho[[ 'd_cell_id', 'd_cell_tp','d_admi']]
data_242_grid.drop_duplicates(subset=['d_cell_id', 'd_cell_tp', 'd_admi'], inplace=True)
data_241_grid = data_241_sort_seocho[[ 'd_cell_id', 'd_cell_tp','d_admi']]
data_241_grid.drop_duplicates(subset=['d_cell_id', 'd_cell_tp', 'd_admi'], inplace=True)
grid_250_tp = pd.concat([data_241_grid, data_242_grid, data_243_grid,data_244_grid,data_245_grid], ignore_index=True)
grid_250_tp.drop_duplicates(subset=['d_cell_id', 'd_cell_tp', 'd_admi'], inplace=True)
grid_250_key = pd.merge(grid_250_tp,id_key,left_on='d_cell_id',right_on='생활이동인구_cell_id',how='left')
grid_250_5181_tp = pd.merge(grid_250_5181_s,grid_250_key,on='gid',how='left')
grid_250_5181_tp = grid_250_5181_tp[['gid', 'lbl', 'val','생활이동인구_cell_id', 'd_cell_id', 'd_cell_tp', 'd_admi', 'geometry']]
grid_250_5181_tp.to_file(PATH_RESULT3 + '//격자//생활이동//grid_2024.gpkg', driver='GPKG')

# 시간대 그룹화 함수 정의
def categorize_time(hour):
    if hour == 0:
        adjusted_hour = 24
    else:
        adjusted_hour = hour
    if 11 <= adjusted_hour < 14:
        return '점심'
    elif 18 <= adjusted_hour < 21:
        return '저녁'
    elif 21 <= adjusted_hour <= 24:
        return '야간'
    else:
        return None
# 계절별 구분 함수
def categorize_season(month):
    if month in [12, 1, 2]:
        return '겨울'
    elif month in [3, 4, 5]:
        return '봄'
    elif month in [6, 7, 8]:
        return '여름'
    else:
        return '가을'


# 시간대별 유입인구 분석(행정동별 트렌드)
# 시간대 카테고리 생성
data_241_sort_seocho['time_category'] = data_241_sort_seocho['d_time'].apply(categorize_time)
data_242_sort_seocho['time_category'] = data_242_sort_seocho['d_time'].apply(categorize_time)
data_243_sort_seocho['time_category'] = data_243_sort_seocho['d_time'].apply(categorize_time)
data_244_sort_seocho['time_category'] = data_244_sort_seocho['d_time'].apply(categorize_time)
data_245_sort_seocho['time_category'] = data_245_sort_seocho['d_time'].apply(categorize_time)

# 점심과 저녁 시간대 데이터만 선택
df_filtered3 = data_243_sort_seocho[data_243_sort_seocho['time_category'].notnull()]
df_filtered4 = data_244_sort_seocho[data_244_sort_seocho['time_category'].notnull()]
df_filtered5 = data_245_sort_seocho[data_245_sort_seocho['time_category'].notnull()]

# 최근 3개월의 고유한 날짜 수 계산
days_count3 = df_filtered3['date'].nunique()
days_count4 = df_filtered4['date'].nunique()
days_count5 = df_filtered5['date'].nunique()

# 행정동별, 시간대별 유입 인구 합계 계산
time_trend3 = df_filtered3.groupby(['월','d_admi', 'time_category'])['total_cnt'].sum().reset_index()
time_trend4 = df_filtered4.groupby(['월','d_admi', 'time_category'])['total_cnt'].sum().reset_index()
time_trend5 = df_filtered5.groupby(['월','d_admi', 'time_category'])['total_cnt'].sum().reset_index()

# 일평균 유입 인구 계산
time_trend3['daily_avg_cnt'] = time_trend3['total_cnt'] / days_count3
time_trend4['daily_avg_cnt'] = time_trend5['total_cnt'] / days_count4
time_trend5['daily_avg_cnt'] = time_trend5['total_cnt'] / days_count5
time_trend = pd.concat([time_trend3, time_trend4, time_trend5], ignore_index=True)
time_trend.to_excel(path_result + '//생활이동//행정동별_시간대별_유입인구트렌드(최근3개월).xlsx', index=False)

# 요일별 유입 패턴 분석
df_filtered3.columns
# 시간대별 평일 vs 주말 유입 인구 분석
# 평일/주말 + 시간대별 유입 인구 합계
time_trend2_3 = df_filtered3.groupby(['d_admi','요일','평일구분', 'time_category'])['total_cnt'].sum().reset_index()
time_trend2_4 = df_filtered4.groupby(['d_admi','요일','평일구분', 'time_category'])['total_cnt'].sum().reset_index()
time_trend2_5 = df_filtered5.groupby(['d_admi','요일','평일구분', 'time_category'])['total_cnt'].sum().reset_index()

# 일평균 유입 인구 계산
days_count1 = df_filtered3.groupby('평일구분')['date'].nunique().to_dict()
days_count2 = df_filtered4.groupby('평일구분')['date'].nunique().to_dict()
days_count3 = df_filtered5.groupby('평일구분')['date'].nunique().to_dict()
time_trend2_3['daily_avg_cnt'] = time_trend2_3.apply(lambda row: row['total_cnt'] / days_count1[row['평일구분']], axis=1)
time_trend2_4['daily_avg_cnt'] = time_trend2_4.apply(lambda row: row['total_cnt'] / days_count2[row['평일구분']], axis=1)
time_trend2_5['daily_avg_cnt'] = time_trend2_5.apply(lambda row: row['total_cnt'] / days_count3[row['평일구분']], axis=1)

#time_trend2_3['daily_avg_cnt'] = time_trend2_3['total_cnt'] / days_count3
#time_trend2_4['daily_avg_cnt'] = time_trend2_4['total_cnt'] / days_count4
#time_trend2_5['daily_avg_cnt'] = time_trend2_5['total_cnt'] / days_count5
time_trend2 = pd.concat([time_trend2_3, time_trend2_4, time_trend2_5], ignore_index=True)
time_trend2.to_excel(path_result + '//생활이동//행정동별_요일별(평일주말)_유입패턴분석(최근3개월)_2.xlsx', index=False)

# 주요 출발지 분석 및 유입 특성
# 출발 행정동별 유입 인구 합계 및 평균 이동 거리 계산
# 시간대 카테고리 생성
data_241_sort_seocho['time_category'] = data_241_sort_seocho['d_time'].apply(categorize_time)
data_242_sort_seocho['time_category'] = data_242_sort_seocho['d_time'].apply(categorize_time)
data_243_sort_seocho['time_category'] = data_243_sort_seocho['d_time'].apply(categorize_time)
data_244_sort_seocho['time_category'] = data_244_sort_seocho['d_time'].apply(categorize_time)
data_245_sort_seocho['time_category'] = data_245_sort_seocho['d_time'].apply(categorize_time)

# 점심과 저녁 시간대 데이터만 선택
df_filtered1 = data_241_sort_seocho[data_241_sort_seocho['time_category'].notnull()]
df_filtered2 = data_242_sort_seocho[data_242_sort_seocho['time_category'].notnull()]
df_filtered3 = data_243_sort_seocho[data_243_sort_seocho['time_category'].notnull()]
df_filtered4 = data_244_sort_seocho[data_244_sort_seocho['time_category'].notnull()]
df_filtered5 = data_245_sort_seocho[data_245_sort_seocho['time_category'].notnull()]

# 최근 5개월의 고유한 날짜 수 계산
days_count1 = df_filtered1['date'].nunique()
days_count2 = df_filtered2['date'].nunique()
days_count3 = df_filtered3['date'].nunique()
days_count4 = df_filtered4['date'].nunique()
days_count5 = df_filtered5['date'].nunique()
'''
# 일평균 유입 인구 계산
days_count1['daily_avg_cnt'] = days_count1['total_cnt'] / days_count1
days_count2['daily_avg_cnt'] = days_count1['total_cnt'] / days_count2
days_count3['daily_avg_cnt'] = days_count1['total_cnt'] / days_count3
days_count4['daily_avg_cnt'] = days_count1['total_cnt'] / days_count4
days_count5['daily_avg_cnt'] = days_count1['total_cnt'] / days_count5
'''

destination_origin_1 = df_filtered1.groupby(['o_sgg','d_admi'])['total_cnt'].sum().reset_index()
destination_origin_2 = df_filtered2.groupby(['o_sgg','d_admi'])['total_cnt'].sum().reset_index()
destination_origin_3 = df_filtered3.groupby(['o_sgg','d_admi'])['total_cnt'].sum().reset_index()
destination_origin_4 = df_filtered4.groupby(['o_sgg','d_admi'])['total_cnt'].sum().reset_index()
destination_origin_5 = df_filtered5.groupby(['o_sgg','d_admi'])['total_cnt'].sum().reset_index()
destination_origin = pd.concat([destination_origin_1, destination_origin_2, destination_origin_3,destination_origin_4,destination_origin_5], ignore_index=True)
destination_origin = destination_origin.groupby(['o_sgg','d_admi'])['total_cnt'].sum().reset_index()

top_origins_per_destination = destination_origin.sort_values(['d_admi', 'total_cnt'], ascending=[True, False])
top_origins_per_destination.to_excel(path_result + '//생활이동//행정동별_주요출발지(시군구)_유입특성분석(2024기준).xlsx', index=False) #강남구 217577



# 강남구 출발 서초구 도착 데이터에 대한 특정 시간대별 ,평일주말별 유입패턴
#서초구및 강남구 출발 기준
df_filtered_og1 = df_filtered1[(df_filtered1['o_sgg'] == '서초구') | (df_filtered1['o_sgg'] == '강남구')]
df_filtered_og2 = df_filtered2[(df_filtered2['o_sgg'] == '서초구') | (df_filtered2['o_sgg'] == '강남구')]
df_filtered_og3 = df_filtered3[(df_filtered3['o_sgg'] == '서초구') | (df_filtered3['o_sgg'] == '강남구')]
df_filtered_og4 = df_filtered4[(df_filtered4['o_sgg'] == '서초구') | (df_filtered4['o_sgg'] == '강남구')]
df_filtered_og5 = df_filtered5[(df_filtered5['o_sgg'] == '서초구') | (df_filtered5['o_sgg'] == '강남구')]
avg_gn = pd.concat([df_filtered_og1, df_filtered_og2, df_filtered_og3, df_filtered_og4, df_filtered_og5], ignore_index=True)

# 서초구에서 출발하여 서초구로 도착하는 데이터 필터링
seocho_to_seocho = avg_gn[(avg_gn['o_sgg'].str.contains('서초구')) & (avg_gn['d_sgg'].str.contains('서초구'))]
# 서초구에서 출발하여 서초구로 도착하는 행정동별 유입 합계 계산
seocho_to_seocho_result = seocho_to_seocho.groupby(['o_admi', 'd_admi']).agg(total_cnt=('total_cnt', 'sum')).reset_index()
seocho_to_seocho_result.to_excel(path_result + '//생활이동//서초구출발_서초구도착(2024기준).xlsx', index=False)

# 강남구에서 출발하여 서초구로 도착하는 데이터 필터링
gangnam_to_seocho = avg_gn[(avg_gn['o_sgg'].str.contains('강남구')) & (avg_gn['d_sgg'].str.contains('서초구'))]
# 강남구에서 출발하여 서초구로 도착하는 행정동별 유입 합계 계산
gangnam_to_seocho_result = gangnam_to_seocho.groupby(['o_admi', 'd_admi']).agg(total_cnt=('total_cnt', 'sum')).reset_index()
gangnam_to_seocho_result.to_excel(path_result + '//생활이동//강남구출발_서초구도착(2024기준).xlsx', index=False)


# 격자 밀집도와 인프라 수용 능력 분석(격자별 특정시간대 기준 유입인구 분석과 인프라 개선 방향)
data_241_sort_seocho['time_category'] = data_241_sort_seocho['d_time'].apply(categorize_time) #점심/저녁/야간시간에 포함안되면 NONE값
data_242_sort_seocho['time_category'] = data_242_sort_seocho['d_time'].apply(categorize_time)
data_243_sort_seocho['time_category'] = data_243_sort_seocho['d_time'].apply(categorize_time)
data_244_sort_seocho['time_category'] = data_244_sort_seocho['d_time'].apply(categorize_time)
data_245_sort_seocho['time_category'] = data_245_sort_seocho['d_time'].apply(categorize_time)

days_count1 = data_241_sort_seocho['date'].nunique()
days_count2 = data_242_sort_seocho['date'].nunique()
days_count3 = data_243_sort_seocho['date'].nunique()
days_count4 = data_244_sort_seocho['date'].nunique()
days_count5 = data_245_sort_seocho['date'].nunique()

data_241_sort_seocho.columns
# 격자별 시간대별 유입 인구 밀집도 분석
time_density1 = data_241_sort_seocho.groupby(['월','d_cell_id','d_cell_tp', 'time_category'])['total_cnt'].sum().reset_index()
time_density2 = data_242_sort_seocho.groupby(['월','d_cell_id','d_cell_tp', 'time_category'])['total_cnt'].sum().reset_index()
time_density3 = data_243_sort_seocho.groupby(['월','d_cell_id','d_cell_tp', 'time_category'])['total_cnt'].sum().reset_index()
time_density4 = data_244_sort_seocho.groupby(['월','d_cell_id','d_cell_tp', 'time_category'])['total_cnt'].sum().reset_index()
time_density5 = data_245_sort_seocho.groupby(['월','d_cell_id','d_cell_tp', 'time_category'])['total_cnt'].sum().reset_index()

time_density1['daily_avg_cnt'] = time_density1['total_cnt'] / days_count1
time_density2['daily_avg_cnt'] = time_density2['total_cnt'] / days_count2
time_density3['daily_avg_cnt'] = time_density3['total_cnt'] / days_count3
time_density4['daily_avg_cnt'] = time_density4['total_cnt'] / days_count4
time_density5['daily_avg_cnt'] = time_density5['total_cnt'] / days_count5

time_density = pd.concat([time_density1, time_density2, time_density3,time_density4,time_density5], ignore_index=True)
time_density.to_excel(path_result + '//생활이동//격자별_특정시간대별(점심,저녁,야간)_유입인구_(2024기준).xlsx', index=False)
summary = time_density.groupby(['d_cell_id', 'time_category']).agg(total_cnt=('total_cnt', 'sum'),daily_avg_cnt=('daily_avg_cnt', 'mean')).reset_index()
time_density_key = pd.merge(summary,id_key,left_on='d_cell_id',right_on='생활이동인구_cell_id',how='left')
time_density_key2 = pd.merge(grid_250_5181_s,time_density_key,on='gid',how='left')
time_density_key3 = time_density_key2[['gid','time_category', 'total_cnt', 'daily_avg_cnt', 'geometry']]
time_density_key3.to_file(PATH_RESULT3 + '//격자//생활이동//격자별_특정시간대별_유입인구_(2024기준).gpkg', driver='GPKG')

# 격자 밀집도와 인프라 수용 능력 분석(격자별 평일주말 기준 유입인구 분석과 인프라 개선 방향)
data_241_sort_seocho['time_category'] = data_241_sort_seocho['d_time'].apply(categorize_time) #점심/저녁/야간시간에 포함안되면 NONE값
data_242_sort_seocho['time_category'] = data_242_sort_seocho['d_time'].apply(categorize_time)
data_243_sort_seocho['time_category'] = data_243_sort_seocho['d_time'].apply(categorize_time)
data_244_sort_seocho['time_category'] = data_244_sort_seocho['d_time'].apply(categorize_time)
data_245_sort_seocho['time_category'] = data_245_sort_seocho['d_time'].apply(categorize_time)
# 격자별 평일주말별 유입인구 합계
time_density1 = data_241_sort_seocho.groupby(['월','d_cell_id','d_cell_tp', '평일구분'])['total_cnt'].sum().reset_index()
time_density2 = data_242_sort_seocho.groupby(['월','d_cell_id','d_cell_tp', '평일구분'])['total_cnt'].sum().reset_index()
time_density3 = data_243_sort_seocho.groupby(['월','d_cell_id','d_cell_tp', '평일구분'])['total_cnt'].sum().reset_index()
time_density4 = data_244_sort_seocho.groupby(['월','d_cell_id','d_cell_tp', '평일구분'])['total_cnt'].sum().reset_index()
time_density5 = data_245_sort_seocho.groupby(['월','d_cell_id','d_cell_tp', '평일구분'])['total_cnt'].sum().reset_index()
# 일평균 유입 인구 계산
days_count1 = data_241_sort_seocho.groupby('평일구분')['date'].nunique().to_dict()
days_count2 = data_242_sort_seocho.groupby('평일구분')['date'].nunique().to_dict()
days_count3 = data_243_sort_seocho.groupby('평일구분')['date'].nunique().to_dict()
days_count4 = data_244_sort_seocho.groupby('평일구분')['date'].nunique().to_dict()
days_count5 = data_245_sort_seocho.groupby('평일구분')['date'].nunique().to_dict()
time_density1['daily_avg_cnt'] = time_density1.apply(lambda row: row['total_cnt'] / days_count1[row['평일구분']], axis=1)
time_density2['daily_avg_cnt'] = time_density2.apply(lambda row: row['total_cnt'] / days_count2[row['평일구분']], axis=1)
time_density3['daily_avg_cnt'] = time_density3.apply(lambda row: row['total_cnt'] / days_count3[row['평일구분']], axis=1)
time_density4['daily_avg_cnt'] = time_density4.apply(lambda row: row['total_cnt'] / days_count4[row['평일구분']], axis=1)
time_density5['daily_avg_cnt'] = time_density5.apply(lambda row: row['total_cnt'] / days_count5[row['평일구분']], axis=1)

time_density = pd.concat([time_density1, time_density2, time_density3,time_density4,time_density5], ignore_index=True)
time_density.to_excel(path_result + '//생활이동//격자별_평일구분별(평일,주말)_(2024기준).xlsx', index=False)
summary2 = time_density.groupby(['d_cell_id', '평일구분']).agg(total_cnt=('total_cnt', 'sum'),daily_avg_cnt=('daily_avg_cnt', 'mean')).reset_index()

time_density_key = pd.merge(summary2,id_key,left_on='d_cell_id',right_on='생활이동인구_cell_id',how='left')
time_density_key2 = pd.merge(grid_250_5181_s,time_density_key,on='gid',how='left')
time_density_key3 = time_density_key2[['gid','평일구분', 'total_cnt','daily_avg_cnt','geometry']]
time_density_key3.to_file(PATH_RESULT3 + '//격자//생활이동//격자별_평일구분별_(2024기준).gpkg', driver='GPKG')

#유출기준
data_o_241 = pd.read_pickle('D://24project//A39_서초구 인구이동 및 도시계획 분석//2.analyze//생활이동//3.행정동정보//출발기준//mv_2024_1_o.pkl')
data_o_242 = pd.read_pickle('D://24project//A39_서초구 인구이동 및 도시계획 분석//2.analyze//생활이동//3.행정동정보//출발기준//mv_2024_2_o.pkl')
data_o_243 = pd.read_pickle('D://24project//A39_서초구 인구이동 및 도시계획 분석//2.analyze//생활이동//3.행정동정보//출발기준//mv_2024_3_o.pkl')
data_o_244 = pd.read_pickle('D://24project//A39_서초구 인구이동 및 도시계획 분석//2.analyze//생활이동//3.행정동정보//출발기준//mv_2024_4_o.pkl')
data_o_245 = pd.read_pickle('D://24project//A39_서초구 인구이동 및 도시계획 분석//2.analyze//생활이동//3.행정동정보//출발기준//mv_2024_5_o.pkl')

data_o_241['평일구분'] = data_o_241['요일'].apply(lambda x: 0 if x in ['Saturday', 'Sunday'] else 1)
data_o_242['평일구분'] = data_o_242['요일'].apply(lambda x: 0 if x in ['Saturday', 'Sunday'] else 1)
data_o_243['평일구분'] = data_o_243['요일'].apply(lambda x: 0 if x in ['Saturday', 'Sunday'] else 1)
data_o_244['평일구분'] = data_o_244['요일'].apply(lambda x: 0 if x in ['Saturday', 'Sunday'] else 1)
data_o_245['평일구분'] = data_o_245['요일'].apply(lambda x: 0 if x in ['Saturday', 'Sunday'] else 1)

data_241 = data_o_241[['연도', '월', 'date', '요일','평일구분', 's_time', 'o_cell_id','o_cell_tp',
             'o_admi_cd', 'd_admi_cd', 'o_sgg', 'o_admi', 'o_full', 'd_sgg','d_admi', 'd_full',
             'move_purpose', 'move_dist', 'move_time', 'total_cnt',
             'male_00_cnt', 'male_20_cnt','male_40_cnt', 'male_60_cnt',
             'feml_00_cnt', 'feml_20_cnt','feml_40_cnt', 'feml_60_cnt']]
data_242 = data_o_242[['연도', '월', 'date', '요일','평일구분', 's_time', 'o_cell_id','o_cell_tp',
             'o_admi_cd', 'd_admi_cd', 'o_sgg', 'o_admi', 'o_full', 'd_sgg','d_admi', 'd_full',
             'move_purpose', 'move_dist', 'move_time', 'total_cnt',
             'male_00_cnt', 'male_20_cnt','male_40_cnt', 'male_60_cnt',
             'feml_00_cnt', 'feml_20_cnt','feml_40_cnt', 'feml_60_cnt']]
data_243 = data_o_243[['연도', '월', 'date', '요일','평일구분', 's_time', 'o_cell_id','o_cell_tp',
             'o_admi_cd', 'd_admi_cd', 'o_sgg', 'o_admi', 'o_full', 'd_sgg','d_admi', 'd_full',
             'move_purpose', 'move_dist', 'move_time', 'total_cnt',
             'male_00_cnt', 'male_20_cnt','male_40_cnt', 'male_60_cnt',
             'feml_00_cnt', 'feml_20_cnt','feml_40_cnt', 'feml_60_cnt']]
data_244 = data_o_244[['연도', '월', 'date', '요일','평일구분', 's_time', 'o_cell_id','o_cell_tp',
             'o_admi_cd', 'd_admi_cd', 'o_sgg', 'o_admi', 'o_full', 'd_sgg','d_admi', 'd_full',
             'move_purpose', 'move_dist', 'move_time', 'total_cnt',
             'male_00_cnt', 'male_20_cnt','male_40_cnt', 'male_60_cnt',
             'feml_00_cnt', 'feml_20_cnt','feml_40_cnt', 'feml_60_cnt']]
data_245 = data_o_245[['연도', '월', 'date', '요일','평일구분', 's_time', 'o_cell_id','o_cell_tp',
             'o_admi_cd', 'd_admi_cd', 'o_sgg', 'o_admi', 'o_full', 'd_sgg','d_admi', 'd_full',
             'move_purpose', 'move_dist', 'move_time', 'total_cnt',
             'male_00_cnt', 'male_20_cnt','male_40_cnt', 'male_60_cnt',
             'feml_00_cnt', 'feml_20_cnt','feml_40_cnt', 'feml_60_cnt']]

data_241_sort = data_241.sort_values(by=['연도', '월', 'date', '요일','평일구분', 's_time','o_cell_id'], ascending=True)
data_242_sort = data_242.sort_values(by=['연도', '월', 'date', '요일','평일구분', 's_time','o_cell_id'], ascending=True)
data_243_sort = data_243.sort_values(by=['연도', '월', 'date', '요일','평일구분', 's_time','o_cell_id'], ascending=True)
data_244_sort = data_244.sort_values(by=['연도', '월', 'date', '요일','평일구분', 's_time','o_cell_id'], ascending=True)
data_245_sort = data_245.sort_values(by=['연도', '월', 'date', '요일','평일구분', 's_time','o_cell_id'], ascending=True)

data_241_sort_seocho = data_241_sort[data_241_sort['o_sgg'] == '서초구']
data_242_sort_seocho = data_242_sort[data_242_sort['o_sgg'] == '서초구']
data_243_sort_seocho = data_243_sort[data_243_sort['o_sgg'] == '서초구']
data_244_sort_seocho = data_244_sort[data_244_sort['o_sgg'] == '서초구']
data_245_sort_seocho = data_245_sort[data_245_sort['o_sgg'] == '서초구']

data_241_sort_seocho['time_category'] = data_241_sort_seocho['s_time'].apply(categorize_time)
data_242_sort_seocho['time_category'] = data_242_sort_seocho['s_time'].apply(categorize_time)
data_243_sort_seocho['time_category'] = data_243_sort_seocho['s_time'].apply(categorize_time)
data_244_sort_seocho['time_category'] = data_244_sort_seocho['s_time'].apply(categorize_time)
data_245_sort_seocho['time_category'] = data_245_sort_seocho['s_time'].apply(categorize_time)
# 고유 날짜 수 계산
unique_days1 = data_241_sort_seocho['date'].nunique()
unique_days2 = data_242_sort_seocho['date'].nunique()
unique_days3 = data_243_sort_seocho['date'].nunique()
unique_days4 = data_244_sort_seocho['date'].nunique()
unique_days5 = data_245_sort_seocho['date'].nunique()
# 시간대별 유출 인구 합계 및 일평균 계산 (행정동별)
time_trend1 = data_241_sort_seocho.groupby(['o_admi', 'time_category']).agg(total_cnt=('total_cnt', 'sum')).reset_index()
time_trend2 = data_242_sort_seocho.groupby(['o_admi', 'time_category']).agg(total_cnt=('total_cnt', 'sum')).reset_index()
time_trend3 = data_243_sort_seocho.groupby(['o_admi', 'time_category']).agg(total_cnt=('total_cnt', 'sum')).reset_index()
time_trend4 = data_244_sort_seocho.groupby(['o_admi', 'time_category']).agg(total_cnt=('total_cnt', 'sum')).reset_index()
time_trend5 = data_245_sort_seocho.groupby(['o_admi', 'time_category']).agg(total_cnt=('total_cnt', 'sum')).reset_index()

time_trend1['daily_avg_cnt'] = time_trend1['total_cnt'] / unique_days1  # 일평균 계산
time_trend2['daily_avg_cnt'] = time_trend2['total_cnt'] / unique_days2
time_trend3['daily_avg_cnt'] = time_trend3['total_cnt'] / unique_days3
time_trend4['daily_avg_cnt'] = time_trend4['total_cnt'] / unique_days4
time_trend5['daily_avg_cnt'] = time_trend5['total_cnt'] / unique_days5
time_trend = pd.concat([time_trend1, time_trend2, time_trend3,time_trend4,time_trend5], ignore_index=True)
time_trend.to_excel(path_result + '//생활이동//행정동별_시간대별_유출인구트렌드(2024기준).xlsx', index=False)


# 요일별 특성분석
# 주말과 평일 구분 데이터프레임 생성
weekday_weekend_analysis1 = data_241_sort_seocho.groupby(['o_admi','평일구분','time_category']).agg(total_cnt=('total_cnt', 'sum')).reset_index()
weekday_weekend_analysis2 = data_242_sort_seocho.groupby(['o_admi','평일구분','time_category']).agg(total_cnt=('total_cnt', 'sum')).reset_index()
weekday_weekend_analysis3 = data_243_sort_seocho.groupby(['o_admi','평일구분','time_category']).agg(total_cnt=('total_cnt', 'sum')).reset_index()
weekday_weekend_analysis4 = data_244_sort_seocho.groupby(['o_admi','평일구분','time_category']).agg(total_cnt=('total_cnt', 'sum')).reset_index()
weekday_weekend_analysis5 = data_245_sort_seocho.groupby(['o_admi','평일구분','time_category']).agg(total_cnt=('total_cnt', 'sum')).reset_index()

# 평일/주말별 고유 날짜 수 계산 (딕셔너리 형태)
days_count1 = data_241_sort_seocho.groupby('평일구분')['date'].nunique().to_dict()
days_count2 = data_242_sort_seocho.groupby('평일구분')['date'].nunique().to_dict()
days_count3 = data_243_sort_seocho.groupby('평일구분')['date'].nunique().to_dict()
days_count4 = data_244_sort_seocho.groupby('평일구분')['date'].nunique().to_dict()
days_count5 = data_245_sort_seocho.groupby('평일구분')['date'].nunique().to_dict()

# 일평균 유출 계산
weekday_weekend_analysis1['daily_avg_cnt'] = weekday_weekend_analysis1.apply(lambda row: row['total_cnt'] / days_count1[row['평일구분']], axis=1)
weekday_weekend_analysis2['daily_avg_cnt'] = weekday_weekend_analysis2.apply(lambda row: row['total_cnt'] / days_count2[row['평일구분']], axis=1)
weekday_weekend_analysis3['daily_avg_cnt'] = weekday_weekend_analysis3.apply(lambda row: row['total_cnt'] / days_count3[row['평일구분']], axis=1)
weekday_weekend_analysis4['daily_avg_cnt'] = weekday_weekend_analysis4.apply(lambda row: row['total_cnt'] / days_count4[row['평일구분']], axis=1)
weekday_weekend_analysis5['daily_avg_cnt'] = weekday_weekend_analysis5.apply(lambda row: row['total_cnt'] / days_count5[row['평일구분']], axis=1)
weekday_weekend_analysis = pd.concat([weekday_weekend_analysis1, weekday_weekend_analysis2, weekday_weekend_analysis3,weekday_weekend_analysis4,weekday_weekend_analysis5], ignore_index=True)
weekday_weekend_analysis.to_excel(path_result + '//생활이동//행정동별_평일구분별_시간대별_유출인구트렌드(2024기준).xlsx', index=False)


# 행정동별 성연령별 유축특성
# 성별 유출 합계
#data_241_sort_seocho['male_cnt'] = data_241_sort_seocho[['male_00_cnt', 'male_20_cnt', 'male_40_cnt', 'male_60_cnt']].sum(axis=1)
#data_241_sort_seocho['female_cnt'] = data_241_sort_seocho[[ 'feml_00_cnt', 'feml_20_cnt', 'feml_40_cnt', 'feml_60_cnt']].sum(axis=1)
#data_242_sort_seocho['male_cnt'] = data_242_sort_seocho[['male_00_cnt', 'male_20_cnt', 'male_40_cnt', 'male_60_cnt']].sum(axis=1)
#data_242_sort_seocho['female_cnt'] = data_242_sort_seocho[[ 'feml_00_cnt', 'feml_20_cnt', 'feml_40_cnt', 'feml_60_cnt']].sum(axis=1)
data_243_sort_seocho['male_cnt'] = data_243_sort_seocho[['male_00_cnt', 'male_20_cnt', 'male_40_cnt', 'male_60_cnt']].sum(axis=1)
data_243_sort_seocho['female_cnt'] = data_243_sort_seocho[[ 'feml_00_cnt', 'feml_20_cnt', 'feml_40_cnt', 'feml_60_cnt']].sum(axis=1)
data_244_sort_seocho['male_cnt'] = data_244_sort_seocho[['male_00_cnt', 'male_20_cnt', 'male_40_cnt', 'male_60_cnt']].sum(axis=1)
data_244_sort_seocho['female_cnt'] = data_244_sort_seocho[[ 'feml_00_cnt', 'feml_20_cnt', 'feml_40_cnt', 'feml_60_cnt']].sum(axis=1)
data_245_sort_seocho['male_cnt'] = data_245_sort_seocho[['male_00_cnt', 'male_20_cnt', 'male_40_cnt', 'male_60_cnt']].sum(axis=1)
data_245_sort_seocho['female_cnt'] = data_245_sort_seocho[[ 'feml_00_cnt', 'feml_20_cnt', 'feml_40_cnt', 'feml_60_cnt']].sum(axis=1)

# 평일/주말별 고유 날짜 수 계산 (딕셔너리 형태)
days_count1 = data_241_sort_seocho.groupby('평일구분')['date'].nunique().to_dict()
days_count2 = data_242_sort_seocho.groupby('평일구분')['date'].nunique().to_dict()
days_count3 = data_243_sort_seocho.groupby('평일구분')['date'].nunique().to_dict()
days_count4 = data_244_sort_seocho.groupby('평일구분')['date'].nunique().to_dict()
days_count5 = data_245_sort_seocho.groupby('평일구분')['date'].nunique().to_dict()
# 평일/주말별, 시간대별 유출 합계 계산
hjd_sx1 = data_241_sort_seocho.groupby(['o_admi','평일구분']).agg(total_cnt=('total_cnt', 'sum'),male_total=('male_cnt', 'sum'),female_total=('female_cnt', 'sum')).reset_index()
hjd_sx2 = data_242_sort_seocho.groupby(['o_admi','평일구분']).agg(total_cnt=('total_cnt', 'sum'),male_total=('male_cnt', 'sum'),female_total=('female_cnt', 'sum')).reset_index()
hjd_sx3 = data_243_sort_seocho.groupby(['o_admi','평일구분']).agg(total_cnt=('total_cnt', 'sum'),male_total=('male_cnt', 'sum'),female_total=('female_cnt', 'sum')).reset_index()
hjd_sx4 = data_244_sort_seocho.groupby(['o_admi','평일구분']).agg(total_cnt=('total_cnt', 'sum'),male_total=('male_cnt', 'sum'),female_total=('female_cnt', 'sum')).reset_index()
hjd_sx5 = data_245_sort_seocho.groupby(['o_admi','평일구분']).agg(total_cnt=('total_cnt', 'sum'),male_total=('male_cnt', 'sum'),female_total=('female_cnt', 'sum')).reset_index()
# 일평균 계산
hjd_sx1['daily_avg_cnt'] = hjd_sx1.apply(lambda row: row['total_cnt'] / days_count1[row['평일구분']], axis=1)
hjd_sx1['daily_avg_male'] = hjd_sx1.apply(lambda row: row['male_total'] / days_count1[row['평일구분']], axis=1)
hjd_sx1['daily_avg_female'] = hjd_sx1.apply(lambda row: row['female_total'] / days_count1[row['평일구분']], axis=1)
hjd_sx2['daily_avg_cnt'] = hjd_sx2.apply(lambda row: row['total_cnt'] / days_count2[row['평일구분']], axis=1)
hjd_sx2['daily_avg_male'] = hjd_sx2.apply(lambda row: row['male_total'] / days_count2[row['평일구분']], axis=1)
hjd_sx2['daily_avg_female'] = hjd_sx2.apply(lambda row: row['female_total'] / days_count2[row['평일구분']], axis=1)
hjd_sx3['daily_avg_cnt'] = hjd_sx3.apply(lambda row: row['total_cnt'] / days_count3[row['평일구분']], axis=1)
hjd_sx3['daily_avg_male'] = hjd_sx3.apply(lambda row: row['male_total'] / days_count3[row['평일구분']], axis=1)
hjd_sx3['daily_avg_female'] = hjd_sx3.apply(lambda row: row['female_total'] / days_count3[row['평일구분']], axis=1)
hjd_sx4['daily_avg_cnt'] = hjd_sx4.apply(lambda row: row['total_cnt'] / days_count4[row['평일구분']], axis=1)
hjd_sx4['daily_avg_male'] = hjd_sx4.apply(lambda row: row['male_total'] / days_count4[row['평일구분']], axis=1)
hjd_sx4['daily_avg_female'] = hjd_sx4.apply(lambda row: row['female_total'] / days_count4[row['평일구분']], axis=1)
hjd_sx5['daily_avg_cnt'] = hjd_sx5.apply(lambda row: row['total_cnt'] / days_count5[row['평일구분']], axis=1)
hjd_sx5['daily_avg_male'] = hjd_sx5.apply(lambda row: row['male_total'] / days_count5[row['평일구분']], axis=1)
hjd_sx5['daily_avg_female'] = hjd_sx5.apply(lambda row: row['female_total'] / days_count5[row['평일구분']], axis=1)

hjd_sx = pd.concat([hjd_sx1,hjd_sx2,hjd_sx3, hjd_sx4, hjd_sx5], ignore_index=True)
hjd_sx.to_excel(path_result + '//생활이동//행정동별_성별_유출인구트렌드(2024기준).xlsx', index=False)

# 성연령별 컬럼 리스트 정의
gender_age_columns = [
    'male_00_cnt', 'male_20_cnt', 'male_40_cnt', 'male_60_cnt',
    'feml_00_cnt', 'feml_20_cnt', 'feml_40_cnt', 'feml_60_cnt'
]
hjd_sxage1 = data_241_sort_seocho.groupby(['o_admi', '평일구분', 'time_category'])[gender_age_columns].sum().reset_index()
hjd_sxage2 = data_242_sort_seocho.groupby(['o_admi', '평일구분', 'time_category'])[gender_age_columns].sum().reset_index()
hjd_sxage3 = data_243_sort_seocho.groupby(['o_admi', '평일구분', 'time_category'])[gender_age_columns].sum().reset_index()
hjd_sxage4 = data_244_sort_seocho.groupby(['o_admi', '평일구분', 'time_category'])[gender_age_columns].sum().reset_index()
hjd_sxage5 = data_245_sort_seocho.groupby(['o_admi', '평일구분', 'time_category'])[gender_age_columns].sum().reset_index()
hjd_sxage = pd.concat([hjd_sxage1,hjd_sxage2,hjd_sxage3, hjd_sxage4, hjd_sxage5], ignore_index=True)
hjd_sxage.to_excel(path_result + '//생활이동//행정동별_성연령별_합계_유출인구트렌드(2024기준).xlsx', index=False)


# 시군구별 도착지 분석: 어떤 시군구로 많이 도착하는지 계산
# 시군구별 도착지 유출 합계 계산
df_filtered1 = data_241_sort_seocho[data_241_sort_seocho['time_category'].notnull()]
df_filtered2 = data_242_sort_seocho[data_242_sort_seocho['time_category'].notnull()]
df_filtered3 = data_243_sort_seocho[data_243_sort_seocho['time_category'].notnull()]
df_filtered4 = data_244_sort_seocho[data_244_sort_seocho['time_category'].notnull()]
df_filtered5 = data_245_sort_seocho[data_245_sort_seocho['time_category'].notnull()]

destination_analysis1 = df_filtered1.groupby(['o_admi','d_sgg'])['total_cnt'].sum().reset_index()
destination_analysis2 = df_filtered2.groupby(['o_admi','d_sgg'])['total_cnt'].sum().reset_index()
destination_analysis3 = df_filtered3.groupby(['o_admi','d_sgg'])['total_cnt'].sum().reset_index()
destination_analysis4 = df_filtered4.groupby(['o_admi','d_sgg'])['total_cnt'].sum().reset_index()
destination_analysis5 = df_filtered5.groupby(['o_admi','d_sgg'])['total_cnt'].sum().reset_index()

destination_analysis = pd.concat([destination_analysis1,destination_analysis2,destination_analysis3, destination_analysis4, destination_analysis5], ignore_index=True)
destination_analysis.to_excel(path_result + '//생활이동//행정동별_주요도착지(시군구)_유입특성분석(2024기준).xlsx', index=False)



# 시간대별 유출 인구 합계 및 일평균 계산 (목적지별)
destination_trend1 = data_241_sort_seocho.groupby(['d_sgg', 'time_category']).agg(total_cnt=('total_cnt', 'sum')).reset_index()
destination_trend2 = data_242_sort_seocho.groupby(['d_sgg', 'time_category']).agg(total_cnt=('total_cnt', 'sum')).reset_index()
destination_trend3 = data_243_sort_seocho.groupby(['d_sgg', 'time_category']).agg(total_cnt=('total_cnt', 'sum')).reset_index()
destination_trend4 = data_244_sort_seocho.groupby(['d_sgg', 'time_category']).agg(total_cnt=('total_cnt', 'sum')).reset_index()
destination_trend5 = data_245_sort_seocho.groupby(['d_sgg', 'time_category']).agg(total_cnt=('total_cnt', 'sum')).reset_index()

destination_trend1['daily_avg_cnt'] = destination_trend1['total_cnt'] / unique_days1  # 일평균 계산
destination_trend2['daily_avg_cnt'] = destination_trend2['total_cnt'] / unique_days2
destination_trend3['daily_avg_cnt'] = destination_trend3['total_cnt'] / unique_days3
destination_trend4['daily_avg_cnt'] = destination_trend4['total_cnt'] / unique_days4
destination_trend5['daily_avg_cnt'] = destination_trend5['total_cnt'] / unique_days5
destination_trend = pd.concat([destination_trend1, destination_trend2, destination_trend3,destination_trend4,destination_trend5], ignore_index=True)
destination_trend.to_excel(path_result + '//생활이동//시간대별_도착지별_유출인구트렌드(2024기준).xlsx', index=False)


# 도착지가 강남구인 데이터 필터링
gangnam_data1 = data_241_sort_seocho[data_241_sort_seocho['d_sgg'] == '강남구']
gangnam_data2 = data_242_sort_seocho[data_242_sort_seocho['d_sgg'] == '강남구']
gangnam_data3 = data_243_sort_seocho[data_243_sort_seocho['d_sgg'] == '강남구']
gangnam_data4 = data_244_sort_seocho[data_244_sort_seocho['d_sgg'] == '강남구']
gangnam_data5 = data_245_sort_seocho[data_245_sort_seocho['d_sgg'] == '강남구']
gangnam_data = pd.concat([gangnam_data1, gangnam_data2, gangnam_data3, gangnam_data4, gangnam_data5], ignore_index=True)

# 서초구에서 출발하여 강남구로 도착하는 행정동별 유입 합계 계산
seocho_to_gangnam = gangnam_data.groupby(['o_admi', 'd_admi']).agg(total_cnt=('total_cnt', 'sum')).reset_index()
seocho_to_gangnam.to_excel(path_result + '//생활이동//서초구출발_강남구도착(2024기준).xlsx', index=False)



# 격자 밀집도와 인프라 수용 능력 분석(격자별 특정시간대 기준 유입인구 분석과 인프라 개선 방향)
# 격자별 시간대별 유출 인구 밀집도 분석
time_density1 = data_241_sort_seocho.groupby(['월','o_cell_id','o_cell_tp', 'time_category'])['total_cnt'].sum().reset_index()
time_density2 = data_242_sort_seocho.groupby(['월','o_cell_id','o_cell_tp', 'time_category'])['total_cnt'].sum().reset_index()
time_density3 = data_243_sort_seocho.groupby(['월','o_cell_id','o_cell_tp', 'time_category'])['total_cnt'].sum().reset_index()
time_density4 = data_244_sort_seocho.groupby(['월','o_cell_id','o_cell_tp', 'time_category'])['total_cnt'].sum().reset_index()
time_density5 = data_245_sort_seocho.groupby(['월','o_cell_id','o_cell_tp', 'time_category'])['total_cnt'].sum().reset_index()

days_count1 = data_241_sort_seocho['date'].nunique()
days_count2 = data_242_sort_seocho['date'].nunique()
days_count3 = data_243_sort_seocho['date'].nunique()
days_count4 = data_244_sort_seocho['date'].nunique()
days_count5 = data_245_sort_seocho['date'].nunique()

time_density1['daily_avg_cnt'] = time_density1['total_cnt'] / days_count1
time_density2['daily_avg_cnt'] = time_density2['total_cnt'] / days_count2
time_density3['daily_avg_cnt'] = time_density3['total_cnt'] / days_count3
time_density4['daily_avg_cnt'] = time_density4['total_cnt'] / days_count4
time_density5['daily_avg_cnt'] = time_density5['total_cnt'] / days_count5

time_density = pd.concat([time_density1, time_density2, time_density3,time_density4,time_density5], ignore_index=True)
time_density.to_excel(path_result + '//생활이동//격자별_특정시간대별(점심,저녁,야간)_유출인구_(2024기준).xlsx', index=False)
summary = time_density.groupby(['o_cell_id', 'time_category']).agg(total_cnt=('total_cnt', 'sum'),daily_avg_cnt=('daily_avg_cnt', 'mean')).reset_index()
time_density_key = pd.merge(summary,id_key,left_on='o_cell_id',right_on='생활이동인구_cell_id',how='left')
time_density_key2 = pd.merge(grid_250_5181_s,time_density_key,on='gid',how='left')
time_density_key3 = time_density_key2[['gid','time_category', 'total_cnt', 'daily_avg_cnt', 'geometry']]
time_density_key3.to_file(PATH_RESULT3 + '//격자//생활이동//격자별_특정시간대별_유출인구_(2024기준).gpkg', driver='GPKG')

# 서초2동, 서초4동, 서초3동 격자 데이터 필터링
seocho_target_admins = ['서초2동', '서초4동', '서초3동']
filtered_data1 = data_241_sort_seocho[data_241_sort_seocho['o_admi'].isin(seocho_target_admins)]
filtered_data2 = data_242_sort_seocho[data_242_sort_seocho['o_admi'].isin(seocho_target_admins)]
filtered_data3 = data_243_sort_seocho[data_243_sort_seocho['o_admi'].isin(seocho_target_admins)]
filtered_data4 = data_244_sort_seocho[data_244_sort_seocho['o_admi'].isin(seocho_target_admins)]
filtered_data5 = data_245_sort_seocho[data_245_sort_seocho['o_admi'].isin(seocho_target_admins)]
gangnam_data1 = filtered_data1[filtered_data1['d_sgg'] == '강남구']
gangnam_data2 = filtered_data2[filtered_data2['d_sgg'] == '강남구']
gangnam_data3 = filtered_data3[filtered_data3['d_sgg'] == '강남구']
gangnam_data4 = filtered_data4[filtered_data4['d_sgg'] == '강남구']
gangnam_data5 = filtered_data5[filtered_data5['d_sgg'] == '강남구']

# 그룹화하여 강남구 행정동별 유출 데이터 계산
gangnam_analysis1 = gangnam_data1.groupby(['o_admi', 'd_admi', 'time_category']).agg(total_cnt=('total_cnt', 'sum')).reset_index()
gangnam_analysis2 = gangnam_data2.groupby(['o_admi', 'd_admi', 'time_category']).agg(total_cnt=('total_cnt', 'sum')).reset_index()
gangnam_analysis3 = gangnam_data3.groupby(['o_admi', 'd_admi', 'time_category']).agg(total_cnt=('total_cnt', 'sum')).reset_index()
gangnam_analysis4 = gangnam_data4.groupby(['o_admi', 'd_admi', 'time_category']).agg(total_cnt=('total_cnt', 'sum')).reset_index()
gangnam_analysis5 = gangnam_data5.groupby(['o_admi', 'd_admi', 'time_category']).agg(total_cnt=('total_cnt', 'sum')).reset_index()

gangnam_analysis = pd.concat([gangnam_analysis1, gangnam_analysis2, gangnam_analysis3,gangnam_analysis4,gangnam_analysis5], ignore_index=True)
gangnam_analysis = gangnam_analysis.groupby(['o_admi', 'd_admi', 'time_category']).agg(total_cnt=('total_cnt', 'sum')).reset_index()
gangnam_analysis.to_excel(path_result + '//생활이동//강남구유출_TOP3_유출인구합계(2024기준).xlsx', index=False)

# 격자별 그룹화하여 강남구 행정동별 유출 데이터 계산
gangnam_analysis1 = gangnam_data1.groupby(['o_cell_id', 'time_category']).agg(total_cnt=('total_cnt', 'sum')).reset_index()
gangnam_analysis2 = gangnam_data2.groupby(['o_cell_id', 'time_category']).agg(total_cnt=('total_cnt', 'sum')).reset_index()
gangnam_analysis3 = gangnam_data3.groupby(['o_cell_id', 'time_category']).agg(total_cnt=('total_cnt', 'sum')).reset_index()
gangnam_analysis4 = gangnam_data4.groupby(['o_cell_id', 'time_category']).agg(total_cnt=('total_cnt', 'sum')).reset_index()
gangnam_analysis5 = gangnam_data5.groupby(['o_cell_id', 'time_category']).agg(total_cnt=('total_cnt', 'sum')).reset_index()
gangnam_analysis = pd.concat([gangnam_analysis1, gangnam_analysis2, gangnam_analysis3,gangnam_analysis4,gangnam_analysis5], ignore_index=True)
gangnam_analysis = gangnam_analysis.groupby(['o_cell_id', 'time_category']).agg(total_cnt=('total_cnt', 'sum')).reset_index()
time_density_key = pd.merge(gangnam_analysis,id_key,left_on='o_cell_id',right_on='생활이동인구_cell_id',how='left')
time_density_key2 = pd.merge(grid_250_5181_s,time_density_key,on='gid',how='left')

time_density_key3 = time_density_key2[['gid', 'time_category','total_cnt', 'geometry']]
time_density_key3.to_file(PATH_RESULT3 + '//격자//생활이동//강남유출TOP3행정동_격자별_유출인구합계_(2024기준).gpkg', driver='GPKG')






############################################### 생활이동  샘플데이터 처리 #################################################
'''
data = pd.read_pickle('D://24project//서초구_생활이동//df(1,2)//df1.pkl')
data = data.groupby(['etl_ymd', 'o_cell_id', 'o_cell_x', 'o_cell_y', 'o_cell_tp',
                     'd_cell_id', 'd_cell_x', 'd_cell_y', 'd_cell_tp', 'time_o', 'time_d',
                     'new_hjd_o', 'new_hjd_d', 'move_purpose'])[['move_dist', 'move_time',
                     'male_00-19', 'male_20', 'male_30', 'male_40', 'male_50', 'male_60up',
                     'female_00-19', 'female_20', 'female_30', 'female_40', 'female_50',
                     'female_60up', 'total_cnt']].sum().reset_index()

data_head = data.head()
data_head.to_csv('D://24project//서초구_생활이동//df(1,2)//data_head.csv', index=False,encoding='cp949')
data_tail = data.tail()
data_tail.to_csv('D://24project//서초구_생활이동//df(1,2)//data_tail.csv', index=False,encoding='cp949')
folder_path = 'your_folder_path_here'

# 특정 폴더 경로 설정
folder_path = 'D://24project//서초구_생활이동//'
pkl_files = glob.glob(os.path.join(folder_path, '*.pkl'))

data_frames = []
# pkl 파일들을 하나씩 읽어와서 전처리 후 DataFrame에 추가
for pkl_file in pkl_files:
    # .pkl 파일을 열고 데이터 로드
    with open(pkl_file, 'rb') as f:
        data = pickle.load(f)
        data_g = data.groupby(['etl_ymd', 'o_cell_id', 'o_cell_x', 'o_cell_y', 'o_cell_tp',
                               'd_cell_id', 'd_cell_x', 'd_cell_y', 'd_cell_tp', 'time_o', 'time_d',
                               'new_hjd_o', 'new_hjd_d', 'move_purpose'])[['move_dist', 'move_time',
                                                                           'male_00-19', 'male_20', 'male_30', 'male_40','male_50', 'male_60up',
                                                                           'female_00-19', 'female_20', 'female_30','female_40', 'female_50','female_60up',
                                                                           'total_cnt']].sum().reset_index()
    data_frames.append(data_g)
final_df = pd.concat(data_frames, ignore_index=True)
col = [
'etl_ymd', 'o_cell_id', 'o_cell_x', 'o_cell_y', 'o_cell_tp',
       'd_cell_id', 'd_cell_x', 'd_cell_y', 'd_cell_tp', 'time_o', 'time_d',
       'new_hjd_o', 'new_hjd_d', 'move_purpose']
final_df = final_df.sort_values(by=col, ascending=True)
final_df.to_pickle(path_data_analyze + '//생활이동//move_pop.pkl')
final_df = pd.read_pickle(path_data_analyze + '//생활이동//move_pop.pkl')

'''


#추가분석
data_d_245 = pd.read_pickle('D://24project//A39_서초구 인구이동 및 도시계획 분석//2.analyze//생활이동//3.행정동정보//도착기준//mv_2024_5_d.pkl')
data_o_245 = pd.read_pickle('D://24project//A39_서초구 인구이동 및 도시계획 분석//2.analyze//생활이동//3.행정동정보//출발기준//mv_2024_5_o.pkl')
data_d_245['평일구분'] = data_d_245['요일'].apply(lambda x: 0 if x in ['Saturday', 'Sunday'] else 1)
data_o_245['평일구분'] = data_o_245['요일'].apply(lambda x: 0 if x in ['Saturday', 'Sunday'] else 1)

data_d_245 = data_d_245[['연도', '월', 'date', '요일','평일구분', 'd_time',
             'o_admi_cd', 'd_admi_cd', 'o_sgg', 'o_admi', 'd_sgg','d_admi',
             'move_purpose', 'move_dist', 'move_time', 'total_cnt',
             'male_00_cnt', 'male_20_cnt','male_40_cnt', 'male_60_cnt',
             'feml_00_cnt', 'feml_20_cnt','feml_40_cnt', 'feml_60_cnt']]

data_o_245 = data_o_245[['연도', '월', 'date', '요일','평일구분', 's_time',
             'o_admi_cd', 'd_admi_cd', 'o_sgg', 'o_admi', 'd_sgg','d_admi',
             'move_purpose', 'move_dist', 'move_time', 'total_cnt',
             'male_00_cnt', 'male_20_cnt','male_40_cnt', 'male_60_cnt',
             'feml_00_cnt', 'feml_20_cnt','feml_40_cnt', 'feml_60_cnt']]

data_d_245 = data_d_245.sort_values(by=['연도', '월', 'date', '요일','평일구분', 'd_time'], ascending=True)
data_o_245 = data_o_245.sort_values(by=['연도', '월', 'date', '요일','평일구분', 's_time'], ascending=True)

data_d_245_sort_seocho = data_d_245[data_d_245['d_sgg'] == '서초구']
data_o_245_sort_seocho = data_o_245[data_o_245['o_sgg'] == '서초구']

data_d_245_sort_seocho.to_pickle(path_data_analyze + '//추가분석//202405_유입.pkl')
data_o_245_sort_seocho.to_pickle(path_data_analyze + '//추가분석//202405_유출.pkl')

# 추가분석
data_d_245_sort_seocho = pd.read_pickle(path_data_analyze + '//유입인구//data_245_sort_seocho.pkl')
data_d_245_sort_seocho_weekday = data_d_245_sort_seocho[data_d_245_sort_seocho['평일구분'] == 1]

data_d_245_sort_seocho_weekday_day = data_d_245_sort_seocho_weekday.groupby(['d_cell_id','d_admi','date'])['total_cnt'].sum().reset_index()
data_d_245_sort_seocho_weekday_month = data_d_245_sort_seocho_weekday.groupby(['d_cell_id','d_admi'])['total_cnt'].sum().reset_index()

seocho_weekday_month = pd.merge(data_d_245_sort_seocho_weekday_month,id_key,left_on='d_cell_id',right_on='생활이동인구_cell_id',how='left')
seocho_weekday_month2 = pd.merge(grid_250_5181_s,seocho_weekday_month,on='gid',how='left')
seocho_weekday_month3 = seocho_weekday_month2[['gid','d_admi','total_cnt', 'geometry']]
seocho_weekday_month3 = seocho_weekday_month3.dropna(subset=['gid'])
seocho_weekday_month3.to_file(PATH_RESULT3 + '//격자//생활이동//평일생활이동인구(유입)_202405.gpkg', driver='GPKG')


# 추가분석
data_d_245_sort_seocho = pd.read_pickle(path_data_analyze + '//유입인구//data_245_sort_seocho.pkl')
data_d_245_sort_seocho = data_d_245_sort_seocho[data_d_245_sort_seocho['평일구분'] == 1]
data = data_d_245_sort_seocho[['d_cell_id','d_admi','연도', '월', '평일구분','d_time','total_cnt']]
data789 = data[data['d_time'].isin([7, 8, 9])] # 평일 출근,등교
data789_g = data789.groupby(['d_cell_id','d_admi'])['total_cnt'].sum().reset_index()
data789_g = pd.merge(data789_g,id_key,left_on='d_cell_id',right_on='생활이동인구_cell_id',how='left')
data789_g = pd.merge(grid_250_5181_s,data789_g,on='gid',how='left')
data789_g = data789_g[['gid','d_admi','total_cnt', 'geometry']]
data789_g = data789_g.dropna(subset=['gid'])
data789_g.to_file(PATH_RESULT3 + '//격자//생활이동//평일_출근등교시간대_유입_202405.gpkg', driver='GPKG')

data111213 = data[data['d_time'].isin([11, 12, 13])] #평일 점심시간대
data111213_g = data111213.groupby(['d_cell_id','d_admi'])['total_cnt'].sum().reset_index()
data111213_g = pd.merge(data111213_g,id_key,left_on='d_cell_id',right_on='생활이동인구_cell_id',how='left')
data111213_g = pd.merge(grid_250_5181_s,data111213_g,on='gid',how='left')
data111213_g = data111213_g[['gid','d_admi','total_cnt', 'geometry']]
data111213_g = data111213_g.dropna(subset=['gid'])
data111213_g.to_file(PATH_RESULT3 + '//격자//생활이동//평일_점심시간대_유입_202405.gpkg', driver='GPKG')

data141516 = data[data['d_time'].isin([14, 15, 16])] #평일 오후시간대
data141516_g = data141516.groupby(['d_cell_id','d_admi'])['total_cnt'].sum().reset_index()
data141516_g = pd.merge(data141516_g,id_key,left_on='d_cell_id',right_on='생활이동인구_cell_id',how='left')
data141516_g = pd.merge(grid_250_5181_s,data141516_g,on='gid',how='left')
data141516_g = data141516_g[['gid','d_admi','total_cnt', 'geometry']]
data141516_g = data141516_g.dropna(subset=['gid'])
data141516_g.to_file(PATH_RESULT3 + '//격자//생활이동//평일_오후시간대_유입_202405.gpkg', driver='GPKG')

data17181920 = data[data['d_time'].isin([17, 18, 19, 20])] #평일 저녁시간대
data17181920_g = data17181920.groupby(['d_cell_id','d_admi'])['total_cnt'].sum().reset_index()
data17181920_g = pd.merge(data17181920_g,id_key,left_on='d_cell_id',right_on='생활이동인구_cell_id',how='left')
data17181920_g = pd.merge(grid_250_5181_s,data17181920_g,on='gid',how='left')
data17181920_g = data17181920_g[['gid','d_admi','total_cnt', 'geometry']]
data17181920_g = data17181920_g.dropna(subset=['gid'])
data17181920_g.to_file(PATH_RESULT3 + '//격자//생활이동//평일_저녁시간대_유입_202405.gpkg', driver='GPKG')


# 추가분석
data_d_245_sort_seocho = pd.read_pickle(path_data_analyze + '//유입인구//data_245_sort_seocho.pkl')
data_d_245_sort_seocho = data_d_245_sort_seocho[data_d_245_sort_seocho['평일구분'] == 1]
data_d_245_sort_seocho['남성'] = data_d_245_sort_seocho[[ 'male_00_cnt', 'male_20_cnt', 'male_40_cnt', 'male_60_cnt']].sum(axis=1)
data_d_245_sort_seocho['여성'] = data_d_245_sort_seocho[[ 'feml_00_cnt', 'feml_20_cnt', 'feml_40_cnt', 'feml_60_cnt']].sum(axis=1)
data_d_245_sort_seocho['20대미만'] = data_d_245_sort_seocho[['male_00_cnt','feml_00_cnt']].sum(axis=1)
data_d_245_sort_seocho['20-30대'] = data_d_245_sort_seocho[['male_20_cnt','feml_20_cnt']].sum(axis=1)
data_d_245_sort_seocho['40-50대'] = data_d_245_sort_seocho[['male_40_cnt','feml_40_cnt']].sum(axis=1)
data_sx_age = data_d_245_sort_seocho.groupby(['d_cell_id','d_admi'])[['남성', '여성','20대미만', '20-30대', '40-50대']].sum().reset_index()
data_sx_age = pd.merge(data_sx_age,id_key,left_on='d_cell_id',right_on='생활이동인구_cell_id',how='left')
data_sx_age = pd.merge(grid_250_5181_s,data_sx_age,on='gid',how='left')
data_sx_age = data_sx_age[['gid','d_admi','남성', '여성','20대미만', '20-30대', '40-50대', 'geometry']]
data_sx_age = data_sx_age.dropna(subset=['gid'])
data_sx_age.to_file(PATH_RESULT3 + '//격자//생활이동//평일_성별_연령대별_202405.gpkg', driver='GPKG')


