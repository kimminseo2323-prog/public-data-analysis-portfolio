#### 경로지정 ####

outdir =  r'D:\\10.outfile'    ## output 생성 폴더
os.makedirs(outdir)

datadir =  r'C:\\rawdata\\A28'    ## output 생성 폴더
os.makedirs(datadir)

#############################
#############################
movein_m05 = pd.read_pickle('A29_202405_유입.pkl')
moveout_m05 = pd.read_pickle('A29_202405_유출.pkl')

## 서초구 외부 유입

out_in = movein_m05[movein_m05['o_sgg'] != '서초구']
out_ins = out_in.groupby(['월', 'date', '요일', '평일구분','o_sgg', 'd_admi'])[['total_cnt', 'male_00_cnt', 'male_20_cnt',
         'male_40_cnt', 'male_60_cnt', 'feml_00_cnt', 'feml_20_cnt', 'feml_40_cnt','feml_60_cnt']].sum().reset_index()
out_ins_dsum = out_in.groupby(['월', 'date', '요일', '평일구분'])['total_cnt'].sum().reset_index()

## 일평균 외부 유입인구
out_ins_dsum.groupby(['월'])['total_cnt'].mean().reset_index()
out_ins_dsum.groupby(['월', '평일구분'])['total_cnt'].mean().reset_index()

## 서초구 외부 유출
out_out = moveout_m05[moveout_m05['d_sgg'] != '서초구']
out_outs = out_out.groupby(['월', 'date', '요일', '평일구분','d_sgg', 'o_admi'])[['total_cnt', 'male_00_cnt', 'male_20_cnt',
         'male_40_cnt', 'male_60_cnt', 'feml_00_cnt', 'feml_20_cnt', 'feml_40_cnt','feml_60_cnt']].sum().reset_index()
out_outs_dsum = out_outs.groupby(['월', 'date', '요일', '평일구분'])['total_cnt'].sum().reset_index()

## 일평균 외부 유입인구
out_outs_dsum.groupby(['월'])['total_cnt'].mean().reset_index()
out_outs_dsum.groupby(['월', '평일구분'])['total_cnt'].mean().reset_index()

## 서초구내 이동인구
in_in = movein_m05[(movein_m05['o_sgg'] == '서초구')]
in_in = in_in[in_in['o_admi'] != in_in['d_admi']]
in_ins = in_in.groupby(['월', 'date', '요일', '평일구분','o_sgg', 'd_admi'])[['total_cnt', 'male_00_cnt', 'male_20_cnt',
         'male_40_cnt', 'male_60_cnt', 'feml_00_cnt', 'feml_20_cnt', 'feml_40_cnt','feml_60_cnt']].sum().reset_index()
in_ins_dsum = in_in.groupby(['월', 'date', '요일', '평일구분'])['total_cnt'].sum().reset_index()

## 일평균 내부 이동인구
in_ins_dsum.groupby(['월'])['total_cnt'].mean().reset_index()
in_ins_dsum.groupby(['월', '평일구분'])['total_cnt'].mean().reset_index()

#######################################

## 행정동별 외부 유입인구수
dd_01 = out_in.groupby(['d_admi', 'date'])['total_cnt'].sum().reset_index()
dd_01 = dd_01.groupby(['d_admi'])['total_cnt'].mean().reset_index()
dd_01.to_excel(os.path.join(outdir, 'a29_1129_유입_행정동별일평균.xlsx'))

#######################################

## 유입인구비율 높은 반포4동, 서초3동, 양재2동의 평일/휴일 시간대별 유입/유출
## 유입인구비율 낮은 서초1동, 반포2동, 방배본동의 평일/휴일 시간대별 유입/유출

out_ins = out_in.groupby(['월', 'date', '요일', '평일구분','o_sgg', 'd_admi', 'd_time'])[['total_cnt', 'male_00_cnt', 'male_20_cnt',
         'male_40_cnt', 'male_60_cnt', 'feml_00_cnt', 'feml_20_cnt', 'feml_40_cnt','feml_60_cnt']].sum().reset_index()

out_ins_02 = out_ins[out_ins['d_admi'].isin(['반포4동','서초3동','양재2동','서초1동','반포2동','방배본동'])]
out_ins_02['dong_gb'] = np.where(out_ins_02['d_admi'].isin(['반포4동','서초3동','양재2동']), 1, 0)

