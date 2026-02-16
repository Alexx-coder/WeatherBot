import requests

class WeatherBotError(Exception):
    def __init__(self, message="Возникла ошибка."):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"{self.message}"

class CityError(WeatherBotError):
    def __init__(self):
        super().__init__("Не найден город.")

class URLError(WeatherBotError):
    def __init__(self):
        super().__init__("Не найден URL-адрес.")

class WeatherBot:
    def __init__(self, api_key):
        self.name = "Weather Bot"
        self.version = "v2.0"
        self.base_url = "https://api.weatherapi.com/v1/current.json"
        self.API_key = api_key
    
    def weather_bot(self):
        while True:
            try:
                city = input("Введите город: ").strip()
                if not city:
                    continue

                params = {
                    "key": self.API_key,
                    "q": city,
                    "lang": "ru"
                }

                response = requests.get(self.base_url, params=params)
                data = response.json()

                if "error" in data:
                    if data["error"]["code"] == 1006:
                        raise CityError()
                    else:
                        raise WeatherBotError(data["error"]["message"])

                print(f"Погода в {data['location']['name']}:")
                print(f"Температура: {data['current']['temp_c']} градусов C")
                print(f"Состояние: {data['current']['condition']['text']}")
                print(f"Влажность: {data['current']['humidity']}%")
                print(f"Ветер: {data['current']['wind_kph']} км/ч")
                
            
                go = input("Продолжить: ").strip().lower()
                if go == "да":
                    print("Продолжаю...")
                    continue
                elif go == "нет":
                    print("Заканчиваю...")
                    return False
                else:
                    print("Ваш ответ не понятен. Повторите попытку")
                    continue
                    

            except CityError as e:
                print(e)
                continue
            except requests.exceptions.ConnectionError:
                print(URLError())
                return False
            except KeyError:
                print("Ошибка ключа API.")
                return False
            except KeyboardInterrupt:
                print("Остановлено.")
                break
            except Exception as e:
                print(f"Ошибка: {e}")
                continue

if __name__ == "__main__":
    api_key = "Not real API-KEY" 
    
    try:
        app = WeatherBot(api_key)
        app.weather_bot()
    except Exception:
        pass
    finally:

        print("Weather Bot завершает свою работу! До свидания!")
