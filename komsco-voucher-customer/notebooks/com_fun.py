# ---------------------------------------------------------------------------------------------
# 라이브러리 호출
# ---------------------------------------------------------------------------------------------
# 데이터 전처리 관련 라이브러리
import os
import time
import re
from tqdm import tqdm

# 데이터 불러오기 및 전처리 패키지
import pandas as pd
import numpy as np
import seaborn as sns
import pickle
import datetime as dt
from datetime import datetime, timedelta

import warnings; warnings.filterwarnings(action='ignore')

# 분석 관련 라이브러리
import statsmodels.api as sm
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from statsmodels.stats.outliers_influence import variance_inflation_factor
from sklearn.metrics import mean_squared_error, r2_score

# 시각화 관련 라이브러리

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib import rc
import matplotlib as mpl
import platform
plt.rcParams['axes.unicode_minus'] = False

# Window
if platform.system() == 'Windows':
    plt.rc('font', family='Malgun Gothic')
elif platform.system() == 'Darwin': # Mac
    plt.rc('font', family='AppleGothic')
else: #linux
    plt.rc('font', family='NanumGothic')

# ---------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------------------