###########################################################
# 과 제 명: A39_서초구_인구이동 및 도시계획
# 파 일 명: 카드 분석 2
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

#격자
grid_100_5181_s = gpd.read_file(PATH_RESULT3 + '//격자//100M격자거주인구//grid100_seocho_5181.gpkg', driver='GPKG')
grid_100_5181_g = gpd.read_file(PATH_RESULT3 + '//격자//100M격자거주인구//grid100_gangnam_5181.gpkg', driver='GPKG')
#행정경계
boundary_hjd_sc = gpd.read_file(PATH_RESULT3 + '//경계면//행정동//boundary_hjd_seocho_5181.gpkg', driver='GPKG')
boundary_hjd_gn = gpd.read_file(PATH_RESULT3 + '//경계면//행정동//boundary_hjd_gangnam_5181.gpkg', driver='GPKG')

#집계구
boundary_oa_sc = gpd.read_file(PATH_RESULT3 + '//경계면//집계구//boundary_oa_seocho_5181.gpkg', driver='GPKG')
boundary_oa_gn = gpd.read_file(PATH_RESULT3 + '//경계면//집계구//boundary_oa_gangnam_5181.gpkg', driver='GPKG')

#카드 데이터 50m
grid50_card_day_time = pd.read_pickle('D://24project//A39_서초구 인구이동 및 도시계획 분석//2.analyze//카드//grid50_card_day_time.pkl') # 50m 격자 내 가맹점 기준 일별 시간대별 카드데이터

#분석 대상 50m격자
card_grid = gpd.read_file(PATH_RESULT3 + '//격자//카드격자//50m격자정보//강남역_50.gpkg',driver='GPKG')
############################################ 카드 #####################################################################

#격자데이터 읽어오기(분석결과)
p13 = pd.read_excel(path_result + '//카드상권분석2//a29_격자_p13_일평균금액횟수.xlsx')
p1415 = pd.read_excel(path_result + '//카드상권분석2//a29_격자_p14_p15_요일별일평균금액횟수.xlsx')
p1617 = pd.read_excel(path_result + '//카드상권분석2//a29_격자_p16_17_요일별시간대별.xlsx')

#격자 geo매핑
def save_geo_dataframe(df, file_path):
    try:
        merged_df = pd.merge(df, card_grid, on='SPO_NO_CD', how='left')
        geo_df = gpd.GeoDataFrame(merged_df, geometry='geometry')
        if 'Unnamed: 0' in geo_df.columns:
            geo_df = geo_df.drop(columns=['Unnamed: 0'])
        geo_df.to_file(PATH_RESULT3 + f'//격자//카드격자2//{file_path}.gpkg', driver='GPKG')
        print(f"파일이 성공적으로 저장되었습니다: {file_path}")
    except Exception as e:
        print(f"오류가 발생했습니다: {e}")

save_geo_dataframe(p13,'a29_격자_p13_일평균금액횟수')
save_geo_dataframe(p1415,'a29_격자_p14_p15_요일별일평균금액횟수')
save_geo_dataframe(p1617,'a29_격자_p16_17_요일별시간대별')


p20_md = pd.read_excel(path_result + '//카드상권분석2//a29_격자_p20_의료.xlsx', header=[1, 2])
p20_md_day = pd.read_excel(path_result + '//카드상권분석2//a29_격자_p20_의료요일.xlsx', header=[1, 2])
p22_time = pd.read_excel(path_result + '//카드상권분석2//a29_격자_p22_소매유통시간.xlsx', header=[1, 2])
p22_day = pd.read_excel(path_result + '//카드상권분석2//a29_격자_p22_소매유통요일.xlsx', header=[1, 2])
p24 = pd.read_excel(path_result + '//카드상권분석2//a29_격자_p24_교육11시.xlsx', header=[1, 2])
p24_sat = pd.read_excel(path_result + '//카드상권분석2//a29_격자_p24_교육토요일.xlsx', header=[1, 2])
p26 = pd.read_excel(path_result + '//카드상권분석2//a29_격자_p26_생활서비스11시.xlsx', header=[1, 2])
p26_sat = pd.read_excel(path_result + '//카드상권분석2//a29_격자_p26_생활서비스토요일.xlsx', header=[1, 2])
p28 = pd.read_excel(path_result + '//카드상권분석2//a29_격자_p28_음식시간.xlsx', header=[1, 2])
p28_sat = pd.read_excel(path_result + '//카드상권분석2//a29_격자_p28_음식토요일.xlsx', header=[1, 2])

