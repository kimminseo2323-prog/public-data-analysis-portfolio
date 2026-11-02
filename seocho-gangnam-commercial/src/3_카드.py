###########################################################
# 과 제 명: A39_서초구_인구이동 및 도시계획
# 파 일 명: 카드 분석
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

############################################ 카드 #####################################################################
'''
# 행정동별성연령대별/2020~2022.08 : hjd_card_month_sxage
df1 = pd.read_excel(path_data_out + '//빅데이터캠퍼스//카드//행정동별(2020~2022.08)//행정동별_성연령대별(2020).xlsx')
df1['card_total_amount_org'] = df1['card_total_amount_ratio'] * 16210910819317
df1['card_total_count_org'] = df1['card_total_count_ratio'] * 408427676

df1_p = df1[['기준년월', '서울시민업종코드', 'CLASS1', 'CLASS2', 'CLASS3', 'SIGNGU_NM',
       'ADSTRD_NM', '성별', '연령대별', 'card_amount_grate', 'card_count_grate',
       'card_total_amount_org', 'card_total_count_org','card_mean_amount_ratio', 'card_mean_count_ratio']]

df2 = pd.read_excel(path_data_out + '//빅데이터캠퍼스//카드//행정동별(2020~2022.08)//행정동별_성연령대별(2021).xlsx')
df2['card_total_amount_org'] = df2['card_total_amount_ratio'] * 18547532084223
df2['card_total_count_org'] = df2['card_total_count_ratio'] * 426945907
df2_p = df2[['기준년월', '서울시민업종코드', 'CLASS1', 'CLASS2', 'CLASS3', 'SIGNGU_NM',
       'ADSTRD_NM', '성별', '연령대별', 'card_amount_grate', 'card_count_grate',
       'card_total_amount_org', 'card_total_count_org','card_mean_amount_ratio', 'card_mean_count_ratio']]

df3 = pd.read_excel(path_data_out + '//빅데이터캠퍼스//카드//행정동별(2020~2022.08)//행정동별_성연령대별(2022).xlsx')
df3['card_total_amount_org'] = df3['card_total_amount_ratio'] * 14152085744208
df3['card_total_count_org'] = df3['card_total_count_ratio'] * 310221627
df3_p = df3[['기준년월', '서울시민업종코드', 'CLASS1', 'CLASS2', 'CLASS3', 'SIGNGU_NM',
       'ADSTRD_NM', '성별', '연령대별', 'card_amount_grate', 'card_count_grate',
       'card_total_amount_org', 'card_total_count_org','card_mean_amount_ratio', 'card_mean_count_ratio']]

dfs = [df1, df2, df3]
hjd_card_month_sxage = pd.concat(dfs, ignore_index=True)

# 행정동별일별소비지역별/2023 ~ 2024 : hjd_card_day_cost
df1 = pd.read_csv(path_data_out + '//빅데이터캠퍼스//카드//행정동별_일별소비지역별//행정동별_일별소비지역별_2023.csv')
df2 = pd.read_csv(path_data_out + '//빅데이터캠퍼스//카드//행정동별_일별소비지역별//행정동별_일별소비지역별_2024.csv')
dfs = [df1, df2]
hjd_card_day_cost = pd.concat(dfs, ignore_index=True)
hjd_card_day_cost['card_total_amount_org'] = hjd_card_day_cost['card_total_amount_ratio'] * 53198961296189
hjd_card_day_cost['card_total_count_org'] = hjd_card_day_cost['card_total_count_ratio'] * 802604684


# 행정동별일별시간대별/2023 ~ 2024 : hjd_card_day_time
df1 = pd.read_csv(path_data_out + '//빅데이터캠퍼스//카드//행정동별_일별시간대별//행정동별_일별시간대별_2023.csv')
df2 = pd.read_csv(path_data_out + '//빅데이터캠퍼스//카드//행정동별_일별시간대별//행정동별_일별시간대별_2024.csv')
dfs = [df1, df2]
hjd_card_day_time = pd.concat(dfs, ignore_index=True)
hjd_card_day_time['card_total_amount_org'] = hjd_card_day_time['card_total_amount_ratio'] * 58258489224495
hjd_card_day_time['card_total_count_org'] = hjd_card_day_time['card_total_count_ratio'] * 886922251


# 가맹점행정동별_내국인성연령대별/2023 ~2024 : costhjd_card_month_sxage
df1 = pd.read_csv(path_data_out + '//빅데이터캠퍼스//카드//가맹점행정동별_내국인성연령대별//가맹점행정동별_내국인성연령대별_2023.csv')
df2 = pd.read_csv(path_data_out + '//빅데이터캠퍼스//카드//가맹점행정동별_내국인성연령대별//가맹점행정동별_내국인성연령대별_2024.csv')
dfs = [df1, df2]
costhjd_card_month_sxage = pd.concat(dfs, ignore_index=True)
costhjd_card_month_sxage['card_total_amount_org'] = costhjd_card_month_sxage['card_total_amount_ratio'] * 302056665491219
costhjd_card_month_sxage['card_total_count_org'] = costhjd_card_month_sxage['card_total_count_ratio'] * 3078111540

# 집계구별일별소비지역별/2020 ~ 2022.08 : oa_card_day_cost
df1 = pd.read_pickle(path_data_out + '//빅데이터캠퍼스//카드//집계구별_일별소비지역별//집계구별_일별소비지역별(2020).pkl')
df1['card_total_amount_org'] = df1['card_total_amount_ratio'] * 16393090832401
df1['card_total_count_org'] = df1['card_total_count_ratio'] * 406930580
df2 = pd.read_pickle(path_data_out + '//빅데이터캠퍼스//카드//집계구별_일별소비지역별//집계구별_일별소비지역별(2021).pkl')
df2['card_total_amount_org'] = df2['card_total_amount_ratio'] * 18547974386169
df2['card_total_count_org'] = df2['card_total_count_ratio'] * 425141990
df3 = pd.read_pickle(path_data_out + '//빅데이터캠퍼스//카드//집계구별_일별소비지역별//집계구별_일별소비지역별(2022).pkl')
df3['card_total_amount_org'] = df3['card_total_amount_ratio'] * 14152978276075
df3['card_total_count_org'] = df3['card_total_count_ratio'] * 308426974
dfs = [df1, df2, df3]
oa_card_day_cost = pd.concat(dfs, ignore_index=True)

# 집계구별일별시간대별/2020 ~ 2022.08 : oa_card_day_time
df1 = pd.read_pickle(path_data_out + '//빅데이터캠퍼스//카드//집계구별_일별시간대별//집계구별_일별시간대별(2020).pkl')
df1['card_total_amount_org'] = df1['card_total_amount_ratio'] * 16393090747056
df1['card_total_count_org'] = df1['card_total_count_ratio'] * 408044896
df2 = pd.read_pickle(path_data_out + '//빅데이터캠퍼스//카드//집계구별_일별시간대별//집계구별_일별시간대별(2021).pkl')
df2['card_total_amount_org'] = df2['card_total_amount_ratio'] * 18547974304009
df2['card_total_count_org'] = df2['card_total_count_ratio'] * 425999930
df3 = pd.read_pickle(path_data_out + '//빅데이터캠퍼스//카드//집계구별_일별시간대별//집계구별_일별시간대별(2022).pkl')
df3['card_total_amount_org'] = df3['card_total_amount_ratio'] * 14152978204481
df3['card_total_count_org'] = df3['card_total_count_ratio'] * 309720053
dfs = [df1, df2, df3]
oa_card_day_time = pd.concat(dfs, ignore_index=True)

# 50M격자 내 가맹점기준_일별시간대별/2023.08 ~ 2024.08 : 50_card_day_time
df1 = pd.read_pickle(path_data_out + '//빅데이터캠퍼스//카드//50M격자내가맹점기준_일별시간대별//202308.pkl')
df2 = pd.read_pickle(path_data_out + '//빅데이터캠퍼스//카드//50M격자내가맹점기준_일별시간대별//202309.pkl')
df3 = pd.read_pickle(path_data_out + '//빅데이터캠퍼스//카드//50M격자내가맹점기준_일별시간대별//202310.pkl')
df4 = pd.read_pickle(path_data_out + '//빅데이터캠퍼스//카드//50M격자내가맹점기준_일별시간대별//202311.pkl')
df5 = pd.read_pickle(path_data_out + '//빅데이터캠퍼스//카드//50M격자내가맹점기준_일별시간대별//202312.pkl')
df6 = pd.read_pickle(path_data_out + '//빅데이터캠퍼스//카드//50M격자내가맹점기준_일별시간대별//202401.pkl')
df7 = pd.read_pickle(path_data_out + '//빅데이터캠퍼스//카드//50M격자내가맹점기준_일별시간대별//202402.pkl')
df8 = pd.read_pickle(path_data_out + '//빅데이터캠퍼스//카드//50M격자내가맹점기준_일별시간대별//202403.pkl')
df9 = pd.read_pickle(path_data_out + '//빅데이터캠퍼스//카드//50M격자내가맹점기준_일별시간대별//202404.pkl')
df10 = pd.read_pickle(path_data_out + '//빅데이터캠퍼스//카드//50M격자내가맹점기준_일별시간대별//202405.pkl')
df11 = pd.read_pickle(path_data_out + '//빅데이터캠퍼스//카드//50M격자내가맹점기준_일별시간대별//202406.pkl')
df12 = pd.read_pickle(path_data_out + '//빅데이터캠퍼스//카드//50M격자내가맹점기준_일별시간대별//202407.pkl')
df13 = pd.read_pickle(path_data_out + '//빅데이터캠퍼스//카드//50M격자내가맹점기준_일별시간대별//202408.pkl')


df1['카드사용금액'] = df1['카드이용금액_비율'] * 1132682078288
df1['카드사용건수'] = df1['카드이용건수_비율'] * 6671861
df2['카드사용금액'] = df2['카드이용금액_비율'] * 158810959263
df2['카드사용건수'] = df2['카드이용건수_비율'] * 3440852
df3['카드사용금액'] = df3['카드이용금액_비율'] * 964167593289
df3['카드사용건수'] = df3['카드이용건수_비율'] * 6380493
df4['카드사용금액'] = df4['카드이용금액_비율'] * 1201183383139
df4['카드사용건수'] = df4['카드이용건수_비율'] * 6508154
df5['카드사용금액'] = df5['카드이용금액_비율'] * 185528017696
df5['카드사용건수'] = df5['카드이용건수_비율'] * 3693798
df6['카드사용금액'] = df6['카드이용금액_비율'] * 1021591276035
df6['카드사용건수'] = df6['카드이용건수_비율'] * 6721117
df7['카드사용금액'] = df7['카드이용금액_비율'] * 923422297082
df7['카드사용건수'] = df7['카드이용건수_비율'] * 6946557
df8['카드사용금액'] = df8['카드이용금액_비율'] * 196492665083
df8['카드사용건수'] = df8['카드이용건수_비율'] * 4437671
df9['카드사용금액'] = df9['카드이용금액_비율'] * 943761121425
df9['카드사용건수'] = df9['카드이용건수_비율'] * 7091298
df10['카드사용금액'] = df10['카드이용금액_비율'] * 995431568800
df10['카드사용건수'] = df10['카드이용건수_비율'] * 7175490
df11['카드사용금액'] = df11['카드이용금액_비율'] * 252840837442
df11['카드사용건수'] = df11['카드이용건수_비율'] * 4647223
df12['카드사용금액'] = df12['카드이용금액_비율'] * 341501289542
df12['카드사용건수'] = df12['카드이용건수_비율'] * 7129853
df13['카드사용금액'] = df13['카드이용금액_비율'] * 242990518207
df13['카드사용건수'] = df13['카드이용건수_비율'] * 4874935

dfs = [df1, df2, df3, df4, df5, df6, df7, df8, df9, df10, df11, df12, df13]
grid50_card_day_time = pd.concat(dfs, ignore_index=True)
grid50_card_day_time = grid50_card_day_time[['SPO_NO_CD', 'SECT_CD', '기준일자', '요일', '시간대', '업종대분류', '카드사용금액', '카드사용건수']]


#데이터 저장
hjd_card_month_sxage.to_pickle(path_data_analyze + '//카드//hjd_card_month_sxage.pkl')
hjd_card_day_cost.to_pickle(path_data_analyze + '//카드//hjd_card_day_cost.pkl')
hjd_card_day_time.to_pickle(path_data_analyze + '//카드//hjd_card_day_time.pkl')
costhjd_card_month_sxage.to_pickle(path_data_analyze + '//카드//costhjd_card_month_sxage.pkl')
oa_card_day_cost.to_pickle(path_data_analyze + '//카드//oa_card_day_cost.pkl')
oa_card_day_time.to_pickle(path_data_analyze + '//카드//oa_card_day_time.pkl')
grid50_card_day_time.to_pickle(path_data_analyze + '//카드//grid50_card_day_time.pkl') # 50m 격자 내 가맹점 기준 일별 시간대별 카드데이터

# shp 매핑
grid50_card_day_time = pd.read_pickle(path_data_analyze + '//카드//grid50_card_day_time.pkl') # 50m 격자 내 가맹점 기준 일별 시간대별 카드데이터
grid50_card = gpd.read_file(path_data_out + '//빅데이터캠퍼스//카드_50m격자//pre_grid.gpkg',driver='GPKG')
grid50_card_day_time = pd.merge(grid50_card_day_time,grid50_card,on='SPO_NO_CD',how='left')
grid50_card_day_time.to_pickle(path_data_analyze + '//카드//grid50_card_day_time.pkl') # 50m 격자 내 가맹점 기준 일별 시간대별 카드데이터
'''
'''
#데이터 불러오기
hjd_card_month_sxage = pd.read_pickle('D://24project//A39_서초구 인구이동 및 도시계획 분석//2.analyze//카드//hjd_card_month_sxage.pkl')
hjd_card_day_cost = pd.read_pickle('D://24project//A39_서초구 인구이동 및 도시계획 분석//2.analyze//카드//hjd_card_day_cost.pkl')
hjd_card_day_time = pd.read_pickle('D://24project//A39_서초구 인구이동 및 도시계획 분석//2.analyze//카드//hjd_card_day_time.pkl')
costhjd_card_month_sxage = pd.read_pickle('D://24project//A39_서초구 인구이동 및 도시계획 분석//2.analyze//카드//costhjd_card_month_sxage.pkl')
oa_card_day_cost = pd.read_pickle('D://24project//A39_서초구 인구이동 및 도시계획 분석//2.analyze//카드//oa_card_day_cost.pkl')
oa_card_day_time = pd.read_pickle('D://24project//A39_서초구 인구이동 및 도시계획 분석//2.analyze//카드//oa_card_day_time.pkl')

#정합성 검증
hjd_card_day_cost['기준일자'] = pd.to_datetime(hjd_card_day_cost['기준일자'], format='%Y%m%d')
hjd_card_day_cost['연월'] = hjd_card_day_cost['기준일자'].dt.to_period('M').astype(str)
hjd_card_day_cost['행정동코드_앞5글자'] = hjd_card_day_cost['고객행정동코드'].astype(str).str[:5]
test6 = hjd_card_day_cost.groupby(['행정동코드_앞5글자','연월'])['card_total_amount_org'].sum().reset_index()
test6.to_excel(path_result + '//카드상권분석//시군구별_연월별_전체카드사용금액2.xlsx', index=False)

hjd_card_day_time['기준일자'] = pd.to_datetime(hjd_card_day_time['기준일자'], format='%Y%m%d')
hjd_card_day_time['연월'] = hjd_card_day_time['기준일자'].dt.to_period('M').astype(str)
hjd_card_day_time['행정동코드_앞5글자'] = hjd_card_day_time['고객행정동코드'].astype(str).str[:5]
test6 = hjd_card_day_time.groupby(['행정동코드_앞5글자','연월'])['card_total_amount_org'].sum().reset_index()
test6.to_excel(path_result + '//카드상권분석//시군구별_연월별_전체카드사용금액3.xlsx', index=False)

costhjd_card_month_sxage['기준일자'] = pd.to_datetime(costhjd_card_month_sxage['기준일자'], format='%Y%m%d')
costhjd_card_month_sxage['연월'] = costhjd_card_month_sxage['기준일자'].dt.to_period('M').astype(str)
costhjd_card_month_sxage['행정동코드_앞5글자'] = costhjd_card_month_sxage['가맹점행정동코드'].astype(str).str[:5]
test2 = costhjd_card_month_sxage.groupby(['행정동코드_앞5글자','연월'])['card_total_amount_org'].sum().reset_index()
test2.rename(columns={'행정동코드_앞5글자': '시군구코드'}, inplace=True)
test2['시군구명'] = test2['시군구코드'].map({'11650': '서초구', '11680': '강남구'})
test2 = test2[['시군구명','시군구코드','연월','card_total_amount_org']]
test2.to_excel(path_result + '//카드상권분석//가맹점시군구별_연월별_전체카드사용금액.xlsx', index=False)

test4 = costhjd_card_month_sxage.groupby(['행정동코드_앞5글자','업종대분류','연월'])['card_total_amount_org'].sum().reset_index()
test4 = test4[['가맹점행정동코드','업종대분류','연월','card_total_amount_org']]
test4.to_excel(path_result + '//카드상권분석//가맹점행정동별_업종별_전체카드사용금액.xlsx', index=False)
'''
'''
# 업종 매핑
org_cate = pd.read_excel(path_data_out + '//빅데이터캠퍼스//카드//업종분류_LIME.xlsx')
bigdata_cate = pd.read_excel(path_data_out + '//빅데이터캠퍼스//카드//서울시민의 업종별 카드소비 데이터.xlsx',sheet_name='2023년_서울시업종')

org_cate.columns
bigdata_cate.columns
data = pd.merge(org_cate, bigdata_cate, left_on='업종',right_on='서울시 업종', how='outer')
data.to_excel(path_data_out + '//빅데이터캠퍼스//카드//매핑업종.xlsx')
'''
#카드 데이터 50m
grid50_card_day_time = pd.read_pickle('D://24project//A39_서초구 인구이동 및 도시계획 분석//2.analyze//카드//grid50_card_day_time.pkl') # 50m 격자 내 가맹점 기준 일별 시간대별 카드데이터

