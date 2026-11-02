# -*- coding: utf-8 -*-
"""
[재구성 예시] 공주시 취약지역 점수 모델
=========================================
notebooks/01_pre_data_분석.ipynb 의 "점수환산" 단계만 떼어내 스크립트로 다시 쓴 예시입니다.
지표 산출(리 단위 집계·버퍼 밀집도)은 원천 데이터가 필요해 포함하지 않았고,
이미 만들어진 리 단위 지표표(data/sample/ri_indicators_sample.csv 와 같은 구조)를 입력으로 받습니다.
가중치는 원 노트북의 값을 그대로 사용했습니다. (docs/methodology.md 참고)

실행:  python src/score_model_example.py [지표표 CSV 경로]
"""
import sys
import os
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

KEY_COLS = ["코드", "행정기관", "리"]
INDICATORS = [
    "기초생활수급자_비율", "차상위계층_비율", "장애인_비율",
    "상수도보급률", "하수도보급률", "65세이상고령자_비율",
    "30년이상_노후주택비율", "빈집_비율", "슬레이트주택_비율",
    "밀집도_200m", "밀집도_400m",
]
# 항목 점수 = 표준화 지표의 평균(또는 단일 지표) × 가중치. 상·하수도는 (1 - 값)으로 역방향.
ITEMS = [
    ("취약계층비율_기초생활수급자/차상위", ["기초생활수급자_비율", "차상위계층_비율"], 6, False),
    ("취약계층비율_고령자/장애인", ["장애인_비율", "65세이상고령자_비율"], 4, False),
    ("생활위생인프라_상수도", ["상수도보급률"], 4, True),
    ("생활위생인프라_하수도", ["하수도보급률"], 4, True),
    ("주택취약도_노후주택", ["30년이상_노후주택비율"], 5, False),
    ("주택취약도_슬레이트", ["슬레이트주택_비율"], 5, False),
    ("주택취약도_공폐가", ["빈집_비율"], 2, False),
    ("밀집도_200m기준", ["밀집도_200m"], 4, False),
]


def minmax_scale(df: pd.DataFrame) -> pd.DataFrame:
    """지표 컬럼을 0–1로 Min-Max 스케일링 (원 노트북과 같이 소수 둘째 자리 반올림)."""
    out = df.copy()
    scaler = MinMaxScaler()
    out[INDICATORS] = scaler.fit_transform(out[INDICATORS])
    return out.round(2).sort_values("코드").reset_index(drop=True)


def score(df_scaled: pd.DataFrame) -> pd.DataFrame:
    """항목 점수와 총합점수 산출."""
    res = df_scaled[KEY_COLS].copy()
    item_cols = []
    for name, cols, weight, reverse in ITEMS:
        v = df_scaled[cols].mean(axis=1).round(2)
        if reverse:
            v = 1 - v
        res[name] = v * weight
        item_cols.append(name)
    res["총합점수"] = res[item_cols].sum(axis=1)
    return res


def main(path: str) -> None:
    df = pd.read_csv(path, encoding="utf-8-sig")
    scaled = minmax_scale(df)
    result = score(scaled)
    top5 = result.sort_values("총합점수", ascending=False).head(5)
    pd.set_option("display.width", 200)
    print("[총합점수 상위 5개 리]")
    print(top5.to_string(index=False))
    # 항목별로 시 평균보다 취약한지 분해
    item_cols = [i[0] for i in ITEMS]
    mean = result[item_cols].mean()
    print("\n[상위 5개 리: 시 평균보다 취약한 항목 수 / 8]")
    for _, row in top5.iterrows():
        n_bad = int((row[item_cols] > mean).sum())
        print(f"  {row['행정기관']} {row['리']}: {n_bad}개 항목")


if __name__ == "__main__":
    default = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "sample", "ri_indicators_sample.csv")
    main(sys.argv[1] if len(sys.argv) > 1 else default)