out_ins_dsum2 = out_ins_02.groupby(['월', 'date', '요일', '평일구분','dong_gb', 'd_admi', 'd_time'])['total_cnt'].sum().reset_index()
out_ins_wday = out_ins_dsum2.groupby(['dong_gb', '평일구분','d_admi', 'd_time'])['total_cnt'].mean().reset_index()
out_ins_wday2 = out_ins_wday.pivot(index=[ '평일구분', 'd_time'], columns=['dong_gb','d_admi'], values='total_cnt').reset_index()

## 연령대별, 성별 유입인구 비율
out_ins_dage = out_ins_02.groupby(['월', 'date', '요일', '평일구분','dong_gb', 'd_admi', 'd_time'])[['total_cnt', 'male_00_cnt', 'male_20_cnt',
                    'male_40_cnt', 'male_60_cnt', 'feml_00_cnt', 'feml_20_cnt', 'feml_40_cnt','feml_60_cnt']].sum().reset_index()
out_ins_dage2 = out_ins_dage.groupby(['dong_gb', '평일구분','d_admi', 'd_time'])[['total_cnt', 'male_00_cnt', 'male_20_cnt',
                    'male_40_cnt', 'male_60_cnt', 'feml_00_cnt', 'feml_20_cnt', 'feml_40_cnt','feml_60_cnt']].mean().reset_index()

out_ins_dage3 = out_ins_dage2.groupby(['dong_gb', '평일구분','d_admi'])[['total_cnt', 'male_00_cnt', 'male_20_cnt',
                    'male_40_cnt', 'male_60_cnt', 'feml_00_cnt', 'feml_20_cnt', 'feml_40_cnt','feml_60_cnt']].sum().reset_index()

#####  행정동별 시간대별 유입인구수
out_ins_wday2.to_excel(os.path.join(outdir, 'a29_1129_유입_행정동별시간대별.xlsx'))

#####  행정동별 일별 연령/성별 유입인구수
out_ins_dage3.to_excel(os.path.join(outdir, 'a29_1129_유입_행정동별연령대별.xlsx'))





####################################

#유출인구
out_outs = out_out.groupby(['월', 'date', '요일', '평일구분','d_sgg', 'o_admi', 's_time'])[['total_cnt', 'male_00_cnt', 'male_20_cnt',
         'male_40_cnt', 'male_60_cnt', 'feml_00_cnt', 'feml_20_cnt', 'feml_40_cnt','feml_60_cnt']].sum().reset_index()

out_outs_02 = out_outs[out_outs['o_admi'].isin(['반포4동','서초3동','양재2동','서초1동','반포2동','방배본동'])]
out_outs_02['dong_gb'] = np.where(out_outs_02['o_admi'].isin(['반포4동','서초3동','양재2동']), 1, 0)

out_outs_dsum2 = out_outs_02.groupby(['월', 'date', '요일', '평일구분','dong_gb', 'o_admi', 's_time'])['total_cnt'].sum().reset_index()
out_outs_wday = out_outs_dsum2.groupby(['dong_gb', '평일구분','o_admi', 's_time'])['total_cnt'].mean().reset_index()
out_outs_wday2 = out_outs_wday.pivot(index=[ '평일구분', 's_time'], columns=['dong_gb','o_admi'], values='total_cnt').reset_index()

#####  행정동별 시간대별 유입인구수
out_outs_wday2.to_excel(os.path.join(outdir, 'a29_1129_유출_행정동별시간대별.xlsx'))

## 평일 시간대별 유입인구수/유출인구수
out_ins_dtot = out_ins_wday.groupby(['평일구분', 'd_time'])['total_cnt'].sum().reset_index()
out_ins_dtot.columns = ['평일구분', 'time', 'in_totcnt']
out_outs_dtot = out_outs_wday.groupby(['평일구분', 's_time'])['total_cnt'].sum().reset_index()
out_outs_dtot.columns = ['평일구분', 'time', 'out_totcnt']
out_inout = pd.merge(out_ins_dtot, out_outs_dtot, how = 'left', on = ['평일구분', 'time'])

## 평일/주말 서초구전체 시간대별 유입/유출 인구수
out_inout.to_excel(os.path.join(outdir, 'a29_1202_서초구전체 시간대별 유입유출인구.xlsx'))