#분석 대상 50m격자
card_grid = gpd.read_file(PATH_RESULT3 + '//격자//카드격자//50m격자정보//강남역_50.gpkg',driver='GPKG')
# 카드 데이터와 분석대상 격자 데이터를 공통키(SPO_NO_CD)를 사용하여 병합
filtered_card_data = pd.merge(grid50_card_day_time, card_grid[['SPO_NO_CD', 'SECT_CD']], on='SPO_NO_CD', how='inner')
print(filtered_card_data.columns)

filtered_card_data = filtered_card_data[['SPO_NO_CD', 'SECT_CD','기준일자', '요일', '시간대', '업종대분류', '카드사용금액', '카드사용건수', 'geometry']] # 컬럼추출
filtered_card_data = filtered_card_data.dropna(subset=['기준일자','업종대분류','카드사용금액', '카드사용건수']) # 널값제거
# 널값 제거 후 확인
print(filtered_card_data.isnull().sum())

# '기준일자' 컬럼을 datetime 형태로 변환
filtered_card_data['기준일자'] = filtered_card_data['기준일자'].astype(int)
filtered_card_data['기준일자'] = pd.to_datetime(filtered_card_data['기준일자'].astype(str), format='%Y%m%d')
# 월 추출
filtered_card_data['연월'] = filtered_card_data['기준일자'].dt.to_period('M').astype(str)
filtered_card_data['월'] = filtered_card_data['기준일자'].dt.month


