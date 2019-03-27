from config.db_config import db_session
from models.project import Project
from models.task import Task
from services import task_service, user_service
from utils.message_parser import message_parser
from utils.service_utils import save, flush, find_all, find_one_by_id


def find_all_by_user_id(user_id):
    projects = find_all(Project)
    projects_by_user = [p for p in projects if user_id == p.get_user_id()]
    return projects_by_user


def find_duration(category, user):
    projects = find_all(Project)
    res = [p for p in projects if p.title == category and p.user_id == user]
    return res[0].duration


def create_or_get_project(message, user_id):
    # TODO somehow find out message's category
    title = message_parser.parse_message_for_project(message)

    projects_of_user = find_all_by_user_id(user_id)
    # check if theres already a project with same title(category)
    for p in projects_of_user:
        if title == p.get_title():
            return p

    # there is no project with this title -> create new
    new_proj = flush(Project(title, user_id))
    saved_proj = save(new_proj)
    return saved_proj


def update_duration(category, dur):
    entity_by_id = db_session.query(Project).filter_by(title=category)
    if entity_by_id[0].duration:
        dur = dur + entity_by_id[0].duration
    if entity_by_id[0].tasks:
        amount = entity_by_id[0].tasks
    else:
        amount = 0
    db_session.query(Project).filter_by(title=category).update({'duration': dur})
    db_session.query(Project).filter_by(title=category).update({'tasks': amount + 1})
    db_session.commit()


def update_nearest_task_for_project(project_id_value):
    project_id = int(project_id_value)
    project = find_one_by_id(project_id, Project)

    if project:
        all_tasks = find_all(Task)
        tasks_by_project_id = [t for t in all_tasks
                               if t.get_project_id() == project_id and t.get_next_remind_date() is not None]
        sorted_by_next_remind_date = sorted(tasks_by_project_id, key=lambda t: t.get_next_remind_date())

        if 0 != len(sorted_by_next_remind_date):
            nearest_task = sorted_by_next_remind_date[0]
            project.set_next_task_id(nearest_task)

            saved_proj = save(project)
            return saved_proj

        else:
            return project