## 평일 출근/등교 행정동
out_ins_work = out_ins.groupby(['date', '요일', '평일구분','d_admi', 'd_time'])['total_cnt'].sum().reset_index()
out_ins_work = out_ins_work[(out_ins_work['평일구분'] == 1) & (out_ins_work['d_time'].isin([7, 8,9]))]
out_ins_work2 = out_ins_work.groupby(['d_admi', 'd_time'])['total_cnt'].mean().reset_index()
out_ins_work3 = out_ins_work2.groupby(['d_admi'])['total_cnt'].sum().reset_index()

## 평일 퇴근/하교 행정동
out_outs_work = out_outs.groupby(['date', '요일', '평일구분','o_admi', 's_time'])['total_cnt'].sum().reset_index()
out_outs_work = out_outs_work[(out_outs_work['평일구분'] == 1) & (out_outs_work['s_time'].isin([17, 18]))]
out_outs_work2 = out_outs_work.groupby(['o_admi', 's_time'])['total_cnt'].mean().reset_index()
out_outs_work3 = out_outs_work2.groupby(['o_admi'])['total_cnt'].sum().reset_index()

## 평일 출근 & 퇴근 조인
out_ins_work3.columns = ['행정동', '출근유입']
out_outs_work3.columns = ['행정동', '퇴근유출']
out_inout_work = pd.merge(out_ins_work3, out_outs_work3, how = 'left', on = '행정동')

## 평일 출퇴근 행정동
out_inout_work.to_excel(os.path.join(outdir, 'a29_1202_행정동별 외부출근유입 순위.xlsx'))


## 주말 유입/유출 행정동
out_ins_week = out_ins.groupby(['date', '요일', '평일구분','d_admi'])['total_cnt'].sum().reset_index()
out_ins_week = out_ins_week[out_ins_week['평일구분'] == 0]
out_ins_week2 = out_ins_week.groupby(['d_admi'])['total_cnt'].mean().reset_index()

out_outs_week = out_outs.groupby(['date', '요일', '평일구분','o_admi'])['total_cnt'].sum().reset_index()
out_outs_week = out_outs_week[out_outs_week['평일구분'] == 0]
out_outs_week2 = out_outs_week.groupby(['o_admi'])['total_cnt'].mean().reset_index()

# 주말 유입 & 유출 조인
out_ins_week2.columns = ['행정동', '주말유입']
out_outs_week2.columns = ['행정동', '주말유출']
out_inout_week = pd.merge(out_ins_week2, out_outs_week2, how = 'left', on = '행정동')

## 주말 출퇴근 행정동
out_inout_week.to_excel(os.path.join(outdir, 'a29_1202_행정동별 주말외부유입 순위.xlsx'))

####################
##  평일 행정동별 유입인구수
out_ins_dd = out_ins.groupby(['date', '요일', '평일구분','d_admi', 'd_time'])['total_cnt'].sum().reset_index()
out_ins_dd = out_ins_dd[out_ins_dd['평일구분'] == 1]
out_ins_dd2 = out_ins_dd.groupby(['d_admi', 'd_time'])['total_cnt'].mean().reset_index()
out_ins_dd3 = out_ins_dd2.groupby(['d_admi'])['total_cnt'].sum().reset_index()

## 평일 퇴근/하교 행정동
out_outs_dd = out_outs.groupby(['date', '요일', '평일구분','o_admi', 's_time'])['total_cnt'].sum().reset_index()
out_outs_dd = out_outs_dd[out_outs_dd['평일구분'] == 1]
out_outs_dd2 = out_outs_dd.groupby(['o_admi', 's_time'])['total_cnt'].mean().reset_index()
out_outs_dd3 = out_outs_dd2.groupby(['o_admi'])['total_cnt'].sum().reset_index()

## 평일 출근 & 퇴근 조인
out_ins_dd3.columns = ['행정동', '평일유입']
out_outs_dd3.columns = ['행정동', '평일유출']
out_inout_ddwork = pd.merge(out_ins_dd3, out_outs_dd3, how = 'left', on = '행정동')

####################

## 평일 점심 행정동
out_ins_t3 = out_ins.groupby(['date', '요일', '평일구분','d_admi', 'd_time'])['total_cnt'].sum().reset_index()
out_ins_t3 = out_ins_t3[(out_ins_t3['평일구분'] == 1) & (out_ins_t3['d_time'].isin([11, 12, 13]))]
out_ins_t3_2 = out_ins_t3.groupby(['d_admi', 'd_time'])['total_cnt'].mean().reset_index()
out_ins_t3_3 = out_ins_t3_2.groupby(['d_admi'])['total_cnt'].sum().reset_index()

