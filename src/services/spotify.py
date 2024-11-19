import os
import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Spotify API 클라이언트 ID와 시크릿 설정
client_id = 'aaa35d078a2d4103a86a512a01773b08'
client_secret = 'de1f329c42a748c3957f95b55210346c'

# Spotify API 인증
auth_manager = SpotifyClientCredentials(
    client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(auth_manager=auth_manager)

# 현재 파일의 부모 디렉토리 경로 가져오기
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # 현재 파일의 절대 경로
PARENT_DIR = os.path.dirname(BASE_DIR)  # src
PARENT_DIR = os.path.dirname(PARENT_DIR)  # ai
FILE_DIR = os.path.join(PARENT_DIR, "data")
FILE_PATH = os.path.join(FILE_DIR, "filtered_data_calm.txt")

# 라벨에 따른 파일 이름 매핑
label_to_filename = {
    'sad': 'filtered_data_sad.txt',
    'happy': 'filtered_data_happy.txt',
    'energetic': 'filtered_data_energetic.txt',
    'calm': 'filtered_data_calm.txt'
}

with open(FILE_PATH, 'r') as file:
    track_ids = [line.strip() for line in file.readlines()]

# 트랙 정보 가져오기
for track_id in track_ids:
    try:
        track_info = sp.track(track_id)
        track_name = track_info['name']  # 제목
        artists = ", ".join(artist['name']
                            for artist in track_info['artists'])  # 가수
        print(f"Track: {track_name}, Artists: {artists}")
    except Exception as e:
        print(f"Error retrieving track {track_id}: {e}")