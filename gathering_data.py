import pandas as pd #판다스 임포트
import glob # csv파일 가져오기 위한 라이브러리
import os # OS임포트

# 기본 경로 설정
base_path = r'C:\\Users\\james\\2&3projects\\code\\programming_basic_project\\data'#기본 경로 설정(동일한 폴더 안에 들어있는 여러 파일을 합치기 위한 과정)
output_file = 'combined_output_1905_2024.csv' # 결과물 파일 이륾

# 경로 내의 모든 CSV 파일 가져오기
all_files = glob.glob(os.path.join(base_path, "*.csv")) #모든 


combined_df = pd.DataFrame() #합쳐진 데이터 프레임/  빈 데이터 프레임 생성

# 모든 CSV 파일을 읽어서 하나의 데이터프레임으로 합치기
for file in all_files:
    
    # CSV 파일 읽기
    df = pd.read_csv(file, encoding='cp949') 

    # 데이터프레임을 결합
    combined_df = pd.concat([combined_df, df], ignore_index=True)

# 결과를 새로운 CSV 파일로 저장
combined_df.to_csv(output_file, index=False)
