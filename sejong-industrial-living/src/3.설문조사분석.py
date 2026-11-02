###########################################################
# 과 제 명: A34_세종시_정주인구분석
# 파 일 명: 3.설문조사분석
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
path_base = "2024-06-25"
path_data_out = os.path.join(config_info["PATH_DATA_COLLECT"], "01.외부",path_base)
path_data_in = os.path.join(config_info["PATH_DATA_COLLECT"], "02.내부",path_base)
path_data_analyze = os.path.join(config_info["PATH_DATA_ANALYZE"])
path_data_output = os.path.join(config_info["PATH_DATA_OUTPUT"])
path_base = "2024-07-01"
path_database = os.path.join(config_info["PATH_DATA_OUTPUT_DATEBASE"], path_base)
path_pretreat = os.path.join(config_info["PATH_DATA_OUTPUT_PRETREAT"],path_base)
path_middle = os.path.join(config_info["PATH_DATA_OUTPUT_MIDDLE"], path_base)
path_result = os.path.join(config_info["PATH_DATA_OUTPUT_RESULT"], '2024-07-01')
# 1.1.SQLite 저장시 사용됨
##name_database = f"DB_{config_info['과제ID']}_202309.db" #
# ==================================================================================================

# 필요라이브러리
import pandas as pd
import numpy as np
import re
sdata_wroker = pd.read_excel(path_data_in + '//설문조사 결과 취합(북부권 정주여건)_취합본(원본,그래프,기업주).xlsx',sheet_name='근로자',skiprows=1)

sdata_wroker = sdata_wroker[['연번', 'Q1',  'Q6', '생활여건 만족도', 'Unnamed: 13',
       'Unnamed: 14', 'Unnamed: 15', 'Unnamed: 16', 'Unnamed: 17',
       'Unnamed: 18', 'Unnamed: 19', 'Unnamed: 20', 'Unnamed: 21',
       'Unnamed: 22', 'Unnamed: 23', 'Unnamed: 24',
       'Q7', '시급히 확충 필요분야','Unnamed: 27',
       'Q9','거주지 선택시 중요한 분야', 'Unnamed: 34',]]


# 0번 행을 컬럼으로 사용하기
new_columns = sdata_wroker.iloc[0]
# 데이터프레임의 첫 번째 행을 삭제하고, 새로운 컬럼으로 설정
sdata_wroker = sdata_wroker[1:]
sdata_wroker.columns = new_columns
sdata_wroker.columns = ['ID', '산업단지구분', '주거_만족도', '교통_만족도','주차_만족도','보율_만족도', '교육_만족도', '쇼핑_만족도', '의료_만족도', '편의_만족도', '식음_만족도', '휴식_만족도', '문화_만족도','체육_만족도', '업무_만족도', '전반적_만족도', '시급_1순위','시급_2순위','시급_3순위','중요_1순위','중요_2순위','중요_3순위']

# 숫자만 추출하는 함수
def extract_number(text):
    # NaN일 경우 처리
    if pd.isnull(text):
        return ''
    # 정수 데이터인 경우 그대로 반환
    if isinstance(text, int):
        return str(text)
    # 문자열인 경우 숫자만 추출
    return ''.join(filter(str.isdigit, text))
def extract_numbers_from_columns(df, columns):
    for col in columns:
        df[col] = df[col].apply(extract_number)
    return df

# 시급성과 중요도 컬럼 리스트
urgency_columns = ['시급_1순위', '시급_2순위', '시급_3순위']
importance_columns = ['중요_1순위', '중요_2순위', '중요_3순위']
sdata_wroker = extract_numbers_from_columns(sdata_wroker, urgency_columns + importance_columns)
#sdata_wroker.to_excel(path_pretreat + '//설문조사//설문조사결과.xlsx',index=False)

sdata_wroker_pre = pd.read_excel(path_pretreat + '//설문조사//설문조사결과.xlsx')
sdata_wroker_pre
# 만족도
sdata_wroker_A = sdata_wroker_pre.copy()
satisfaction_columns = [col for col in sdata_wroker_A.columns if '만족도' in col]
df_satisfaction_mean = sdata_wroker.groupby('산업단지구분')[satisfaction_columns].mean().round(2).reset_index()
df_satisfaction_mean.to_excel(path_result + '//설문조사분석//만족도.xlsx',index=False)
df_satisfaction_mean

