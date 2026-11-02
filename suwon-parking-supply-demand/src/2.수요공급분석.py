###########################################################
# 과 제 명: A28_수원시_주차장수요공급분석
# 파 일 명: 2.수요공급분석
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
from shapely.geometry import Point
from pyproj import Proj, transform
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from sklearn.linear_model import LinearRegression


grid100_sw_5179 = gpd.read_file(PATH_RESULT3 + '//거주인구//100m격자_거주인구.gpkg',driver='GPKG')
base_cd_5179 = gpd.read_file(PATH_RESULT3 + '//경계면데이터//기초구역경계//기초구역경계.gpkg',driver='GPKG')
hjd_cd = gpd.read_file(PATH_RESULT3 + '//경계면데이터//행정동경계//행정동경계.gpkg',driver='GPKG')
sgg_hjd = gpd.read_file(PATH_RESULT3 + '//경계면데이터//행정동경계//시군구_행정동경계.gpkg',driver='GPKG')
card_block = gpd.read_file(path_data_in +'//2024-07-15//카드블록경계//tbshp_block_v8.shp',encoding='cp949')

base_cd_area = base_cd_5179.copy()
base_cd_area['기초구역면적'] = base_cd_area['geometry'].area
base_cd_area['기초구역면적'].sum()
base_cd_area = base_cd_area[['기초구역번호','기초구역면적']]
base_cd_area.to_pickle(path_pretreat + '//기초구역별면적.pkl')


parking1_result = gpd.read_file(PATH_RESULT3+'//주차장//공영주차장.gpkg',driver='GPKG')
parking2_result = gpd.read_file(PATH_RESULT3+'//주차장//거주자우선주차장.gpkg',driver='GPKG')
parking3_result = gpd.read_file(PATH_RESULT3+'//주차장//최종_건축물대장주차장.gpkg',driver='GPKG')

car = pd.read_excel(path_data_in + '//2024-06-13//분석용 데이터//차량등록현황_202405//자동차 등록 현황.xlsx')

'''
# 100m격자와 기초구역 경계면 매핑 (교차되는 면적을 기준으로 격자 거주인구 분배)
base_cd_5179['area'] = base_cd_5179.geometry.area
def distribute_population(grids, areas):
    results = []

    for _, grid in grids.iterrows():
        grid_geom = grid.geometry
        grid_id = grid.gid
        grid_population = grid.val

        # 격자와 교차하는 기초구역 찾기
        intersected_areas = areas[areas.geometry.intersects(grid_geom)]

        if intersected_areas.empty:
            continue

        # 교차 면적 비율 계산
        total_intersection_area = 0
        area_fractions = {}

        for _, area in intersected_areas.iterrows():
            area_geom = area.geometry
            intersection_geom = area_geom.intersection(grid_geom)
            if intersection_geom.is_empty:
                continue

            intersection_area = intersection_geom.area
            total_intersection_area += intersection_area
            area_fractions[area['기초구역번호']] = intersection_area

        # 면적 비율을 기반으로 인구 분배
        for area_id, intersection_area in area_fractions.items():
            area_fraction = intersection_area / total_intersection_area
            population_for_area = grid_population * area_fraction

            results.append({
                '기초구역번호': area_id,
                'population': population_for_area
            })

    return pd.DataFrame(results)
# 인구 배분 계산
population_distribution = distribute_population(grid100_sw_5179, base_cd_5179)
# 기초구역별로 인구 수 집계
population_summary = population_distribution.groupby('기초구역번호').agg({'population': 'sum'}).reset_index()
base_cd_pop5179 = pd.merge(base_cd_5179,population_summary,on='기초구역번호',how='left')
base_cd_pop5179.to_file(PATH_RESULT3 + '//기초구역경계//기초구역경계_거주인구.gpkg',driver='GPKG')
'''
# 주차장 데이터 생성
p1 = parking1_result.copy()
p1['주차면수'] = p1['주차면수'].astype(int)
p1['운영형태'] = '전일'
p1['종류'] = '공영주차장'
p1.at[0, '운영형태'] = '야간'
p1 = p1[['시군구명', '행정동명', '행정동코드', '기초구역번호', '구분','운영형태', '주소', '주차면수','종류','geometry']]


