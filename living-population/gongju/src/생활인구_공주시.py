
###########################################################################################

##  카드사용 패턴 분석  ##

###########################################################################################

## 데이터 생성

## 1. 업종별 매출규모별 휴폐업 데이터

file_paths = glob.glob('D:\\data\\생활인구_card_공주상권\\*.csv')  # 특정 경로의 텍스트 파일을 모두 가져오는 예시

# 모든 CSV 파일을 담을 리스트 생성
all_data = []
for file_path in file_paths:
    df = pd.read_csv(file_path)
    all_data.append(df)

    # 리스트에 있는 모든 데이터프레임을 하나로 합치기
go_card_area = pd.concat(all_data)
go_card_area.to_pickle('go_card_area.pkl')

##############################################################

## 2. 업종별 매출규모별 휴폐업 데이터

file_paths = glob.glob('D:\\data\\생활인구_card_공주매출\\*.csv')  # 특정 경로의 텍스트 파일을 모두 가져오는 예시

# 모든 CSV 파일을 담을 리스트 생성
all_data = []
for file_path in file_paths:
    df = pd.read_csv(file_path)
    all_data.append(df)

    # 리스트에 있는 모든 데이터프레임을 하나로 합치기
go_card_totamt = pd.concat(all_data)
go_card_totamt.to_pickle('go_card_totamt.pkl')

##############################################################

## 3. 비씨카드 사용액 (공주시)

file_paths = glob.glob('D:\data\\생활인구_card_공주지역내거주\\*.csv')  # 특정 경로의 텍스트 파일을 모두 가져오는 예시

# 모든 CSV 파일을 담을 리스트 생성
all_data = []
for file_path in file_paths:
    df = pd.read_csv(file_path)
    all_data.append(df)

    # 리스트에 있는 모든 데이터프레임을 하나로 합치기
go_card_in = pd.concat(all_data)
go_card_in.to_pickle('go_card_in.pkl')

##############################################################

## 4. 기타지역 거주 공주 사용액

file_paths = glob.glob('D:\data\\생활인구_card_공주기타지역거주\\*.csv')  # 특정 경로의 텍스트 파일을 모두 가져오는 예시

# 모든 CSV 파일을 담을 리스트 생성
all_data = []
for file_path in file_paths:
    df = pd.read_csv(file_path)
    all_data.append(df)

    # 리스트에 있는 모든 데이터프레임을 하나로 합치기
go_card_out = pd.concat(all_data)
go_card_out.to_pickle('go_card_out.pkl')

##############################################################

## 5. 재난지원금 사용액

file_paths = glob.glob('D:\data\\생활인구_card_공주재난지원금\\*.csv')  # 특정 경로의 텍스트 파일을 모두 가져오는 예시

# 모든 CSV 파일을 담을 리스트 생성
all_data = []
for file_path in file_paths:
    df = pd.read_csv(file_path)
    all_data.append(df)

    # 리스트에 있는 모든 데이터프레임을 하나로 합치기
go_card_add = pd.concat(all_data)
go_card_add.to_pickle('go_card_add.pkl')


###########################################################

## 6. 업종 데이터

card_bizcd = pd.read_excel('카드업종_대분류.xlsx', dtype=str)
card_bizcd.columns = ['bizcd', 'biznm']


###########################################################################################
###########################################################################################

go_card_area   = pd.read_pickle('go_card_area.pkl')
go_card_totamt = pd.read_pickle('go_card_totamt.pkl')
go_card_in     = pd.read_pickle('go_card_in.pkl')
go_card_out    = pd.read_pickle('go_card_out.pkl')


##  카드 데이터 분석

##1. 공주시 전체 데이터 분석

go_card_totamt = go_card_totamt.fillna(0)
go_card_totamt['year'] = go_card_totamt['CRTR_YM'].astype('str').str[:4]
go_card_totamt['bizcd'] = go_card_totamt['TOBIZ_CD'].astype('str').str[:2]

## 2022.12 행정동별 매출액, 건수

go_amt_202212 = go_card_totamt[go_card_totamt['CRTR_YM'] == 202212 ]

go_amt_sum = go_amt_202212.groupby(['DONG_NM']).agg({'USE_AMT_SUM':"sum", 'USE_NOCS_SUM':"sum" }).reset_index()
go_amt_sum.to_excel('d:\\out\\공주시_D1010_카드지역별매출액_202212.xlsx')
## 행정동별 월별 매출액

go_amt_mm = go_card_totamt.groupby(['CRTR_YM'])['USE_AMT_SUM'].sum().reset_index()
go_amt_mm.to_excel('d:\\out\\공주시_D1010_카드월별매출액.xlsx')

## 2022.12  업종별 카드 사용액
go_amt_202212['bizcd'] = go_amt_202212['TOBIZ_CD'].astype('str').str[:2]
go_amt_sum2 = go_amt_202212.groupby(['bizcd']).agg({'USE_AMT_SUM':"sum", 'USE_NOCS_SUM':"sum" }).reset_index()
go_amt_sum2 = pd.merge(go_amt_sum2, card_bizcd, how = 'left', on = 'bizcd' )
go_amt_sum2.to_excel('d:\\out\\공주시_D1010_업종별사용액_202212.xlsx')

