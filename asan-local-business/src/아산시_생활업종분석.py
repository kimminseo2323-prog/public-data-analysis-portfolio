
########################################################################################

##  아산시 생활업종 분석     ####

########################################################################################

## 창폐업 현황 분석

#1. 업종별 인허가건수
st1_01_upjong_lv1 = living_com.groupby(['job_area']).size().reset_index()
st1_02_upjong_lv2 = living_com.groupby(['job_area', 'job_cate']).size().reset_index()

#2. 1개 업체가 여러건 인허가 샘플
st1_03_upjong_cnt = living_com.groupby(['좌표정보(x)', '좌표정보(y)', '사업장명']).size().reset_index()

sam1 = living_com[(living_com['좌표정보(x)'] == 205631.312131464) & (living_com['사업장명'] == '삼성전자(주)')]
sam11 = job_0928_gas[(job_0928_gas['좌표정보(x)'] == '205631.312131464' ) & (job_0928_gas['사업장명'] == '삼성전자(주)')]
sam2 = living_com[(living_com['좌표정보(x)'] == 198347.641465429) & (living_com['사업장명'] == '(주)경보제약')]
sam21 = job_0928_gas[(job_0928_gas['좌표정보(x)'] == '198347.641465429' ) & (job_0928_gas['사업장명'] == '(주)경보제약')]

sam3 = living_com[(living_com['좌표정보(x)'] == 201508.583572712) & (living_com['사업장명'] == '미소약국')]
sam4 = living_com[(living_com['좌표정보(x)'] == 201256.960573236) & (living_com['사업장명'] == '주공세탁소')]

## 좌표정보 없는 건
sam = living_com[living_com['좌표정보(x)']]

st1_03_upjong_cnt.to_excel('d:\\out\\아산시_D112300_인허가건수.xlsx')
sam1.to_excel('d:\\out\\아산시_D112301_인허가중복_삼성전자.xlsx')
sam11.to_excel('d:\\out\\아산시_D112302_인허가원천데이터_삼성전자.xlsx')
sam2.to_excel('d:\\out\\아산시_D112303_인허가중복_경보제약.xlsx')
sam3.to_excel('d:\\out\\아산시_D112304_인허가중복_미소약국.xlsx')
sam4.to_excel('d:\\out\\아산시_D112305_인허가중복_주공세탁소.xlsx')

st1_01_upjong_lv1.to_excel('d:\\out\\아산시_D112701_업종대분류.xlsx')
st1_02_upjong_lv2.to_excel('d:\\out\\아산시_D112702_업종중분류.xlsx')

st_stat = living_com.groupby(['영업상태명']).size().reset_index()
st_stat.to_excel('d:\\out\\아산시_D112703_사업체상태.xlsx')

##  소매업종 업체별 인허가 건수
sam  = living_com[living_com['job_area'] == '소매업']
sam_cnt = sam.groupby(['좌표정보(x)', '좌표정보(y)', '사업장명']).size().reset_index()

sam01 = job_0826_sales[job_0826_sales['사업장명'] == '라벤더향기']

## 인허가 연도
living_com['begin_year'] = living_com['인허가일자'].str[:4]
living_com['begin_year'].head()

living_com['begin_yy'] = np.where(living_com['begin_year'] < '2000', '1999', living_com['begin_year'])

st_begin = living_com.groupby(['begin_yy']).size().reset_index()

st_begin2 = pd.crosstab(living_com["begin_yy"], living_com["영업상태명"], margins=True).reset_index()
st_begin2.to_excel('d:\\out\\아산시_D112704_인허가연도별상태.xlsx')

## 폐업, 휴업 연도

comdb = living_com

comdb['stop_year'] = np.where(comdb['휴업종료일자'].isnull(), comdb['휴업시작일자'].str[:4], '' )
comdb['default_year'] = comdb['폐업일자'].str[:4]

comdb['default_yy'] = np.where(comdb['default_year'].isnull(),comdb['stop_year'], comdb['default_year'] )
comdb['default_yy'] = np.where(comdb['default_yy'] < '2000', '1999', comdb['default_yy'])
comdb['comage'] = 2023 -  comdb['begin_year'].astype(int)

comdb['begin_gr'] = '00000'
comdb['begin_gr'] = np.where(comdb['begin_year'] < '2000', '1999이전', comdb['begin_gr'])
comdb['begin_gr'] = np.where((comdb['begin_year'] >= '2000') & (comdb['begin_year'] < '2005') , '2000~', comdb['begin_gr'])
comdb['begin_gr'] = np.where((comdb['begin_year'] >= '2005') & (comdb['begin_year'] < '2010') , '2005~', comdb['begin_gr'])
comdb['begin_gr'] = np.where((comdb['begin_year'] >= '2010') & (comdb['begin_year'] < '2015') , '2010~', comdb['begin_gr'])
comdb['begin_gr'] = np.where((comdb['begin_year'] >= '2015') & (comdb['begin_year'] < '2020') , '2015~', comdb['begin_gr'])
comdb['begin_gr'] = np.where((comdb['begin_year'] >= '2020') & (comdb['begin_year'] < '2025') , '2020~', comdb['begin_gr'])



st_default = comdb.groupby(['default_yy']).size().reset_index()
st_default.to_excel('d:\\out\\아산시_D112705_연도별폐업건수.xlsx')

comdb['폐업일자'].max()

## 업종별 정상 사업체 수
comdb2 = comdb[comdb['영업상태명'] == '영업/정상']

aa_01 = comdb2.groupby(['job_area']).size().reset_index()
aa_02 = comdb2.groupby(['job_area', 'job_cate']).size().reset_index()

aa_01.to_excel('d:\\out\\아산시_D1129_업종(정상업체).xlsx')
aa_02.to_excel('d:\\out\\아산시_D1129_업종상세(정상업체).xlsx')

## 업종별 / 인허가연도 분포
aa_02 = comdb2.groupby(['job_area', 'begin_year']).size().reset_index()
aa_02 = aa_02[aa_02['begin_year'] >= '2010']
aa_02.to_excel('d:\\out\\아산시_D1129_업종별등록연도(정상업체).xlsx')

## 업종별 업력
aa_03 = comdb2.groupby(['begin_gr']).size().reset_index()
aa_04 = pd.crosstab(comdb2["job_area"], comdb2["begin_gr"], margins=True)
aa_04.to_excel('d:\\out\\아산시_D1129_업종별등록연도그룹(정상).xlsx')

sam_upjong_lv1 = sam.groupby(['job_area']).size().reset_index()
sam_upjong_lv2 = sam.groupby(['job_area', 'job_cate']).size().reset_index()

sam_upjong_lv1.to_excel('d:\\out\\아산시_D112706_업종대분류(정상).xlsx')
sam_upjong_lv2.to_excel('d:\\out\\아산시_D112707_업종중분류(정상).xlsx')


## 업종별 상세업종 추이 : 소매업

sam = comdb2[comdb2['job_area'] == '소매업']
sam = sam[sam['begin_year'] >= '2010']
aa_05 = pd.crosstab(sam["begin_year"], sam["job_cate"], margins=True).reset_index()
aa_05.to_excel('d:\\out\\아산시_D1129_상세업종별등록연도그룹(소매업).xlsx')

## 업종별 상세업종 추이 : 여가생활

sam = comdb2[comdb2['job_area'] == '여가생활']
sam = sam[sam['begin_year'] >= '2010']
aa_05 = pd.crosstab(sam["begin_year"], sam["job_cate"], margins=True).reset_index()
aa_05.to_excel('d:\\out\\아산시_D1129_상세업종별등록연도그룹(여가생활).xlsx')

## 업종별 상세업종 추이 : 음식

sam = comdb2[comdb2['job_area'] == '음식']
sam = sam[sam['begin_year'] >= '2010']
aa_05 = pd.crosstab(sam["begin_year"], sam["job_cate"], margins=True).reset_index()
aa_05.to_excel('d:\\out\\아산시_D1129_상세업종별등록연도그룹(음식).xlsx')

## 업종별 상세업종 추이 : 숙박

sam = comdb2[comdb2['job_area'] == '숙박']
sam = sam[sam['begin_year'] >= '2010']
aa_05 = pd.crosstab(sam["begin_year"], sam["job_cate"], margins=True).reset_index()
aa_05.to_excel('d:\\out\\아산시_D1129_상세업종별등록연도그룹(숙박).xlsx')

## 업종별 상세업종 추이 : 생활서비스

sam = comdb2[comdb2['job_area'] == '생활서비스']
sam = sam[sam['begin_year'] >= '2010']
aa_05 = pd.crosstab(sam["begin_year"], sam["job_cate"], margins=True).reset_index()
aa_05.to_excel('d:\\out\\아산시_D1129_상세업종별등록연도그룹(생활서비스).xlsx')

## 업종별 상세업종 추이 : 의료

sam = comdb2[comdb2['job_area'] == '의료']
sam = sam[sam['begin_year'] >= '2010']
aa_05 = pd.crosstab(sam["begin_year"], sam["job_cate"], margins=True).reset_index()
aa_05.to_excel('d:\\out\\아산시_D1129_상세업종별등록연도그룹(의료).xlsx')

comdb2['comage'] = 2023 -  comdb2['begin_year'].astype(int)
comdb2.groupby('job_area')['comage'].mean().reset_index()


##### 업종별 상세업종 분석
## 업종별 정상/폐업 비율,  연도별 정상/폐업 추이..

## 업종별 상세업종 추이 : 음식

sam = comdb[comdb['job_area'] == '음식']
sam = sam[sam['run_yn'] == 1]
print(pd.crosstab(sam["job_cate"], sam["begin_gr"], margins=True).reset_index())
print(sam.groupby('job_cate')['comage'].mean().reset_index())

## 업종별 상세업종 추이 : 소매업

sam = comdb[comdb['job_area'] == '소매업']
print(pd.crosstab(sam["job_cate"], sam["run_yn"], margins=True).reset_index())

sam2 = sam[sam['run_yn'] == 1]
print(pd.crosstab(sam2["job_cate"], sam2["begin_gr"], margins=True).reset_index())
print(sam2.groupby('job_cate')['comage'].mean().reset_index())

## 업종별 상세업종 추이 : 생활서비스

sam = comdb[comdb['job_area'] == '생활서비스']
print(pd.crosstab(sam["job_cate"], sam["run_yn"], margins=True).reset_index())