p2 = parking2_result.copy()
p2['구분'] = '노상'
p2 = p2.groupby(['시군구명', '행정동명', '행정동코드', '기초구역번호','구분', '운영형태', '주차장명', '주소', 'geometry']).size().reset_index(name='주차면수') #동일한 위치의 행은 주차면수로 판단
p2['종류'] = '거주자우선주차장'
p2 = p2[['시군구명', '행정동명', '행정동코드', '기초구역번호','구분', '운영형태', '주소','주차면수','종류','geometry']]



p3 = parking3_result.copy()
p3.columns
p3['구분'] = '부설'
p3['운영형태'] = '전일'
p3 = p3.rename(columns={'총주차수':'주차면수'})
p3['종류'] = '건축물대장표제부'
p3 = p3[['시군구명', '행정동명', '행정동코드', '기초구역번호', '구분', '운영형태','주소', '주차면수','종류','주용도코드명','옥내기계식대수(대)', '옥외기계식대수(대)', '옥내자주식대수(대)', '옥외자주식대수(대)','geometry']]

p1_total = p1[['시군구명', '행정동명', '행정동코드', '기초구역번호', '구분', '운영형태','주소', '주차면수','종류']]
p2_total = p2[['시군구명', '행정동명', '행정동코드', '기초구역번호', '구분', '운영형태','주소', '주차면수','종류']]
p3_total = p3[['시군구명', '행정동명', '행정동코드', '기초구역번호', '구분', '운영형태','주소', '주차면수','종류']]
p4 = pd.concat([p1_total,p2_total,p3_total],axis=0)

with pd.ExcelWriter(path_result+'//주차장현황//수원시_주차장현황.xlsx') as writer:
    p1.to_excel(writer, sheet_name='공영주차장', index=False)
    p2.to_excel(writer, sheet_name='거주자우선주차장', index=False)
    p3.to_excel(writer, sheet_name='건축물대장주차장', index=False)
    p4.to_excel(writer, sheet_name='구분별주차장현황', index=False)


#카드블록데이터 경계에 시군구,행정동,기초구역 매핑
card_block_a = card_block.sort_values(by='blk_cd_int')

# 교차되는 부분의 면적을 계산하여 더 큰 면적의 기초구역으로 매핑하는 함수
def map_largest_intersection_area(blocks, areas):
    mapped_results = []
    unmapped_results = []

    for _, block in blocks.iterrows():
        block_geom = block.geometry
        block_id = block.BLK_CD

        # 블록과 교차하는 기초구역 찾기
        intersected_areas = areas[areas.geometry.intersects(block_geom)]

        if intersected_areas.empty:
            unmapped_results.append({
                'BLK_CD': block_id,
                'geometry': block_geom
            })
            continue

        # 교차 면적 계산
        max_intersection_area = 0
        selected_area_id = None

        for _, area in intersected_areas.iterrows():
            area_geom = area.geometry
            intersection_geom = area_geom.intersection(block_geom)
            if intersection_geom.is_empty:
                continue

            intersection_area = intersection_geom.area

            if intersection_area > max_intersection_area:
                max_intersection_area = intersection_area
                selected_area_id = area['기초구역번호']

        # 가장 큰 교차 면적을 가진 기초구역으로 매핑
        if selected_area_id is not None:
            mapped_results.append({
                'BLK_CD': block_id,
                '기초구역번호': selected_area_id,
                'intersection_area': max_intersection_area,
                'geometry': block_geom
            })
        else:
            unmapped_results.append({
                'BLK_CD': block_id,
                '기초구역번호': selected_area_id,
                'intersection_area': max_intersection_area,
                'geometry': block_geom
            })

    return pd.DataFrame(mapped_results), pd.DataFrame(unmapped_results)

# 함수 호출
mapped_areas, unmapped_areas = map_largest_intersection_area(card_block_a, base_cd_5179)

