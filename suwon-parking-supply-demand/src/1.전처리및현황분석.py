###########################################################
# 과 제 명: A28_수원시_주차장수요공급분석
# 파 일 명: 1.전처리_현황
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
fl.f_log_line("1.전처리및현황분석.py")

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
from shapely.geometry import Point
from shapely import wkt
import numpy as np
####################################### 경계면데이터 좌표계 변환 전처리 #######################################
## 경계면 데이터 불러오기
grid100_sw = gpd.read_file(path_data_out + '//100m격자//nlsp_021001001.shp',encoding = 'utf-8') # 수원시 100m 격자 - 거주인구(2024.04 기준)
grid100_sw_5179 = gpd.GeoDataFrame(grid100_sw,geometry='geometry',crs=5179)
grid100_sw_5179['val'] = grid100_sw_5179['val'].fillna(0)
grid100_sw_5179.to_file(PATH_RESULT3 + '//100M격자_거주인구//100m격자_거주인구.gpkg',driver='GPKG')

sgg_cd = gpd.read_file(path_data_out + '//시군구경계//BND_SIGUNGU_PG.shp',encoding = 'cp949') # 수원시 시군구경계
codes = ['31011', '31012', '31013', '31014'] # 'SIGUNGU_CD' 열의 값이 codes 리스트에 포함된 행 필터링
sw_sgg = sgg_cd[sgg_cd['SIGUNGU_CD'].isin(codes)]
sw_sgg_5179 = sw_sgg.to_crs(epsg=5179)
sw_sgg_5179.to_file(PATH_RESULT3 + '//시군구경계//시군구경계.gpkg',driver='GPKG')

hjd_cd = gpd.read_file(path_data_in + '//2024-07-15//행정동경계//행정동.shp',encoding = 'cp949') ##행정동 (2023.07 기준)
hjd_cd.nunique()
hjd_cd.head()
hjd_cd.crs
hjd_cd.columns = [['']]
#hjd_cd.to_file(PATH_RESULT3 + '//행정동경계//행정동경계.gpkg',driver='GPKG')
hjd_cd.columns
hjd_cd_kr = hjd_cd[['ADM_NM', 'ADM_CD', 'geometry']]
hjd_cd_kr.to_excel(path_data_analyze +'//행정동코드//hjd_cd.xlsx',index=False)


base_cd = gpd.read_file(path_data_in + '//2024-07-15//기초구역경계//기초구역.shp',encoding = 'utf-8') #기초구역
base_cd.columns = ['면적','기초구역번호','관리번호','시도명','이동일자','이동사유','고시일자','작업일시','시군구코드','시군구명','geometry']
base_cd = base_cd[['기초구역번호','관리번호','면적','geometry']]
base_cd.head()
base_cd.nunique()
base_cd_5179 = gpd.GeoDataFrame(base_cd,geometry='geometry',crs=5179)
base_cd_5179.crs
#base_cd_5179.to_file(PATH_RESULT3 + '//기초구역경계//기초구역경계.gpkg',driver='GPKG')
###################################################################################################


#경계면데이터
grid100_sw_5179 = gpd.read_file(PATH_RESULT3 + '//거주인구//100m격자_거주인구.gpkg',driver='GPKG') # 100m격자-거주인구
sgg_cd = gpd.read_file(PATH_RESULT3 + '//경계면데이터//시군구경계//시군구경계.gpkg',driver='GPKG') #행정동경계
hjd_cd = gpd.read_file(PATH_RESULT3 + '//경계면데이터//행정동경계//행정동경계.gpkg',driver='GPKG') #행정동경계
base_cd_5179 = gpd.read_file(PATH_RESULT3 + '//경계면데이터//기초구역경계//기초구역경계.gpkg',driver='GPKG') #기초구역경계
sgg_hjd = pd.read_excel(path_data_analyze +'//행정동코드//sgg_hjd.xlsx')
card_block = gpd.read_file(path_data_in +'//2024-07-15//카드블록경계//tbshp_block_v8.shp',encoding='cp949')


hjd_cd['ADM_CD'] = hjd_cd['ADM_CD'].astype(int)
sgg_hjd = pd.merge(sgg_hjd,hjd_cd,on=['ADM_NM','ADM_CD'],how='left')
sgg_hjd = sgg_hjd[['시군구명','ADM_NM','ADM_CD','geometry']]
sgg_hjd = gpd.GeoDataFrame(sgg_hjd,geometry='geometry',crs=5179)
sgg_hjd.rename(columns={'ADM_NM': '행정동명'}, inplace=True)
sgg_hjd.rename(columns={'ADM_CD': '행정동코드'}, inplace=True)
sgg_hjd.to_file(PATH_RESULT3 + '//행정동경계//시군구_행정동경계.gpkg',driver='GPKG')


# 주차장 및 차량 데이터 원천
parking1 = pd.read_excel(path_data_in + '//2024-06-13//분석용 데이터//공영주차장_202405//1. 공영주차장.xlsx',sheet_name='Sheet3') #66개
parking2 = pd.read_excel(path_data_in + '//2024-06-13//분석용 데이터//공영주차장_202405//2. 거주자우선주차장.xlsx') #4012개

# 공영주차장 데이터 지오코딩 후 전처리
parking1_shp = gpd.read_file(path_data_analyze + '//지오코딩//공영주차장//공영주차장.shp',encoding='cp949') #공영주차장
parking1_shp = parking1_shp[['구분', '주차장명', '주소', '주차면수','geometry']]
pre_parking1 = parking1_shp.drop_duplicates()
pre_parking1 = gpd.GeoDataFrame(pre_parking1, geometry='geometry', crs='EPSG:4326')
pre_parking1_5179 = pre_parking1.to_crs(epsg=5179)

# 공영주차장 현황분석

