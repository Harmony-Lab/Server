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
    'angry': 'filtered_data_energetic.txt',
    'fear': ['filtered_data_sad.txt', 'filtered_data_calm.txt'],
    'neutral': None,  # 다 섞어서 가져옴
    'disgust': ['filtered_data_sad.txt', 'filtered_data_calm.txt'],
    'surprise': ['filtered_data_happy.txt', 'filtered_data_energetic.txt']
}


def create_playlist(emotion: str, play_list_size: int) -> Playlist:
    # 감정에 따라 파일 경로 선택
    if emotion not in label_to_filename:
        raise ValueError("Invalid emotion provided.")
    
    file_names = label_to_filename[emotion]
    track_ids = []
    
    if isinstance(file_names, list):
        # 각 데이터셋에서 필요한 곡 수 계산
        base_count = play_list_size // len(file_names)
        remainder = play_list_size % len(file_names)  # 나머지 곡 수

        for i, file_name in enumerate(file_names):
            file_path = os.path.join(FILE_DIR, file_name)

            with open(file_path, 'r') as file:
                available_tracks = [line.strip() for line in file.readlines()]

            # 필요한 곡 수 결정
            if base_count > len(available_tracks):
                raise ValueError(f"Requested number of tracks exceeds available tracks in '{file_name}'.")

            # 랜덤으로 선택
            selected_tracks = random.sample(available_tracks, base_count)
            track_ids.extend(selected_tracks)

            # 나머지 곡을 첫 번째 데이터셋에 추가
            if i < remainder:
                if len(available_tracks) > base_count:
                    selected_tracks = random.sample(available_tracks, 1)
                    track_ids.extend(selected_tracks)

    elif file_names is None:
        # neutral인 경우 모든 파일에서 트랙을 가져옴
        all_file_names = set()  # 중복 제거를 위한 set 사용

        for name in label_to_filename.values():
            if isinstance(name, list):
                all_file_names.update(name)  # 리스트의 모든 요소 추가
            elif name is not None:
                all_file_names.add(name)  # 단일 파일 이름 추가
                
        all_tracks = []

        for file_name in all_file_names:
            file_path = os.path.join(FILE_DIR, file_name)
            with open(file_path, 'r') as file:
                all_tracks.extend([line.strip() for line in file.readlines()])

        # 플레이리스트 크기만큼 랜덤으로 선택
        if play_list_size > len(all_tracks):
            raise ValueError("Requested playlist size exceeds the number of available tracks.")
        
        track_ids = random.sample(all_tracks, play_list_size)

    else:
        # 단일 파일에서 곡을 가져올 경우
        file_path = os.path.join(FILE_DIR, file_names)
        with open(file_path, 'r') as file:
            available_tracks = [line.strip() for line in file.readlines()]

        if play_list_size > len(available_tracks):
            raise ValueError("Requested number of tracks exceeds available tracks.")

        track_ids = random.sample(available_tracks, play_list_size)
    
    songs = []

    # 트랙 정보 가져오기
    for track_id in track_ids:
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
for song in playlist.songs:
    print(f"url: {song.url}")