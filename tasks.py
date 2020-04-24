#set FORKED_BY_MULTIPROCESSING=1 && celery -A tasks worker --loglevel=info ------not work
#pip install eventlet
#pip install pyopenssl==19.1.0
#celery -A <mymodule> worker -l info -P eventlet
# set FORKED_BY_MULTIPROCESSING=1 && celery -A tasks worker -l info -P eventlet
# celery -A tasks beat - запускает расписание и посылает celery tasks которые заданы в @celery_app.on_after_configure.connect
# celery -A tasks beat - запускается отдельным процессом


from celery import Celery
from celery.schedules import crontab
from app import create_app
from app.news.parsers import habr

flask_app = create_app()
celery_app = Celery("tasks", broker="redis://localhost:6379/0")


@celery_app.task
def news_titles():
    with flask_app.app_context():
        habr.get_habr_snippets()
   
@celery_app.task
def news_content():
    with flask_app.app_context():
        habr.get_habr_content()

# расписание
# через sender управляем celery
# каждую минуту и вторую минуту будут выполняться задачи по сбору заголовков
# news_titles.s() - сигнатура функции говорит что мы будем вызывать ее
@celery_app.on_after_configure.connect
def setup_period_tasks(sender, **kwargs):
    sender.add_periodic_task(crontab(minute="*/1"), news_titles.s())
    sender.add_periodic_task(crontab(minute="*/2"), news_content.s())