# 시군구명 행정동명 매핑
parking1_result = gpd.sjoin(pre_parking1_5179,sgg_hjd, how='left', op='within')
parking1_result = parking1_result[[ '시군구명', '행정동명','행정동코드','구분', '주차장명', '주소', '주차면수', 'geometry']]
#기초구역 번호 매핑
parking1_result = gpd.sjoin( parking1_result,base_cd_5179, how='left', op='within')
parking1_result.columns
parking1_result = parking1_result[['시군구명', '행정동명', '행정동코드','기초구역번호', '구분', '주소', '주차면수', '면적','geometry']]

parking1_result.to_excel(path_result+'//주차장현황//공영주차장.xlsx',index=False)
parking1_result.to_file(PATH_RESULT3+'//주차장//공영주차장.gpkg',driver='GPKG')


#거주자우선주차장 데이터 지오코딩 후 전처리
parking2_shp = gpd.read_file(path_data_analyze + '//지오코딩//거주자우선주차장//거주자우선주차장.shp',encoding='cp949') #거주자우선주차장
parking2_shp = parking2_shp[['거주자우선','운영형태','소재지지번', 'geometry']]
parking2_shp = parking2_shp.drop_duplicates()
parking2_shp = gpd.GeoDataFrame(parking2_shp, geometry='geometry', crs='EPSG:4326')
pre_parking2_5179 = parking2_shp.to_crs(epsg=5179)
pre_parking2_5179.rename(columns={'거주자우선': '주차구역명'}, inplace=True)

# 거주자우선주차장 현황분석
parking22 = parking2[['거주자우선주차구획번호', '거주자우선주차구획위도', '거주자우선주차구획경도','거주자우선주차구역명' ,'소재지지번주소', '운영형태' ]]
parking22.rename(columns={'소재지지번주소': '소재지지번'}, inplace=True)
parking22.rename(columns={'거주자우선주차구역명': '주차구역명'}, inplace=True)
parking2_result = pd.merge(parking22,pre_parking2_5179[['주차구역명','소재지지번', 'geometry']],how='left',on=['소재지지번','주차구역명'])
parking2_result = gpd.GeoDataFrame(parking2_result, geometry='geometry')
parking2_result_5179 = parking2_result.to_crs(epsg=5179)

# 시군구명 행정동명 매핑
parking2_result = gpd.sjoin(parking2_result_5179,sgg_hjd, how='left', op='within')
parking2_result.rename(columns={'소재지지번': '주소'}, inplace=True)
parking2_result.rename(columns={'주차구역명': '주차장명'}, inplace=True)
parking2_result = parking2_result[[ '시군구명', '행정동명','행정동코드','운영형태', '주차장명', '주소', 'geometry']]

#기초구역 번호 매핑
parking2_result = gpd.sjoin( parking2_result,base_cd_5179, how='left', op='within')
parking2_result = parking2_result[['시군구명', '행정동명','행정동코드','기초구역번호','운영형태', '주차장명', '주소', 'geometry']]
parking2_result.to_excel(path_result+'//주차장현황//거주자우선주차장.xlsx',index=False)
parking2_result.to_file(PATH_RESULT3+'//주차장//거주자우선주차장.gpkg',driver='GPKG')


#행궁동 일대만 수원시 표제부 데이터로 지오코딩  + #대표표제부 데이터 수급
# 건축물대장 표제부
jang = pd.read_excel(path_data_in + "//2024-06-13//분석용 데이터//건축물대장 표제부_202404//1. 장안구.xlsx",skiprows=4)
gwon = pd.read_excel(path_data_in + "//2024-06-13//분석용 데이터//건축물대장 표제부_202404//2. 권선구.xlsx",skiprows=4)
pal = pd.read_excel(path_data_in + "//2024-06-13//분석용 데이터//건축물대장 표제부_202404//3. 팔달구.xlsx",skiprows=4)
young = pd.read_excel(path_data_in + "//2024-06-13//분석용 데이터//건축물대장 표제부_202404//4. 영통구.xlsx",skiprows=4)

jang['시군구'] = '장안구'
gwon['시군구'] = '권선구'
pal['시군구'] = '팔달구'
young['시군구'] = '영통구'

pre_jang = jang[['시군구','대지위치','건물명','주용도코드명','옥내기계식대수(대)', '옥내기계식면적(㎡)', '옥외기계식대수(대)',
                 '옥외기계식면적(㎡)','옥내자주식대수(대)', '옥내자주식면적(㎡)', '옥외자주식대수(대)', '옥외자주식면적(㎡)']]

pre_gwon = gwon[['시군구','대지위치','건물명','주용도코드명','옥내기계식대수(대)', '옥내기계식면적(㎡)', '옥외기계식대수(대)',
                 '옥외기계식면적(㎡)','옥내자주식대수(대)', '옥내자주식면적(㎡)', '옥외자주식대수(대)', '옥외자주식면적(㎡)']]

pre_pal = pal[['시군구','대지위치','건물명','주용도코드명','옥내기계식대수(대)', '옥내기계식면적(㎡)', '옥외기계식대수(대)',
                 '옥외기계식면적(㎡)','옥내자주식대수(대)', '옥내자주식면적(㎡)', '옥외자주식대수(대)', '옥외자주식면적(㎡)']]

pre_young = young[['시군구','대지위치','건물명','주용도코드명','옥내기계식대수(대)', '옥내기계식면적(㎡)', '옥외기계식대수(대)',
                 '옥외기계식면적(㎡)','옥내자주식대수(대)', '옥내자주식면적(㎡)', '옥외자주식대수(대)', '옥외자주식면적(㎡)']]

br_data = pd.concat([pre_jang,pre_gwon,pre_pal,pre_young],axis=0).reset_index(drop=True)
pre_br_data1 = br_data.groupby(['시군구', '대지위치','건물명','주용도코드']).first().reset_index()