## 평일 퇴근/하교 행정동
out_outs_t3 = out_outs.groupby(['date', '요일', '평일구분','o_admi', 's_time'])['total_cnt'].sum().reset_index()
out_outs_t3 = out_outs_t3[(out_outs_t3['평일구분'] == 1) & (out_outs_t3['s_time'].isin([11, 12, 13]))]
out_outs_t3_2 = out_outs_t3.groupby(['o_admi', 's_time'])['total_cnt'].mean().reset_index()
out_outs_t3_3 = out_outs_t3_2.groupby(['o_admi'])['total_cnt'].sum().reset_index()

## 평일 출근 & 퇴근 조인
out_ins_t3_3.columns = ['행정동', '점심유입']
out_outs_t3_3.columns = ['행정동', '점심유출']
out_inout_t3 = pd.merge(out_ins_t3_3, out_outs_t3_3, how = 'left', on = '행정동')
out_inout_t3 = pd.merge(out_inout_t3, out_inout_ddwork, how = 'left', on = '행정동')
out_inout_t3['유입비율'] = out_inout_t3['점심유입'] / out_inout_t3['평일유입']
out_inout_t3['유출비율'] = out_inout_t3['점심유출'] / out_inout_t3['평일유출']

## 평일 출퇴근 행정동
out_inout_t3.to_excel(os.path.join(outdir, 'a29_1202_행정동별 외부점심 순위.xlsx'))

####################

## 평일 오후 행정동
out_ins_t4 = out_ins.groupby(['date', '요일', '평일구분','d_admi', 'd_time'])['total_cnt'].sum().reset_index()
out_ins_t4 = out_ins_t4[(out_ins_t4['평일구분'] == 1) & (out_ins_t4['d_time'].isin([14, 15, 16]))]
out_ins_t4_2 = out_ins_t4.groupby(['d_admi', 'd_time'])['total_cnt'].mean().reset_index()
out_ins_t4_3 = out_ins_t4_2.groupby(['d_admi'])['total_cnt'].sum().reset_index()

## 평일 퇴근/하교 행정동
out_outs_t4 = out_outs.groupby(['date', '요일', '평일구분','o_admi', 's_time'])['total_cnt'].sum().reset_index()
out_outs_t4 = out_outs_t4[(out_outs_t4['평일구분'] == 1) & (out_outs_t4['s_time'].isin([14, 15, 16]))]
out_outs_t4_2 = out_outs_t4.groupby(['o_admi', 's_time'])['total_cnt'].mean().reset_index()
out_outs_t4_3 = out_outs_t4_2.groupby(['o_admi'])['total_cnt'].sum().reset_index()

## 평일 출근 & 퇴근 조인
out_ins_t4_3.columns = ['행정동', '유입']
out_outs_t4_3.columns = ['행정동', '유출']
out_inout_t4 = pd.merge(out_ins_t4_3, out_outs_t4_3, how = 'left', on = '행정동')
out_inout_t4 = pd.merge(out_inout_t4, out_inout_ddwork, how = 'left', on = '행정동')
out_inout_t4['유입비율'] = out_inout_t4['유입'] / out_inout_t3['평일유입']
out_inout_t4['유출비율'] = out_inout_t4['유출'] / out_inout_t3['평일유출']

## 평일 출퇴근 행정동
out_inout_t4.to_excel(os.path.join(outdir, 'a29_1202_행정동별 외부오후 순위.xlsx'))


####################

## 평일 저녁 행정동
out_ins_t5 = out_ins.groupby(['date', '요일', '평일구분','d_admi', 'd_time'])['total_cnt'].sum().reset_index()
out_ins_t5 = out_ins_t5[(out_ins_t5['평일구분'] == 1) & (out_ins_t5['d_time'].isin([17, 18, 19, 20]))]
out_ins_t5_2 = out_ins_t5.groupby(['d_admi', 'd_time'])['total_cnt'].mean().reset_index()
out_ins_t5_3 = out_ins_t5_2.groupby(['d_admi'])['total_cnt'].sum().reset_index()

## 평일 퇴근/하교 행정동
out_outs_t5 = out_outs.groupby(['date', '요일', '평일구분','o_admi', 's_time'])['total_cnt'].sum().reset_index()
out_outs_t5 = out_outs_t5[(out_outs_t5['평일구분'] == 1) & (out_outs_t5['s_time'].isin([17, 18, 19, 20]))]
out_outs_t5_2 = out_outs_t5.groupby(['o_admi', 's_time'])['total_cnt'].mean().reset_index()
out_outs_t5_3 = out_outs_t5_2.groupby(['o_admi'])['total_cnt'].sum().reset_index()