sam2 = sam[sam['run_yn'] == 1]
print(pd.crosstab(sam2["job_cate"], sam2["begin_gr"], margins=True).reset_index())
print(sam2.groupby('job_cate')['comage'].mean().reset_index())

## 업종별 상세업종 추이 : 여가생활

sam = comdb[comdb['job_area'] == '여가생활']
print(pd.crosstab(sam["job_cate"], sam["run_yn"], margins=True).reset_index())

sam2 = sam[sam['run_yn'] == 1]
print(pd.crosstab(sam2["job_cate"], sam2["begin_gr"], margins=True).reset_index())
print(sam2.groupby('job_cate')['comage'].mean().reset_index())

## 업종별 상세업종 추이 : 의료

sam = comdb[comdb['job_area'] == '의료']
print(pd.crosstab(sam["job_cate"], sam["run_yn"], margins=True).reset_index())

sam2 = sam[sam['run_yn'] == 1]
print(pd.crosstab(sam2["job_cate"], sam2["begin_gr"], margins=True).reset_index())
print(sam2.groupby('job_cate')['comage'].mean().reset_index())

## 업종별 상세업종 추이 : 숙박

sam = comdb[comdb['job_area'] == '숙박']
print(pd.crosstab(sam["job_cate"], sam["run_yn"], margins=True).reset_index())

sam2 = sam[sam['run_yn'] == 1]
print(pd.crosstab(sam2["job_cate"], sam2["begin_gr"], margins=True).reset_index())
print(sam2.groupby('job_cate')['comage'].mean().reset_index())

## 상세업종별, 지역별, 이름별 Count

aa_00 = sam.groupby(['job_cate', 'dong', '사업장명']).size().reset_index()

aa_001 = sam[(sam['dong'] == '온천동') & (sam['사업장명'] == '갤러리')]
aa_002 = sam[(sam['dong'] == '실옥동') & (sam['사업장명'] == 'CF치킨')]

## 업종별 상세업종 추이 : 소매업

sam = comdb[comdb['job_area'] == '소매업']
# sam = sam[sam['begin_year'] >= '2010']
print(sam.groupby('run_yn').size().reset_index())
print(pd.crosstab(sam["job_cate"], sam["run_yn"], margins=True).reset_index())
print(pd.crosstab(sam["begin_yy"], sam["run_yn"], margins=True).reset_index())
sam2 = sam[sam['run_yn'] == 1]
print(sam2.groupby('job_cate')['comage'].mean().reset_index())

aa_05 = pd.crosstab(sam["begin_year"], sam["job_cate"], margins=True).reset_index()
aa_05.to_excel('d:\\out\\아산시_D1129_상세업종별등록연도그룹(소매업).xlsx')

## 주소정제
comdb['addr_1'] = np.where(comdb['소재지전체주소'].isnull(), 0, 1)
comdb['addr_2'] = np.where(comdb['도로명전체주소'].isnull(), 0, 1)
comdb['addr_type'] = np.where((comdb['addr_1'] == 1 ) & (comdb['addr_2'] == 1 ), 1,
                        np.where((comdb['addr_1'] == 1 ) & (comdb['addr_2'] == 0 ), 2,
                                 np.where((comdb['addr_1'] == 0 ) & (comdb['addr_2'] == 1 ), 3, 0)))

st_addr = comdb.groupby(['addr_type']).size().reset_index()

comdb['addr1_1'] = comdb['소재지전체주소'].str.split(' ').str[0]
comdb['addr1_2'] = comdb['소재지전체주소'].str.split(' ').str[1]
comdb['addr1_3'] = comdb['소재지전체주소'].str.split(' ').str[2]

comdb['addr2_1'] = comdb['도로명전체주소'].str.split(' ').str[0]
comdb['addr2_2'] = comdb['도로명전체주소'].str.split(' ').str[1]
comdb['addr2_3'] = comdb['도로명전체주소'].str.split(' ').str[2]

comdb['addr1_re'] =  comdb['addr1_2'] + ' ' + comdb['addr1_3']
comdb['addr2_re'] =  comdb['addr2_2'] + ' ' + comdb['addr2_3']

## 주소분포

addr_list = comdb[['addr1_re', 'addr2_re']]
addr_list.columns = ['소재지주소', '도로명주소']

### 할일  : 법정동 '1'인 값을 기준으로 빈도표 뽑아서... 주소분류 체계 확정

st_addr1 = addr_list.groupby(['소재지주소']).size().reset_index()
st_addr1.to_excel('d:\\out\\아산시_D112801_주소읍면동건수.xlsx')

st_addr2 = addr_list.groupby(['소재지주소', '도로명주소']).size().reset_index()

st_addr3 = comdb[['addr1_re', 'addr2_re','addr1_3']]
st_addr3_stat = st_addr3.groupby(['addr1_3']).size().reset_index()
st_addr3_stat.to_excel('d:\\out\\아산시_D112902_주소읍면동건수(원본).xlsx')

sam1 = comdb[comdb['addr1_re'] == '아산시 ']
sam1 = sam1[['개방서비스명', '인허가일자', '영업상태명', '소재지전체주소', '도로명전체주소']]


comdb['dong'] = comdb['addr1_3']
comdb['dong'] = np.where(comdb['addr1_re'] == '아산시 온천1동', '온천동', comdb['dong'])
comdb['dong'] = np.where(comdb['addr1_re'] == '아산시 온양1동', '온천동', comdb['dong'])
comdb['dong'] = np.where(comdb['addr1_re'] == '아산시 온천2동', '온천동', comdb['dong'])
comdb['dong'] = np.where(comdb['addr1_re'] == '아산시 온양*동', '온천동', comdb['dong'])
comdb['dong'] = np.where(comdb['addr1_re'] == '아산시 온양2동', '온천동', comdb['dong'])
comdb['dong'] = np.where(comdb['addr1_re'] == '아산시 온천2동222-8', '온천동', comdb['dong'])
comdb['dong'] = np.where(comdb['addr1_re'] == '아산시 배방면', '배방읍', comdb['dong'])
comdb['dong'] = np.where(comdb['addr1_re'] == '모종동 ***-*', '모종동', comdb['dong'])
comdb['dong'] = np.where(comdb['addr1_re'] == '아산시 번영로***번길', '권곡동', comdb['dong'])
comdb['dong'] = np.where(comdb['addr1_re'] == '아산시 장존동305-7', '장존동', comdb['dong'])

comdb['dong'] = np.where(comdb['소재지전체주소'] == '충청남도 아산시  공수리 배방택지개발지구 26블록 6롯트 배방메디칼센터 1층', '배방읍', comdb['dong'])
comdb['dong'] = np.where(comdb['소재지전체주소'] == '충청남도 아산시  555번지 9호', '모종동', comdb['dong'])
comdb['dong'] = np.where(comdb['소재지전체주소'] == '충청남도 아산시  ***번지 아산아이파크 ***동 ****호', '풍기동', comdb['dong'])
comdb['dong'] = np.where(comdb['소재지전체주소'] == '충청남도 아산시  공수리 ***번지 한라비발디 ***동 ***호', '배방읍', comdb['dong'])

sam2 = comdb.groupby(['dong']).size().reset_index()
sam2.to_excel('d:\\out\\아산시_D112901_주소읍면동건수(보정).xlsx')

comdb.columns

comdb['run_yn'] = np.where(comdb['영업상태명'] == '영업/정상', 1, 0)
comdb['stop_yn'] = np.where(comdb['영업상태명'] != '영업/정상', 1, 0)

comdb.groupby(['run_yn']).size().reset_index()
comdb.groupby(['stop_yn']).size().reset_index()


## 지역별 정상업종 비율
sam2 = comdb.groupby('dong').agg({'run_yn':'sum', 'stop_yn':'sum'}).reset_index()
sam2.to_excel('d:\\out\\아산시_D112903_행정동별정상업체비율.xlsx')


## 지역별 업종별 분포 (정상업체)

area = comdb[comdb['run_yn'] == 1]

sam = area.groupby(['dong', 'job_area']).size().reset_index()
sam.columns = ['dong', 'job_area', 'cnt']
sam.to_excel('d:\\out\\아산시_D1204_행정동별업종별분포.xlsx')


## 동별/업종별 비율 정보 추가 : 행정동별 업종별 건수, 비율.  아산시 전체 업종별 비율

sam1 = area.groupby(['job_area']).size().reset_index()
sam1.columns = ['job_area', 'job_cnt']
sam1['job_totrt'] = sam1['job_cnt'] / sam1['job_cnt'].sum()


sam2 = area.groupby(['dong']).size().reset_index()
sam2.columns = ['dong', 'dong_cnt']


sam3 = pd.merge(sam, sam2, how = 'left', on = 'dong')
sam3['dong_rt'] = sam3['cnt'] /sam3['dong_cnt']

sam3 = pd.merge(sam3, sam1, how = 'left', on = 'job_area')
# sam2['job_rt'] = sam2['cnt'] /sam2['job_cnt']
sam2 = pd.merge(sam2, sam1_2, how = 'left', on = 'dong')

sam3.to_excel('d:\\out\\아산시_D1204_행정동별업종별분포2.xlsx')

## 행정동별 업종별 인허가수 산출
living_cnt = pd.crosstab(area["dong"], area["job_area"], margins=True).reset_index()
living_cnt.to_pickle('living_cnt.pkl')



##################################################################################################

## 카드 데이터 분석  : living_card

living_card = pd.read_pickle('living_card.pkl')

## BC카드 업종 대분류 정보 생성
card_bizcd = pd.read_excel('카드업종_대분류.xlsx', dtype=str)
card_bizcd.columns = ['bizcd', 'biznm']

##########################################

living_card = living_card.fillna(0)
living_card['year'] = living_card['CRTR_YM'].astype('str').str[:4]
living_card['bizcd'] = living_card['TOBIZ_CD'].astype('str').str[:2]

card = living_card

## 지역별 카드 매출액 (2023)
card_s =living_card[living_card['year'] == '2023']

sam1 = card_s.groupby(['STDG_NM','CRTR_YM' ])['USE_AMT_SUM'].sum().reset_index()
sam11 = sam1.groupby(['STDG_NM'])['USE_AMT_SUM'].mean().reset_index()
sam11.to_excel('d:\\out\\아산시_D1213_지역별카드사용액(2023).xlsx')

