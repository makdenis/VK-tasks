import datetime
import json
import random
import time
import math
from threading import Timer

from config import keyboard as kb
from config.db_config import db_session
from models.task_remind import Task_remind
from services import task_service, user_service, project_service
import webbrowser
from cryptography.fernet import Fernet

MAXINT = 9223372036854775807

timers = {}


def statistics(message, vk):
    cipher_suite = Fernet(b'MYVtGxQGE1GG3lZdtXezVO39SY8GtK_Ohs7P2k6gWqM=')
    id = cipher_suite.encrypt(str.encode(str(message.user_id)))
    id2 = cipher_suite.decrypt(id)
    url = 'http://127.0.0.1:5000/stat?id=' + str(id.decode("utf-8"))
    webbrowser.open(url, new=2)


def parse_date_msg(basedate):
    basedate = basedate.split(u' ')
    day = basedate[0]
    month = basedate[1]
    months = ['янв', 'фев', 'мар', 'апр', 'мая', 'июн', 'июл', 'авг', 'сен', 'окт', 'ноя', 'дек']
    month_prefix = month[0: 3]  # декабрь ->дек, дек -> дек
    if month_prefix in months:
        num = str(months.index(month_prefix) + 1)  # 11+1 -> '12'
        if len(num) < 2:
            num = '0' + num
    if month_prefix not in months:
        raise ValueError('Could not recognize provided month')
    if basedate[-1][0: 3] in months:
        time = '0.01'
    else:
        time = str(basedate[2]).replace(":", '.').replace("-", '.')
    date_line = str(day) + ' ' + str(num) + ' ' + str(datetime.date.today().year) + ' ' + time
    parse_date = datetime.datetime.strptime(date_line, "%d %m %Y %H.%M")
    return parse_date


def task(message, vk):
    text = vk.messages.getConversations()['items'][0]['last_message']['text']
    while (text == 'Добавить заданиe'):
        text = vk.messages.getConversations()['items'][0]['last_message']['text']
        time.sleep(0.2)
    print(text)
    name = vk.users.get(user_id=message.user_id)
    print(name[0])
    user = user_service.create_or_get_user(message.user_id, name[0]['first_name'] + name[0]['last_name'],
                                           name[0]['first_name'])
    task = task_service.create_task(message.user_id, text)
    task_service.create_category(task.id, message.user_id)
    task_service.create_date(task.id, message.user_id)
    task_service.create_user_id(task.id, message.user_id)

    vk.messages.send(user_id=message.user_id, message=u'Ваше задание добавлено',
                     random_id=random.randint(1, MAXINT))


def showtask(message, vk):
    try:
        user = user_service.find_one_by_id(message.user_id)
        user_tasks = task_service.find_tasks_by_user_id(user.get_id())

        tasks_to_show = [f'[{t.get_id()}] {t.get_description()}' for t in user_tasks]

        first_name = user.get_first_name()
        if 0 == len(tasks_to_show):
            vk.messages.send(user_id=message.user_id, message=f'{first_name}, you don\'t have any tasks yet',
                             random_id=random.randint(1, MAXINT))

        else:
            vk.messages.send(user_id=message.user_id,
                             message=first_name + ', here are your tasks:\n' + '\n'.join(tasks_to_show),
                             random_id=random.randint(1, MAXINT))

    except Exception as e:
        reply_on_error = f'Sorry, there were an error: {e}'
        vk.messages.send(user_id=message.user_id,
                         message=reply_on_error, random_id=random.randint(1, MAXINT)
                         )
        return