## 평일 출근 & 퇴근 조인
out_ins_t5_3.columns = ['행정동', '유입']
out_outs_t5_3.columns = ['행정동', '유출']
out_inout_t5 = pd.merge(out_ins_t5_3, out_outs_t5_3, how = 'left', on = '행정동')
out_inout_t5 = pd.merge(out_inout_t5, out_inout_ddwork, how = 'left', on = '행정동')
out_inout_t5['유입비율'] = out_inout_t5['유입'] / out_inout_t3['평일유입']
out_inout_t5['유출비율'] = out_inout_t5['유출'] / out_inout_t3['평일유출']

## 평일 출퇴근 행정동
out_inout_t5.to_excel(os.path.join(outdir, 'a29_1202_행정동별 외부저녁 순위.xlsx'))


##################################

## 평일 여성비율 :
out_ins_sex = out_ins.groupby(['date', '요일', '평일구분','d_admi', 'd_time'])[['male_00_cnt', 'male_20_cnt',
         'male_40_cnt', 'male_60_cnt', 'feml_00_cnt', 'feml_20_cnt', 'feml_40_cnt','feml_60_cnt']].sum().reset_index()
out_ins_sex = out_ins_sex[out_ins_sex['평일구분'] == 1]
out_ins_sex['male'] = out_ins_sex['male_00_cnt']+out_ins_sex['male_20_cnt']+out_ins_sex['male_40_cnt']+out_ins_sex['male_60_cnt']
out_ins_sex['feml'] = out_ins_sex['feml_00_cnt']+out_ins_sex['feml_20_cnt']+out_ins_sex['feml_40_cnt']+out_ins_sex['feml_60_cnt']
out_ins_sex2 = out_ins_sex.groupby(['d_admi', 'd_time'])[['male', 'feml']].mean().reset_index()
out_ins_sex3 = out_ins_sex2.groupby(['d_admi'])[['male', 'feml']].sum().reset_index()

## 평일 여성유출 행정동
out_outs_sex = out_outs.groupby(['date', '요일', '평일구분','o_admi', 's_time'])[['male_00_cnt', 'male_20_cnt',
         'male_40_cnt', 'male_60_cnt', 'feml_00_cnt', 'feml_20_cnt', 'feml_40_cnt','feml_60_cnt']].sum().reset_index()
out_outs_sex = out_outs_sex[out_outs_sex['평일구분'] == 1]
out_outs_sex['male'] = out_outs_sex['male_00_cnt']+out_outs_sex['male_20_cnt']+out_outs_sex['male_40_cnt']+out_outs_sex['male_60_cnt']
out_outs_sex['feml'] = out_outs_sex['feml_00_cnt']+out_outs_sex['feml_20_cnt']+out_outs_sex['feml_40_cnt']+out_outs_sex['feml_60_cnt']
out_outs_sex2 = out_outs_sex.groupby(['o_admi', 's_time'])[['male', 'feml']].mean().reset_index()
out_outs_sex3 = out_outs_sex2.groupby(['o_admi'])[['male', 'feml']].sum().reset_index()

## 평일 출근 & 퇴근 조인
out_ins_sex3.columns = ['행정동', '남성유입', '여성유입']
out_outs_sex3.columns = ['행정동', '남성유출', '여성유출']
out_inout_sex = pd.merge(out_ins_sex3, out_outs_sex3, how = 'left', on = '행정동')
out_inout_sex = pd.merge(out_inout_sex, out_inout_ddwork, how = 'left', on = '행정동')
out_inout_sex['남성유입비율'] = out_inout_sex['남성유입'] / out_inout_sex['평일유입']
out_inout_sex['남성유출비율'] = out_inout_sex['남성유출'] / out_inout_sex['평일유출']
out_inout_sex['여성유입비율'] = out_inout_sex['여성유입'] / out_inout_sex['평일유입']
out_inout_sex['여성유출비율'] = out_inout_sex['여성유출'] / out_inout_sex['평일유출']

## 평일 출퇴근 행정동
out_inout_sex.to_excel(os.path.join(outdir, 'a29_1202_행정동별 평일성별 순위.xlsx'))

##################################