#시급성
sdata_wroker_B = sdata_wroker_pre.copy()
sdata_wroker_B = sdata_wroker_B[['ID','산업단지구분','시급_1순위', '시급_2순위', '시급_3순위']]
sdata_wroker_B.head()


# 시급별 가중치
weights = {'시급_1순위': 3, '시급_2순위': 2, '시급_3순위': 1}
# 결과를 저장할 리스트
results = []
# 각 산업단지구분별로 시급별 시설번호의 빈도수 계산
for industry in sdata_wroker_B['산업단지구분'].unique():
    industry_data = sdata_wroker_B[sdata_wroker_B['산업단지구분'] == industry]
    facility_counts = {facility: {'count': 0, 'weighted_count': 0} for facility in range(1, 15)}

    for priority, weight in weights.items():
        counts = industry_data[priority].value_counts(dropna=True)
        for facility, count in counts.items():
            if facility not in facility_counts:
                facility_counts[facility] = {'count': 0, 'weighted_count': 0}
            facility_counts[facility]['count'] += count
            facility_counts[facility]['weighted_count'] += count * weight

    for facility, counts in facility_counts.items():
        results.append({
            '산업단지번호': industry,
            '시설번호': facility,
            '개수': counts['count'],
            '가중치합': counts['weighted_count']
        })

# 결과를 데이터프레임으로 변환
result_df = pd.DataFrame(results)
result_df = result_df.sort_values(by=['산업단지번호', '시설번호']).reset_index(drop=True)

pivot_df = result_df.pivot(index='산업단지번호', columns='시설번호', values='가중치합').reset_index()
# 첫 번째 열을 제외한 각 행의 데이터를 최소값과 최대값을 이용하여 1~5 사이의 값으로 표준화합니다
min_vals = pivot_df.iloc[:, 1:].min(axis=1)
max_vals = pivot_df.iloc[:, 1:].max(axis=1)

# 최소값을 1, 최대값을 5로 스케일링하여 표준화합니다
df_standardized = pivot_df.copy()  # 원본 데이터프레임 복사
df_standardized
# 첫 번째 열(A)을 제외한 각 행의 데이터를 표준화합니다
df_standardized.iloc[:, 1:] = (df_standardized.iloc[:, 1:] - min_vals.values[:, np.newaxis]) / (max_vals.values[:, np.newaxis] - min_vals.values[:, np.newaxis]) * 4 + 1
df_standardized
df_standardized.to_excel(path_result + '//설문조사분석//시급성.xlsx',index=False)

#중요도
sdata_wroker_C = sdata_wroker_pre.copy()
sdata_wroker_C = sdata_wroker_C[['ID','산업단지구분','중요_1순위', '중요_2순위', '중요_3순위']]
sdata_wroker_C.head()

# 시급별 가중치
weights = {'중요_1순위': 3, '중요_2순위': 2, '중요_3순위': 1}
# 결과를 저장할 리스트
results = []
# 각 산업단지구분별로 시급별 시설번호의 빈도수 계산
for industry in sdata_wroker_C['산업단지구분'].unique():
    industry_data = sdata_wroker_C[sdata_wroker_C['산업단지구분'] == industry]
    facility_counts = {facility: {'count': 0, 'weighted_count': 0} for facility in range(1, 15)}

    for priority, weight in weights.items():
        counts = industry_data[priority].value_counts(dropna=True)
        for facility, count in counts.items():
            if facility not in facility_counts:
                facility_counts[facility] = {'count': 0, 'weighted_count': 0}
            facility_counts[facility]['count'] += count
            facility_counts[facility]['weighted_count'] += count * weight

    for facility, counts in facility_counts.items():
        results.append({
            '산업단지번호': industry,
            '시설번호': facility,
            '개수': counts['count'],
            '가중치합': counts['weighted_count']
        })

# 결과를 데이터프레임으로 변환
result_df = pd.DataFrame(results)
result_df = result_df.sort_values(by=['산업단지번호', '시설번호']).reset_index(drop=True)