#정상데이터 추출((동료))
import holidays
korea_holidays = holidays.KR()
filtered_card_data_isin = filtered_card_data[filtered_card_data['연월'].isin(['2023-08', '2023-10', '2023-11','2024-01','2024-02','2024-04', '2024-05', '2024-07'])]
filtered_card_data_isin['시군구명'] = filtered_card_data_isin['SECT_CD'].map({'11650': '서초구', '11680': '강남구'})
filtered_card_data_isin['휴일여부'] = filtered_card_data_isin['기준일자'].apply(lambda x: '휴일' if (x in korea_holidays or x.weekday() >= 5) else '평일')
filtered_card_data_isin_c = filtered_card_data_isin[['SPO_NO_CD', '시군구명','연월', '기준일자', '요일','휴일여부', '시간대', '업종대분류', '카드사용금액','카드사용건수']]
filtered_card_data_isin_c
filtered_card_data_isin_c.to_pickle(path_pretreat + '//카드//card_spec_month.pkl')

grid_counts = filtered_card_data_isin_c['시군구명'].value_counts()
seocho_count = grid_counts['서초구']
gangnam_count = grid_counts['강남구']
scaling_factor = seocho_count / gangnam_count


# 계절 생성
def get_season(month):
    if month in [12, 1, 2]:
        return '겨울'
    elif month in [3, 4, 5]:
        return '봄'
    elif month in [6, 7, 8]:
        return '여름'
    else:
        return '가을'
