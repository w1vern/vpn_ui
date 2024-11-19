import requests
from test_config import login, password



url = "http://94.131.112.203/my-fckng-panel/"
default_path = "panel/api/inbounds/"

import requests
from test_config import login, password

class SessionManager:
    def __init__(self, base_url, login_endpoint, username, password):
        self.base_url = base_url
        self.login_endpoint = login_endpoint
        self.username = username
        self.password = password
        self.session = None  # Сессия инициализируется как None, чтобы создать её при первом вызове

    def get_session(self):
        # Если сессия отсутствует или авторизация не прошла, создаём новую сессию и логинимся
        if self.session is None or not self._is_authenticated():
            self._login()
        return self.session

    def _login(self):
        # Создаём новую сессию
        self.session = requests.Session()
        
        # Отправляем POST-запрос для авторизации
        auth_response = self.session.post(
            f"{self.base_url}{self.login_endpoint}",
            json={'username': self.username, 'password': self.password}
        )
        
        # Проверяем успешность авторизации
        if auth_response.status_code == 200:
            print("Авторизация успешна!")
        else:
            print("Ошибка авторизации!")
            print("Код статуса:", auth_response.status_code)
            print("Ответ:", auth_response.text)
            # Если авторизация не удалась, удаляем сессию
            self.session = None

    def _is_authenticated(self):
        # Метод для проверки авторизации. Можно отправить запрос для проверки состояния сессии.
        # Здесь предполагаем, что сервер вернёт 401 (Unauthorized), если сессия недействительна
        response = self.session.get(f"{self.base_url}panel/api/inbounds/list")
        return response.status_code != 401  # Если статус не 401, то сессия активна

    def make_request(self, method, endpoint, **kwargs):
        # Получаем активную сессию
        session = self.get_session()
        
        # Формируем полный URL
        url = f"{self.base_url}{endpoint}"
        
        # Отправляем запрос с нужным методом (GET, POST и т.д.)
        response = session.request(method, url, **kwargs)
        
        # Проверяем успешность и возвращаем ответ
        if response.status_code == 200:
            try:
                return response.json()
            except requests.exceptions.JSONDecodeError:
                print("Ошибка: Ответ не в формате JSON")
                return response.text
        else:
            print(f"Ошибка: Код статуса {response.status_code}")
            return response.text

# Пример использования:
if __name__ == "__main__":
    base_url = "http://94.131.112.203/my-fckng-panel/"
    login_endpoint = "login"

    session_manager = SessionManager(base_url, login_endpoint, login, password)
    
    # Пример GET-запроса на получение списка инбоундов
    response = session_manager.make_request("GET", "panel/api/inbounds/list")
    print(response)


# Создаем сессию для сохранения состояния авторизации
session = requests.Session()

# Отправляем запрос на авторизацию
auth_response = session.post(url + "login", json={"username": login, "password": password})

# Проверяем успешность авторизации
if auth_response.status_code == 200:
    # Получаем список инбоундов
    response = session.get(url + default_path + "list")
    
    # Проверяем, действительно ли ответ в формате JSON
    try:
        print(response.json())
    except requests.exceptions.JSONDecodeError:
        print("Ошибка: Сервер вернул ответ не в формате JSON")
        print("Ответ сервера:", response.text)
else:
    print("Ошибка авторизации. Код статуса:", auth_response.status_code)
    print("Ответ:", auth_response.text)
