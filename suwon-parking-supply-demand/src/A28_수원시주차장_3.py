import os
import pandas as pd
import matplotlib.pyplot as plt
import pickle
import seaborn as sns

#### 경로지정 ####

outdir =  r'D:\\10.outfile'    ## output 생성 폴더
os.makedirs(outdir)

datadir =  r'C:\\rawdata\\A28'    ## output 생성 폴더
os.makedirs(datadir)

#############################
#############################

## 분석데이터 불러오기 : csv 파일 로드

# 폴더 내의 파일 목록 가져오기
csv_files = [f for f in os.listdir(datadir) if f.endswith('.CSV')]

# Excel 파일을 읽어와서 데이터프레임 생성
for idx, csv_file in enumerate(csv_files, start=1):
    full_path = os.path.join(datadir, csv_file)
    dataframe = pd.read_csv(full_path)

    # 파일 이름의 마지막 10글자를 가져오기
    base_name = csv_file[-11:-4]  # 마지막 10글자만 남기고 확장자 제거
    pickle_file_name = 'card' + base_name + '.pkl'

    # DataFrame을 pickle 파일로 저장하기
    dataframe.to_pickle(pickle_file_name)
    print(f"Converted {csv_file} to {pickle_file_name}")

#### 유동인구 15번 데이터 로드
datadir =  r'C:\\rawdata\\A28\\move_t15'    ## output 생성 폴더
# 폴더 내의 파일 목록 가져오기
csv_files = [f for f in os.listdir(datadir) if f.endswith('.csv')]

# Excel 파일을 읽어와서 데이터프레임 생성
for idx, csv_file in enumerate(csv_files, start=1):
    full_path = os.path.join(datadir, csv_file)
    dataframe = pd.read_csv(full_path)

    # 파일 이름의 마지막 10글자를 가져오기
    base_name = csv_file[-16:-9]  # 연월 추출
    pickle_file_name = 'move' + base_name + '.pkl'

    # DataFrame을 pickle 파일로 저장하기
    dataframe.to_pickle(pickle_file_name)
    print(f"Converted {csv_file} to {pickle_file_name}")


#### 유동인구 13번 데이터 로드  : 출발지별 목적지별 방문목적
datadir =  r'C:\\rawdata\\A28\\move_t13'    ## output 생성 폴더
# 폴더 내의 파일 목록 가져오기
csv_files = [f for f in os.listdir(datadir) if f.endswith('.csv')]

# Excel 파일을 읽어와서 데이터프레임 생성
for idx, csv_file in enumerate(csv_files, start=1):
    full_path = os.path.join(datadir, csv_file)
    dataframe = pd.read_csv(full_path)

    # 파일 이름의 마지막 10글자를 가져오기
    base_name = csv_file[-16:-9]  # 연월 추출
    pickle_file_name = 'move_t13_' + base_name + '.pkl'

    # DataFrame을 pickle 파일로 저장하기
    dataframe.to_pickle(pickle_file_name)
    print(f"Converted {csv_file} to {pickle_file_name}")



#### 유동인구 17번 데이터 로드 : 방문목적 체류시간
datadir =  r'C:\\rawdata\\A28\\move_t17'    ## 원천데이터 경로 폴더

# 폴더 내의 파일 목록 가져오기
csv_files = [f for f in os.listdir(datadir) if f.endswith('.csv')]

# Excel 파일을 읽어와서 데이터프레임 생성
all_data = []
for idx, csv_file in enumerate(csv_files, start=1):
    full_path = os.path.join(datadir, csv_file)
    dataframe = pd.read_csv(full_path)
    print(f"Converted {csv_file} ")
    all_data.append(dataframe)

    move_t17 = pd.concat(all_data)
    move_t17.to_pickle('move_t17.pkl')



#### 유동인구 17번 데이터 로드 : 이동시간 체류시간
datadir =  r'C:\\rawdata\\A28\\move_t19'    ## 원천데이터 경로 폴더

# 폴더 내의 파일 목록 가져오기
csv_files = [f for f in os.listdir(datadir) if f.endswith('.csv')]

# Excel 파일을 읽어와서 데이터프레임 생성
all_data = []
for idx, csv_file in enumerate(csv_files, start=1):
    full_path = os.path.join(datadir, csv_file)
    dataframe = pd.read_csv(full_path)
    print(f"Converted {csv_file} ")
    all_data.append(dataframe)

    move_t19 = pd.concat(all_data)
    move_t19.to_pickle('move_t19.pkl')



#### 유동인구 5번 데이터 로드 : 유입인구 이동목적
datadir =  r'C:\\rawdata\\A28\\move_t5'    ## 원천데이터 경로 폴더

# 폴더 내의 파일 목록 가져오기
csv_files = [f for f in os.listdir(datadir) if f.endswith('.csv')]

# Excel 파일을 읽어와서 데이터프레임 생성
all_data = []
for idx, csv_file in enumerate(csv_files, start=1):
    full_path = os.path.join(datadir, csv_file)
    dataframe = pd.read_csv(full_path)
    print(f"Converted {csv_file} ")
    all_data.append(dataframe)

    move_t5 = pd.concat(all_data)
    move_t5.to_pickle('move_t5.pkl')

#### 유동인구 7번 데이터 로드 : 유입인구 이동수단
datadir =  r'C:\\rawdata\\A28\\move_t7'    ## 원천데이터 경로 폴더

# 폴더 내의 파일 목록 가져오기
csv_files = [f for f in os.listdir(datadir) if f.endswith('.csv')]

# Excel 파일을 읽어와서 데이터프레임 생성
all_data = []
for idx, csv_file in enumerate(csv_files, start=1):
    full_path = os.path.join(datadir, csv_file)
    dataframe = pd.read_csv(full_path)
    print(f"Converted {csv_file} ")
    all_data.append(dataframe)

    move_t7 = pd.concat(all_data)
    move_t7.to_pickle('move_t7.pkl')

#### 유동인구 11번 데이터 로드 : 유출인구 이동수단
datadir =  r'C:\\rawdata\\A28\\move_t11'    ## 원천데이터 경로 폴더

# 폴더 내의 파일 목록 가져오기
csv_files = [f for f in os.listdir(datadir) if f.endswith('.csv')]

# Excel 파일을 읽어와서 데이터프레임 생성
all_data = []
for idx, csv_file in enumerate(csv_files, start=1):
    full_path = os.path.join(datadir, csv_file)
    dataframe = pd.read_csv(full_path)
    print(f"Converted {csv_file} ")
    all_data.append(dataframe)

    move_t11 = pd.concat(all_data)
    move_t11.to_pickle('move_t11.pkl')


#### 유동인구 셀단위집계

move_t1_202405 = pd.read_csv('C:\\rawdata\\A28\\T1_GG_50CELL_FLOWPOP_202405_4111.csv', delimiter = ',')
move_t3_202405 = pd.read_csv('C:\\rawdata\\A28\\T3_GG_50CELL_LIVEPOP_202405_4111.csv', delimiter = ',')

move_t1_202405.to_pickle('move_t1_202405.pkl')
move_t3_202405.to_pickle('move_t3_202405.pkl')



## 동이름, 시군구 이름 데이터
filenm = os.path.join(datadir, 'sgg_hjd.xlsx')
dong_cd = pd.read_excel(filenm, dtype=str)

## 카드격자별, 동이름, 시군구 이름 데이터
filenm = os.path.join(datadir, 'card_cd.xlsx')
card_cd = pd.read_excel(filenm, dtype=str)

## 주차장 공급 데이터
filenm = os.path.join(datadir, '수원시_기초구역별_주차장공급분석(구분).xlsx')
park_cnt = pd.read_excel(filenm)
park_cnt['주차장'] = park_cnt['노상'] + park_cnt['노외'] + park_cnt['부설']


##################################################################

## 현황 분석 : 카드 데이터 분석하여 구역ID 특징 생성. 지역/업종 현황분석 최소화

## 개요1 : 월별 카드사용금액, 지역별 카드사용금액, 업종별 카드사용금액
## 동별 특성 : 카드사용액 많고/적음,
## 동별/업종별 카드사용액 특징 : 동별 카드사용액금액 비율로 업종별 카드사용액금액비율 나누기..

## 업종별 vs. 시간대별 특징, 주중/주말 특징
## 동별 vs. 시간대별 특징, 주중/주말 특징

## 업종별 vs. 연령대별 특징
## 동별 vs. 연령대별 특징

amt_list = ['202301', '202302', '202303', '202304', '202305', '202306', '202307', '202308', '202309', '202310', '202311',
             '202312', '202401', '202402', '202403', '202404', '202405']

card_sum = pd.DataFrame()
for amtnm in (amt_list):
    pickle_file = 'card_' + amtnm + '.pkl'
    base_amt = pd.read_pickle(pickle_file)
    amtsum = base_amt.groupby(['ta_ymd','admi_cty_no','card_tpbuz_nm_1', 'card_tpbuz_nm_2'])['amt'].sum().reset_index()
    card_sum = pd.concat([card_sum, amtsum], axis = 0 )

card_sum_ymd = card_sum
card_sum_ymd.to_pickle('card_sum_ymd.pkl')

card_sum_ymd = pd.read_pickle('card_sum_ymd.pkl')

## 카드 블럭별, 업종별 금액 합계

card_blksum = pd.DataFrame()
for amtnm in (amt_list):
    pickle_file = 'card_' + amtnm + '.pkl'
    base_amt = pd.read_pickle(pickle_file)
    amtsum = base_amt.groupby(['ta_ymd', 'blk_cd','card_tpbuz_nm_1', 'card_tpbuz_nm_2'])['amt'].sum().reset_index()
    card_blksum = pd.concat([card_blksum, amtsum], axis = 0 )

card_blksum.to_pickle('card_blksum.pkl')
card_blksum = pd.read_pickle('card_blksum.pkl')

card_blksum2 = card_blksum.groupby(['blk_cd','card_tpbuz_nm_1', 'card_tpbuz_nm_2'])['amt'].sum().reset_index()
card_blksum2['blk_cd'] = card_blksum2['blk_cd'].astype(str)
card_blksum2 = pd.merge(card_blksum2, card_cd, how = 'left', left_on = 'blk_cd', right_on = 'BLK_CD')

card_blksum2.to_pickle('card_blksum2.pkl')
card_blksum2 = pd.read_pickle('card_blksum2.pkl')

# 카드 데이터
card_sum_ymd['ym'] = card_sum_ymd['ta_ymd'].astype(str).str[:6]
card_sum = card_sum_ymd.groupby(['ym','admi_cty_no','card_tpbuz_nm_1', 'card_tpbuz_nm_2'])['amt'].sum().reset_index()

## 현황분석 결과 생성

# 월별 카드사용 금액
aa10 = card_sum.groupby(['ym'])['amt'].sum().reset_index()
amt_tot = aa10['amt'].sum()

aa10.to_excel(os.path.join(outdir, 'a28_0805_월별카드총액.xlsx'))

# 업종 대분류 카드사용금액
aa12 = card_sum.groupby(['card_tpbuz_nm_1'])['amt'].sum().reset_index()
aa12.to_excel(os.path.join(outdir, 'a28_0805_업종대분류카드총액.xlsx'))

# 업종 중분류 카드사용금액
aa13 = card_sum.groupby(['card_tpbuz_nm_1', 'card_tpbuz_nm_2'])['amt'].sum().reset_index()
aa13.to_excel(os.path.join(outdir, 'a28_0805_업종중분류카드총액.xlsx'))

## 구별 금액
aa21 = card_blksum2.groupby(['SGG_NM'])['amt'].sum().reset_index()
aa21.to_excel(os.path.join(outdir, 'a28_0805_구별카드총액.xlsx'))

## 구별, 업종대분류별 금액
aa22 = card_blksum2.groupby(['SGG_NM', 'card_tpbuz_nm_1'])['amt'].sum().reset_index()
aa22.to_excel(os.path.join(outdir, 'a28_0805_구별업종별카드총액.xlsx'))

## 동별 금액
aa23 = card_blksum2.groupby(['SGG_NM', 'HJD_NM'])['amt'].sum().reset_index()
aa23.to_excel(os.path.join(outdir, 'a28_0805_동별카드총액.xlsx'))
## 동별, 업종대분류별 금액
aa24 = card_blksum2.groupby(['SGG_NM', 'HJD_NM', 'card_tpbuz_nm_1'])['amt'].sum().reset_index()
aa24.to_excel(os.path.join(outdir, 'a28_0805_동별업종별카드총액.xlsx'))

## 기초구역 금액
aa25 = card_blksum2.groupby(['SGG_NM', 'HJD_NM', '기초구역번호'])['amt'].sum().reset_index()
aa25.to_excel(os.path.join(outdir, 'a28_0805_기초구역카드총액.xlsx'))

aa25.columns = ['SGG_NM', 'HJD_NM', '기초구역번호', '카드총액']

## 기초구역별 업종별 금액
area_amt = card_blksum2.groupby(['SGG_NM', 'HJD_NM', '기초구역번호', 'card_tpbuz_nm_1'])['amt'].sum().reset_index()
area_amt['업종'] = area_amt['card_tpbuz_nm_1'].str[:2]
area_amt2 = area_amt.pivot(index=['SGG_NM', 'HJD_NM', '기초구역번호'], columns='업종', values='amt').reset_index()
area_amt2 = area_amt2.fillna(0)
area_amt2 = pd.merge(area_amt2, aa25, how = 'left', on = ['SGG_NM', 'HJD_NM', '기초구역번호'])
park_cnt['기초구역번호'] = park_cnt['기초구역번호'].astype('str')
area_amt3 = pd.merge(area_amt2, park_cnt, how = 'left', on = ['SGG_NM', 'HJD_NM', '기초구역번호'])
area_amt3.to_pickle('card_blkamt.pkl')



