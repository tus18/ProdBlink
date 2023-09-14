import cv2
import dlib
from imutils import face_utils
from scipy.spatial import distance
import numpy

class Landmark:#画像を処理するクラス(ランドマークを扱うとこ)
    def __init__(self):
        self.face_detector = dlib.get_frontal_face_detector()
        self.face_parts_detector = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")#ポイント位置を出力するツール
        self.mode = 0
        self.size = (240,320)

    def face_landmark_find(self,img):
        eye = 10
        img_gry = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = self.face_detector(img_gry, 1)

        for face in faces:
            # 顔のランドマーク検出
            landmark = self.face_parts_detector(img_gry, face)
            # 処理高速化のためランドマーク群をNumPy配列に変換(必須)
            landmark = face_utils.shape_to_np(landmark)

            left_eye_ear = self.calc_ear(landmark[42:48])
            right_eye_ear = self.calc_ear(landmark[36:42])
            eye = (left_eye_ear + right_eye_ear) / 2.0

            #白い画面の作成
            if self.mode == 1:
                img = cv2.imread("fig/white.png")
            #ランドマークの描画
            for (i, (x, y)) in enumerate(landmark):
                cv2.circle(img, (x, y), 1, (255, 0, 0), -1)

        return eye,img
    
    def change_mode(self):
        self.mode = (self.mode+1) % 2
    
    def calc_ear(self,eye):
        A = distance.euclidean(eye[1], eye[5])
        B = distance.euclidean(eye[2], eye[4])
        C = distance.euclidean(eye[0], eye[3])
        eye_ear = (A + B) / (2.0 * C)
        return eye_ear
    
    def image_show(self,img):
        cv2.imshow("frame",img)