# unmapped_areas 수작업으로 처리
unmapped_areas_list = []

for _, row in unmapped_areas.iterrows():
    blk_cd = row['BLK_CD']

    geometry = row['geometry']

    # 수작업으로 값을 지정
    if blk_cd == '432456':
        base_cd = '16695'
    elif blk_cd == '534718':
        base_cd = '16686'
    elif blk_cd == '571900':
        base_cd = '16684'
    elif blk_cd == '571901':
        base_cd = '16684'
    else:
        base_cd = None  # 필요에 따라 기본값을 설정

    unmapped_areas_list.append({
        'BLK_CD': blk_cd,
        '기초구역번호': base_cd,
        'geometry': geometry
    })

# unmapped_areas 수작업 데이터프레임 생성
manual_mapped_areas = pd.DataFrame(unmapped_areas_list)

# mapped_areas와 manual_mapped_areas 결합
final_areas = pd.concat([mapped_areas, manual_mapped_areas], ignore_index=True)
block_base = gpd.GeoDataFrame(final_areas, geometry='geometry', crs='EPSG:5179')
block_base = block_base.to_crs(epsg=5179)
block_base.to_file(PATH_RESULT3+'//카드블록경계//카드블록경계(기초구역매핑).gpkg',driver='GPKG')

def map_largest_intersection_area(blocks, areas):
    mapped_results = []
    unmapped_results = []

    for _, block in blocks.iterrows():
        block_geom = block.geometry
        block_id = block.기초구역번호

        # 블록과 교차하는 기초구역 찾기
        intersected_areas = areas[areas.geometry.intersects(block_geom)]

        if intersected_areas.empty:
            unmapped_results.append({
                'BASE_CD': block_id,
                'geometry': block_geom
            })
            continue

        # 교차 면적 계산
        max_intersection_area = 0
        selected_area_id = None

        for _, area in intersected_areas.iterrows():
            area_geom = area.geometry
            intersection_geom = area_geom.intersection(block_geom)
            if intersection_geom.is_empty:
                continue

            intersection_area = intersection_geom.area

            if intersection_area > max_intersection_area:
                max_intersection_area = intersection_area
                selected_area_id = area['행정동코드']
                selected_area_nm = area['행정동명']
                selected_area_SGGnm = area['시군구명']

        # 가장 큰 교차 면적을 가진 기초구역으로 매핑
        if selected_area_id is not None:
            mapped_results.append({
                '기초구역번호': block_id,
                'HJD_CD': selected_area_id,
                'HJD_NM': selected_area_nm,
                'SGG_NM': selected_area_SGGnm,
                'intersection_area': max_intersection_area,
                'geometry': block_geom
            })
        else:
            unmapped_results.append({
                'BASE_CD': '기초구역번호',
                '기초구역번호': selected_area_id,
                'intersection_area': max_intersection_area,
                'geometry': block_geom
            })

    return pd.DataFrame(mapped_results), pd.DataFrame(unmapped_results)

mapped_areas_base, unmapped_areas = map_largest_intersection_area(base_cd_5179, sgg_hjd)


mapped_areas_base = gpd.GeoDataFrame(mapped_areas_base, geometry='geometry', crs = 'EPSG:5179')
mapped_areas_base = mapped_areas_base.to_crs(epsg=5179)
mapped_areas_base.to_file(PATH_RESULT3+'//기초구역경계//기초구역경계(시군구,행정동매핑).gpkg',driver='GPKG')

#카드블럭에 시군구행정동 매핑
block_base = gpd.read_file(PATH_RESULT3+'//카드블록경계//카드블록경계(기초구역매핑).gpkg')
card_block_r = pd.merge(block_base[['BLK_CD', '기초구역번호',  'geometry']],mapped_areas_base[['기초구역번호', 'HJD_CD', 'HJD_NM', 'SGG_NM']],on='기초구역번호',how='left')
card_block_nm = card_block_r[['SGG_NM','HJD_NM','기초구역번호','BLK_CD']]
card_block_nm.to_excel(path_data_analyze +'//행정동코드//card_cd.xlsx',index=False)
card_block_geo = card_block_r[['SGG_NM','HJD_NM','기초구역번호','BLK_CD','geometry']]
card_block_geo.to_file(PATH_RESULT3+'//카드블록경계//카드블록경계(시군구,행정동,기초구역매핑).gpkg',driver='GPKG')

