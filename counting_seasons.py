import pandas as pd #판다스를 사용하기 위한 판다스 임포트
import matplotlib.pyplot as plt #맷플롯립 임포트
from matplotlib import font_manager, rc # VSC에서 한글 폰트를 사용하기 위한 방법
import numpy as np #수식 계산을 위해 필요함
from scipy.optimize import * #다항 함수 근사에 필요한 라이브러리

font_name = font_manager.FontProperties(fname="c:/Windows/Fonts/malgun.ttf").get_name() #한글 폰트 설정 방법
rc('font', family=font_name)#한글 폰트 설정 방법

#시작하는 연도와 끝나는 연도를 자주 사용하여 변수로 처리함 + 원하는 년도부터 시작 가능
start_year = 1910 #시작 연도
end_year = 2023 #끈 연도
year_num = end_year-start_year+1 #기간 설정 For문에 넣기 위함


df = pd.read_csv("C:\\Users\\james\\2&3projects\\Seoul_mean_data_1905.csv", encoding='utf-8') # CSV파일 불러오기

year_season_num_lst = [[0 for _ in range(year_num)] for __ in range(4)] #길이에 맞는 리스트 미리 만들어 두기 (겨울 수를 구할때, append가 아닌 +연산자를 사용하기 때문)
#0: 봄, 1:여름, 2:가을, 3:겨울

for i in range(start_year,end_year+1): #메인 for문, 연도 개수 만큼 반복한다
    index = i- start_year #리스트에 할당하기 위한 인덱스 조정
    year_df = df[df['일시'].str.match(f'^{i}')] # 정규 표현식을 사용하여 일시의 앞부분을 통해 원하는 연도만 처리한다 
    if len(year_df) != 365 and len(year_df) != 366: #중간에 결측값이 있을 것을 대비하여, 1년 날수가 맞지 않으면, 그 전년도와 똑같이 맞춰준다.
        year_season_num_lst[0][index] = year_season_num_lst[0][index-1] #봄 할당
        year_season_num_lst[1][index] = year_season_num_lst[1][index-1] # 여름 할당
        year_season_num_lst[2][index] = year_season_num_lst[2][index-1] # 가을 할당
        year_season_num_lst[3][index] = year_season_num_lst[3][index-1] # 겨울 할당
        continue # 해당 연도 스킵
        

    season = 0 #season 변수 초기화 / 현재 수를 세고 있는 연도의 상태를 표현한다.

    #앞으로 편하게 리스트를 사용학기 위한 데이터 프레임을 리스트로 변환
    dates = list(year_df['일시']) #해당 연도에 대해서만 일시를 리스트로 만든다
    temps = list(year_df['평균기온(°C)']) #해당 연도에 대해서만 평균기온을 리스트로 변환한다


    for x in range(len(dates)): # 해당 연도 for문
        if season == 0: #봄 측정 상태(디폴트값)
            # 7일 이상동안 5도 이상(봄의 조건)
            lst = [temps[a] >= 5.0  for a in range(x,x+7)] # 기준 일로부터 일주일 뒤 까지의 5도 이상인지에 대한 결과값을 반영한 bool값을 값으로 가지는 리스트 생성
            if all(lst): #전부 참
                start_date = x # 이 날을 기준으로 시작일
                season =1 # 앞으로 여름 측정
                year_season_num_lst[3][index] += start_date# 봄 일 전까지의 날짜를 겨울 일수에 추가한다. 
        elif season ==1:# 여름 측정 상태
            lst = [temps[a] >= 20.0  for a in range(x,x+7)]# 기준일로 부터 20도이상
            if all(lst):# 전부 충족하는지 판단
                end_date = x# 봄의 마지막 날짜 설정 = 여름 날짜 시작
                season+=1# 여름 계절 설정
                year_season_num_lst[0][index] = (end_date-start_date) # 봄 날짜 계산
                start_date = end_date # 여름 시작 날짜 설정
        elif season == 2: # 여름 상태
            lst = [temps[a] <= 20.0  for a in range(x,x+7)] # 가을 조건: 일주일 동안 20도 이하
            if all(lst): # 조건 다 만족 
                end_date = x # 여름의 끝  = 가을의 시작
                season +=1# 가을 계절 알려줌
                year_season_num_lst[1][index] = (end_date-start_date) #여름 일수 계산
                start_date = end_date # 가을 시작을 위한 start_date 초기화
        else: #가을 상태
            try: #오류 처리, 가을이 12월달을 넘어갈것을 대비함,
                lst = [temps[a] <= 5.0  for a in range(x,x+7)] # 가을 조건
                if all(lst): # 모두 만족
                    end_date = x #가을 끝 = 겨울 시작
                    year_season_num_lst[2][index] = (end_date-start_date) # 가을 일수 계산
            except: #예외 처리
                year_season_num_lst[2][index] = (len(dates) - start_date) #가을 계산
                end_date = len(dates) + 1 # for문 밑의 글에서 겨울에 더하지 않기 위한 과정
                break # 일년 마지막까지 처리를 마친후
    year_season_num_lst[3][index] += len(dates)+1 - end_date #마지막 남은 날들에 겨울을 더함
    if (year_season_num_lst[0][index] > 150 or year_season_num_lst[1][index] > 150 # 이상값 처리 4개중 하나가 150 넘는건  
    or year_season_num_lst[2][index]>150 or year_season_num_lst[3][index] > 150): # 데이터 상으로 뭔가 특수한 케이스에 해당하기 때문에 전년도와 똑같이 처리해준다.
        year_season_num_lst[0][index] = year_season_num_lst[0][index-1] #봄
        year_season_num_lst[1][index] = year_season_num_lst[1][index-1] #여름
        year_season_num_lst[2][index] = year_season_num_lst[2][index-1] #가을
        year_season_num_lst[3][index] = year_season_num_lst[3][index-1] #겨울
        
