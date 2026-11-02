#시도기준

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
df_2015 <- read.csv("H:/Microdata/220916_최초신청/지역별고용조사_ 하반기 C형_2015.csv", header=T)
#복사본 생성하기 
df_2015_copy <- df_2015

#사용컬럼 
#c1 : 1인가구 여부
#c2 : 조사연월 
#c3 : 가구주관계코드
#c15 : 최근3개월 급여평균
#c18 : 4자리 행정구역 분류코드 
#c19 : 시도가중값
#c24 : 막내자녀연령
df_2015_use <- df_2015_copy[,c("C1","C2","C3","C15","C18","C19","C24")]

# 1. 막내자녀 연령수가 학령인구인(7~12세) 가구추출 (22353)
#df_2019_schboy 
df_2015_schboy <- df_2015_use %>% filter(between(C24,7,12))

# 2. 시도별 한글명 컬럼 추가 
df_2015_sch_pre <- df_2015_schboy %>% mutate(C18_k = case_when(
  C18 == 11 ~ "서울",
  C18 == 21 ~ "부산",
  C18 == 22 ~ "대구",
  C18 == 23 ~ "인천",
  C18 == 24 ~ "광주",
  C18 == 25 ~ "대전",
  C18 == 26 ~ "울산",
  C18 == 29 ~ "세종",
  C18 == 31 ~ "경기",
  C18 == 32 ~ "강원",
  C18 == 33 ~ "충북",
  C18 == 34 ~ "충남",
  C18 == 35 ~ "전북",
  C18 == 36 ~ "전남",
  C18 == 37 ~ "경북",
  C18 == 38 ~ "경남",
  C18 == 39 ~ "제주",
  TRUE ~ NA_character_
))

# 3. 가구주관계코드 1(가구주) 추출
df_2015_sch_pre_1 <- filter(df_2015_sch_pre, C3 == 1)
#view(df_2019_sch_pre_1)

#추후 사용, 가구주관계코드 2(배우자)추출
df_2015_sch_pre_2 <- filter(df_2015_sch_pre, C3 ==2)
#df_2019_sch_pre_2

# 4.외벌이로 판단 (DUAL) = 0)
df_2015_sch_pre_1 <- df_2015_sch_pre_1 %>% mutate(DUAL = 0)


# 5. 시도가구 가중값 c20컬럼 소수점 반올림 정수형변환 
df_2015_sch_pre_1$C19 <- round(df_2015_sch_pre_1$C19)

# 6. 널값 0으로 대체 
df_2015_sch_pre_1[is.na(df_2015_sch_pre_1)] <- 0
#df_2019_sch_pre_1

# 7. 데이터프레임 널값 확인
sum(is.na(df_2015_sch_pre_1))

# 8.시도가중값 곱하기
df_2015_pre_weight <- df_2015_sch_pre_1[rep(row.names(df_2015_sch_pre_1), df_2015_sch_pre_1$C19),1:9]
df_2015_pre_weight_copy <- df_2015_pre_weight
df_2015_pre_weight_copy <- df_2015_pre_weight_copy[!(df_2015_pre_weight_copy$C15 == 0), ]

# ** quantile 이상치 해결 규칙 ** 
# 1번 : quantile 의 min, max 값이 동일할 경우 : 이상치 제거 진행 
# 2번(1번 이상치 제거 후 2차 이상발생 시 ) : 특정컬럼만 지정하여 위,아래 quantile mid값으로 변경 (단, 기존의의 컬럼값에서 변경할 것)


# 8.1 이상치 제거
# 8.1.1 인천(1번) 
ic01 <- df_2015_pre_weight_copy[df_2015_pre_weight_copy$C18 == 23 & df_2015_pre_weight_copy$DUAL == 0,]
ic_out <- boxplot(ic01$C15)$stats
str(ic_out) #이상치 확인 
ic01$C15 <- ifelse(ic01$C15 > ic_out[5]|ic01$C15 < ic_out[1],NA, ic01$C15)
df_2015_pre_weight_copy[df_2015_pre_weight_copy$C18 == 23 & df_2015_pre_weight_copy$DUAL == 0,]$C15 <- ic01$C15