filtered_card_data['계절'] = filtered_card_data['월'].apply(get_season)
filtered_card_data['행정동'] = filtered_card_data['SECT_CD'].apply(lambda x: '서초구' if x == '11650' else '강남구' if x == '11680' else '기타')
gdf = gpd.GeoDataFrame(filtered_card_data, geometry=filtered_card_data['geometry'])

gdf_card_grid = gdf[['SPO_NO_CD','SECT_CD','geometry']].drop_duplicates()
gdf_card_grid.to_file(PATH_RESULT3 + '//격자//카드격자//50m격자정보//분석대상카드격자.gpkg', driver='GPKG')
gdf_card_grid_SC = gdf_card_grid[gdf_card_grid['SECT_CD'] == '11650']
gdf_card_grid_GN = gdf_card_grid[gdf_card_grid['SECT_CD'] == '11680']
gdf_card_grid_SC.to_file(PATH_RESULT3 + '//격자//카드격자//50m격자정보//서초구_분석대상카드격자.gpkg', driver='GPKG')
gdf_card_grid_GN.to_file(PATH_RESULT3 + '//격자//카드격자//50m격자정보//강남구_분석대상카드격자.gpkg', driver='GPKG')

# 각 격자(fid)별 행정동(SPO_NO_CD) 개수 확인
grid_count = gdf_card_grid.groupby('SPO_NO_CD')['SECT_CD'].nunique().reset_index()
grid_count.columns = ['SPO_NO_CD', 'num_of_sections']
overlapping_grids = grid_count[grid_count['num_of_sections'] > 1] # 2개 이상의 행정동에 걸쳐진 격자 필터링
overlapping_grids = pd.merge(overlapping_grids[['SPO_NO_CD']],gdf[['SPO_NO_CD','SECT_CD','geometry']],on='SPO_NO_CD',how='left')
overlapping_grids.drop_duplicates(inplace=True)
overlapping_grids = gpd.GeoDataFrame(overlapping_grids, geometry=overlapping_grids['geometry'])
overlapping_grids.to_file(PATH_RESULT3 + '//격자//카드격자//카드교차격자.gpkg', driver='GPKG')

# 1.행정동별로 카드 사용 금액 합계와 면적 비율 조정 금액 계산
card_usage_summary = (
    gdf.groupby(['행정동','연월'])
    .agg( 카드사용금액=('카드사용금액', 'sum'),  # 카드 사용 금액 합계
          총면적=('geometry', lambda x: x.unary_union.area)).reset_index())

# 서초구와 강남구 면적 가져오기
seocho_area = card_usage_summary.loc[card_usage_summary['행정동'] == '서초구', '총면적'].values[0]
gangnam_area = card_usage_summary.loc[card_usage_summary['행정동'] == '강남구', '총면적'].values[0]

# 면적 비율로 강남구 카드 사용 금액 조정
card_usage_summary['카드사용금액_면적비율'] = card_usage_summary.apply(
    lambda row: row['카드사용금액'] * (seocho_area / gangnam_area)
    if row['행정동'] == '강남구' else row['카드사용금액'],
    axis=1
)
card_usage_summary['변동폭(%)'] = card_usage_summary.groupby('행정동')['카드사용금액'].pct_change().fillna(0)
card_usage_summary.to_excel(path_result + '//카드상권분석//행정동별_월별_카드사용금액추이(최근1년).xlsx', index=False)

# 2. 계절별 카드사용금액 합계 계산
seasonal_card_usage = gdf.groupby(['행정동', '계절']).agg(카드사용금액=('카드사용금액', 'sum')).reset_index()
# 서초구와 강남구 총 면적 계산
total_area = gdf.groupby('행정동')['geometry'].apply(lambda x: x.unary_union.area)
seocho_area = total_area['서초구']
gangnam_area = total_area['강남구']


# 면적 비율 조정된 값 추가
seasonal_card_usage['카드사용금액_면적비율'] = seasonal_card_usage.apply(
    lambda row: row['카드사용금액'] * (seocho_area / gangnam_area)
    if row['행정동'] == '강남구' else row['카드사용금액'],
    axis=1
)
seasonal_card_usage.to_excel(path_result + '//카드상권분석//행정동별_계절별_카드사용금액추이(최근1년).xlsx', index=False)