## 지역별 카드 매출액 증감 (연간 매출액)

sam2 = card.groupby(['STDG_NM', 'year', 'CRTR_YM' ])['USE_AMT_SUM'].sum().reset_index()
sam21 = sam2.groupby(['STDG_NM', 'year'])['USE_AMT_SUM'].mean().reset_index()
sam3 = sam21.groupby(['year'])['USE_AMT_SUM'].sum().reset_index()

sam3.to_excel('d:\\out\\아산시_D1214_아산시연간카드사용액.xlsx')

sam4 = sam21.pivot(index='STDG_NM', columns='year', values='USE_AMT_SUM').reset_index()
sam4.to_excel('d:\\out\\아산시_D1214_지역별연간월평균사용액.xlsx')


##  요일분석, 시간대분석,  개인법인분석,
card_week = card[['year','STDG_NM','CRTR_YM' , 'MON_USE_AMT', 'TUES_USE_AMT', 'WEDNES_USE_AMT',
       'THURS_USE_AMT', 'FRI_USE_AMT', 'SATUR_USE_AMT', 'SUN_USE_AMT']]

card_week = card_week.groupby(['STDG_NM', 'year']).sum().reset_index()

card_week_y = card_week[['STDG_NM','year', 'MON_USE_AMT', 'TUES_USE_AMT', 'WEDNES_USE_AMT',
                           'THURS_USE_AMT', 'FRI_USE_AMT', 'SATUR_USE_AMT', 'SUN_USE_AMT']]

card_week_y = card_week_y.groupby(['STDG_NM', 'year']).mean().reset_index()

card_week_2023 = card_week_y[card_week_y['year'] == '2023']
card_week_2023['day_mean'] = (card_week_2023['MON_USE_AMT']+card_week_2023['TUES_USE_AMT']+card_week_2023['WEDNES_USE_AMT']+
                              card_week_2023['THURS_USE_AMT']+card_week_2023['FRI_USE_AMT']) / 5
card_week_2023['week_mean'] = (card_week_2023['SATUR_USE_AMT']+card_week_2023['SUN_USE_AMT']) / 2
card_week_2023['week_rt'] =  card_week_2023['week_mean'] / card_week_2023['day_mean']

card_week_2023.to_excel('d:\\out\\아산시_D1214_행정동요일사용금액.xlsx')


## 업종 카드사용액 (2023)

card_s['bizcd'] = card_s['TOBIZ_CD'].astype('str').str[:2]
card_s = pd.merge(card_s, card_bizcd, how = 'left' , on = 'bizcd')

sam0 = card_s.groupby(['biznm', 'year', 'CRTR_YM' ])['USE_AMT_SUM'].sum().reset_index()
sam0_1 = sam0.groupby(['biznm', 'year'])['USE_AMT_SUM'].mean().reset_index()

## 업종 상세 (2023)
card_biz = card_s.groupby(['biznm'])['USE_AMT_SUM'].sum().reset_index()
card_biz.to_excel('d:\\out\\아산시_D1214_업종별사용액_2023.xlsx')

card_biz2 = card_s.groupby(['biznm', 'TOBIZ_NM'])['USE_AMT_SUM'].sum().reset_index()
card_biz2.to_excel('d:\\out\\아산시_D1214_업종상세별사용액_2023.xlsx')


## 업종별 연도별 카드매출액 월평균

card = pd.merge(card, card_bizcd, how = 'left' , on = 'bizcd')

sam = card.groupby(['biznm', 'year', 'CRTR_YM' ])['USE_AMT_SUM'].sum().reset_index()
sam1 = sam.groupby(['biznm', 'year'])['USE_AMT_SUM'].mean().reset_index()
sam1_1 = sam1.pivot(index='biznm', columns='year', values='USE_AMT_SUM').reset_index()
sam1_1.columns =  ['biznm', 'yr_2019', 'yr_2020', 'yr_2021', 'yr_2022', 'yr_2023']
sam1_1['add_rt'] =  (sam1_1['yr_2023']  - sam1_1['yr_2019']) / sam1_1['yr_2019']

sam1_1.to_excel('d:\\out\\아산시_D1214_업종별사용액증감율.xlsx')


## 업종별 지역별 카드매출액 월평균
sam2 = card.groupby(['biznm', 'STDG_NM', 'year', 'CRTR_YM' ])['USE_AMT_SUM'].sum().reset_index()
sam2_1 = card.groupby(['biznm', 'STDG_NM', 'year' ])['USE_AMT_SUM'].mean().reset_index()
sam2_2 = sam2_1.pivot(index= (['biznm','STDG_NM']) , columns='year', values='USE_AMT_SUM').reset_index()

sam2_2.to_excel('d:\\out\\아산시_D1214_업종별지역별증감율.xlsx')

##### 상관관계 분석  : 인허가수가 2023기준이라 증감율 의미 없음

## 2023 금액기준,  음식 업종 금액 기준,   주말 비율,

living_cnt = pd.read_pickle('living_cnt.pkl')
living_cnt.columns = ['EMD_NM', '생활서비스', '소매업', '숙박', '여가생활', '음식', '의료', 'All']
living_cnt =  living_cnt.loc[living_cnt['EMD_NM'] != 'All']
living_cnt['기타인허가'] = living_cnt['생활서비스'] + living_cnt['숙박'] + living_cnt['여가생활'] + living_cnt['의료']

## 2023년 월사용액

## 음식업종
card_cnt_1 = sam11
card_cnt_2 = sam2_2[sam2_2['biznm'] == '일반/휴게음식']
card_cnt_2 = card_cnt_2[['STDG_NM', '2023']]
card_cnt_2.columns = ['STDG_NM', '음식업종금액']
card_cnt_3 = card_week_2023[['STDG_NM', 'week_rt']]

card_cnt = pd.merge(card_cnt_1, card_cnt_2, how = 'left', on = 'STDG_NM')
card_cnt = pd.merge(card_cnt, card_cnt_3, how = 'left', on = 'STDG_NM')

card_cnt.to_pickle('card_cnt.pkl')

## cordb 생성
card_cnt.columns = ['EMD_NM', 'USE_AMT_SUM', '음식업종금액', 'week_rt']
cordb = pd.merge(living_cnt,card_cnt, how = 'left', on = 'EMD_NM')

pearsonr(cordb['USE_AMT_SUM'], cordb['All'])        # 카드사용금액  vs. 인허가전체
pearsonr(cordb['USE_AMT_SUM'], cordb['소매업'])      # 소매업인허가
pearsonr(cordb['USE_AMT_SUM'], cordb['음식'])        # 음식업인허가
pearsonr(cordb['USE_AMT_SUM'], cordb['기타인허가'])   # 기타인허가

pearsonr(cordb['음식업종금액'], cordb['All'])        #
pearsonr(cordb['week_rt'], cordb['All'])        # 주말비율 

cordb.to_excel('d:\\out\\아산시_D1212_card_상관관계분석.xlsx')




## 분석설계를 위한 분석 프로그램 (최초 분석내용)

# cllist_1 = pd.DataFrame(card_2308.columns)
# cllist_1.columns = ['list1']
# cllist_2 = pd.DataFrame(card_st_2308.columns)
# cllist_2.columns = ['list2']
# cl_list_3 = pd.concat([cllist_1, cllist_2], axis = 1)

# card_2308['USE_AMT_SUM'] = card_2308['USE_AMT_SUM'].astype('int')
# card_st_2308['USE_AMT_SUM'] = card_st_2308['USE_AMT_SUM'].astype('int')

# st_carduse1 = card_2308.groupby(['DONG_NM'])['USE_AMT_SUM'].sum().reset_index()
# st_carduse1.to_excel('d:\\out\\아산시_D1107_지역별카드사용금액.xlsx')

# st_carduse2 = card_st_2308.groupby(['STDG_NM'])['USE_AMT_SUM'] .sum().reset_index()
# st_carduse2.to_excel('d:\\out\\아산시_D1107_지역별카드사용금액2.xlsx')


####################################################################################################
####################################################################################################
####################################################################################################

## 업종 분류

# 인허가 데이터 업종 분류 기준 생성

## 업종, 영업상태 분포

comdb = living_comdb
## 업종 분류
comdb['cate_1'] = 'C_' + comdb['개방서비스아이디'].str[:2]
comdb['cate_2'] = 'C_' + comdb['개방서비스아이디'].str[:5]
comdb['yn'] = 1

comdb = pd.merge(comdb, industry_lv1, how = 'left', on = 'cate_1' )
comdb = pd.merge(comdb, industry_lv2, how = 'left', on = 'cate_2' )

st_cate = comdb.groupby(['catenm_1', 'catenm_2', '개방서비스명' ]).size().reset_index()

st_cate.to_excel('d:\\out\\아산시_D1120_업종카테고리.xlsx')


industry_lv1.columns = ['cate_1', 'catenm_1']
industry_lv2.columns = ['cate_2', 'catenm_2']

st_cate1 = pd.merge(st_cate1, industry_lv1, how = 'left', on = 'cate_1' )
st_cate2 = pd.merge(st_cate2, industry_lv2, how = 'left', on = 'cate_2' )

st_stat2 =  comdb.groupby(['catenm_1', 'catenm_2', '개방서비스명'])['yn'].sum().reset_index()

st_cate1.to_excel('d:\\out\\아산시_D1107_업종카테고리_대분류.xlsx')
st_cate2.to_excel('d:\\out\\아산시_D1107_업종카테고리_중분류.xlsx')
st_stat2.to_excel('d:\\out\\아산시_D1107_업종카테고리_소분류.xlsx')



####################################################################################################
####################################################################################################

##### KCB 데이터 분석

## 분석데이터 불러오기 : 월별 법정동별 연령대별 정보

kcb = pd.read_pickle('living_kcb4.pkl')

# 동별 합산정보 생성
kcb_dong = kcb[['CRTR_YM','dong','NOPE','ML_NOPE','FM_NOPE','SLR_NOPE','S_OWNR_NOPE','ETC_NOPE','FRGNR_NOPE',
                'CARD_OWRN_NOPE', 'LON_OWNR_NOPE','CR_LON_OWNR_NOPE','HOUSE_LON_OWRN_NOPE', 'PLC_LON_OWRN_NOPE',
                'incm_nope', 'incm_sum', 'card_usesum', 'lon_sum', 'crlon_sum', 'houselon_sum' ]]

