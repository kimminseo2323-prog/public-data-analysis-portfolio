#2020년도 전국 기준

getwd()#현재경로
#install.packages("dplyr", repos="file:///I:/R-library/2108", type="win.binary")
#install.packages("tidyr", repos="file:///I:/R-library/2108", type="win.binary")
#install.packages("tidyverse", repos="file:///I:/R-library/2108", type="win.binary")
#install.packages("reshape2", repos="file:///I:/R-library/2108", type="win.binary")

library(tidyr)
library(dplyr)
library(tidyverse)
library(reshape2)

#데이터 불러오기
df_2020<- read.csv("H:/Microdata/220916_최초신청/지역별고용조사_ 하반기 C형_2020.csv", header=T)

#복사본생성
df_2020_copy <- df_2020

#사용컬럼 c1 / c3 / c4 / c16 / c17 / c20 / c26 /c27
#c1:가구단위일련번호,c3:조사연월,c4:가구주관계코드,C6:만연령, c16:최근3개월 월평균 급여, c17:배우자동거여부, c20:2자리시도분류코드,c21:시도가중값 ,c26:막내자녀연령
df_2020_use <- df_2020_copy[,c("C1","C3","C4","C6","C16","C17","C20","C21","C26")]


#df_2020_schboy <- 막내자녀 연령수가 학령인구인(7~12세) 가구추출 
df_2020_schboy <- df_2020_use %>% filter(between(C26,7,12)) 


df_2020_sch_pre <- df_2020_schboy %>% group_by(C1) %>% mutate(C16_SUM = sum(C16, na.rm = TRUE)) 
#부부 별 급여합계를 c16_SUM 컬럼으로 C1그룹별 추가 

df_2020_sch_pre <- df_2020_sch_pre %>% mutate(C20_k = case_when(
  C20 == 11 ~ "서울",
  C20 == 21 ~ "부산",
  C20 == 22 ~ "대구",
  C20 == 23 ~ "인천",
  C20 == 24 ~ "광주",
  C20 == 25 ~ "대전",
  C20 == 26 ~ "울산",
  C20 == 29 ~ "세종",
  C20 == 31 ~ "경기",
  C20 == 32 ~ "강원",
  C20 == 33 ~ "충북",
  C20 == 34 ~ "충남",
  C20 == 35 ~ "전북",
  C20 == 36 ~ "전남",
  C20 == 37 ~ "경북",
  C20 == 38 ~ "경남",
  C20 == 39 ~ "제주",
  TRUE ~ NA_character_
))


#2020_데이터 전체 적용
#필요컬럼 c1,c3,c20,c21,c26,c16_sum,c20_k,dual 
#dual 컬럼 0,1로바꿔놓기
#컬럼순서: c3.c20,c20_k,c1,dual,c16_sum,c21,c26

# 1. 2020_데이터 전체 적용
df_2020_pre_copy <- df_2020_sch_pre


#혼자있는 외벌이만 추출
df_2020_pre_solo <- df_2020_pre_copy[which(!(duplicated(df_2020_pre_copy$C1)|duplicated(df_2020_pre_copy$C1, fromLast = T))),]
df_2020_pre_solo <- df_2020_pre_solo %>% mutate(dual = "FALSE")


#맞벌이 + 외벌이 추출
df_2020_pre_dual <- df_2020_pre_copy[which(duplicated(df_2020_pre_copy$C1)|duplicated(df_2020_pre_copy$C1, fromLast = T)),] 

df_2020_pre_dual[is.na(df_2020_pre_dual)] <- 0
df_2020_pre_dual <- df_2020_pre_dual %>% group_by(C1) %>% mutate(C16_log = as.logical(C16))
df_2020_pre_dual <- df_2020_pre_dual %>% group_by(C1) %>% mutate(dual = (all(C16_log == 1 )))
df_2020_pre_dual <- df_2020_pre_dual[duplicated(df_2020_pre_dual$C1),]
df_2020_pre_dual <- df_2020_pre_dual[!(names(df_2020_pre_dual) %in% c("C16_log"))]

