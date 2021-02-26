# Программа сервера для получения приветствия от клиента и отправки ответа
from contextlib import closing, nullcontext
import json
from socket import *
from click.decorators import command, option

from jim import jim

CODE = 'utf-8'


@command()
@option('-a', default='', help='< addr > — IP-адрес для прослушивания \
    (по умолчанию слушает все доступные адреса)')
@option('-p', default=7780, help='< port > — TCP-порт для работы(по умолчанию использует 7777)')
def run_process(a=None, p=None):
    MessengerServer((a, p))


class MessengerServer:

    def __init__(self, host):

        with socket(AF_INET, SOCK_STREAM) as self.__socket:  # Создает сокет TCP
            self.__socket.bind(host)  # Присваивает порт 8007
            self.__socket.listen()  # Слушаем порт
            self.__run_processing  # Обрабатываем сообщения

    @property
    def __run_processing(self):

        while True:
            client, addr = self.__socket.accept()
            # with closing(client) as cl:
            self.__process_client(client, addr)

    def __process_client(self, client, addr):

        data = client.recv(1000000)
        print(
            f'Сообщение: {data.decode(CODE)} было отправлено клиентом: {addr}')
        data = json.loads(data)
        msg = self.__get_message(data)
        if msg:
            client.send(msg.encode(CODE))

    @staticmethod
    def __get_message(data):

        method = data['action']
        if method == 'presence':
            # присутствие. Сервисное сообщение для извещения сервера о присутствии клиента online
            return 'сервер получил статус ваше присутствия'
        elif method == 'prоbe':
            # проверка присутствия. Сервисное сообщение от сервера для проверки присутствии клиента online
            pass
        elif method == 'msg':
            # простое сообщение пользователю или в чат
            pass
        elif method == 'quit':
            # отключение от сервера
            pass
        elif method == 'authenticate':
            # авторизация на сервере
            pass
        elif method == 'join':
            # присоединиться к чату
            pass
        elif method == 'leave':
            # покинуть чат.
            pass
        return None


if __name__ == '__main__':
    run_process()
