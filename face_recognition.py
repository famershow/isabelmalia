

import cv2

class FaceRecognizer:
    def __init__(self, cascade_file_path):
        self.face_cascade = cv2.CascadeClassifier(cascade_file_path)

    # 识别人脸，并返回人脸图像、人脸所在位置和人脸所在区域
    def detect_face(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
        if len(faces) > 0:
            # 只处理第一个识别到的人脸
            x, y, w, h = faces[0]
            return frame[y:y+h, x:x+w], (x, y), (w, h)
        else:
            return None, None, None

    # 绘制人脸边框和标签
    def draw_face_label(self, frame, label, face_rect):
        (x, y), (w, h) = face_rect
        cv2.putText(frame, label, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)


