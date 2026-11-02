###########################################################
# 과 제 명: A34_세종시_정주인구분석
# 파 일 명: 1.데이터전처리
# 작 성 자: 김민서
###########################################################

import os, importlib, warnings;
warnings.filterwarnings(action='ignore')
# DB 접속: 사내 모듈 사용 (비공개)  # 원본: from config import config_A34 as config;
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
fl.f_log_line("1.데이터전처리.py")
###########################################################
# 모 듈 명: 모 듈 명 - 1.데이터전처리.py
# 파 일 명: 1.데이터전처리.py
# 작 성 자: 김민서
# 설    명: 세종시 정주인구 분석
# 파일 버전: v1.0 [2024.04.01]
# 작성 일자: 2024.04.03
# 수정 일자: 2024.04.25 00:00
###########################################################
# 1.실행 변수 정의
log.info("1.실행 변수 정의")

path_data_out = os.path.join(config_info["PATH_DATA_COLLECT"], "01.외부")
path_data_in = os.path.join(config_info["PATH_DATA_COLLECT"], "02.내부")
path_data_analyze = os.path.join(config_info["PATH_DATA_ANALYZE"])
path_data_output = os.path.join(config_info["PATH_DATA_OUTPUT"])
path_base = "2024-06-25"
path_database = os.path.join(config_info["PATH_DATA_OUTPUT_DATEBASE"], path_base)
path_pretreat = os.path.join(config_info["PATH_DATA_OUTPUT_PRETREAT"], path_base)
path_middle = os.path.join(config_info["PATH_DATA_OUTPUT_MIDDLE"], path_base)
path_result = os.path.join(config_info["PATH_DATA_OUTPUT_RESULT"], path_base)
# 1.1.SQLite 저장시 사용됨
##name_database = f"DB_{config_info['과제ID']}_202309.db" #
# ==================================================================================================

# 필요라이브러리
import pandas as pd
import geopandas as gpd
import warnings
warnings.filterwarnings("ignore")

house = gpd.read_file(path_data_in + "//2024-05-30//세종시 북부권 산업단지 정주여건 개선 과제 수행관련 데이터 제공//건축물대장_geocoding//건축물대장 현황자료('24.4.shp",encoding='cp949')
Industrial_point = gpd.read_file(path_data_in + "//2024-05-30//세종시 북부권 산업단지 정주여건 개선 과제 수행관련 데이터 제공//세종시 산업단지 위치_geocoding//세종시 산업단지 정보 현황자료_24.shp",encoding='cp949')
#국토부제공 세종시 국가관심지점 데이터
poi_sejong = gpd.read_file(path_data_out + "//국가관심지점//DownloadMap(20240618)//SEJONG_POI//TN_POI//TN_POI_세종특별자치시.shp")
poi_chungnam = gpd.read_file(path_data_out + "//국가관심지점//CHUNGNAM_POI//TN_POI//TN_POI_충청남도.shp")
poi_chungbuk = gpd.read_file(path_data_out + "//국가관심지점//CHUNGBUK_POI//TN_POI//TN_POI_충청북도.shp")
poi = pd.concat([poi_sejong, poi_chungnam, poi_chungbuk], ignore_index=True)
code = pd.read_csv(path_data_out + "//국가관심지점//DownloadMap(20240618)//FOMAT//TN_ASORTCL_v1.csv")


code = code.rename(columns = {'실제입력코드' : 'POI_CL_DC'})
code = code.reset_index()
code = code[['대분류', '중분류', '소분류', '세분류', '세세분류','POI_CL_DC']]
code['POI_CL_DC'] = code['POI_CL_DC'].astype('int64')
poi['POI_CL_DC'] = poi['POI_CL_DC'].astype('int64')
poi2 = pd.merge(poi,code, on='POI_CL_DC')
poi2 = poi2[['대분류', '중분류', '소분류','세분류', '세세분류','POI_NM','POI_CL_DC','geometry']]
poi2.to_csv(path_data_out + "//국가관심지점//DownloadMap(20240618)//SEJONG_POI//TN_POI//poi_0712.csv",index=False)