kcb_dong = kcb_dong.groupby(['CRTR_YM','dong']).sum().reset_index()
kcb_dong['incm_avg'] = round(kcb_dong['incm_sum'] / kcb_dong['incm_nope'])
kcb_dong['card_avg'] = round(kcb_dong['card_usesum'] / kcb_dong['CARD_OWRN_NOPE'])
kcb_dong['lon_avg'] = round(kcb_dong['lon_sum'] / kcb_dong['LON_OWNR_NOPE'])
kcb_dong['crlon_avg'] = round(kcb_dong['crlon_sum'] / kcb_dong['CR_LON_OWNR_NOPE'])
kcb_dong['houselon_avg'] = round(kcb_dong['houselon_sum'] / kcb_dong['HOUSE_LON_OWRN_NOPE'])

kcb_dong = pd.merge(kcb_dong, addr_nm, how = 'left', on = 'dong')

kcb_s = kcb_dong[kcb_dong['CRTR_YM'] == 202308]
kcb_s['NOPE'].sum()             # 300426
kcb_s['ML_NOPE'].sum()          # 162041
kcb_s['FM_NOPE'].sum()          # 138385
kcb_s['incm_nope'].sum()        # 300426
kcb_s['CARD_OWRN_NOPE'].sum()   # 275002
kcb_s['LON_OWNR_NOPE'].sum()    # 113365
kcb_s['CR_LON_OWNR_NOPE'].sum()    # 81326
kcb_s['HOUSE_LON_OWRN_NOPE'].sum() # 31424

## 행정동별 인구수
kcb_s.to_excel('d:\\out\\아산시_D1205_KCB_202308.xlsx')

## 행정동별 급여소득자수 증감율

kcb_s0 = kcb_dong[kcb_dong['CRTR_YM'] == 201601]
kcb_s01 =  kcb_s0.groupby(['STDG_NM'])['SLR_NOPE'].sum().reset_index()
kcb_s01.to_excel('d:\\out\\아산시_D1205_KCB_201601.xlsx')

## 행정동별 급여소득자수 증감추이 (연평균 산출 비교)
kcb_yy = kcb_dong[['CRTR_YM','STDG_NM', 'SLR_NOPE', 'incm_avg', 'card_avg', 'lon_avg']]
kcb_yy['year'] = kcb_dong['CRTR_YM'].astype('str').str[:4]
kcb_yy = kcb_yy[['year','STDG_NM', 'SLR_NOPE', 'incm_avg', 'card_avg', 'lon_avg']]
kcb_yy2 = kcb_yy.groupby(['STDG_NM','year']).mean().reset_index()

kcb_2016 = kcb_yy2[kcb_yy2['year'] == '2016']
kcb_2023 = kcb_yy2[kcb_yy2['year'] == '2023']
kcb_2016.columns = ['STDG_NM', 'year', 'SLR_2016', 'incm_2016', 'card_2016', 'lon_2016']
kcb_2023.columns = ['STDG_NM', 'year', 'SLR_2023', 'incm_2023', 'card_2023', 'lon_2023']
kcb_2016 = kcb_2016[['STDG_NM', 'SLR_2016', 'incm_2016', 'card_2016', 'lon_2016']]
kcb_2023 = kcb_2023[['STDG_NM', 'SLR_2023', 'incm_2023', 'card_2023', 'lon_2023']]

kcb_yyrt = pd.merge(kcb_2016, kcb_2023, how = 'left', on = 'STDG_NM')
kcb_yyrt['slr_rt'] = (kcb_yyrt['SLR_2023'] -  kcb_yyrt['SLR_2016'] ) / kcb_yyrt['SLR_2016']
kcb_yyrt['incm_rt'] = (kcb_yyrt['incm_2023'] -  kcb_yyrt['incm_2016'] ) / kcb_yyrt['incm_2016']
kcb_yyrt['card_rt'] = (kcb_yyrt['card_2023'] -  kcb_yyrt['card_2016'] ) / kcb_yyrt['card_2016']
kcb_yyrt['lon_rt'] = (kcb_yyrt['lon_2023'] -  kcb_yyrt['lon_2016'] ) / kcb_yyrt['lon_2016']

kcb_yyrt.to_excel('d:\\out\\아산시_D1206_KCB_연간증감율.xlsx')
kcb_yy2.to_excel('d:\\out\\아산시_D1206_KCB_지역별증감율.xlsx')

## 상관관계 분석 :  행정동별 인허가수 vs. 급여소득자, 카드사용액, 대출금액 상관분석

living_cnt.columns = ['STDG_NM', '생활서비스', '소매업', '숙박', '여가생활', '음식', '의료', 'All']

kcb_corr = pd.merge(kcb_s, living_cnt, how = 'left' , on = 'STDG_NM')

kcb_corr.corr(kcb_corr['SLR_NOPE'],   kcb_corr['All'])

from scipy.stats import pearsonr
correlation_coefficient, p_value =  pearsonr(kcb_corr['SLR_NOPE'], kcb_corr['All'])
print(f"Pearson 상관계수: {correlation_coefficient, p_value}")

pearsonr(kcb_corr['SLR_NOPE'], kcb_corr['소매업'])   # 소매업인허가 vs. 급여소득자
pearsonr(kcb_corr['SLR_NOPE'], kcb_corr['음식'])   # 소매업인허가 vs. 급여소득자

kcb_corr['기타인허가'] = kcb_corr['생활서비스'] + kcb_corr['숙박'] + kcb_corr['여가생활'] + kcb_corr['의료']
pearsonr(kcb_corr['SLR_NOPE'], kcb_corr['기타인허가'])   # 기타인허가 vs. 급여소득자

pearsonr(kcb_corr['card_avg'], kcb_corr['기타인허가'])   # 기타인허가 vs. 급여소득자
pearsonr(kcb_corr['lon_avg'], kcb_corr['기타인허가'])   # 기타인허가 vs. 급여소득자

np.corrcoef(kcb_corr['SLR_NOPE'],   kcb_corr['All'])

kcb_time_slr = kcb_dong[['CRTR_YM','STDG_NM', 'SLR_NOPE' ]]
kcb_time_slr_01 =  kcb_time_slr[kcb_time_slr['STDG_NM'] == '실옥동']
kcb_time_slr_02 =  kcb_time_slr[kcb_time_slr['STDG_NM'] == '신인동']
kcb_time_slr_03 =  kcb_time_slr[kcb_time_slr['STDG_NM'] == '둔포면']
kcb_time_slr_04 =  kcb_time_slr[kcb_time_slr['STDG_NM'] == '법곡동']

####################################################################################################
####################################################################################################

##### TMAP 데이터 분석 : 20190101 ~ 20230831

## 분석데이터 불러오기 : 월별 법정동별 연령대별 정보

tmap = pd.read_pickle('living_tmap.pkl')

tmap['ym'] = tmap['drv_ymd'].astype('str').str[:6]
tmap['year'] = tmap['drv_ymd'].astype('str').str[:4]

# 업종별, 지역별 가게수 Count 위해 좌표 + 가게이름 Key 생성
tmap['id'] =  tmap['dstn_coord_x'].astype('str').str[:9] + '_' + tmap['dstn_coord_y'].astype('str').str[:9] + '_' + tmap['dstn_nm']

tmap_s = tmap[tmap['year'] == '2023']

## 목적지별 건수 합 : 좌표로 하는 것이 더 많은 목적지가 생성되나.. 읍면동 분석을 위해 주소 기준으로 적용(건수 낮은 곳 증가)
tmaps_dstn = tmap_s.groupby(['id','dstn_nm'])['vst_cnt'].sum().reset_index()
tmaps_dstn = tmaps_dstn.sort_values('vst_cnt', ascending = False)  # False 내림차순
tmaps_dstn_top100 = tmaps_dstn.head(100)

## 티맵 업종 중복 현황 분석
tmaps_cate = tmap_s[['dstn_addr','dstn_nm', 'dstn_ctgy']].drop_duplicates()
tmaps_dupcnt = tmaps_cate.groupby(['dstn_addr','dstn_nm']).size().reset_index()

tmaps_cate[tmaps_cate['dstn_addr'] == '충남 아산시 신창면 남성리 101-3']
tmaps_cate[tmaps_cate['dstn_addr'] == '충남 아산시 음봉면 산동리 293-3']


sam = tmap[(tmap['dstn_addr'] == '충남 아산시 신창면 남성리 101-3') & (tmap['dstn_nm'] == 'N마트/아산신창점')]
sam = sam.groupby(['dstn_ctgy', 'ym']).size().reset_index()

sam2 = tmap[(tmap['dstn_addr'] == '충남 아산시 음봉면 산동리 293-3') & (tmap['dstn_nm'] == '대영이엔씨')]
sam2 = sam2.groupby(['dstn_ctgy', 'ym']).size().reset_index()

sam.to_excel('d:\\out\\아산시_D1207_tmap_업종변경예시1.xlsx')
sam2.to_excel('d:\\out\\아산시_D1207_tmap_업종변경예시2.xlsx')

## 티맵 업종정보 생성 :  최근정보 없는 목적지 업종 정보 생성을 위해 2개 이상인 경우만 2023.06 ~ 08 3개월 데이터로 업종정보 생성
tmaps_dupcnt = tmap.groupby(['id', 'dstn_ctgy']).size().reset_index()
tmaps_dupcnt = tmaps_dupcnt[['id', 'dstn_ctgy']]
tmaps_dupcnt2 = tmaps_dupcnt.groupby(['id']).size().reset_index()
tmaps_dupcnt2.columns = ['id', 'dupcnt']

tmaps_cate1 = tmaps_dupcnt2[tmaps_dupcnt2['dupcnt'] == 1]
tmaps_cate2 = tmaps_dupcnt2[tmaps_dupcnt2['dupcnt'] > 1]
tmaps_cate1 = pd.merge(tmaps_cate1, tmaps_dupcnt, how = 'left', on = 'id')

# 최근 3개월 업종 정보
sam2 = tmap[tmap['ym'] > '202306']
sam2 = sam2.groupby(['id','dstn_ctgy']).size().reset_index()
sam2 = sam2[['id', 'dstn_ctgy']]
tmaps_cate2 = pd.merge(tmaps_cate2, sam2, how = 'left', on = 'id')

