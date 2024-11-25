from deepface import DeepFace
import cv2
import numpy as np
import base64


def BasetoImage(base64_data):
    # 1. 헤더 제거 (예: "data:image/jpeg;base64," 부분 제거)
    base64_data = base64_data.split(",")[1]

    # 2. Base64 디코딩
    image_data = base64.b64decode(base64_data)

    # 3. 디코딩된 데이터를 numpy 배열로 변환
    image_array = np.frombuffer(image_data, np.uint8)

    # 4. OpenCV에서 읽을 수 있는 형식으로 변환
    image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
    return image


def GetEmotionProbsDeepFace(img):
    # DeepFace를 사용해 감정 확률 추출
    objs = DeepFace.analyze(
        img_path=img,
        actions=['emotion'],
        detector_backend='retinaface',
    )
    objs = objs[0]
    return objs['dominant_emotion']  # 감정별 확률 분포 반환


async def detect_emotion(img_path):
    # Base64 데이터 이미지 변환
    img = BasetoImage(base64_data=img_path)

    # DeepFace로 감정 분석
    deepface_dominant_emotion = GetEmotionProbsDeepFace(img)

    return deepface_dominant_emotion


# img = BasetoImage(base64_data=img_path)
# print(GetEmotionProbsDeepFace(img))