#기초구역경계에 결과 매핑
mapped_areas_base = gpd.read_file(PATH_RESULT3+'//경계면데이터//기초구역경계//기초구역경계(시군구,행정동매핑).gpkg')
base_boundary = mapped_areas_base.copy()
base_boundary.to_excel(path_result + '//수원시_행정동_기초구역매핑.xlsx',index=False)

parking1 = p1_total.groupby('기초구역번호').agg(공영주차장_면수=('주차면수', 'sum'), 공영주차장_개수=('주소', 'count')).reset_index()
base_parking = pd.merge(base_boundary,parking1,on=['기초구역번호'],how='left')
parking2 = p2_total.groupby('기초구역번호').agg(거주자우선주차장_면수=('주차면수', 'sum'), 거주자우선주차장_개수=('주소', 'count')).reset_index()
base_parking = pd.merge(base_parking,parking2,on=['기초구역번호'],how='left')
parking3 = p3_total.groupby('기초구역번호').agg(건축물대장주차장_면수=('주차면수', 'sum'), 건축물대장주차장_개수=('주소', 'count')).reset_index()
base_parking = pd.merge(base_parking,parking3,on=['기초구역번호'],how='left')
base_parking = base_parking.fillna(0)
base_parking.columns
base_parking = base_parking[['SGG_NM','HJD_CD', 'HJD_NM','기초구역번호', 'intersection_area','공영주차장_면수', '공영주차장_개수', '거주자우선주차장_면수', '거주자우선주차장_개수', '건축물대장주차장_면수',
       '건축물대장주차장_개수', 'geometry']]
base_parking_notgeo = base_parking[['SGG_NM','HJD_CD', 'HJD_NM','기초구역번호', 'intersection_area','공영주차장_면수', '공영주차장_개수', '거주자우선주차장_면수', '거주자우선주차장_개수', '건축물대장주차장_면수',
       '건축물대장주차장_개수']]
base_parking.to_file(PATH_RESULT3+'//공급분석//공급분석_기초구역경계(유형).gpkg',driver='GPKG')
base_parking_notgeo.to_excel(path_result+'//공급분석//수원시_기초구역별_주차장공급분석(유형).xlsx',index=False)


p4['기초구역번호'].nunique()
# 피벗 테이블 생성
p4_pivot = pd.pivot_table(
    p4,
    index='기초구역번호',  # 행
    columns='구분',      # 열
    values='주차면수',      # 값
    aggfunc='sum',         # 집계 함수
    fill_value=0           # NaN 값을 0으로 대체
).reset_index()

p4_pivot_geo = pd.merge(base_boundary,p4_pivot,on='기초구역번호',how='left')
p4_pivot_geo = p4_pivot_geo.fillna(0)
p4_pivot_geo = p4_pivot_geo[['SGG_NM','HJD_CD', 'HJD_NM','기초구역번호',  '노상', '노외', '부설','geometry']]
p4_pivot_notgeo = p4_pivot_geo[['SGG_NM','HJD_CD', 'HJD_NM','기초구역번호',  '노상', '노외', '부설']]
p4_pivot_notgeo.to_excel(path_result+'//공급분석//수원시_기초구역별_주차장공급분석(구분).xlsx',index=False)

#데이터 불러오기
base_cd_pop5179 = gpd.read_file(PATH_RESULT3 + '//거주인구//기초구역경계_거주인구.gpkg')
parking11 = pd.read_excel(path_result+'//공급분석//수원시_기초구역별_주차장공급분석(유형).xlsx')
parking11['총주차면수'] = parking11[['공영주차장_면수','거주자우선주차장_면수','건축물대장주차장_면수']].sum(axis=1)
parking11.to_excel(path_result+'//공급분석//수원시_기초구역별_주차장공급분석(유형).xlsx',index=False)