#################################################################

## 상관관계 분석
from scipy.stats import pearsonr
correlation_coefficient, p_value =  pearsonr(area_amt3['카드총액'], area_amt3['주차장'])
print(f"Pearson 상관계수: {correlation_coefficient, p_value}")

correlation_coefficient, p_value =  pearsonr(area_amt3['소매'], area_amt3['주차장'])
print(f"Pearson 상관계수: 소매 {correlation_coefficient, p_value}")

correlation_coefficient, p_value =  pearsonr(area_amt3['음식'], area_amt3['주차장'])
print(f"Pearson 상관계수: 음식 {correlation_coefficient, p_value}")

correlation_coefficient, p_value =  pearsonr(area_amt3['의료'], area_amt3['주차장'])
print(f"Pearson 상관계수: 의료 {correlation_coefficient, p_value}")

correlation_coefficient, p_value =  pearsonr(area_amt3['학문'], area_amt3['주차장'])
print(f"Pearson 상관계수: 학문 {correlation_coefficient, p_value}")

## 업종 비율로 환산 상관관계 분석
area_amt3['소매비율'] =  (area_amt3['소매']/area_amt3['카드총액'])*100
area_amt3['음식비율'] =  (area_amt3['음식']/area_amt3['카드총액'])*100
area_amt3['의료비율'] =  (area_amt3['의료']/area_amt3['카드총액'])*100
area_amt3['학문비율'] =  (area_amt3['학문']/area_amt3['카드총액'])*100

correlation_coefficient, p_value =  pearsonr(area_amt3['소매비율'], area_amt3['주차장'])
print(f"Pearson 상관계수: 소매 {correlation_coefficient, p_value}")

correlation_coefficient, p_value =  pearsonr(area_amt3['음식비율'], area_amt3['주차장'])
print(f"Pearson 상관계수: 음식 {correlation_coefficient, p_value}")

correlation_coefficient, p_value =  pearsonr(area_amt3['의료비율'], area_amt3['주차장'])
print(f"Pearson 상관계수: 의료 {correlation_coefficient, p_value}")

correlation_coefficient, p_value =  pearsonr(area_amt3['학문비율'], area_amt3['주차장'])
print(f"Pearson 상관계수: 학문 {correlation_coefficient, p_value}")


## scatter plot

plt.scatter(area_amt3['카드총액'], area_amt3['주차장'])
sns.regplot(x='카드총액', y='주차장', data=area_amt3, line_kws={'color': 'red'})
plt.show()




#################################################################
## 행정동 클러스터링  ##

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA

## 카드사용금액 클러스터링 데이터 생성
cldata = aa24  # 행정동별, 업종별, 금액
cldata['업종'] = cldata['card_tpbuz_nm_1'].str[:2]
cldata2 = cldata.pivot(index=['SGG_NM', 'HJD_NM'], columns='업종', values='amt').reset_index()
cldata3 = cldata2[['생활', '소매', '여가', '음식', '의료', '학문']]

# 군집분석 항목 탐색 : 각 동별 편차가 심한 항목
cldata4 = cldata2[['HJD_NM', '생활', '소매', '여가', '음식', '의료', '학문']]
cldata4['totamt'] = cldata4['생활']+cldata4['소매']+cldata4['여가']+cldata4['음식']+cldata4['의료']+cldata4['학문']
cldata4['생활2'] = round((cldata4['생활']/cldata4['totamt'])*100, 1)
cldata4['소매2'] = round((cldata4['소매']/cldata4['totamt'])*100, 1)
cldata4['여가2'] = round((cldata4['여가']/cldata4['totamt'])*100, 1)
cldata4['음식2'] = round((cldata4['음식']/cldata4['totamt'])*100, 1)
cldata4['의료2'] = round((cldata4['의료']/cldata4['totamt'])*100, 1)
cldata4['학문2'] = round((cldata4['학문']/cldata4['totamt'])*100, 1)
cldata5 = cldata4[['생활2', '소매2', '여가2', '음식2', '의료2', '학문2']]
cldata6 = cldata4[[ '소매2', '음식2', '의료2', '학문2']]

plt.figure(figsize=(10, 6))
cldata5.boxplot()
plt.show()

cldata5.describe()



# 1. 변수값 표준화
scaler = StandardScaler()
df = cldata6
scaled_data = scaler.fit_transform(df)

## 군집분석 변수 찾기
import matplotlib.pyplot as plt

# scaled_data를 DataFrame으로 변환
scaled_df = pd.DataFrame(scaled_data, columns=df.columns)

# 3. K-평균 클러스터링 모델 생성 및 학습
kmeans = KMeans(n_clusters=4, random_state=0)
kmeans.fit(scaled_data)

# 4. 클러스터 센터 및 예측된 클러스터
centers = kmeans.cluster_centers_
labels = kmeans.labels_

# 5. 결과를 원래 데이터프레임에 추가
cldata4['Cluster'] = labels

## 클러스터별 관측치갯수, 항목 평균값
cl_stat = cldata4.groupby('Cluster')[['소매2', '음식2', '의료2', '학문2']].mean().reset_index()
cl_stat2 = cldata4.groupby('Cluster').size().reset_index()

## 클러스터별 관측치갯수, 항목 평균값
cl_stat2.columns = ['Cluster', 'Size']
cl_stat3 = pd.merge(cl_stat, cl_stat2, how = 'left', on = 'Cluster')
cl_stat3.to_excel(os.path.join(outdir, 'a28_0807_클러스터링결과.xlsx'))

cldata4.to_excel(os.path.join(outdir, 'a28_0808_클러스터링결과행정동.xlsx'))

## 클러스터 프로파일링
cl_var = ['생활', '소매', '여가', '음식', '의료', '학문', 'totamt', '생활2', '소매2',
       '여가2', '음식2', '의료2', '학문2']
cl_stat4 = cldata4.groupby('Cluster')[cl_var].mean().reset_index()
cl_stat4.to_excel(os.path.join(outdir, 'a28_0808_클러스터특성.xlsx'))

## 클러스터별 주차장 정보 확인
park_dong = park_cnt.groupby('HJD_NM')['주차장'].sum().reset_index()
cldata5 = pd.merge(cldata4, park_dong, how = 'left', on = 'HJD_NM')

aa31 = cldata5.groupby('Cluster')['주차장'].mean().reset_index()

## 행정동 카드사용금액 vs. 주차장수 상관관계 분석

plt.scatter(cldata5['totamt'], cldata5['주차장'])
sns.regplot(x='totamt', y='주차장', data=cldata5, line_kws={'color': 'red'})
plt.show()

correlation_coefficient, p_value =  pearsonr(cldata5['totamt'], cldata5['주차장'])
print(f"Pearson 상관계수: 총액 {correlation_coefficient, p_value}")

correlation_coefficient, p_value =  pearsonr(cldata5['소매'], cldata5['주차장'])
print(f"Pearson 상관계수: 소매 {correlation_coefficient, p_value}")

correlation_coefficient, p_value =  pearsonr(cldata5['음식'], cldata5['주차장'])
print(f"Pearson 상관계수: 음식 {correlation_coefficient, p_value}")

correlation_coefficient, p_value =  pearsonr(cldata5['의료'], cldata5['주차장'])
print(f"Pearson 상관계수: 의료 {correlation_coefficient, p_value}")

correlation_coefficient, p_value =  pearsonr(cldata5['학문'], cldata5['주차장'])
print(f"Pearson 상관계수: 학문 {correlation_coefficient, p_value}")

## 업종비율
correlation_coefficient, p_value =  pearsonr(cldata5['소매2'], cldata5['주차장'])
print(f"Pearson 상관계수: 소매 {correlation_coefficient, p_value}")

correlation_coefficient, p_value =  pearsonr(cldata5['음식2'], cldata5['주차장'])
print(f"Pearson 상관계수: 음식 {correlation_coefficient, p_value}")

correlation_coefficient, p_value =  pearsonr(cldata5['의료2'], cldata5['주차장'])
print(f"Pearson 상관계수: 의료 {correlation_coefficient, p_value}")

correlation_coefficient, p_value =  pearsonr(cldata5['학문2'], cldata5['주차장'])
print(f"Pearson 상관계수: 학문 {correlation_coefficient, p_value}")


cldata5.columns

## 행정동 업종별금액비율 vs. 주차장수 상관관계 분석



# 7. 최적의 클러스터 수 찾기 (엘보우 방법)
sum_of_squared_distances = []
K = range(1, 10)
for k in K:
    km = KMeans(n_clusters=k, random_state=0)
    km = km.fit(scaled_data)
    sum_of_squared_distances.append(km.inertia_)

plt.plot(K, sum_of_squared_distances, 'bx-')
plt.xlabel('k')
plt.ylabel('Sum of squared distances')
plt.title('Elbow Method For Optimal k')
plt.show()




# 6. PCA를 사용하여 2차원으로 축소 및 클러스터 결과 시각화
pca = PCA(n_components=2)
pca_components = pca.fit_transform(scaled_data)
pca_df = pd.DataFrame(data=pca_components, columns=['PCA1', 'PCA2'])
pca_df['Cluster'] = labels

plt.figure(figsize=(10, 6))
plt.scatter(pca_df['PCA1'], pca_df['PCA2'], c=pca_df['Cluster'], cmap='viridis', s=50)
plt.scatter(centers[:, 0], centers[:, 1], c='red', s=200, alpha=0.75)
plt.title('K-Means Clustering Results (PCA)')
plt.xlabel('PCA1')
plt.ylabel('PCA2')
plt.show()

# 7. 최적의 클러스터 수 찾기 (엘보우 방법)
sum_of_squared_distances = []
K = range(1, 10)
for k in K:
    km = KMeans(n_clusters=k, random_state=0)
    km = km.fit(scaled_data)
    sum_of_squared_distances.append(km.inertia_)

plt.plot(K, sum_of_squared_distances, 'bx-')
plt.xlabel('k')
plt.ylabel('Sum of squared distances')
plt.title('Elbow Method For Optimal k')
plt.show()


######################################################################

# 2. 클러스터별 최소 3개의 중심점으로 시작
def fit_kmeans_with_min_samples(data, n_clusters, min_samples_per_cluster, max_iter=100):
    for i in range(max_iter):
        kmeans = KMeans(n_clusters=n_clusters, random_state=i)
        kmeans.fit(data)
        labels = kmeans.labels_
        cluster_counts = np.bincount(labels)

        if np.all(cluster_counts >= min_samples_per_cluster):
            return kmeans

    raise ValueError(
        f"Could not fit KMeans with each cluster having at least {min_samples_per_cluster} samples in {max_iter} iterations")


# K-평균 클러스터링 모델 생성 및 학습
n_clusters = 4
min_samples_per_cluster = 3

kmeans = fit_kmeans_with_min_samples(scaled_data, n_clusters, min_samples_per_cluster)
centers = kmeans.cluster_centers_
labels = kmeans.labels_

# 5. 결과를 원래 데이터프레임에 추가
cldata2['Cluster'] = labels

## 클러스터별 관측치갯수, 항목 평균값
cl_stat = cldata2.groupby('Cluster')[['생활', '소매', '여가', '음식', '의료', '학문']].mean().reset_index()
cl_stat2 = cldata2.groupby('Cluster').size().reset_index()
cl_stat2.columns = ['Cluster', 'Size']
cl_stat3 = pd.merge(cl_stat, cl_stat2, how = 'left', on = 'Cluster')
cl_stat3.to_excel(os.path.join(outdir, 'a28_0807_클러스터링결과.xlsx'))


# 6. 최적의 클러스터 수 찾기 (엘보우 방법)
sum_of_squared_distances = []
K = range(1, 10)
for k in K:
    try:
        km = fit_kmeans_with_min_samples(scaled_data, k, min_samples_per_cluster)
        sum_of_squared_distances.append(km.inertia_)
    except ValueError:
        sum_of_squared_distances.append(None)

# 유효한 클러스터 수만 시각화
valid_K = [k for k, ssd in zip(K, sum_of_squared_distances) if ssd is not None]
valid_ssd = [ssd for ssd in sum_of_squared_distances if ssd is not None]

plt.plot(valid_K, valid_ssd, 'bx-')
plt.xlabel('k')
plt.ylabel('Sum of squared distances')
plt.title('Elbow Method For Optimal k')
plt.show()


################################################################

## 유동인구 교통수단 데이터 분석

move_t7 = pd.read_pickle('move_t7.pkl')

## 구별 유입인구 분석
move_t7['ETL_YMD'] = move_t7['ETL_YMD'].astype(str)
move_t7s = move_t7[move_t7['ETL_YMD'].str[:6] == '202405']

move_t7['ETL_YMD'].head()
move_t7.columns

# 구별 일자별 방문인구수 합계
aa10 = move_t7s.groupby(['ETL_YMD', 'D_CTY_NM'])['CNT'].sum().reset_index()

# 구별 일평균 방문인구수 합계
aa101 = aa10.groupby(['D_CTY_NM'])['CNT'].mean().reset_index()
aa101.to_excel(os.path.join(outdir, 'a28_0812_구별방문인구수평균.xlsx'))

# 일별 방문인구수 합계
aa11 = move_t7s.groupby(['ETL_YMD'])['CNT'].sum().reset_index()
aa11.to_excel(os.path.join(outdir, 'a28_0812_일자별방문인구수.xlsx'))

## 교통수단별 방문인구수 합계
aa12 = move_t7s.groupby(['TRANS_GB'])['CNT'].sum().reset_index()
aa12['cnt_day'] = aa12['CNT']/31
aa12.to_excel(os.path.join(outdir, 'a28_0812_교통수단별방문인구수.xlsx'))