# 3. 업종별 카드사용 금액 막대그래프 (서초, 강남비교)
gdf['업종대분류'].nunique() #72개
top10 = gdf[gdf['행정동'] == '서초구']
# 서초구 기준 상위 10개 업종 선정
top_10_sectors = (
    top10.groupby('업종대분류')['카드사용금액'].sum()
    .sort_values(ascending=False)
    .head(10).index.tolist()
)

# 행정동별 상위 10개 업종의 카드사용금액 계산
sector_usage = (
    filtered_card_data[filtered_card_data['업종대분류'].isin(top_10_sectors)]
    .groupby(['행정동', '업종대분류'])['카드사용금액'].sum()
    .reset_index()
)
# 면적 비율 조정 값 추가
sector_usage['카드사용금액_조정'] = sector_usage.apply(
    lambda row: row['카드사용금액'] * (seocho_area / gangnam_area)
    if row['행정동'] == '강남구' else row['카드사용금액'],
    axis=1
)

sector_usage.to_excel(path_result + '//카드상권분석//행정동별_업종별_카드사용금액추이(최근1년상위10개).xlsx', index=False)


# 업종별 카드 금액 비중카드 사용 금액 합계 계산
hjd_industry_card_usage = (gdf.groupby(['행정동', '업종대분류'])['카드사용금액'].sum().reset_index())
pivot_table = hjd_industry_card_usage.pivot_table(index='업종대분류', columns='행정동', values='카드사용금액', aggfunc='sum', fill_value=0).reset_index()
pivot_table.rename(columns={'서초구': '서초구_카드사용금액', '강남구': '강남구_카드사용금액'}, inplace=True)
# 강남구_카드사용금액 조정 (면적 비율 적용)
pivot_table['강남구_카드사용금액_조정'] = pivot_table['강남구_카드사용금액'] * (seocho_area / gangnam_area)

# 전체 카드 사용 금액 계산
gangnam_total = pivot_table['강남구_카드사용금액'].sum()
seocho_total = pivot_table['서초구_카드사용금액'].sum()

# 강남구와 서초구의 업종별 비중 계산
pivot_table['강남구_업종별_비중'] = pivot_table['강남구_카드사용금액'] / gangnam_total
pivot_table['서초구_업종별_비중'] = pivot_table['서초구_카드사용금액'] / seocho_total
pivot_table.to_excel(path_result + '//카드상권분석//행정동별_업종별_카드사용금액비중.xlsx', index=False)


# 상위매출 top10에 대하여 월별 카드사용금액 추이
top3 = gdf[gdf['행정동'] == '서초구']
# 서초구 기준 상위 3개 업종 선정
top3 = (top3.groupby('업종대분류')['카드사용금액'].sum().sort_values(ascending=False).head(10).index.tolist())
filtered_top3 = gdf[gdf['업종대분류'].isin(top3)]

monthly_card_usage = (filtered_top3.groupby(['행정동', '연월', '업종대분류'])['카드사용금액'].sum().reset_index())
monthly_card_usage['카드사용금액_면적비율'] = monthly_card_usage.apply(lambda row: row['카드사용금액'] * (seocho_area / gangnam_area) if row['행정동'] == '강남구' else row['카드사용금액'],axis=1)
monthly_card_usage.to_excel(path_result + '//카드상권분석//행정동별_상위업종top10_월별카드사용금액.xlsx', index=False)

# 월별 업종별 카드사용금액 추이
card_data = gdf.groupby(['행정동', '연월', '업종대분류'])['카드사용금액'].sum().reset_index()
card_data['카드사용금액_면적비율'] = card_data.apply(lambda row: row['카드사용금액'] * (seocho_area / gangnam_area) if row['행정동'] == '강남구' else row['카드사용금액'],axis=1)
card_data.to_excel(path_result + '//카드상권분석//행정동별_업종별_월별카드사용금액.xlsx', index=False)

# 시간대별 카드사용금액
time_mapping = pd.DataFrame({
    '시간대': [1, 2, 3, 4, 5, 6],
    '시간': ['0시~6시 미만', '6시~11시 미만', '11시~14시 미만', '14시~17시 미만', '17시~21시 미만', '21시~24시 미만']})

gdf['평일구분'] = gdf['요일'].apply(lambda x: '주말' if x in ['토요일', '일요일'] else '평일')
gdf['시간대'] =gdf['시간대'].astype(int)
gdf_time = pd.merge(gdf,time_mapping,on='시간대',how='left')

time_usage_summary = (gdf_time.groupby(['행정동', '평일구분', '시간대','시간'])['카드사용금액'].sum().reset_index())
time_usage_summary['카드사용금액_면적비율'] = time_usage_summary.apply(lambda row: row['카드사용금액'] * (seocho_area / gangnam_area)if row['행정동'] == '강남구' else row['카드사용금액'],axis=1)
time_usage_summary.to_excel(path_result + '//카드상권분석//행정동별_평일구분_시간대별_카드사용금액.xlsx', index=False)

#시간대구간별 업종별 카드사용 금액 비중
time_usage_summary2 = (gdf_time.groupby(['행정동', '시간대','시간','업종대분류'])['카드사용금액'].sum().reset_index())
time_usage_summary2

pivot_table = time_usage_summary2.pivot_table(index=['시간대','시간','업종대분류'], columns='행정동', values='카드사용금액', aggfunc='sum', fill_value=0).reset_index()
pivot_table.reset_index(inplace=True)
# 시간대별로 강남구와 서초구 카드 사용 금액 합산
pivot_table['강남구_합계'] = pivot_table.groupby('시간대')['강남구'].transform('sum')
pivot_table['서초구_합계'] = pivot_table.groupby('시간대')['서초구'].transform('sum')

# 강남구와 서초구 카드 사용 금액에 대한 업종별 비중 계산
pivot_table['강남구_비중'] = pivot_table['강남구'] / pivot_table['강남구_합계']
pivot_table['서초구_비중'] = pivot_table['서초구'] / pivot_table['서초구_합계']

pivot_table['강남구_시간대_평균비중'] = pivot_table.groupby('시간대')['강남구_비중'].transform('mean')
pivot_table['서초구_시간대_평균비중'] = pivot_table.groupby('시간대')['서초구_비중'].transform('mean')
result = pivot_table[['시간대','시간','업종대분류', '서초구_비중','서초구_시간대_평균비중', '강남구_비중','강남구_시간대_평균비중']]
result.to_excel(path_result + '//카드상권분석//행정동별_시간대별_업종별_카드사용금액비중.xlsx', index=False)



