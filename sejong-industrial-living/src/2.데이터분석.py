###########################################################
# 과 제 명: A34_세종시_정주인구분석
# 파 일 명: 2.데이터분석
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
path_pretreat = os.path.join(config_info["PATH_DATA_OUTPUT_PRETREAT"],path_base)
path_middle = os.path.join(config_info["PATH_DATA_OUTPUT_MIDDLE"], path_base)
path_result = os.path.join(config_info["PATH_DATA_OUTPUT_RESULT"], '2024-07-01')
# 1.1.SQLite 저장시 사용됨
##name_database = f"DB_{config_info['과제ID']}_202309.db" #
# ==================================================================================================

# 필요라이브러리
import pandas as pd
from shapely.geometry import Polygon, mapping, shape, Point
import geopandas as gpd
import warnings
from sklearn.preprocessing import MinMaxScaler
warnings.filterwarnings("ignore")

Industrial_point = gpd.read_file(path_data_in + "//2024-05-30//세종시 북부권 산업단지 정주여건 개선 과제 수행관련 데이터 제공//세종시 산업단지 위치_geocoding//세종시 산업단지 정보 현황자료_24.shp",encoding='cp949')
poi_sejong_hjd = gpd.read_file(path_pretreat + '//세종시_시설v2//point_sejoing_0712.gpkg',driver='GPKG')
SGG_sejong = gpd.read_file(path_data_analyze + '//시군구경계//sgg_sejong.gpkg',driver='GPKG')
HJD_sejong = gpd.read_file(path_data_analyze + '//행정동경계//hjd_sejong.gpkg',driver='GPKG')
house = gpd.read_file(path_data_in + "//2024-05-30//세종시 북부권 산업단지 정주여건 개선 과제 수행관련 데이터 제공//건축물대장_geocoding//건축물대장 현황자료('24.4.shp",encoding='cp949')
# 산업단지위치기준 버퍼생성 700m,2km,5km (QGIS에서 생성함)
path_pretreat = os.path.join(config_info["PATH_DATA_OUTPUT_PRETREAT"], '2024-07-01')
BF_700 = gpd.read_file(path_pretreat + '//700M_buffer//700_BF.gpkg',driver='GPKG')
BF_2000 = gpd.read_file(path_pretreat + '//2KM_buffer//2000_BF.gpkg',driver='GPKG')
BF_5000 = gpd.read_file(path_pretreat + '//5KM_buffer//5000_BF.gpkg',driver='GPKG')

#기준데이터 생성
name = Industrial_point[['산업단지명']]
standard = poi_sejong_hjd[['중분류', '소분류']].drop_duplicates().reset_index(drop=True)
standard = name.merge(standard, how='cross')
standard


#주거 공급량 분석
#주거시설
poi_housing = house[['도로명주소','(층)주용도','연면적','건물명','geometry']]
poi_housing['중분류'] = '주거시설'
poi_housing = poi_housing[['중분류','(층)주용도','연면적','건물명','geometry']]
poi_housing.columns = ['중분류','소분류','연면적','POI_NM','geometry']
poi_housing = poi_housing.drop_duplicates()
poi_housing = gpd.GeoDataFrame(poi_housing, geometry='geometry', crs='EPSG:4326')
poi_housing = poi_housing.to_crs(epsg=5179)
poi_housing['연면적'] = poi_housing['연면적'].astype(float)
point_col1 = poi_housing
def perform_spatial_join_house(buffer_gdf, facilities_gdf, buffer_name):
    joined_gdf = gpd.sjoin(facilities_gdf, buffer_gdf, how="inner", op='within')
    print(f"시설들이 {buffer_name} 내에 포함된 산업단지:")
    print(joined_gdf[['중분류', '소분류', '연면적', '연번', '분류','산업단지명', 'distance']])
    return joined_gdf

facilities_in_700m_buffer = perform_spatial_join_house(BF_700, point_col1, '700m 버퍼')
facilities_in_2000m_buffer = perform_spatial_join_house(BF_2000, point_col1, '2000m 버퍼')
facilities_in_5000m_buffer = perform_spatial_join_house(BF_5000, point_col1, '5000m 버퍼')
grouped_700m = facilities_in_700m_buffer.groupby(['산업단지명', '중분류', '소분류'])['연면적'].sum().reset_index(name='반경700m')
grouped_2000m = facilities_in_2000m_buffer.groupby(['산업단지명', '중분류', '소분류'])['연면적'].sum().reset_index(name='반경2km')
grouped_5000m = facilities_in_5000m_buffer.groupby(['산업단지명', '중분류', '소분류'])['연면적'].sum().reset_index(name='반경5km')

merged_df = pd.merge(grouped_700m, grouped_2000m, on=['산업단지명', '중분류', '소분류'], how='outer')
supply1 = pd.merge(merged_df, grouped_5000m, on=['산업단지명', '중분류', '소분류'], how='outer')
supply1 = pd.merge(standard,supply1,on=['산업단지명','중분류','소분류'],how='left')
supply1.fillna(0, inplace=True)
supply1