## 2022.12  상세업종별 카드 사용액
go_amt_sum3 = go_amt_202212.groupby(['bizcd', 'TOBIZ_NM' ]).agg({'USE_AMT_SUM':"sum", 'USE_NOCS_SUM':"sum" }).reset_index()
go_amt_sum3 = pd.merge(go_amt_sum3, card_bizcd, how = 'left', on = 'bizcd' )
go_amt_sum3.to_excel('d:\\out\\공주시_D1010_상세업종별사용액_202212.xlsx')


## 업종별 연간 증가율
go_amt_year = go_card_totamt.groupby(['year', 'bizcd'])['USE_AMT_SUM'].sum().reset_index()
go_amt_year = pd.merge(go_amt_year, card_bizcd, how = 'left', on = 'bizcd' )

go_amt_year1 =  go_amt_year[go_amt_year['year'] == '2021']
go_amt_year2 =  go_amt_year[go_amt_year['year'] == '2022']

go_amt_year1.columns  = ['year', 'bizcd', 'amt_2021', 'biznm']
go_amt_year2.columns  = ['year', 'bizcd', 'amt_2022', 'biznm']

go_amt_year3 = pd.merge(go_amt_year1, go_amt_year2, how = 'left' , on = ['bizcd', 'biznm'])

go_amt_year3['add_rt'] =  (go_amt_year3['amt_2022'] - go_amt_year3['amt_2021']) / go_amt_year3['amt_2021']
go_amt_year3.to_excel('d:\\out\\공주시_D1010_업종별증가율.xlsx')

## 업종 증가율 분석 : '32' 주방용품 2% 최대금액, '33' 연료판매 27%, '84' 건강식품 -45%

## 여행업
go_card_biz1 =  go_card_totamt[go_card_totamt['bizcd'] == '32']
go_card_biz1_y = go_card_biz1.groupby(['year', 'DONG_NM'])['USE_AMT_SUM'].sum().reset_index()

go_card_biz1_y0 = go_card_biz1.groupby('DONG_NM')['USE_AMT_SUM'].sum().reset_index()
go_card_biz1_y1 =  go_card_biz1_y[go_card_biz1_y['year'] == '2021']
go_card_biz1_y2 =  go_card_biz1_y[go_card_biz1_y['year'] == '2022']

go_card_biz1_y1.columns  = ['year', 'DONG_NM', 'amt_2021']
go_card_biz1_y2.columns  = ['year', 'DONG_NM', 'amt_2022']

go_card_biz1_y3 = pd.merge(go_card_biz1_y0, go_card_biz1_y1, how = 'left' , on = 'DONG_NM')
go_card_biz1_y3 = pd.merge(go_card_biz1_y3, go_card_biz1_y2, how = 'left' , on = 'DONG_NM')

go_card_biz1_y3['add_rt'] =  (go_card_biz1_y3['amt_2022'] - go_card_biz1_y3['amt_2021']) / go_card_biz1_y3['amt_2021']
go_card_biz1_y3.to_excel('d:\\out\\공주시_D1010_업종1_주방용품증가율.xlsx')

## 연료판매
go_card_biz2 =  go_card_totamt[go_card_totamt['bizcd'] == '33']
go_card_biz2_y = go_card_biz2.groupby(['year', 'DONG_NM'])['USE_AMT_SUM'].sum().reset_index()

go_card_biz2_y0 = go_card_biz2.groupby('DONG_NM')['USE_AMT_SUM'].sum().reset_index()
go_card_biz2_y1 =  go_card_biz2_y[go_card_biz2_y['year'] == '2021']
go_card_biz2_y2 =  go_card_biz2_y[go_card_biz2_y['year'] == '2022']

go_card_biz2_y1.columns  = ['year', 'DONG_NM', 'amt_2021']
go_card_biz2_y2.columns  = ['year', 'DONG_NM', 'amt_2022']

go_card_biz2_y3 = pd.merge(go_card_biz2_y0, go_card_biz2_y1, how = 'left' , on = 'DONG_NM')
go_card_biz2_y3 = pd.merge(go_card_biz2_y3, go_card_biz2_y2, how = 'left' , on = 'DONG_NM')

go_card_biz2_y3['add_rt'] =  (go_card_biz2_y3['amt_2022'] - go_card_biz2_y3['amt_2021']) / go_card_biz2_y3['amt_2021']
go_card_biz2_y3.to_excel('d:\\out\\공주시_D1010_업종2_연료판매증가율.xlsx')

## 건강식품
go_card_biz3 =  go_card_totamt[go_card_totamt['bizcd'] == '84']
go_card_biz3_y = go_card_biz3.groupby(['year', 'DONG_NM'])['USE_AMT_SUM'].sum().reset_index()

go_card_biz3_y0 = go_card_biz3.groupby('DONG_NM')['USE_AMT_SUM'].sum().reset_index()
go_card_biz3_y1 =  go_card_biz3_y[go_card_biz3_y['year'] == '2021']
go_card_biz3_y2 =  go_card_biz3_y[go_card_biz3_y['year'] == '2022']

go_card_biz3_y1.columns  = ['year', 'DONG_NM', 'amt_2021']
go_card_biz3_y2.columns  = ['year', 'DONG_NM', 'amt_2022']

go_card_biz3_y3 = pd.merge(go_card_biz3_y0, go_card_biz3_y1, how = 'left' , on = 'DONG_NM')
go_card_biz3_y3 = pd.merge(go_card_biz3_y3, go_card_biz3_y2, how = 'left' , on = 'DONG_NM')

