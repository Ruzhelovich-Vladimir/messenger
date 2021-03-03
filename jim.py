'''
    работа с протоколом JIM
'''
from datetime import datetime

MSG_CODE_LST = {
    100: 'базовое уведомление',
    101: 'важное уведомление.',
    200: 'OK',
    201: '(created) — объект создан',
    202: '(accepted) — подтверждение',
    400: 'неправильный запрос/JSON-объект',
    401: 'не авторизован',
    402: 'неправильный логин/пароль',
    403: '(forbidden) — пользователь заблокирован',
    404: '(not found) — пользователь/чат отсутствует на сервере',
    409: '(conflict) — уже имеется подключение с указанным логином',
    410: '(gone) — адресат существует, но недоступен(offline)',
    500: 'ошибка сервера'
}

MSG_GROUP_LST = {
    1: 'информационные сообщения',
    2: 'успешное завершение',
    4: 'ошибка на стороне клиента',
    5: 'ошибка на стороне сервера'
}


class Jim:

    def __init__(self, account_name, password, action_time=datetime.now().timestamp()):

        self.account_name = account_name
        self.password = password
        self.action_time = action_time

    def __get_msg(self, code):

        if code in MSG_CODE_LST:
            return MSG_CODE_LST[code]
        if code//100 in MSG_GROUP_LST:
            return MSG_GROUP_LST[code//100]
        return 'неизвестная ошибка'

    @property
    def get_auth(self):
        # Авторизация
        return {
            "action": "authenticate",
            "time": self.action_time,
            "user": {
                "account_name": self.account_name,
                "password": self.password
            }
        }

    def presence(self, type='Yep, I am here!'):
        # Статус
        return{
            "action": "presence",
            "time": self.action_time,
            "type": 'status',
            "user": {
                "account_name": self.account_name,
                "status": type
            }
        }

    def probe_request_from_server(self):
        # Состояние
        return {
            "action": "probe",
            "time": self.action_time,
        }

    def request(self, to_account_name, message, encoding='utf-8'):
        # Запрос
        return {
            "action": "msg",
            "time": self.action_time,
            "to": to_account_name,
            "from": self.account_name,
            "encoding": encoding,
            "message": message
        }

    def response(self, code):
        # Ответ
        key_msg = 'alert' if code < 300 else 'error'
        return {
            "response": code,
            "time": datetime.now().timestamp(),
            key_msg: self.__get_msg(code)
        }

    @property
    def quit(self):
        # Выхода
        return {
            "action": "quit"
        }


if __name__ == '__main__':
    res_json = Jim('test', 'password').get_auth
    print(res_json)
