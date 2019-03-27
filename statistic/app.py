from flask import Flask, render_template, request, url_for
import os
from flask import request
from config.db_config import init_db
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from utils.service_utils import find_all
import math
import datetime
from models.project import Project
from models.category import Category
from models.task_remind import Task_remind
from services import task_service, user_service, project_service
import plotly.plotly as py
import plotly.figure_factory as ff
import plotly.io as pio
from datetime import timedelta
from flask import send_file


def pie(user_id):
    # print(user_id)
    data_names = []
    # user_id = 80148422
    data_values = []
    all_stat = find_all(Category)
    for i in all_stat:
        if i.user_id == user_id:
            if i.category not in data_names:
                data_names.append(i.category)
                data_values.append(len(task_service.find_tasks_by_category(i.task_id)))

    dpi = 80
    fig = plt.figure(dpi=dpi, figsize=(512 / dpi, 384 / dpi))
    mpl.rcParams.update({'font.size': 9})

    plt.title('Распределение по категориям (%)')

    xs = range(len(data_names))

    plt.pie(
        data_values, autopct='%.1f', radius=1.1,
        explode=[0.15] + [0 for _ in range(len(data_names) - 1)])
    plt.legend(
        bbox_to_anchor=(-0.16, 0.45, 0.25, 0.25),
        loc='lower left', labels=data_names)
    fig.savefig(f'static/plots/{user_id}_pie.png')


def day(user_id):
    data_names = []
    categories = []
    flag = False
    # user_id = 80148422
    all_stat = task_service.get_remind(user_id)
    for i in all_stat:
        if i.Task_remind.next_remind_date is not None and i.Task.user_id == user_id:
            a = math.fabs((i.Task_remind.next_remind_date - datetime.datetime.now()).days)
            if a < 1:
                data_names.append(i.Task.description)
                categories.append(i.Category.category)
    # TODO брать из даты время, складыаать, считать протяженность
    data_values = []
    for i in categories:
        data_values.append(project_service.find_duration(i, user_id))
    time = sum(data_values)
    if time > 540:
        flag = True
    dpi = 80
    fig = plt.figure(dpi=dpi, figsize=(512 / dpi, 384 / dpi))
    mpl.rcParams.update({'font.size': 9})

    plt.title('Распределение по времени за день (%)')

    xs = range(len(data_names))

    plt.pie(
        data_values, autopct='%.1f', radius=1.1,
        explode=[0.15] + [0 for _ in range(len(data_names) - 1)])
    plt.legend(
        bbox_to_anchor=(-0.16, 0.45, 0.25, 0.25),
        loc='lower left', labels=data_names)
    fig.savefig(f'static/plots/{user_id}_day.png')
    return flag


def gant(user_id):
    stat = task_service.get_gant()
    df = []
    # user_id = 80148422
    for i in stat:
        if i.Task.user_id == user_id:
            # TODO сделать энд дате
            if task_service.get_end(i.Task.id, user_id) == False:
                finish = task_service.get_stat(i.Category.category, user_id)
                df.append(dict(Task=i.Task.description, Start=str(i.Task_remind.next_remind_date),
                               Finish=str(i.Task_remind.next_remind_date + timedelta(minutes=finish[0].duration))))
            else:
                df.append(dict(Task=i.Task.description, Start=str(i.Task_remind.next_remind_date),
                               Finish=str(task_service.get_end(i.Task.id, user_id))))

    fig = ff.create_gantt(df)

    pio.write_image(fig, f'./static/plots/{user_id}_gant.jpeg')


app = Flask(__name__)
plots = os.path.join('static', 'plots')
app.config['UPLOAD_FOLDER'] = plots

@app.after_request
def add_header(response):
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.route('/stat')
def hello_world():
    from cryptography.fernet import Fernet
    cipher_suite = Fernet(b'MYVtGxQGE1GG3lZdtXezVO39SY8GtK_Ohs7P2k6gWqM=')
    id = cipher_suite.decrypt(str.encode(request.args.get('id')))
    user_id = int(id.decode("utf-8"))
    init_db()
    pie(user_id)
    gant(user_id)
    flag = day(user_id)

    full_filename = os.path.join(app.config['UPLOAD_FOLDER'], f'{user_id}_pie.png')
    full_filename2 = os.path.join(app.config['UPLOAD_FOLDER'], f'{user_id}_gant.jpeg')
    full_filename3 = os.path.join(app.config['UPLOAD_FOLDER'], f'{user_id}_day.png')
    if flag:
        return render_template("index.html", user_image1=full_filename, user_image2=full_filename2,
                               user_image3=full_filename3, text="Внимание, вы можете не успеть выполнить все задания!")
    else:
        return render_template("index.html", user_image1=full_filename, user_image2=full_filename2,
                               user_image3=full_filename3)


if __name__ == '__main__':
    app.run()