# 주거시설 이외 공급량 분석
point_col2 = poi_sejong_hjd[poi_sejong_hjd['중분류'] != '주거시설']
point = point_col2[['중분류', '소분류', 'ADM_NM', 'geometry']]
# 버퍼와 시설 목록 간의 공간 조인 수행
def perform_spatial_join(buffer_gdf, facilities_gdf, buffer_name):
    joined_gdf = gpd.sjoin(facilities_gdf, buffer_gdf, how="inner", op='within')
    print(f"시설들이 {buffer_name} 내에 포함된 산업단지:")
    print(joined_gdf[['중분류', '소분류', 'ADM_NM', '연번', '분류','산업단지명', 'distance']])
    return joined_gdf

# 각 버퍼에 대해 공간 조인 수행
facilities_in_700m_buffer = perform_spatial_join(BF_700, point, '700m 버퍼')
facilities_in_2000m_buffer = perform_spatial_join(BF_2000, point, '2000m 버퍼')
facilities_in_5000m_buffer = perform_spatial_join(BF_5000, point, '5000m 버퍼')

grouped_700m = facilities_in_700m_buffer.groupby(['산업단지명', '중분류', '소분류']).size().reset_index(name='반경700m')
grouped_2000m = facilities_in_2000m_buffer.groupby(['산업단지명', '중분류', '소분류']).size().reset_index(name='반경2km')
grouped_5000m = facilities_in_5000m_buffer.groupby(['산업단지명', '중분류', '소분류']).size().reset_index(name='반경5km')

merged_df = pd.merge(grouped_700m, grouped_2000m, on=['산업단지명', '중분류', '소분류'], how='outer')
supply = pd.merge(merged_df, grouped_5000m, on=['산업단지명', '중분류', '소분류'], how='outer')

supply = pd.merge(standard,supply,on=['산업단지명','중분류','소분류'],how='left')
supply.fillna(0, inplace=True)

supply =  supply[supply['중분류'] != '주거시설']
supply1 = supply1[supply1['중분류'] == '주거시설']
supply = pd.concat([supply1,supply],ignore_index=True)
supply

supply['반경2km'] = supply['반경2km'] - supply['반경700m']
supply['반경5km'] = supply['반경5km'] - supply['반경2km']
supply


path_result = os.path.join(config_info["PATH_DATA_OUTPUT_RESULT"], '2024-07-01')
supply.to_excel(path_result + '//공급량_0712.xlsx',index=False)
supply


## 접근성 분석
# 각 산업단지 위치로부터 시설까지의 거리 계산
Industrial_point.crs = 'EPSG:4326'
industrial_gdf = Industrial_point.to_crs(epsg=5179)

distances = []
for idx, industrial in industrial_gdf.iterrows():
    for f_idx, facility in poi_sejong_hjd.iterrows():
        distance = industrial.geometry.distance(facility.geometry)
        distances.append({
            '산업단지명': industrial['산업단지명'],
            '중분류': facility['중분류'],
            '소분류': facility['소분류'],
            '거리': distance
        })

distances_df = pd.DataFrame(distances)

# 중분류, 소분류별로 최근 거리값 및 표준편차 계산
nearest_distances = distances_df.groupby(['산업단지명', '중분류', '소분류'])['거리'].agg(['min', 'std']).round(1).reset_index()
nearest_distances = nearest_distances.rename(columns={'min': '최근거리값', 'std': '최근거리표준편차'})

# 각 버퍼별 해당 시설의 평균 거리값 계산
def calculate_mean_distances(buffer_gdf, facilities_gdf, buffer_name):
    mean_distances = []
    for idx, buffer in buffer_gdf.iterrows():
        industrial_name = buffer['산업단지명']
        facilities_in_buffer = gpd.sjoin(facilities_gdf, gpd.GeoDataFrame(geometry=[buffer.geometry]), how="inner", op='within')
        if not facilities_in_buffer.empty:
            for (middle_class, sub_class), group in facilities_in_buffer.groupby(['중분류', '소분류']):
                mean_distance = group.geometry.apply(lambda x: buffer.geometry.centroid.distance(x)).mean().round(1)
                mean_distances.append({
                    '산업단지명': industrial_name,
                    '중분류': middle_class,
                    '소분류': sub_class,
                    f'{buffer_name}평균거리': mean_distance
                })
    return pd.DataFrame(mean_distances)

mean_distances_700m = calculate_mean_distances(BF_700, poi_sejong_hjd, '반경700m')
mean_distances_2000m = calculate_mean_distances(BF_2000, poi_sejong_hjd, '반경2km')
mean_distances_5000m = calculate_mean_distances(BF_5000, poi_sejong_hjd, '반경5km')