pre_br_data1['총주차수'] = pre_br_data1[['옥내기계식대수(대)','옥외기계식대수(대)','옥내자주식대수(대)','옥외자주식대수(대)']].sum(axis=1)
pre_br_data1 = pre_br_data1[['시군구','대지위치','주용도코드명','건물명','총주차수','옥내기계식대수(대)', '옥내기계식면적(㎡)', '옥외기계식대수(대)','옥외기계식면적(㎡)','옥내자주식대수(대)', '옥내자주식면적(㎡)', '옥외자주식대수(대)', '옥외자주식면적(㎡)']]
pre_br_data1.columns
pre_br_data1.to_excel(path_pretreat+'//건축물대장//건축물대장_표제부.xlsx',index = False)
pre_br_data1 = pd.read_excel(path_pretreat+'//건축물대장//건축물대장_표제부.xlsx')
pre_br_data1.to_pickle(path_pretreat+'//건축물대장//건축물대장_표제부.pkl')
pre_br_data1

tot_jang = pd.read_excel(path_data_out + "//건축물대장_총괄표제부(2024.06)//총괄표제부_장안구.xlsx",skiprows=4)
tot_gwon = pd.read_excel(path_data_out + "//건축물대장_총괄표제부(2024.06)//총괄표제부_권선구.xlsx",skiprows=4)
tot_pal = pd.read_excel(path_data_out + "//건축물대장_총괄표제부(2024.06)//총괄표제부_팔달구.xlsx",skiprows=4)
tot_young = pd.read_excel(path_data_out + "//건축물대장_총괄표제부(2024.06)//총괄표제부_영통구.xlsx",skiprows=4)

tot_jang['시군구'] = '장안구'
tot_gwon['시군구'] = '권선구'
tot_pal['시군구'] = '팔달구'
tot_young['시군구'] = '영통구'

pre_tot_jang = tot_jang[['관리건축물대장PK','시군구','대지위치','건물명','주용도코드명','총주차수','옥내기계식대수(대)', '옥내기계식면적(㎡)', '옥외기계식대수(대)',
                 '옥외기계식면적(㎡)','옥내자주식대수(대)', '옥내자주식면적(㎡)', '옥외자주식대수(대)', '옥외자주식면적(㎡)']]

pre_tot_gwon = tot_gwon[['관리건축물대장PK','시군구','대지위치','건물명','주용도코드명','총주차수','옥내기계식대수(대)', '옥내기계식면적(㎡)', '옥외기계식대수(대)',
                 '옥외기계식면적(㎡)','옥내자주식대수(대)', '옥내자주식면적(㎡)', '옥외자주식대수(대)', '옥외자주식면적(㎡)']]

pre_tot_pal = tot_pal[['관리건축물대장PK','시군구','대지위치','건물명','주용도코드명','총주차수','옥내기계식대수(대)', '옥내기계식면적(㎡)', '옥외기계식대수(대)',
                 '옥외기계식면적(㎡)','옥내자주식대수(대)', '옥내자주식면적(㎡)', '옥외자주식대수(대)', '옥외자주식면적(㎡)']]

pre_tot_young = tot_young[['관리건축물대장PK','시군구','대지위치','건물명','주용도코드명','총주차수','옥내기계식대수(대)', '옥내기계식면적(㎡)', '옥외기계식대수(대)',
                 '옥외기계식면적(㎡)','옥내자주식대수(대)', '옥내자주식면적(㎡)', '옥외자주식대수(대)', '옥외자주식면적(㎡)']]

br_data_tot = pd.concat([pre_tot_jang,pre_tot_gwon,pre_tot_pal,pre_tot_young],axis=0).reset_index(drop=True)

pre_br_data2 = br_data_tot.groupby(['시군구','대지위치']).first().reset_index()
pre_br_data2.to_excel(path_pretreat+'//건축물대장//건축물대장_총괄표제부.xlsx',index = False)
#####################################################

dfa =  br_data.groupby(['대지위치']).first().reset_index()
dfb =  br_data_tot.groupby(['대지위치']).first().reset_index()

combined_df = pd.concat([dfa, dfb])
before_dedup_df = combined_df.copy()
result_df = combined_df.sort_values(by='총주차수', ascending=False).drop_duplicates(subset=['대지위치'])

#####################################################
combined_df = pd.concat([pre_br_data1, pre_br_data2])
# 중복 제거 전 데이터프레임
before_dedup_df = combined_df.copy()
# 중복 제거 (총주차수가 큰 값을 남기기 위해 sort_values와 drop_duplicates 사용)
result_df = combined_df.sort_values(by='총주차수', ascending=False).drop_duplicates(subset=['시군구', '대지위치','주용도코드명'])

df1 = result_df.iloc[:9000]  # 처음 9000행
df2 = result_df.iloc[9000:]  # 나머지 행

df1.to_excel(path_pretreat+'//건축물대장//건축물대장_주차장(지오코딩전_9000)_1.xlsx',index = False) #ㅈ지오코딩 전
df2.to_excel(path_pretreat+'//건축물대장//건축물대장_주차장(지오코딩전_1664)_2.xlsx',index = False) #ㅈ지오코딩 전
#중복제거된 행 확인
removed_rows_df = before_dedup_df[~before_dedup_df.index.isin(result_df.index)]

#지오코딩 후
common1 = pd.read_excel(path_middle+'//건축물대장//old//건축물대장주차장(지오코딩)_1_WGS84.xlsx')
common2 = pd.read_excel(path_middle+'//건축물대장//old//건축물대장주차장(지오코딩)_2_WGS84.xlsx')
parking3_re = pd.concat([common1,common2],axis=0).reset_index(drop=True)
parking3_re

parking3_re['geometry'] = parking3_re.apply(lambda row: Point(row['X'], row['Y']), axis=1)
result_df_shp_5179 = parking3_re[['시군구', '대지위치', '주용도코드명','총주차수','옥내기계식대수(대)', '옥내기계식면적(㎡)', '옥외기계식대수(대)','옥외기계식면적(㎡)', '옥내자주식대수(대)', '옥내자주식면적(㎡)', '옥외자주식대수(대)', '옥외자주식면적(㎡)','geometry']]
pre_filter = gpd.GeoDataFrame(result_df_shp_5179, geometry='geometry', crs='EPSG:4326')
pre_filter = pre_filter.to_crs(epsg=5179)
pre_filter['총주차수'].sum()
#result_df_shp_5179 = pre_filter.groupby([ '시군구', '대지위치', '건물명', '주용도코드명','geometry'])[['옥내기계식대수(대)', '옥내기계식면적(㎡)', '옥외기계식대수(대)','옥외기계식면적(㎡)', '옥내자주식대수(대)', '옥내자주식면적(㎡)', '옥외자주식대수(대)', '옥외자주식면적(㎡)']].sum().reset_index()
pd.set_option('display.max_columns', None)
pd.set_option('display.max_colwidth', None)
pre_filter[pre_filter['대지위치'] == '경기도 수원시 장안구 천천동 333번지']