def select(message, vk):
    showtask(message, vk)
    vk.messages.send(user_id=message.user_id, message=u'Введите id задания',
                     random_id=random.randint(1, MAXINT))
    text = vk.messages.getConversations()['items'][0]['last_message']['text']
    while (text == 'Введите id задания'):
        text = vk.messages.getConversations()['items'][0]['last_message']['text']
        time.sleep(0.2)
    task = task_service.find_tasks_by_id(int(text))

    KEYBOARD_STEP_1 = kb.Keyboard.KEYBOARD_STEP_3
    keyboard = json.dumps(KEYBOARD_STEP_1, ensure_ascii=False).encode('utf-8')
    keyboard = str(keyboard.decode('utf-8'))
    vk.messages.send(user_id=message.user_id, message=u"Задание выбрано",
                     random_id=random.randint(1, MAXINT), keyboard=keyboard)
    text = vk.messages.getConversations()['items'][0]['last_message']['text']
    while (text == 'Задание выбрано'):
        text = vk.messages.getConversations()['items'][0]['last_message']['text']
        time.sleep(0.2)
    if text == 'Выполнено':
        delta = datetime.datetime.now() - task_service.get_date(task[0].id)
        print(int(delta.total_seconds() / 60) - 180)
        project_service.update_duration(str(task_service.get_category(task[0].id, message.user_id)),
                                        int(delta.total_seconds() / 60) - 180)
        task_service.delete_task(task[0].id)
    if text == 'Посмотреть сведения':
        category, create_date, next_remind_date, end_date = task_service.get_info(task[0].id, message.user_id)
        res = f'Категория: {category}\n' \
            f'Дата создания: {create_date}\n' \
            f'Дата напоминания: {next_remind_date}\n' \
            f'Дата окончания: {end_date}\n'
        vk.messages.send(user_id=message.user_id, message=res,
                         random_id=random.randint(1, MAXINT), keyboard=keyboard)
    if text == 'Удалить':
        task_service.delete_task(task[0].id)
    if text == 'Изменить текст':
        while (text == 'Изменить текст'):
            text = vk.messages.getConversations()['items'][0]['last_message']['text']
            time.sleep(0.2)
        task_service.update_text(task[0].id, text)
    if text == 'Добавить время окончания':
        while (text == 'Добавить время окончания'):
            text = vk.messages.getConversations()['items'][0]['last_message']['text']
            time.sleep(0.2)
        time1 = parse_date_msg(text)
        entity_by_id = task_service.create_end(task[0].id, message.user_id, time1)
    if text == 'Изменить врeмя напоминания':
        while (text == 'Изменить врeмя напоминания'):
            text = vk.messages.getConversations()['items'][0]['last_message']['text']
            time.sleep(0.2)
        # task_service.update_text(task[0].id, text)
        if timers.get(task[0].get_id()) is not None:
            timers[task[0].get_id()].cancel()
        notification_message = task[0].get_description()
        print(message.text.split(u' '))
        # time1 = message.text.split(u' ')[1]
        time1 = parse_date_msg(text)
        print(time1)
        reply_text = 'Notification not found'
        delta = time1 - datetime.datetime.now()
        entity_by_id = db_session.query(Task_remind).filter_by(task_id=task[0].id, user_id=message.user_id).update(
            {'next_remind_date': time1})
        db_session.commit()
        print(delta.total_seconds())
        seconds_till_notify = delta.total_seconds()
        if not notification_message:
            vk.messages.send(user_id=message.user_id,
                             message=reply_text,
                             random_id=random.randint(1, MAXINT))
            return

        context = [
            vk,
            message.user_id,
            notification_message
        ]
        print(context)
        try:
            vk.messages.send(user_id=message.user_id,
                             message='notification is added',
                             random_id=random.randint(1, MAXINT))

            seconds_as_int = int(seconds_till_notify)  # do not forget casting to float
            t = Timer(seconds_as_int, callback_notifier, context)
            timers['1'] = t
            t.start()
        except Exception as e:
            reply_text = 'There were an error: ' + str(e)

        else:
            reply_text = 'Notification has been set up'

        vk.messages.send(user_id=message.user_id,
                         message=reply_text,
                         random_id=random.randint(1, MAXINT))
    if text == 'Изменить кaтегорию':
        KEYBOARD_STEP_1 = kb.Keyboard.KEYBOARD_STEP_2

        keyboard = json.dumps(KEYBOARD_STEP_1, ensure_ascii=False).encode('utf-8')
        keyboard = str(keyboard.decode('utf-8'))
        vk.messages.send(user_id=message.user_id, message=u"Выберите кaтегорию",
                         random_id=random.randint(1, MAXINT), keyboard=keyboard)
        text = vk.messages.getConversations()['items'][0]['last_message']['text']
        while (text == 'Выберите кaтегорию'):
            text = vk.messages.getConversations()['items'][0]['last_message']['text']
            time.sleep(0.2)
        task_service.set_category(task[0].id, message.user_id, text)
        task_service.add_category(text, message.user_id)
    KEYBOARD_STEP_1 = kb.Keyboard.KEYBOARD_STEP_1
    keyboard = json.dumps(KEYBOARD_STEP_1, ensure_ascii=False).encode('utf-8')
    keyboard = str(keyboard.decode('utf-8'))
    vk.messages.send(user_id=message.user_id, message=u"Выберите действие",
                     random_id=random.randint(1, MAXINT), keyboard=keyboard)