go_card_biz3_y3['add_rt'] =  (go_card_biz3_y3['amt_2022'] - go_card_biz3_y3['amt_2021']) / go_card_biz3_y3['amt_2021']
go_card_biz3_y3.to_excel('d:\\out\\공주시_D1010_업종3_건강식품증가율.xlsx')

## 2. 행정동별 카드 데이터 분석   :  업종분석, 가맹점수분석, 성별/연령대분석,  시간대분석, 요일분석, 거주지역분석,  개인법인분석

## 행정동별 매출액 증가율
go_card_dong = go_card_totamt.groupby(['year', 'DONG_NM'])['USE_AMT_SUM'].sum().reset_index()
go_card_dong_y1 =  go_card_dong[go_card_dong['year'] == '2021']
go_card_dong_y2 =  go_card_dong[go_card_dong['year'] == '2022']

go_card_dong_y1.columns  = ['year', 'DONG_NM', 'amt_2021']
go_card_dong_y2.columns  = ['year', 'DONG_NM', 'amt_2022']

go_card_dong_y3 = pd.merge(go_card_dong_y1, go_card_dong_y2, how = 'left' , on = 'DONG_NM')
go_card_dong_y3['add_rt'] =  (go_card_dong_y3['amt_2022'] - go_card_dong_y3['amt_2021']) / go_card_dong_y3['amt_2021']
go_card_dong_y3.to_excel('d:\\out\\공주시_D1010_행정동별증가율.xlsx')


## 행정동별 업종별 매출액 증가율

go_card_dong2 = go_card_totamt.groupby(['year', 'DONG_NM', 'bizcd'])['USE_AMT_SUM'].sum().reset_index()

go_card_dong2_y0 =  go_card_totamt.groupby(['DONG_NM', 'bizcd'])['USE_AMT_SUM'].sum().reset_index()
go_card_dong2_y1 =  go_card_dong2[go_card_dong2['year'] == '2021']
go_card_dong2_y2 =  go_card_dong2[go_card_dong2['year'] == '2022']

go_card_dong2_y1.columns  = ['year', 'DONG_NM', 'bizcd', 'amt_2021']
go_card_dong2_y2.columns  = ['year', 'DONG_NM', 'bizcd', 'amt_2022']

go_card_dong2_y3 = pd.merge(go_card_dong2_y0, go_card_dong2_y1, how = 'left' , on = ['DONG_NM', 'bizcd'])
go_card_dong2_y3 = pd.merge(go_card_dong2_y3, go_card_dong2_y2, how = 'left' , on = ['DONG_NM', 'bizcd'])

go_card_dong2_y3['add_rt'] =  (go_card_dong2_y3['amt_2022'] - go_card_dong2_y3['amt_2021']) / go_card_dong2_y3['amt_2021']
go_card_dong2_y3 = pd.merge(go_card_dong2_y3, card_bizcd, how = 'left', on = 'bizcd' )
go_card_dong2_y3.to_excel('d:\\out\\공주시_D1010_행정동업종별증가율.xlsx')

## 행정동별 가맹점 현황

go_card_area['year'] = go_card_area['CRTR_YM'].astype('str').str[:4]
go_card_area['bizcd'] = go_card_area['TOBIZ_CD'].astype('str').str[:2]


go_card_store = go_card_area[['year', 'CRTR_YM','DONG_NM', 'bizcd', 'BIZ_MM_CNT', 'FRCS_CNT']]
go_card_store_term = go_card_store.groupby(['year', 'CRTR_YM','DONG_NM', 'bizcd'])['BIZ_MM_CNT'].mean().reset_index()
go_card_store_term = pd.merge(go_card_store_term, card_bizcd, how = 'left', on = 'bizcd' )
go_card_store_cnt = go_card_store.groupby(['year', 'CRTR_YM','DONG_NM', 'bizcd'])['FRCS_CNT'].sum().reset_index()
go_card_store_cnt = pd.merge(go_card_store_cnt, card_bizcd, how = 'left', on = 'bizcd' )

go_card_store_term12 = go_card_store_term[go_card_store_term['CRTR_YM'] == 202212]
go_card_store_cnt12 = go_card_store_cnt[go_card_store_cnt['CRTR_YM'] == 202212]


##  요일분석, 시간대분석, 거주지역분석,  개인법인분석, 성별/연령대분석,
go_card_dongamt = go_card_totamt[['year','DONG_NM', 'MON_USE_AMT', 'TUES_USE_AMT', 'WEDNES_USE_AMT',
       'THURS_USE_AMT', 'FRI_USE_AMT', 'SATUR_USE_AMT', 'SUN_USE_AMT', '00_05_HR_USE_AMT', '06_10_HR_USE_AMT', '11_13_HR_USE_AMT',
       '14_17_HR_USE_AMT', '18_20_HR_USE_AMT', '21_23_HR_USE_AMT', 'INDIV_USE_AMT_SUM', 'COR_USE_AMT_SUM','CNND_CUST_USE_AMT',
       'CNND_EXCL_CUST_USE_AMT']]

go_card_dongamt2 = go_card_dongamt.groupby(['year','DONG_NM']).sum().reset_index()

go_card_dongamt2.to_excel('d:\\out\\공주시_D1010_행정동요일시간대.xlsx')