#행정동명 매핑
parking3_result = gpd.sjoin(pre_filter,sgg_hjd, how='left', op='within')
parking3_result.rename(columns={'대지위치': '주소'}, inplace=True)
parking3_result = parking3_result[[ '시군구명', '행정동명','행정동코드','주소', '주용도코드명','총주차수', '옥내기계식대수(대)', '옥내기계식면적(㎡)', '옥외기계식대수(대)','옥외기계식면적(㎡)', '옥내자주식대수(대)', '옥내자주식면적(㎡)', '옥외자주식대수(대)', '옥외자주식면적(㎡)','geometry']]
parking3_result.isnull().sum() #널값 행 존재 ( 지오코딩 이상으로인하여 3개 행 수작업 진행)

#기초구역 번호 매핑
parking3_result = gpd.sjoin(parking3_result,base_cd_5179, how='left', op='within')
parking3_result = parking3_result[['시군구명', '행정동명','행정동코드','기초구역번호','주소','주용도코드명','총주차수', '옥내기계식대수(대)', '옥내기계식면적(㎡)', '옥외기계식대수(대)','옥외기계식면적(㎡)', '옥내자주식대수(대)', '옥내자주식면적(㎡)', '옥외자주식대수(대)', '옥외자주식면적(㎡)','geometry',]]
parking3_result[parking3_result.isna().any(axis=1)]
parking3_result.to_file(PATH_RESULT3+'//주차장//최종_건축물대장주차장.gpkg',driver='GPKG')
parking3_result.to_excel(path_result+'//주차장현황//최종_건축물대장주차장.xlsx',index=False)
parking3_result


# 검증
pre_br_data1 = pd.read_excel(path_pretreat+'//건축물대장//old//건축물대장_표제부.xlsx')
pre_br_data2 = pd.read_excel(path_pretreat+'//건축물대장//old//건축물대장_총괄표제부.xlsx')
result3 = pd.read_excel(path_result + '//주차장현황//최종_건축물대장주차장.xlsx')

pre_br_data1.to_pickle(path_middle + '//건축물대장//검증//건축물대장_표제부.pkl')
pre_br_data2.to_pickle(path_middle + '//건축물대장//검증//건축물대장_총괄표제부.pkl')
result3.to_pickle(path_middle + '//건축물대장//검증//최종_건축물대장주차장.pkl')

pre_br_data1 # 10138행
pre_br_data2 # 1143행

pre_br_data1['총주차수'].sum()
pre_br_data2['총주차수'].sum()
df_A = pre_br_data1[['시군구','대지위치', '주용도코드명', '옥내기계식대수(대)','옥외기계식대수(대)','옥내자주식대수(대)','옥외자주식대수(대)','총주차수']]
df_B = pre_br_data2[['시군구','대지위치', '주용도코드명', '옥내기계식대수(대)','옥외기계식대수(대)','옥내자주식대수(대)','옥외자주식대수(대)','총주차수']]

combined_df = pd.concat([pre_br_data1, pre_br_data2])
combined_df['총주차수'].sum()

before_dedup_df = combined_df.copy()
result_df1 = before_dedup_df.sort_values(by='총주차수', ascending=False).drop_duplicates(subset=['시군구','대지위치','건물명','주용도코드명'])#10357행
result_df1['총주차수'].sum() #604223

result_df2 = before_dedup_df.sort_values(by='총주차수', ascending=False).drop_duplicates(subset=['시군구','대지위치','주용도코드명'])#9808행
result_df2['총주차수'].sum() #563766

result_df3 = before_dedup_df.sort_values(by='총주차수', ascending=False).drop_duplicates(subset=['대지위치','건물명'])#9949행
result_df3['총주차수'].sum() #569559

result_df4 = before_dedup_df.sort_values(by='총주차수', ascending=False).drop_duplicates(subset=['대지위치']) #9237행
result_df4['총주차수'].sum() #526578


# 두 데이터프레임을 '대지위치주소'를 기준으로 병합
merged_df = pd.merge(df_A, df_B, on=['대지위치','주용도코드명'], suffixes=('_A', '_B'), how='outer')
# 각 컬럼의 값 중 더 큰 값을 선택
merged_df['옥내기계식대수'] = merged_df[['옥내기계식대수(대)_A', '옥내기계식대수(대)_B']].max(axis=1)
merged_df['옥외기계식대수'] = merged_df[['옥외기계식대수(대)_A', '옥외기계식대수(대)_B']].max(axis=1)
merged_df['옥내자주식대수'] = merged_df[['옥내자주식대수(대)_A', '옥내자주식대수(대)_B']].max(axis=1)
merged_df['옥외자주식대수'] = merged_df[['옥외자주식대수(대)_A', '옥외자주식대수(대)_B']].max(axis=1)

merged_df['총면수'] = merged_df[['옥내기계식대수', '옥외기계식대수', '옥내자주식대수', '옥외자주식대수']].sum(axis=1)
merged_df['총면수'].sum() #673060

# 두 데이터프레임을 '대지위치주소'를 기준으로 병합
merged_df = pd.merge(df_A, df_B, on=['대지위치'], suffixes=('_A', '_B'), how='outer')
# 각 컬럼의 값 중 더 큰 값을 선택
merged_df['옥내기계식대수'] = merged_df[['옥내기계식대수(대)_A', '옥내기계식대수(대)_B']].max(axis=1)
merged_df['옥외기계식대수'] = merged_df[['옥외기계식대수(대)_A', '옥외기계식대수(대)_B']].max(axis=1)
merged_df['옥내자주식대수'] = merged_df[['옥내자주식대수(대)_A', '옥내자주식대수(대)_B']].max(axis=1)
merged_df['옥외자주식대수'] = merged_df[['옥외자주식대수(대)_A', '옥외자주식대수(대)_B']].max(axis=1)

