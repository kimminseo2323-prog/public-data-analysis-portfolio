#### 경로지정 ####

outdir =  r'D:\\10.outfile'    ## output 생성 폴더
os.makedirs(outdir)

datadir =  r'C:\\rawdata\\A28'    ## output 생성 폴더
os.makedirs(datadir)

#############################
#############################

card_spec_month = pd.read_pickle('card_spec_month.pkl')
card_spec_month = card_spec_month[card_spec_month['연월'] != '2024-07']

job = pd.read_excel('매핑업종2.xlsx', dtype=str)
job.columns = ['업종분류', '업종대분류', '업종구분']

card_spec_month2 = pd.merge(card_spec_month, job, how = 'left', on = '업종대분류')

card_amt_mm = card_spec_month2.groupby(['시군구명','연월'])[['카드사용금액', '카드사용건수']].sum().reset_index()

card_spec_month3 = card_spec_month2[card_spec_month2['업종구분'] != '요금/금융']



#####  월별 카드사용 금액
card_amt_mm.to_excel(os.path.join(outdir, 'a29_1206_카드_월별금액.xlsx'))

#####  업종별 금액
card_job = card_spec_month2.groupby(['업종구분','업종대분류','시군구명'])[['카드사용금액', '카드사용건수']].sum().reset_index()
card_job2 = card_job.pivot(index=['업종구분','업종대분류'], columns=['시군구명'], values=['카드사용금액', '카드사용건수']).reset_index()

card_job3 = card_spec_month2.groupby(['업종구분','시군구명'])[['카드사용금액', '카드사용건수']].sum().reset_index()
card_job4 = card_job3.pivot(index=['업종구분'], columns=['시군구명'], values=['카드사용금액', '카드사용건수']).reset_index()

card_amt_mm2 = card_spec_month2.groupby(['시군구명','연월'])[['카드사용금액', '카드사용건수']].sum().reset_index()

#####  업종별 카드사용 금액
card_job2.to_excel(os.path.join(outdir, 'a29_1206_카드_업종.xlsx'))
card_job4.to_excel(os.path.join(outdir, 'a29_1206_카드_업종분류.xlsx'))

##################################################

## 시간대별 카드금액