house.head()
house.columns
#주거
poi_housing = house[['도로명주소','(층)주용도','연면적','건물명','geometry']]
poi_housing['중분류'] = '주거시설'
poi_housing = poi_housing[['중분류','(층)주용도','연면적','건물명','geometry']]
poi_housing.columns = ['중분류','소분류','연면적','POI_NM','geometry']
poi_housing = poi_housing.drop_duplicates()
poi_housing = gpd.GeoDataFrame(poi_housing, geometry='geometry', crs='EPSG:4326')
poi_housing = poi_housing.to_crs(epsg=5179)
poi_housing

#의료
poi_medical = poi2[poi2['소분류'].isin(['병원','의원','종합병원'])]
poi_medical['중분류'] = '의료시설'
poi_medical = poi_medical[['중분류','소분류','POI_NM','geometry']]
poi_medical = poi_medical.drop_duplicates()
poi_medical.head()

#교통
poi_trans = poi2[poi2['세분류'].isin(['버스터미널/정류장','고속철도','보통철도','철도/지하철'])]
poi_trans['중분류'] = '교통시설'
poi_trans = poi_trans[['중분류','세분류','POI_NM','geometry']]
poi_trans.columns = ['중분류','소분류','POI_NM','geometry']
poi_trans = poi_trans.drop_duplicates()
poi_trans.head()

#공원
poi_park = poi2[poi2['세분류'].isin(['근린공원','어린이공원','소공원'])]
poi_park['중분류'] = '공원시설'
poi_park = poi_park[['중분류','세분류','POI_NM','geometry']]
poi_park.columns = ['중분류','소분류','POI_NM','geometry']
poi_park = poi_park.drop_duplicates()
poi_park.head()


#보육
poi_child = poi2[poi2['세세분류'].isin(['국공립어린이집','민간어린이집','법인/단체등어린이집','사회복지법인어린이집','직장어린이집'])]
poi_child['중분류'] = '보육시설'
poi_child = poi_child[['중분류','세세분류','POI_NM','geometry']]
poi_child.columns = ['중분류','소분류','POI_NM','geometry']
poi_child = poi_child.drop_duplicates()
poi_child.head()

#교육
poi_edu = poi2[poi2['세세분류'].isin(['초등학교','중학교','고등학교'])]
poi_edu['중분류'] = '교육시설'
poi_edu = poi_edu[['중분류','세세분류','POI_NM','geometry']]
poi_edu.columns = ['중분류','소분류','POI_NM','geometry']
poi_edu = poi_edu.drop_duplicates()
poi_edu.head()


#복지
poi_welf = poi2[poi2['세분류'].isin(['기타거주복지시설운영업','노인거주복지시설운영업','노인양로복지시설운영업','심신장애인거주복지시설운영업'])]
poi_welf['중분류'] = '복지시설'
poi_welf = poi_welf[['중분류','세분류','POI_NM','geometry']]
poi_welf.columns = ['중분류','소분류','POI_NM','geometry']
poi_welf = poi_welf.drop_duplicates()
poi_welf.head()

#상업/금융
poi_com = poi2[(poi2['세분류'].isin(['체인화편의점','슈퍼마켓','백화점'])) | (poi2['소분류'].isin(['은행및저축기관']))]
poi_com['중분류'] = '상업/금융시설'
poi_com = poi_com[['중분류','세분류','POI_NM','geometry']]
poi_com.columns = ['중분류','소분류','POI_NM','geometry']
poi_com = poi_com.drop_duplicates()
poi_com.head()

#문화/체육
poi_cul = poi2[(poi2['소분류'].isin(['공공도서관'])) | (poi2['세분류'].isin(['커피전문점','영화및비디오물상영업','기타스포츠시설운영업']))]
poi_cul['중분류'] = '문화/체육시설'
poi_cul = poi_cul[['중분류','세분류','POI_NM','geometry']]
poi_cul.columns = ['중분류','소분류','POI_NM','geometry']
poi_cul = poi_cul.drop_duplicates()
poi_cul.head()

#주거,의료,교통,공원,보육,교육,복지,상업/금융,문화/체육 데이터 합치기
poi_sejong = pd.concat([poi_housing,poi_medical,poi_trans,poi_park,poi_child,poi_edu,poi_welf,poi_com,poi_cul],axis=0)
poi_sejong