tmaps_cate = pd.concat([tmaps_cate1, tmaps_cate2], axis = 0)
tmaps_cate['cate_lv1'] = tmaps_cate['dstn_ctgy'].str.split('_').str[0]
tmaps_cate['cate_lv2'] = tmaps_cate['dstn_ctgy'].str.split('_').str[1]
tmaps_cate['cate_lv3'] = tmaps_cate['dstn_ctgy'].str.split('_').str[2]

tmaps_cate.to_pickle('tmaps_cate.pkl')

# 상위 100개 목적지에 업종정보 추가
tmaps_dstn_top100 = pd.merge(tmaps_dstn_top100, tmaps_cate, how = 'left', on = 'id')

tmaps_dstn_top100.to_excel('d:\\out\\아산시_D1207_tmap_top100.xlsx')

## 업종별 방문건수 분포
tmaps_cate = tmaps_cate[['id', 'cate_lv1', 'cate_lv2', 'cate_lv3']]
tmap = pd.merge(tmap, tmaps_cate, how ='left', on = 'id')
tmaps_dstn = tmap_s.groupby(['id','dstn_nm'])['vst_cnt'].sum().reset_index()
tmap.to_pickle('tmap2.pkl')

##### 데이터 전처리 후 분석을 위한 데이터샛 호출

tmap2 = pd.read_pickle('tmap2.pkl')    # ID, 업종정보 추가된 데이터샛

# 업종 대분류별 목적지 수, Tmap 방문건수 합계

tmap_s = tmap2[tmap2['year'] == '2023']

aa1 = tmap_s.groupby(['cate_lv1', 'id'])['vst_cnt'].sum().reset_index()
aa2 = tmap_s.groupby(['cate_lv1'])['vst_cnt'].sum().reset_index()
aa3 = tmap_s.groupby(['cate_lv1']).size().reset_index()

## 중분류 기준
aa4 = tmap_s.groupby(['cate_lv1', 'cate_lv2'])['vst_cnt'].sum().reset_index()
aa4_1 = tmap_s.groupby(['cate_lv1', 'cate_lv2', 'cate_lv3'])['vst_cnt'].sum().reset_index()
aa4_2 = tmap_s[tmap_s['cate_lv1'] == 'AOI']
aa4_3 = tmap_s[tmap_s['cate_lv3'] == '주차장']

aa2.to_excel('d:\\out\\아산시_D1211_tmap_업종건수.xlsx')
aa3.to_excel('d:\\out\\아산시_D1211_tmap_업종별사업체갯수.xlsx')
aa4.to_excel('d:\\out\\아산시_D1211_tmap_업종중분류.xlsx')
aa4_1.to_excel('d:\\out\\아산시_D1211_tmap_업종소분류.xlsx')

## 업종별 연간 시계열
aa1 = tmap2.groupby(['cate_lv1', 'year'])['vst_cnt'].sum().reset_index()
aa1.to_excel('d:\\out\\아산시_D1211_tmap_업종연간증감.xlsx')

## 업종별 지역별 구성비, 증감추이
aa2 = tmap_s.groupby(['cate_lv1', 'STDG_NM'])['vst_cnt'].sum().reset_index()
aa2.to_excel('d:\\out\\아산시_D1211_tmap_업종별지역분포.xlsx')

aa4_4 = tmap_s[tmap_s['cate_lv3'] == '농장/농원']

## 지역별 외지인 분석 : 당일 출발지 아산시...

tmap_s['local_yn'] = np.where(tmap_s['frst_dptre_sgg_nm'] == '아산시', 1, 0)

sam1 = tmap_s[tmap_s['local_yn'] == 1]
sam0 = tmap_s[tmap_s['local_yn'] == 0]

sam1 = sam1.groupby(['STDG_NM'])['vst_cnt'].sum().reset_index()
sam0 = sam0.groupby(['STDG_NM'])['vst_cnt'].sum().reset_index()

sam1.columns = ['STDG_NM', 'vst_local']
sam0.columns = ['STDG_NM', 'vst_out']

sam2 = pd.merge(sam1, sam0, how = 'left', on = 'STDG_NM')
sam2['out_rt'] = sam2['vst_out']  / (sam2['vst_out'] +  sam2['vst_local'])
sam2.to_excel('d:\\out\\아산시_D1212_tmap_지역별 외부 방문비율.xlsx')

## 목적지별 외지인방문 비율

sam11 = tmap_s[tmap_s['local_yn'] == 1]
sam01 = tmap_s[tmap_s['local_yn'] == 0]

sam11 = sam11.groupby(['STDG_NM', 'id'])['vst_cnt'].sum().reset_index()
sam01 = sam01.groupby(['STDG_NM', 'id'])['vst_cnt'].sum().reset_index()
sam02 = tmap_s.groupby(['STDG_NM', 'id'])['vst_cnt'].sum().reset_index()

sam11.columns = ['STDG_NM', 'id', 'vst_local']
sam01.columns = ['STDG_NM', 'id', 'vst_out']

sam3 = pd.merge(sam02, sam11, how = 'left', on = ['STDG_NM', 'id'])
sam3 = pd.merge(sam3, sam01, how = 'left', on = ['STDG_NM', 'id'])
sam3['out_rt'] = sam3['vst_out']  /sam3['vst_cnt']

sam3_1 = sam3[sam3['STDG_NM'] == '선장면']
sam3_2 = sam3[sam3['STDG_NM'] == '음봉면']


##### 상관관계 분석

living_cnt = pd.read_pickle('living_cnt.pkl')
living_cnt.columns = ['EMD_NM', '생활서비스', '소매업', '숙박', '여가생활', '음식', '의료', 'All']
living_cnt =  living_cnt.loc[living_cnt['EMD_NM'] != 'All']
living_cnt['기타인허가'] = living_cnt['생활서비스'] + living_cnt['숙박'] + living_cnt['여가생활'] + living_cnt['의료']

## Tmap 변수 생성
tmap_cnt.columns

tmap_cnt['tmap_cnt'] = tmap_cnt['vst_local']  + tmap_cnt['vst_out']
tmap_2 = aa2[aa2['cate_lv1'] == '생활편의']
tmap_2 = tmap_2[['STDG_NM', 'vst_cnt']]
tmap_cnt = pd.merge(tmap_cnt, tmap_2, how = 'left', on = 'STDG_NM')
tmap_cnt = tmap_cnt[['STDG_NM', 'tmap_cnt', 'vst_cnt', 'out_rt']]
tmap_cnt.columns = ['EMD_NM', 'tmap_cnt', '생활편의건수', '외부방문비율']

## cordb 생성
cordb = pd.merge(living_cnt, tmap_cnt, how = 'left', on = 'EMD_NM')

pearsonr(cordb['tmap_cnt'], cordb['All'])        # 티맵건수  vs. 인허가전체
pearsonr(cordb['tmap_cnt'], cordb['소매업'])      # 소매업인허가
pearsonr(cordb['tmap_cnt'], cordb['음식'])        # 음식업인허가
pearsonr(cordb['tmap_cnt'], cordb['기타인허가'])   # 기타인허가

pearsonr(cordb['생활편의건수'], cordb['All'])        # 30세이하 유동인구
pearsonr(cordb['외부방문비율'], cordb['All'])        # 30세이하 유동인구

cordb.to_excel('d:\\out\\아산시_D1212_TMAP_상관관계분석.xlsx')


#################################################################################################

## 유동인구 데이터 분석

skt_2023 = pd.read_pickle('living_skt_2023.pkl')
skt_point_asan = pd.read_pickle('skt_point_asan.pkl')

## 행정동 정보 추가

skt_2023['flow_10'] = (skt_2023['ML_FLOW_PPLTN_CNT_10_BELOW']+skt_2023['ML_FLOW_PPLTN_CNT_10_14']+skt_2023['ML_FLOW_PPLTN_CNT_15_19'] +
                      skt_2023['FM_FLOW_PPLTN_CNT_10_BELOW']+skt_2023['FM_FLOW_PPLTN_CNT_10_14']+skt_2023['FM_FLOW_PPLTN_CNT_15_19'])
skt_2023['flow_20'] = (skt_2023['ML_FLOW_PPLTN_CNT_20_24']+skt_2023['ML_FLOW_PPLTN_CNT_25_29'] +
                      skt_2023['FM_FLOW_PPLTN_CNT_20_24']+skt_2023['FM_FLOW_PPLTN_CNT_25_29'] )
skt_2023['flow_30'] = ( skt_2023['ML_FLOW_PPLTN_CNT_30_34']+skt_2023['ML_FLOW_PPLTN_CNT_35_39'] +
                      skt_2023['FM_FLOW_PPLTN_CNT_30_34']+skt_2023['FM_FLOW_PPLTN_CNT_35_39'] )
skt_2023['flow_40'] = ( skt_2023['ML_FLOW_PPLTN_CNT_40_44']+skt_2023['ML_FLOW_PPLTN_CNT_45_49'] +
                      skt_2023['FM_FLOW_PPLTN_CNT_40_44']+skt_2023['FM_FLOW_PPLTN_CNT_45_49'] )
skt_2023['flow_50'] = ( skt_2023['ML_FLOW_PPLTN_CNT_50_54']+skt_2023['ML_FLOW_PPLTN_CNT_55_59'] +
                      skt_2023['FM_FLOW_PPLTN_CNT_50_54']+skt_2023['FM_FLOW_PPLTN_CNT_55_59'] )
skt_2023['flow_60'] = ( skt_2023['ML_FLOW_PPLTN_CNT_60_64']+skt_2023['ML_FLOW_PPLTN_CNT_65_69'] +
                      skt_2023['FM_FLOW_PPLTN_CNT_60_64']+skt_2023['FM_FLOW_PPLTN_CNT_65_69'] )
skt_2023['flow_70'] = ( skt_2023['ML_FLOW_PPLTN_CNT_70_ABV']+skt_2023['FM_FLOW_PPLTN_CNT_70_ABV'] )

skt_2023 = skt_2023[['CRTR_YMD','COORD_X', 'COORD_Y', 'flow_10','flow_20','flow_30','flow_40','flow_50','flow_60', 'flow_70']]

skt_point = skt_point_asan[['COORD_X', 'COORD_Y', 'EMD_NM']]