go_card_dongbiz = go_card_totamt[['year','DONG_NM', 'bizcd', 'MON_USE_AMT', 'TUES_USE_AMT', 'WEDNES_USE_AMT',
       'THURS_USE_AMT', 'FRI_USE_AMT', 'SATUR_USE_AMT', 'SUN_USE_AMT', '00_05_HR_USE_AMT', '06_10_HR_USE_AMT', '11_13_HR_USE_AMT',
       '14_17_HR_USE_AMT', '18_20_HR_USE_AMT', '21_23_HR_USE_AMT', 'INDIV_USE_AMT_SUM', 'COR_USE_AMT_SUM','CNND_CUST_USE_AMT',
       'CNND_EXCL_CUST_USE_AMT']]

go_card_dongbiz2 = go_card_dongbiz.groupby(['year','DONG_NM', 'bizcd']).sum().reset_index()
go_card_dongbiz2 = pd.merge(go_card_dongbiz2, card_bizcd, how = 'left', on = 'bizcd' )


## 성별/연령대 분석

## 공주시 사용 데이터만 추출
go_card_in['in_yn'] = np.where(go_card_in['FRCS_SGG_NM'] == '공주시', 1, 0)
go_card_in['year'] = go_card_in['CRTR_YM'].astype('str').str[:4]
go_card_in['bizcd'] = go_card_in['TOBIZ_CD'].astype('str').str[:2]

## 연도별 행정동별 공주시 내/외부 사용금액 비율
go_card_inout = go_card_in[['year','CUST_DONG_NM', 'ALL_USE_AMT',  'ML_USE_AMT',
       'FM_USE_AMT', 'TEEN_BELOW_USE_AMT', 'TEEN_USE_AMT', 'TWT_USE_AMT',
       'TRT_USE_AMT', 'FRT_USE_AMT', 'FFT_USE_AMT', 'SXT_USE_AMT',
       'SVT_ABV_USE_AMT']]

go_card_inoutamt = go_card_inout.groupby(['year','CUST_DONG_NM']).sum().reset_index()
go_card_inoutamt.to_excel('d:\\out\\공주시_D1010_행정동연령대.xlsx')

go_card_inout2 = go_card_in[['year','CUST_DONG_NM', 'in_yn', 'ALL_USE_AMT',  'ML_USE_AMT',
       'FM_USE_AMT', 'TEEN_BELOW_USE_AMT', 'TEEN_USE_AMT', 'TWT_USE_AMT',
       'TRT_USE_AMT', 'FRT_USE_AMT', 'FFT_USE_AMT', 'SXT_USE_AMT',
       'SVT_ABV_USE_AMT']]

go_card_inoutamt2 = go_card_inout2.groupby(['year','CUST_DONG_NM', 'in_yn']).sum().reset_index()
go_card_inoutamt2.to_excel('d:\\out\\공주시_D1010_행정동연령대2.xlsx')

## 공주시 지역별/월별 외부 사용금액,  성별/연령별
go_card_inhis = go_card_in[['year','CRTR_YM', 'CUST_DONG_NM', 'in_yn', 'ALL_USE_AMT',  'ML_USE_AMT',
       'FM_USE_AMT', 'TEEN_BELOW_USE_AMT', 'TEEN_USE_AMT', 'TWT_USE_AMT',
       'TRT_USE_AMT', 'FRT_USE_AMT', 'FFT_USE_AMT', 'SXT_USE_AMT',   'SVT_ABV_USE_AMT']]
go_card_inhis2 = go_card_inhis.groupby(['year','CRTR_YM', 'CUST_DONG_NM', 'in_yn']).sum().reset_index()





## 공주시 외부거주인구의 공주시 사용 금액,  성별/연령별
go_card_out['year'] = go_card_out['CRTR_YM'].astype('str').str[:4]
go_card_out['bizcd'] = go_card_out['TOBIZ_CD'].astype('str').str[:2]

go_card_out.columns

## 거주 시도별 공주시 지역별 사용금액,  성별/연령별
go_card_outamt = go_card_out[['year','CUST_CTPV_NM', 'ALL_USE_AMT',  'ML_USE_AMT',
       'FM_USE_AMT', 'TEEN_BELOW_USE_AMT', 'TEEN_USE_AMT', 'TWT_USE_AMT',
       'TRT_USE_AMT', 'FRT_USE_AMT', 'FFT_USE_AMT', 'SXT_USE_AMT',   'SVT_ABV_USE_AMT']]
go_card_outamt2 = go_card_outamt.groupby(['year','CUST_CTPV_NM']).sum().reset_index()

## 공주시 지역별 외부 사용금액,  성별/연령별
go_card_outdong = go_card_out[['year','FRCS_DONG_NM', 'ALL_USE_AMT',  'ML_USE_AMT',
       'FM_USE_AMT', 'TEEN_BELOW_USE_AMT', 'TEEN_USE_AMT', 'TWT_USE_AMT',
       'TRT_USE_AMT', 'FRT_USE_AMT', 'FFT_USE_AMT', 'SXT_USE_AMT',   'SVT_ABV_USE_AMT']]
go_card_outdong2 = go_card_outdong.groupby(['year','FRCS_DONG_NM']).sum().reset_index()

## 공주시 지역별/월별 외부 사용금액,  성별/연령별
go_card_outhis = go_card_out[['year','CRTR_YM', 'FRCS_DONG_NM', 'ALL_USE_AMT',  'ML_USE_AMT',
       'FM_USE_AMT', 'TEEN_BELOW_USE_AMT', 'TEEN_USE_AMT', 'TWT_USE_AMT',
       'TRT_USE_AMT', 'FRT_USE_AMT', 'FFT_USE_AMT', 'SXT_USE_AMT',   'SVT_ABV_USE_AMT']]