merged_df['총면수'] = merged_df[['옥내기계식대수', '옥외기계식대수', '옥내자주식대수', '옥외자주식대수']].sum(axis=1)
merged_df['총면수'].sum() #1,021,213



'''
###################################################################################################
## kt 유동인구데이터 - 최근한달
upop_2404 = pd.read_csv('F:\\24Project\\A28_수원시\\202404\\T1_GG_50CELL_FLOWPOP_202404_4111.csv') # 유동인구 데이터(2024.04)
###################################################################################################
# 전체 유동인구 값 계산
flow_c = upop_2404.columns
flow_list = flow_c[flow_c.str.contains('M_')|flow_c.str.contains('F_')]
upop_2404['flow_pop'] = upop_2404[flow_list].sum(axis=1)

# 위경도 기준 지오데이터프레임변환
flow_df_2  = upop_2404[['UTMK_X', 'UTMK_Y','flow_pop']]
flow_g = flow_df_2.groupby(['UTMK_X', 'UTMK_Y',],as_index=False).sum()
flow_geo = gpd.GeoDataFrame(flow_g,geometry = gpd.points_from_xy(flow_g['UTMK_X'],flow_g['UTMK_Y']),crs=5179)
flow_geo.to_file(path_data_analyze + '//유동인구//전체유동인구.shp',encoding='cp949')
# 유동인구 데이터 격자 매핑
flow_grid = gpd.sjoin(grid100_sw_5179,flow_geo)
flow_grid.drop_duplicates(subset='index_right',inplace=True)
flow_final_geo = gpd.GeoDataFrame(flow_grid,geometry='geometry')
flow_final_geo.to_file(path_data_analyze + '//유동인구//100m격자매핑//100m격자_유동인구.shp',encoding='cp949')

###################################################################################################
## kt 생활인구데이터 - 최근한달
spop_2404 = pd.read_csv('F:\\24Project\\A28_수원시\\202404\\T3_GG_50CELL_LIVEPOP_202404_4111.csv') # 생활인구 데이터(2024.04)
###################################################################################################
flow_s = spop_2404.columns
flow_list = flow_s[flow_s.str.contains('H_M')|flow_s.str.contains('H_F')|flow_s.str.contains('W_M')|flow_s.str.contains('W_F')|flow_s.str.contains('V_M')|flow_s.str.contains('V_F')]
spop_2404['flow_pop'] = spop_2404[flow_list].sum(axis=1)

flow_list_H = flow_s[flow_s.str.contains('H_M')|flow_s.str.contains('H_F')]
spop_2404['flow_pop_H'] = spop_2404[flow_list_H].sum(axis=1)

flow_list_W = flow_s[flow_s.str.contains('W_M')|flow_s.str.contains('W_F')]
spop_2404['flow_pop_W'] = spop_2404[flow_list_W].sum(axis=1)

flow_list_V = flow_s[flow_s.str.contains('V_M')|flow_s.str.contains('V_F')]
spop_2404['flow_pop_V'] = spop_2404[flow_list_V].sum(axis=1)


# 위경도 기준 지오데이터프레임변환
flow_df_2  = spop_2404[['UTMK_X', 'UTMK_Y','flow_pop_H','flow_pop_W','flow_pop_V','flow_pop']]
flow_g = flow_df_2.groupby(['UTMK_X', 'UTMK_Y',],as_index=False).sum()
flow_geo = gpd.GeoDataFrame(flow_g,geometry = gpd.points_from_xy(flow_g['UTMK_X'],flow_g['UTMK_Y']),crs=5179)
flow_geo.to_file(path_data_analyze + '//생활인구//전체생활인구.shp',encoding='cp949')
# 생활인구 데이터 격자 매핑
flow_grid = gpd.sjoin(grid100_sw_5179,flow_geo)
flow_grid.drop_duplicates(subset='index_right',inplace=True)
flow_final_geo = gpd.GeoDataFrame(flow_grid,geometry='geometry')
flow_final_geo.to_file(path_data_analyze + '//생활인구//100m격자매핑//100m격자_생활인구.shp',encoding='cp949')
'''


# 건축물대장 표제부 재수정
jang = pd.read_excel(path_data_in + "//2024-06-13//분석용 데이터//건축물대장 표제부_202404//1. 장안구.xlsx",skiprows=4)
gwon = pd.read_excel(path_data_in + "//2024-06-13//분석용 데이터//건축물대장 표제부_202404//2. 권선구.xlsx",skiprows=4)
pal = pd.read_excel(path_data_in + "//2024-06-13//분석용 데이터//건축물대장 표제부_202404//3. 팔달구.xlsx",skiprows=4)
young = pd.read_excel(path_data_in + "//2024-06-13//분석용 데이터//건축물대장 표제부_202404//4. 영통구.xlsx",skiprows=4)

jang['시군구'] = '장안구'
gwon['시군구'] = '권선구'
pal['시군구'] = '팔달구'
young['시군구'] = '영통구'

pre_jang = jang[['시군구','대지위치','건물명','주용도코드명','연면적(㎡)','옥내기계식대수(대)', '옥내기계식면적(㎡)', '옥외기계식대수(대)',
                 '옥외기계식면적(㎡)','옥내자주식대수(대)', '옥내자주식면적(㎡)', '옥외자주식대수(대)', '옥외자주식면적(㎡)']]

pre_gwon = gwon[['시군구','대지위치','건물명','주용도코드명','연면적(㎡)','옥내기계식대수(대)', '옥내기계식면적(㎡)', '옥외기계식대수(대)',
                 '옥외기계식면적(㎡)','옥내자주식대수(대)', '옥내자주식면적(㎡)', '옥외자주식대수(대)', '옥외자주식면적(㎡)']]