parking22 = pd.read_excel(path_result+'//공급분석//수원시_기초구역별_주차장공급분석(구분).xlsx')
parking22['총주차면수'] = parking22[['노상','노외','부설']].sum(axis=1)
parking22.to_excel(path_result+'//공급분석//수원시_기초구역별_주차장공급분석(구분).xlsx',index=False)
#기초구역별 총 주차장면수
parking = parking11[['SGG_NM', 'HJD_CD', 'HJD_NM', '기초구역번호','intersection_area', '총주차면수']]


#차량등록대수 현황
pre_car = car.copy()
pre_car.isnull().sum()
pre_car['sgg_name'] = pre_car['등록주소'].str.extract(r' (\S+구)')
#pre_car.to_excel(path_middle+'//수원시_수요_차량등록대수.xlsx',index=False)
pre_car = pre_car[['sgg_name','등록주소', '용도', '차종',]]

pre_car_pivot = pre_car.pivot_table(index=['sgg_name','등록주소', '용도'], columns='차종', aggfunc='size', fill_value=0).reset_index()
pre_car_pivot['합계'] = pre_car_pivot[['경형', '대형', '소형', '저상형', '중형']].sum(axis=1)
pre_car_pivot.groupby('sgg_name')['합계'].sum()#(568,327건 기타 8건)
#우편번호 프로그램 후
pre_car2 = pd.read_excel(path_middle+'//차량등록대수//차량등록대수(우편번호).xlsx')
pre_car2 = pre_car2[['우편번호','등록주소']]
pre_car2.drop_duplicates(inplace=True)
pre_car3 = pd.merge(pre_car_pivot,pre_car2[['등록주소','우편번호']],on='등록주소',how="left")
pre_car3 = pre_car3.rename(columns={'우편번호':'기초구역번호'})
pre_car3.groupby('sgg_name')['합계'].sum()#(568,327건 기타 8건)
#pre_car3.isnull().sum()
pre_car4 = pre_car3.dropna()
#pre_car4.isnull().sum()
#pre_car3['기초구역번호'].nunique()
#pre_car4['기초구역번호'].nunique()
pre_car4['기초구역번호'] = pre_car4['기초구역번호'].astype(int)
pre_car4['기초구역번호'] = pre_car4['기초구역번호'].astype(str)
pre_car3.to_excel(path_middle + '//차량등록대수//차량등록대수_null존재.xlsx',index=False )

pre_car4_geo = pd.merge(pre_car4,base_boundary,on='기초구역번호',how='left')
pre_car4 = pre_car4_geo[['SGG_NM','HJD_NM','기초구역번호', '용도', '경형', '대형', '소형', '저상형', '중형', '합계']]
pre_car5 = pre_car4.groupby(['SGG_NM','HJD_NM','기초구역번호', '용도'])[['경형', '대형', '소형', '저상형', '중형', '합계']].sum().reset_index()
pre_car5.to_excel(path_result + '//차량등록대수//차량등록대수.xlsx',index=False )

# 자가용
pre_car4_geo_1 = pre_car4_geo[pre_car4_geo['용도'] == '자가용']
pre_car4_geo_1 = pre_car4_geo_1.groupby(['기초구역번호'])[['경형', '대형', '소형', '저상형', '중형', '합계']].sum().reset_index()
pre_car4_geo_1 = pd.merge(base_boundary,pre_car4_geo_1,on='기초구역번호',how='left')
pre_car4_geo_1 = pre_car4_geo_1.fillna(0)
pre_car4_geo_1 = gpd.GeoDataFrame(pre_car4_geo_1, geometry='geometry', crs='EPSG:5179')
pre_car4_geo_1.to_file(PATH_RESULT3 + '//차량등록대수//차량등록대수_자가용.gpkg',driver='GPKG')