go_card_outhis2 = go_card_outhis.groupby(['year','CRTR_YM','FRCS_DONG_NM']).sum().reset_index()


## 공주시 업종별 외부 사용금액,  성별/연령별
go_card_outind = go_card_out[['year','bizcd', 'ALL_USE_AMT',  'ML_USE_AMT',
       'FM_USE_AMT', 'TEEN_BELOW_USE_AMT', 'TEEN_USE_AMT', 'TWT_USE_AMT',
       'TRT_USE_AMT', 'FRT_USE_AMT', 'FFT_USE_AMT', 'SXT_USE_AMT',   'SVT_ABV_USE_AMT']]
go_card_outind2 = go_card_outind.groupby(['year','bizcd']).sum().reset_index()
go_card_outind2 = pd.merge(go_card_outind2, card_bizcd, how = 'left', on = 'bizcd' )

## 공주시 지역별/업종별 외부 사용금액,  성별/연령별
go_card_outseg = go_card_out[['year','FRCS_DONG_NM', 'bizcd', 'ALL_USE_AMT',  'ML_USE_AMT',
       'FM_USE_AMT', 'TEEN_BELOW_USE_AMT', 'TEEN_USE_AMT', 'TWT_USE_AMT',
       'TRT_USE_AMT', 'FRT_USE_AMT', 'FFT_USE_AMT', 'SXT_USE_AMT',   'SVT_ABV_USE_AMT']]
go_card_outseg2 = go_card_outseg.groupby(['year','FRCS_DONG_NM', 'bizcd']).sum().reset_index()
go_card_outseg2 = pd.merge(go_card_outseg2, card_bizcd, how = 'left', on = 'bizcd' )


###################################################################################
###################################################################################
###################################################################################

## 지역축제 분석

##1. 석장리 박물관

gj_tmap = pd.read_pickle('gj_tmap.pkl')

gj_tmap.columns
gj_tmap_s1 = gj_tmap[gj_tmap['dstn_nm'] == '석장리박물관']

tmap = gj_tmap_s1

tmap['vst_cnt'] = tmap['vst_cnt'].astype('int')
tmap['fm_user_cnt'] = tmap['fm_user_cnt'].astype('int')
tmap['ml_user_cnt'] = tmap['ml_user_cnt'].astype('int')
tmap['sx_abs_user_cnt'] = tmap['sx_abs_user_cnt'].astype('int')
tmap['twt_les_user_cnt'] = tmap['twt_les_user_cnt'].astype('int')
tmap['trt_user_cnt'] = tmap['trt_user_cnt'].astype('int')
tmap['frt_user_cnt'] = tmap['frt_user_cnt'].astype('int')
tmap['fft_user_cnt'] = tmap['fft_user_cnt'].astype('int')
tmap['sxt_abv_user_cnt']  = tmap['sxt_abv_user_cnt'].astype('int')
tmap['age_abs_user_cnt'] = tmap['age_abs_user_cnt'].astype('int')
tmap['avg_stay_min'] = tmap['avg_stay_min'].astype('float')

tmap['befo_gj_yn'] = np.where(tmap['frst_dptre_sgg_nm'] == "공주시", 1, 0)
tmap['year'] = tmap['drv_ymd'].str[:4]
tmap['yymm'] = tmap['drv_ymd'].str[:6]
tmap['vst_addtime'] = tmap['vst_cnt']*tmap['avg_stay_min']

tmap['vst_cnt2'] = tmap['vst_cnt']*0.5
tmap['vst_cnt3'] = tmap['vst_cnt']*0.2

tmap_sam1_sum2 = tmap_s0.groupby(['scnd_next_dstn_nm'])["vst_cnt"].sum().reset_index()

## 일자별 방문 건수

s1_totcnt = tmap.groupby(['drv_ymd'])["vst_cnt"].sum().reset_index()
s1_totcnt2 = s1_totcnt[(s1_totcnt['drv_ymd'].str[:6] == '202204')|(s1_totcnt['drv_ymd'].str[:6] == '202205')]
s1_totcnt2.to_excel('d:\\out\\공주시_D1016_구석기일별티맵.xlsx')


# 외부 방문지 Top10
## 당일 첫 출발지 공주시 여부
tmap_s0 = tmap[tmap["befo_gj_yn"] == 0]
tmap_s0 = tmap_s0[(tmap_s0['drv_ymd'] == '20220505')|(tmap_s0['drv_ymd'] == '20220506')|(tmap_s0['drv_ymd'] == '20220507')|(tmap_s0['drv_ymd'] == '20220508')]

# 외부 방문지 Top10
tmap_out_sum = tmap_s0.groupby(['drv_ymd'])["vst_cnt"].sum().reset_index()
tmap_out_area = tmap_s0.groupby(['frst_dptre_ctpv_nm', 'frst_dptre_sgg_nm'])["vst_cnt"].sum().reset_index()
tmap_out_area1 = tmap_s0.groupby(['frst_dptre_ctpv_nm'])["vst_cnt"].sum().reset_index()

tmap_out_sum.to_excel('d:\\out\\공주시_D1016_구석기일별티맵 공주시여부.xlsx')
tmap_out_area.to_excel('d:\\out\\공주시_D1016_구석기일별티맵 외부지역시군구.xlsx')
tmap_out_area1.to_excel('d:\\out\\공주시_D1016_구석기일별티맵 외부지역시도.xlsx')

