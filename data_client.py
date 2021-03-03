# Программа сервера для отправки приветствия сервера и получения ответа
from socket import *
from click import command, option
from datetime import datetime

import json
from jim import Jim

CODE = 'utf-8'


@command()
@option('-a', default='localhost', help='< addr > — IP-адрес для прослушивания \
    (по умолчанию слушает все доступные адреса)')
@option('-p', default=7780, help='< port > — TCP-порт для работы(по умолчанию использует 7777)')
def run_process(a=None, p=None):
    MessengerClient((a, p), 'vladimr', '123456').processing_action(
        'action:presence', 'I`m here', datetime.now().timestamp())


class MessengerClient:

    def __init__(self, addr_port, username, password):
        self.username = username
        self.password = password

        self.__socket = None
        self.timeout = 3
        self.addr_port = addr_port

    def processing_action(self, method,  msg=''):
        # Обработка действия

        data = self.get_data(method,  msg)
        # Отправка пакета данных на сервер
        if self.__connection:
            received_message = self.send_msg(data)
            if received_message:
                # TO DO: Процедура обрабработки полученного сообщения
                bite_cnd = len(received_message.encode(CODE))
                print(
                    f'Сообщение от сервера:{received_message}. Длина сообщения {bite_cnd} байт')
            self.__close()

    def get_data(self, method, msg=''):
        # Формирования пакета данных
        if method == 'action:presence':
            # присутствие. Сервисное сообщение для извещения сервера о присутствии клиента online
            return Jim(self.username, self.password).presence(msg)
        elif method == 'action:prоbe':
            # проверка присутствия. Сервисное сообщение от сервера для проверки присутствии клиента online
            pass
        elif method == 'action:msg':
            # простое сообщение пользователю или в чат
            return msg
        elif method == 'action:quit':
            # отключение от сервера
            pass
        elif method == 'action:authenticate':
            # авторизация на сервере
            pass
        elif method == 'action:join':
            # присоединиться к чату
            pass
        elif method == 'action:leave':
            # покинуть чат.
            pass
        return msg

    def send_msg(self, msg):

        try:
            self.__socket.send(json.dumps(msg).encode(CODE))
            data = self.__socket.recv(10000000)
        except Exception as err:
            print(f'Сообщение {msg} на север не было отправлено ошибка:{err}')
            self.__socket = None
            return None

        received_message = data.decode(CODE)

        return received_message

    def __close(self):
        try:
            self.__socket.close()
        except:
            print('Ошибка закрытие соединения к сервером')
            return False
        return True

    @property
    def __connection(self):
        try:
            self.__socket = socket(AF_INET, SOCK_STREAM)
            self.__socket.connect(self.addr_port)
        except:
            self.__socket = None
            print('Ошибка соедения к сервером')
            return False
        return True

    # @property
    # def run_process(self):
    #     msg = None
    #     con_try_cnt = 0  # Колличество попыток

    #     while True:
    #         if not msg:  # если требуется запросить у пользователя сообщение
    #             msg = input('Enter message or "Q":')
    #         elif msg == "Q":  # Если выход
    #             break
    #         else:
    #             # Решил пока упростить закрывая каждый раз сокет, пока не разбирусь
    #             if self.__connection and self.send(msg):
    #                 msg = None
    #                 self.__close
    #             elif con_try_cnt < 2:  # 2 попытки с паузой
    #                 if con_try_cnt == 1:
    #                     time.sleep(self.timeout)
    #                 con_try_cnt = 0 if self.__connection else con_try_cnt + 1
    #             else:
    #                 msg = None  # Очищаем сообщение для отправки, и повторяем вопрос
    #                 con_try_cnt = 0

    #     self.__socket.close()


if __name__ == "__main__":
    run_process()
