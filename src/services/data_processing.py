import os
import csv

# 현재 파일의 부모 디렉토리 경로 가져오기
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # 현재 파일의 절대 경로
PARENT_DIR = os.path.dirname(BASE_DIR)  # src
PARENT_DIR = os.path.dirname(PARENT_DIR)  # ai

# CSV 파일 경로 설정
CSV_FILE_PATH = os.path.join(PARENT_DIR, "data", "emotion_labelled_song_dataset.csv")  # 원본 CSV 파일의 절대 경로
OUTPUT_CSV_PATH = os.path.join(PARENT_DIR, "data", "filtered_data.csv")  # 출력 CSV 파일의 절대 경로

# data 패키지에 filtered_data.csv 만듦
def process_csv():
    data = []
    try:
        # 원본 CSV 파일 읽기
        with open(CSV_FILE_PATH, mode='r', encoding='utf-8') as csv_file:
            reader = csv.DictReader(csv_file)  # DictReader를 사용하여 열 이름으로 접근
            for row in reader:
                # 'labels'와 'uri' 열만 추출
                if 'labels' in row and 'uri' in row:
                    data.append({'labels': row['labels'], 'uri': row['uri']})

        # 새로운 CSV 파일로 저장
        with open(OUTPUT_CSV_PATH, mode='w', encoding='utf-8', newline='') as output_file:
            fieldnames = ['labels', 'uri']
            writer = csv.DictWriter(output_file, fieldnames=fieldnames)
            writer.writeheader()  # 헤더 작성
            writer.writerows(data)  # 데이터 작성

    except Exception as e:
        print(f"Error: {str(e)}")
        
# 함수 호출
process_csv()