## 방문 패쓰 : 외부인
tmap_sam1_sum = tmap_s0.groupby(['frst_next_dstn_nm'])["vst_cnt"].sum().reset_index()
tmap_sam1_sum2 = tmap_s0.groupby(['scnd_next_dstn_nm'])["vst_cnt2"].sum().reset_index()

tmap_sam1_sum.columns = ['dstn_nm', 'vst_cnt']
tmap_sam1_sum2.columns = ['dstn_nm', 'vst_cnt']

tmap_sam1_sum3 = pd.concat([tmap_sam1_sum, tmap_sam1_sum2], axis = 0)
tmap_path = tmap_sam1_sum3.groupby(['dstn_nm'])["vst_cnt"].sum().reset_index()
tmap_pathinfo = gj_tmap.groupby(['dstn_nm', 'dstn_dong_nm', 'dstn_ctgy'])["vst_cnt"].sum().reset_index()
tmap_pathinfo = tmap_pathinfo[['dstn_nm', 'dstn_dong_nm', 'dstn_ctgy']]
tmap_pathinfo.columns = [['dstn_nm', 'dstn_dong_nm', 'dstn_ctgy']]
tmap_path2 = pd.merge(tmap_path, tmap_pathinfo, how ='left' , on = 'dstn_nm')

tmap_path2.to_excel('d:\\out\\공주시_D1016_구석기외부방문패쓰.xlsx')

## 연령대 : 행사분석
tmap_ss = tmap[(tmap['drv_ymd'] == '20220505')|(tmap['drv_ymd'] == '20220506')|(tmap['drv_ymd'] == '20220507')|(tmap['drv_ymd'] == '20220508')]
tmap_sam1_age = tmap_ss.groupby(["befo_gj_yn"])[["twt_les_user_cnt", "trt_user_cnt","frt_user_cnt", "fft_user_cnt", "sxt_abv_user_cnt"]].sum().reset_index()
tmap_sam1_age.to_excel('d:\\out\\공주시_D1016_구석기티맵연령대.xlsx')

## 평균체류시간
print(tmap_ss['vst_addtime'].sum() / tmap_ss['vst_cnt'].sum() )

## 방문 시간
tmap_hh = tmap_ss.groupby(['frst_arvl_hr'])["vst_cnt"].sum().reset_index()
tmap_ss['vst_time2'] = tmap_ss['vst_cnt']*0.5

tmap_time_sum = tmap_ss.groupby(['frst_arvl_hr'])["vst_cnt"].sum().reset_index()
tmap_time_sum2 = tmap_ss.groupby(['scnd_arvl_hr'])["vst_time2"].sum().reset_index()

tmap_time_sum.columns = ['arvl_hr', 'vst_cnt']
tmap_time_sum2.columns = ['arvl_hr', 'vst_cnt']

tmap_time_sum3 = pd.concat([tmap_time_sum, tmap_time_sum2], axis = 0)
tmap_time_sum4 = tmap_time_sum3.groupby(['arvl_hr'])["vst_cnt"].sum().reset_index()
tmap_time_sum4.to_excel('d:\\out\\공주시_D1016_구석기티맵시간대.xlsx')

#############

gj_tmap_s2 = gj_tmap[gj_tmap['dstn_nm'] == '유구색동수국정원']
ym_befo = '202205'
ym_target = '202206'
dd_target = ['20220617','20220618', '20220619']

tmap = gj_tmap_s2

tmap['vst_cnt'] = tmap['vst_cnt'].astype('int')
tmap['fm_user_cnt'] = tmap['fm_user_cnt'].astype('int')
tmap['ml_user_cnt'] = tmap['ml_user_cnt'].astype('int')
tmap['sx_abs_user_cnt'] = tmap['sx_abs_user_cnt'].astype('int')
tmap['twt_les_user_cnt'] = tmap['twt_les_user_cnt'].astype('int')
tmap['trt_user_cnt'] = tmap['trt_user_cnt'].astype('int')
tmap['frt_user_cnt'] = tmap['frt_user_cnt'].astype('int')
tmap['fft_user_cnt'] = tmap['fft_user_cnt'].astype('int')
tmap['sxt_abv_user_cnt']  = tmap['sxt_abv_user_cnt'].astype('int')
tmap['age_abs_user_cnt'] = tmap['age_abs_user_cnt'].astype('int')
tmap['avg_stay_min'] = tmap['avg_stay_min'].astype('float')

tmap['befo_gj_yn'] = np.where(tmap['frst_dptre_sgg_nm'] == "공주시", 1, 0)
tmap['year'] = tmap['drv_ymd'].str[:4]
tmap['yymm'] = tmap['drv_ymd'].str[:6]
tmap['vst_addtime'] = tmap['vst_cnt']*tmap['avg_stay_min']

tmap['vst_cnt2'] = tmap['vst_cnt']*0.5
tmap['vst_cnt3'] = tmap['vst_cnt']*0.2

tmap_sam1_sum2 = tmap_s0.groupby(['scnd_next_dstn_nm'])["vst_cnt"].sum().reset_index()

## 일자별 방문 건수