## 교통수단별 방문인구수 합계
aa13 = move_t7s.groupby(['ETL_YMD','TRANS_GB'])['CNT'].sum().reset_index()
aa13.to_excel(os.path.join(outdir, 'a28_0812_일자별교통수단별방문인구수.xlsx'))

## 교통수단별/구별 방문인구수 합계
aa14 = move_t7s.groupby(['TRANS_GB', 'D_CTY_NM' ])['CNT'].sum().reset_index()
aa14['cnt_day'] = aa14['CNT']/31
aa14.to_excel(os.path.join(outdir, 'a28_0812_교통수단별구별방문인구수.xlsx'))

## 월별 구별 차량 방문인구수 추이 : 월별일별 차량방문인구, 일평균환산

aa15 = move_t7[move_t7['TRANS_GB'] == 0]
aa15['mm'] = aa15['ETL_YMD'].str[:6]
aa151 = aa15.groupby(['mm', 'ETL_YMD','D_CTY_NM'])['CNT'].sum().reset_index()
aa152 = aa151.groupby(['mm', 'D_CTY_NM'])['CNT'].mean().reset_index()
aa153 = aa152.pivot(index='mm', columns='D_CTY_NM', values='CNT').reset_index()
aa153.to_excel(os.path.join(outdir, 'a28_0812_교통수단별구별월별방문인구수.xlsx'))

## 동별 차량 방문인구 추이

aa154 = aa15.groupby(['mm', 'ETL_YMD','D_CTY_NM', 'D_ADMI_NM' ])['CNT'].sum().reset_index()
aa155 = aa154.groupby(['mm', 'D_CTY_NM', 'D_ADMI_NM'])['CNT'].mean().reset_index()
aa156 = aa155.pivot(index=['D_CTY_NM', 'D_ADMI_NM'], columns='mm', values='CNT').reset_index()
aa156.to_excel(os.path.join(outdir, 'a28_0812_교통수단별동별월별방문인구수.xlsx'))

## 차량 유입 시간대 분석
move_t7_car_202405 = move_t7s[move_t7s['TRANS_GB'] == 0]
t7_car_2405 = move_t7_car_202405.groupby(['ETL_YMD', 'D_MEGA_NM', 'D_CTY_NM', 'D_ADMI_NM', 'D_TIME_CD'])['CNT'].sum().reset_index()
weeklist = ['04','05','06', '11','12', '15', '18', '19', '25', '26']

t7_car_2405['week_yn'] = np.where(t7_car_2405['ETL_YMD'].str[6:8].isin(weeklist), '1', '0')
t7_car_2405['dd'] = t7_car_2405['ETL_YMD'].str[6:8]

aa16 = t7_car_2405.groupby(['week_yn', 'D_TIME_CD'])['CNT'].mean().reset_index()
aa16.to_excel(os.path.join(outdir, 'a28_0812_교통수단별시간대별인구수.xlsx'))

aa161 = t7_car_2405.groupby(['D_CTY_NM', 'week_yn', 'D_TIME_CD'])['CNT'].mean().reset_index()
aa161.to_excel(os.path.join(outdir, 'a28_0812_교통수단별시간대별구별인구수.xlsx'))

# 평일 추출
aa17 = t7_car_2405[t7_car_2405['week_yn'] == '0']
aa171 = aa17.groupby(['D_ADMI_NM', 'D_TIME_CD'])['CNT'].mean().reset_index()
## 출근시간대 합계
aa172 = aa171[(aa171['D_TIME_CD']==7)|(aa171['D_TIME_CD']==8)]
aa173 = aa172.groupby(['D_ADMI_NM'])['CNT'].mean().reset_index()
aa173.to_excel(os.path.join(outdir, 'a28_0812_교통수단별출근시간대동별.xlsx'))


## 퇴근시간대 합계
aa174 = aa171[aa171['D_TIME_CD'].isin([17,18,19])]
aa175 = aa174.groupby(['D_ADMI_NM'])['CNT'].mean().reset_index()
aa175.to_excel(os.path.join(outdir, 'a28_0812_교통수단별퇴근시간대동별.xlsx'))

## 샘플 매탄3동
aa176 = aa171[aa171['D_ADMI_NM'] == '매탄3동']



aa161.to_excel(os.path.join(outdir, 'a28_0812_교통수단별시간대별구별인구수.xlsx'))


####################################################################################
################################################################

## 유동인구 차량유출 교통수단 데이터 분석

move_t11 = pd.read_pickle('move_t11.pkl')

## 구별 유입인구 분석
move_t11['ETL_YMD'] = move_t11['ETL_YMD'].astype(str)
move_t11s = move_t11[move_t11['ETL_YMD'].str[:6] == '202405']

move_t11['ETL_YMD'].head()
move_t11.columns

# 구별 일자별 방문인구수 합계
aa10 = move_t11s.groupby(['ETL_YMD', 'O_CTY_NM'])['CNT'].sum().reset_index()

# 구별 일평균 방문인구수 합계
aa101 = aa10.groupby(['O_CTY_NM'])['CNT'].mean().reset_index()
aa101.to_excel(os.path.join(outdir, 'a28_0830_구별유출인구수평균.xlsx'))

# 일별 유출인구수 합계
aa11 = move_t11s.groupby(['ETL_YMD'])['CNT'].sum().reset_index()
aa11.to_excel(os.path.join(outdir, 'a28_0830_일자별유출인구수.xlsx'))

## 교통수단별 유출인구수 합계
aa12 = move_t11s.groupby(['TRANS_GB'])['CNT'].sum().reset_index()
aa12['cnt_day'] = aa12['CNT']/31
aa12.to_excel(os.path.join(outdir, 'a28_0830_교통수단별유출인구수.xlsx'))

## 교통수단별 유출인구수 합계
aa13 = move_t11s.groupby(['ETL_YMD','TRANS_GB'])['CNT'].sum().reset_index()
aa13.to_excel(os.path.join(outdir, 'a28_0830_일자별교통수단별유출인구수.xlsx'))

## 교통수단별/구별 유출인구수 합계
aa14 = move_t11s.groupby(['TRANS_GB', 'O_CTY_NM' ])['CNT'].sum().reset_index()
aa14['cnt_day'] = aa14['CNT']/31
aa14.to_excel(os.path.join(outdir, 'a28_0830_교통수단별구별유출인구수.xlsx'))

## 월별 구별 차량 유출인구수 추이 : 월별일별 차량유출인구, 일평균환산

aa15 = move_t11[move_t11['TRANS_GB'] == 0]
aa15['mm'] = aa15['ETL_YMD'].str[:6]
aa151 = aa15.groupby(['mm', 'ETL_YMD','O_CTY_NM'])['CNT'].sum().reset_index()
aa152 = aa151.groupby(['mm', 'O_CTY_NM'])['CNT'].mean().reset_index()
aa153 = aa152.pivot(index='mm', columns='O_CTY_NM', values='CNT').reset_index()
aa153.to_excel(os.path.join(outdir, 'a28_0830_교통수단별구별월별유출인구수.xlsx'))

## 동별 차량 유출인구 추이

aa154 = aa15.groupby(['mm', 'ETL_YMD','O_CTY_NM', 'O_ADMI_NM' ])['CNT'].sum().reset_index()
aa155 = aa154.groupby(['mm', 'O_CTY_NM', 'O_ADMI_NM'])['CNT'].mean().reset_index()
aa156 = aa155.pivot(index=['O_CTY_NM', 'O_ADMI_NM'], columns='mm', values='CNT').reset_index()
aa156.to_excel(os.path.join(outdir, 'a28_0830_교통수단별동별월별유출인구수.xlsx'))

## 차량 유출 시간대 분석
move_t11_car_202405 = move_t11s[move_t11s['TRANS_GB'] == 0]
t11_car_2405 = move_t11_car_202405.groupby(['ETL_YMD', 'O_MEGA_NM', 'O_CTY_NM', 'O_ADMI_NM', 'O_TIME_CD'])['CNT'].sum().reset_index()
weeklist = ['04','05','06', '11','12', '15', '18', '19', '25', '26']

t11_car_2405['week_yn'] = np.where(t11_car_2405['ETL_YMD'].str[6:8].isin(weeklist), '1', '0')
t11_car_2405['dd'] = t11_car_2405['ETL_YMD'].str[6:8]

aa16 = t11_car_2405.groupby(['week_yn', 'O_TIME_CD'])['CNT'].mean().reset_index()
aa16.to_excel(os.path.join(outdir, 'a28_0830_교통수단별시간대별인구수.xlsx'))

aa161 = t11_car_2405.groupby(['O_CTY_NM', 'week_yn', 'O_TIME_CD'])['CNT'].mean().reset_index()
aa161.to_excel(os.path.join(outdir, 'a28_0830_교통수단별시간대별구별인구수.xlsx'))

# 평일 추출
aa17 = t11_car_2405[t11_car_2405['week_yn'] == '0']
aa171 = aa17.groupby(['O_ADMI_NM', 'O_TIME_CD'])['CNT'].mean().reset_index()
## 출근시간대 합계
aa172 = aa171[(aa171['O_TIME_CD']==7)|(aa171['O_TIME_CD']==8)]
aa173 = aa172.groupby(['O_ADMI_NM'])['CNT'].mean().reset_index()
aa173.to_excel(os.path.join(outdir, 'a28_0830_교통수단별출근시간대동별.xlsx'))


## 퇴근시간대 합계
aa174 = aa171[aa171['O_TIME_CD'].isin([17,18,19])]
aa175 = aa174.groupby(['O_ADMI_NM'])['CNT'].mean().reset_index()
aa175.to_excel(os.path.join(outdir, 'a28_0830_교통수단별퇴근시간대동별.xlsx'))

## 샘플 매탄3동
aa176 = aa171[aa171['O_ADMI_NM'] == '매탄3동']


## 차량이동차량 출발지, 목적지 분석 : 외부 vs. 수원시   #################################

move_202301 = pd.read_pickle('move_202301.pkl')
move_202302 = pd.read_pickle('move_202302.pkl')
move_202303 = pd.read_pickle('move_202303.pkl')
move_202304 = pd.read_pickle('move_202304.pkl')
move_202305 = pd.read_pickle('move_202305.pkl')
move_202306 = pd.read_pickle('move_202306.pkl')
move_202307 = pd.read_pickle('move_202307.pkl')
move_202308 = pd.read_pickle('move_202308.pkl')
move_202309 = pd.read_pickle('move_202309.pkl')
move_202310 = pd.read_pickle('move_202310.pkl')
move_202311 = pd.read_pickle('move_202311.pkl')
move_202312 = pd.read_pickle('move_202312.pkl')
move_202401 = pd.read_pickle('move_202401.pkl')
move_202402 = pd.read_pickle('move_202402.pkl')
move_202403 = pd.read_pickle('move_202403.pkl')
move_202404 = pd.read_pickle('move_202404.pkl')
move_202405 = pd.read_pickle('move_202405.pkl')


move_list = [move_202301, move_202302, move_202303, move_202304, move_202305, move_202306,
             move_202307, move_202308, move_202309, move_202310, move_202311, move_202312,
             move_202401, move_202402, move_202403, move_202404, move_202405]
move_t15_car = pd.DataFrame()
for raw_file in (move_list):
    base_file = raw_file[raw_file['TRANS_GB'] == 0]
    base_file['ym'] = base_file['ETL_YMD'].astype(str).str[:6]
    base_file2 = base_file.groupby(['ym', 'O_MEGA_NM', 'O_CTY_NM', 'O_ADMI_NM', 'D_MEGA_NM', 'D_CTY_NM', 'D_ADMI_NM', 'SEX_CD', 'AGE_GRP'])['CNT'].sum().reset_index()
    move_t15_car = pd.concat([move_t15_car, base_file2], axis = 0 )

move_t15_car.to_pickle('move_t15_car.pkl')
move_t15_car = pd.read_pickle('move_t15_car.pkl')


move_t15_car['o_do'] = np.where(move_t15_car['O_CTY_NM'].isin(['수원시 권선구', '수원시 영통구', '수원시 장안구', '수원시 팔달구' ]),
                           '수원시', move_t15_car['O_MEGA_NM'])
move_t15_car['d_do'] = np.where(move_t15_car['D_CTY_NM'].isin(['수원시 권선구', '수원시 영통구', '수원시 장안구', '수원시 팔달구' ]),
                           '수원시', move_t15_car['D_MEGA_NM'])
bb11 = move_t15_car.groupby(['o_do'])['CNT'].sum().reset_index()
bb11.to_excel(os.path.join(outdir, 'a28_0812_차량이동출발지역.xlsx'))

## 교차표 생성
bb111 = pd.crosstab(move_t15_car["o_do"], move_t15_car["d_do"], margins=True)
bb111.to_excel(os.path.join(outdir, 'a28_0812_차량이동출발지역도착지역.xlsx'))


## 데이터 검증 : 월별 sum

bb111 = move_t15_car.groupby(['ym'])['CNT'].sum().reset_index()
bb111.to_excel(os.path.join(outdir, 'a28_0812_차량이동출발월별건수.xlsx'))

move_t15_cars = move_t15_car.head(10000)

## 수원시 출발 건   :  총 517일
move_t15_01 = move_t15_car[move_t15_car['o_do'] == '수원시']
move_t15_01['d_suwon_cnt'] = np.where(move_t15_01['d_do'] == '수원시', move_t15_01['CNT'], 0)
move_t15_01['d_etc_cnt'] = np.where(move_t15_01['d_do'] == '수원시', 0, move_t15_01['CNT'])
bb12 = move_t15_01.groupby(['d_do'])['CNT'].sum().reset_index()
bb12.to_excel(os.path.join(outdir, 'a28_0812_차량수원출발_도착지역.xlsx'))