pivot_df = result_df.pivot(index='산업단지번호', columns='시설번호', values='가중치합').reset_index()
# 첫 번째 열을 제외한 각 행의 데이터를 최소값과 최대값을 이용하여 1~5 사이의 값으로 표준화합니다
min_vals = pivot_df.iloc[:, 1:].min(axis=1)
max_vals = pivot_df.iloc[:, 1:].max(axis=1)

# 최소값을 1, 최대값을 5로 스케일링하여 표준화합니다
df_standardized = pivot_df.copy()  # 원본 데이터프레임 복사
df_standardized
# 첫 번째 열(A)을 제외한 각 행의 데이터를 표준화합니다
df_standardized.iloc[:, 1:] = (df_standardized.iloc[:, 1:] - min_vals.values[:, np.newaxis]) / (max_vals.values[:, np.newaxis] - min_vals.values[:, np.newaxis]) * 4 + 1
df_standardized
df_standardized.to_excel(path_result + '//설문조사분석//중요도.xlsx',index=False)



# 기업주 분석 ======================================================================================================================
sdata_owner = pd.read_excel(path_data_in + '//설문조사 결과 취합(북부권 정주여건)_취합본(원본,그래프,기업주).xlsx',sheet_name='기업주',skiprows=1)
sdata_owner = sdata_owner[['연번', 'Q1', 'Q2', 'Q15','산단 주변 정주여건 강화 분야', 'Unnamed: 48',]]

# 0번 행을 컬럼으로 사용하기
new_columns = sdata_owner.iloc[0]
# 데이터프레임의 첫 번째 행을 삭제하고, 새로운 컬럼으로 설정
sdata_owner = sdata_owner[1:]
sdata_owner.columns = new_columns

sdata_owner.columns = ['ID','기업명', '산업단지구분', '시급_1순위','시급_2순위','시급_3순위']

#시급성
sdata_owner_B = sdata_owner.copy()
sdata_owner_B = sdata_owner_B[['ID','산업단지구분','시급_1순위', '시급_2순위', '시급_3순위']]
sdata_owner_B.head()


# 시급별 가중치
weights = {'시급_1순위': 3, '시급_2순위': 2, '시급_3순위': 1}
# 결과를 저장할 리스트
results = []
# 각 산업단지구분별로 시급별 시설번호의 빈도수 계산
for industry in sdata_owner_B['산업단지구분'].unique():
    industry_data = sdata_owner_B[sdata_owner_B['산업단지구분'] == industry]
    facility_counts = {facility: {'count': 0, 'weighted_count': 0} for facility in range(1, 13)}

    for priority, weight in weights.items():
        counts = industry_data[priority].value_counts(dropna=True)
        for facility, count in counts.items():
            if facility not in facility_counts:
                facility_counts[facility] = {'count': 0, 'weighted_count': 0}
            facility_counts[facility]['count'] += count
            facility_counts[facility]['weighted_count'] += count * weight

    for facility, counts in facility_counts.items():
        results.append({
            '산업단지번호': industry,
            '시설번호': facility,
            '개수': counts['count'],
            '가중치합': counts['weighted_count']
        })

# 결과를 데이터프레임으로 변환
result_df = result_df.sort_values(by=['산업단지번호', '시설번호']).reset_index(drop=True)

pivot_df = result_df.pivot(index='산업단지번호', columns='시설번호', values='가중치합').reset_index()
# 첫 번째 열을 제외한 각 행의 데이터를 최소값과 최대값을 이용하여 1~5 사이의 값으로 표준화합니다
min_vals = pivot_df.iloc[:, 1:].min(axis=1)
max_vals = pivot_df.iloc[:, 1:].max(axis=1)

# 최소값을 1, 최대값을 5로 스케일링하여 표준화합니다
df_standardized = pivot_df.copy()  # 원본 데이터프레임 복사

df_standardized = pd.DataFrame(df_standardized)

# 첫 번째 열(A)을 제외한 각 행의 데이터를 표준화합니다
df_standardized.iloc[:, 1:-1] = (df_standardized.iloc[:, 1:-1] - min_vals.values[:, np.newaxis]) / (max_vals.values[:, np.newaxis] - min_vals.values[:, np.newaxis]) * 4 + 1
df_standardized
df_standardized.to_excel(path_result + '//설문조사분석//기업주//기업주_결과.xlsx',index=False)