s1_totcnt = tmap.groupby(['drv_ymd'])["vst_cnt"].sum().reset_index()
s1_totcnt2 = s1_totcnt[(s1_totcnt['drv_ymd'].str[:6] == ym_befo)|(s1_totcnt['drv_ymd'].str[:6] == ym_target)]
s1_totcnt2.to_excel('d:\\out\\공주시_D1016_수국정원일별티맵.xlsx')


# 외부 방문지 Top10
## 당일 첫 출발지 공주시 여부
tmap_s0 = tmap[tmap["befo_gj_yn"] == 0]
tmap_s0 = tmap_s0[tmap_s0['drv_ymd'].isin(dd_target)]

tmap_inout = tmap[tmap['drv_ymd'].isin(dd_target)]
# 외부 방문지 Top10
tmap_out_sum = tmap_inout.groupby(['drv_ymd', "befo_gj_yn"])["vst_cnt"].sum().reset_index()
tmap_out_area = tmap_s0.groupby(['frst_dptre_ctpv_nm', 'frst_dptre_sgg_nm'])["vst_cnt"].sum().reset_index()
tmap_out_area1 = tmap_s0.groupby(['frst_dptre_ctpv_nm'])["vst_cnt"].sum().reset_index()

tmap_out_sum.to_excel('d:\\out\\공주시_D1016_수국정원 공주시여부.xlsx')
tmap_out_area.to_excel('d:\\out\\공주시_D1016_수국정원 외부지역시군구.xlsx')
tmap_out_area1.to_excel('d:\\out\\공주시_D1016_수국정원 외부지역시도.xlsx')

## 방문 패쓰 : 외부인
tmap_sam1_sum = tmap_s0.groupby(['frst_next_dstn_nm'])["vst_cnt"].sum().reset_index()
tmap_sam1_sum2 = tmap_s0.groupby(['scnd_next_dstn_nm'])["vst_cnt2"].sum().reset_index()

tmap_sam1_sum.columns = ['dstn_nm', 'vst_cnt']
tmap_sam1_sum2.columns = ['dstn_nm', 'vst_cnt']

tmap_sam1_sum3 = pd.concat([tmap_sam1_sum, tmap_sam1_sum2], axis = 0)
tmap_path = tmap_sam1_sum3.groupby(['dstn_nm'])["vst_cnt"].sum().reset_index()
tmap_pathinfo = gj_tmap.groupby(['dstn_nm', 'dstn_dong_nm', 'dstn_ctgy'])["vst_cnt"].sum().reset_index()
tmap_pathinfo = tmap_pathinfo[['dstn_nm', 'dstn_dong_nm', 'dstn_ctgy']]
tmap_path2 = pd.merge(tmap_path, tmap_pathinfo, how ='left' , on = 'dstn_nm')

tmap_path2.to_excel('d:\\out\\공주시_D1016_수국정원외부방문패쓰.xlsx')

## 연령대 : 행사분석
tmap_ss = tmap[tmap['drv_ymd'].isin(dd_target)]

tmap_sam1_age = tmap_ss.groupby(["befo_gj_yn"])[["twt_les_user_cnt", "trt_user_cnt","frt_user_cnt", "fft_user_cnt", "sxt_abv_user_cnt"]].sum().reset_index()
tmap_sam1_age.to_excel('d:\\out\\공주시_D1016_수국정원티맵연령대.xlsx')

## 평균체류시간
print(tmap_ss['vst_addtime'].sum() / tmap_ss['vst_cnt'].sum() )

## 방문 시간
tmap_hh = tmap_ss.groupby(['frst_arvl_hr'])["vst_cnt"].sum().reset_index()
tmap_ss['vst_time2'] = tmap_ss['vst_cnt']*0.5

tmap_time_sum = tmap_ss.groupby(['frst_arvl_hr'])["vst_cnt"].sum().reset_index()
tmap_time_sum2 = tmap_ss.groupby(['scnd_arvl_hr'])["vst_time2"].sum().reset_index()

tmap_time_sum.columns = ['arvl_hr', 'vst_cnt']
tmap_time_sum2.columns = ['arvl_hr', 'vst_cnt']

tmap_time_sum3 = pd.concat([tmap_time_sum, tmap_time_sum2], axis = 0)
tmap_time_sum4 = tmap_time_sum3.groupby(['arvl_hr'])["vst_cnt"].sum().reset_index()
tmap_time_sum4.to_excel('d:\\out\\공주시_D1016_수국정원티맵시간대.xlsx')


#############  금강신관공원

gj_tmap_s3 = gj_tmap[gj_tmap['dstn_nm'] == '금강신관공원']
ym_befo = '202209'
ym_target = '202210'
dd_target = ['20221001','20221002', '20221003', '20221004', '20221005', '20221006', '20221007', '20221008', '20221009', '20221010']

tmap = gj_tmap_s3

tmap['vst_cnt'] = tmap['vst_cnt'].astype('int')
tmap['fm_user_cnt'] = tmap['fm_user_cnt'].astype('int')
tmap['ml_user_cnt'] = tmap['ml_user_cnt'].astype('int')
tmap['sx_abs_user_cnt'] = tmap['sx_abs_user_cnt'].astype('int')
tmap['twt_les_user_cnt'] = tmap['twt_les_user_cnt'].astype('int')
tmap['trt_user_cnt'] = tmap['trt_user_cnt'].astype('int')
tmap['frt_user_cnt'] = tmap['frt_user_cnt'].astype('int')
tmap['fft_user_cnt'] = tmap['fft_user_cnt'].astype('int')
tmap['sxt_abv_user_cnt']  = tmap['sxt_abv_user_cnt'].astype('int')
tmap['age_abs_user_cnt'] = tmap['age_abs_user_cnt'].astype('int')
tmap['avg_stay_min'] = tmap['avg_stay_min'].astype('float')

