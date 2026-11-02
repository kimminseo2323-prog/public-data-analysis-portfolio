# public-data-analysis-portfolio

라임솔루션㈜ 빅데이터사업본부 데이터분석팀 재직(2022.07 – 2025.02) 중 수행한 공공기관 데이터 분석 과제 10건의 **분석 코드 정리본**입니다. 주로 "정책현안 데이터분석 및 기술지원 사업"(2022·2023·2024년도) 과제이며, 각 폴더에 코드·README·합성 샘플·보고서 캡쳐를 담았습니다.

> **원천 데이터와 발주처 제출 보고서는 비공개입니다.** 레포에는 코드와 구조만 같은 합성 샘플(`data/sample/`, numpy seed 42)만 들어 있습니다. 사내 공통 모듈(`config`, `utils`)과 DB 접속부는 제외·주석 처리했습니다.

## 프로젝트 목록

| 기간 | 프로젝트 | 발주처 | 핵심 방법 | 본인 역할 | 폴더 |
|---|---|---|---|---|---|
| 2022.08–12 | 교육부 초등전일제(늘봄교실) 수요예측 | 교육부 (행안부 통합데이터분석센터) | 통계청 MDIS 원격 R 집계, 상관분석, (팀) ARIMA | 인턴: MDIS R 코드·데이터 수집·상관분석·Excel | [neulbom-demand-mdis-r](./neulbom-demand-mdis-r) |
| 2023.03–05 | 민원인 제출 구비서류 다빈도 분석 | 디지털플랫폼정부위원회 | KoNLPy 형태소, word2vec 유사도, 워드클라우드 | 전 과정 | [civil-document-frequency](./civil-document-frequency) |
| 2023.04–06 | 취약지역 생활여건 개조사업 대상지·우선순위 | 공주시 | 10개 지표 Min-Max, 가중 합산, 밀집도, QGIS | 전 과정 | [gongju-vulnerable-area](./gongju-vulnerable-area) |
| 2023.07–08 | 농기계 임대현황 분석 | 진도군 농업기술센터 | 기종·시기·지역 현황분석, 엑셀 필터 시각화 | 전 과정 | [jindo-farm-machinery-rental](./jindo-farm-machinery-rental) |
| 2023.08–10 | 생활인구 분석 (공주시·시흥시) | 공주시 / 시흥시 | 통신·카드·Tmap 통합, 시공간 패턴, K-Means 유형화 | 전 과정 | [living-population](./living-population) |
| 2023.09–12 | 지역사랑상품권 고객데이터 분석 | 한국조폐공사 | 대용량 분할 전처리(ODS), 결제 패턴, 지역·업종 QGIS | 전 과정 | [komsco-voucher-customer](./komsco-voucher-customer) |
| 2023.11–12 | 생활업종 빅데이터 분석 | 아산시 | 인허가 196종 통합, 창폐업·영업기간, 외부데이터 연계 | 전 과정 | [asan-local-business](./asan-local-business) |
| 2024.05–07 | 북부권 산업단지 정주여건 개선 분석 | 세종특별자치시 | POI 공급량 × 최단거리 접근성, QGIS Heatmap | 전 과정 | [sejong-industrial-living](./sejong-industrial-living) |
| 2024.07–10 | 주차 수요·공급 분석 | 수원시청 | 수요·공급 지표, KT 인구 연계, MariaDB 적재, 주차체감지도 | 데이터 구축·지표·시각화·DB 적재 | [suwon-parking-supply-demand](./suwon-parking-supply-demand) |
| 2024.10–12 | 강남역 인구이동 및 상권·이면도로 분석 | 서초구청 스마트도시과 | 신한카드·생활이동 집계, 서초 vs 강남 비교, QGIS | 전 과정 | [seocho-gangnam-commercial](./seocho-gangnam-commercial) |

## 공통 기술 스택
- **언어·라이브러리**: Python(Pandas, NumPy, GeoPandas, Shapely, Scikit-learn, Matplotlib/Seaborn, KoNLPy, gensim), R(dplyr·tidyr·reshape2, MDIS 원격분석환경)
- **DB·SQL**: MariaDB(JOIN·집계 조회, Python 적재 파이프라인)
- **GIS**: QGIS(행정동·격자·버퍼 시각화), EPSG 5179/5181/4326 좌표 변환
- **데이터**: 공공·행정 데이터, 카드(BC·신한), 통신(SKT·KT), 내비(Tmap), 신용(KCB), 인허가(LOCALDATA), 통계청 MDIS
- **협업·산출**: Slack·Confluence, 결과보고서(PPT), 엑셀 필터형 시각화 자료

## 레포 구성 원칙
- 각 폴더: `README.md` · `src/` 또는 `notebooks/` · `data/sample/` · `docs/images/`
- 노트북은 출력 셀을 모두 제거했습니다. 코드 안의 경로(`H:/Microdata/...`, `D:/data/...`, 사내 config 경로)는 당시 환경 기준이므로 실행 시 환경에 맞게 수정해야 합니다.
- 동료가 작성한 코드(공통모듈, 일부 스크립트)는 포함하지 않았고, 포함 여부와 치환 내역은 `_manifest.md`, `_redactions.md`에 기록했습니다.
- 라이선스는 미정입니다.

## 참고
- 경력 전체 개요와 과제별 상세는 Obsidian 노트(`01_경력_라임솔루션/_라임솔루션_경력_개요`)를 기준으로 작성했습니다.
- 라임솔루션 재직 중 수행한 나머지 과제(양주시 지역불균형, 시흥시 문화생활SOC, 대전 타슈 재배치, 광양시 공영주차장 최적입지)는 별도 레포로 정리합니다.
