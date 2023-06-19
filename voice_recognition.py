
import pyaudio
import wave
import speech_recognition as sr

class VoiceRecognizer:
    def __init__(self):
        self.r = sr.Recognizer()
        self.audio = pyaudio.PyAudio()
        self.stream = self.audio.open(format=pyaudio.paInt16, channels=1, rate=16000,
                                      input=True, frames_per_buffer=1024)

    # 从麦克风中读取声音数据，并进行语音识别
    def recognize(self):
        data = self.stream.read(1024, exception_on_overflow=False)
        try:
            text = self.r.recognize_google(data)
            return text
        except:
            return ""

    # 关闭资源
    def close(self):
        self.stream.stop_stream()
        self.stream.close()
        self.audio.terminate()



        