## 수원도착지 기준 출발지역
move_t15_02 = move_t15_car[move_t15_car['d_do'] == '수원시']
move_t15_02['o_suwon_cnt'] = np.where(move_t15_02['o_do'] == '수원시', move_t15_02['CNT'], 0)
move_t15_02['o_etc_cnt'] = np.where(move_t15_02['o_do'] == '수원시', 0, move_t15_02['CNT'])
bb13 = move_t15_02.groupby(['o_do'])['CNT'].sum().reset_index()
bb13.to_excel(os.path.join(outdir, 'a28_0812_수원도착_출발지역.xlsx'))

# 수원도착지 시군구 / 수원시, 기타지역
bb131 = move_t15_02.groupby(['D_CTY_NM'])['CNT'].sum().reset_index()
bb132 = move_t15_02.groupby(['D_CTY_NM'])['o_suwon_cnt'].sum().reset_index()
bb133 = move_t15_02.groupby(['D_CTY_NM'])['o_etc_cnt'].sum().reset_index()
bb134 = pd.merge(bb131, bb132, how = 'left', on = 'D_CTY_NM')
bb134 = pd.merge(bb134, bb133, how = 'left', on = 'D_CTY_NM')
bb134.to_excel(os.path.join(outdir, 'a28_0812_수원도착_출발지역_구.xlsx'))

## 행정동. 수원출발 도착지 구분 

bb135 = move_t15_02.groupby(['D_ADMI_NM'])['CNT'].sum().reset_index()
bb136 = move_t15_02.groupby(['D_ADMI_NM'])['o_suwon_cnt'].sum().reset_index()
bb137 = move_t15_02.groupby(['D_ADMI_NM'])['o_etc_cnt'].sum().reset_index()
bb138 = pd.merge(bb135, bb136, how = 'left', on = 'D_ADMI_NM')
bb138 = pd.merge(bb138, bb137, how = 'left', on = 'D_ADMI_NM')
bb138.to_excel(os.path.join(outdir, 'a28_0812_수원도착_출발지역_동.xlsx'))

# 수원출발지 시군구 / 도착 수원시, 기타지역
bb141 = move_t15_01.groupby(['O_CTY_NM'])['CNT'].sum().reset_index()
bb142 = move_t15_01.groupby(['O_CTY_NM'])['d_suwon_cnt'].sum().reset_index()
bb143 = move_t15_01.groupby(['O_CTY_NM'])['d_etc_cnt'].sum().reset_index()
bb144 = pd.merge(bb141, bb142, how = 'left', on = 'O_CTY_NM')
bb144 = pd.merge(bb144, bb143, how = 'left', on = 'O_CTY_NM')
bb144.to_excel(os.path.join(outdir, 'a28_0812_수원출발_출발지역_구.xlsx'))

## 행정동. 수원출발 도착지 구분 

bb145 = move_t15_01.groupby(['O_ADMI_NM'])['CNT'].sum().reset_index()
bb146 = move_t15_01.groupby(['O_ADMI_NM'])['d_suwon_cnt'].sum().reset_index()
bb147 = move_t15_01.groupby(['O_ADMI_NM'])['d_etc_cnt'].sum().reset_index()
bb148 = pd.merge(bb145, bb146, how = 'left', on = 'O_ADMI_NM')
bb148 = pd.merge(bb148, bb147, how = 'left', on = 'O_ADMI_NM')
bb148.to_excel(os.path.join(outdir, 'a28_0812_수원출발_출발지역_동.xlsx'))




## 차량 유입인구의 방문 목적  ###########################################################


## 차량이동차량 출발지, 목적지 분석 : 외부 vs. 수원시

move_t13_202301 = pd.read_pickle('move_t13__202301.pkl')
move_t13_202302 = pd.read_pickle('move_t13__202302.pkl')
move_t13_202303 = pd.read_pickle('move_t13__202303.pkl')
move_t13_202304 = pd.read_pickle('move_t13__202304.pkl')
move_t13_202305 = pd.read_pickle('move_t13__202305.pkl')
move_t13_202306 = pd.read_pickle('move_t13__202306.pkl')
move_t13_202307 = pd.read_pickle('move_t13__202307.pkl')
move_t13_202308 = pd.read_pickle('move_t13__202308.pkl')
move_t13_202309 = pd.read_pickle('move_t13__202309.pkl')
move_t13_202310 = pd.read_pickle('move_t13__202310.pkl')
move_t13_202311 = pd.read_pickle('move_t13__202311.pkl')
move_t13_202312 = pd.read_pickle('move_t13__202312.pkl')
move_t13_202401 = pd.read_pickle('move_t13__202401.pkl')
move_t13_202402 = pd.read_pickle('move_t13__202402.pkl')
move_t13_202403 = pd.read_pickle('move_t13__202403.pkl')
move_t13_202404 = pd.read_pickle('move_t13__202404.pkl')
move_t13_202405 = pd.read_pickle('move_t13__202405.pkl')


move_list = [move_t13_202301, move_t13_202302, move_t13_202303, move_t13_202304, move_t13_202305, move_t13_202306,
             move_t13_202307, move_t13_202308, move_t13_202309, move_t13_202310, move_t13_202311, move_t13_202312,
             move_t13_202401, move_t13_202402, move_t13_202403, move_t13_202404, move_t13_202405]
move_t13_car = pd.DataFrame()
for raw_file in (move_list):
    # base_file = raw_file[raw_file['TRANS_GB'] == 0]   T13 테이블은 차량 구분정보 없음
    base_file = raw_file
    base_file['ym'] = base_file['ETL_YMD'].astype(str).str[:6]
    base_file2 = base_file.groupby(['ym', 'O_MEGA_NM', 'O_CTY_NM', 'O_ADMI_NM', 'D_MEGA_NM', 'D_CTY_NM', 'D_ADMI_NM', 'PURPOSE', 'SEX_CD', 'AGE_GRP'])['CNT'].sum().reset_index()
    move_t13_car = pd.concat([move_t13_car, base_file2], axis = 0 )

move_t13_car.to_pickle('move_t13_car.pkl')
move_t13_car = pd.read_pickle('move_t13_car.pkl')


move_t13_car['o_do'] = np.where(move_t13_car['O_CTY_NM'].isin(['수원시 권선구', '수원시 영통구', '수원시 장안구', '수원시 팔달구' ]),
                           '수원시', move_t13_car['O_MEGA_NM'])
move_t13_car['d_do'] = np.where(move_t13_car['D_CTY_NM'].isin(['수원시 권선구', '수원시 영통구', '수원시 장안구', '수원시 팔달구' ]),
                           '수원시', move_t13_car['D_MEGA_NM'])


## 수원도착지 기준 출발지역
move_t13_02 = move_t13_car[move_t13_car['d_do'] == '수원시']
move_t13_02['o_suwon_cnt'] = np.where(move_t13_02['o_do'] == '수원시', move_t13_02['CNT'], 0)
move_t13_02['o_etc_cnt'] = np.where(move_t13_02['o_do'] == '수원시', 0, move_t13_02['CNT'])

aa10 = move_t13_02.groupby(['PURPOSE'])['CNT'].sum().reset_index()   # 수원 도착 차량 목적 count
aa101 = move_t13_02.groupby(['PURPOSE'])['o_suwon_cnt'].sum().reset_index()   # 수원 도착 수원출발 차량 목적 count
aa102 = move_t13_02.groupby(['PURPOSE'])['o_etc_cnt'].sum().reset_index()   # 수원 도착 외부출발 차량 목적 count

aa10.to_excel(os.path.join(outdir, 'a28_0819_차량유입_목적.xlsx'))
aa101.to_excel(os.path.join(outdir, 'a28_0819_차량유입_목적_수원출발.xlsx'))
aa102.to_excel(os.path.join(outdir, 'a28_0819_차량유입_목적_외부출발.xlsx'))

## 수원시 출발 건   :  총 517일
move_t13_01 = move_t13_car[move_t13_car['o_do'] == '수원시']
move_t13_01['d_suwon_cnt'] = np.where(move_t13_01['d_do'] == '수원시', move_t13_01['CNT'], 0)
move_t13_01['d_etc_cnt'] = np.where(move_t13_01['d_do'] == '수원시', 0, move_t13_01['CNT'])
bb12 = move_t13_01.groupby(['d_do'])['CNT'].sum().reset_index()
bb12.to_excel(os.path.join(outdir, 'a28_0812_차량수원출발_도착지역.xlsx'))

## 수원출발 기타지역 도착
move_t15_03 = move_t15_car[(move_t15_car['o_do'] == '수원시')&(move_t15_car['d_do'] != '수원시')]
bb14 = move_t15_03.groupby(['d_do'])['CNT'].sum().reset_index()
bb14.to_excel(os.path.join(outdir, 'a28_0812_수원출발_도착지역.xlsx'))


######################################################

## 건축물 대장 표제부 검증

docu_head = pd.read_pickle('건축물대장_총괄표제부_0827.pkl')
docu_unit = pd.read_pickle('건축물대장_표제부_0827(연면적).pkl')

docu_tot = pd.read_pickle('최종_건축물대장주차장_0827.pkl')

docu_key1 =  docu_head[['시군구', '대지위치', '건물명']]
docu_key2 =  docu_unit[['시군구', '대지위치', '건물명']]
docu_key = pd.concat([docu_key1, docu_key2], axis=0)

#1. 총괄표제부 중복제거
  #1.1 총괄표제부 중복현환
a10 = docu_head.groupby(['시군구', '대지위치', '건물명']).size().reset_index()
a11 = docu_head.groupby(['시군구', '대지위치', '건물명'])['총주차수'].sum().reset_index()
a13 = pd.merge(a10, a11, how = 'left', on = ['시군구', '대지위치', '건물명'])
a14 = docu_head[docu_head['건물명'] == '칠보초등학교']   # 중복 1건. 칠보초등학교. 주용도코드가 2가지며 총주차수는 동일하게 30.
a15 = docu_head.groupby(['시군구', '대지위치', '건물명'])['총주차수'].max().reset_index()

#2. 건축물대장 표제부 중복현황
a20 = docu_unit.groupby(['시군구', '대지위치', '건물명']).size().reset_index()
a20.columns = ['시군구', '대지위치', '건물명', '중복건수']
a21 = docu_unit.groupby(['시군구', '대지위치', '건물명'])['총주차수'].sum().reset_index()
a211 = docu_unit.groupby(['시군구', '대지위치', '건물명'])['총주차수'].max().reset_index()
a211.columns = ['시군구', '대지위치', '건물명', '최대주차장']
a23 = pd.merge(a20, a21, how = 'left', on = ['시군구', '대지위치', '건물명'])
a23 = pd.merge(a23, a211, how = 'left', on = ['시군구', '대지위치', '건물명'])
a231 = a23[(a23['총주차수'] > 0) & (a23['중복건수'] > 1)]

## 건축물대장 표제부 : 중복건수 2건 이상이며, 주차장수 있는 건수는  총 70건
  ## 총주차수와 최대주차수가 동일 (중복없음) : 31건

a231['type'] = np.where(a231['총주차수'] == a231['최대주차장'], 1, 0)
a231.groupby(['type']).size()

a232 = a231[a231['type'] == 0]
a232['rt'] = a231['총주차수']/a231['최대주차장']

## 총괄표제부 추가
a15.columns = ['시군구', '대지위치', '건물명', '총괄주차장수']
a24 = pd.merge(a232, a15, how = 'left', on = ['시군구', '대지위치', '건물명'])
a24['noinfo'] = np.where(a24['총괄주차장수'].isnull(),1,0 )
a241 = a24[a24['noinfo'] == 1]

# 주소기준 총괄표제부 붙이기
a151 = a15
a151.columns = ['시군구', '대지위치', '건물명_2', '총괄주차장수_2']
a242 = pd.merge(a241, a151, how = 'left', on = ['시군구', '대지위치'])

## 최종 총괄표제부 정보 부재
a25 = a242[a242['총괄주차장수_2'].isnull()]
a25.columns
a251 = a25[['시군구', '대지위치', '건물명', '중복건수', '총주차수', '최대주차장']]

a251 = pd.merge(a251, docu_unit, how = 'left', on = ['시군구', '대지위치', '건물명'])

## '권선삼성아파트'만 sum값 적용. 다른 건물은 모두 중복 의심. 비율이 2 또는 3 으로 나타나면 모두 중복

####### 건축물대장 표제부 1건과 총괄표제부 값 비교

b10 = a23[a23['중복건수'] == 1]
b11 = pd.merge(b10, a15, how = 'left', on = ['시군구', '대지위치', '건물명'])
b11['noinfo'] = np.where(b11['총괄주차장수'].isnull(),1,0 )
b12 = b11[b11['noinfo'] == 1]  #총괄주차장 정보없음 : 8741건 / 9404건 중

# 건물명 기준 총괄주차장 없는 건물 대상 '대지위치'로 정보 추가
a152 = a15
a152.columns = ['시군구', '대지위치', '건물명_2', '총괄주차장수_2']
b121 = pd.merge(b12, a152, how = 'left', on = ['시군구', '대지위치'])


b13 = b12[b12['총주차수'] == 0]  # 총 2502 건물의 주차장 0 으로 나타남




a1 = docu_key1.groupby(['시군구', '대지위치', '건물명']).size().reset_index()
a10 = docu_head[docu_head['건물명'] == '칠보초등학교']


