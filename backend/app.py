from flask import Flask
import cv2
import dlib
import numpy as np
import pyttsx3
import os
from scipy.spatial import distance as dist
from tensorflow.keras.models import load_model
from tensorflow.keras.optimizers import Adam
import threading

app = Flask(__name__)
# Paths
SHAPE_PREDICTOR_PATH = "shape_predictor_68_face_landmarks.dat"
MODEL_PATH = "drowsiness_model.h5"

if not os.path.exists(SHAPE_PREDICTOR_PATH) or not os.path.exists(MODEL_PATH):
    raise FileNotFoundError("Model or Shape Predictor not found!")

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(SHAPE_PREDICTOR_PATH)
cnn_model = load_model(MODEL_PATH, compile=False)
cnn_model.compile(optimizer=Adam(), loss='binary_crossentropy', metrics=['accuracy'])

# Text to Speech Setup
engine = pyttsx3.init()
engine.setProperty('rate', 160)

def speak(text):
    if not engine._inLoop:
        engine.say(text)
        engine.runAndWait()

def eye_aspect_ratio(eye):
    A = dist.euclidean(eye[1], eye[5])
    B = dist.euclidean(eye[2], eye[4])
    C = dist.euclidean(eye[0], eye[3])
    return (A + B) / (2.0 * C)

def mouth_aspect_ratio(mouth):
    A = dist.euclidean(mouth[2], mouth[10])
    B = dist.euclidean(mouth[4], mouth[8])
    C = dist.euclidean(mouth[0], mouth[6])
    return (A + B) / (2.0 * C)

EYE_AR_THRESH = 0.3
EYE_AR_CONSEC_FRAMES = 20  # ~1 sec if fps=20
MAR_THRESH = 0.6

COUNTER = 0
YAWN_COUNTER = 0

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = detector(gray)

    for face in faces:
        shape = predictor(gray, face)
        landmarks = np.array([[p.x, p.y] for p in shape.parts()])

        left_eye = landmarks[36:42]
        right_eye = landmarks[42:48]
        mouth = landmarks[48:68]

        ear = (eye_aspect_ratio(left_eye) + eye_aspect_ratio(right_eye)) / 2.0
        mar = mouth_aspect_ratio(mouth)

        # For CNN Prediction
        (x, y, w, h) = (face.left(), face.top(), face.width(), face.height())
        face_img = cv2.resize(frame[y:y+h, x:x+w], (100, 100))
        face_img = face_img.astype("float") / 255.0
        face_img = np.expand_dims(face_img, axis=0)
        pred = cnn_model.predict(face_img)[0][0]

        # Display Metrics
        cv2.putText(frame, f'EAR: {ear:.2f}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,255), 2)
        cv2.putText(frame, f'MAR: {mar:.2f}', (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,255), 2)
        cv2.putText(frame, f'CNN: {pred:.2f}', (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,255), 2)

        # EAR Detection Logic
        if ear < EYE_AR_THRESH:
            COUNTER += 1
            if COUNTER >= EYE_AR_CONSEC_FRAMES:
                cv2.putText(frame, "DROWSINESS ALERT!", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0,0,255), 3)
                speak("Wake up! You seem sleepy!")
        else:
            COUNTER = 0

        # MAR Detection Logic
        if mar > MAR_THRESH:
            YAWN_COUNTER += 1
            if YAWN_COUNTER >= 15:  # ~1 sec
                cv2.putText(frame, "YAWNING ALERT!", (x, y+h+30), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255,0,0), 3)
                speak("Stop yawning! Stay fresh!")
        else:
            YAWN_COUNTER = 0

        cv2.rectangle(frame, (x, y), (x + w, y + h), (0,255,0), 2)

    cv2.imshow("Drowsiness Detection", frame)

    if cv2.waitKey(1) & 0xFF == 27:  # ESC to quit
        break

cap.release()
cv2.destroyAllWindows()

@app.route('/')
def home():
    return "Drowsiness Detection Running..."




