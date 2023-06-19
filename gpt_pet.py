import subprocess
import time
from face_recognition import FaceRecognizer
from voice_recognition import VoiceRecognizer
from weather import WeatherAPI

# 用户和角色列表
users = [("Tom", "owner"), ("Bob", "guest"), ("Emma", "child")]

# 角色对应的处理方式和回答内容
roles = {
    "owner": {"greeting": "Hi, Tom! Welcome back! How was your day at work?", "rules": "Don't forget to ask me anything."},
    "guest": {"greeting": "Hi, guest! Welcome to our home.", "rules": "Please feel free to ask me anything you need."},
    "child": {"greeting": "Hi, Emma! Do you want to play a game?", "rules": "Don't forget to ask me before touching anything."}
}

# 初始化人脸识别模块和语音识别模块
face_recognizer = FaceRecognizer("haarcascade_frontalface_default.xml")
voice_recognizer = VoiceRecognizer()

# 初始化天气查询 API
weather_api_key = "your_weather_API_key"
weather_api_city_name = "your_city_name"
weather_api = WeatherAPI(weather_api_key, weather_api_city_name)

# 初始化欢迎语和道别语
welcome_message = "Welcome home!"
goodbye_message = "Goodbye, have a nice day!"

# 解析语音识别结果，并根据场景情况做出相应处理
def parse_voice_command(command, role):
    # 如果是主人，根据命令执行相关操作，并返回相应的回答信息
    if role == "owner":
        if "turn on light" in command:
            # TODO: 实现开灯的操作
            return "I'm turning on the light now."
        elif "play music" in command:
            # TODO: 实现播放音乐的操作
            return "What music do you want to listen to?"
        elif "stop" in command:
            # TODO: 实现停止当前操作的操作
            return "Ok, stopping now."
        else:
            return "Sorry, I don't understand."
    # 如果是访客或儿童，给出相应的提示信息
    else:
        if "light" in command or "music" in command:
            return "I'm sorry. Only the owner can operate the lights or music."
        else:
            return "Sorry, I don't understand."

# 主循环
cap = cv2.VideoCapture(0)
while True:
    # 从摄像头中读取图像，进行人脸识别并获取用户名
    ret, frame = cap.read()
    face_image, face_pos, face_size = face_recognizer.detect_face(frame)
    username = None
    if face_image is not None:
        username = voice_recognizer.recognize()
        if username:
            role = "guest"  # 如果只是访客，则默认为访客
            for user, user_role in users:
                if user == username:
                    role = user_role
                    break
            role_info = roles.get(role, {"greeting": "Hi! Welcome to our home.", "rules": "Please feel free to ask me anything."})
        else:
            role = "guest"
            role_info = roles.get(role, {"greeting": "Hi! Welcome to our home.", "rules": "Please feel free to ask me anything."})

        # 绘制人脸边框和显示欢迎语
        face_recognizer.draw_face_label(frame, role_info["greeting"], (face_pos, face_size))
        cv2.imshow("GPT pet", frame)

        # 从麦克风中读取声音数据，并进行语音识别
        command = voice_recognizer.recognize()

        # 如果有语音指令，则解析指令并执行相应操作
        if command:
            response = parse_voice_command(command, role)
            subprocess.call(f"espeak '{response}'", shell=True)
            time.sleep(2)

    # 按 Q 退出程序
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# 释放资源
cap.release()
cv2.destroyAllWindows()
voice_recognizer.close()