def category(message, vk):
    KEYBOARD_STEP_1 = kb.Keyboard.KEYBOARD_STEP_2
    keyboard = json.dumps(KEYBOARD_STEP_1, ensure_ascii=False).encode('utf-8')
    keyboard = str(keyboard.decode('utf-8'))
    vk.messages.send(user_id=message.user_id, message=u"Выберите категорию",
                     random_id=random.randint(1, MAXINT), keyboard=keyboard)
    text = vk.messages.getConversations()['items'][0]['last_message']['text']
    while (text == 'Выберите категорию'):
        text = vk.messages.getConversations()['items'][0]['last_message']['text']
        time.sleep(0.2)

    task = task_service.find_nearest_task(message.user_id)

    task[0].set_category(text)
    task_service.change_category(message.user_id, task[0].id, text)
    # task_service.set_category(task.get_id(), text)
    task_service.add_category(text, message.user_id)
    KEYBOARD_STEP_1 = kb.Keyboard.KEYBOARD_STEP_1

    keyboard = json.dumps(KEYBOARD_STEP_1, ensure_ascii=False).encode('utf-8')
    keyboard = str(keyboard.decode('utf-8'))
    stat = task_service.get_stat(text, message.user_id)
    data_names = []
    categories = []
    # user_id = 80148422
    all_stat = task_service.get_remind(message.user_id)
    for i in all_stat:
        if i.Task_remind.next_remind_date is not None and i.Task.user_id == message.user_id:
            a = math.fabs((i.Task_remind.next_remind_date - datetime.datetime.now()).days)
            if a < 1:
                data_names.append(i.Task.description)
                categories.append(i.Category.category)
    # TODO брать из даты время, складыаать, считать протяженность
    data_values = []
    for i in categories:
        data_values.append(project_service.find_duration(i, message.user_id))
    tm = sum(data_values)
    if tm > 540:
        vk.messages.send(user_id=message.user_id,
                         message=u"Внимание! Выможете не успеть выполнить все задачи на сегодня ",
                         random_id=random.randint(1, MAXINT), keyboard=keyboard)
    if len(stat) > 0 and stat[0].duration:
        vk.messages.send(user_id=message.user_id,
                         message=u"Категория добавлена " + "По статистике выполнение задания займет " + str(
                             stat[0].duration / stat[0].tasks) + " часа",
                         random_id=random.randint(1, MAXINT), keyboard=keyboard)
    else:
        vk.messages.send(user_id=message.user_id,
                         message=u"Категория добавлена",
                         random_id=random.randint(1, MAXINT), keyboard=keyboard)


def entertime(message, vk):
    text = vk.messages.getConversations()['items'][0]['last_message']['text']
    while (text == 'Добавить время'):
        text = vk.messages.getConversations()['items'][0]['last_message']['text']
        time.sleep(0.2)
    name = vk.users.get(user_id=message.user_id)
    task = task_service.find_nearest_task(message.user_id)

    notification_message = task.Task.description
    print(message.text.split(u' '))
    # time1 = message.text.split(u' ')[1]
    time1 = parse_date_msg(text)
    print(time1)
    reply_text = 'Notification not found'
    delta = time1 - datetime.datetime.now()
    entity_by_id = task_service.create_remind(task.Task.id, message.user_id, time1)

    print(delta.total_seconds())
    seconds_till_notify = delta.total_seconds()
    if not notification_message:
        vk.messages.send(user_id=message.user_id,
                         message=reply_text,
                         random_id=random.randint(1, MAXINT))
        return

    context = [
        vk,
        message.user_id,
        notification_message
    ]
    print(context)
    try:
        vk.messages.send(user_id=message.user_id,
                         message='notification is added',
                         random_id=random.randint(1, MAXINT))

        seconds_as_int = int(seconds_till_notify)  # do not forget casting to float
        t = Timer(seconds_as_int, callback_notifier, context)
        timers[task.Task.id] = t
        t.start()
    except Exception as e:
        reply_text = 'There were an error: ' + str(e)

    else:
        reply_text = 'Notification has been set up'

    vk.messages.send(user_id=message.user_id,
                     message=reply_text,
                     random_id=random.randint(1, MAXINT))


def callback_notifier(*context):
    print(context)
    vk = context[0]
    chat_id = context[1]
    message = context[2]

    vk.messages.send(user_id=chat_id,
                     message=message,
                     random_id=random.randint(1, MAXINT))