# 영업용
pre_car4_geo_2 = pre_car4_geo[pre_car4_geo['용도'] == '영업용']
pre_car4_geo_2 = pre_car4_geo_2.groupby(['기초구역번호'])[['경형', '대형', '소형', '저상형', '중형', '합계']].sum().reset_index()
pre_car4_geo_2 = pd.merge(base_boundary,pre_car4_geo_2,on='기초구역번호',how='left')
pre_car4_geo_2 = pre_car4_geo_2.fillna(0)
pre_car4_geo_2 = gpd.GeoDataFrame(pre_car4_geo_2, geometry='geometry', crs='EPSG:5179')
pre_car4_geo_2.to_file(PATH_RESULT3 + '//차량등록대수//차량등록대수_영업용.gpkg',driver='GPKG')

#거주인구
base_pop = base_cd_pop5179[['기초구역번호', '면적', 'area', 'population']]
base_pop['기초구역번호'] = base_pop['기초구역번호'].astype(str)
base_boundary['기초구역번호'] = base_boundary['기초구역번호'].astype(str)
base_pop_mer = pd.merge(base_boundary,base_pop,on='기초구역번호',how='left')
base_pop_mer2 = base_pop_mer[[ 'SGG_NM','HJD_CD', 'HJD_NM', '기초구역번호','population']]
#base_pop_mer2.to_excel(path_result+'//수요분석//수원시_기초구역별_거주인구.xlsx',index=False)
base_pop_mer = base_pop_mer[[ 'SGG_NM','HJD_CD', 'HJD_NM', '기초구역번호','population','geometry']]
base_pop_mer['기초구역번호'] = base_pop_mer['기초구역번호'].astype(str)
base_pop_mer.columns = ['SGG_NM','HJD_CD','HJD_NM','기초구역번호','거주인구','geometry']
# 거주인구 대비 주차장 공급비율
parking['기초구역번호'] = parking['기초구역번호'].astype(str)
parking_r = pd.merge(parking,base_pop_mer,on=['SGG_NM','HJD_CD','HJD_NM','기초구역번호'],how='left')
parking_r['주차장공급비율(%)'] = ((parking_r['총주차면수'] / parking_r['거주인구'])*100).round(1)


# 거주인구 대비 차량 대수 비율 계산
pre_car6 = pre_car4.groupby(['SGG_NM','HJD_NM','기초구역번호'])[['경형', '대형', '소형', '저상형', '중형', '합계']].sum().reset_index()

parking_r2 = pd.merge(parking_r,pre_car6,on=['SGG_NM','HJD_NM','기초구역번호'],how='left')
parking_r2 = parking_r2.fillna(0)
parking_r2['차량대수비율(%)'] = ((parking_r2['합계'] / parking_r2['거주인구'])*100).round(1)
parking_r2.replace([np.inf, -np.inf], np.nan, inplace=True)
parking_r2.fillna(0, inplace=True)

X = parking_r2[['거주인구']]# 회귀 모델 적합
y = parking_r2['합계']
model = LinearRegression()
model.fit(X, y)

parking_r2['예측값'] = model.predict(X)# 회귀선 예측값 계산
parking_r2['잔차'] = parking_r2['합계'] - parking_r2['예측값']# 잔차 계산
# 잔차의 절대값이 큰 포인트 식별 (예: 상위 2개)
threshold = parking_r2['잔차'].abs().quantile(0.9)  # 상위 10%를 기준으로 설정
outliers = parking_r2[parking_r2['잔차'].abs() > threshold]
plt.figure(figsize=(9, 6))# 회귀선이 포함된 산점도 시각화
sns.regplot(x='거주인구', y='합계', data=parking_r2, scatter_kws={'s':70}, line_kws={'color':'red'})

for idx, row in outliers.iterrows():
    plt.text(row['거주인구'], row['합계'], row['기초구역번호'],
             fontsize=9, ha='right', va='bottom', color='black')# 잔차가 큰 포인트에 라벨 추가

plt.xlabel('거주인구')
plt.ylabel('등록차량대수')
plt.title('거주인구와 등록차량 대수 간의 회귀선')
plt.grid(True)
plt.show()