a21 = docu_unit[docu_unit['건물명'] == '삼성미래기술캠퍼스']
a22 = docu_unit[docu_unit['건물명'] == '송학아파트']
a23 = docu_unit[docu_unit['건물명'] == '삼성전기(주)']
a24 = docu_unit[docu_unit['건물명'] == '아주대학교']
a25 = docu_unit[docu_unit['건물명'] == '경기대학교']



a11 = docu_head[docu_head['건물명'] == '삼성미래기술캠퍼스']
a12 = docu_head[docu_head['건물명'] == '송학아파트']
a13 = docu_head[docu_head['건물명'] == '삼성전기(주)']
a14 = docu_head[docu_head['건물명'] == '아주대학교']

a111 = docu_head[docu_head['대지위치'] == '경기도 수원시 영통구 매탄동 560번지']

#### 동일 주소에 다른 아파트 이름으로 많은 주차장수 중복 발생 --> 주소 기준으로 중복제거 및 조인
## 처음부터 다시

## 건축물 대장 표제부 검증

docu_head = pd.read_pickle('건축물대장_총괄표제부_0827.pkl')
docu_unit = pd.read_pickle('건축물대장_표제부_0827(연면적).pkl')
docu_tot = pd.read_pickle('최종_건축물대장주차장_0827.pkl')

######################################################################################
#1. 총괄표제부 중복제거
  #1.1 총괄표제부 중복현환
a10 = docu_head.groupby(['시군구', '대지위치']).size().reset_index()
a11 = docu_head.groupby(['시군구', '대지위치'])['총주차수'].sum().reset_index()
a13 = pd.merge(a10, a11, how = 'left', on = ['시군구', '대지위치'])
a14 = docu_head[docu_head['건물명'] == '칠보초등학교']   # 중복 1건. 칠보초등학교. 주용도코드가 2가지며 총주차수는 동일하게 30.
a15 = docu_head.groupby(['시군구', '대지위치'])['총주차수'].max().reset_index()
a15.columns = ['시군구', '대지위치','총괄주차장']

#2. 건축물대장 표제부 중복현황
a20 = docu_unit.groupby(['시군구', '대지위치']).size().reset_index()
a20.columns = ['시군구', '대지위치', '중복건수']
a21 = docu_unit.groupby(['시군구', '대지위치'])['총주차수'].sum().reset_index()
a211 = docu_unit.groupby(['시군구', '대지위치'])['총주차수'].max().reset_index()
a211.columns = ['시군구', '대지위치', '최대주차장']
a23 = pd.merge(a20, a21, how = 'left', on = ['시군구', '대지위치'])
a23 = pd.merge(a23, a211, how = 'left', on = ['시군구', '대지위치'])
a23.columns =  ['시군구', '대지위치', '중복건수', '총주차수합계', '최대주차장']
a231 = a23[(a23['총주차수합계'] > 0) & (a23['중복건수'] > 1)]

#3. 건축물대장 표제부에 총괄표제부 정보 추가 : 9145
a30 = pd.merge(a23, a15, how = 'left', on = ['시군구', '대지위치'])
a30 = a30.fillna(0)

#3.1==> 총괄표제부주차장 >0 인경우 최종주차장수산출
f01 = a30[a30['총괄주차장'] > 0 ]
f01['최종주차장수'] =  f01['총괄주차장']   #854건
f01 = f01[['시군구', '대지위치', '최종주차장수']]


#3.2 총괄표제부주차장수 >= 0   # 8,291건
a31 = a30[a30['총괄주차장'] <= 0 ]
a31['rt'] = a31['총주차수합계']/a31['최대주차장']
a31['dup_fix'] = np.where(a31['rt'].isin([1,2,3,4,5,6,7,8,9,10]), 1, 0)

#3.3 건축물대장주차장수 합계가 최댓값과 같거나, 정율배
f02 = a31[a31['dup_fix'] == 1]
f02['최종주차장수'] =  f02['최대주차장']   #6148건
f02 = f02[['시군구', '대지위치', '최종주차장수']]

#3.3 건축물대장주차장수 합계가 정율이 아닌 경우 : 2143
a32 = a31[a31['dup_fix'] == 0 ]

#3.4 건축물대장주차장수 합계가 0인 경우  : 2130
f03 = a32[a32['총주차수합계'] == 0 ]
f03['최종주차장수'] =  f03['총주차수합계']   #6148건
f03 = f03[['시군구', '대지위치', '최종주차장수']]

a33 = a32[a32['총주차수합계'] > 0 ]  # 13건

## 최빈값 산출하여 최빈값과 최댓값 비교 # 13건
a34 = pd.merge(a33, docu_unit, how = 'left', on = ['시군구', '대지위치'] )
a35 = a34.groupby(['시군구', '대지위치', '중복건수', '총주차수합계', '최대주차장', 'rt'])['총주차수'].agg(lambda x: x.mode().iloc[0]).reset_index()
a35.columns = ['시군구', '대지위치', '중복건수', '총주차수합계', '최대주차장', 'rt', '최빈주차장']
a35['rt_최대최빈'] = a35['최빈주차장'] / a35['최대주차장']

## 최빈값이 최댓값의 95% 이상인 경우 : 최빈값 적용
f04 = a35[a35['rt_최대최빈'] >= 0.95]
f04['최종주차장수'] =  f04['최빈주차장']   # 3건
f04 = f04[['시군구', '대지위치', '최종주차장수']]

## 최빈값이 최댓값의 95% 미만인 경우 : 합계값 적용
f05 = a35[a35['rt_최대최빈'] < 0.95]
f05['최종주차장수'] =  f05['총주차수합계']   # 10건
f05 = f05[['시군구', '대지위치', '최종주차장수']]

aa01 = docu_unit[docu_unit['대지위치'] == '경기도 수원시 장안구 이목동 380-2번지']

a0001 = a34[a34['대지위치'] == '경기도 수원시 영통구 매탄동 1211번지']

##############################################
##7. 총괄표제부에는 있는데, 표제부 데이터가 없는 경우

a40 = pd.merge(a15, a23, how = 'left', on = ['시군구', '대지위치'])
a40['noinfo'] = np.where(a40['총주차수합계'].isnull(),1,0 )
# 룰생성 73건 : 총괄표제부에 있는데, 표제부 데이터가 없는 경우 총괄표제부 주차장수 추가
f06 = a40[(a40['noinfo'] == 1) & (a40['총괄주차장'] > 0 )]
f06['최종주차장수'] =  f06['총괄주차장']
f06 = f06[['시군구', '대지위치', '최종주차장수']]

## 최종 주차장수 통합
parking_cnt = pd.concat([f01, f02, f03, f04, f05, f06], axis=0)


###############################################################################################

## 기초구역 특성 세분화
## 거주인구, 유동인구수

seg_1 = pd.read_pickle('5.생활인구(평일,0,14,기초구역).pkl')

#1. 카드사용 금액 생성
card_blksum2 = pd.read_pickle('card_blksum2.pkl')

#2. 기초구역 면적
area_info = pd.read_pickle('기초구역별면적.pkl')
dong_info = pd.read_pickle('기초구역경계_행정동.pkl')

card_db = card_blksum2.groupby(['기초구역번호'])['amt'].sum().reset_index()
card_db.columns = ['기초구역번호', '카드금액']

#2. 건축면적(연면적), 주택면적 산출

## 건축물대장 주소별 기초구역 맵핑

house = docu_unit[['시군구명', '행정동명', '기초구역번호', '주소', '주용도코드명', '건물명', '연면적(㎡)']]
house.columns = ['시군구', '행정동', '기초구역번호', '주소', '주용도', '건물명', '연면적']
house['type'] = np.where(house['주용도'] ==  '단독주택', 1, np.where(house['주용도'] == '공동주택', 1, 2))
print(house.groupby(['type']).size().reset_index())

house_area = house.groupby(['시군구', '행정동', '기초구역번호'])['연면적'].sum().reset_index()
house_area.columns = ['시군구', '행정동', '기초구역번호', '연면적합계']

house_area2 = house.groupby(['시군구', '행정동', '기초구역번호', 'type'])['연면적'].sum().reset_index()
house_area2.columns = ['시군구', '행정동', '기초구역번호', 'type','연면적주택']
house_area2 = house_area2[house_area2['type'] == 1]  # 주택 연면적만 추출
house_area2 = house_area2[['시군구', '행정동', '기초구역번호', '연면적주택']]
house_area3 = pd.merge(house_area, house_area2, how = 'left', on = ['시군구', '행정동', '기초구역번호'])
house_area3 = house_area3.fillna(0)
house_area4 = house_area3.groupby(['기초구역번호'])[['연면적합계', '연면적주택']].sum().reset_index()


## 정보 통합
seg_12 = seg_1.groupby(['ETL_YM', 'ETL_YMD', '기초구역번호','TIME_CD'])[['V_SUM', 'H_SUM', 'W_SUM', '거주인구']].sum().reset_index()
seg_13 = seg_12.groupby(['기초구역번호','TIME_CD'])[['V_SUM', 'H_SUM', 'W_SUM', '거주인구']].mean().reset_index()
seg_2 = seg_13.pivot(index=['기초구역번호'], columns='TIME_CD', values=['V_SUM', 'H_SUM', 'W_SUM', '거주인구']).reset_index()
seg_2.columns = ['기초구역번호', 'V_SUM_h0', 'V_SUM_h14', 'H_SUM_h0', 'H_SUM_h14', 'W_SUM_h0', 'W_SUM_h14', '거주인구_h0', '거주인구_h14']

# 동, 기초구역 Key에 생활인구, 거주인구 정보 추가
seg_3 = pd.merge(dong_info, seg_2, how = 'left', on = '기초구역번호')
seg_31 = pd.merge(seg_3, area_info, how = 'left', on = '기초구역번호')
seg_32 = pd.merge(seg_31, house_area4, how = 'left', on = '기초구역번호')
seg_33 = pd.merge(seg_32, card_db, how = 'left', on = '기초구역번호')
seg_4 = seg_33.fillna(0)
seg_4['생활인구_h0'] = seg_4['V_SUM_h0'] +seg_4['H_SUM_h0'] + seg_4['W_SUM_h0']
seg_4['생활인구_h14'] = seg_4['V_SUM_h14'] +seg_4['H_SUM_h14'] + seg_4['W_SUM_h14']
seg_4['직장방문비율_h14'] = (seg_4['V_SUM_h14'] +seg_4['W_SUM_h14']) /seg_4['생활인구_h14']
seg_4['건물면적비율'] = seg_4['연면적합계'] /seg_4['기초구역면적']
seg_4['주택비율'] = seg_4['연면적주택'] /seg_4['연면적합계']
seg_4['생활인구비율_h14'] = np.where(seg_4['거주인구_h14'] == 0, 0, seg_4['생활인구_h14'] / seg_4['거주인구_h14'])


# 상관관계 계산
seg_corr = seg_4[[ '직장방문비율_h14', '생활인구비율_h14', '거주인구_h14',  '주택비율', '카드금액']]
correlation_matrix = seg_corr.corr()

#################################################################################
## 군집분석 이전에 사람 살지 않는 관심대사 아닌 지역 제외 : 거주인구, 카드금액으로 생성
## 히스토그램 확인

plt.hist(seg_4['거주인구_h14'], bins=10, color='skyblue', edgecolor='black')
plt.show()  # 그래프 출력

## box plot 그리기
plt.boxplot(seg_4['거주인구_h14'])
plt.show()
seg_4['거주인구_h14'].describe()

plt.boxplot(seg_4['건물면적비율'])
plt.show()
seg_4['건물면적비율'].describe()

aa = seg_4[(seg_4['거주인구_h14'] < 1538) & (seg_4['건물면적비율'] < 0.335)  ]


plt.boxplot(seg_4['카드금액'])
plt.show()
seg_4['카드금액'].describe()




#################################################################################
## 기초구역 배후지역 특성 세분화 : 군집분석

##1. 산, 농경지 등 제외 지역 탐색
# cl_db = seg_4[[ '직장방문비율_h14', '생활인구비율_h14', '거주인구_h14',  '주택비율', '카드금액']]
##1. 분석변수 표준화 : 분석데이터에서 클러스터링 대상 변수만 추출
cl_db = seg_4[[ '거주인구_h14',  '건물면적비율']]
cl_db =  cl_db.fillna(0)

## 극단값으로 산, 농경지 등의 최소한의 기초지역 갯수 파악 어려움 : 많은 기초구역(133개)이 한 그룹으로 묶임
## ==> 중위수 이하 값만으로 클러스터링 수행
cl_db.describe()    # 중위수 2614.86    0.50
seg_4s = seg_4[(seg_4['거주인구_h14'] <= 2614)& (seg_4['건물면적비율'] <= 0.5)]
cl_db = seg_4s[[ '거주인구_h14',  '건물면적비율']]

scaler = StandardScaler()
scaled_data = scaler.fit_transform(cl_db)

# 참고 : infinity 값 확인
print(np.isinf(cl_db).any())

##2. 최적의 클러스터 숫자 확인(엘보우 방법)

sum_of_squared_distances = []
K = range(1, 10)
for k in K:
    km = KMeans(n_clusters=k, random_state=0)
    km = km.fit(scaled_data)
    sum_of_squared_distances.append(km.inertia_)

plt.plot(K, sum_of_squared_distances, 'bx-')
plt.xlabel('k')
plt.ylabel('Sum of squared distances')
plt.title('Elbow Method For Optimal k')
plt.show()

## 클러스터별 갯수 확인
# 3. K-평균 클러스터링 모델 생성 및 학습
kmeans = KMeans(n_clusters=6, random_state=0)
kmeans.fit(scaled_data)

