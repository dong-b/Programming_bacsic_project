# import pandas as pd  # 판다스 임포트

# file_path = 'C:\\Users\\james\\2&3projects\\combined_output.csv'  # 파일 경로 설정

# df = pd.read_csv(file_path, encoding='utf-8')  # csv 파일을 데이터 프레임으로 변환

# df.drop(['지점', '지점명'], axis=1, inplace=True)  # 지점 삭제하기

# # 그룹화하여 평균 계산하고 새로운 데이터프레임에 저장
# mean_df = df.groupby('일시')['평균기온(°C)'].mean().round(1).reset_index()# 

# # 결과를 CSV 파일로 저장
# mean_df.to_csv('mean_data.csv', index=False)

# print('평균 데이터가 성공적으로 저장되었습니다.')




# #########################2024 제외한 데이터 만들기
# import pandas as pd  # 판다스 임포트

# file_path = 'C:\\Users\\james\\2&3projects\\combined_output.csv'  # 파일 경로 설정

# df = pd.read_csv(file_path, encoding='utf-8')  # csv 파일을 데이터 프레임으로 변환

# df.drop(['지점', '지점명'], axis=1, inplace=True)  # 지점 삭제하기

# # 그룹화하여 평균 계산하고 새로운 데이터프레임에 저장
# mean_df = df.groupby('일시')['평균기온(°C)'].mean().round(1).reset_index()

# mean_df = mean_df[mean_df['일시'].str[:4] != '2024']

# # 결과를 CSV 파일로 저장
# mean_df.to_csv('mean_data_2024removed.csv', index=False)

# print('평균 데이터가 성공적으로 저장되었습니다.')


#########################서울에만 해당 하는 값 모으기
import pandas as pd  # 판다스 임포트

file_path = 'C:\\Users\\james\\2&3projects\\combined_output_1905_2024.csv'  # 파일 경로 설정

df = pd.read_csv(file_path, encoding='utf-8')  # csv 파일을 데이터 프레임으로 변환

df2 = df.loc[df['지점명'] == '서울'] #지점명이 서울인것만 모아서 새 대이터 프레임 생성

df2.drop(['지점', '지점명'], axis=1, inplace=True)  # 지점 삭제하기

df2 = df2[df2['일시'].str[:4] != '2024'] #2024는 제외해서 저장

# 결과를 CSV 파일로 저장
df2.to_csv('Seoul_mean_data_1905.csv', index=False)