#격자별 카드 분석
gdf_card_grid_SC = gpd.read_file(PATH_RESULT3 + '//격자//카드격자//50m격자정보//서초구_분석대상카드격자.gpkg', driver='GPKG')
gdf_card_grid_GN = gpd.read_file(PATH_RESULT3 + '//격자//카드격자//50m격자정보//강남구_분석대상카드격자.gpkg', driver='GPKG')
gdf_data_sc = gdf[gdf['SECT_CD'] == '11650'] #서초구 분석데이터
gdf_data_gn = gdf[gdf['SECT_CD'] == '11680'] #강남구 분석데이터

gdf_data_sc.columns
# 상세지역별 카드매출 - 사용금액 (1)
gdf_data_sc_g = gdf_data_sc.groupby(['SPO_NO_CD', 'SECT_CD', 'geometry'])[[ '카드사용금액','카드사용건수']].sum().reset_index()
gdf_data_gn_g = gdf_data_gn.groupby(['SPO_NO_CD', 'SECT_CD', 'geometry'])[[ '카드사용금액','카드사용건수']].sum().reset_index()
gdf_data_sc_g = gpd.GeoDataFrame(gdf_data_sc_g, geometry='geometry')
gdf_data_gn_g = gpd.GeoDataFrame(gdf_data_gn_g, geometry='geometry')
gdf_data_sc_g.to_file(PATH_RESULT3 + '//격자//카드격자//서초구_카드사용금액_최근1년.gpkg', driver='GPKG')
gdf_data_gn_g.to_file(PATH_RESULT3 + '//격자//카드격자//강남구_카드사용금액_최근1년.gpkg', driver='GPKG')

# 상세지역별 카드매출 - 업종별 사용금액 (2)
sc_top_10 = gdf_data_sc.groupby(['업종대분류'])[[ '카드사용금액','카드사용건수']].sum().reset_index()
gn_top_10 = gdf_data_gn.groupby(['업종대분류'])[[ '카드사용금액','카드사용건수']].sum().reset_index()
sc_top_1 = sc_top_10[sc_top_10['카드사용금액'] == sc_top_10['카드사용금액'].max()] # 일반병원  1.695789e+12  3.395528e+06
gn_top_1 = gn_top_10[gn_top_10['카드사용금액'] == gn_top_10['카드사용금액'].max()] # 보험  6.397638e+12  4.541638e+07

gdf_data_gn_top1 = gdf_data_gn[gdf_data_gn['업종대분류'] == '보험']
gdf_data_sc_top1 = gdf_data_sc[gdf_data_sc['업종대분류'] == '일반병원']
gdf_data_gn_top1 = gdf_data_gn_top1.groupby(['SPO_NO_CD', 'SECT_CD', 'geometry'])[[ '카드사용금액','카드사용건수']].sum().reset_index()
gdf_data_sc_top1 = gdf_data_sc_top1.groupby(['SPO_NO_CD', 'SECT_CD', 'geometry'])[[ '카드사용금액','카드사용건수']].sum().reset_index()

gdf_data_gn_top1 = gpd.GeoDataFrame(gdf_data_gn_top1, geometry='geometry')
gdf_data_sc_top1 = gpd.GeoDataFrame(gdf_data_sc_top1, geometry='geometry')
gdf_data_sc_top1.to_file(PATH_RESULT3 + '//격자//카드격자//서초구_top1업종_카드사용금액_최근1년.gpkg', driver='GPKG')
gdf_data_gn_top1.to_file(PATH_RESULT3 + '//격자//카드격자//강남구_top1업종_카드사용금액_최근1년.gpkg', driver='GPKG')


# 8월기준 증가율
# 상세지역별 카드매출 - 금액증가율
gdf_data_sc_8 = gdf_data_sc[gdf_data_sc['월'] == 8]
gdf_data_gn_8 = gdf_data_gn[gdf_data_gn['월'] == 8]
gdf_data_sc_8['연도'] = gdf_data_sc_8['기준일자'].dt.year
gdf_data_gn_8['연도'] = gdf_data_gn_8['기준일자'].dt.year
gdf_data_sc_8g = gdf_data_sc_8.groupby(['SPO_NO_CD', '연도', '업종대분류', 'geometry'])['카드사용금액'].sum().reset_index()
gdf_data_gn_8g = gdf_data_gn_8.groupby(['SPO_NO_CD', '연도', '업종대분류', 'geometry'])['카드사용금액'].sum().reset_index()


# 증가율 계산
# 전년도 대비 증가율 계산
gdf_data_sc_8g['전년도대비증가율'] = (
    gdf_data_sc_8g.sort_values(by=['SPO_NO_CD', '업종대분류', '연도'])  # 격자, 업종, 연도를 기준으로 정렬
    .groupby(['SPO_NO_CD', '업종대분류'])['카드사용금액']          # 격자와 업종별로 그룹화
    .pct_change()                              # 전년도 대비 증가율 계산
    * 100                                      # 백분율로 변환
)
gdf_data_gn_8g['전년도대비증가율'] = (
    gdf_data_gn_8g.sort_values(by=['SPO_NO_CD', '업종대분류', '연도'])  # 격자, 업종, 연도를 기준으로 정렬
    .groupby(['SPO_NO_CD', '업종대분류'])['카드사용금액']          # 격자와 업종별로 그룹화
    .pct_change()                              # 전년도 대비 증가율 계산
    * 100                                      # 백분율로 변환
)

grid_avg_growth = gdf_data_sc_8g.groupby('SPO_NO_CD')['전년도대비증가율'].mean().reset_index()
grid_avg_growth.rename(columns={'전년도대비증가율': '격자별_증가율평균'}, inplace=True)
gdf_data_sc_8g = pd.merge(gdf_data_sc_8g, grid_avg_growth, on='SPO_NO_CD', how='left')

grid_avg_growth = gdf_data_gn_8g.groupby('SPO_NO_CD')['전년도대비증가율'].mean().reset_index()
grid_avg_growth.rename(columns={'전년도대비증가율': '격자별_증가율평균'}, inplace=True)
gdf_data_gn_8g = pd.merge(gdf_data_gn_8g, grid_avg_growth, on='SPO_NO_CD', how='left')

