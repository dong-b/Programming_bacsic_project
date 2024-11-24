import matplotlib.pyplot as plt # 맷플롯립 설정
import pandas as pd # 판다스 설정
from matplotlib import font_manager, rc # 한글 폰트

font_name = font_manager.FontProperties(fname="c:/Windows/Fonts/malgun.ttf").get_name() # 한글 폰트
rc('font', family=font_name) # 한글 폰트

df = pd.read_csv("C:\\Users\\james\\2&3projects\\Seoul_mean_data_1905.csv", encoding='utf-8') # 경로 설정

# '일시' 열을 datetime 형식으로 변환
df['일시'] = pd.to_datetime(df['일시'], errors='coerce')

# 변환에 실패한 행 제거
df = df.dropna(subset=['일시'])

# 연도 추출
df['연도'] = df['일시'].dt.year

# 연도별 평균 계산
annual_mean = df.groupby('연도')['평균기온(°C)'].mean()

# 그래프 그리기
plt.figure(figsize=(10, 6))
plt.plot(annual_mean.index, annual_mean.values, marker='o', linestyle='-')
plt.title('연도별 평균 기온 변화')
plt.xlabel('연도')
plt.ylabel('평균기온(°C)')
plt.grid(True)
plt.show()