skt_2023 = pd.merge(skt_2023, skt_point, how = 'left', on = ['COORD_X', 'COORD_Y'])
sam = skt_2023.head(1000)


skt_sum_2023 = skt_2023[['CRTR_YMD', 'EMD_NM', 'flow_10','flow_20','flow_30','flow_40','flow_50','flow_60', 'flow_70']]
skt_sum_2023 = skt_sum_2023.groupby(['CRTR_YMD', 'EMD_NM']).sum().reset_index()

skt_day_2023 =skt_sum_2023[['EMD_NM', 'flow_10','flow_20','flow_30','flow_40','flow_50','flow_60', 'flow_70']]
skt_day_2023 = skt_day_2023.groupby(['EMD_NM']).mean().reset_index()
skt_day_2023['flow_sum'] = round(skt_day_2023['flow_10']+skt_day_2023['flow_20']+skt_day_2023['flow_30']+skt_day_2023['flow_40']+
                            skt_day_2023['flow_50']+skt_day_2023['flow_60']+skt_day_2023['flow_70'])

skt_day_2023.to_excel('d:\\out\\아산시_D1212_skt_지역별유동인구.xlsx')

## 2022년 
skt_2022 = pd.read_pickle('living_skt_2022.pkl')

skt_2022['ML_FLOW_PPLTN_CNT_10_BELOW' ] = skt_2022['ML_FLOW_PPLTN_CNT_10_BELOW'].str[:4].astype('float')
skt_2022['FM_FLOW_PPLTN_CNT_10_BELOW' ] = skt_2022['FM_FLOW_PPLTN_CNT_10_BELOW'].str[:4].astype('float')

skt_2022['flow_10'] = (skt_2022['ML_FLOW_PPLTN_CNT_10_BELOW']+skt_2022['ML_FLOW_PPLTN_CNT_10_14']+skt_2022['ML_FLOW_PPLTN_CNT_15_19'] +
                      skt_2022['FM_FLOW_PPLTN_CNT_10_BELOW']+skt_2022['FM_FLOW_PPLTN_CNT_10_14']+skt_2022['FM_FLOW_PPLTN_CNT_15_19'])
skt_2022['flow_20'] = (skt_2022['ML_FLOW_PPLTN_CNT_20_24']+skt_2022['ML_FLOW_PPLTN_CNT_25_29'] +
                      skt_2022['FM_FLOW_PPLTN_CNT_20_24']+skt_2022['FM_FLOW_PPLTN_CNT_25_29'] )
skt_2022['flow_30'] = ( skt_2022['ML_FLOW_PPLTN_CNT_30_34']+skt_2022['ML_FLOW_PPLTN_CNT_35_39'] +
                      skt_2022['FM_FLOW_PPLTN_CNT_30_34']+skt_2022['FM_FLOW_PPLTN_CNT_35_39'] )
skt_2022['flow_40'] = ( skt_2022['ML_FLOW_PPLTN_CNT_40_44']+skt_2022['ML_FLOW_PPLTN_CNT_45_49'] +
                      skt_2022['FM_FLOW_PPLTN_CNT_40_44']+skt_2022['FM_FLOW_PPLTN_CNT_45_49'] )
skt_2022['flow_50'] = ( skt_2022['ML_FLOW_PPLTN_CNT_50_54']+skt_2022['ML_FLOW_PPLTN_CNT_55_59'] +
                      skt_2022['FM_FLOW_PPLTN_CNT_50_54']+skt_2022['FM_FLOW_PPLTN_CNT_55_59'] )
skt_2022['flow_60'] = ( skt_2022['ML_FLOW_PPLTN_CNT_60_64']+skt_2022['ML_FLOW_PPLTN_CNT_65_69'] +
                      skt_2022['FM_FLOW_PPLTN_CNT_60_64']+skt_2022['FM_FLOW_PPLTN_CNT_65_69'] )
skt_2022['flow_70'] = ( skt_2022['ML_FLOW_PPLTN_CNT_70_ABV']+skt_2022['FM_FLOW_PPLTN_CNT_70_ABV'] )

skt_2022 = skt_2022[['CRTR_YMD','COORD_X', 'COORD_Y', 'flow_10','flow_20','flow_30','flow_40','flow_50','flow_60', 'flow_70']]

skt_point = skt_point_asan[['COORD_X', 'COORD_Y', 'EMD_NM']]

skt_2022 = pd.merge(skt_2022, skt_point, how = 'left', on = ['COORD_X', 'COORD_Y'])

skt_sum_2022 = skt_2022[['CRTR_YMD', 'EMD_NM', 'flow_10','flow_20','flow_30','flow_40','flow_50','flow_60', 'flow_70']]
skt_sum_2022 = skt_sum_2022.groupby(['CRTR_YMD', 'EMD_NM']).sum().reset_index()

skt_day_2022 =skt_sum_2022[['EMD_NM', 'flow_10','flow_20','flow_30','flow_40','flow_50','flow_60', 'flow_70']]
skt_day_2022 = skt_day_2022.groupby(['EMD_NM']).mean().reset_index()
skt_day_2022['flow_sum'] = round(skt_day_2022['flow_10']+skt_day_2022['flow_20']+skt_day_2022['flow_30']+skt_day_2022['flow_40']+
                            skt_day_2022['flow_50']+skt_day_2022['flow_60']+skt_day_2022['flow_70'])

## 2021년

skt_2021 = pd.read_pickle('living_skt_2021.pkl')

#skt_2022['ML_FLOW_PPLTN_CNT_10_BELOW' ] = skt_2022['ML_FLOW_PPLTN_CNT_10_BELOW'].str[:4].astype('float')
#skt_2022['FM_FLOW_PPLTN_CNT_10_BELOW' ] = skt_2022['FM_FLOW_PPLTN_CNT_10_BELOW'].str[:4].astype('float')

skt_2021['flow_10'] = (skt_2021['ML_FLOW_PPLTN_CNT_10_BELOW']+skt_2021['ML_FLOW_PPLTN_CNT_10_14']+skt_2021['ML_FLOW_PPLTN_CNT_15_19'] +
                      skt_2021['FM_FLOW_PPLTN_CNT_10_BELOW']+skt_2021['FM_FLOW_PPLTN_CNT_10_14']+skt_2021['FM_FLOW_PPLTN_CNT_15_19'])
skt_2021['flow_20'] = (skt_2021['ML_FLOW_PPLTN_CNT_20_24']+skt_2021['ML_FLOW_PPLTN_CNT_25_29'] +
                      skt_2021['FM_FLOW_PPLTN_CNT_20_24']+skt_2021['FM_FLOW_PPLTN_CNT_25_29'] )
skt_2021['flow_30'] = ( skt_2021['ML_FLOW_PPLTN_CNT_30_34']+skt_2021['ML_FLOW_PPLTN_CNT_35_39'] +
                      skt_2021['FM_FLOW_PPLTN_CNT_30_34']+skt_2021['FM_FLOW_PPLTN_CNT_35_39'] )
skt_2021['flow_40'] = ( skt_2021['ML_FLOW_PPLTN_CNT_40_44']+skt_2021['ML_FLOW_PPLTN_CNT_45_49'] +
                      skt_2021['FM_FLOW_PPLTN_CNT_40_44']+skt_2021['FM_FLOW_PPLTN_CNT_45_49'] )
skt_2021['flow_50'] = ( skt_2021['ML_FLOW_PPLTN_CNT_50_54']+skt_2021['ML_FLOW_PPLTN_CNT_55_59'] +
                      skt_2021['FM_FLOW_PPLTN_CNT_50_54']+skt_2021['FM_FLOW_PPLTN_CNT_55_59'] )
skt_2021['flow_60'] = ( skt_2021['ML_FLOW_PPLTN_CNT_60_64']+skt_2021['ML_FLOW_PPLTN_CNT_65_69'] +
                      skt_2021['FM_FLOW_PPLTN_CNT_60_64']+skt_2021['FM_FLOW_PPLTN_CNT_65_69'] )
skt_2021['flow_70'] = ( skt_2021['ML_FLOW_PPLTN_CNT_70_ABV']+skt_2021['FM_FLOW_PPLTN_CNT_70_ABV'] )

skt_2021 = skt_2021[['CRTR_YMD','COORD_X', 'COORD_Y', 'flow_10','flow_20','flow_30','flow_40','flow_50','flow_60', 'flow_70']]

skt_point = skt_point_asan[['COORD_X', 'COORD_Y', 'EMD_NM']]

skt_2021 = pd.merge(skt_2021, skt_point, how = 'left', on = ['COORD_X', 'COORD_Y'])

skt_sum_2021 = skt_2021[['CRTR_YMD', 'EMD_NM', 'flow_10','flow_20','flow_30','flow_40','flow_50','flow_60', 'flow_70']]
skt_sum_2021 = skt_sum_2021.groupby(['CRTR_YMD', 'EMD_NM']).sum().reset_index()

skt_day_2021 =skt_sum_2021[['EMD_NM', 'flow_10','flow_20','flow_30','flow_40','flow_50','flow_60', 'flow_70']]
skt_day_2021 = skt_day_2021.groupby(['EMD_NM']).mean().reset_index()
skt_day_2021['flow_sum'] = round(skt_day_2021['flow_10']+skt_day_2021['flow_20']+skt_day_2021['flow_30']+skt_day_2021['flow_40']+
                            skt_day_2021['flow_50']+skt_day_2021['flow_60']+skt_day_2021['flow_70'])


## 2020년

skt_2020 = pd.read_pickle('living_skt_2020.pkl')

#skt_2022['ML_FLOW_PPLTN_CNT_10_BELOW' ] = skt_2022['ML_FLOW_PPLTN_CNT_10_BELOW'].str[:4].astype('float')
#skt_2022['FM_FLOW_PPLTN_CNT_10_BELOW' ] = skt_2022['FM_FLOW_PPLTN_CNT_10_BELOW'].str[:4].astype('float')

skt_2020['flow_10'] = (skt_2020['ML_FLOW_PPLTN_CNT_10_BELOW']+skt_2020['ML_FLOW_PPLTN_CNT_10_14']+skt_2020['ML_FLOW_PPLTN_CNT_15_19'] +
                      skt_2020['FM_FLOW_PPLTN_CNT_10_BELOW']+skt_2020['FM_FLOW_PPLTN_CNT_10_14']+skt_2020['FM_FLOW_PPLTN_CNT_15_19'])