## 연령대 비율 :
out_ins_age = out_ins.groupby(['date', '요일', '평일구분','d_admi', 'd_time'])[['male_00_cnt', 'male_20_cnt',
         'male_40_cnt', 'male_60_cnt', 'feml_00_cnt', 'feml_20_cnt', 'feml_40_cnt','feml_60_cnt']].sum().reset_index()
out_ins_age = out_ins_age[out_ins_age['평일구분'] == 1]
out_ins_age['age1'] = out_ins_age['male_00_cnt']+out_ins_age['feml_00_cnt']
out_ins_age['age2'] = out_ins_age['male_20_cnt']+out_ins_age['feml_20_cnt']
out_ins_age['age3'] = out_ins_age['male_40_cnt']+out_ins_age['feml_40_cnt']
out_ins_age2 = out_ins_age.groupby(['d_admi', 'd_time'])[['age1', 'age2', 'age3']].mean().reset_index()
out_ins_age3 = out_ins_age2.groupby(['d_admi'])[['age1', 'age2', 'age3']].sum().reset_index()

## 평일 여성유출 행정동
out_outs_age = out_outs.groupby(['date', '요일', '평일구분','o_admi', 's_time'])[['male_00_cnt', 'male_20_cnt',
         'male_40_cnt', 'male_60_cnt', 'feml_00_cnt', 'feml_20_cnt', 'feml_40_cnt','feml_60_cnt']].sum().reset_index()
out_outs_age = out_outs_age[out_outs_age['평일구분'] == 1]
out_outs_age['age1'] = out_outs_age['male_00_cnt']+out_outs_age['feml_00_cnt']
out_outs_age['age2'] = out_outs_age['male_20_cnt']+out_outs_age['feml_20_cnt']
out_outs_age['age3'] = out_outs_age['male_40_cnt']+out_outs_age['feml_40_cnt']
out_outs_age2 = out_outs_age.groupby(['o_admi', 's_time'])[['age1', 'age2', 'age3']].mean().reset_index()
out_outs_age3 = out_outs_age2.groupby(['o_admi'])[['age1', 'age2', 'age3']].sum().reset_index()

## 평일 출근 & 퇴근 조인
out_ins_age3.columns = ['행정동', '연령1유입', '연령2유입', '연령3유입']
out_outs_age3.columns = ['행정동', '연령1유출', '연령2유출', '연령3유출']
out_inout_age = pd.merge(out_ins_age3, out_outs_age3, how = 'left', on = '행정동')
out_inout_age = pd.merge(out_inout_age, out_inout_ddwork, how = 'left', on = '행정동')
out_inout_age['연령1유입비율'] = out_inout_age['연령1유입'] / out_inout_age['평일유입']
out_inout_age['연령1유출비율'] = out_inout_age['연령1유출'] / out_inout_age['평일유출']
out_inout_age['연령2유입비율'] = out_inout_age['연령2유입'] / out_inout_age['평일유입']
out_inout_age['연령2유출비율'] = out_inout_age['연령2유출'] / out_inout_age['평일유출']
out_inout_age['연령3유입비율'] = out_inout_age['연령3유입'] / out_inout_age['평일유입']
out_inout_age['연령3유출비율'] = out_inout_age['연령3유출'] / out_inout_age['평일유출']

## 평일 출퇴근 행정동
out_inout_age.to_excel(os.path.join(outdir, 'a29_1202_행정동별 평일연령 순위.xlsx'))






moveout_m05.columns









## 평일 출근시간대 7~8:59 유입, 퇴근시간대 18:00~19:59 유출 많은 지역
out_ins_wday_t1  = out_ins_wday[out_ins_wday['s_time'].isin ([])




## 평일 출근시간대 7~8:59 유출 , 퇴근시간대 18:00~19:59 유입 많은 지역









## 시간대구분 : 0~6시, 7시~10시, 11시~1시, 2시~4시, 5시~8시, 9시~11시

## 출근시간 유입인구 Top3

## 출근시간 유출인구 Top3

## 오후시간 / 저녁시간 유입 Top3

## 오후시간 / 저녁시간 유출 Top3







ss.columns


'연도', '월', 'date', '요일', '평일구분', 'd_time', 'o_admi_cd', 'd_admi_cd',
       'o_sgg', 'o_admi', 'd_sgg', 'd_admi', 'move_purpose', 'move_dist',
       'move_time', 'total_cnt', 'male_00_cnt', 'male_20_cnt', 'male_40_cnt',
       'male_60_cnt', 'feml_00_cnt', 'feml_20_cnt', 'feml_40_cnt',
       'feml_60_cnt'],