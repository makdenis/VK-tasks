import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from utils.service_utils import  find_all
import math
import datetime
from models.project import Project
from models.task import Task
from services import task_service, user_service, project_service
def pie():
    data_names=[]
    all_stat = find_all(Project)
    for i in all_stat:
        data_names.append(i.title)

    data_values = []
    for i in data_names:

        data_values.append(len(task_service.find_tasks_by_category(i)))
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
    fig.savefig('pie.png')

def day():
    data_names = []
    categories=[]
    all_stat = find_all(Task)
    a=datetime.datetime.now().timetuple().tm_yday-1
    b=datetime.datetime.now().timetuple().tm_yday+1
    for i in all_stat:
        if i.next_remind_date is not None:
            a=math.fabs((i.next_remind_date-datetime.datetime.now()).days)
            if a<1:
                data_names.append(i.description)
                categories.append(i.category)

    data_values = []
    for i in categories:
        data_values.append(project_service.find_duration(i))
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
    fig.savefig('day.png')