labels = kmeans.labels_
cl_db['Cluster'] = labels
print(cl_db.groupby('Cluster').size().reset_index())    ## 사이즈가 너무 작은 클러스터 포함
print(cl_db.groupby('Cluster')[['거주인구_h14',  '건물면적비율']].mean().reset_index())    ## 사이즈가 너무 작은 클러스터 포함

# 4. 클러스터 결과 시각화

## 클러스터별 다른 색깔 지정 스캐터플랏
sns.scatterplot(data=cl_db, x='거주인구_h14', y='건물면적비율', hue='Cluster', palette='Set1', s=100)
plt.show()

## cluster 1에 해당하는 데이터 추출
seg_4s['Cluster'] = labels
print(seg_4s.groupby('Cluster').size().reset_index())    ## 사이즈가 너무 작은 클러스터 포함
print(seg_4s.groupby('Cluster')[['거주인구_h14',  '건물면적비율']].mean().reset_index())    ## 사이즈가 너무 작은 클러스터 포함
seg_out = seg_4s[seg_4s['Cluster'] == 1]

###########################################################################
## 제외 기초구역 제외 후 분석데이터 구성
seg_4db = seg_4[~seg_4['기초구역번호'].isin(seg_out['기초구역번호'])]

cl_db = seg_4db[['직장방문비율_h14', '생활인구비율_h14', '거주인구_h14', '건물면적비율', '주택비율', '카드금액']]
cl_db =  cl_db.fillna(0)
scaler = StandardScaler()
scaled_data = scaler.fit_transform(cl_db)

# 참고 : infinity 값 확인
print(np.isinf(cl_db).any())

##2. 최적의 클러스터 숫자 확인(엘보우 방법)

sum_of_squared_distances = []
K = range(1, 10)
for k in K:
    km = KMeans(n_clusters=k, random_state=0)
    km = km.fit(scaled_data)
    sum_of_squared_distances.append(km.inertia_)

plt.plot(K, sum_of_squared_distances, 'bx-')
plt.xlabel('k')
plt.ylabel('Sum of squared distances')
plt.title('Elbow Method For Optimal k')
plt.show()

## 클러스터별 갯수 확인
# 3. K-평균 클러스터링 모델 생성 및 학습
kmeans = KMeans(n_clusters=5, random_state=0)
kmeans.fit(scaled_data)

labels = kmeans.labels_
cl_db['Cluster'] = labels
print(cl_db.groupby('Cluster').size().reset_index())    ## 사이즈가 너무 작은 클러스터 포함

# 4. 클러스터별 최소 3개의 중심점으로 시작
def fit_kmeans_with_min_samples(data, n_clusters, min_samples_per_cluster, max_iter=100):
    for i in range(max_iter):
        kmeans = KMeans(n_clusters=n_clusters, random_state=i)
        kmeans.fit(data)
        labels = kmeans.labels_
        cluster_counts = np.bincount(labels)

        if np.all(cluster_counts >= min_samples_per_cluster):
            return kmeans

    raise ValueError(
        f"Could not fit KMeans with each cluster having at least {min_samples_per_cluster} samples in {max_iter} iterations")


# K-평균 클러스터링 모델 생성 및 학습
n_clusters = 4
min_samples_per_cluster = 30     # 최소 중심점 갯수 지정

kmeans = fit_kmeans_with_min_samples(scaled_data, n_clusters, min_samples_per_cluster)
centers = kmeans.cluster_centers_
labels_4 = kmeans.labels_

# 결과를 원래 데이터프레임에 추가
seg_4db['Cluster_4'] = labels_4
print(seg_4db.groupby('Cluster_4').size().reset_index())
print(cl_db.groupby('Cluster')[['직장방문비율_h14', '생활인구비율_h14', '거주인구_h14', '건물면적비율', '주택비율', '카드금액']].mean().reset_index())

#########################
n_clusters = 5
min_samples_per_cluster = 25     # 최소 중심점 갯수 지정

kmeans = fit_kmeans_with_min_samples(scaled_data, n_clusters, min_samples_per_cluster)
centers = kmeans.cluster_centers_
labels_5 = kmeans.labels_

# 결과를 원래 데이터프레임에 추가
seg_4db['Cluster_5'] = labels_5
print(cl_db.groupby('Cluster_5').size().reset_index())
print(cl_db.groupby('Cluster')[['직장방문비율_h14', '생활인구비율_h14', '거주인구_h14', '건물면적비율', '주택비율', '카드금액']].mean().reset_index())

seg_4db.to_pickle('seg_4db.pkl')
seg_4db = pd.read_pickle('seg_4db.pkl')

## 정보생성  ###############################################

## 기초구역별 포인트좌표
point = docu_unit[['기초구역번호', 'geometry']]
point = point.drop_duplicates()

cluster_rslt = seg_4db[['HJD_NM', '기초구역번호', 'Cluster_4', 'Cluster_5']]
seg_info =  seg_4[['HJD_NM', '기초구역번호']]
seg_info = pd.merge(seg_info, cluster_rslt, how = 'left', on = ['HJD_NM', '기초구역번호'])
seg_info['Cluster_4'] = np.where(seg_info['Cluster_4'].isna(), 9, seg_info['Cluster_4'])
seg_info['Cluster_5'] = np.where(seg_info['Cluster_5'].isna(), 9, seg_info['Cluster_5'])
seg_info.to_pickle('seg_info.pkl')
seg_info = pd.read_pickle('seg_info.pkl')


## 기초구역 좌표정보 추가
seg_position = pd.merge(seg_info, point, how = 'left', on = ['기초구역번호'])
seg_position.to_pickle('seg_position.pkl')

seg_position = pd.read_pickle('seg_position.pkl')

## 해야할일 : 지도 참조하여 클러스터4, 클러스터5 중 더 적합한것 판단 후 분석보고서 생성   ######################
seg_infotot = seg_4db[['HJD_NM', '기초구역번호', '직장방문비율_h14', '생활인구비율_h14', '거주인구_h14', '건물면적비율', '주택비율', '카드금액' ]]
seg_infotot = pd.merge(seg_info, seg_infotot, how='left', on = ['HJD_NM', '기초구역번호'])
seg_infotot.to_pickle('seg_infotot.pkl')

###################################################################################################

## 주차 체감지표 개발

## 유입/유출 좌표로 기초구역 ID 생성
move_id = pd.read_pickle('최근한달유동인구_기초구역매핑.pkl')
move_id_var = move_id[['기초구역번호', 'UTMK_X', 'UTMK_Y']]
move_id_dong = move_id[['기초구역번호', 'HJD_NM']]
move_id_dong = move_id_dong.drop_duplicates()

# move_t1_202405 = pd.read_pickle('move_t1_202405.pkl')
move_t3_202405 = pd.read_pickle('move_t3_202405.pkl')
move_t3_202405['M_AGE_02'] = (move_t3_202405['H_M_10_CNT']+move_t3_202405['W_M_10_CNT']+move_t3_202405['V_M_10_CNT']
                             + move_t3_202405['H_M_15_CNT']+move_t3_202405['W_M_15_CNT']+move_t3_202405['V_M_15_CNT'])
move_t3_202405['M_AGE_03'] = (move_t3_202405['H_M_20_CNT']+move_t3_202405['W_M_20_CNT']+move_t3_202405['V_M_20_CNT']
                             + move_t3_202405['H_M_25_CNT']+move_t3_202405['W_M_25_CNT']+move_t3_202405['V_M_25_CNT'])
move_t3_202405['M_AGE_04'] = (move_t3_202405['H_M_30_CNT']+move_t3_202405['W_M_30_CNT']+move_t3_202405['V_M_30_CNT']
                             + move_t3_202405['H_M_35_CNT']+move_t3_202405['W_M_35_CNT']+move_t3_202405['V_M_35_CNT'])
move_t3_202405['M_AGE_05'] = (move_t3_202405['H_M_40_CNT']+move_t3_202405['W_M_40_CNT']+move_t3_202405['V_M_40_CNT']
                             + move_t3_202405['H_M_45_CNT']+move_t3_202405['W_M_45_CNT']+move_t3_202405['V_M_45_CNT'])
move_t3_202405['M_AGE_06'] = (move_t3_202405['H_M_50_CNT']+move_t3_202405['W_M_50_CNT']+move_t3_202405['V_M_50_CNT']
                             + move_t3_202405['H_M_55_CNT']+move_t3_202405['W_M_55_CNT']+move_t3_202405['V_M_55_CNT'])
move_t3_202405['M_AGE_08'] = (move_t3_202405['H_M_70_CNT']+move_t3_202405['W_M_70_CNT']+move_t3_202405['V_M_70_CNT'])

move_t3_202405['F_AGE_02'] = (move_t3_202405['H_F_10_CNT']+move_t3_202405['W_F_10_CNT']+move_t3_202405['V_F_10_CNT']
                             + move_t3_202405['H_F_15_CNT']+move_t3_202405['W_F_15_CNT']+move_t3_202405['V_F_15_CNT'])
move_t3_202405['F_AGE_03'] = (move_t3_202405['H_F_20_CNT']+move_t3_202405['W_F_20_CNT']+move_t3_202405['V_F_20_CNT']
                             + move_t3_202405['H_F_25_CNT']+move_t3_202405['W_F_25_CNT']+move_t3_202405['V_F_25_CNT'])
move_t3_202405['F_AGE_05'] = (move_t3_202405['H_F_40_CNT']+move_t3_202405['W_F_40_CNT']+move_t3_202405['V_F_40_CNT']
                             + move_t3_202405['H_F_45_CNT']+move_t3_202405['W_F_45_CNT']+move_t3_202405['V_F_45_CNT'])
move_t3_202405['F_AGE_06'] = (move_t3_202405['H_F_50_CNT']+move_t3_202405['W_F_50_CNT']+move_t3_202405['V_F_50_CNT']
                             + move_t3_202405['H_F_55_CNT']+move_t3_202405['W_F_55_CNT']+move_t3_202405['V_F_55_CNT'])
move_t3_202405['F_AGE_07'] = (move_t3_202405['H_F_60_CNT']+move_t3_202405['W_F_60_CNT']+move_t3_202405['V_F_60_CNT']
                             + move_t3_202405['H_F_65_CNT']+move_t3_202405['W_F_65_CNT']+move_t3_202405['V_F_65_CNT'])
move_t3_202405['F_AGE_08'] = (move_t3_202405['H_F_70_CNT']+move_t3_202405['W_F_70_CNT']+move_t3_202405['V_F_70_CNT'])

move_t3_202405 = pd.merge(move_t3_202405, move_id_var, how = 'left', on = [ 'UTMK_X', 'UTMK_Y'])
t3_202405 = move_t3_202405.groupby(['기초구역번호', 'ETL_YMD', 'TIME_CD' ])[['M_AGE_02', 'M_AGE_03', 'M_AGE_04',
       'M_AGE_05', 'M_AGE_06', 'M_AGE_07', 'M_AGE_08', 'F_AGE_02', 'F_AGE_03', 'F_AGE_04',
       'F_AGE_05', 'F_AGE_06', 'F_AGE_07', 'F_AGE_08']].sum().reset_index()

###################

t3_202405.to_pickle('t3_202405.pkl')
t3_202405 = pd.read_pickle('t3_202405.pkl')

t3_202405_male = t3_202405[['기초구역번호',  'ETL_YMD', 'TIME_CD',
                             'M_AGE_02', 'M_AGE_03', 'M_AGE_04','M_AGE_05', 'M_AGE_06', 'M_AGE_07', 'M_AGE_08']]
t3_202405_male['SEX_CD'] = 'M'
t3_202405_male['ETL_YMD'] = t3_202405_male['ETL_YMD'].astype(str)
t3_202405_male.columns = ['기초구역번호', 'ETL_YMD', 'TIME_CD', 'AGE_02', 'AGE_03', 'AGE_04',
                           'AGE_05', 'AGE_06', 'AGE_07', 'AGE_08', 'SEX_CD']
t3_male = t3_202405_male.melt(id_vars=['기초구역번호',  'ETL_YMD', 'TIME_CD', 'SEX_CD'],
                              value_vars=['AGE_02', 'AGE_03','AGE_04','AGE_05','AGE_06','AGE_07','AGE_08'],
                              var_name = 'AGE_GB',
                              value_name = 'CNT')
t3_male = pd.merge(t3_male, move_id_dong, how = 'left', on = '기초구역번호')

t3_202405_female = t3_202405[['기초구역번호',  'ETL_YMD', 'TIME_CD',
                             'F_AGE_02', 'F_AGE_03', 'F_AGE_04','F_AGE_05', 'F_AGE_06', 'F_AGE_07', 'F_AGE_08']]
t3_202405_female['SEX_CD'] = 'F'
t3_202405_female['ETL_YMD'] = t3_202405_female['ETL_YMD'].astype(str)
t3_202405_female.columns = ['기초구역번호', 'ETL_YMD', 'TIME_CD', 'AGE_02', 'AGE_03', 'AGE_04',
                           'AGE_05', 'AGE_06', 'AGE_07', 'AGE_08', 'SEX_CD']
t3_female = t3_202405_female.melt(id_vars=['기초구역번호',  'ETL_YMD', 'TIME_CD', 'SEX_CD'],
                              value_vars=['AGE_02', 'AGE_03','AGE_04','AGE_05','AGE_06','AGE_07','AGE_08'],
                              var_name = 'AGE_GB',
                              value_name = 'CNT')
t3_female = pd.merge(t3_female, move_id_dong, how = 'left', on = '기초구역번호')

### 자동차 유입인구 : move_t7