tmap['befo_gj_yn'] = np.where(tmap['frst_dptre_sgg_nm'] == "공주시", 1, 0)
tmap['year'] = tmap['drv_ymd'].str[:4]
tmap['yymm'] = tmap['drv_ymd'].str[:6]
tmap['vst_addtime'] = tmap['vst_cnt']*tmap['avg_stay_min']

tmap['vst_cnt2'] = tmap['vst_cnt']*0.5
tmap['vst_cnt3'] = tmap['vst_cnt']*0.2

tmap_sam1_sum2 = tmap_s0.groupby(['scnd_next_dstn_nm'])["vst_cnt"].sum().reset_index()

## 일자별 방문 건수

s1_totcnt = tmap.groupby(['drv_ymd'])["vst_cnt"].sum().reset_index()
s1_totcnt2 = s1_totcnt[(s1_totcnt['drv_ymd'].str[:6] == ym_befo)|(s1_totcnt['drv_ymd'].str[:6] == ym_target)]
s1_totcnt2.to_excel('d:\\out\\공주시_D1016_백제문화제티맵.xlsx')


# 외부 방문지 Top10
## 당일 첫 출발지 공주시 여부
tmap_s0 = tmap[tmap["befo_gj_yn"] == 0]
tmap_s0 = tmap_s0[tmap_s0['drv_ymd'].isin(dd_target)]

tmap_inout = tmap[tmap['drv_ymd'].isin(dd_target)]
# 외부 방문지 Top10
tmap_out_sum = tmap_inout.groupby(['drv_ymd', "befo_gj_yn"])["vst_cnt"].sum().reset_index()
tmap_out_area = tmap_s0.groupby(['frst_dptre_ctpv_nm', 'frst_dptre_sgg_nm'])["vst_cnt"].sum().reset_index()
tmap_out_area1 = tmap_s0.groupby(['frst_dptre_ctpv_nm'])["vst_cnt"].sum().reset_index()

tmap_out_sum.to_excel('d:\\out\\공주시_D1016_백제문화제 공주시여부.xlsx')
tmap_out_area.to_excel('d:\\out\\공주시_D1016_백제문화제 외부지역시군구.xlsx')
tmap_out_area1.to_excel('d:\\out\\공주시_D1016_백제문화제 외부지역시도.xlsx')

## 방문 패쓰 : 외부인
tmap_sam1_sum = tmap_s0.groupby(['frst_next_dstn_nm'])["vst_cnt"].sum().reset_index()
tmap_sam1_sum2 = tmap_s0.groupby(['scnd_next_dstn_nm'])["vst_cnt2"].sum().reset_index()

tmap_sam1_sum.columns = ['dstn_nm', 'vst_cnt']
tmap_sam1_sum2.columns = ['dstn_nm', 'vst_cnt']

tmap_sam1_sum3 = pd.concat([tmap_sam1_sum, tmap_sam1_sum2], axis = 0)
tmap_path = tmap_sam1_sum3.groupby(['dstn_nm'])["vst_cnt"].sum().reset_index()
tmap_pathinfo = gj_tmap.groupby(['dstn_nm', 'dstn_dong_nm', 'dstn_ctgy'])["vst_cnt"].sum().reset_index()
tmap_pathinfo = tmap_pathinfo[['dstn_nm', 'dstn_dong_nm', 'dstn_ctgy']]
tmap_path2 = pd.merge(tmap_path, tmap_pathinfo, how ='left' , on = 'dstn_nm')

tmap_path2.to_excel('d:\\out\\공주시_D1016_백제문화제외부방문패쓰.xlsx')

## 연령대 : 행사분석
tmap_ss = tmap[tmap['drv_ymd'].isin(dd_target)]

tmap_sam1_age = tmap_ss.groupby(["befo_gj_yn"])[["twt_les_user_cnt", "trt_user_cnt","frt_user_cnt", "fft_user_cnt", "sxt_abv_user_cnt"]].sum().reset_index()
tmap_sam1_age.to_excel('d:\\out\\공주시_D1016_백제문화제티맵연령대.xlsx')

## 평균체류시간
print(tmap_ss['vst_addtime'].sum() / tmap_ss['vst_cnt'].sum() )

## 방문 시간
tmap_hh = tmap_ss.groupby(['frst_arvl_hr'])["vst_cnt"].sum().reset_index()
tmap_ss['vst_time2'] = tmap_ss['vst_cnt']*0.5

tmap_time_sum = tmap_ss.groupby(['frst_arvl_hr'])["vst_cnt"].sum().reset_index()
tmap_time_sum2 = tmap_ss.groupby(['scnd_arvl_hr'])["vst_time2"].sum().reset_index()

tmap_time_sum.columns = ['arvl_hr', 'vst_cnt']
tmap_time_sum2.columns = ['arvl_hr', 'vst_cnt']

tmap_time_sum3 = pd.concat([tmap_time_sum, tmap_time_sum2], axis = 0)
tmap_time_sum4 = tmap_time_sum3.groupby(['arvl_hr'])["vst_cnt"].sum().reset_index()
tmap_time_sum4.to_excel('d:\\out\\공주시_D1016_백제문화제티맵시간대.xlsx')