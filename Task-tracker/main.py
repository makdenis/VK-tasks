import vk_api
from vk_api import VkUpload
from vk_api.longpoll import VkLongPoll, VkEventType
import requests
from handlers.task_handler import parse_date_msg
from config.db_config import init_db
from services import task_service, user_service, project_service
import random
import json
import handlers
from config import keyboard as kb

MAXINT = 9223372036854775807


class VKBot:
    """
    VKBot object
    """
    vk = 0
    vk_session = 0
    session = 0
    upload = 0
    long_poll = 0
    event = 0

    def __init__(self, log=None, passwd=None, token=None):
        """
        Run authorization methods.
        To choose login type enter token or your login and password.
        How to get token: https://vk.com/dev/bots_docs
        :param log: your VK.com login
        :param passwd: your VK.com passsword
        :param token: your community token
        """
        if token:
            self.vk_session = vk_api.VkApi(token=token)
        else:
            self.vk_session = vk_api.VkApi(log, passwd)
            try:
                self.vk_session.auth()
            except vk_api.AuthError as error_msg:
                print(error_msg)
                return
        self.vk = self.vk_session.get_api()
        self.session = requests.session()
        self.upload = VkUpload(self.vk_session)
        self.long_poll = VkLongPoll(self.vk_session)

    def __command_handler__(self, commands, handler):
        """
        Run user function if message contain a commands
        :param commands: list of command. For example ["command1", "command2", ...]
        :param handler: function, that should run if message contain a command
        """
        message_set = self.event.text.split(u' ')
        for command in commands:
            if command in message_set:
                handler(self.event, self.vk)
                break

    def __query_manager__(self, queryset):
        """
        Sets a query of commands and handlers
        :param queryset: list of commands and hanlers. For example [["command", handler], ...]
        """
        for item in queryset:
            self.__command_handler__(item[0], item[1])

    def run(self, query):
        """
        Main bot`s cycle.
        :param query: list of commands and hanlers. For example [["command", handler], ...]
        """
        for event in self.long_poll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                self.event = event
                self.__query_manager__(query)


def start(message, vk):
    name = vk.users.get(user_id=message.user_id)
    print(name[0])
    user = user_service.create_or_get_user(message.user_id, name[0]['first_name'] + name[0]['last_name'],
                                           name[0]['first_name'])
    KEYBOARD_STEP_1 = kb.Keyboard.KEYBOARD_STEP_1

    keyboard = json.dumps(KEYBOARD_STEP_1, ensure_ascii=False).encode('utf-8')
    keyboard = str(keyboard.decode('utf-8'))
    vk.messages.send(user_id=message.user_id, message=u"Здравствуйте. Выберите действие",
                     random_id=random.randint(1, MAXINT), keyboard=keyboard)


if __name__ == '__main__':
    queryset = [[[u"время"], handlers.task_handler.entertime], [[u"заданиe"], handlers.task_handler.task],
                [[u"Начать"], start], [[u"задания"], handlers.task_handler.showtask],
                [[u"категорию"], handlers.task_handler.category], [[u"Выбрать"], handlers.task_handler.select],
                [[u"статистику"], handlers.task_handler.statistics]]
    init_db()

    # if you want use bot by community token
    bot = VKBot(token='87938395826ec8f170fe180afe194d30f364d713b681c84f4d7f8aae42e3e896858f2da9c98d1e3d5e2ab')
    bot.run(query=queryset)