move_t7 = pd.read_pickle('move_t7.pkl')
move_t7['ETL_YMD'] = move_t7['ETL_YMD'].astype(str)
move_t7s = move_t7[move_t7['ETL_YMD'].str[:6] == '202405']
move_t7s_car = move_t7s[move_t7s['TRANS_GB'] == 0]
move_t7s_car = move_t7s_car[move_t7s_car['D_CTY_NM'].isin(['수원시 권선구', '수원시 영통구', '수원시 장안구', '수원시 팔달구' ])]
t7s_car_sum = move_t7s_car.groupby(['ETL_YMD', 'D_TIME_CD', 'D_ADMI_NM', 'SEX_CD', 'AGE_GRP'])['CNT'].sum().reset_index()
t7s_car_sum.columns = ['ETL_YMD', 'TIME_CD', 'HJD_NM', 'SEX_CD', 'AGE_GRP', 'CNT']
t7s_car_sum['AGE_GB'] = np.where(t7s_car_sum['AGE_GRP'] == 1, 'AGE_02',
                            np.where(t7s_car_sum['AGE_GRP'] == 2, 'AGE_02',
                                np.where(t7s_car_sum['AGE_GRP'] == 3, 'AGE_03',
                                    np.where(t7s_car_sum['AGE_GRP'] == 4, 'AGE_04',
                                        np.where(t7s_car_sum['AGE_GRP'] == 5, 'AGE_05',
                                           np.where(t7s_car_sum['AGE_GRP'] == 6, 'AGE_06',
                                              np.where(t7s_car_sum['AGE_GRP'] == 7, 'AGE_07',  'AGE_08')))))))

t7s_car_sum = t7s_car_sum.groupby(['ETL_YMD', 'TIME_CD', 'HJD_NM', 'SEX_CD', 'AGE_GB'])['CNT'].sum().reset_index()
t7s_car_sum.columns = ['ETL_YMD', 'TIME_CD', 'HJD_NM', 'SEX_CD', 'AGE_GB', 'CNT_CAR']
t7s_car_sum['ETL_YMD'] = t7s_car_sum['ETL_YMD'].astype(str)

weeklist = ['04','05','06', '11','12', '15', '18', '19', '25', '26']
t7s_car_sum['week_yn'] = np.where(t7s_car_sum['ETL_YMD'].str[6:8].isin(weeklist), '1', '0')

#### 전체 유입인구 : move_7
move_t7s_2 = move_t7s[move_t7s['D_CTY_NM'].isin(['수원시 권선구', '수원시 영통구', '수원시 장안구', '수원시 팔달구' ])]
t7s_sum = move_t7s_2.groupby(['ETL_YMD', 'D_TIME_CD', 'D_ADMI_NM', 'SEX_CD', 'AGE_GRP'])['CNT'].sum().reset_index()
t7s_sum.columns = ['ETL_YMD', 'TIME_CD', 'HJD_NM', 'SEX_CD', 'AGE_GRP', 'CNT']
t7s_sum['AGE_GB'] = np.where(t7s_sum['AGE_GRP'] == 1, 'AGE_02',
                            np.where(t7s_sum['AGE_GRP'] == 2, 'AGE_02',
                                np.where(t7s_sum['AGE_GRP'] == 3, 'AGE_03',
                                    np.where(t7s_sum['AGE_GRP'] == 4, 'AGE_04',
                                        np.where(t7s_sum['AGE_GRP'] == 5, 'AGE_05',
                                           np.where(t7s_sum['AGE_GRP'] == 6, 'AGE_06',
                                              np.where(t7s_sum['AGE_GRP'] == 7, 'AGE_07',  'AGE_08')))))))

t7s_sum = t7s_sum.groupby(['ETL_YMD', 'TIME_CD', 'HJD_NM', 'SEX_CD', 'AGE_GB'])['CNT'].sum().reset_index()
t7s_sum.columns = ['ETL_YMD', 'TIME_CD', 'HJD_NM', 'SEX_CD', 'AGE_GB', 'CNT_TOT']
t7s_sum['ETL_YMD'] = t7s_sum['ETL_YMD'].astype(str)

weeklist = ['04','05','06', '11','12', '15', '18', '19', '25', '26']
t7s_sum['week_yn'] = np.where(t7s_sum['ETL_YMD'].str[6:8].isin(weeklist), '1', '0')



### 자동차 유출인구 : move_t11

move_t11 = pd.read_pickle('move_t11.pkl')
move_t11['ETL_YMD'] = move_t11['ETL_YMD'].astype(str)
move_t11s = move_t11[move_t11['ETL_YMD'].str[:6] == '202405']
move_t11s_car = move_t11s[move_t11s['TRANS_GB'] == 0]
move_t11s_car = move_t11s_car[move_t11s_car['O_CTY_NM'].isin(['수원시 권선구', '수원시 영통구', '수원시 장안구', '수원시 팔달구' ])]
t11s_car_sum = move_t11s_car.groupby(['ETL_YMD', 'O_TIME_CD', 'O_ADMI_NM', 'SEX_CD', 'AGE_GRP'])['CNT'].sum().reset_index()
t11s_car_sum.columns = ['ETL_YMD', 'TIME_CD', 'HJD_NM', 'SEX_CD', 'AGE_GRP', 'CNT']
t11s_car_sum['AGE_GB'] = np.where(t11s_car_sum['AGE_GRP'] == 1, 'AGE_02',
                            np.where(t11s_car_sum['AGE_GRP'] == 2, 'AGE_02',
                                np.where(t11s_car_sum['AGE_GRP'] == 3, 'AGE_03',
                                    np.where(t11s_car_sum['AGE_GRP'] == 4, 'AGE_04',
                                        np.where(t11s_car_sum['AGE_GRP'] == 5, 'AGE_05',
                                           np.where(t11s_car_sum['AGE_GRP'] == 6, 'AGE_06',
                                              np.where(t11s_car_sum['AGE_GRP'] == 7, 'AGE_07',  'AGE_08')))))))

t11s_car_sum = t11s_car_sum.groupby(['ETL_YMD', 'TIME_CD', 'HJD_NM', 'SEX_CD', 'AGE_GB'])['CNT'].sum().reset_index()
t11s_car_sum.columns = ['ETL_YMD', 'TIME_CD', 'HJD_NM', 'SEX_CD', 'AGE_GB', 'CNT_CAR']
t11s_car_sum['ETL_YMD'] = t11s_car_sum['ETL_YMD'].astype(str)
t11s_car_sum['week_yn'] = np.where(t11s_car_sum['ETL_YMD'].str[6:8].isin(weeklist), '1', '0')

#### 전체 유입인구 : move_11
move_t11s_2 = move_t11s[move_t11s['O_CTY_NM'].isin(['수원시 권선구', '수원시 영통구', '수원시 장안구', '수원시 팔달구' ])]
t11s_sum = move_t11s_2.groupby(['ETL_YMD', 'O_TIME_CD', 'O_ADMI_NM', 'SEX_CD', 'AGE_GRP'])['CNT'].sum().reset_index()
t11s_sum.columns = ['ETL_YMD', 'TIME_CD', 'HJD_NM', 'SEX_CD', 'AGE_GRP', 'CNT']
t11s_sum['AGE_GB'] = np.where(t11s_sum['AGE_GRP'] == 1, 'AGE_02',
                            np.where(t11s_sum['AGE_GRP'] == 2, 'AGE_02',
                                np.where(t11s_sum['AGE_GRP'] == 3, 'AGE_03',
                                    np.where(t11s_sum['AGE_GRP'] == 4, 'AGE_04',
                                        np.where(t11s_sum['AGE_GRP'] == 5, 'AGE_05',
                                           np.where(t11s_sum['AGE_GRP'] == 6, 'AGE_06',
                                              np.where(t11s_sum['AGE_GRP'] == 7, 'AGE_07',  'AGE_08')))))))

t11s_sum = t11s_sum.groupby(['ETL_YMD', 'TIME_CD', 'HJD_NM', 'SEX_CD', 'AGE_GB'])['CNT'].sum().reset_index()
t11s_sum.columns = ['ETL_YMD', 'TIME_CD', 'HJD_NM', 'SEX_CD', 'AGE_GB', 'CNT_TOT']
t11s_sum['ETL_YMD'] = t11s_sum['ETL_YMD'].astype(str)

weeklist = ['04','05','06', '11','12', '15', '18', '19', '25', '26']
t11s_sum['week_yn'] = np.where(t11s_sum['ETL_YMD'].str[6:8].isin(weeklist), '1', '0')







## 생활인구와 자동차유입인구 합치기
t3_male_2 = pd.merge(t3_male, t7s_car_sum, how = 'left', on = ['ETL_YMD', 'TIME_CD', 'HJD_NM', 'SEX_CD', 'AGE_GB'])

## 동별 생활인구수
t3_male_dong = t3_male_2.groupby(['HJD_NM', 'ETL_YMD', 'TIME_CD', 'SEX_CD', 'AGE_GB'])['CNT'].sum().reset_index()
t3_male_dong.columns = ['HJD_NM', 'ETL_YMD', 'TIME_CD', 'SEX_CD', 'AGE_GB', 'CNT_DONG']
t3_male_2 = pd.merge(t3_male_2, t3_male_dong, how = 'left', on = ['HJD_NM', 'ETL_YMD', 'TIME_CD', 'SEX_CD', 'AGE_GB'])
t3_male_2 = t3_male_2.fillna(0)
t3_male_2['CAR_RT'] = t3_male_2['CNT_CAR']*(t3_male_2['CNT']/t3_male_2['CNT_DONG'])
correlation_coefficient, p_value =  pearsonr(t3_male_2['CNT'], t3_male_2['CAR_RT'])
print(f"Pearson 상관계수: {correlation_coefficient, p_value}")  # (0.5584910364438951, 0.0)

## 기초구역별 시간대별 증가/감소 생활인구 생성
t3_male_2 = t3_male_2.sort_values(by = ['HJD_NM','기초구역번호','SEX_CD', 'AGE_GB', 'ETL_YMD','TIME_CD' ], ascending = True)
aa01 = t3_male_2.head(10000)

# '이전 값' 항목 생성하여 앞 행의 값을 유지하도록 함  retain
t3_male_2['cnt_add'] = t3_male_2['CNT'] - t3_male_2['CNT'].shift()

# A 그룹, B 그룹의 순서 number 생성   : 그룹의 첫번째 행 값 생성 . 그룹별 순번
t3_male_2['no'] = t3_male_2.groupby(['HJD_NM','기초구역번호','SEX_CD', 'AGE_GB']).cumcount() + 1

t3_male_2['cnt_add'] = np.where(t3_male_2['no'] == 1, 0, t3_male_2['cnt_add'])
t3_male_2['cnt_incr'] = np.where(t3_male_2['cnt_add'] >0, t3_male_2['cnt_add'], 0)

correlation_coefficient, p_value =  pearsonr(t3_male_2['cnt_add'], t3_male_2['CAR_RT'])
print(f"Pearson 상관계수: {correlation_coefficient, p_value}")  # (0.3086913879805461, 0.0)

correlation_coefficient, p_value =  pearsonr(t3_male_2['cnt_incr'], t3_male_2['CAR_RT'])
print(f"Pearson 상관계수: {correlation_coefficient, p_value}")  # Pearson 상관계수:  (0.584539409123632, 0.0)

## 증가만 합쳐서 차량 비율을 다시 배분해야 함. 1. 증가량합치기, 2. 비율 생성, 3. 차량증가분 산출
## 동별 생활인구수 시간대별 증가분 산출
t3_male_dong2 = t3_male_2.groupby(['HJD_NM', 'ETL_YMD', 'TIME_CD', 'SEX_CD', 'AGE_GB'])['cnt_incr'].sum().reset_index()
t3_male_dong2.columns = ['HJD_NM', 'ETL_YMD', 'TIME_CD', 'SEX_CD', 'AGE_GB', 'cntincr_dong']
t3_male_2 = pd.merge(t3_male_2, t3_male_dong2, how = 'left', on = ['HJD_NM', 'ETL_YMD', 'TIME_CD', 'SEX_CD', 'AGE_GB'])
t3_male_2 = t3_male_2.fillna(0)
t3_male_2['car_incr'] = t3_male_2['CNT_CAR']*(t3_male_2['cnt_incr']/t3_male_2['cntincr_dong'])
t3_male_2 = t3_male_2.fillna(0)

correlation_coefficient, p_value =  pearsonr(t3_male_2['cnt_incr'], t3_male_2['car_incr'])
print(f"Pearson 상관계수: {correlation_coefficient, p_value}")  #  (0.5625232106847086, 0.0)

################################################

## 기초구역 할당로직  :기초구역별 자동차 순증/순감 : 행정동별 유입인구 중 자동차 비율 * 기초구역 시간별 생활인구 순증/순감*자동차수



#############################################################################################

## 행정동 단위 차량 유입 / 유출 패턴 분석. 생활인구 연관성 분석. 연관 항목으로 기초구역 할당..
#### 행정동단위로 체감지표 먼저 만들고, 기초구역으로 할당 후 기초구역 분포 확인

##2024.05 일별 차량 유출, 차량유입
in_01 = t7s_car_sum.groupby(['ETL_YMD'])['CNT_CAR'].sum().reset_index()

out_01 = t11s_car_sum.groupby(['ETL_YMD'])['CNT_CAR'].sum().reset_index()

## 평일 시간대별 유입차량/유출차량
in_02 = t7s_car_sum[t7s_car_sum['week_yn'] == '0']
in_02 = in_02.groupby(['TIME_CD','ETL_YMD' ])['CNT_CAR'].sum().reset_index()
in_02 = in_02.groupby(['TIME_CD' ])['CNT_CAR'].mean().reset_index()