def process_and_save_geo_data(df,  file_name):
    try:
        df.columns = ['_'.join(map(str, col)).strip() for col in df.columns]
        df = df.drop(index=0)
        df = df.iloc[:, 1:]
        df.rename(columns={df.columns[0]: 'SPO_NO_CD'}, inplace=True)

        # 서초구와 강남구 데이터 분리
        seocho_columns = ['SPO_NO_CD'] + [col for col in df.columns if '서초구' in str(col)]
        gangnam_columns = ['SPO_NO_CD'] + [col for col in df.columns if '강남구' in str(col)]
        seocho_data = df[seocho_columns]
        gangnam_data = df[gangnam_columns]

        merged_seocho_data = pd.merge(seocho_data, card_grid, on='SPO_NO_CD', how='left')
        merged_gangnam_data = pd.merge(gangnam_data, card_grid, on='SPO_NO_CD', how='left')
        geo_df_seocho = gpd.GeoDataFrame(merged_seocho_data, geometry='geometry')
        geo_df_gangnam = gpd.GeoDataFrame(merged_gangnam_data, geometry='geometry')
        geo_df_seocho = geo_df_seocho[geo_df_seocho['SECT_CD'] != '11680']
        geo_df_gangnam = geo_df_gangnam[geo_df_gangnam['SECT_CD'] != '11650']

        geo_df_seocho.to_file(PATH_RESULT3 + f"//격자//카드격자2//{file_name}_서초구.gpkg", driver='GPKG')
        geo_df_gangnam.to_file(PATH_RESULT3 + f"//격자//카드격자2//{file_name}_강남구.gpkg", driver='GPKG')
        print("GeoDataFrames 저장이 완료되었습니다!")
    except Exception as e:
        print(f"오류가 발생했습니다: {e}")

df = p20_md_day.copy()
df.columns = ['_'.join(map(str, col)).strip() for col in df.columns]
df = df.drop(index=0)
df = df.iloc[:, 1:]
df.rename(columns={df.columns[0]: 'SPO_NO_CD'}, inplace=True)

# 서초구와 강남구 데이터 분리
seocho_columns = ['SPO_NO_CD'] + [col for col in df.columns if '서초구' in str(col)]
gangnam_columns = ['SPO_NO_CD'] + [col for col in df.columns if '강남구' in str(col)]
seocho_data = df[seocho_columns]
gangnam_data = df[gangnam_columns]

merged_seocho_data = pd.merge(seocho_data, card_grid, on='SPO_NO_CD', how='left')
merged_gangnam_data = pd.merge(gangnam_data, card_grid, on='SPO_NO_CD', how='left')
geo_df_seocho = gpd.GeoDataFrame(merged_seocho_data, geometry='geometry')
geo_df_gangnam = gpd.GeoDataFrame(merged_gangnam_data, geometry='geometry')
geo_df_seocho = geo_df_seocho[geo_df_seocho['SECT_CD'] != '11680']
geo_df_gangnam = geo_df_gangnam[geo_df_gangnam['SECT_CD'] != '11650']

geo_df_seocho.to_file(PATH_RESULT3 + f"//격자//카드격자2//a29_격자_p20_의료요일_서초구.gpkg", driver='GPKG')
geo_df_gangnam.to_file(PATH_RESULT3 + f"//격자//카드격자2//a29_격자_p20_의료요일_강남구.gpkg", driver='GPKG')


process_and_save_geo_data(p20_md, file_name='a29_격자_p20_의료')
process_and_save_geo_data(p20_md_day, file_name='a29_격자_p20_의료요일1')
process_and_save_geo_data(p22_time, file_name='a29_격자_p22_소매유통시간')
process_and_save_geo_data(p22_day, file_name='a29_격자_p22_소매유통요일')
process_and_save_geo_data(p24, file_name='a29_격자_p24_교육11시')
process_and_save_geo_data(p24_sat, file_name='a29_격자_p24_교육토요일')
process_and_save_geo_data(p26, file_name='a29_격자_p26_생활서비스11시')
process_and_save_geo_data(p26_sat, file_name='a29_격자_p26_생활서비스토요일')
process_and_save_geo_data(p28, file_name='a29_격자_p28_음식시간')
process_and_save_geo_data(p28_sat, file_name='a29_격자_p28_음식토요일')





