skt_2020['flow_20'] = (skt_2020['ML_FLOW_PPLTN_CNT_20_24']+skt_2020['ML_FLOW_PPLTN_CNT_25_29'] +
                      skt_2020['FM_FLOW_PPLTN_CNT_20_24']+skt_2020['FM_FLOW_PPLTN_CNT_25_29'] )
skt_2020['flow_30'] = ( skt_2020['ML_FLOW_PPLTN_CNT_30_34']+skt_2020['ML_FLOW_PPLTN_CNT_35_39'] +
                      skt_2020['FM_FLOW_PPLTN_CNT_30_34']+skt_2020['FM_FLOW_PPLTN_CNT_35_39'] )
skt_2020['flow_40'] = ( skt_2020['ML_FLOW_PPLTN_CNT_40_44']+skt_2020['ML_FLOW_PPLTN_CNT_45_49'] +
                      skt_2020['FM_FLOW_PPLTN_CNT_40_44']+skt_2020['FM_FLOW_PPLTN_CNT_45_49'] )
skt_2020['flow_50'] = ( skt_2020['ML_FLOW_PPLTN_CNT_50_54']+skt_2020['ML_FLOW_PPLTN_CNT_55_59'] +
                      skt_2020['FM_FLOW_PPLTN_CNT_50_54']+skt_2020['FM_FLOW_PPLTN_CNT_55_59'] )
skt_2020['flow_60'] = ( skt_2020['ML_FLOW_PPLTN_CNT_60_64']+skt_2020['ML_FLOW_PPLTN_CNT_65_69'] +
                      skt_2020['FM_FLOW_PPLTN_CNT_60_64']+skt_2020['FM_FLOW_PPLTN_CNT_65_69'] )
skt_2020['flow_70'] = ( skt_2020['ML_FLOW_PPLTN_CNT_70_ABV']+skt_2020['FM_FLOW_PPLTN_CNT_70_ABV'] )

skt_2020 = skt_2020[['CRTR_YMD','COORD_X', 'COORD_Y', 'flow_10','flow_20','flow_30','flow_40','flow_50','flow_60', 'flow_70']]

skt_point = skt_point_asan[['COORD_X', 'COORD_Y', 'EMD_NM']]

skt_2020 = pd.merge(skt_2020, skt_point, how = 'left', on = ['COORD_X', 'COORD_Y'])

skt_sum_2020 = skt_2020[['CRTR_YMD', 'EMD_NM', 'flow_10','flow_20','flow_30','flow_40','flow_50','flow_60', 'flow_70']]
skt_sum_2020 = skt_sum_2020.groupby(['CRTR_YMD', 'EMD_NM']).sum().reset_index()

skt_day_2020 =skt_sum_2020[['EMD_NM', 'flow_10','flow_20','flow_30','flow_40','flow_50','flow_60', 'flow_70']]
skt_day_2020 = skt_day_2020.groupby(['EMD_NM']).mean().reset_index()
skt_day_2020['flow_sum'] = round(skt_day_2020['flow_10']+skt_day_2020['flow_20']+skt_day_2020['flow_30']+skt_day_2020['flow_40']+
                            skt_day_2020['flow_50']+skt_day_2020['flow_60']+skt_day_2020['flow_70'])

## 2019년

skt_2019 = pd.read_pickle('living_skt_2019.pkl')

#skt_2022['ML_FLOW_PPLTN_CNT_10_BELOW' ] = skt_2022['ML_FLOW_PPLTN_CNT_10_BELOW'].str[:4].astype('float')
#skt_2022['FM_FLOW_PPLTN_CNT_10_BELOW' ] = skt_2022['FM_FLOW_PPLTN_CNT_10_BELOW'].str[:4].astype('float')

skt_2019['flow_10'] = (skt_2019['ML_FLOW_PPLTN_CNT_10_BELOW']+skt_2019['ML_FLOW_PPLTN_CNT_10_14']+skt_2019['ML_FLOW_PPLTN_CNT_15_19'] +
                      skt_2019['FM_FLOW_PPLTN_CNT_10_BELOW']+skt_2019['FM_FLOW_PPLTN_CNT_10_14']+skt_2019['FM_FLOW_PPLTN_CNT_15_19'])
skt_2019['flow_20'] = (skt_2019['ML_FLOW_PPLTN_CNT_20_24']+skt_2019['ML_FLOW_PPLTN_CNT_25_29'] +
                      skt_2019['FM_FLOW_PPLTN_CNT_20_24']+skt_2019['FM_FLOW_PPLTN_CNT_25_29'] )
skt_2019['flow_30'] = ( skt_2019['ML_FLOW_PPLTN_CNT_30_34']+skt_2019['ML_FLOW_PPLTN_CNT_35_39'] +
                      skt_2019['FM_FLOW_PPLTN_CNT_30_34']+skt_2019['FM_FLOW_PPLTN_CNT_35_39'] )
skt_2019['flow_40'] = ( skt_2019['ML_FLOW_PPLTN_CNT_40_44']+skt_2019['ML_FLOW_PPLTN_CNT_45_49'] +
                      skt_2019['FM_FLOW_PPLTN_CNT_40_44']+skt_2019['FM_FLOW_PPLTN_CNT_45_49'] )
skt_2019['flow_50'] = ( skt_2019['ML_FLOW_PPLTN_CNT_50_54']+skt_2019['ML_FLOW_PPLTN_CNT_55_59'] +
                      skt_2019['FM_FLOW_PPLTN_CNT_50_54']+skt_2019['FM_FLOW_PPLTN_CNT_55_59'] )
skt_2019['flow_60'] = ( skt_2019['ML_FLOW_PPLTN_CNT_60_64']+skt_2019['ML_FLOW_PPLTN_CNT_65_69'] +
                      skt_2019['FM_FLOW_PPLTN_CNT_60_64']+skt_2019['FM_FLOW_PPLTN_CNT_65_69'] )
skt_2019['flow_70'] = ( skt_2019['ML_FLOW_PPLTN_CNT_70_ABV']+skt_2019['FM_FLOW_PPLTN_CNT_70_ABV'] )

skt_2019 = skt_2019[['CRTR_YMD','COORD_X', 'COORD_Y', 'flow_10','flow_20','flow_30','flow_40','flow_50','flow_60', 'flow_70']]

skt_point = skt_point_asan[['COORD_X', 'COORD_Y', 'EMD_NM']]

skt_2019 = pd.merge(skt_2019, skt_point, how = 'left', on = ['COORD_X', 'COORD_Y'])

skt_sum_2019 = skt_2019[['CRTR_YMD', 'EMD_NM', 'flow_10','flow_20','flow_30','flow_40','flow_50','flow_60', 'flow_70']]
skt_sum_2019 = skt_sum_2019.groupby(['CRTR_YMD', 'EMD_NM']).sum().reset_index()

skt_day_2019 =skt_sum_2019[['EMD_NM', 'flow_10','flow_20','flow_30','flow_40','flow_50','flow_60', 'flow_70']]
skt_day_2019 = skt_day_2019.groupby(['EMD_NM']).mean().reset_index()
skt_day_2019['flow_sum'] = round(skt_day_2019['flow_10']+skt_day_2019['flow_20']+skt_day_2019['flow_30']+skt_day_2019['flow_40']+
                            skt_day_2019['flow_50']+skt_day_2019['flow_60']+skt_day_2019['flow_70'])


skt_2019 = skt_day_2019[['EMD_NM', 'flow_sum']]
skt_2020 = skt_day_2020[['EMD_NM', 'flow_sum']]
skt_2021 = skt_day_2021[['EMD_NM', 'flow_sum']]
skt_2022 = skt_day_2022[['EMD_NM', 'flow_sum']]
skt_2023 = skt_day_2023[['EMD_NM', 'flow_sum']]

skt_2019.columns = ['EMD_NM', 'flow_2019']
skt_2020.columns = ['EMD_NM', 'flow_2020']
skt_2021.columns = ['EMD_NM', 'flow_2021']
skt_2022.columns = ['EMD_NM', 'flow_2022']
skt_2023.columns = ['EMD_NM', 'flow_2023']

skt_year = pd.merge(skt_2019, skt_2020, how = 'left', on = 'EMD_NM')
skt_year = pd.merge(skt_year, skt_2021, how = 'left', on = 'EMD_NM')
skt_year = pd.merge(skt_year, skt_2022, how = 'left', on = 'EMD_NM')
skt_year = pd.merge(skt_year, skt_2023, how = 'left', on = 'EMD_NM')
skt_year['add_rt'] = (skt_year['flow_2023'] - skt_year['flow_2019']) / skt_year['flow_2019']

skt_year.to_excel('d:\\out\\아산시_D1212_skt_연간동인구증감.xlsx')

## 연령대 구성비

skt_day_2023['age20_rt'] = (skt_day_2023['flow_10'] + skt_day_2023['flow_20']+ skt_day_2023['flow_30']) / skt_day_2023['flow_sum']
skt_day_2023['age40_rt'] = (skt_day_2023['flow_40'] + skt_day_2023['flow_50']) / skt_day_2023['flow_sum']
skt_day_2023['age60_rt'] = (skt_day_2023['flow_60'] + skt_day_2023['flow_70']) / skt_day_2023['flow_sum']

skt_day_2023.to_excel('d:\\out\\아산시_D1212_skt_연령대분포(2023).xlsx')

## 주중/주말 구성비

def what_day_is_it(date):
    days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    day = date.weekday()
    return days[day]

skt_sum_2023['CRTR_YMD'] = skt_sum_2023['CRTR_YMD'].astype('str')
skt_sum_2023['CRTR_YMD'] = pd.to_datetime(skt_sum_2023['CRTR_YMD'], format='%Y%m%d')

skt_sum_2023['weeknm'] = skt_sum_2023['CRTR_YMD'].apply(lambda x: what_day_is_it(x))
skt_sum_2023['flow_sum'] = (skt_sum_2023['flow_10'] + skt_sum_2023['flow_20']+ skt_sum_2023['flow_30'] + skt_sum_2023['flow_40'] +
                            skt_sum_2023['flow_50'] + skt_sum_2023['flow_60']+ skt_sum_2023['flow_70'] )