out_02 = t11s_car_sum[t11s_car_sum['week_yn'] == '0']
out_02 = out_02.groupby(['TIME_CD','ETL_YMD' ])['CNT_CAR'].sum().reset_index()
out_02 = out_02.groupby(['TIME_CD'])['CNT_CAR'].mean().reset_index()

## 주말 시간대별 유입차량/유출차량
in_021 = t7s_car_sum[t7s_car_sum['week_yn'] == '1']
in_021 = in_021.groupby(['TIME_CD','ETL_YMD' ])['CNT_CAR'].sum().reset_index()
in_021 = in_021.groupby(['TIME_CD' ])['CNT_CAR'].mean().reset_index()

out_021 = t11s_car_sum[t11s_car_sum['week_yn'] == '1']
out_021 = out_021.groupby(['TIME_CD','ETL_YMD' ])['CNT_CAR'].sum().reset_index()
out_021 = out_021.groupby(['TIME_CD'])['CNT_CAR'].mean().reset_index()


## 기초구역별 일평균
in_03 = t7s_car_sum.groupby(['HJD_NM','ETL_YMD' ])['CNT_CAR'].sum().reset_index()
in_03 = in_03.groupby(['HJD_NM'])['CNT_CAR'].mean().reset_index()

out_03 = t11s_car_sum.groupby(['HJD_NM','ETL_YMD' ])['CNT_CAR'].sum().reset_index()
out_03 = out_03.groupby(['HJD_NM'])['CNT_CAR'].mean().reset_index()

## 연령대별 일평균
in_04 = t7s_car_sum.groupby(['AGE_GB','ETL_YMD' ])['CNT_CAR'].sum().reset_index()
in_04 = in_04.groupby(['AGE_GB'])['CNT_CAR'].mean().reset_index()

out_04 = t11s_car_sum.groupby(['AGE_GB','ETL_YMD' ])['CNT_CAR'].sum().reset_index()
out_04 = out_04.groupby(['AGE_GB'])['CNT_CAR'].mean().reset_index()

## 성별 연령대별 일평균
in_05 = t7s_car_sum.groupby(['SEX_CD', 'AGE_GB','ETL_YMD' ])['CNT_CAR'].sum().reset_index()
in_05 = in_05.groupby(['SEX_CD', 'AGE_GB'])['CNT_CAR'].mean().reset_index()

out_05 = t11s_car_sum.groupby(['SEX_CD', 'AGE_GB','ETL_YMD' ])['CNT_CAR'].sum().reset_index()
out_05 = out_05.groupby(['SEX_CD', 'AGE_GB'])['CNT_CAR'].mean().reset_index()


in_01.to_excel(os.path.join(outdir, 'a28_0911_유입_일자별.xlsx'))
in_02.to_excel(os.path.join(outdir, 'a28_0911_유입_시간대별.xlsx'))
in_03.to_excel(os.path.join(outdir, 'a28_0911_유입_행정동별.xlsx'))
in_04.to_excel(os.path.join(outdir, 'a28_0911_유입_연령대별.xlsx'))
in_05.to_excel(os.path.join(outdir, 'a28_0911_유입_성별연령대별.xlsx'))

out_01.to_excel(os.path.join(outdir, 'a28_0911_유출_일자별.xlsx'))
out_02.to_excel(os.path.join(outdir, 'a28_0911_유출_시간대별.xlsx'))
out_03.to_excel(os.path.join(outdir, 'a28_0911_유출_행정동별.xlsx'))
out_04.to_excel(os.path.join(outdir, 'a28_0911_유출_연령대별.xlsx'))
out_05.to_excel(os.path.join(outdir, 'a28_0911_유출_성별연령대별.xlsx'))

## 행정동별, 성별/연령별, 시간대별 차량 비율
## 기초구역별 일평균
intot_03 = t7s_sum.groupby(['HJD_NM','ETL_YMD' ])['CNT_TOT'].sum().reset_index()
intot_03 = intot_03.groupby(['HJD_NM'])['CNT_TOT'].mean().reset_index()

intot_03 = pd.merge(intot_03, in_03, how = 'left', on = 'HJD_NM')
intot_03['car_rt'] =intot_03['CNT_CAR'] /intot_03['CNT_TOT']

## 유입 시간대별
## 평일 시간대별 유입차량/유출차량
intot_02 = t7s_sum[t7s_sum['week_yn'] == '0']
intot_02 = intot_02.groupby(['TIME_CD','ETL_YMD' ])['CNT_TOT'].sum().reset_index()
intot_02 = intot_02.groupby(['TIME_CD' ])['CNT_TOT'].mean().reset_index()
intot_02 = pd.merge(intot_02, in_02, how = 'left', on = 'TIME_CD')
intot_02['car_rt'] =intot_02['CNT_CAR'] /intot_02['CNT_TOT']

intot_021 = t7s_sum[t7s_sum['week_yn'] == '1']
intot_021 = intot_021.groupby(['TIME_CD','ETL_YMD' ])['CNT_TOT'].sum().reset_index()
intot_021 = intot_021.groupby(['TIME_CD' ])['CNT_TOT'].mean().reset_index()
intot_021 = pd.merge(intot_021, in_021, how = 'left', on = 'TIME_CD')
intot_021['car_rt'] =intot_021['CNT_CAR'] /intot_021['CNT_TOT']


## 유입인구 전체, 차량 합치가
t7s_sum2 = pd.merge(t7s_sum, t7s_car_sum, how = 'left', on = ['ETL_YMD', 'TIME_CD', 'HJD_NM', 'SEX_CD', 'AGE_GB', 'week_yn'])


aa00 = t7s_sum2.head(1000)

t7s_car_sum.columns

t7s_sum.columns



## 성별,연령별 유동인구 : move_t1_202405 , move_t3_202405

move_t3_202405.columns
## 유입지역
t7_center = move_t7[['D_CENTER_X', 'D_CENTER_Y']]
t7_center2 = t7_center.groupby(['D_CENTER_X', 'D_CENTER_Y']).size().reset_index()

## 날짜별 시간대별 행정동별 차량유

t1_202405 = move_t1_202405[['ETL_YMD', 'UTMK_X', 'UTMK_Y', 'TIME_CD',
                          'FORN_GB', 'M_10_CNT', 'M_15_CNT', 'M_20_CNT', 'M_25_CNT', 'M_30_CNT',
                          'M_35_CNT', 'M_40_CNT', 'M_45_CNT', 'M_50_CNT', 'M_55_CNT', 'M_60_CNT',
                          'M_65_CNT', 'M_70_CNT', 'F_10_CNT', 'F_15_CNT', 'F_20_CNT', 'F_25_CNT',
                          'F_30_CNT', 'F_35_CNT', 'F_40_CNT', 'F_45_CNT', 'F_50_CNT', 'F_55_CNT',
                          'F_60_CNT', 'F_65_CNT', 'F_70_CNT']]

t1_202405 = pd.merge(t1_202405, move_id_var, how = 'left', on = [ 'UTMK_X', 'UTMK_Y'])

t1_202405 = t1_202405.groupby(['기초구역번호', 'ETL_YMD', 'TIME_CD' ])[[ 'M_10_CNT', 'M_15_CNT', 'M_20_CNT', 'M_25_CNT', 'M_30_CNT',
                          'M_35_CNT', 'M_40_CNT', 'M_45_CNT', 'M_50_CNT', 'M_55_CNT', 'M_60_CNT',
                          'M_65_CNT', 'M_70_CNT', 'F_10_CNT', 'F_15_CNT', 'F_20_CNT', 'F_25_CNT',
                          'F_30_CNT', 'F_35_CNT', 'F_40_CNT', 'F_45_CNT', 'F_50_CNT', 'F_55_CNT',
                          'F_60_CNT', 'F_65_CNT', 'F_70_CNT']].sum().reset_index()

t1_202405_male = t1_202405[['기초구역번호',  'ETL_YMD', 'TIME_CD',
                                 'M_10_CNT', 'M_15_CNT', 'M_20_CNT', 'M_25_CNT', 'M_30_CNT',
                                 'M_35_CNT', 'M_40_CNT', 'M_45_CNT', 'M_50_CNT', 'M_55_CNT', 'M_60_CNT',
                                 'M_65_CNT', 'M_70_CNT']]
t1_202405_male['SEX_CD'] = 'M'
t1_202405_male['AGE_02'] = t1_202405_male['M_10_CNT'] + t1_202405_male['M_15_CNT']
t1_202405_male['AGE_03'] = t1_202405_male['M_20_CNT'] + t1_202405_male['M_25_CNT']
t1_202405_male['AGE_04'] = t1_202405_male['M_30_CNT'] + t1_202405_male['M_35_CNT']
t1_202405_male['AGE_05'] = t1_202405_male['M_40_CNT'] + t1_202405_male['M_45_CNT']
t1_202405_male['AGE_06'] = t1_202405_male['M_50_CNT'] + t1_202405_male['M_55_CNT']
t1_202405_male['AGE_07'] = t1_202405_male['M_60_CNT'] + t1_202405_male['M_65_CNT']
t1_202405_male['AGE_08'] = t1_202405_male['M_70_CNT']

t1_202405_male_melt = t1_202405_male.melt(id_vars=['기초구역번호',  'ETL_YMD', 'TIME_CD', 'SEX_CD'],
                              value_vars=['AGE_02', 'AGE_03','AGE_04','AGE_05','AGE_06','AGE_07','AGE_08'],
                              var_name = 'AGE_GB',
                              value_name = 'CNT')
t1_202405_male_melt = pd.merge(t1_202405_male_melt, move_id_dong, how  = 'left', on  = '기초구역번호')

t1_202405_female = t1_202405[['기초구역번호',  'ETL_YMD', 'TIME_CD',
                                 'F_10_CNT', 'F_15_CNT', 'F_20_CNT', 'F_25_CNT', 'F_30_CNT',
                                 'F_35_CNT', 'F_40_CNT', 'F_45_CNT', 'F_50_CNT', 'F_55_CNT', 'F_60_CNT',
                                 'F_65_CNT', 'F_70_CNT']]
t1_202405_female['SEX_CD'] = 'F'
t1_202405_female['AGE_02'] = t1_202405_female['F_10_CNT'] + t1_202405_female['F_15_CNT']
t1_202405_female['AGE_03'] = t1_202405_female['F_20_CNT'] + t1_202405_female['F_25_CNT']
t1_202405_female['AGE_04'] = t1_202405_female['F_30_CNT'] + t1_202405_female['F_35_CNT']
t1_202405_female['AGE_05'] = t1_202405_female['F_40_CNT'] + t1_202405_female['F_45_CNT']
t1_202405_female['AGE_06'] = t1_202405_female['F_50_CNT'] + t1_202405_female['F_55_CNT']
t1_202405_female['AGE_07'] = t1_202405_female['F_60_CNT'] + t1_202405_female['F_65_CNT']
t1_202405_female['AGE_08'] = t1_202405_female['F_70_CNT']

t1_202405_female_melt = t1_202405_female.melt(id_vars=['기초구역번호',  'ETL_YMD', 'TIME_CD', 'SEX_CD'],
                              value_vars=['AGE_02', 'AGE_03','AGE_04','AGE_05','AGE_06','AGE_07','AGE_08'],
                              var_name = 'AGE_GB',
                              value_name = 'CNT')
t1_202405_female_melt = pd.merge(t1_202405_female_melt, move_id_dong, how  = 'left', on  = '기초구역번호')

## 남자, 여자 합쳐야 함 / 따로 분석


t1_202405_male_melt['ETL_YMD'] = t1_202405_male_melt['ETL_YMD'].astype(str)

t1_202405_male_melt2 = pd.merge(t1_202405_male_melt, t11s_car_sum, how = 'left', on = ['ETL_YMD', 'TIME_CD', 'HJD_NM', 'SEX_CD', 'AGE_GB'])

## 행정동별 유동인구수 중에서 기초구역별 유동인구비율 :














t1_202405_female_melt['ETL_YMD'].head()
t11s_car_sum['ETL_YMD'].head()

aa01 = t1_202405_male_melt2.head(1000)
aa02 = move_id.groupby('HJD_NM').size().reset_index()


t11s_car_sum.groupby(['AGE_GRP']).size().reset_index()
move_id_2 = move_id[['HJD_NM', '기초구역번호']]
t1_202405_male_melt.columns

aa01 = t1_202405_male_melt.head(1000)
aa02 = t1_202405_female_melt.head(1000)
t11s_car_sum.columns

t3_202405 = pd.merge(move_t3_202405, move_id_var, how = 'left', on = [ 'UTMK_X', 'UTMK_Y'])
aa02  =  t3_202405.head(10000)


move_id.columns




move_t11s.columns


'ETL_YMD', 'O_TIME_CD', 'O_ADMI_NM', 'TRANS_GB', 'SEX_CD', 'AGE_GRP', 'CNT'








aa01 = t1_melt.head(1000)

['ADMI_CD', 'CTY_NM', 'ADMI_NM', 'UTMK_X', 'UTMK_Y', 'TIME_CD',
       'FORN_GB', 'M_10_CNT', 'M_15_CNT', 'M_20_CNT', 'M_25_CNT', 'M_30_CNT',
       'M_35_CNT', 'M_40_CNT', 'M_45_CNT', 'M_50_CNT', 'M_55_CNT', 'M_60_CNT',
       'M_65_CNT', 'M_70_CNT', 'F_10_CNT', 'F_15_CNT', 'F_20_CNT', 'F_25_CNT',
       'F_30_CNT', 'F_35_CNT', 'F_40_CNT', 'F_45_CNT', 'F_50_CNT', 'F_55_CNT',
       'F_60_CNT', 'F_65_CNT', 'F_70_CNT', 'ETL_YMD']



