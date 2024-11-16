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
print(sp)

df = pd.read_csv(r'data\filtered_data.csv')

# uri = 'spotify:track:1fyysXwSGNtMeqMBLwW3SI'

# track = sp.track(uri)
# print(track)
# track_name = track['name']
# artist_names = ", ".join([artist['name'] for artist in track['artists']])

# print(f"track_name = {track_name}")
# print(f"artist_names = {artist_names}")
# # URI 리스트를 최대 50개씩 나누기
# uris = df['uri'].tolist()
# batch_size = 50
# batches = [uris[i:i + batch_size] for i in range(0, len(uris), batch_size)]

# # 트랙 정보 가져오기
# track_names = []
# artist_names = []

# for batch in batches:
#     tracks_info = sp.tracks(batch)
#     for track in tracks_info['tracks']:
#         track_names.append(track['name'])
#         artist_names.append(track['artists'][0]['name'])

# # 결과를 DataFrame에 추가
# df['track_name'] = track_names
# df['artist_name'] = artist_names

# # 새 CSV 파일로 저장
# df.to_csv(
#     'C:/Users/dldns/K-lab/Server/data/filtered_data_with_tracks.csv', index=False)

# print("곡 정보가 추가된 CSV 파일이 저장되었습니다!")