sam1 =skt_sum_2023[(skt_sum_2023['weeknm'] == 'Sat') | (skt_sum_2023['weeknm'] == 'Sun')]
sam2 =skt_sum_2023[(skt_sum_2023['weeknm'] != 'Sat') & (skt_sum_2023['weeknm'] != 'Sun')]

sam11 =  sam1[['EMD_NM', 'flow_sum']]
sam21 =  sam2[['EMD_NM', 'flow_sum']]

sam11 = sam11.groupby(['EMD_NM']).mean().reset_index()
sam21 = sam21.groupby(['EMD_NM']).mean().reset_index()

sam11.columns =  ['EMD_NM', 'weekend']
sam21.columns =  ['EMD_NM', 'weekday']

sam3 = pd.merge(sam11, sam21, how = 'left', on = 'EMD_NM')
sam3['weekend_rt'] =  sam3['weekend'] / sam3['weekday']

sam3.to_excel('d:\\out\\아산시_D1212_skt_주말비율(2023).xlsx')


##### 상관관계 분석

living_cnt = pd.read_pickle('living_cnt.pkl')
living_cnt.columns = ['EMD_NM', '생활서비스', '소매업', '숙박', '여가생활', '음식', '의료', 'All']
living_cnt =  living_cnt.loc[living_cnt['EMD_NM'] != 'All']
living_cnt['기타인허가'] = living_cnt['생활서비스'] + living_cnt['숙박'] + living_cnt['여가생활'] + living_cnt['의료']

skt_cnt = skt_day_2023[['EMD_NM','flow_sum', 'age20_rt', 'age40_rt', 'age60_rt']]
skt_1 = sam3[['EMD_NM', 'weekend_rt']]

skt_cnt = pd.merge(skt_cnt, skt_1, how = 'left', on = 'EMD_NM')
skt_cnt.to_pickle('skt_cnt.pkl')

## cordb 생성
cordb = pd.merge(living_cnt, skt_cnt, how = 'left', on = 'EMD_NM')

pearsonr(cordb['flow_sum'], cordb['All'])        # 유동인구  vs. 인허가전체
pearsonr(cordb['flow_sum'], cordb['소매업'])      # 소매업인허가
pearsonr(cordb['flow_sum'], cordb['음식'])        # 음식업인허가
pearsonr(cordb['flow_sum'], cordb['기타인허가'])   # 기타인허가

pearsonr(cordb['age20_rt'], cordb['All'])        # 30세이하 유동인구
pearsonr(cordb['age40_rt'], cordb['All'])        # 30세이하 유동인구
pearsonr(cordb['age60_rt'], cordb['All'])        # 30세이하 유동인구
pearsonr(cordb['weekend_rt'], cordb['All'])      # 주말유동인구비율

cordb.to_excel('d:\\out\\아산시_D1212_skt_상관관계분석.xlsx')













####################################################################################################

############    EDA   최초 분석 내용 ###################################################################

####################################################################################################


## 아산시 제공 최초데이터 : 전국데이터, 30만건 오류로 아산시 데이터 누락

folder_path = 'D:\\data\\생활업종'

# 폴더 내의 Excel 파일 목록 가져오기
xlsx_files = [f for f in os.listdir(folder_path) if f.endswith('.xlsx')]

# 데이터프레임을 담을 딕셔너리 초기화
dataframes = {}

varlist = ['번호', '개방서비스명', '개방서비스아이디', '개방자치단체코드', '관리번호', '인허가일자', '인허가취소일자',
           '영업상태구분코드', '영업상태명', '상세영업상태코드', '상세영업상태명', '폐업일자', '휴업시작일자', '휴업종료일자',
           '재개업일자', '소재지전체주소', '도로명전체주소','사업장명', '최종수정시점', '데이터갱신일자','좌표정보(X)', '좌표정보(Y)']

# Excel 파일을 읽어와서 데이터프레임 생성
for idx, xlsx_file in enumerate(xlsx_files, start=1):
    full_path = os.path.join(folder_path, xlsx_file)
    dataframe = pd.read_excel(full_path)
    dataframes[f'db{idx}'] = dataframe[varlist]
living_comdb = []
living_comdb = pd.concat(dataframes)

living_comdb.to_pickle('living_comdb.pkl')


#####################################
## 시흥시 업종분류
#############   경기도 인허가데이터 다운로드. csv 파일로 로드

folder_path = 'D:\\data\\생활업종_경기도'

# 폴더 내의 Excel 파일 목록 가져오기
csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]

# 데이터프레임을 담을 딕셔너리 초기화
dataframes = {}

varlist = ['번호', '개방서비스명', '개방서비스아이디', '개방자치단체코드', '관리번호', '인허가일자', '인허가취소일자',
           '영업상태구분코드', '영업상태명', '상세영업상태코드', '상세영업상태명', '폐업일자', '휴업시작일자', '휴업종료일자',
           '재개업일자', '소재지전체주소', '도로명전체주소','사업장명', '최종수정시점', '데이터갱신일자','좌표정보(x)', '좌표정보(y)']

# Excel 파일을 읽어와서 데이터프레임 생성
for idx, csv_file in enumerate(csv_files, start=1):
    full_path = os.path.join(folder_path, csv_file)
    dataframe = pd.read_csv(full_path, encoding='CP949', dtype=str)
    dataframes[f'db{idx}'] = dataframe[varlist]
    print(csv_file)
living_comdb = []
living_comdb = pd.concat(dataframes)

## 오류데이터 추가

sam1 = pd.read_excel('D:\\data\\생활업종_경기도_오류\\6410000_경기도_01_01_02_P_의원.xlsx', dtype=str)
sam2 = pd.read_excel('D:\\data\\생활업종_경기도_오류\\6410000_경기도_03_05_07_P_청소년게임제공업.xlsx', dtype=str)
sam3 = pd.read_excel('D:\\data\\생활업종_경기도_오류\\6410000_경기도_03_08_03_P_문화예술법인.xlsx', dtype=str)
sam41 = pd.read_excel('D:\\data\\생활업종_경기도_오류\\6410000_경기도_08_26_04_P_통신판매업.xlsx', dtype=str, sheet_name=0)
sam42 = pd.read_excel('D:\\data\\생활업종_경기도_오류\\6410000_경기도_08_26_04_P_통신판매업.xlsx', dtype=str, sheet_name=1)
sam43 = pd.read_excel('D:\\data\\생활업종_경기도_오류\\6410000_경기도_08_26_04_P_통신판매업.xlsx', dtype=str, sheet_name=2)
sam5 = pd.read_excel('D:\\data\\생활업종_경기도_오류\\6410000_경기도_11_43_02_P_담배소매업.xlsx', dtype=str)

## 오류발생하는 라인 제외 후 데이터 생성
try:
    sam4 = pd.read_csv('D:\\data\\생활업종_경기도_오류\\6410000_경기도_08_26_04_P_통신판매업.csv', encoding='CP949', dtype=str, skiprows=473919)
except pd.errors.ParserError as e:
    # ParserError가 발생했을 때, 해당 라인을 무시하거나 다른 처리를 수행할 수 있음
    print(f"Error: {e}")

sam4 = df

varlist = ['번호', '개방서비스명', '개방서비스아이디', '개방자치단체코드', '관리번호', '인허가일자', '인허가취소일자',
           '영업상태구분코드', '영업상태명', '상세영업상태코드', '상세영업상태명', '폐업일자', '휴업시작일자', '휴업종료일자',
           '재개업일자', '소재지전체주소', '도로명전체주소','사업장명', '최종수정시점', '데이터갱신일자','좌표정보(x)', '좌표정보(y)']
varlist_2 = ['번호', '개방서비스명', '개방서비스아이디', '개방자치단체코드', '관리번호', '인허가일자', '인허가취소일자',
           '영업상태구분코드', '영업상태명', '상세영업상태코드', '상세영업상태명', '폐업일자', '휴업시작일자', '휴업종료일자',
           '재개업일자', '소재지전체주소', '도로명전체주소','사업장명', '최종수정시점', '데이터갱신일자','좌표정보(X)', '좌표정보(Y)']

sam1 = sam1[varlist_2]
sam2 = sam2[varlist_2]
sam3 = sam3[varlist_2]
sam41 = sam41[varlist_2]
sam42 = sam42[varlist_2]
sam43 = sam43[varlist_2]
sam5 = sam5[varlist_2]

samtot = pd.concat([sam1, sam2, sam3, sam41, sam42, sam43, sam5], axis=0)
samtot.columns = varlist

living_comdb = pd.concat([living_comdb, samtot], axis=0)

living_comdb3 = living_comdb[(living_comdb['소재지전체주소'].str[:7] == '경기도 시흥시')|(living_comdb['도로명전체주소'].str[:7] == '경기도 시흥시')]
living_comdb3.to_pickle('company_sh.pkl')

##

folder_path = 'D:\\data\\생활업종_경기도_엑셀'

# 폴더 내의 Excel 파일 목록 가져오기
xlsx_files = [f for f in os.listdir(folder_path) if f.endswith('.xlsx')]

# 데이터프레임을 담을 딕셔너리 초기화
dataframes = {}

varlist = ['번호', '개방서비스명', '개방서비스아이디', '개방자치단체코드', '관리번호', '인허가일자', '인허가취소일자',
           '영업상태구분코드', '영업상태명', '상세영업상태코드', '상세영업상태명', '폐업일자', '휴업시작일자', '휴업종료일자',
           '재개업일자', '소재지전체주소', '도로명전체주소','사업장명', '최종수정시점', '데이터갱신일자','좌표정보(X)', '좌표정보(Y)']

# Excel 파일을 읽어와서 데이터프레임 생성
for idx, xlsx_file in enumerate(xlsx_files, start=1):
    full_path = os.path.join(folder_path, xlsx_file)
    dataframe = pd.read_excel(full_path)
    dataframes[f'db{idx}'] = dataframe[varlist]
living_comdb = []
living_comdb = pd.concat(dataframes)

living_comdb.to_pickle('living_comdb.pkl')




samdb = pd.read_excel('D:\\data\\생활업종\\fulldata_07_24_04_P_일반음식점.xlsx' ,  dtype=str)
samdb2 = pd.read_excel('D:\\data\\생활업종\\fulldata_07_24_04_P_일반음식점.xlsx')

dglist = pd.DataFrame(xlsx_files)
dglist.to_excel('d:\\out\\아산시_D110_인허가데이터리스트.xlsx')