# 9. 분위수 구하기
df_2015_pre_weight_quantile <- df_2015_pre_weight_copy %>% group_by(DUAL, C18, C18_k) %>%
  summarise(quantile1 = quantile(C15, 0.10, na.rm = TRUE),
            quantile2 = quantile(C15, 0.20, na.rm = TRUE),
            quantile3 = quantile(C15, 0.30, na.rm = TRUE),
            quantile4 = quantile(C15, 0.40, na.rm = TRUE),
            quantile5 = quantile(C15, 0.50, na.rm = TRUE),
            quantile6 = quantile(C15, 0.60, na.rm = TRUE),
            quantile7 = quantile(C15, 0.70, na.rm = TRUE),
            quantile8 = quantile(C15, 0.80, na.rm = TRUE),
            quantile9 = quantile(C15, 0.90, na.rm = TRUE),
            quantile10 = quantile(C15, 1.0, na.rm = TRUE),)

melt_quantile <- melt(df_2015_pre_weight_quantile, id.vars = c('DUAL','C18','C18_k'),
                      measure.vars = c('quantile1', 'quantile2', 'quantile3', 'quantile4', 'quantile5',
                                       'quantile6', 'quantile7', 'quantile8', 'quantile9', 'quantile10'))


melt_quantile <- melt_quantile %>% arrange(DUAL,C18,variable) %>% group_by(DUAL,C18)  %>%  mutate(value_1 = lag(value,1))
melt_quantile[is.na(melt_quantile)] <- 0

# 9.1 이상치 확인 
outlier <- subset(melt_quantile, value == value_1)
outlier

# 8.1.2 제주 (2번)

melt_quantile[which(melt_quantile$value == melt_quantile$value_1) + -1, 'value1'] = 
  (melt_quantile[which(melt_quantile$value == melt_quantile$value_1) + -1,]$value_1+melt_quantile[melt_quantile$value == melt_quantile$value_1,]$value_1)/2

melt_quantile[melt_quantile$value == melt_quantile$value_1, 'value1_1'] = 
  (melt_quantile[which(melt_quantile$value == melt_quantile$value_1) + -1,]$value_1+melt_quantile[melt_quantile$value == melt_quantile$value_1,]$value_1)/2


#a : value 값
a <- melt_quantile[!is.na(melt_quantile$value1),]
a["value"] <- a["value1"]

#b : value_1값
b <- melt_quantile[!is.na(melt_quantile$value1_1),]
b["value_1"] <- b["value1_1"]

# 평균값 추출 후 merge
c <- merge(melt_quantile,a, all =TRUE)
c <- merge(c,b, all = TRUE)

#value1,value1_1 컬럼 삭제 
d <- subset(c, select = -c(value1,value1_1))

melt_quantile <- d %>% group_by(C18) %>% filter(! duplicated(variable))
View(melt_quantile)

#  10. 분위수 개수 구하기
df_2015_not0 <- df_2015_sch_pre_1[!(df_2015_sch_pre_1$C15 =="0"),]

join_df <- left_join(df_2015_not0, melt_quantile, by = c('DUAL','C18','C18_k'))
join_df <- join_df %>% mutate(tf = ifelse(C15 >= value_1 & C15 < value, "TRUE","FALSE"))
join_df <- join_df[!(join_df$tf =="FALSE"),]


cnt_join_df <- join_df %>%
  group_by(DUAL,C18,variable) %>%
  summarise(cnt = sum(C19))

res_join_df <- left_join(melt_quantile, cnt_join_df, by = c('DUAL','C18','variable'))

# 10. 컬럼명 수정 및 저장
names(res_join_df) <- c("DUAL","SIDO_CODE","SIDO_NM","QUANTILE","MAX_Q","MIN_Q","CNT_Q")
res_join_df <- cbind(res_join_df, YEAR = rep(2015))
res_join_df <- res_join_df[,c("YEAR","DUAL","SIDO_CODE","SIDO_NM","QUANTILE","MAX_Q","MIN_Q","CNT_Q")]


#res_join_df$CNT_Q <- round(res_join_df$CNT_Q) 카운트값 소수점일때 반올림 
View(res_join_df)

write.csv(res_join_df, file = "H:/Microdata/take_out/sido_res_2015.csv", row.names = FALSE)