y = [i for i in range(start_year,end_year+1)] # 그래프를 위한 y축 설정
season_days = year_season_num_lst[3] #보고 싶은 계절
season_name = '겨울' # 보고싶은 계절 이름

plt.plot(y,season_days, marker='o', linestyle='-') #시각화
plt.title(f'연도별 {season_name} 일수 세기') # 제목
plt.xlabel('연도') # x축 제목
plt.ylabel(f'{season_name} 일수') # y축 제목
plt.show() #보여주기



################################################### 다항 함수 근사

# 근사 함수 정의 (예: 2차 함수)
def polynomial(x, a, b, c):
    # 다항식 정의: y = ax^2 + bx + c 형태
    return a * x**2 + b * x + c

# x, y 데이터
x_data = np.array(y)  # 연도 데이터
y_data = np.array(season_days)  # 계절 일수 데이터

# 데이터 근사
# curve_fit 함수를 이용해 다항 함수에 데이터를 근사시킴
params, _ = curve_fit(polynomial, x_data, y_data)  # 최적의 매개변수 a, b, c 찾기
a, b, c = params  # 매개변수 할당

# 근사 곡선 데이터
x_fit = np.linspace(start_year, end_year, 500)  # 근사 곡선을 위한 x 값 범위 생성
y_fit = polynomial(x_fit, a, b, c)  # 근사 곡선의 y 값 계산

# 시각화
plt.plot(x_data, y_data, 'o', label='Original Data', markersize=5)  # 원본 데이터 점으로 표시
plt.plot(x_fit, y_fit, '-', label=f'Polynomial Fit: {a:.2e}x² + {b:.2e}x + {c:.2e}')  # 근사 곡선 표시
plt.title(f'연도별 {season_name} 일수와 근사 곡선') #제목
plt.xlabel('연도') #x축 제목
plt.ylabel(f'{season_name} 일수') # y축 제목
plt.show() # 보여주기

# 근사된 함수식 출력
print(f"근사된 함수식: y = {a:.2e}x² + {b:.2e}x + {c:.2e}")


######################################################################################
# 테일러 다항식 근사 함수 정의 (여기서는 3차 다항식 사용)
def taylor_approximation(x, a, b, c, d):
    """
    테일러 다항식 근사 함수 정의:
    y = a + b * (x - 기준연도) + c * (x - 기준연도)^2 + d * (x - 기준연도)^3
    """
    return a + b * (x - end_year) + c * (x - end_year)**2 + d * (x - end_year)**3

# numpy 배열로 변환 (연도와 봄 일수 데이터를 사용)
x_data = np.array(y)  # x축 데이터: 연도
y_data = np.array(season_days)  # 계절일수

# 테일러 다항식 근사 수행
try:
    # curve_fit으로 최적화된 파라미터 추정
    params, _ = curve_fit(
        taylor_approximation,  # 근사 함수
        x_data, # x축 데이터 (연도)
        y_data, # y축 데이터 (계절 일수)
        p0=(1, 1, 1, 1), # 초기 파라미터 값 설정
        maxfev=10000 # 최대 반복 횟수 설정 (복잡한 데이터 대응)
    )
    a, b, c, d = params  # 최적화된 파라미터 추출

    # 근사 곡선 데이터 생성
    x_fit = np.linspace(start_year, end_year, 500)  # 근사 곡선의 x 범위
    y_fit = taylor_approximation(x_fit, a, b, c, d)  # 근사 곡선의 y 값 계산

    # 근사 결과 시각화
    plt.plot(x_data, y_data, 'o', label='Original Data', markersize=5) # 원본 데이터
    plt.plot(x_fit, y_fit, '-', color='green')  # 근사 곡선
    plt.title(f'연도별 {season_name} 일수와 테일러 근사 곡선')  # 제목
    plt.xlabel('연도')  # x축 제목
    plt.ylabel(f'{season_name} 일수')  # y축 제목
    plt.show()  # 그래프 표시

    # 근사된 함수식 출력
    print(f"테일러 근사 함수식: y = {a:.2e} + {b:.2e} * (x - {end_year}) + {c:.2e} * (x - {end_year})² + {d:.2e} * (x - {end_year})³")

except RuntimeError:
    # 근사가 실패할 경우 메시지 출력
    print("실패")