sc_with_growth = gdf_data_sc_8g[gdf_data_sc_8g['전년도대비증가율'].notna()]
gn_with_growth = gdf_data_gn_8g[gdf_data_gn_8g['전년도대비증가율'].notna()]
sc_with_growth = sc_with_growth[['SPO_NO_CD', '연도', '업종대분류', '전년도대비증가율','격자별_증가율평균', 'geometry']]
gn_with_growth = gn_with_growth[['SPO_NO_CD', '연도', '업종대분류', '전년도대비증가율','격자별_증가율평균', 'geometry']]
sc_with_growth = gpd.GeoDataFrame(sc_with_growth, geometry='geometry')
gn_with_growth = gpd.GeoDataFrame(gn_with_growth, geometry='geometry')
sc_with_growth.to_file(PATH_RESULT3 + '//격자//카드격자//서초구_8월기준_전년대비증가율.gpkg', driver='GPKG')
gn_with_growth.to_file(PATH_RESULT3 + '//격자//카드격자//강남구_8월기준_전년대비증가율.gpkg', driver='GPKG')

sc_top_10_percent = sc_with_growth[['SPO_NO_CD', '연도', '업종대분류', '전년도대비증가율','격자별_증가율평균']]
gn_top_10_percent = gn_with_growth[['SPO_NO_CD', '연도', '업종대분류', '전년도대비증가율','격자별_증가율평균']]
sc_top_10_percent.to_excel(path_result + '//카드상권분석//서초구_8월기준_전년대비증가율%.xlsx', index=False)
gn_top_10_percent.to_excel(path_result + '//카드상권분석//강남구_8월기준_전년대비증가율%.xlsx', index=False)
'''
# 격자별_증가율평균 상위 10% 격자 선택
sc_top_10_percent = sc_with_growth.nlargest(int(len(sc_with_growth) * 0.1), '격자별_증가율평균')
gn_top_10_percent = gn_with_growth.nlargest(int(len(gn_with_growth) * 0.1), '격자별_증가율평균')


sc_top_10_percent = gpd.GeoDataFrame(sc_top_10_percent, geometry='geometry')
gn_top_10_percent = gpd.GeoDataFrame(gn_top_10_percent, geometry='geometry')
sc_top_10_percent.to_file(PATH_RESULT3 + '//격자//카드격자//서초구_8월기준_격자별_증가율평균_상위10%.gpkg', driver='GPKG')
gn_top_10_percent.to_file(PATH_RESULT3 + '//격자//카드격자//강남구_8월기준_격자별_증가율평균_상위10%.gpkg', driver='GPKG')

sc_top_10_percent = sc_top_10_percent[['SPO_NO_CD', '연도', '업종대분류', '전년도대비증가율','격자별_증가율평균']]
gn_top_10_percent = gn_top_10_percent[['SPO_NO_CD', '연도', '업종대분류', '전년도대비증가율','격자별_증가율평균']]
sc_top_10_percent.to_excel(path_result + '//카드상권분석//서초구_8월기준_격자별_증가율평균_상위10%.xlsx', index=False)
gn_top_10_percent.to_excel(path_result + '//카드상권분석//강남구_8월기준_격자별_증가율평균_상위10%.xlsx', index=False)
'''
# 12월기준 카드매출
# 상세지역별 카드매출 - 금액증가율
gdf_data_sc_12 = gdf_data_sc[gdf_data_sc['월'] == 12]
gdf_data_gn_12 = gdf_data_gn[gdf_data_gn['월'] == 12]
gdf_data_sc_12['연도'] = gdf_data_sc_12['기준일자'].dt.year
gdf_data_gn_12['연도'] = gdf_data_gn_12['기준일자'].dt.year
gdf_data_sc_12G = gdf_data_sc_12.groupby(['SPO_NO_CD',  'geometry'])['카드사용금액'].sum().reset_index()
gdf_data_gn_12G = gdf_data_gn_12.groupby(['SPO_NO_CD',  'geometry'])['카드사용금액'].sum().reset_index()

gdf_data_sc_12G = gpd.GeoDataFrame(gdf_data_sc_12G, geometry='geometry')
gdf_data_gn_12G = gpd.GeoDataFrame(gdf_data_gn_12G, geometry='geometry')
gdf_data_sc_12G.to_file(PATH_RESULT3 + '//격자//카드격자//서초구_12월기준_카드사용금액.gpkg', driver='GPKG')
gdf_data_gn_12G.to_file(PATH_RESULT3 + '//격자//카드격자//강남구_12월기준_카드사용금액.gpkg', driver='GPKG')

gdf_data_sc_12c = gdf_data_sc_12.groupby(['SPO_NO_CD', '업종대분류',  'geometry'])['카드사용금액'].sum().reset_index()
gdf_data_sc_12c_g = gdf_data_sc_12c[gdf_data_sc_12c['SPO_NO_CD'] == '다사582a445a']
gdf_data_sc_12c_g = gdf_data_sc_12c_g[['업종대분류','카드사용금액']]
gdf_data_sc_12c_g.to_excel(path_result + '//카드상권분석//12월기준_top1격자_업종별.xlsx', index=False)

gdf_data_sc_12c = gdf_data_sc_12.groupby(['SPO_NO_CD', '업종대분류',  'geometry'])['카드사용금액'].sum().reset_index()
gdf_data_sc_12c = gpd.GeoDataFrame(gdf_data_sc_12c, geometry='geometry')
gdf_data_sc_12c.to_file(PATH_RESULT3 + '//격자//카드격자//서초구_12월기준_업종별_카드사용금액.gpkg', driver='GPKG')

gdf_data_gn_12c = gdf_data_gn_12.groupby(['SPO_NO_CD', '업종대분류',  'geometry'])['카드사용금액'].sum().reset_index()
gdf_data_gn_12c = gpd.GeoDataFrame(gdf_data_gn_12c, geometry='geometry')
gdf_data_gn_12c.to_file(PATH_RESULT3 + '//격자//카드격자//강남구_12월기준_업종별_카드사용금액.gpkg', driver='GPKG')

# 시간대별 카드매출
'''
구간	설명
01	0시~6시 미만
02	6시~11시 미만
03	11시~14시 미만
04	14시~17시 미만
05	17시~21시 미만
06	21시~24시 미만
'''
def time(time):
    time = str(time)
    if time in '1.0':
        return '0시~6시 미만'
    elif time in '2.0':
        return '6시~11시 미만'
    elif time in '3.0':
        return '11시~14시 미만'
    elif time in '4.0':
        return '14시~17시 미만'
    elif time in '5.0':
        return '17시~21시 미만'
    elif time in '6.0':
        return '21시~24시 미만'
