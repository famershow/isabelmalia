
import requests
import json

class WeatherAPI:
    def __init__(self, api_key, city_name):
        self.api_key = api_key
        self.city_name = city_name
        self.base_url = "https://api.openweathermap.org/data/2.5/weather"

    # 查询天气情况，返回相应结构化数据
    def get_data(self):
        url = self.base_url + f"?q={self.city_name}&appid={self.api_key}"
        response = requests.get(url)
        data = json.loads(response.text)
        return data

    # 根据天气情况提醒主人应该做什么
    def get_advice(self, weather_data):
        temp = weather_data["main"]["temp"] - 273.15  # 温度：开尔文转摄氏度
        description = weather_data["weather"][0]["description"]  # 天气描述
        advice = f"The temperature is {temp:.1f}℃, and the weather is {description}."
        # TODO: 根据天气情况生成相应建议
        return advice
    
    