# 2. 맞벌이 외벌이 데이터프레임 합치기
df_2020_pre_solo$dual <- as.logical(df_2020_pre_solo$dual) ## 외벌이 프레임의 'dual'컬럼 자료형변환 , 문자형 -> 논리형
df_2020_pre_all <- rbind(df_2020_pre_dual,df_2020_pre_solo) ## 데이터프레임 합치기


# 3. dual 컬럼 수치형으로 변경 | 맞벌이(TRUE) : 1, 외벌이(FALSE) : 0
df_2020_pre_all$dual <- as.numeric(df_2020_pre_all$dual)


# 4. 필요컬럼만 남기기 c1,c3,c20,c21,c26,c16_sum,c20_k,dual 
df_2020_pre_all <- subset(df_2020_pre_all, select = c(C3,dual,C20,C20_k,C1,C16_SUM,C21,C26))

# 5. 시도가구 가중값 c21컬럼 소수점 반올림 정수형변환 
df_2020_pre_all$C21 <- round(df_2020_pre_all$C21)

# 6. 데이터프레임 널값 확인
sum(is.na(df_2020_pre_all))

#  7. 시도가중값 곱하기
df_2020_pre_weight <- df_2020_pre_all[rep(row.names(df_2020_pre_all), df_2020_pre_all$C21),1:8]
df_2020_pre_weight_copy <- df_2020_pre_weight
df_2020_pre_weight_copy <- df_2020_pre_weight_copy[!(df_2020_pre_weight_copy$C16_SUM == 0), ]


#  8. 분위수 구하기
df_2020_pre_weight_quantile <- df_2020_pre_weight_copy %>% group_by(dual) %>%
  summarise(quantile1 = quantile(C16_SUM, 0.10, na.rm = TRUE),
            quantile2 = quantile(C16_SUM, 0.20, na.rm = TRUE),
            quantile3 = quantile(C16_SUM, 0.30, na.rm = TRUE),
            quantile4 = quantile(C16_SUM, 0.40, na.rm = TRUE),
            quantile5 = quantile(C16_SUM, 0.50, na.rm = TRUE),
            quantile6 = quantile(C16_SUM, 0.60, na.rm = TRUE),
            quantile7 = quantile(C16_SUM, 0.70, na.rm = TRUE),
            quantile8 = quantile(C16_SUM, 0.80, na.rm = TRUE),
            quantile9 = quantile(C16_SUM, 0.90, na.rm = TRUE),
            quantile10 = quantile(C16_SUM, 1.0, na.rm = TRUE),)

melt_quantile <- melt(df_2020_pre_weight_quantile, id.vars = c('dual'),
                      measure.vars = c('quantile1', 'quantile2', 'quantile3', 'quantile4', 'quantile5',
                                       'quantile6', 'quantile7', 'quantile8', 'quantile9', 'quantile10'))

melt_quantile <- melt_quantile %>% arrange(dual,variable) %>% group_by(dual)  %>%  mutate(value_1 = lag(value,1))
melt_quantile[is.na(melt_quantile)] <- 0
View(melt_quantile)

#  9. 분위수 개수 구하기
df_2020_pre_all_not0 <- df_2020_pre_all[!(df_2020_pre_all$C16_SUM =="0"),]

join_df <- left_join(df_2020_pre_all_not0, melt_quantile, by = c('dual'))
join_df <- join_df %>% mutate(tf = ifelse(C16_SUM >= value_1 & C16_SUM < value, "TRUE","FALSE")) 
join_df <- join_df[!(join_df$tf =="FALSE"),]


cnt_join_df <- join_df %>%
  group_by(dual, variable) %>%
  summarise(cnt = sum(C21))

res_join_df <- left_join(melt_quantile, cnt_join_df, by = c('dual', 'variable'))

# 10. 컬럼명 수정 및 저장 
names(res_join_df) <- c("DUAL","QUANTILE","MAX_Q","MIN_Q","CNT_Q")
res_join_df <- cbind(res_join_df, YEAR = rep(2020))
res_join_df <- res_join_df[,c("YEAR","DUAL","QUANTILE","MAX_Q","MIN_Q","CNT_Q")]
View(res_join_df)

write.csv(res_join_df, file = "H:/Microdata/take_out/all_res_2020.csv",row.names = FALSE)
