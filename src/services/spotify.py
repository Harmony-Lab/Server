import os
import random
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from src.models.song import Song
from src.models.playlist import Playlist


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

# 라벨에 따른 파일 이름 매핑
label_to_filename = {
    'sad': 'filtered_data_sad.txt',
    'happy': 'filtered_data_happy.txt',
    'energetic': 'filtered_data_energetic.txt',
    'neutral': 'filtered_data_calm.txt'
}

def create_playlist(emotion: str, play_list_size: int) -> Playlist:
    # 감정에 따라 파일 경로 선택
    if emotion not in label_to_filename:
        raise ValueError("Invalid emotion provided.")
    
    file_name = label_to_filename[emotion]
    file_path = os.path.join(FILE_DIR, file_name)
    
    with open(file_path, 'r') as file:
        track_ids = [line.strip() for line in file.readlines()]
        
    # 플레이리스트 크기만큼 랜덤하게 트랙 ID 선택
    if play_list_size > len(track_ids):
        raise ValueError("Requested playlist size exceeds the number of available tracks.")
    
    random_selected_track_ids = random.sample(track_ids, play_list_size)
    
    songs = []

    # 트랙 정보 가져오기
    for track_id in random_selected_track_ids:
        try:
            track_info = sp.track(track_id)
            track_name = track_info['name']  # 제목
            artists = ", ".join(artist['name'] for artist in track_info['artists'])  # 가수
            url = f"https://open.spotify.com/track/{track_id}"  # Spotify 링크 생성
            
            # Song 객체 생성
            song = Song(title=track_name, artist=artists, url=url)
            songs.append(song)
            
        except Exception as e:
            print(f"Error retrieving track {track_id}: {e}")
            
    # Playlist 객체 생성 및 반환
    return Playlist(size=play_list_size, songs=songs)

playlist = create_playlist("sad", 5)
print(playlist)