gdf_data_sc['연도'] = gdf_data_sc['기준일자'].dt.year
gdf_data_gn['연도'] = gdf_data_gn['기준일자'].dt.year

gdf_data_sc_2024 = gdf_data_sc[gdf_data_sc['연도'] == 2024]
gdf_data_sc_t = gdf_data_sc_2024.groupby(['SPO_NO_CD','시간대', '업종대분류', 'geometry'])[['카드사용금액','카드사용건수']].sum().reset_index()
gdf_data_sc_t['시간대구분']= gdf_data_sc_t['시간대'].apply(time)
gdf_data_gn_2024 = gdf_data_gn[gdf_data_gn['연도'] == 2024]
gdf_data_gn_t = gdf_data_gn.groupby(['SPO_NO_CD','시간대', '업종대분류', 'geometry'])[['카드사용금액','카드사용건수']].sum().reset_index()
gdf_data_gn_t['시간대구분']= gdf_data_gn_t['시간대'].apply(time)

# 오후 시간대만 추출
gdf_data_sc_4 = gdf_data_sc_t[gdf_data_sc_t['시간대'] == 4.0]
gdf_data_gn_4 = gdf_data_gn_t[gdf_data_gn_t['시간대'] == 4.0]
# 저녁 시간대만 추출
gdf_data_sc_5 = gdf_data_sc_t[gdf_data_sc_t['시간대'] == 5.0]
gdf_data_gn_5 = gdf_data_gn_t[gdf_data_gn_t['시간대'] == 5.0]

gdf_data_sc_4g = gpd.GeoDataFrame(gdf_data_sc_4, geometry='geometry')
gdf_data_gn_4g = gpd.GeoDataFrame(gdf_data_gn_4, geometry='geometry')
gdf_data_sc_4g.to_file(PATH_RESULT3 + '//격자//카드격자//서초구_오후시간대_카드매출.gpkg', driver='GPKG')
gdf_data_gn_4g.to_file(PATH_RESULT3 + '//격자//카드격자//강남구_오후시간대_카드매출.gpkg', driver='GPKG')

gdf_data_sc_5g = gpd.GeoDataFrame(gdf_data_sc_5, geometry='geometry')
gdf_data_gn_5g = gpd.GeoDataFrame(gdf_data_gn_5, geometry='geometry')
gdf_data_sc_5g.to_file(PATH_RESULT3 + '//격자//카드격자//서초구_저녁시간대_카드매출.gpkg', driver='GPKG')
gdf_data_gn_5g.to_file(PATH_RESULT3 + '//격자//카드격자//강남구_저녁시간대_카드매출.gpkg', driver='GPKG')

# 시간대별 차이업종
gdf_data_sc_2024 = gdf_data_sc[gdf_data_sc['연도'] == 2024]
gdf_data_sc_tt = gdf_data_sc_2024.groupby(['시간대', '업종대분류'])[['카드사용금액','카드사용건수']].sum().reset_index()
gdf_data_sc_tt['시간대구분']= gdf_data_sc_tt['시간대'].apply(time)
gdf_data_gn_2024 = gdf_data_gn[gdf_data_gn['연도'] == 2024]
gdf_data_gn_tt = gdf_data_gn_2024.groupby(['시간대', '업종대분류'])[['카드사용금액','카드사용건수']].sum().reset_index()
gdf_data_gn_tt['시간대구분']= gdf_data_gn_tt['시간대'].apply(time)

# 보험, ZZ나머지 제외
excluded_categories = ['보험', "ZZ_나머지"]
filtered_df1 = gdf_data_sc_2024[~gdf_data_sc_2024["업종대분류"].isin(excluded_categories)]
filtered_df2 = gdf_data_gn_2024[~gdf_data_gn_2024["업종대분류"].isin(excluded_categories)]

# 시간대별 카드사용금액이 가장 많은 업종 추출
top_category_per_time = filtered_df1.groupby(['시간대','업종대분류'])["카드사용금액"].sum().reset_index()
top_seocho = top_category_per_time.loc[top_category_per_time.groupby("시간대")["카드사용금액"].idxmax()]

top_category_per_time2 = filtered_df2.groupby(['시간대','업종대분류'])["카드사용금액"].sum().reset_index()
top_gangnam  = top_category_per_time2.loc[top_category_per_time2.groupby("시간대")["카드사용금액"].idxmax()]

# 서초구와 강남구 데이터 병합
merged_df = pd.merge(
    top_category_per_time,
    top_category_per_time2,
    on=["시간대", "업종대분류"],
    suffixes=("_서초", "_강남")
)

# 강남 > 서초 조건 필터링
merged_df["금액차이"] = merged_df["카드사용금액_강남"] - merged_df["카드사용금액_서초"]
merged_df.to_excel(path_result + '//카드상권분석//시간대별_업종별차이(강남-서초)_2024기준.xlsx', index=False)
filtered_df = merged_df[merged_df["금액차이"] > 0]
# 시간대별로 강남이 서초보다 크고 차이가 큰 업종 추출
top_diff_per_time = filtered_df.loc[filtered_df.groupby("시간대")["금액차이"].idxmax()]
top_diff_per_time.to_excel(path_result + '//카드상권분석//시간대별_차이업종TOP(강남-서초)_2024기준.xlsx', index=False)


gdf_data_sc_2024 = gdf_data_sc[gdf_data_sc['연도'] == 2024]
gdf_data_gn_2024 = gdf_data_gn[gdf_data_gn['연도'] == 2024]

gdf_data_sc_tt = gdf_data_sc_2024.groupby(['SPO_NO_CD','시간대', '업종대분류', 'geometry'])[['카드사용금액','카드사용건수']].sum().reset_index()
gdf_data_gn_tt = gdf_data_gn_2024.groupby(['SPO_NO_CD','시간대', '업종대분류', 'geometry'])[['카드사용금액','카드사용건수']].sum().reset_index()
gdf_data_sc_tt = gpd.GeoDataFrame(gdf_data_sc_tt, geometry='geometry')
gdf_data_gn_tt = gpd.GeoDataFrame(gdf_data_gn_tt, geometry='geometry')
gdf_data_sc_tt.to_file(PATH_RESULT3 + '//격자//카드격자//서초구_시간대별_업종별_카드사용금액.gpkg', driver='GPKG')
gdf_data_gn_tt.to_file(PATH_RESULT3 + '//격자//카드격자//강남구_시간대별_업종별_카드사용금액.gpkg', driver='GPKG')