parking_r2.rename(columns ={'합계':'등록차량대수'},inplace=True)
# 상관관계 분석
correlation = parking_r2[['거주인구', '등록차량대수']].corr().iloc[0, 1]
print(f'거주인구와 등록차량 대수 간의 상관관계: {correlation:.2f}')

parking_r2.columns
parking_r2
parking_r3 = parking_r2[['SGG_NM', 'HJD_CD', 'HJD_NM', '기초구역번호','거주인구','등록차량대수','총주차면수','주차장공급비율(%)', '차량대수비율(%)']]
parking_r3.to_excel(path_result + '//수요분석//거주인구대비분석.xlsx',index=False )
parking_r2_geo = parking_r2[['SGG_NM', 'HJD_CD', 'HJD_NM', '기초구역번호','거주인구','등록차량대수','총주차면수','주차장공급비율(%)', '차량대수비율(%)','geometry']]
parking_r2_geo = gpd.GeoDataFrame(parking_r2_geo, geometry='geometry', crs='EPSG:5179')
parking_r2_geo.to_file(PATH_RESULT3 + '//거주인구//거주인구대비분석.gpkg',driver='GPKG')


#기초구역별 거주인구 및 거주자주차장 데이터 생성
parking_1 = pd.read_excel(path_result + '//공급분석//수원시_기초구역별_주차장공급분석(유형).xlsx')
parking_2 = pd.read_excel(path_result + '//주차장현황//최종_건축물대장주차장.xlsx')

base_pop_mer.columns = ['시군구명','행정동코드','행정동명','기초구역번호','거주인구','geometry']
base_pop_mer2 = base_pop_mer[['행정동명','기초구역번호','거주인구','geometry']]

parking_1_p = parking_1[['기초구역번호','거주자우선주차장_면수']]
parking_1_p = parking_1.groupby('기초구역번호')['거주자우선주차장_면수'].sum().reset_index()
parking_1_p['거주자우선주차장_면수'].sum()

parking_2_p = parking_2[parking_2['주용도코드명'].isin(['공동주택', '단독주택'])]
parking_2_p = parking_2_p.groupby('기초구역번호')['총주차수'].sum().reset_index()
parking_2_p['총주차수'].sum()

base_pop_mer2['기초구역번호'] = base_pop_mer2['기초구역번호'].astype(str)
parking_1_p['기초구역번호'] = parking_1_p['기초구역번호'].astype(str)
parking_2_p['기초구역번호'] = parking_2_p['기초구역번호'].astype(float)
parking_2_p['기초구역번호'] = parking_2_p['기초구역번호'].astype(int)
parking_2_p['기초구역번호'] = parking_2_p['기초구역번호'].astype(str)

base_pop_mer3 = pd.merge(base_pop_mer2,parking_1_p,on='기초구역번호',how='left')
base_pop_mer_r = pd.merge(base_pop_mer3,parking_2_p,on='기초구역번호',how='left')
base_pop_mer_r.fillna(0, inplace=True)

base_pop_mer_r['거주자주차장'] = base_pop_mer_r['거주자우선주차장_면수'] + base_pop_mer_r['총주차수']
base_pop_mer_r =base_pop_mer_r[['행정동명', '기초구역번호', '거주인구', '거주자우선주차장_면수', '총주차수', '거주자주차장', 'geometry']]
base_pop_mer_r.columns = ['행정동명','기초구역번호','거주인구','거주자우선_면수','건축물대장(공동,단독)_면수','거주자주차장','geometry']
base_pop_mer_rx = base_pop_mer_r[['행정동명','기초구역번호','거주인구','거주자우선_면수','건축물대장(공동,단독)_면수','거주자주차장']]
base_pop_mer_rx.to_excel(path_result + '//수요분석//거주인구_거주자주차장(기초구역).xlsx',index=False)

