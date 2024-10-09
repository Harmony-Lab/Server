from deepface import DeepFace


objs = DeepFace.analyze(
    img_path="../data/angry_test.jpg",
    actions=['age', 'gender', 'race', 'emotion']
)

print(objs)