final_df = pd.merge(nearest_distances, mean_distances_700m, on=['산업단지명', '중분류', '소분류'], how='outer')
final_df = pd.merge(final_df, mean_distances_2000m, on=['산업단지명', '중분류', '소분류'], how='outer')
accessibility = pd.merge(final_df, mean_distances_5000m, on=['산업단지명', '중분류', '소분류'], how='outer')

accessibility.fillna(0, inplace=True)
accessibility = accessibility.drop(columns=['최근거리표준편차'])
accessibility.to_excel(path_result + '//이용접근성_0712.xlsx',index=False)
accessibility

#분석결과 매핑
result = pd.merge(accessibility,supply,on=['산업단지명','중분류','소분류'],how='left')
result.fillna(0, inplace=True)
path_middle = os.path.join(config_info["PATH_DATA_OUTPUT_MIDDLE"], '2024-07-01')
result.to_excel(path_result + '//공급량_이용접근성_0712.xlsx',index=False)

# 공급지수 산출
result = pd.read_excel(path_result + '//공급량_이용접근성_0712.xlsx')
result.columns
result['전체시설수'] = result['반경700m'] + result['반경2km'] + result['반경5km']
result
# 그룹바이를 사용하여 합계와 평균을 계산하고 컬럼 이름을 수정
result_2 = result.groupby(['중분류', '산업단지명']).agg({'전체시설수': 'sum', '반경5km평균거리': 'mean'}).reset_index()
result_2.rename(columns={'전체시설수': '공급량', '반경5km평균거리': '이용접근성'}, inplace=True)


#시설별 표준화 진행하기위해 데이터 분류
park = result_2[result_2['중분류'] == '공원시설']
edu = result_2[result_2['중분류'] == '교육시설']
traffic = result_2[result_2['중분류'] == '교통시설']
cul = result_2[result_2['중분류'] == '문화/체육시설']
care = result_2[result_2['중분류'] == '보육시설']
wel = result_2[result_2['중분류'] == '복지시설']
bank = result_2[result_2['중분류'] == '상업/금융시설']
medical = result_2[result_2['중분류'] == '의료시설']
house = result_2[result_2['중분류'] == '주거시설']

# 시설별로 공급량과 이용접근성을 0에서 1 사이의 값으로 표준화하고 공급지수 계산
def calculate_deprivation_index(df):
    scaler = MinMaxScaler()
    df[['공급량_scaled', '이용접근성_scaled']] = scaler.fit_transform(df[['공급량', '이용접근성']])
    df['공급량_scaled'] = df['공급량_scaled']
    df['이용접근성_scaled'] = df['이용접근성_scaled']
    df['이용접근성_scaled2'] = 1 - df['이용접근성_scaled']
    df.loc[(df['공급량'] == 0) & (df['이용접근성'] == 0), '이용접근성_scaled2'] = 0
    df['공급지수'] = ((df['공급량_scaled'] + df['이용접근성_scaled2']) / 2)
    return df

# 각 데이터프레임에 대해 결핍지수 계산 적용
dfs = [park, edu, traffic, cul, care, wel, bank, medical, house]
processed_dfs = [calculate_deprivation_index(df) for df in dfs]
combined_df = pd.concat(processed_dfs)
combined_df
combined_df.to_excel(path_result + '//공급지수_0712.xlsx',index=False)





# ppt
# 전체 거리별 공급량현황
graph_2 = supply.groupby(['중분류'])[['반경700m','반경2km','반경5km']].sum().reset_index()
graph_2.to_excel(path_result + '//그래프_시각화//전체공급량현황_0712.xlsx',index=False)

# 공급량
graph_22 = supply.groupby(['산업단지명','중분류'])[['반경700m','반경2km','반경5km']].sum().reset_index()
graph_22
graph_22.to_excel(path_result + '//그래프_시각화//산업단지별공급량현황_0712.xlsx',index=False)

#graph3
graph3 = combined_df.groupby('산업단지명')[['공급량_scaled','이용접근성_scaled']].sum().reset_index()
graph3
graph3.to_excel(path_result + '//그래프_시각화//정주시설분석결과_0712.xlsx',index=False)

#graph33
graph33 = combined_df.groupby(['산업단지명'])[['공급량_scaled','이용접근성_scaled2']].sum().reset_index()
graph33
graph33.to_excel(path_result + '//그래프_시각화//정주환경평가_종합결과_0712.xlsx',index=False)




#graph4
graph4 = combined_df.copy()
graph4 = graph4[[ '산업단지명','중분류','공급량', '이용접근성', '공급량_scaled', '이용접근성_scaled','이용접근성_scaled2', '공급지수']]
graph4
graph4['공급지수평균'] = graph4.groupby('중분류')['공급지수'].transform('mean')
graph4 = graph4[['산업단지명','중분류','공급지수','공급지수평균']]
graph4 = graph4.sort_values(by=['산업단지명','중분류'])
graph4
graph4.to_excel(path_result + '//그래프_시각화//산업단지별_분석결과_0712.xlsx',index=False)