#세종시 시군구경계,행정동경계 추출
SGG = gpd.read_file(path_data_out + "//시군구경계//BND_SIGUNGU_PG/BND_SIGUNGU_PG.shp",encoding='cp949')
hjd = gpd.read_file(path_data_out + "//행정동경계//BND_ADM_DONG_PG/BND_ADM_DONG_PG.shp",encoding='cp949')
SGG_sejong = SGG[SGG['SIGUNGU_CD'] == '29010']
HJD_sejong = hjd[hjd['ADM_CD'].str.startswith('29010')]
SGG_sejong.to_file(path_data_analyze + '//시군구경계//sgg_sejong.gpkg',driver='GPKG')
HJD_sejong.to_file(path_data_analyze + '//행정동경계//hjd_sejong.gpkg',driver='GPKG')

poi_sejong = gpd.GeoDataFrame(poi_sejong, geometry='geometry')
HJD_sejong = gpd.GeoDataFrame(HJD_sejong, geometry='geometry')
HJD_sejong = HJD_sejong.to_crs(poi_sejong.crs)



poi_sejong_hjd = gpd.sjoin(poi_sejong, HJD_sejong[['ADM_NM','geometry']], how='left',op='within')
poi_sejong_hjd = poi_sejong_hjd[['중분류','소분류', 'ADM_NM', 'POI_NM', 'geometry']]
# 공공도서관으로 합치기
poi_sejong_hjd.loc[(poi_sejong_hjd['중분류'] == '문화/체육시설') & (poi_sejong_hjd['소분류'].isin(['공공전문도서관', '공공작은도서관'])), '소분류'] = '공공도서관'
# 은행/저축기관 합치기
poi_sejong_hjd.loc[(poi_sejong_hjd['중분류'] == '상업/금융시설') & (poi_sejong_hjd['소분류'].isin(['일반은행', '신용조합및저축기관'])), '소분류'] = '은행·저축기관'

poi_sejong_hjd.to_excel(path_pretreat + '//세종시_시설v2//point_sejoing_0712.xlsx',index=False)
poi_sejong_hjd.to_file(path_pretreat + '//세종시_시설v2//point_sejoing_0712.gpkg',driver='GPKG')

#산업단지 위치 좌표계 재정의
Industrial_point = gpd.GeoDataFrame(Industrial_point, geometry='geometry', crs="EPSG:4326")
Industrial_point = Industrial_point.to_crs(epsg='5179')
Industrial_point_1 = Industrial_point[Industrial_point['연번'] == '1']
Industrial_point_2 = Industrial_point[Industrial_point['연번'] == '2']
Industrial_point_3 = Industrial_point[Industrial_point['연번'] == '3']
Industrial_point_4 = Industrial_point[Industrial_point['연번'] == '4']
Industrial_point_5 = Industrial_point[Industrial_point['연번'] == '5']
Industrial_point_6 = Industrial_point[Industrial_point['연번'] == '6']
Industrial_point.to_file(path_pretreat + '//산업단지위치.gpkg',driver='GPKG')
path_pretreat = os.path.join(config_info["PATH_DATA_OUTPUT_PRETREAT"], '2024-07-01')
Industrial_point_1.to_file(path_pretreat + '//산업단지별_bf//전의12일반//산업단지위치_전의12일반.gpkg',driver='GPKG')
Industrial_point_2.to_file(path_pretreat + '//산업단지별_bf//소정일반//산업단지위치_소정일반.gpkg',driver='GPKG')
Industrial_point_3.to_file(path_pretreat + '//산업단지별_bf//첨단일반//산업단지위치_첨단일반.gpkg',driver='GPKG')
Industrial_point_4.to_file(path_pretreat + '//산업단지별_bf//미래일반//산업단지위치_미래일반.gpkg',driver='GPKG')
Industrial_point_5.to_file(path_pretreat + '//산업단지별_bf//노장농공//산업단지위치_노장농공.gpkg',driver='GPKG')
Industrial_point_6.to_file(path_pretreat + '//산업단지별_bf//청송농공//산업단지위치_청송농공.gpkg',driver='GPKG')


#
#