pre_pal = pal[['시군구','대지위치','건물명','주용도코드명','연면적(㎡)','옥내기계식대수(대)', '옥내기계식면적(㎡)', '옥외기계식대수(대)',
                 '옥외기계식면적(㎡)','옥내자주식대수(대)', '옥내자주식면적(㎡)', '옥외자주식대수(대)', '옥외자주식면적(㎡)']]

pre_young = young[['시군구','대지위치','건물명','주용도코드명','연면적(㎡)','옥내기계식대수(대)', '옥내기계식면적(㎡)', '옥외기계식대수(대)',
                 '옥외기계식면적(㎡)','옥내자주식대수(대)', '옥내자주식면적(㎡)', '옥외자주식대수(대)', '옥외자주식면적(㎡)']]

br_data = pd.concat([pre_jang,pre_gwon,pre_pal,pre_young],axis=0).reset_index(drop=True)

pre_br_data1 = br_data.drop_duplicates(subset='대지위치')


#기존 최종pkl 가져와서 주소만 매핑
old_pkl = pd.read_pickle(path_middle + '//건축물대장//old//검증//최종_건축물대장주차장.pkl')
old_pkl= old_pkl.drop_duplicates(subset='주소')
old_pkl_geo = old_pkl[['주소','geometry']]
old_pkl_geo.rename(columns={'주소':'대지위치'},inplace=True)

pre_br_data1_geo = pd.merge(pre_br_data1,old_pkl_geo,on='대지위치',how='left')
pre_br_data1_geo_notnull = pre_br_data1_geo[pre_br_data1_geo['geometry'].notna()]

pre_br_data1_geo_null = pre_br_data1_geo[pre_br_data1_geo['geometry'].isna()]
pre_br_data1_geo_null # 40781행

