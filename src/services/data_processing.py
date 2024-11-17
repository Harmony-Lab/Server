import os
import csv

# 현재 파일의 부모 디렉토리 경로 가져오기
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # 현재 파일의 절대 경로
PARENT_DIR = os.path.dirname(BASE_DIR)  # src
PARENT_DIR = os.path.dirname(PARENT_DIR)  # ai

# CSV 파일 경로 설정
CSV_FILE_PATH = os.path.join(PARENT_DIR, "data", "emotion_labelled_song_dataset.csv")  # 원본 CSV 파일의 절대 경로

# 라벨에 따른 파일 이름 매핑
label_to_filename = {
    '0': 'filtered_data_sad.csv',
    '1': 'filtered_data_happy.csv',
    '2': 'filtered_data_energetic.csv',
    '3': 'filtered_data_calm.csv'
}

# data 패키지에 필터링된 CSV 파일을 만듦
def process_csv():
    # 각 레이블에 해당하는 데이터를 저장할 딕셔너리
    data_dict = {key: [] for key in label_to_filename.keys()}
    
    try:
        # 원본 CSV 파일 읽기
        with open(CSV_FILE_PATH, mode='r', encoding='utf-8') as csv_file:
            reader = csv.DictReader(csv_file)  # DictReader를 사용하여 열 이름으로 접근
            for row in reader:
                # 'labels'와 'uri' 열만 추출
                if 'labels' in row and 'uri' in row:
                    # uri 값 처리: 'spotify:track:' 제거하고 새로운 URL 추가
                    uri = row['uri'].replace('spotify:track:', 'https://open.spotify.com/track/')
                    # labels에 따라 적절한 리스트에 추가
                    if row['labels'] in data_dict:
                        data_dict[row['labels']].append({'uri': uri})

        # 각 레이블에 따른 CSV 파일로 저장
        for label, data in data_dict.items():
            if data:  # 데이터가 있는 경우에만 파일 생성
                output_file_path = os.path.join(PARENT_DIR, "data", label_to_filename[label])
                with open(output_file_path, mode='w', encoding='utf-8', newline='') as output_file:
                    fieldnames = ['uri']
                    writer = csv.DictWriter(output_file, fieldnames=fieldnames)
                    #writer.writeheader()  # 헤더 작성
                    writer.writerows(data)  # 데이터 작성

    except Exception as e:
        print(f"Error: {str(e)}")
        
# 함수 호출
process_csv()