base_pop_mer_rx_hjd = base_pop_mer_rx.groupby('행정동명')[['거주인구','거주자우선_면수','건축물대장(공동,단독)_면수','거주자주차장']].sum().reset_index()
base_pop_mer_rx_hjd['거주인구기준_주차장공급비율'] = ((base_pop_mer_rx_hjd['거주자주차장']/base_pop_mer_rx_hjd['거주인구'])*100).astype(int)

base_pop_mer_rx_hjd.to_excel(path_result + '//수요분석//거주인구_거주자주차장(행정동).xlsx',index=False)


df_sorted = base_pop_mer_rx_hjd.sort_values(by='거주인구', ascending=False)
df_sorted.reset_index(drop=True, inplace=True)
# 그룹 생성
grouped = df_sorted.groupby(df_sorted.index // 4).agg(
    거주인구그룹평균=('거주인구', 'mean'),
    주차면수그룹평균=('거주자주차장', 'mean'),
    공급비율=('거주자주차장', lambda x: (x.sum() / (df_sorted.iloc[x.index]['거주인구'].sum())) * 100),
    그룹=('행정동명', lambda x: f"{x.tolist()}")
).reset_index(drop=True)

# 공급비율 포맷팅
grouped['공급비율'] = grouped['공급비율'].map('{:.1f}%'.format)
grouped.to_excel(path_result + '//수요분석//거주인구_거주자주차장공급비율(행정동그룹).xlsx',index=False)

#기초구역별 차량등록대수 대비 주차장공급비율
base_car = pd.read_excel(path_result + "//차량등록대수//차량등록대수.xlsx")
base_parkk = pd.read_excel(path_result + "//공급분석//수원시_기초구역별_주차장공급분석(구분).xlsx")

base_carr = base_car.groupby('기초구역번호')['합계'].sum().reset_index()
base_carr.columns = ['기초구역번호','총등록차량수']

base_result1 = pd.merge(base_parkk,base_carr,on='기초구역번호',how='left')
base_result1 = base_result1.fillna(0)

base_result1['주차장확보율'] = ((base_result1['총주차면수']/base_result1['총등록차량수'])*100).round(1)
base_result1['주차장확보율'].replace([np.inf, -np.inf], 0, inplace=True)
base_result1 = base_result1.fillna(0)
base_result1.columns

base_result1.to_pickle(path_middle + '//기초구역경계//기초구역경계_주차장확보율.pkl')
base_result1.to_excel(path_result + '//주차장확보율//차량등록수_주차장공급비율_기초구역기준.xlsx',index=False)
base_boundary['기초구역번호'] = base_boundary['기초구역번호'].astype(int)
base_result2 = pd.merge(base_boundary[['기초구역번호','geometry']],base_result1,on='기초구역번호',how='left')
base_result2 = base_result2[['기초구역번호',  'SGG_NM', 'HJD_CD', 'HJD_NM', '노상', '노외', '부설','총주차면수', '총등록차량수', '주차장확보율','geometry']]
base_result2 = gpd.GeoDataFrame(base_result2, geometry='geometry', crs='EPSG:5179')
base_result2.to_file(PATH_RESULT3 + '//주차장확보율//차량등록수_주차장공급비율_기초구역기준.gpkg',driver='GPKG')


#qgis 생성
base_cd_5179.info()
parking11 = pd.read_excel(path_result+'//공급분석//수원시_기초구역별_주차장공급분석(유형).xlsx')
parking11['']
parking11['기초구역번호'] = parking11['기초구역번호'].astype(str)
parking11_geo = pd.merge(base_cd_5179,parking11,on='기초구역번호',how='left')
parking11_geo = parking11_geo[['기초구역번호', 'SGG_NM', 'HJD_CD', 'HJD_NM','intersection_area', '공영주차장_면수', '공영주차장_개수', '거주자우선주차장_면수','거주자우선주차장_개수', '건축물대장주차장_면수', '건축물대장주차장_개수', '총주차면수', 'geometry']]
parking11_geo = gpd.GeoDataFrame(parking11_geo, geometry='geometry', crs='EPSG:5179')
parking11_geo.to_file(PATH_RESULT3 + '//공급분석//기초구역별_주차장공급.gpkg',driver='GPKG')