chunk_size = 9999
num_chunks = (len(pre_br_data1_geo_null) // chunk_size) + 1

for i in range(num_chunks):
    start = i * chunk_size
    end = min((i + 1) * chunk_size, len(pre_br_data1_geo_null))
    chunk = pre_br_data1_geo_null.iloc[start:end]
    chunk.to_excel(path_data_analyze + f'//건축물대장//지오코딩필요//data_chunk_{i + 1}.xlsx', index=False)

#지오코딩 후
data1 = pd.read_excel(path_data_analyze + '//건축물대장//지오코딩후_0827//data_chunk_1.xlsx')
data2 = pd.read_csv(path_data_analyze + '//건축물대장//지오코딩후_0827//data_chunk_2.csv',encoding='cp949')
data3 = pd.read_excel(path_data_analyze + '//건축물대장//지오코딩후_0827//data_chunk_3.xlsx')
data4 = pd.read_csv(path_data_analyze + '//건축물대장//지오코딩후_0827//data_chunk_4.csv',encoding='cp949')
data5 = pd.read_excel(path_data_analyze + '//건축물대장//지오코딩후_0827//data_chunk_5.xlsx')

pre_br_data1_geo_2 = pd.concat([data1,data2,data3,data4,data5],axis=0).reset_index(drop=True)
pre_br_data1_geo_2 = pre_br_data1_geo_2[['시군구', '대지위치', '건물명', '주용도코드명', '옥내기계식대수(대)', '옥내기계식면적(㎡)',
       '옥외기계식대수(대)', '옥외기계식면적(㎡)', '옥내자주식대수(대)', '옥내자주식면적(㎡)', '옥외자주식대수(대)',
       '옥외자주식면적(㎡)', 'geometry',  'X', 'Y']]
pre_br_data1_geo_2['geometry'] = pre_br_data1_geo_2.apply(lambda row: Point(row['X'], row['Y']), axis=1)
pre_br_data1_geo_2 = gpd.GeoDataFrame(pre_br_data1_geo_2, geometry='geometry',crs='epsg:4326')
pre_br_data1_geo_2 = pre_br_data1_geo_2.to_crs(epsg=5179)
pre_br_data1_geo_2
pre_br_data1_geo_3 = pre_br_data1_geo_2[['시군구', '대지위치', '건물명', '주용도코드명', '옥내기계식대수(대)', '옥내기계식면적(㎡)',
       '옥외기계식대수(대)', '옥외기계식면적(㎡)', '옥내자주식대수(대)', '옥내자주식면적(㎡)', '옥외자주식대수(대)',
       '옥외자주식면적(㎡)', 'geometry']]

pre_br_data1_geo_notnull['geometry'] = pre_br_data1_geo_notnull['geometry'].apply(wkt.loads)
pre_br_data1_geo_notnull = gpd.GeoDataFrame(pre_br_data1_geo_notnull, geometry='geometry',crs='epsg:5179')
pre_br_data1_geo_notnull = pre_br_data1_geo_notnull.to_crs(epsg=5179)

result_brdata = pd.concat([pre_br_data1_geo_notnull,pre_br_data1_geo_3],axis=0).reset_index(drop=True)
result_brdata['총주차수'] = result_brdata[['옥내기계식대수(대)','옥외기계식대수(대)','옥내자주식대수(대)','옥외자주식대수(대)']].sum(axis=1)
result_brdata = result_brdata[['시군구', '대지위치', '건물명', '주용도코드명', '총주차수','옥내기계식대수(대)', '옥내기계식면적(㎡)',
       '옥외기계식대수(대)', '옥외기계식면적(㎡)', '옥내자주식대수(대)', '옥내자주식면적(㎡)', '옥외자주식대수(대)',
       '옥외자주식면적(㎡)', 'geometry']]



#행정동명 매핑
result_brdata2 = gpd.sjoin(result_brdata,sgg_hjd, how='left', op='within')
result_brdata2.rename(columns={'대지위치': '주소'}, inplace=True)
result_brdata2 = result_brdata2[[ '시군구명', '행정동명','행정동코드','주소','건물명', '주용도코드명','총주차수', '옥내기계식대수(대)', '옥내기계식면적(㎡)', '옥외기계식대수(대)','옥외기계식면적(㎡)', '옥내자주식대수(대)', '옥내자주식면적(㎡)', '옥외자주식대수(대)', '옥외자주식면적(㎡)','geometry']]
result_brdata2.isnull().sum() #널값 행 존재 ( 지오코딩 이상으로인하여 3개 행 수작업 진행)

#기초구역 번호 매핑
result_brdata3 = gpd.sjoin(result_brdata2,base_cd_5179, how='left', op='within')
result_brdata3 = result_brdata3[['시군구명', '행정동명','행정동코드','기초구역번호','주소','건물명','주용도코드명','총주차수', '옥내기계식대수(대)', '옥내기계식면적(㎡)', '옥외기계식대수(대)','옥외기계식면적(㎡)', '옥내자주식대수(대)', '옥내자주식면적(㎡)', '옥외자주식대수(대)', '옥외자주식면적(㎡)','geometry',]]
result_brdata3[result_brdata3.isna().any(axis=1)]
result_brdata3.to_excel(path_result+'//주차장현황//건축물대장_표제부_0827.xlsx',index=False)
result_brdata3.to_pickle(path_middle+'//건축물대장//건축물대장_표제부0827.pkl')

#주소데이터 생성
add = result_brdata3[['시군구명', '행정동명', '행정동코드', '기초구역번호', '주소','geometry']]
add = add.drop_duplicates()
# 총괄표제부 재수정
tot_jang = pd.read_excel(path_data_out + "//건축물대장_총괄표제부(2024.06)//총괄표제부_장안구.xlsx",skiprows=4)
tot_gwon = pd.read_excel(path_data_out + "//건축물대장_총괄표제부(2024.06)//총괄표제부_권선구.xlsx",skiprows=4)
tot_pal = pd.read_excel(path_data_out + "//건축물대장_총괄표제부(2024.06)//총괄표제부_팔달구.xlsx",skiprows=4)
tot_young = pd.read_excel(path_data_out + "//건축물대장_총괄표제부(2024.06)//총괄표제부_영통구.xlsx",skiprows=4)

tot_jang['시군구'] = '장안구'
tot_gwon['시군구'] = '권선구'
tot_pal['시군구'] = '팔달구'
tot_young['시군구'] = '영통구'

pre_tot_jang = tot_jang[['시군구','대지위치','건물명','주용도코드명','총주차수','옥내기계식대수(대)', '옥내기계식면적(㎡)', '옥외기계식대수(대)',
                 '옥외기계식면적(㎡)','옥내자주식대수(대)', '옥내자주식면적(㎡)', '옥외자주식대수(대)', '옥외자주식면적(㎡)']]

pre_tot_gwon = tot_gwon[['시군구','대지위치','건물명','주용도코드명','총주차수','옥내기계식대수(대)', '옥내기계식면적(㎡)', '옥외기계식대수(대)',
                 '옥외기계식면적(㎡)','옥내자주식대수(대)', '옥내자주식면적(㎡)', '옥외자주식대수(대)', '옥외자주식면적(㎡)']]

pre_tot_pal = tot_pal[['시군구','대지위치','건물명','주용도코드명','총주차수','옥내기계식대수(대)', '옥내기계식면적(㎡)', '옥외기계식대수(대)',
                 '옥외기계식면적(㎡)','옥내자주식대수(대)', '옥내자주식면적(㎡)', '옥외자주식대수(대)', '옥외자주식면적(㎡)']]

pre_tot_young = tot_young[['시군구','대지위치','건물명','주용도코드명','총주차수','옥내기계식대수(대)', '옥내기계식면적(㎡)', '옥외기계식대수(대)',
                 '옥외기계식면적(㎡)','옥내자주식대수(대)', '옥내자주식면적(㎡)', '옥외자주식대수(대)', '옥외자주식면적(㎡)']]

br_data_tot = pd.concat([pre_tot_jang,pre_tot_gwon,pre_tot_pal,pre_tot_young],axis=0).reset_index(drop=True)
br_data_tot_1 = br_data_tot.drop_duplicates(subset='대지위치')
br_data_tot_1.rename(columns={'대지위치': '주소'}, inplace=True)

br_data_tot_1_geo = pd.merge(br_data_tot_1,add,on='주소',how='left')
br_data_tot_1_geonotnull = br_data_tot_1_geo[br_data_tot_1_geo['geometry'].notna()]

br_data_tot_1_geo_null = br_data_tot_1_geo[br_data_tot_1_geo['geometry'].isna()]
br_data_tot_1_geo_null.to_excel(path_data_analyze + f'//건축물대장//지오코딩필요//data_chunk_총괄.xlsx',index=False)


#지오코딩 후
br_data_tot_1_geocoding = pd.read_excel(path_data_analyze + '//건축물대장//지오코딩후_0827//data_chunk_총괄.xlsx')
br_data_tot_1_geocoding2 = br_data_tot_1_geocoding[['시군구', '주소', '건물명', '주용도코드명', '옥내기계식대수(대)', '옥내기계식면적(㎡)',
       '옥외기계식대수(대)', '옥외기계식면적(㎡)', '옥내자주식대수(대)', '옥내자주식면적(㎡)', '옥외자주식대수(대)',
       '옥외자주식면적(㎡)', 'geometry',  'X', 'Y']]
br_data_tot_1_geocoding2['geometry'] = br_data_tot_1_geocoding2.apply(lambda row: Point(row['X'], row['Y']), axis=1)
pre_br_data2_geo_1 = gpd.GeoDataFrame(br_data_tot_1_geocoding2, geometry='geometry',crs='epsg:4326')
pre_br_data2_geo_1 = pre_br_data2_geo_1.to_crs(epsg=5179)
pre_br_data2_geo_2 = pre_br_data2_geo_1[['시군구', '주소', '건물명', '주용도코드명', '옥내기계식대수(대)', '옥내기계식면적(㎡)',
       '옥외기계식대수(대)', '옥외기계식면적(㎡)', '옥내자주식대수(대)', '옥내자주식면적(㎡)', '옥외자주식대수(대)',
       '옥외자주식면적(㎡)', 'geometry']]

result_brdata2 = pd.concat([br_data_tot_1_geonotnull,pre_br_data2_geo_2],axis=0).reset_index(drop=True)
result_brdata2['총주차수'] = result_brdata2[['옥내기계식대수(대)','옥외기계식대수(대)','옥내자주식대수(대)','옥외자주식대수(대)']].sum(axis=1)
result_brdata2 = result_brdata2[['시군구', '주소', '건물명', '주용도코드명', '총주차수','옥내기계식대수(대)', '옥내기계식면적(㎡)',
       '옥외기계식대수(대)', '옥외기계식면적(㎡)', '옥내자주식대수(대)', '옥내자주식면적(㎡)', '옥외자주식대수(대)',
       '옥외자주식면적(㎡)', 'geometry']]

result_brdata3 = gpd.GeoDataFrame(result_brdata2, geometry='geometry',crs='epsg:5179')
result_brdata3 = result_brdata3.to_crs(epsg=5179)
result_brdata3.info()
#행정동명 매핑
result_brdata3_hjd = gpd.sjoin(result_brdata3,sgg_hjd, how='left', op='within')
result_brdata3_hjd = result_brdata3_hjd[[ '시군구명', '행정동명','행정동코드','주소','건물명',  '주용도코드명','총주차수', '옥내기계식대수(대)', '옥내기계식면적(㎡)', '옥외기계식대수(대)','옥외기계식면적(㎡)', '옥내자주식대수(대)', '옥내자주식면적(㎡)', '옥외자주식대수(대)', '옥외자주식면적(㎡)','geometry']]
result_brdata3_hjd.isnull().sum() #널값 행 존재 ( 지오코딩 이상으로인하여 3개 행 수작업 진행)

#기초구역 번호 매핑
result_brdata_total = gpd.sjoin(result_brdata3_hjd,base_cd_5179, how='left', op='within')
result_brdata_total = result_brdata_total[['시군구명', '행정동명','행정동코드','기초구역번호','주소','건물명', '주용도코드명','총주차수', '옥내기계식대수(대)', '옥내기계식면적(㎡)', '옥외기계식대수(대)','옥외기계식면적(㎡)', '옥내자주식대수(대)', '옥내자주식면적(㎡)', '옥외자주식대수(대)', '옥외자주식면적(㎡)','geometry',]]
result_brdata_total[result_brdata_total.isna().any(axis=1)]

result_brdata_total.to_excel(path_result+'//주차장현황//건축물대장_총괄표제부_0827.xlsx',index=False)
result_brdata_total.to_pickle(path_middle+'//건축물대장//건축물대장_총괄표제부_0827.pkl')

# 건축물대장표제부_총괄표제부 합치기
ar_parking = pd.read_pickle(path_middle+'//건축물대장//건축물대장_표제부0827.pkl') #50815
total_ar_parking = pd.read_pickle(path_middle+'//건축물대장//건축물대장_총괄표제부_0827.pkl') #총괄표제부 2280
ar_parking

combined_df = pd.concat([ar_parking, total_ar_parking],axis=0).reset_index(drop=True) #53095
before_dedup_df = combined_df.copy()
# 중복 제거 (총주차수가 큰 값을 남기기 위해 sort_values와 drop_duplicates 사용)
result_df = combined_df.sort_values(by='총주차수', ascending=False).drop_duplicates(subset=['시군구명', '주소']) #50852
result_df.to_excel(path_result+'//주차장현황//최종건축물대장주차장_0827.xlsx',index=False)
result_df.to_pickle(path_middle+'//건축물대장//최종건축물대장주차장_0827.pkl')


########################################################################################################################
# (동료 작성 구간 제거) 총괄표제부·표제부 중복 규칙으로 최종 주차장수(parking_cnt)를 산출하는 코드 — 비공개

# 건축물대장_표제부_0827에 연면적 붙이기 -(동료) 요청
docu_unit = pd.read_pickle(path_middle+'//건축물대장//건축물대장_표제부0827.pkl')
pre_br_data1.rename(columns={'대지위치':'주소','시군구':'시군구명'},inplace=True)
pre_br_data1_1 = pre_br_data1[['시군구명','주소','연면적(㎡)']]
pre_br_data1_1

docu_unit2 = pd.merge(docu_unit,pre_br_data1_1,on=['시군구명','주소'],how='left')
docu_unit2 = docu_unit2[['시군구명', '행정동명', '행정동코드', '기초구역번호', '주소', '연면적(㎡)', '건물명', '주용도코드명', '총주차수',
       '옥내기계식대수(대)', '옥내기계식면적(㎡)', '옥외기계식대수(대)', '옥외기계식면적(㎡)', '옥내자주식대수(대)',
       '옥내자주식면적(㎡)', '옥외자주식대수(대)', '옥외자주식면적(㎡)', 'geometry']]

docu_unit2.to_pickle(path_middle+'//건축물대장//건축물대장_표제부_0827(연면적).pkl')

# 건축물대장_표제부_0827에 연면적 붙이기 -(동료) 요청
base_hjd = gpd.read_file(PATH_RESULT3 + '//경계면데이터//기초구역경계//기초구역경계(시군구,행정동매핑).gpkg',driver='GPKG')
base_hjd.columns
base_hjd = base_hjd[['HJD_NM','기초구역번호']]
base_hjd.to_pickle(path_middle+'//기초구역경계//기초구역경계_행정동.pkl')
#parking_cnt 결과를 바탕으로 공급량 수정작업 진행해야함

#최종건축물대장 주차장 저장
parking4 = pd.read_pickle(path_middle+'//건축물대장//최종건축물대장주차장_0827.pkl')
#pre_filter = gpd.GeoDataFrame(parking4, geometry='geometry', crs='EPSG:4326')
#pre_filter = pre_filter.to_crs(epsg=5179)
#pre_filter['총주차수'].sum()
parking4.to_file(PATH_RESULT3+'//주차장//최종_건축물대장주차장.gpkg',driver='GPKG')
parking4.to_excel(path_result+'//주차장현황//최종_건축물대장주차장.xlsx',index=False)







